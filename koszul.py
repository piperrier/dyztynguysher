from numba import njit, types, objmode
from numba.extending import overload
from numba.core.errors import TypingError

import math
import numpy as np
import itertools


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
def index_of_combination(combinaison, n):
    k = combinaison.size
    index = 0
    prev = -1
    for i in range(k):
        for x in range(prev + 1, combinaison[i]):
            index += math.comb(n - x, k - i - 1)
        prev = combinaison[i]
    return index


# TODO: Idealy we would return a ndarray of ndarray and not a list of ndarray
# @njit
# def construct_S(n, k, r, G, C_r):
#     nrows_S = math.comb(k, r+1) * r + math.comb(k, r) * r
#     ncols_S = n * math.comb(k, r-1)

#     print("\n### Const S")
#     print("Sdim", nrows_S, ncols_S)
#     S = []
#     row_S = 0

#     for index_I, I in enumerate(C_r):
#         for alpha in range(I[-1]+1):
#             # for every vec in the cokernel, compute it
#             col = []
#             for j in range(r):
#                 c = G[alpha, :] * G[I[j], :]
#                 for u, gamma in enumerate(c):
#                     shift = index_of_combination(np.concatenate((I[0:j], I[j+1:]), axis=0), k - 1)
#                     if gamma:
#                         col.append(math.comb(k, r-1) * u + shift)
#             col.sort()
#             S.append(np.array(col, dtype='uint32'))
#             row_S += 1
#             progress_percentage = (row_S / nrows_S) * 100
#             with objmode():
#                 print("Matrix construction in progress:" + str(round(progress_percentage,2))+ "%", end="\r", flush=True)

#     # print("\n")
#     return S

@njit(parallel=True)
def construct_S(n, k, r, G, C_r):
    nrows_S = math.comb(k, r+1) * r + math.comb(k, r) * r
    ncols_S = n * math.comb(k, r-1)

    print("\n### Const S")
    print("Sdim", nrows_S, ncols_S)
    S = []
    row_S = 0

    for index_I, I in enumerate(C_r):
        for alpha in range(I[-1]+1):
            # for every vec in the cokernel, compute it
            col = []
            for j in range(r):
                c = G[alpha, :] * G[I[j], :]
                for u, gamma in enumerate(c):
                    shift = index_of_combination(np.concatenate((I[0:j], I[j+1:]), axis=0), k - 1)
                    if gamma:
                        col.append(shift * n + u)
            col.sort()
            S.append(np.array(col, dtype='uint32'))
            row_S += 1
            progress_percentage = (row_S / nrows_S) * 100
            with objmode():
                print("Matrix construction in progress:" + str(round(progress_percentage,2))+ "%", end="\r", flush=True)

    # print("\n")
    return S

# @njit
# def g_construct_S(n, k, r, G, W, C_r):
#     nrows_S = math.comb(k, r+1) * r + math.comb(k, r) * r
#     ncols_S = n * math.comb(k, r-1)

#     print("\n### Const S")
#     print("Sdim", nrows_S, ncols_S)
#     S = []
#     row_S = 0

#     for index_I, I in enumerate(C_r):
#         for alpha in range(I[-1]+1):
#             # for every vec in the cokernel
#             # compute it
#             col = []
#             for j in range(r):
#                 c = G[alpha, :] * G[I[j], :]
#                 for u, gamma in enumerate(c):
#                     shift = g_index_of_combination(np.concatenate((I[0:j], I[j+1:]), axis=0), k - 1)
#                     if gamma:
#                         col.append(math.comb(k, r-1) * u + shift)
#             col.sort()
#             S.append(col)
#             row_S += 1
#             progress_percentage = (row_S / nrows_S) * 100
#             with objmode():
#                 print("Matrix construction in progress:" + str(round(progress_percentage,2))+ "%", end="\r", flush=True)

#                 # print(round(progress_percentage))
#     print("\n")
#     # return np.array([np.array(x)] for x in S)
#     return S


def Koszul(G, r):
    k, n = G.shape

    C_r = [np.array(subset) for subset in itertools.combinations(np.arange(k), r)]
    # print(C_r)
    S_coker = np.array(construct_S(n, k, r, G, C_r), dtype=np.ndarray)

    return S_coker
