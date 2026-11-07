# Orbit Data and Integer Certificate for X_5

This file "orbit_certificate" contains five standalone Python programs and their recorded outputs for Section 6.1 ("The lower bound") and Appendix A. They enumerate the relevant group orbits of the quotient graph $X_5$, generate its adjacency data and orbit neighbor-count matrix, reproduce the first four columns of Table A.4, and evaluate the integer certificate in Appendix A.3.

## Requirements and usage

The programs use only the Python standard library. They have been tested with Python 3.8.8 and require no third-party packages or input files.

Run any program from this directory, for example:

```bash
python 01_all_orbits.py
```

Each program prints its result to standard output. The corresponding `.txt` file contains the recorded output. To regenerate an output file, redirect the program's output:

```bash
python 01_all_orbits.py > 01_all_orbits.txt
python 02_vertex_neighbors.py > 02_vertex_neighbors.txt
python 03_quotient_matrix.py > 03_quotient_matrix.txt
python 04_table_a4.py > 04_table_a4.txt
python 05_appendix_a3_slack_vectors.py > 05_appendix_a3_slack_vectors.txt
```

All five programs run independently. Programs 3 and 4 reconstruct the orbits and graph data internally. Program 5 explicitly defines its matrix and vectors in the source code. No execution order is required.

## Graph and indexing conventions

The quotient graph has vertex set

$$
V(X_5)=\{0,1\}\times\mathbb{Z}_4^4.
$$

Vertices are printed as `(0;z1z2z3z4)` or `(1;z1z2z3z4)`, where every coordinate `zi` belongs to `{0, 1, 2, 3}`. For example, `(1;0123)` denotes $(1;0,1,2,3)$.

Set $S=\{0,e_1,e_2,e_3,e_4\}$. A vertex $(0;z)$ is adjacent to $(1;z+s)$ for every $s\in S$, with arithmetic modulo 4. Equivalently,

$$
N(\epsilon;z)=\{(1-\epsilon;z)\}
\cup\{(1-\epsilon;z+(-1)^\epsilon e_i):1\leq i\leq4\}.
$$

Thus $X_5$ has 512 vertices, degree 5 at every vertex, and 1,280 undirected edges.

The orbit computations use the group $\Gamma\cong S_5$ of 120 coordinate permutations described in Section 6.1. These permutations act on the encoding

$$
\Psi_\epsilon(z)=\left(\epsilon-\sum_{i=1}^{4}z_i,z_1,z_2,z_3,z_4\right)\in\mathbb{Z}_4^5
$$

and fix the root $o=(0;0000)$. This action has 28 orbits. Orbits are numbered **0 through 27** in increasing lexicographic order of their smallest vertices. Vertices within each orbit are also sorted lexicographically. The root forms the singleton orbit $O_0$.

## Files

| Program | Recorded output | Purpose |
| --- | --- | --- |
| [01_all_orbits.py](01_all_orbits.py) | [01_all_orbits.txt](01_all_orbits.txt) | Enumerate every orbit, its size, and all of its vertices. |
| [02_vertex_neighbors.py](02_vertex_neighbors.py) | [02_vertex_neighbors.txt](02_vertex_neighbors.txt) | List every vertex and its five neighbors in lexicographic order. |
| [03_quotient_matrix.py](03_quotient_matrix.py) | [03_quotient_matrix.txt](03_quotient_matrix.txt) | Compute the complete $28\times28$ orbit neighbor-count matrix $Q$. |
| [04_table_a4.py](04_table_a4.py) | [04_table_a4.txt](04_table_a4.txt) | Reproduce the first four columns of Table A.4. |
| [05_appendix_a3_slack_vectors.py](05_appendix_a3_slack_vectors.py) | [05_appendix_a3_slack_vectors.txt](05_appendix_a3_slack_vectors.txt) | Compute the two integer slack vectors $u$ and $v$ in Appendix A.3. |

### 1. Complete orbit enumeration

`01_all_orbits.py` generates each orbit by applying all 120 coordinate permutations to its representative. It checks that the orbits are disjoint and that their total size is 512.

`01_all_orbits.txt` contains exactly 28 lines. Each line has three tab-separated fields:

```text
orbit_index    orbit_size    [all vertices in the orbit]
```

For example, the first line is:

```text
0    1    ['(0;0000)']
```

### 2. Vertex adjacency lists

`02_vertex_neighbors.py` constructs the five neighbors of each vertex directly from the adjacency rule. It checks that each vertex has five distinct neighbors, that there are no self-loops, and that adjacency is symmetric.

`02_vertex_neighbors.txt` is a nested Python list with 512 entries. Each entry has the form `[vertex, [five neighbors]]`. Both the outer vertex order and each neighbor list are lexicographic. For example:

```python
['(0;0000)', ['(1;0000)', '(1;0001)', '(1;0010)', '(1;0100)', '(1;1000)']]
```

The file has 514 lines, including the opening and closing brackets of the outer list.

### 3. Orbit neighbor-count matrix

`03_quotient_matrix.py` reconstructs the orbit partition and computes

$$
Q_{ij}=|N_{X_5}(x)\cap O_j|,\qquad x\in O_i.
$$

It verifies this count for **every vertex** of each orbit, establishing that the value is independent of the chosen $x$. It also checks

$$
\sum_{j=0}^{27}Q_{ij}=5,
\qquad
|O_i|Q_{ij}=|O_j|Q_{ji}.
$$

`03_quotient_matrix.txt` contains $Q$ as a nested Python list with 28 rows and 28 integer entries per row. Row and column indices both start at zero. The matrix records neighbors **per vertex**, so its entries are not total edge counts between orbits.

### 4. First four columns of Table A.4

`04_table_a4.py` reconstructs the orbits and $Q$, performs the same matrix consistency checks as Program 3, and prints a compact orbit table.

`04_table_a4.txt` contains exactly 28 lines, with no header. Each line has four tab-separated fields:

```text
orbit_index    representative    orbit_size    [nonzero entries of the corresponding row of Q]
```

The representative is the lexicographically smallest vertex in the orbit. A sparse entry `j:c` means $Q_{ij}=c$; omitted entries are zero. Entries are ordered by increasing column index. For example:

```text
0    (0;0000)    1     [14:5]
1    (0;0001)    20    [14:1, 15:1, 16:3]
```

### 5. Slack vectors in Appendix A.3

`05_appendix_a3_slack_vectors.py` explicitly defines the matrix $Q$, the integer vectors $\alpha$ and $\beta$ from Table A.4, the standard basis vector $e_0=(1,0,\ldots,0)^T$, and the $28\times28$ identity matrix $I_{28}$. All vector entries use the same orbit order, from 0 through 27.

The program checks the dimensions of $Q$, $\alpha$, $\beta$, and $e_0$, then uses exact integer arithmetic to compute

$$
u=Q^T\alpha+\beta-64e_0,
$$

$$
v=(2Q^T+I_{28})\alpha+\beta-128e_0.
$$

`05_appendix_a3_slack_vectors.txt` contains two labeled lines:

```text
u = [4, 0, 0, 8, 8, 0, 9, 1, 0, 0, 0, 4, 0, 2, 0, 18, 64, 0, 0, 0, 0, 10, 3, 0, 38, 0, 12, 0]
v = [1, 32, 2, 4, 4, 0, 5, 10, 2, 3, 11, 6, 6, 1, 67, 4, 7, 26, 11, 19, 64, 1, 0, 59, 4, 17, 2, 7]
```

Every component is nonnegative, and these values reproduce Table A.5. Together with $\beta\geq0$, $\sum_i\alpha_i=43$, and $\sum_i\beta_i=30$, they provide the componentwise certificate used in Section 6.1 to exclude a feasible configuration of weight 192 and establish $\gamma_{\times2}(BH_5)\geq193$.
