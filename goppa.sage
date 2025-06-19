# q  the base field cardinality
# m  the extension degree
# t  the error correcting capability
# s  the amount of shortening

def goppa_short(q, m, t, s):
    F = GF(2)
    n = 2^m
    K.<b> = F.extension(m)
    # print(K)

    S = list(K)
    random.shuffle(S)
    
    while True:
        p_sup = [i for i in range(1,n+1)]
        random.shuffle(p_sup)
        p = Permutation(p_sup)
        p.action(S)
        
        R.<z> = PolynomialRing(K)
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
