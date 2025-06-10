def matrix_to_sage(matrix, nrows, ncols):
    S_sage = zero_matrix(GF(2),nrows, ncols, sparse = True) # sparse = True is best for visualization (matrix_plot, see self.pretty_print )
    for index,row in enumerate(matrix):
        for coeff in row :
            S_sage[index,coeff] = 1
    return S_sage


def sage_to_matrix(sage_mat):
    matrix= []
    i=0
    for sage_row in sage_mat:
        matrix.append(sage_row.support())
        i+=1
        progress_percentage = float(i) / float(sage_mat.nrows()) * 100
        print(f"\rMatrix construction in progress: {progress_percentage:.2f}%", end="", flush=True)
    return matrix


def matrix_to_bin(path , name, matrix):
    with open(path + "/"+ name  +".bin", 'wb') as f:
        for row in matrix:
        # Write the number of non-zero entries as a 32-bit little-endian integer
            f.write(struct.pack('<I', len(row)))
        # Write each column index as a 32-bit little-endian integer
            for col in row:
                f.write(struct.pack('<I', col))


def matrix_from_bin(path, name):
    print(f"\nReading the matrix {name} from a bin")
    filename = path + "/"+ name +".bin"

    matrix = []
    
    try:
        with open(filename, 'rb') as f:
            while True:
                # Read the number of non-zero entries as a 32-bit little-endian integer
                num_entries_bytes = f.read(4)
                if not num_entries_bytes:
                    break  # End of file
                num_entries = struct.unpack('<I', num_entries_bytes)[0]

                # Read each column index as a 32-bit little-endian integer
                row = []
                for _ in range(num_entries):
                    col_bytes = f.read(4)
                    col = struct.unpack('<I', col_bytes)[0]
                    row.append(col)

                # Add the row to the matrix
                matrix.append(row)
            # print("here")
            return matrix

    except FileNotFoundError:
        print("No file found: " + filename + " doesn't exist !")

    
def sage_from_bin(path, matrix_name, nrows, ncols):
    filename = path + "/" + matrix_name  + ".bin"
 
    S_sage = zero_matrix(GF(2), nrows, ncols, sparse=True)
    
    try:
        with open(filename, 'rb') as f:
            row_index = 0
            while True:
                # Read the number of non-zero entries as a 32-bit little-endian integer
                num_entries_bytes = f.read(4)
                if not num_entries_bytes:
                    break  # End of file
                num_entries = struct.unpack('<I', num_entries_bytes)[0]

                # Read each column index as a 32-bit little-endian integer
                for _ in range(num_entries):
                    col_bytes = f.read(4)
                    col_index = struct.unpack('<I', col_bytes)[0]
                    S_sage[row_index,col_index] = 1

                # Add the row to the matrix
                row_index+=1
            # print("here")
            return S_sage

    except FileNotFoundError:
        print("No file found: " + filename + " doesn't exist !")

    
def solution_from_bin(path, solution_name, nrows, ncols):
    print(f"{bcolors.BOLD}### Reading solutions {soltion_name}{bcolors.ENDC}")
    # W is the result file outputed by CADO NFS
    filename = path + "/" + solution_name

    try:
        with open(filename, 'rb') as f:
            #read the bin as 32-bit le integer
            data = f.read()
            num_integers = len(data) // 4
            vectors = struct.unpack('<' + 'I' * num_integers, data)

            # convert 32-bit integer as vector in 0/1
            bit_vectors = []
            for num in vectors:
                for i in range(32):
                    bit_vectors.append((num >> i) & 1)
            
            dim_base = max(nrows,  ncols)
            dim_ker = len(bit_vectors) // dim_base
                
            ker = Matrix(GF(2), dim_base, dim_ker, bit_vectors)
            print(f"{bcolors.OKGREEN}Solutions read {self.instance_dir}{bcolors.ENDC}")
            
            return ker
    
    except FileNotFoundError:
        print("Cannot read solution, no file found: " + filename + " doesn't exist !")

    # def read_zero(self, file):
    #     filename = self.instance_dir + "/" + file

    #     try:
    #         with open(filename, 'rb') as f:
    #             #read the bin as 32-bit le integer
    #             data = f.read()
    #             num_integers = len(data) // 4
    #             vectors = struct.unpack('<' + 'I' * num_integers, data)

    #             # convert 32-bit integer as vector in 0/1
    #             bit_vectors = []
    #             for num in vectors:
    #                 for i in range(32):
    #                     bit_vectors.append((num >> i) & 1)

    #             dim_base = max(self.nrows,  self.ncols)
    #             dim_ker = len(bit_vectors) // dim_base

    #             self.zero = Matrix(GF(2), dim_base, dim_ker, bit_vectors)

    #     except FileNotFoundError:
    #         print("No file found: " + filename + " doesn't exist !")
        
