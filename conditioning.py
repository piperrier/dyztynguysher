import numpy as np
import struct

from enum import Enum
from abc import ABC, abstractmethod
from koszul import diff_supp, diff_supp_red, random_row, index_to_base_coker
from utils import bcolors

from sage.functions.other import binomial

class ConditioningType(Enum):
    RAW = 'raw'
    RANDOMPAD = 'randompad'
    RED = 'red'
    REDPAD = 'redpad'


####################################


class Conditioning(ABC):
    @abstractmethod
    def get_dim(nrows, ncols):
        """
        Size of the matrix outputed by format()
        """
        pass

    @abstractmethod
    def format():
        """
        Compute the marix if the given formating
        """
        pass


class Raw(Conditioning):
    def get_dim(nrows, ncols):
        return nrows, ncols

    def format(nrows, ncols, G, r, data_queue):
        print(f"{bcolors.BOLD}### Raw conditioning{bcolors.ENDC}")
        k, n = G.shape
        try:
            for i in range(nrows):
                elem = index_to_base_coker(i, k, r)
                row = diff_supp(elem, G, r)
                data_queue.put(row)
                
                progress_percentage = round(float(i)/nrows * 100,2)
                print(f"Matrix construction in progress: {progress_percentage:.2f}%", end="\r", flush=True)

            data_queue.put(None)  # Signal that computation is done
            print("")

        except Exception as e:
            print(f"Error in computation thread: {e}")
            data_queue.put(None)  # Ensure the writing thread can exit


class RandomRowPad(Conditioning):
    def get_dim(nrows, ncols):
        if nrows > ncols:
            raise Exception(f"Cannot add random rows to a matrix with more rows than columns, {nrows}>{ncols}")
        return ncols, ncols


    def get_padding(nrows, ncols):
        return ncols - nrows


    def format(nrows, ncols, G, r, data_queue, weight):
        print(f"{bcolors.BOLD}### Randow Row Pad conditioning{bcolors.ENDC}")
        k, n = G.shape
        try:
            for i in range(nrows):
                elem = index_to_base_coker(i, k, r)
                row = diff_supp(elem, G, r)
                data_queue.put(row)
                
                progress_percentage = round(float(i)/ncols * 100,2)
                print(f"Matrix construction in progress: {progress_percentage:.2f}%", end="\r", flush=True)

            for i in range(ncols - nrows):
                row = random_row(ncols, weight)
                data_queue.put(row)
                
                progress_percentage = round(float(nrows+i)/ncols * 100,2)
                print(f"Matrix construction in progress: {progress_percentage:.2f}%", end="\r", flush=True)
            
            data_queue.put(None)  # Signal that computation is done
            print("\n")
            
        except Exception as e:
            print(f"Error in computation thread: {e}")
            data_queue.put(None)  # Ensure the writing thread can exit


class Red(Conditioning):
    def get_dim(nrows, ncols, k, r):
        return (nrows - r * binomial(k, r), ncols - k * binomial(k, r-1))
    
    def format(nrows, ncols, G, r, data_queue):
        k, n = G.shape
        try:
            for i in range(nrows):
                elem = index_to_base_coker(i, k, r)
                if elem[r] not in elem[0:r]:
                    row = diff_supp_red(elem, G, r)
                    data_queue.put(row)
                
                #progress_percentage = round(float(i)/ncols * 100,2)
                #print(f"Matrix construction in progress: {progress_percentage:.2f}%", end="\r", flush=True)
            
            data_queue.put(None)  # Signal that computation is done
            #print("\n")
        
        except Exception as e:
            print(f"Error in computation thread: {e}")
            data_queue.put(None)  # Ensure the writing thread can exit


class RedPad(Conditioning):
    def get_dim(nrows, ncols, k, r):
        return (nrows - r * binomial(k, r), ncols - k * binomial(k, r-1))


    def get_padding(nrows, ncols,k, r):
        return (ncols - k * binomial(k, r-1)) - (nrows - r * binomial(k, r))


    def format(nrows, ncols, G, r, data_queue, weight):
        k, n = G.shape
        try:
            for i in range(nrows):
                elem = index_to_base_coker(i, k, r)
                if elem[r] not in elem[0:r]:
                    row = diff_supp_red(elem, G, r)
                
                    data_queue.put(struct.pack('<I', len(row)))
                    data_queue.put(row.tobytes())
                
                progress_percentage = round(float(i)/ncols * 100,2)
                print(f"Matrix construction in progress: {progress_percentage:.2f}%", end="\r", flush=True)

            for i in range((nrows - r * binomial(k, r)) - (ncols - k * binomial(k, r-1))):
                row = random_row(ncols, weight)
                
                data_queue.put(struct.pack('<I', weight))
                data_queue.put(row.tobytes())
                
                progress_percentage = round(float(nrows+i)/ncols * 100,2)
                print(f"Matrix construction in progress: {progress_percentage:.2f}%", end="\r", flush=True)
            data_queue.put(None)  # Signal that computation is done
            print("\n")
            
        except Exception as e:
            print(f"Error in computation thread: {e}")
            data_queue.put(None)  # Ensure the writing thread can exit