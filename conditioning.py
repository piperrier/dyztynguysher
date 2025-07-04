import numpy as np
import struct

from enum import Enum
from abc import ABC, abstractmethod
from koszul import diff_supp, random_row


class ConditioningType(Enum):
    RAW = 'raw'
    RANDOMPAD= 'randompad'


####################################


class Conditioning(ABC):
    @abstractmethod
    def get_dim(nrows, ncols):
        pass

    @abstractmethod
    def format():
        pass


class Raw(Conditioning):
    def get_dim(nrows, ncols):
        return nrows, ncols

    def format(nrows, ncols, G, r, data_queue):
        try:
            for i in range(nrows):
                row = diff_supp(i, G, r)
                data_queue.put(struct.pack('<I', len(row)))
                data_queue.put(row.tobytes())
                progress_percentage = round(float(i)/nrows * 100,2)
                print(f"Matrix construction in progress: {progress_percentage:.2f}%", end="\r", flush=True)

            data_queue.put(None)  # Signal that computation is done
        except Exception as e:
            print(f"Error in computation thread: {e}")
            data_queue.put(None)  # Ensure the writing thread can exit


class RandomRowPad(Conditioning):
    def get_dim(nrows, ncols):
        if nrows > ncols:
            raise Exception(f"Cannot add random rows to a matrix with more rows than columns, {nrows}>{ncols}")
        return ncols, ncols

    
    def format(nrows, ncols, G, r, data_queue, weight):
        try:
            for i in range(nrows):
                row = diff_supp(i, G, r)
                data_queue.put(struct.pack('<I', len(row)))
                data_queue.put(row.tobytes())
                progress_percentage = round(float(i)/ncols * 100,2)
                print(f"Matrix construction in progress: {progress_percentage:.2f}%", end="\r", flush=True)

            for i in range(ncols - nrows):
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

