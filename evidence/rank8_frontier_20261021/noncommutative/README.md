# Noncommutative rank-eight frontier: central support and full rotations

These new computations concern R8_3_721, R8_3_928, R8_3_941, and
R8_3_1154. They do **not** give a categorification or a new general-complex
exclusion. The numerical searches are separated from exact acceptance.
In particular, an unsuccessful separating-ray search is not labelled feasible.
`certified_*.json` records an exact rational primal witness when feasibility
of the stated finite relaxation has actually been proved.

## Central-image refinement

Let B be the induction Gram matrix, B_ij=[F I(X_i):X_j]. If M is the
restriction matrix from the Drinfeld center, B=MM^t. For u in ker(B),
0=u^t B u=||M^t u||^2. Thus **every** restriction column c satisfies
u^t c=0, including the distinguished constituents of I(1). Equivalently,
the class of a central object commutes with every basis object. These
equations are especially useful before enumerating distinguished columns;
the earlier independent-coordinate minima did not impose them.

For an irreducible representation E of the fusion algebra, the distinguished
column begins with dim(E), and its pseudo-unitary dimension is D/f_E.
Every one of the four algebras has shape C^4 plus M_2(C). The column for
the matrix block begins with 2. It contributes its square **once** to MM^t;
its contribution to the unit row is multiplied by 2.

The exact central-support calculation gives:

| Ring | Four nonunit distinguished-column counts | Weighted low frames | Frames surviving Gram and first moment bounds |
|---|---|---:|---:|
| R8_3_721 | 7, 5, 5, 2 | 13 | 1 |
| R8_3_928 | 1, 1, 1, 1 | 1 | 1 |
| R8_3_941 | 1, 1, 1, 1 | 1 | 1 |
| R8_3_1154 | 9, 7, 2, 6 | 59 | 4 |

`verify_independent.py` derives the center from all multiplication
commutators, enumerates its nonnegative integral coordinate box, and only
then checks dimensions. This independent enumeration agrees with the
Gram-kernel implementation. Published unitary models R8_3_448, R8_3_458,
and R8_3_715 are positive controls.

## Rotation search and exact residual boundary

The search imposes the complete residual Gram matrix, normalized relative
cyclotomic traces, the first and second indicator equations, and joint
cyclic-rotation spectra of tensor powers. The quadratic implementation
`full_rotation.py` adds all divisor-power compatibility equations, instead
of retaining only separate rational upper/lower bounds. The quartic cases
use the existing exact Q(sqrt(2),sqrt(3)) relative trace implementation with
the new central-support columns.

Exact dual rays show the following **pseudo-unitary necessary conditions**:

* R8_3_721: all self-dual simples have second indicator +1; in particular
  the otherwise undetermined object 7 has indicator +1.
* R8_3_928: the nontrivial invertible object 7 has indicator -1.
* R8_3_941: the nontrivial invertible object 3 has indicator +1.
* R8_3_1154: the nontrivial invertible object 3 has indicator -1 and
  object 4 has indicator +1. Of the four Gram-compatible low frames,
  only frames 30 and 31 survive, with indicators
  (0,0,-1,+1,+1,+1,+1) on objects 1 through 7.

The last conclusions are proved by exact rays against all complementary
branches. Complete enumeration here means all low frames and all second
indicator choices within the displayed finite relaxation. It does not mean
all associators, all possible centers, or all models have been enumerated.

Exact rational primal witnesses establish that the surviving branches pass
the full joint relaxation through height 6 for R721, R928, and R941 and
through height 8 for both surviving R1154 frames. R721 additionally has
an exact witness through height 12. Higher-height attempts with unresolved
numerical reconstruction remain explicitly undecided in their receipts.

At height12, unscaled floating-point optimization initially declared the
R721 positive-indicator system infeasible. Scaling variables by the exact
upper bounds furnished by positive Gram/count rows recovered an exact
feasible solution. This is why no numerical infeasibility is accepted.

## Full-character modular equations

Write m_E=dim(E), and let chi_E denote the ordinary matrix trace character,
including the two-dimensional representation. For a central simple Z with
restriction column c_Z, Deshpande's central-character description gives

    S_(A_E,Z) = D/(f_E m_E) chi_E(c_Z).

Here S is unnormalized, S_(1,Z)=dim(Z), and D=FPdim(C). The distinguished
objects A_E all have twist1. The Drinfeld center has positive Gauss sum D,
so STS=D T^(-1) S T^(-1) yields, for every pair E,F,

    sum_Z chi_E(c_Z) chi_F(c_Z) theta_Z
       = f_F m_F chi_E(c_(A_F)).

These are quadratic in the restriction column and linear in the joint
column/twist multiplicities. They are additional equations beyond the
ordinary indicator equations, which are linear in the restriction column.
`character_modular.py` checks full character orthogonality, enumerates all
equal-codegree/multiplicity assignments while fixing the unit, requires
symmetry of the distinguished S submatrix, and adds the displayed equations.

The exact height6 consequences are:

* R721: one of the two symmetric character assignments is excluded; the
  other has an exact rational feasible witness.
* R1154: frame30 is excluded, leaving only frame31 with its forced indicator
  assignment. Frame31 has an exact rational feasible witness.
* R928 and R941: their remaining assignments have exact rational feasible
  witnesses.

Published unitary models R458 and R715 retain exact feasible branches under
the same added equations. Their other indicator/character assignments are
also recorded, including exact exclusions where obtained.

Additionally, S_(A_E,Z)/dim(Z) is an eigenvalue of the integral fusion matrix
of A_E in the center. `spectral_filter.py` therefore rejects a high column
if any such number is not an algebraic integer. For R721 it removes two
columns with eigenvalue plus or minus sqrt(17)/2, having monic polynomial
x^2-17/4. The surviving modular branch still has an exact feasible witness.

## Complete integral Gram patterns for R721

The single surviving R721 low frame has ten high column types. Its Gram
equations have rank6. Exhausting the 240-point box of free coordinates
leaves exactly four nonnegative integral multiplicity vectors, in the saved
high-column order:

    (4,0,0,1,4,8,0,0,0,0)
    (4,0,0,1,0,8,0,0,1,0)
    (0,1,0,1,4,8,0,0,0,0)
    (0,1,0,1,0,8,0,0,1,0).

`integral_gram.py` independently re-enumerates this complete finite box.
Each of the four patterns has an exact rational witness for the full joint
rotation relaxation through height12. This is stronger evidence than a
single feasible convex combination of different integral Gram patterns,
but it still does not construct fusion rules or associators for the center.
Each of the four patterns also has an exact rational witness for the joint
height6 rotation system with the full-character STS equations and its high
multiplicities fixed, in `integral_modular_721_h6.json`.

`central_fusion.py` adds a separate tensor-product test for every one of
these four complete Gram patterns. For all ten unordered pairs of the
four nonunit distinguished central objects, it requires the forgetful
tensor equation and a common nonnegative set of low fusion coefficients.
Exact duality-invariance of all five characters makes these distinguished
objects selfdual; Frobenius reciprocity therefore makes the coefficients
of three nonunit low objects symmetric in all three labels. The unit
coefficient is the Kronecker delta. All four patterns pass this combined
rational feasibility test, with exact witnesses in
`central_fusion_721.json`. High objects with the same restriction column
are aggregated. Neither integrality of the center fusion coefficients nor
their full associativity has been imposed, so this is a necessary
relaxation and not a constructed center fusion ring.

`verlinde_low.py` strengthens this test by calculating all twenty low
fusion coefficients from the known complete S rows:

    N_(A_E,A_F)^(A_G) = D^(-2) sum_Z S_(A_E,Z) S_(A_F,Z) S_(A_G,Z)/dim(Z).

The distinguished objects are selfdual, so no dual label is needed on the
third factor. All four R721 Gram patterns, under both symmetric character
assignments, give nonnegative integer coefficients. Their tensor-product
systems remain exactly feasible when those coefficients are fixed, as
recorded in `verlinde_low_721.json`. This uses the ordinary Verlinde
formula, equivalently Deshpande, *On twisted Verlinde formulae for modular
categories*, Theorem1.1 with M=C, https://arxiv.org/abs/1811.08447.

## Complete integral Gram and cubic filters for R1154

The independent exact enumeration in
`../central_integrality/integer_gram_1154.py` exhausts all integral Gram
patterns for the unique surviving low frame31. Affine bounds reduce the
2,634,508,800-point naive box to 40,583 visited search nodes, yielding
exactly 14,211 solutions of all original Gram equations.
`central_integral_filters.py` checks every solution. Nonnegative integrality
of all twenty cubic Verlinde coefficients leaves 1,238 patterns. As a
separate test, the known eigenvalues S_(A_E,Z)/dim(Z) of the integral center
fusion matrices must have Galois-invariant multiplicities. This leaves
7,274 patterns, including all 1,238 cubic survivors.

For every cubic survivor, `cubic_tensor.py` tests the forgetful tensor
equations for all ten distinguished pairs with those exact integer low
coefficients fixed. It exhausts the rational cones using all nonsingular
bases of the active high-column space. All 1,238 patterns pass, with 12,380
exact nonnegative rational witnesses in `cubic_tensor_1154.json`. These
receipts completely cover their stated finite domains. They do not impose
integral high fusion coefficients, full associativity, or associators, and
therefore do not establish categorification.

## Matrix blocks and pointed bimodules

`matricial_structure.py` independently checks the duality involution on the
four scalar characters and the remaining matrix block. R928 has symplectic
matrix involution; the other three have orthogonal matrix involution.
For R928 and R941 the nontrivial invertible g is central on labels. In the
rational quotient g=-1:

* R928 has basis 1,a,b,c with a^2=b^2=c^2=-1 and pairwise
  anticommutation. It is the Hamilton quaternion algebra.
* R941 has squares (-1,+1,+1), with the corresponding split-quaternion
  multiplication, hence M_2(Q).

This rational distinction is information absent from scalar characters and
formal codegrees. **It is not an obstruction by itself:** the group ring of
the quaternion group already occurs as the fusion ring of Vec(Q8).

The exact pointed-bimodule check enumerates every C2 x C2 orbit and its
stabilizer. R928 and R941 have four orbits of size2, each with diagonal
stabilizer. R1154 has orbit sizes2,4,2, with diagonal or trivial stabilizer.
For both pointed associator classes omega=0,1, the restriction of
omega(left) omega(right)^(-1) is trivial on every stabilizer. Thus this
complete stabilizer-cohomology test yields **no obstruction**. In the
canonical pseudo-unitary structure, the forced invertible indicators above
mean that the pointed associator is nontrivial for R928/R1154 and trivial
for R941. In particular, an algebra 1+g is available for R941 but not for
R928/R1154 by this route. No Morita-dual fusion rules are claimed from this
observation alone.

## Scope and sources

The dimension equation D/f_E uses pseudo-unitarity. These new necessary
conditions have not been lifted through all oriented sphericalizations and
must not be promoted to general-complex exclusions. Exact feasible
relaxations are not categorical constructions.

The mathematical inputs are the definition of the Drinfeld center and
Frobenius reciprocity; the distinguished induction constituents in Ostrik,
*Pivotal fusion categories of rank 3*, Theorem2.13; and the center-twist
indicator identities of Ng--Schauenburg, *Frobenius--Schur Indicators and
Exponents of Spherical Categories*, https://arxiv.org/abs/math/0601012.
Pointed bimodule obstruction theory is treated in Etingof--Nikshych--Ostrik,
*Fusion categories and homotopy theory*, https://arxiv.org/abs/0909.3140.
The new central-image argument above is elementary linear algebra and does
not require a new categorical hypothesis.
The full-character modular input is Deshpande, *On centers of bimodule
categories and induction-restriction functors*, section2.7 and
Corollary2.18, https://arxiv.org/abs/1611.04486. Ostrik's paper is available
at https://arxiv.org/abs/1309.4822.

Read-only replay:

```
python evidence/rank8_frontier_20261021/noncommutative/verify_independent.py
python evidence/rank8_frontier_20261021/noncommutative/verify_all.py
python -O evidence/rank8_frontier_20261021/noncommutative/verify_all.py
```

All acceptance checks use explicit exceptions and remain active under
`python -O`. The published rank8_m3_20261021 evidence tree is imported
read-only and has not been edited by this work.
