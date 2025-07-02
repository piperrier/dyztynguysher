import struct
import numpy as np

from sage.rings.finite_rings.finite_field_constructor import GF
from sage.matrix.special import zero_matrix
from sage.matrix.constructor import matrix

from utils import bcolors

def matrix_to_sage(matrix, nrows, ncols):
    # works with list of list, list of ndarray and ndarray of ndarray
    S_sage = zero_matrix(GF(2),nrows, ncols, sparse = True) # sparse = True is best for visualization (matrix_plot, see self.pretty_print )
    for index,row in enumerate(matrix):
        for coeff in row :
            S_sage[index,coeff] = 1
    return S_sage


def matrix_to_bin(path , name, matrix):
    print(f"Writing the matrix {name} in a bin:", flush=True)

    with open(path + "/"+ name  +".bin", 'wb') as f:
        for irow, row in enumerate(matrix):
        # Write the number of non-zero entries as a 32-bit little-endian integer
            f.write(struct.pack('<I', len(row)))
            f.write(row.tobytes())

            progress_percentage = float(irow) / float(len(matrix)) * 100
            print(f"Writing matrix: {progress_percentage:.2f}%", end="\r", flush=True)


def matrix_from_bin(path, name, nrows):
    print(f"Reading the matrix {name} from a bin:")
    filename = path + "/"+ name +".bin"
    matrix = np.empty(nrows, dtype=np.ndarray)
        
    try:
        with open(filename, 'rb') as f:
            mmap = np.memmap(f, dtype='uint32', mode='r')
            irow = 0
            index = 0
            while index < len(mmap)-1:
                # number of non-zero entries
                num_entries = mmap[index]
                index += 1

                # column indices
                row = mmap[index:index + num_entries]
                index += num_entries
                matrix[irow] = np.array(row)
                
                irow+=1
                progress_percentage = float(irow) / float(nrows) * 100
                print(f"Reading matrix: {progress_percentage:.2f}%", end="\r", flush=True)

            # mmap.close()
            del mmap
            print("\n")
            return matrix

    except FileNotFoundError:
        print("No file found: " + filename + " doesn't exist !")


# TODO: speed-up    
def sage_from_bin(path, matrix_name, nrows, ncols):
    filename = path + "/" + matrix_name  + ".bin"
 
    S_sage = zero_matrix(GF(2), nrows, ncols, sparse=True)
    
    try:
        with open(filename, 'rb') as f:
            row_index = 0
            while True:
                # Read the number of non-zero entries as a 32-bit little-endian integer
                num_entries_bytes = f.read(4)
                if not num_entries_bytes:
                    break  # End of file
                num_entries = struct.unpack('<I', num_entries_bytes)[0]

                # Read each column index as a 32-bit little-endian integer
                for _ in range(num_entries):
                    col_bytes = f.read(4)
                    col_index = struct.unpack('<I', col_bytes)[0]
                    S_sage[row_index,col_index] = 1

                # Add the row to the matrix
                row_index+=1
            return S_sage

    except FileNotFoundError:
        print("No file found: " + filename + " doesn't exist !")


# FIXME: assert 
# TODO: memory map
def solution_from_bin(path, solution_name, nrows, ncols):
    print(f"{bcolors.BOLD}### Reading solutions {solution_name}{bcolors.ENDC}")
    # W is the result file outputed by CADO NFS
    filename = path + "/" + solution_name + ".bin"

    try:
        with open(filename, 'rb') as f:
            #read the bin as 32-bit le integer
            data = f.read()
            num_integers = len(data) // 4
            vectors = struct.unpack('<' + 'I' * num_integers, data)

            # convert 32-bit integer as vector in 0/1
            bit_vectors = []
            for num in vectors:
                for i in range(32):
                    bit_vectors.append((num >> i) & 1)
            
            dim_base = max(nrows,  ncols)
            dim_ker = len(bit_vectors) // dim_base
            assert (len(bit_vectors) % dim_base) == 0
            assert dim_ker == 64
            ker = matrix(GF(2), dim_base, dim_ker, bit_vectors)
            print(f"Solution dimensions: {ker.dimensions()}")
            print(f"{bcolors.OKGREEN}Solution read{bcolors.ENDC}")
            
            return ker
    
    except FileNotFoundError:
        print("Cannot read solution, no file found: " + filename + " doesn't exist !")
