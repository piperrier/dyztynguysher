from math import comb
# import time

def carre_matrix(M):
    k = M.nrows()
    # lex and skip i<j
    L = [M.row(i).pairwise_product(M.row(j)) for i in range(0,k) for j in range(i,k)]
    return matrix(L)

def span_code(M):
    V = VectorSpace(M.base_ring(), M.ncols())
    W = V.subspace(M)
    return W

def span_carre_code(M):
    carre_code = carre_matrix(M)
    # print(carre_code)
    V = VectorSpace(M.base_ring(),M.ncols())
    # S = V.subspace(map(elt, V(elt) list(carre_code))
    W = V.subspace(carre_code)
    return W

def index_of_combination(combinaison, n):
    k = len(combinaison)
    index = 0
    prev = -1
    for i in range(k):
        for x in range(prev + 1, combinaison[i]):
            # index += binomial(n - x, k - i - 1)
            index += comb(n - x, k - i - 1)
        prev = combinaison[i]
    return index

# S is row convention
# S is a list of list, each list is a row and contains the non zero columns of the row
def construct_S(n,k,r,G,W):
    nrows_S = binomial(k,r+1) * r + binomial(k,r) * r
    ncols_S = W.dimension() * binomial(k,r-1)
    print("\n### Construction of the system matrix S ###")
    print(f"S dimensions: {nrows_S} x {ncols_S}")
    print("dim coker", (k * binomial(k,r)) - binomial(k,r+1))
    print("no repetition", binomial(k,r+1) * r)
    print("repetition", binomial(k,r) * r)
    
    #S = zero_matrix(W.base_ring(), nrows_S, ncols_S)
    S = []
    
    C_r   = Combinations(range(k),r)
    C_rm1 = Combinations(range(k),r-1)
    row_S = 0
    for index_I, I in enumerate(C_r):
        for alpha in range(I[-1]+1):
        # for every vec in the cokernel
        # compute it
            col = []
            for j in range(r):
                c = G.row(alpha).pairwise_product(G.row(I[j]))
                for u, gamma in enumerate(W.coordinate_vector(c)):
                    shift = index_of_combination(I[0:j]+I[j+1:],k-1)
                    if gamma :
                        col.append(binomial(k,r-1)*u + shift)
                    #S[binomial(k,r-1)*u + shift, col_S] = gamma * (-1)^j
            col.sort()
            S.append(col)
            row_S +=1
            progress_percentage = float(row_S) / float(nrows_S) * 100
            print(f"\rMatrix construction in progress: {progress_percentage:.2f}%", end="", flush=True)
    print("\n")
    return (nrows_S, ncols_S, S)
            
def Betti(G,r):
    n = G.ncols()
    k = G.nrows()

    W = span_carre_code(G)
    #print(W)
    nrows_S, ncols_S, S_coker = construct_S(n,k,r,G,W)
    return S_coker
    #print(S_coker)

#Betti(G,6)
