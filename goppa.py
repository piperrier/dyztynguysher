import sage.coding.codes_catalog as codes
import random

from sage.rings.finite_rings.finite_field_constructor import GF
from sage.matrix.constructor import matrix
from sage.misc.functional import rank
from sage.combinat.permutation import Permutation
from sage.rings.polynomial.polynomial_ring_constructor import PolynomialRing


# q  the base field cardinality
# m  the extension degree
# t  the error correcting capability
# s  the amount of shortening

def goppa_short(q, m, t, s):
    F = GF(q)
    n = q**m
    #K.<b> = F.extension(m)
    K = F.extension(m, names=('b',)); (b,) = K._first_ngens(1)

    S = list(K)
    random.shuffle(S)
    
    while True:
        perm_support = [i for i in range(1,n+1)]
        random.shuffle(perm_support)
        p = Permutation(perm_support)
        p.action(S)
        
        #R.<z> = PolynomialRing(K)
        R = PolynomialRing(K, names=('z',)); (z,) = R._first_ngens(1)
        g = R.irreducible_element(t, algorithm="random")
        
        C = codes.GoppaCode(g,S)
        G = C.parity_check_matrix()
        G = G.echelon_form()
        G = G[s:m*t, s:n]
        # print(G.rank(), rank(carre_matrix(G)))
        if G.rank() == m*t-s and rank(carre_matrix(G)) == n-s:
            return G


def carre_matrix(M):
    k = M.nrows()
    # lex and skip i<j
    L = [M.row(i).pairwise_product(M.row(j)) for i in range(0,k) for j in range(i,k)]
    return matrix(L)
