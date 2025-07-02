import math
import numpy as np

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

# OK
@njit
def combination_at_index(i, k, n):
    #assert 0<=k<=n, "k must be less than or equal to n"
    #assert i>=0, "i must be non-negative"

    result = []
    x = 0
    for remaining in range(k, 0, -1):
        while math.comb(n - 1 -  x, remaining - 1) <= i:
            i -= math.comb(n - 1- x, remaining - 1)
            x += 1
        result.append(x)
        x += 1
    return result


# OK
@njit
def index_of_combination(combinaison, n):
    k = combinaison.size
    index = 0
    prev = -1
    for i in range(k):
        #for x in range(prev + 1, combinaison[i]):
        #    index += math.comb(n - x, k - i - 1)
        index += math.comb(n-prev-1,k-i) - math.comb(n-combinaison[i],k-i)
        prev = combinaison[i]
    return index


@njit
def index_to_base_coker(index, k, r):
    elt = []

    cursor = 0
    _cursor = 0

    # first element
    l1 = 0

    lr = l1 + r - 1

    while cursor <= index:
        _cursor = cursor
        for i in range(lr, k):
            cursor += (i+1)*math.comb(i - l1 - 1, r - 2)

        l1 += 1
        lr += 1

    l1 -= 1
    lr -= 1
    cursor = _cursor
    elt.append(l1)

    # loop for 2nd to (r-1)-th element
    for p in range(1, r-1):
        lp = elt[-1] + 1
        lr = lp + r - (p+1)
    
        while cursor <= index:
            _cursor = cursor
            for i in range(lr, k):
                cursor += (i+1)*math.comb(i - lp - 1, r - p - 2)
            lp += 1
            lr += 1

        lp -= 1
        lr -= 1
        cursor = _cursor

        elt.append(lp)

    # last element, r-th
    lr = elt[-1] + 1
    while cursor<=index and lr < k:
        cursor += lr+1
        lr +=1 
    lr -= 1
    cursor -= (lr+1)
    elt.append(lr)

    #tensor element
    elt.append(index - cursor)
    
    return elt



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
        index = index_of_combination(np.array(elem[:j]+elem[j+1:]),k)*n
        #print(index)
        #print(np.nonzero(c)[0])
        #print(c)
        res = np.append(res, (np.nonzero(c)[0] + index).astype('uint32'))   

    res.sort()
    return res


##################################


def Koszul(row_begin, row_end, G, r):
    """
    Computes the image of the cokernel elements between (row_begin and row_end(exluded))
    This function is used to computed the image of the cohomology
    """
    #print("\n### Const S")
    # Initialize an empty list to store the results
    S_coker = []

    for i in range(row_begin, row_end):
        # Compute the image for each element of the base (each row)
        diff_row = diff_supp(i, G, r)
        S_coker.append(diff_row)
        progress_percentage = round(float(i)/row_end * 100,2)
        #print(f"Matrix construction in progress: {progress_percentage:.2f}%", end="\r", flush=True)

    return np.array(S_coker, dtype=np.ndarray)



if __name__ == '__main__':
    import timeit
    import itertools

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
    
    #G = np.array([[1, 0, 0, 0, 1, 0, 1],
    #             [0, 1, 0, 0, 1, 1, 0],
    #             [0, 0, 1, 0, 1, 1, 0],
    #            [0, 0, 0, 1, 0, 1, 1]], 
    #             dtype=int)
    #nrows = 20
    #r = 2

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
    r = 5

    S = Koszul(0, nrows, G, r)

    time = timeit.timeit(lambda: Koszul(0, nrows, G, r), number=1)

    print("Time for Koszul:", time)