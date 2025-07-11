# The syzygy distinguisher
## Description

## Installation
1. Clone the repository with `cado-nfs` (submodule):
    ```bash
    git clone --recurse-submodules https://github.com/tichiste/dyztynguysher.git
    ```

2. Compile `cado-nfs`:
   ```bash
   cd cado-nfs; make
   ```

3. Add `cado-nfs` to your path:
   ```bash
    export PATH=<cado-dir>/build/<hostname>/linalg/bwc/$PATH
   ```

4. Create a python env with: sage<=10.6, python>=3.12, numpy<=2.2, numba<=0.61  
   We recomand using conda and using the environment.yml file.
    ```bash
    conda myenv create -f environment.yml           # Create environment from file
    conda activate myenv                            # Activate environment
    ```

## Usage
1. Activate the env
    ```bash
    conda activate myenv
    ```
2. Create an instance
    ```python
    h48 = Instance("hamming", 15, 11, 8, "128", "64", "2x2")
    C = codes.HammingCode(GF(2),4)
    G = C.generator_matrix()
    h48.set_code_matrix(G)
    ```
3. Run the distinguisher
    ```python
    h48.construct_and_write_matrix(ConditioningType.RANDOMPAD)
    h48.run(ConditioningType.RANDOMPAD)
    h48.check_solution(ConditioningType.RANDOMPAD)
    ```

## Complexity
- Krylov: n*L = N(1 + n/m + o(1)) matrix vector products


## Class info
- [x] density
- [x] conditioning type
- [x] nrows, ncols conditioning

## TODO
- [ ] all FIXME and TODO
- [x] separate conditioning functions
- [ ] use njit and numpy for conditioning when needed
- [x] i/o and ndarray of ndarray
- [x] modules