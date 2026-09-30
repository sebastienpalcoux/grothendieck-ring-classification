# Exact obstruction for R6_5_1204

The remaining 171 induction profiles for `R6_5_1204` are excluded. The new argument has two parts: a simple-object product eliminates 72 profiles, and integral multiplicities of cyclic-rotation eigenvalues eliminate the remaining 99. It requires no enumeration of modular data or associators.

The complete exclusion replay, including the inherited finite reduction, is:

```sh
OPENBLAS_NUM_THREADS=1 python -O research/exclusions/R6_5_1204/verify_exclusion.py
```

The replay disables `scipy.optimize.linprog` and `scipy.optimize.milp` before importing the system builder. Every certificate check uses explicit exceptions, so Python's optimization flag does not disable verification. It reconstructs the inherited domain and verifies 72 structural plus 99 trace exclusions, with 112 integer-bound steps.

## Inherited hypotheses and completeness

Use the established general-to-pseudo-unitary reduction and complete center-profile reduction in `research/round5/m5_1204/profile_certificate.json`, checked by `software/round5_1204.py`. Its retained profiles are exactly those in `remaining_profiles.json`. The verifier first replays this entire reduction and checks the cached low columns, high columns and every profile multiplicity against the reconstructed domain.

Write the simple basis as `(1,X,Y,Z,W,V)`, with dimensions

\[
1,\quad 3+2\sqrt3,\quad3+2\sqrt3,\quad7+4\sqrt3,\quad6+4\sqrt3,\quad8+4\sqrt3.
\]

The global dimension is \(D=336+192\sqrt3\), with norm \(2304\). All five nonunit second indicators are forced to be +1. The surviving low restriction frame consists of

\[
(1,0,0,0,0,0),\ (1,2,2,4,4,4),\ (1,2,2,5,4,5),
\]

and three copies of \((1,1,1,1,2,2)\). The six possible character assignments differ only by permuting those three identical columns; the builder verifies this equivalence before selecting a representative.

## A forced central lift of W

Every retained profile has exactly one central simple \(U\) restricting to \(X+Y\). Since every base simple is self-dual, uniqueness implies \(U\cong U^*\). Thus \(U^2\) contains the central unit exactly once. The fusion tensor gives

\[
F(U^2)=2\cdot1+2X+2Y+2Z+4W+4V.
\]

After removing the unit, precisely one additional low simple must occur, since its unit coordinate must equal one. Coordinate bounds force its restriction to be \(1+X+Y+Z+2W+2V\). The remaining restriction is therefore

\[
X+Y+Z+2W+2V.
\]

For the functional \(\lambda(c)=c_W-c_Z\), this residual has value one. Every active high restriction column other than the pure \(W\) column has nonpositive \(\lambda\). Consequently a central simple restricting to \(W\) must occur. Exactly 72 retained profiles lack that column and are impossible. `forced_W.json` records this partition; the final verifier independently reconstructs it using explicit checks.

## Integral cyclic-rotation multiplicities

For the remaining 99 profiles, use the full-character field \(K=\mathbb Q(\zeta_{24})\) and moments through order six. The existing `round3_m4.system` provides necessary exact equations for Gram products, first and second indicators, every divisor moment of cyclic rotations of orders three through six, Galois balance, and the modular moment identities for pairs of low simples.

For a central high simple, group its twist by the joint tuple of normalized relative traces of powers one through six. Cauchy prime support is \(\{2,3\}\); `trace_domain` gives the complete finite image of all allowed root orders, including the zero tuple. This is not an assumption that the twist has bounded order. The existing saturated dimension-character theorem (`dimension_block_support.py`) forces order dividing 12 precisely on the columns marked with that bound. Those columns are restricted to the actual twelfth-root tuples; all other columns retain the entire finite trace image.

For every cyclic rotation, a variable counts eigenvalues sharing a joint tuple of normalized relative traces of its divisor powers. These counts are nonnegative integers: normalization affects the coefficients, not the multiplicities. This distinction supplies the new obstruction. Every one of the 112 rounded bounds in the final certificate concerns a rotation-eigenvalue count. Integrality of high-simple trace counts is valid but is not needed for these certificates.

For each profile the builder constructs an exact integer system \(Ax=b\), with \(x\ge0\), after fixing the profile's high-column multiplicities and the proved twist support. It verifies that spectral pruning has not changed the expected column offsets. All remaining rows and labels are reconstructed rather than trusted from the certificates.

## Certificate logic and size

An integer Farkas ray \(y\) proves a nonnegative system impossible when

\[
y^T A\ge0,\qquad y^T b<0.
\]

A proposed upper bound \(x_j\le B\) is certified by adjoining the opposite integral branch \(x_j\ge B+1\) and exhibiting such a ray. A proposed lower bound \(x_j\ge B\) is certified analogously by excluding \(x_j\le B-1\). Each inequality is encoded with one nonnegative slack variable. Previously certified bounds may be used in subsequent steps. A final ray excludes the system with all certified bounds.

The height-six certificate covers all 99 profiles: 86 need one rounded bound and 13 need two. There are 112 bound inferences and 99 final contradictions, hence 211 exact rays. The largest ray has 95 nonzero entries. All sign checks and dot products replay in exact Python integer arithmetic, with no numerical feasibility decision accepted as evidence.

Canonical new files:

- `trace_system.py`: guarded exact necessary-system reconstruction.
- `exact_trace_h6.json`: the 99 complete certificates.
- `verify_exclusion.py`: solver-disabled inherited reduction and full 171-profile exclusion.
- `forced_W.json`: the structural 72/99 partition, independently reconstructed by the replay.

The SHA-256 of `exact_trace_h6.json` is `bc39f082a7811df93fe13de42fb73e5c32c492dcfe9b7faa7c0759c07d54ce65`.

Together with the general reduction and complete inherited profile certificate replayed by the verifier, this proves that R6_5_1204 admits no fusion-category categorification over the original characteristic-zero scope. Earlier exploratory logs and solver statuses are not part of the proof.
