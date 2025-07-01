import math
import numpy as np

#from Cython import *

from numba import njit, types
from numba.extending import overload
from numba.core.errors import TypingError


@overload(math.comb)
def jit_comb(n, k):
    if not isinstance(n, types.Integer) or not isinstance(k, types.Integer):
        raise TypingError("'n' and 'k' must be integers")
    else:
        def comb_impl(n, k):
            if k < 0 or k > n:
                return 0
            res = 1
            for i in range(1, k+1):
                res = res * (n-i+1)//i
            return res
        return comb_impl


# FIXME: assert
@njit
def combination_at_index(i, k, n):
    assert 0<=k<=n, "k must be less than or equal to n"
    assert i>=0, "i must be non-negative"

    result = []
    x = 0
    for remaining in range(k, 0, -1):
        while math.comb(n - 1 -  x, remaining - 1) <= i:
            i -= math.comb(n - 1- x, remaining - 1)
            x += 1
        result.append(x)
        x += 1
    return result


@njit
def index_of_combination(combinaison, n):
    k = combinaison.size
    index = 0
    prev = -1
    for i in range(k):
        index += math.comb(n-prev-1,k-i) - math.comb(n-combinaison[i],k-i)
        prev = combinaison[i]
    return index


@njit
def index_to_base_coker(index,k,r):
    cursor = 0   
    subindex = 0
    l1 = 0
    lr = l1+r-1

    #giant step, find the first element of the r-uplet
    while cursor<=index:
        for i in range(lr,k):
            cursor += (i+1)*math.comb(i-l1-1,r-2)
            subindex += math.comb(i-l1-1,r-2)
        l1+=1
        lr+=1

    l1-=1
    lr-=1

    for i in range(lr,k):
        cursor -= (i+1)*math.comb(i-l1-1,r-2)
        subindex -= math.comb(i-l1-1,r-2)
    
    #baby step, find the (sub)index of the r-uplet (whitout the tensoring) among k choose r possibilities
    alpha = lr
    beta = lr

    while cursor <= index and alpha < k:
        beta = alpha
        while cursor <= index and beta < k:
            cursor += (beta+1)
            subindex += 1
            beta += 1
        alpha += 1
    
    beta -= 1
    subindex -= 1
    cursor -= beta+1

    # build the element of the coker
    res = combination_at_index(subindex, r,k)
    res.append(index-cursor)

    return res


##################################


@njit
def diff_supp(v,G,r):
    k, n = G.shape
    
    # we init with an empty array of uint32 for typing system of numba
    init = [np.uint32(0) for _ in range(0)]
    res = np.array(init, dtype='uint32')

    elem = index_to_base_coker(v,k,r)
    l = elem.pop() #indice de la ligne de G correspondant
    
    for j in range(r):
        c = G[l, :] * G[elem[j], :]
        index = index_of_combination(np.array(elem[:j]+elem[j+1:]),k-1)*n
        res = np.append(res, (np.nonzero(c)[0] + index).astype('uint32'))   

    res.sort()
    return res


##################################


def Koszul(row_begin, row_end, G, r):
    """
    Computes the image of the cokernel elements between (row_begin and row_end(exluded))
    This function is used to computed the image of the cohomology
    """

    # Initialize an empty list to store the results
    S_coker = []

    for i in range(row_begin, row_end):
        # Compute the image for each element of the base (each row)
        diff_row = diff_supp(i, G, r)
        S_coker.append(diff_row)
        progress_percentage = float(i)/row_end
        print("Matrix construction in progress:" + str(round(progress_percentage,2))+ "%", end="\r", flush=True)

    return np.array(S_coker, dtype=np.ndarray)



if __name__ == '__main__':
    import timeit


    #G = np.array([[1, 0, 0, 0, 1, 0, 1],
    #             [0, 1, 0, 0, 1, 1, 0],
    #             [0, 0, 1, 0, 1, 1, 0],
    #            [0, 0, 0, 1, 0, 1, 1]], 
    #             dtype=int)

    G = np.array (
        [[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1],
        [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1],
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0]],
        dtype=int)

    #S = Koszul(0,92820,G,2)
    time = timeit.timeit(lambda: Koszul(0, 92820, G, 5), number=1)

    print("Time for Koszul:", time)