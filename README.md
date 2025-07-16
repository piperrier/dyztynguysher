# The syzygy distinguisher

## Description

On veut utiliser l'agorithme de block Wiedemann pour trouver si la $r$-ième homologie suivante est nulle ou non :  

```math
\bigwedge^{r+1} S_1 \xrightarrow{d} \bigwedge^r S_1 \bigotimes C \xrightarrow{d'} \bigwedge^{r-1} S_1 \bigotimes \mathbf F^n
```

Pour cela, on regarde si le noyau de $d'$ sur le supplémentaire de $\mathrm{im}(d)$ ayant pour base $\{ x_{l_1}\wedge \dots \wedge x_{l_r} \otimes c_l\ |\ l_1<\dots <l_r, l \leq l_r \}$ est nulle ou non. Pour cela on utilise block Wiedemann.

## Installation

1. Clone the repository with [`cado-nfs`](https://gitlab.inria.fr/cado-nfs/cado-nfs) (submodule):

    ```bash
    git clone --recurse-submodules https://github.com/tichiste/dyztynguysher.git
    ```

2. Compile `cado-nfs`:

   ```bash
   cd cado-nfs; make
   ```

3. Add `cado-nfs` to your path, we will use [`bwc`](https://gitlab.inria.fr/cado-nfs/cado-nfs/-/tree/master/linalg/bwc) module:

   ```bash
    export PATH="$PATH:/<cado-dir>/build/<hostname>/linalg/bwc"
   ```

4. Create a python env with: sage<=10.6, python>=3.12, numpy<=2.2, numba<=0.61, gallois  
   We provide an environment.yml file, with a conda environement called `syz`.

    ```bash
    conda env create -f environment.yml             # Create the syz environment from file
    conda activate syz                              # Activate syz environment
    ```

## Usage

1. Activate the env

    ```bash
    conda activate syz
    ```

2. On the sage interpreter, load `syz.py`

    ```python
    load("syz.py")
    ```

3. Create an instance

    ```python
    h48 = Instance("hamming", 15, 11, 8, "128", "64", "2x2", wdir="/nvme/user/wdir")
    C = codes.HammingCode(GF(2),4)
    G = C.generator_matrix()
    h48.set_code_matrix(G)
    ```

4. Run the distinguisher with the conditioning of your choice:
   - `RAW`
   - `RAWPAD`
   - `RED`
   - `REDPAD`

    ```python
    h48.construct_and_write_matrix(ConditioningType.RAWPAD)
    h48.run(ConditioningType.RAWPAD)
    h48.check_solution(ConditioningType.RAWPAD)
    ```

## Block Wiedemann & Complexity

**References for Block wiedemann**:

- [Don Coppersmith, 1994](https://www.ams.org/journals/mcom/1994-62-205/S0025-5718-1994-1192970-7/S0025-5718-1994-1192970-7.pdf)

- Emmanuel Thomé, 2022: [slide 1](https://homepages.loria.fr/EThome/teaching/2022-cse-291-14/slides/cse-291-14-lecture-14.pdf), [slide 2](https://members.loria.fr/EThome/teaching/2022-cse-291-14/slides/cse-291-14-lecture-15.pdf)  

**Complexity**:

- `krylov`: $n \times L = N(1 + n/m + o(1))$ matrix vector products

- `krylov+mksol`: $(1 + n/m + r/n) \times N$, where r = 64 when working over GF(2) on a 64 bits processor

- `lingen`: time=$(m+n) \times Nlog(N) \times (m + n + log(N))$

**Probability of success**:

- the matrix shouldn't have a non-zero eigenvalue of high multiplicity

## Potential improvements

- multithreading when constructing the matrix
- improve theoretical matrix reduction before construction
- use `MPI` option of `cado-nfs` to run block Wiedemann on multiple computers
- refactor conditioning

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
