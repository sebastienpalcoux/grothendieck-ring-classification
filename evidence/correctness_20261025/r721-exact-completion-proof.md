# R8_3_721: direct fusion completion without census completeness

Exact proof for the 25 October 2026 correction release, integrated into the current manuscript. The original pre-publication audit snapshot is preserved separately; no fusion tensor or classification status changes.

## Proposition

Let D be the actual unitary category of bimodules over the inherited algebra `1+rho` in the C2 de-equivariantization of the existing GH(C8) category. Use the independently audited rank-selection argument and its unique rank-eight forgetful matrix B. Then the necessary unit, duality, Frobenius-reciprocity, dimension and free-induction equations have exactly two nonnegative integral tensor solutions. They differ only by swapping two equal-dimension basis objects. Both are associative and have the full fusion tensor of R8_3_721.

Consequently D realizes R8_3_721 independently of upstream census completeness. This does not classify its associators or assert novelty up to tensor equivalence.

## Actual categorical input

The existing construction supplies the source category C, its connected separable algebra A, and therefore D before any tensor completion. Its source rules are

\[
g^4=1,\qquad g\rho=\rho g^{-1},\qquad
\rho^2=1+2\sum_{i=0}^{3}g^i\rho,\qquad \dim(\rho)=4+\sqrt{17}.
\]

The existing categorical proof and finite Gram factorization force rank eight. Label the actual dual simples

\[
(1,a_0,a_1,b_0,b_1,d,c,e)
\]

with dimensions `(1,a,a,a+1,a+1,2a+1,2a,2a+2)`, where `a=(3+sqrt(17))/2`. The column order agrees with `r721_dual_fusion.py`. The final verifier freshly checks that all eight columns are precisely the unique recorded rank-eight Gram factor, that the unit column is the underlying object `1+rho`, that all 64 entries of `B B^T` equal the directly reconstructed free-bimodule Gram matrix, and that all eight dimensions equal the underlying dimensions divided by `dim(A)`.

This completion does not re-prove the external GH(C8) existence theorem or the previously audited rank-selection/Q-system-vertex argument. It verifies the exact passage from those categorical inputs to the mandatory completion data.

## Exact finite proof

Free induction satisfies `I(X) tensor_A I(Y) = I(X tensor A tensor Y)`. Accordingly every actual fusion tensor obeys

\[
\sum_{x,y}B_{ix}B_{jy}N_{xy}^{z}
=\sum_{a\in\{1,\rho\}}\sum_{u,t}
N^{\mathcal C}_{ia}{}^uN^{\mathcal C}_{uj}{}^t B_{tz}.
\]

All 512 such equations are imposed, together with unit, duality, Frobenius reciprocity and both rational components of the dimension equations. The unique dimensions force `1,d,c,e` to be self-dual. Each equal-dimension pair is either fixed or exchanged, yielding exactly four possible dualities. No commutativity assumption is imposed.

The existing rational covectors are freshly checked against the reconstructed equations in all four cases: each covector dominates its chosen coefficient and has right-hand side at most three. Thus **every** coefficient of the actual category is an integer in `{0,1,2,3}`. No bound is assumed from the census.

The equation system is reduced over the rationals. Its free coordinates are themselves actual tensor coefficients, so they have the same four-value domain. After clearing denominators, every other coefficient has the form

\[
 n_r=(c_r+\sum_j a_{rj}x_j)/D,
 \qquad 0\le n_r\le3,\quad n_r\in\mathbb Z.
\]

For a candidate value of one free coordinate, exact minimum and maximum sums over the other remaining domains give a necessary interval. A value is removed only if that interval cannot meet `[0,3D]`. The implementation repeatedly applies these deductions, checks the necessary gcd congruences, then branches over every remaining value of a selected coefficient. Fixed coordinates are checked for exact integrality. There is no floating point, SAT solver, MILP solver, native helper, associativity pruning, omitted branch, or time budget in this final proof.

The entire search has only **14 nodes**, including internal and rejected nodes:

| Duality on a-pair | Duality on b-pair | Free coordinates | Search nodes | Integral completions |
|---|---|---:|---:|---:|
| Both fixed | Both fixed | 22 | 3 | 0 |
| Both fixed | Exchanged | 19 | 3 | 0 |
| Exchanged | Both fixed | 19 | 5 | 2 |
| Exchanged | Exchanged | 16 | 3 | 0 |

The explicit branch choices are especially small:

- First branch: `N[a1,b1]^d` is either zero or one; each choice gives an affine contradiction.
- Second branch: `N[a1,d]^c` is either zero or one; each choice gives an affine contradiction.
- Third branch: `N[d,c]^c` lies in `{1,2}`; two is impossible. With value one, `N[a0,d]^b1` is zero or one, and each choice forces a complete tensor.
- Fourth branch: `N[d,c]^c` is one or two; each choice gives an affine contradiction.

The machine-readable receipts record every branch, the propagated domains, and the exact rejected affine row. All rejected leaves use only the affine constraints. On each of the two surviving tensors, the verifier separately checks all 4,096 associativity identities, all 512 induction identities, the unit, exact duality, Frobenius reciprocity and the dimension character.

The two tensors are exchanged by `(0,1,2,4,3,5,6,7)`; alternatively, by `(0,2,1,3,4,5,6,7)`. Thus they are one based-ring class. Only **after** exhaustive generation is complete does the script read the census to name this class. All 512 coefficients match R8_3_721 under the model-to-census order `(0,1,2,4,6,3,5,7)`, up to the harmless equal-dimension relabeling.

The manuscript's 832 stated linear conditions include unit/duality overlaps; the implementation emits 809 rows after coalescing 23 duplicate overlaps. These are the same necessary conditions.

## Evidence and independent checks

- `r721_exact_completion.py`: final solver-free exact proof, with no census loaded before exhaustive completion. Its pure source definitions are extracted verbatim from the existing equation producer, avoiding an unrelated import that loads census data.
- `r721-exact-completion.json` and `r721-exact-completion-optimized.json`: both PASS on the final source; every field agrees after removing timing and the optimization-mode flag. Every assertion relevant to acceptance uses explicit exceptions and remains active under `python -O`.
- `r721_completion_controls.py` and `r721-completion-controls.json`: 240 small independently enumerated Cartesian domains agree exactly with the new interval/congruence search, under optimized Python.
- `rank8-r721-bounded-completions.py` and its normal/optimized receipts: independent finite bit-vector enumeration gives the same four branch counts and exact tensor class. The rank-six auditor reviewed its orbit coverage, safe integer widths, equation deduplication and exhaustive blocking.
- `r721_exact_dfs.cpp`, its driver and receipts: a separately implemented exact native interval/congruence search gives the same node counts and solutions. This is corroboration only; the final proof requires no native binary.

The rank-seven and rank-eight auditors independently reviewed the final Python completion algorithm and its completeness argument. No false model was found. The current manuscript uses this exact completion argument.
