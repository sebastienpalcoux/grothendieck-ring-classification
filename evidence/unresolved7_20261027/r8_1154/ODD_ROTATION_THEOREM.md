# R8_3_1154: all six trivalent rotations are necessarily identity

27 October 2026. **The source ring remains unresolved.** This is a new
necessary categorical theorem, not an associator construction.

## Statement and inherited scope

Apply the established general-complex spherical/Galois gate to any
hypothetical categorification of R8_3_1154 and work in its positive
spherical representative C. In the frozen numbering its noninvertible
simples are X1,X2,X4,X5,X6,X7. Each has dim Hom(1,Xi^3)=2. We prove

    nu_3(X1)=nu_3(X2)=nu_3(X4)=nu_3(X5)=nu_3(X6)=nu_3(X7)=2.

Every cyclic rotation on these two-dimensional trivalent spaces is
therefore identity: two cube roots sum to 2 only if both are 1.
The theorem holds for all three remaining center patterns 6971,8766,8772.
It does not eliminate those patterns or construct a category.

## A dual-lift lemma for odd indicators

Let F:B=C^{C2}->C be the forgetful tensor functor for an actual action by
pivotal tensor autoequivalences, with compatible spherical structures.
Let u be the canonical sign object of the central Rep(C2). Suppose x is
simple, F(x)=X is simple, and x*=ux. For odd n, the two character
subspaces of Hom_C(1,X^n) identify with

    Hom_B(1,x^n) and Hom_B(1,(ux)^n).

Changing the equivariant lift from x to ux multiplies the equivariance
on its n-th tensor power by (-1)^n, interchanging invariants and
anti-invariants. Both subspaces are preserved by cyclic rotation.
The pivotal functor F, including its canonical identification F(u)=1,
intertwines the rotations. This uses the symmetric bosonic tensor
constraints of Rep(C2), not merely a based central involution.

Higher spherical indicators satisfy nu_n(x*)=nu_n(x); this is stated
explicitly in Ng--Schauenburg, *Frobenius--Schur indicators and exponents
of spherical categories*, arXiv:math/0601012, Remark 4.2. It also follows
from their Theorem 4.1 and I(x*)=I(x)*, since dual center simples have the
same dimension and twist. Consequently

    nu_n(X)=nu_n(x)+nu_n(ux)=2 nu_n(x),  n odd.          (1)

If Hom_B(1,x^3) is one-dimensional, this gives

    nu_3(X) in {2,2 zeta_3,2 zeta_3^2}.                (2)

This is a decomposition of actual morphism spaces and their rotations.
It does not claim that arbitrary tensor functors preserve numerical
indicators. The categorical argument received separate reviews from the
audit_fs2 and audit_parity investigators in this research pass.

## Apply the actual rank-ten equivariantization reduction

The preceding investigation proved the following conditional categorical
reduction. Adjoin Semion to C, cancel its pointed C2 anomaly, and take
bimodules over 1+(g tensor s). The dual B is C^{C2} for the coherent
conjugation action, not an action inferred only from a permutation of
labels. Pseudo-unitarity makes its action and F preserve canonical
positive pivotal structures.

Its unique surviving based ring has basis

    1,u,v,uv,x,ux,vx,uvx,y,vy,

with x*=ux and

    x^2=u+(1+u+v+uv)x+2(1+v)y.

The functor maps x,ux to X4 and vx,uvx to X5. Both third vacuum
multiplicities are 1, and (vx)*=uvx. Thus (2) applies to X4 and X5.
The complete inherited categorical proof, including elimination of the
alternative all-selfdual rank-ten ring, is
`evidence/unresolved10_20261027/r8_quartic/R1154_NOTES.md`.

## Exact discrete third-indicator screen

Use the existing complete center domain at
`evidence/rank8_frontier_20261021/central_integrality/integer_gram_1154.json`:
five distinguished restriction columns, sixteen high restriction types,
and surviving pattern indices 6971,8766,8772. No new enumeration is run.

The short test imposes induction Gram equations, each frozen pattern's
exact high multiplicities, first through third rotation traces,
distinguished-character STS, and the established four packet twists
(i,i,-i,-i). Equations are averaged to Q(sqrt(5)). Since that field and
Q(zeta_3) are disjoint, the normalized trace of a cube-root sum is its
real part. Hence (2) leaves exactly {-1,2}^2 for (X4,X5).

For each pattern, exact integer Farkas certificates eliminate the three
choices other than (2,2). This forces both actual indicators to equal 2.
Each other noninvertible's third vacuum multiplicity is two, so its
averaged indicator belongs to {-1,1/2,2}. Duality equates X1 with X2,
and the actual inner autoequivalence Ad(g) equates X6 with X7. There are
only nine choices for (X1,X6) once X4,X5 are fixed. Exact certificates
eliminate all eight choices other than (2,2), on all three patterns.

Two certificates were obtained by transferring an existing ray to
another right-hand side. The verifier checks its inequalities directly
there; no categorical symmetry is inferred from that numerical transfer.
All six retained branch records (three patterns in each of two stages)
have exact rational feasibility witnesses.

The finite trace-type list is complete through height three, including
unbounded twist orders. It uses the established exponent prime support
{2,3,5}; sufficiently high prime powers give zero normalized moments
through that height. This is not a bound on the actual FS exponent and
does not place all twists in Q(sqrt(5)).

## Verification and remaining gap

Run from the repository root:

    python evidence/unresolved7_20261027/r8_1154/verify_odd_rotation.py
    python -O evidence/unresolved7_20261027/r8_1154/verify_odd_rotation.py

The replay regenerates both exact matrices, checks all integer Farkas
rays and rational primal vectors, verifies complete branch coverage and
the source tensor hash, and rejects a zero-ray negative control. It uses
no optimizer and does not rely on removable assertions. Runtime is a few
seconds. A separate investigator rebuilt the first-stage matrices and
checked their twelve certificates independently, then replayed both
stages. See `../audit_parity/` for that independent review.

`build_odd_rotation_system.py` uses the existing exact engine with the
frozen high-column domain. `replay_dependencies/` restores small Python
dependencies from frozen public commit
6a426acf6465dd674351be92dcca41b72f371521. The `probe_...` discovery scripts
use numerical optimization only to propose certificates; exact replay
determines the accepted statement.

All three center patterns remain feasible after this restriction.
Their remaining simultaneous fusion operators, associators, and algebra
multiplications are still unknown. Identity of the trivalent rotations
alone neither constructs a separable algebra nor provides a model of
R8_3_1154. Accordingly its classification status remains unresolved.
