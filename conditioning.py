import numpy as np


from enum import Enum
from abc import ABC, abstractmethod


class ConditioningType(Enum):
    RAW = 'raw'
    # BLOCK1 = 'block1'
    RANDOMPAD= 'randompad'


####################################


class Conditioning(ABC):
    @abstractmethod
    def get_dim(nrows, ncols):
        pass

    @abstractmethod
    def format(matrix, nrows, ncols):
        pass


class Raw(Conditioning):
    def get_dim(nrows, ncols):
        return nrows, ncols

    def format(matrix, nrows, ncols):
        return matrix


class RandomRowPad(Conditioning):
    def get_dim(nrows, ncols):
        if nrows > ncols:
            raise Exception(f"Cannot add random rows to a matrix with more rows than columns, {nrows}>{ncols}")
        return ncols, ncols

    def format(matrix, nrows, ncols, row_weight):
        # print(f"{bcolors.BOLD}### Random row pad conditioning{bcolors.ENDC}")
        print("### Random row pad conditioning")

        row_pad = ncols - nrows
        if row_pad < 0:
            raise Exception(f"Cannot add random rows to a matrix with more rows than columns, {nrows}>{ncols}")

        print(f"Padding {row_pad} rows with {row_weight} elements")
        padding = np.empty(row_pad, dtype=np.ndarray)
        rng = np.random.default_rng()

        for j in range(row_pad):
            row = rng.choice(np.arange(ncols, dtype='uint32'), size=row_weight, replace=False)
            row.sort()
            padding[j] = row

        pad_matrix = np.append(matrix, padding)
        pad_matrix_nrows = nrows + row_pad
        pad_matrix_ncols = ncols
        return (pad_matrix, pad_matrix_nrows, pad_matrix_ncols)
