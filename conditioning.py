import numpy as np
import struct

from enum import Enum
from abc import ABC, abstractmethod
from koszul import diff_supp, diff_supp_red, random_row, index_to_base_coker
from utils import bcolors

from sage.functions.other import binomial

class ConditioningType(Enum):
    RAW = 'raw'
    RAWPAD = 'rawpad'
    RED = 'red'
    REDPAD = 'redpad'


####################################
### Abstract class
####################################


class Conditioning(ABC):
    @abstractmethod
    def get_dim(n, k, r):
        """
        Size of the matrix outputed by format() and number of row padded
        """
        pass

    @abstractmethod
    def format():
        """
        Compute the marix if the given formating
        """
        pass


####################################
### Real conditioning
####################################


class Raw(Conditioning):
    def get_dim(n, k, r):
        nrows = k * binomial(k, r) - binomial(k, r+1)
        ncols = n * binomial(k, r-1)
        padding = 0
        return nrows, ncols, padding

    def format(n, k, r, G, data_queue):
        print(f"{bcolors.BOLD}### Raw conditioning{bcolors.ENDC}")

        dim_coker = k * binomial(k, r) - binomial(k, r+1)

        try:
            for i in range(dim_coker):
                elem = index_to_base_coker(i, k, r)
                row = diff_supp(elem, G, r)
                data_queue.put(row)
                
                progress_percentage = round(float(i)/dim_coker * 100, 2)
                print(f"Matrix construction in progress: {progress_percentage:.2f}%", end="\r", flush=True)

            data_queue.put(None)
            print("")

        except Exception as e:
            print(f"Error in computation thread: {e}")
            data_queue.put(None)


class RawPad(Conditioning):
    def get_dim(n, k, r):
        nrows = k * binomial(k, r) - binomial(k, r+1)
        ncols = n * binomial(k, r-1)
        padding = ncols - nrows
        return ncols, ncols, padding


    def format(n, k, r, G, weight, data_queue):
        print(f"{bcolors.BOLD}### Raw Pad conditioning{bcolors.ENDC}")

        dim_coker = k * binomial(k, r) - binomial(k, r+1)
        _, ncols, padding = RawPad.get_dim(n, k, r)


        try:
            for i in range(dim_coker):
                elem = index_to_base_coker(i, k, r)
                row = diff_supp(elem, G, r)
                data_queue.put(row)
                
                progress_percentage = round(float(i) / (dim_coker + padding) * 100, 2)
                print(f"Matrix construction in progress (image): {progress_percentage:.2f}%", end="\r", flush=True)
            
            for i in range(padding):
                row = random_row(ncols, weight)
                data_queue.put(row)
                
                progress_percentage = round(float(dim_coker+i) / (dim_coker + padding) * 100, 2)
                print(f"Matrix construction in progress (padding): {progress_percentage:.2f}%", end="\r", flush=True)
            
            data_queue.put(None)
            print("\n")
            
        except Exception as e:
            print(f"Error in computation thread: {e}")
            data_queue.put(None)


class Red(Conditioning):
    def get_dim(n, k, r):
        nrows = k * binomial(k, r) - binomial(k, r+1) - (r * binomial(k, r))
        ncols = n * binomial(k, r-1) - k * binomial(k, r-1)
        padding = 0
        return (nrows, ncols, padding)
    
    
    def format(n, k, r, G, data_queue):
        print(f"{bcolors.BOLD}### Reduction conditioning{bcolors.ENDC}")
        
        dim_coker = k * binomial(k, r) - binomial(k, r+1)

        try:
            for i in range(dim_coker):
                elem = index_to_base_coker(i, k, r)
                if elem[r] not in elem[0:r]:
                    row = diff_supp_red(elem, G, r)
                    data_queue.put(row)
                
                progress_percentage = round(float(i) / dim_coker * 100, 2)
                print(f"Matrix construction in progress: {progress_percentage:.2f}%", end="\r", flush=True)
            
            data_queue.put(None)
            print("\n")
        
        except Exception as e:
            print(f"Error in computation thread: {e}")
            data_queue.put(None)


class RedPad(Conditioning):
    def get_dim(n, k, r):
        nrows = k * binomial(k, r) - binomial(k, r+1) - (r * binomial(k, r))
        ncols = n * binomial(k, r-1) - k * binomial(k, r-1)
        padding = ncols - nrows
        return (ncols, ncols, padding)


    def format(n, k, r, G, weight, data_queue):
        print(f"{bcolors.BOLD}### Reduction Pad conditioning{bcolors.ENDC}")
        
        dim_coker = k * binomial(k, r) - binomial(k, r+1)
        _, ncols, padding = RedPad.get_dim(n, k, r)
        
        try:
            for i in range(dim_coker):
                elem = index_to_base_coker(i, k, r)
                if elem[r] not in elem[0:r]:
                    row = diff_supp_red(elem, G, r)
                    data_queue.put(row)
                
                progress_percentage = round(float(i) / (dim_coker + padding) * 100, 2)
                print(f"Matrix construction in progress (image): {progress_percentage:.2f}%", end="\r", flush=True)

            for i in range(padding):
                row = random_row(ncols - k * binomial(k, r-1), weight)
                data_queue.put(row)
                
                progress_percentage = round(float(dim_coker+i) / (dim_coker + padding) * 100, 2)
                print(f"Matrix construction in progress (padding): {progress_percentage:.2f}%", end="\r", flush=True)
            data_queue.put(None)
            print("\n")
            
        except Exception as e:
            print(f"Error in computation thread: {e}")
            data_queue.put(None)