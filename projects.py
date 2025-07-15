from syz import *
from conditioning import *

def goppa_2_10_9_s34():
    i = Instance("goppa_2_10_9_s34", 990, 56, 3, "64", "64", "10x10" )
    G = goppa_short(2,10,9,34)
    
    i.set_code_matrix(G)
    i.construct_and_write_matrix(ConditioningType.RANDOMPAD)
    i.run(ConditioningType.RANDOMPAD)
    i.check_solution(ConditioningType.RANDOMPAD)

    return i


def goppa_2_10_10_s40():
    i = Instance("goppa_2_10_10_s40", 984, 60, 4, "64", "64", "10x10" )
    G = goppa_short(2,10,10,40)
    
    i.set_code_matrix(G)
    # i.construct_matrix()
    # i.Sraw = syst
    # i.Sraw = matrix_from_bin(i.path,"Sraw", nrows = i.nrows)
    # matrix_to_bin(i.path,"Stest",i.Sraw)

    # i.run(ConditioningType.RANDOMPAD)
    
    # Stest = matrix_from_bin(i.path,"Stest", nrows = i.nrows)

    # eq = np.all([np.array_equal(i.Sraw[j], Stest[j]) for j in range(Stest.size)])
    # print(eq)
    
    return i


goppa = goppa_2_10_9_s34()
#goppa = goppa_2_10_10_s40()