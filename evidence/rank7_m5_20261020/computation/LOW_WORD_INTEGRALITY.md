# Low-object word integrality

This is an exact necessary condition on a proposed center spectrum. It does not construct a center or, by itself, exclude either remaining fusion ring.

Let the positive global dimension of the proposed fusion category be `D`, so the normalized center matrix satisfies `S[0,Y] = d_Y / D`. For the distinguished center simple `A_E` corresponding to a one-dimensional ring character `chi_E` of formal codegree `f_E`, the existing induction identities give

\[
 d_{A_E}=D/f_E,\qquad S_{A_E,Y}=\chi_E(FY)/f_E.
\]

The fusion character at `Y` therefore has value

\[
 \lambda_E(Y)=\frac{D\chi_E(FY)}{f_Ed_Y}.
\]

For a word `w=(E_1,...,E_k)`, simultaneous diagonalization of the fusion matrices gives the coefficient of the unit:

\[
 \tau(w)=[\mathbf1:A_{E_1}\otimes\cdots\otimes A_{E_k}]
 =\sum_Y\frac{d_Y^2}{D^2}\prod_{j=1}^k\lambda_{E_j}(Y)
 =\frac{D^{k-2}}{\prod_j f_{E_j}}
   \sum_Y\frac{\prod_j\chi_{E_j}(FY)}{d_Y^{k-2}}
 \in\mathbb Z_{\ge0}.
\]

Repeated restriction rows are counted with their multiplicities. This formula uses no conjugation because it computes a unit coefficient, rather than a coefficient at a prescribed output object. The `k=3` case is the already imposed symmetric low Verlinde condition. The `k=4` and `k=5` conditions are further linear integrality constraints on unknown row multiplicities.

For two low products `P=A_E A_F` and `Q=A_G A_H`, the four-point coefficient `tau(E,F,G*,H*)` is their fusion coefficient inner product. Subtracting the contribution of known low output objects leaves the Gram matrix of their nonnegative integer coefficients at all other center simples. Consequently this residual matrix must have nonnegative integer entries and be positive semidefinite. The checker currently records seven principal slices; a simultaneous larger Gram decomposition is a separate strengthening.

## Exact observations on the archived ghosts

- R3895, low frame 8, old active branch 0: all 126 nonunit quartics are integral, but `tau(1,1,1,1,1)=5663/2`. All six quintics using only characters 1 and 2 have this value. Thirteen sextics also fail integrality.
- R3895, old active branches 160 and 165: `tau(1,1,1,1)=85/2`, `tau(1,1,1,2)=73/2`, and `tau(1,1,2,2)=81/2`. The two character-swapped quartics also fail.
- R3895, the stronger 37-phase full-field branch-165 witness of center rank 35: the same five quartic failures persist.
- R5039, both full-field witnesses and their replacements incorporating the common fifth-primary restriction: all 126 quartics, 252 quintics, and 462 sextics pass. Passing these tests is not an existence claim.

Character indices are those of `ExactQuadraticCharacterTable` and are pinned through the source tensor. In R3895, characters 1 and 2 have formal codegree 16. The observations above were replayed with ordinary and optimized Python. They reject individual necessary-data ghosts; they do not show that the entire corresponding active branch is impossible. Indeed, adding the fourth and fifth moment equations to the original frame-eight systems still leaves all four hard branches in the unrestricted integer lattice, so nonnegativity or further equations remain relevant.

## Files and use

- `low_four_point.py`: recomputes all 210 low quartics, 84 triples, and residual fusion-operator Gram slices from exact source characters and witness rows.
- `low_word_moments.py`: computes all nonunit words of each requested length; `--max-degree 6` gives the results above.
- `word_coefficients.py`: exports exact rational and square-root-of-five coefficient pairs for arbitrary specified low words and any supplied orbit domain. Its output columns must be multiplied by the phase multiplicity unit before use in an integer system.
- `word_branch_lattice.py`: checks the fourth/fifth word equations against the existing exact residual-Gram-pruned frame-eight branch lattices.
- `low_four_point_full_field.json`, `low_word_moment_results.json`, and `R7_5_5039_fp5_word_moments.json`: exact computed results.
- `R7_5_3895_full_field_word_coefficients.json`: coefficients for 145 full-field orbits and words `[1,1,1,1]`, `[1,1,1,1,1]`; known-low contributions are `2329/64` and `182129/64`.

The all-word order closure, which can replace an arbitrary degree cutoff by finite lattice saturation in the joint character algebra, is being developed separately under `theory/`.
