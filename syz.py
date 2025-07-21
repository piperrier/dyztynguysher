import subprocess
import os
import re
import shutil
import numpy as np
import queue
import threading

from utils import DEFAULT_IDIR, DEFAULT_WDIR, bcolors
from goppa import *
from matrix_bin import *
from koszul import *
from conditioning import *

import sage.coding.codes_catalog

from sage.plot.matrix_plot import matrix_plot
from sage.functions.other import binomial
from sage.matrix.constructor import matrix
from sage.misc.functional import log
from sage.modules.free_module_element import vector


class Instance:
    """The class representing the instance we try to solve.
    
    Attributes:
        * Code parameters
        name (str): the name of the code.
        n_code (int): the length of the code.
        k_code (int): the dimension of the code.
        r (int): the betti number to compute betti_r_r+1

        * Wiedemann parameters
        m (str): size of the left block
        n (str): size of the right block
        thr (str): number of threads on which you run cado-nfs/bwc

        * Matrix system and sol
        code_matrix (sage.matrix): the generating matrix of the code
        nrows (int): the number of rows of the "raw" system matrix
        ncols (int): the number of columns of the "raw" system matrix
        self.S (ndarray of uint32-ndarray): the sparse representation of the system matrix, only use this with light matrices (cf self.construct_and_collect_matrix)

        * dir/wdir
        dir (str): absolute path to the directory where we construct the matrix and eventually put the kernel vectors
        wdir (str): absolute path to the directory where cado nfs work, should be fast in I/O, everything is deleted at the end of the running time 

    """
    def __init__(self, name, n_code, k_code, r, m, n, threads, idir=DEFAULT_IDIR, wdir=DEFAULT_WDIR):
        """Initializes the Instance with the given parameters.

        Args:
            name (str): name of the code in lower case, eg: hamming, goppa.
            n_code(int): size of the code.
            k_code(int): dimension of the code.
            r(int): compute betti_r_r+1
            m,n(str): a multiple of 64 declared as an str, the m and n of block wiedemann, eg m = "128" and n ="64"
            threads(str): number of threads you use, if your machine has 12 threads, threads = "3x4"
            dir(str) : absolute path to the directory where we construct the matrix and eventually put the kernel vectors
            wdir(str): absolute path to the directory where cado nfs work, should be fast in I/O, everything is deleted at the end of the running time 
        """

        # code parameters
        self.name = name
        self.n_code = n_code
        self.k_code = k_code
        self.r = r #betti_r_r+1
        
        # wiedemann parameters
        self.m = m
        self.n = n
        self.thr = threads

        # matrix system and sol
        self.code_matrix = None
        self.nrows = binomial(self.k_code,self.r+1) * self.r + binomial(self.k_code,self.r) * self.r # dim of cokernel
        self.ncols = self.n_code * binomial(self.k_code,self.r-1) # dim of arrival space
        self.S = None #S is a ndarray of ndarray, best for speed and memory usage, for very large matrix we don't construct it, and prefer to write it in memory
        # self.ker = None

        # idir / wdir
        self.idir = idir + "/" + f"{self.name}_{self.n_code}_{self.k_code}_b{self.r}_{self.r + 1}"
        self.wdir = wdir # on some lame.enst.fr machine : "/nvme/pperrier-22/wdir"
    
        if not os.path.exists(self.idir):
            os.makedirs(self.idir)
        
        if not os.path.exists(self.wdir):
            os.makedirs(self.wdir)
    
    
    def __repr__(self):
        density = self.density()

        row_red=self.nrows-self.r*binomial(self.k_code, self.r)
        col_red=self.ncols - self.k_code*binomial(self.k_code, self.r-1)
        space_red = (row_red * col_red * density + row_red)*4*10**-9        

        return f"{self.name}_{self.n_code}_{self.k_code}_b{self.r}_{self.r + 1}:\n\
        m={self.m} n={self.n}\n\
        thr={self.thr}\n\
        nrows={self.nrows} ncols={self.ncols} row_red={self.r*binomial(self.k_code, self.r)} col_red={self.k_code*binomial(self.k_code, self.r-1)}\n\
        density={round(density*100,5)}% weight={self.ncols * self.nrows * density:.0f} space={(self.ncols * self.nrows * density + self.nrows)*4*10**-9:.3f}Gb spacered={space_red}\n\
        idir={self.idir} wdir={self.wdir}"


    def complexity(self):
        """
        Approximate complexity of the block wiedemann algorithm
        """
        n, m = float(self.n), float(self.m)
        logcol = float(log(self.ncols))

        print((f"matrix: space={(self.ncols * self.nrows * self.density() + self.nrows)*4*10**-9}Gb\n"
        f"krylov & mksol: matrix-times-vector products={(1 + n/m + 64/n)*self.ncols:.2E}\n"
        f"lingen: time={(m+n)*self.ncols*logcol*(m+n+logcol):.2E} space={(m+n)*self.ncols:.2E}"))
        


    def pretty(self, conditioning=ConditioningType.RAW, dpi=200):
        """
        Plot and print the matrix.
        The matrix should be written in a .bin file before calling this function !
        """
        print(self)
        print("\n")
        
        matrix_file, _ = self.get_files_names(conditioning)

        match conditioning:
            case ConditioningType.RAW:
                nrows, ncols = Raw.get_dim(self.nrows, self.ncols)

            case ConditioningType.RAWPAD:
                nrows, ncols = RawPad.get_dim(self.nrows, self.ncols)

            case ConditioningType.RED:
                nrows, ncols = Red.get_dim(self.nrows, self.ncols, self.k_code, self.r)

            case ConditioningType.REDPAD:
                nrows, ncols = RedPad.get_dim(self.nrows, self.ncols, self.k_code, self.r)
            
        matrix = sage_from_bin(self.idir, matrix_file, nrows, ncols)
        
        P = matrix_plot(matrix, marker=',')
        P.show(dpi=dpi, axes_pad=0,fontsize=3)


    def get_files_names(self, conditioning: ConditioningType) -> tuple[str,str]:
        matrix_name = "S" + conditioning.value
        solution_name = "W" + conditioning.value

        return (matrix_name, solution_name)


#################################
### Code related
#################################


    def set_code_matrix(self, matrix: sage.matrix):
        self.code_matrix = matrix
        
    
    def construct_and_collect_matrix(self, conditioning=ConditioningType.RAW):
        """
        Construct the whole matrix and return a ndarray of ndarray. Doesn't write in a file. You can access the matrix with self.S
        Don't use this function for large matrices (3>GB)
        """
        if self.code_matrix == None:
            raise TypeError(f"No generating matrix specified for self\nDefine the generating matrix of the code with {bcolors.BOLD}self.set_code_matrix(G){bcolors.ENDC}")
        
        data_queue = queue.Queue()
        data_container = []

        match conditioning:
            case ConditioningType.RAW:
                func = Raw.format
                arg = (int(self.nrows), int(self.ncols), np.array(self.code_matrix, dtype=int), int(self.r), data_queue)

            case ConditioningType.RAWPAD:
                func = RawPad.format
                arg = (int(self.nrows), int(self.ncols), np.array(self.code_matrix, dtype=int), int(self.r), data_queue, int(self.density()*self.ncols))

            case ConditioningType.RED:
                func = Red.format
                arg = (int(self.nrows), int(self.ncols), np.array(self.code_matrix, dtype=int), int(self.r), data_queue)
            
            case ConditioningType.REDPAD:
                func = RedPad.format
                _, ncols_red = RedPad.get_dim(self.nrows, self.n_code, self.k_code, self.r)
                arg = (int(self.nrows), int(self.ncols), np.array(self.code_matrix, dtype=int), int(self.r), data_queue, int(self.density()*ncols_red))

        compute_thread  = threading.Thread(target=func, args=arg)
        collect_thread  = threading.Thread(target=matrix_collect_queue, args=(data_queue, data_container))

        compute_thread.start()
        collect_thread.start()

        compute_thread.join()
        collect_thread.join()

        print("Matrix computation and collection completed.")
        self.S = np.array(data_container, dtype=np.ndarray)


    def construct_and_write_matrix(self, conditioning=ConditioningType.RAW):
        """
        Construct the whole matrix row by row and write in a file at the same time through a buffer
        Prefer this function for large matrices (3>GB)
        """
        if self.code_matrix == None:
            raise TypeError(f"No generating matrix specified for self\nDefine the generating matrix of the code with {bcolors.BOLD}self.set_code_matrix(G){bcolors.ENDC}")
        
        matrix_name, _ = self.get_files_names(conditioning)
        data_queue = queue.Queue()

        match conditioning:
            case ConditioningType.RAW:
                func = Raw.format
                arg = (int(self.nrows), int(self.ncols), np.array(self.code_matrix, dtype=int), int(self.r), data_queue)
            
            case ConditioningType.RAWPAD:
                func = RawPad.format
                arg = (int(self.nrows), int(self.ncols), np.array(self.code_matrix, dtype=int), int(self.r), data_queue, int(self.density()*self.ncols))
            
            case ConditioningType.RED:
                func = Red.format
                arg = (int(self.nrows), int(self.ncols), np.array(self.code_matrix, dtype=int), int(self.r), data_queue)

            case ConditioningType.REDPAD:
                func = RedPad.format
                arg = (int(self.nrows), int(self.ncols), np.array(self.code_matrix, dtype=int), int(self.r), data_queue, int(self.density()*self.ncols))
                

        compute_thread  = threading.Thread(target=func, args=arg)
        write_thread  = threading.Thread(target=matrix_to_bin_queue, args=(self.idir, matrix_name, data_queue))

        compute_thread.start()
        write_thread.start()

        compute_thread.join()
        write_thread.join()
        print("Matrix computation and writing completed.")


    def size(self, r_min=None, r_max=None):
        """
        Size of the koszul cohomology matrices
        """
        if r_min == r_max == None :
            r_min = self.r
            r_max = self.r+1

        for r in range(r_min, r_max):
            nrows = binomial(self.k_code, r+1) * r + binomial(self.k_code, r) * r # dim of cokernel
            ncols = self.n_code * binomial(self.k_code, r-1) # dim of arrival space
            print(f"b{r}_{r+1}: {nrows} x {ncols}")
            

    # WARNING! Not the exact density of the matrix representing the system but it should be close to the real one
    def density(self)->float:
        """
        Approximate density of the koszul cohomology matrix
        """        
        square_code_matrix = matrix([self.code_matrix.row(i).pairwise_product(self.code_matrix.row(j)) for i in range(0,self.k_code) for j in range(i,self.k_code)])
        square_code_density = square_code_matrix.density()
        S_density = float(square_code_density) * self.n_code * self.r / self.ncols
        return S_density

        
#################################
### Verifications
#################################


    def check_solution(self, conditioning):
        """
        When padding is added, check that at least one vector of the kernel is zero on the padding and non zero on the relevant elements.
        """
        print(f"{bcolors.BOLD}### Checking solution{bcolors.ENDC}")
        
        _, solution_file = self.get_files_names(conditioning)

        match conditioning:
            case ConditioningType.RAWPAD:
                nrows, ncols = RawPad.get_dim(self.nrows, self.ncols)
                padding = RawPad.get_padding(self.nrows, self.ncols)

            case ConditioningType.REDPAD:
                nrows, ncols = RedPad.get_dim(self.nrows, self.ncols, self.k_code, self.r)
                padding = RedPad.get_padding(self.nrows, self.ncols, self.k_code, self.r)
                
            case _:
                print(f"No verification aivalable for the {conditioning} conditioning, maybe it's not needed or maybe you should add it")
                return None

        # ker is a sage matrix with 64 (for now) vectors in columns notation
        ker = solution_from_bin(self.idir, solution_file, nrows, ncols)

        solution = False

        relevant_base = vector([any(c) for c in ker[:-padding,:].columns()])
        irrelevant_base = vector([1-any(c) for c in ker[-padding:,:].columns()])

        dim = sum(relevant_base.pairwise_product(irrelevant_base))
        solution = any(relevant_base.pairwise_product(irrelevant_base))

        if solution: 
            print(f"{bcolors.OKGREEN}The solution is valid, found a vector space of dim {dim}{bcolors.ENDC}")
        else:
            print(f"{bcolors.FAIL}The solution is not valid, dim is {dim}{bcolors.ENDC}")
            
        return ker
        

#################################
### Calls to CADO-NFS
#################################


    def scan(self, matrix_file):
        """
        Call to cado-nfs/bwc: mf_scan2 function
        """
        print(f"{bcolors.BOLD}### Scan{bcolors.ENDC}")
        subprocess.run("mf_scan2 " + self.idir + "/"+ matrix_file  +".bin", shell=True)


    def balancing(self, matrix_file):
        """
        Call to cado-nfs/bwc: mf_bal function
        """
        print(f"{bcolors.BOLD}### Balancing{bcolors.ENDC}")
        subprocess.run("mf_bal "
        + self.thr + "                      \
        mfile=" + self.idir + "/" + matrix_file + ".bin       \
        reorder=columns                     \
        rwfile=" + self.idir + "/" + matrix_file + ".rw.bin   \
        cwfile=" + self.idir + "/" + matrix_file + ".cw.bin", shell=True)


    def bwc(self, matrix_file):
        """
        Call to cado-nfs/bwc: bwc.pl script
        """
        print(f"{bcolors.BOLD}### Bwc{bcolors.ENDC}")
        threads = (self.thr).split('x')
        thr = ''.join(threads)

        subprocess.run("mkdir -p " + self.wdir + ";         \
        bwc.pl :complete                            \
        wdir=" + self.wdir + "                              \
        m=" + self.m + "                            \
        n=" + self.n + "                            \
        nullspace=left                              \
        matrix=" + self.idir +"/"+ matrix_file  +".bin               \
        thr=" + self.thr, shell = True)
        
        # balancing=$(find " + self.idir + " -name '"+ matrix_file +"."+ thr +".*.bin')",shell=True)


    def retrieve_solution(self, solution_file):
        """
        At the end of bwc, if a solution exist in self.wdir, copy it in self.dir
        """
        print(f"{bcolors.BOLD}### Retrieving solution{bcolors.ENDC}")
        if os.path.exists(self.wdir + "/W"):
            shutil.copy(self.wdir + "/W", self.idir + "/" + solution_file + ".bin")
            print(f"{bcolors.OKGREEN}Solution retrieved and placed in {self.idir}{bcolors.ENDC}")
        else:
            print(f"{bcolors.FAIL}No solution file found, maybe CADO NFS did not succeed{bcolors.ENDC}")


    def run(self, conditioning=ConditioningType.RAW):
        """
        Runs the dystiguisher:
            1. scan()
            2. balancing()
            3. bwc()
            4. retrieve_solution()
            5. 6. clear()
            
        """
        print(f"{bcolors.BOLD}### Run{bcolors.ENDC}")
        
        matrix_file, solution_file = self.get_files_names(conditioning)

        if not os.path.exists(self.idir + "/" + matrix_file + ".bin"):
            raise Exception(f"{self.idir}/{matrix_file}.bin doesn't exist !")
            
        self.scan(matrix_file)
        # self.balancing(matrix_file)
        self.bwc(matrix_file)
        self.retrieve_solution(solution_file)
                
        self.clear_idir()
        self.clear_wdir()
        

#################################
### Cleaning
#################################


    def clear_wdir(self):
        subprocess.run("rm -r " + self.wdir + "/*", shell=True)
    

    def clear_idir(self):
        dot_bin = re.compile(r'^[^.]*\.bin$')
        
        for filename in os.listdir(self.idir + "/"):
            file_path = os.path.join(self.idir + "/", filename)

            if os.path.isfile(file_path) and not dot_bin.match(filename) :
                os.remove(file_path)
