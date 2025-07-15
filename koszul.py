import math
import numpy as np
import random

from numba import njit, types
from numba.extending import overload
from numba.core.errors import TypingError


#################################
### Support functions 
#################################


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


@njit
def combination_at_index(i, k, n):
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
def index_to_base_coker(index, k, r):
    cursor = 0
    _cursor = 0
    lp = -1
    elt = []

    for p in range(1,r+1):
        while cursor <= index:
            lp += 1
            _cursor = cursor
            cursor += (r-p) * math.comb(k-lp,r-p+1)+(lp+1)*math.comb(k-lp-1,r-p)
        elt.append(lp)
        cursor = _cursor
    elt.append(index-cursor)
       
    return elt


def base_to_index_supp(elt,k,r):
    index = 0

    #p=1
    for l in range(elt[0]):
        index += (r-1) * math.comb(k-l,r-1+1)+(l+1)*math.comb(k-l-1,r-1)
    #p suivants
    
    for p in range(2,r+1):
        for l in range(elt[p-2]+1,elt[p-1]):
            index += (r-p) * math.comb(k-l,r-p+1)+(l+1)*math.comb(k-l-1,r-p)
    
    
    return index + elt[r]


#################################
### Image of the homology a a basis element (used for conditioning)
#################################


# RAW conditioning
@njit
def diff_supp(elem, G, r):
    k, n = G.shape

    # we init with an empty array of uint32 for typing system of numba
    init = [np.uint32(0) for _ in range(0)]
    res = np.array(init, dtype='uint32')

    l = elem.pop() #indice de la ligne de G correspondant
    for j in range(r):
        c = G[l, :] * G[elem[j], :]
        index = index_of_combination(np.array(elem[:j]+elem[j+1:]),k)*n
        res = np.append(res, (np.nonzero(c)[0] + index).astype('uint32'))   

    res.sort()
    return res


# RANDOMPAD Conditioning
#@njit
def random_row(rng, ncols, weight):
    #row = np.random.choice(np.arange(ncols), size=weight, replace=False).astype('uint32')
    row = rng.choice(np.arange(ncols, dtype='uint32'), size=weight, replace=False)

    row.sort()
    return row


# RED Conditioning
@njit
def diff_supp_red(elem: list, G:np.ndarray, r:int) -> np.ndarray:
    k, n = G.shape
    
    # we init with an empty array of uint32 for typing system of numba
    init = [np.uint32(0) for _ in range(0)]
    res = np.array(init, dtype='uint32')

    l = elem.pop() #indice de la ligne de G correspondant
    for j in range(r):
        c = G[l, :] * G[elem[j], :] #only the n-k last columns
        c = c[k:]
        index = index_of_combination(np.array(elem[:j]+elem[j+1:]),k)*(n-k)
        res = np.append(res, (np.nonzero(c)[0] + index).astype('uint32'))   

    res.sort()
    return res


#################################
### Homology functions (used for test)
#################################


def koszul_cohom(nrows, ncols, G, r):
    """
    Computes the image of the cokernel elements between row_begin and row_end(exluded)
    This function is used to computed the image of the cohomology
    """
    # Initialize an empty list to store the results
    k, n = G.shape
    S_coker = []

    for i in range(nrows):
        # Compute the image for each element of the base (each row)
        elem = index_to_base_coker(i, k, r)
        diff_row = diff_supp(elem, G, r)
        S_coker.append(diff_row)
        progress_percentage = round(float(i)/nrows * 100,2)
        print(f"Matrix construction in progress: {progress_percentage:.2f}%", end="\r", flush=True)

    return np.array(S_coker, dtype=np.ndarray)


def koszul_cohom_red(nrows, ncols, G, r):
    """
    Computes the image of the cokernel elements between row_begin and row_end(exluded)
    This function is used to computed the image of the cohomology
    """
    # Initialize an empty list to store the results
    k, n = G.shape
    S_coker = []

    for i in range(nrows):
        # Compute the image for each element of the base (each row)
        elem = index_to_base_coker(i, k, r)
        if elem[r] not in elem[0:r]:    # remove row with pivots
            diff_row = diff_supp_red(elem, G, r)
            S_coker.append(diff_row)
        progress_percentage = round(float(i)/nrows * 100,2)
        print(f"Matrix construction in progress: {progress_percentage:.2f}%", end="\r", flush=True)

    return np.array(S_coker, dtype=np.ndarray)

if __name__ == '__main__':
    import timeit
    import itertools
    from matrix_bin import *

    ### base
    """
    k = 30
    r = 5

    kCr = [list(x) for x in itertools.combinations(range(k), r)]

    coker = []
    for i in kCr:
        for alpha in range(i[-1]+1):
            coker.append(i + [alpha])

    test = [index_to_base_coker(i, k, r) for i in range(len(coker))]
    print("base eq")
    print(coker==test)
    """

    ### randrow
    rng = np.random.default_rng()
    time = timeit.timeit(lambda: random_row(rng, 1_524_600, 722), number = 10_000)
    print(time)
    #print("randrom",time)
    
    #G = np.array([[1, 0, 0, 0, 0, 1, 1],
    #             [0, 1, 0, 0, 1, 0, 1],
    #             [0, 0, 1, 0, 1, 1, 0],
    #             [0, 0, 0, 1, 1, 1, 1]], 
    #             dtype=int)
    #nrows = 20
    #ncols = 28
    #k = 4
    #r = 2

    """
    G = np.array(
        [[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
        [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1]], dtype=int)
    

    G[:,[10,11]] = G[:,[11,10]]
    
    
    nrows = 1760
    ncols = 4950
    
    k = 11
    r = 8
    """
    

    """
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
    nrows = 92820
    ncols = 111860
    k=17
    r = 5
    """

    """
    #S = koszul_cohom(nrows, ncols, G, r)
    S_red = koszul_cohom_red(nrows, ncols, G, r)


    #test = matrix_to_sage(S, nrows,ncols)
    test_red = matrix_to_sage(S_red, nrows-r*math.comb(k,r),ncols-k*math.comb(k,r-1))
    
    #print(test.dimensions())
    #ker = test.kernel()
    #print(ker.dimension())


    print("")
    
    print(test_red.dimensions())
    ker_red = test_red.kernel()
    print(ker_red.dimension())
    """
    #time = timeit.timeit(lambda: koszul_cohom(0, nrows, G, r), number=1)
    #print(f"Time for Koszul: {time:.2f} sec")