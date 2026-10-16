# Independent audit: projective square-root obstruction, conditional local input

Auditor: rank6_center. Date: 16 October 2026.

I read `PU_2D2_NO_INNER_SQUARE_DRAFT.md` and inspected the rendered original
published EIP pages 506 and 507 (`eip_crossing_506.png`, `eip_loop_507.png`).
The matrix-normalizer argument is correct, conditional on the stated algebraic
dual frame and the two nonzero D coefficients with their specified gauge weights.
This audit does not establish that remaining local bridge or exclude R24.

The normalized crossing display on page 506 is a pivotal one-click relation
with an inverse crossing presentation, not a dagger operation. With the simple
self-dual forms preserved, a tensor autoequivalence that rescales the crossing
by lambda rescales the two compared presentations by lambda and lambda^-1.
Thus lambda^2=1. The sign acquired by the three-crossing K_H loop is lambda;
inverse crossings have the same sign when lambda is plus or minus one.

The projective action of a simple-label-fixing tensor autoequivalence on
H=Hom(r tensor r,r) is well-defined on tensor-isomorphism classes. Changing
Fr -> r by a scalar changes the H action by an overall scalar; monoidal
natural transformations have the same effect. Composition gives composition
in PGL(H). Thus showing that the square of the H action is scalar really
excludes a tensor-isomorphic square root of an inner autoequivalence whose
H action is not scalar.

If lambda=-1, the H action exchanges the two one-dimensional K_H eigenlines;
its matrix is antidiagonal and its square is scalar. If lambda=1, preservation
of the nondegenerate paired theta form gives diag(u,u^-1) on H, and similarly
diag(v,v^-1) on J with the stipulated compatible gr form. Invariance of nonzero
y,z having weights u^-2 v^2 and u^-2 v^-2 yields u^4=1, so the H square is
again scalar. No positivity or Hermitian diagonalization is needed here.

For the Ad(g) identification, choose q:g r g* -> r by moving g* through r
using the chosen crossing and then evaluating g g*. Expanding
q Ad_g(f) tensorator (q^-1 tensor q^-1) contracts the adjacent evaluation and
coevaluation pairs to precisely the closed g strand crossing the three r legs
in EIP's K_H diagram on page 507. Reversing orientation can replace K_H by
its inverse; since K_H^2=-I these define the same projective operator. Changes
in q contribute only an overall scalar. Hence Ad(g) acts projectively as the
nonscalar matrix diag(i,-i).

The local input to this audited implication is the full C-linear dual-frame derivation of the
restricted tetrahedral normal form and the three retained diagonal source resolutions forcing
y,z nonzero. Categorical duality fixes the scalar i, while dagger conjugation
does not; any required loop-eigenlabel swap must be proved diagrammatically.
The draft correctly isolates this issue rather than asserting automatic
complexification of every unitary coefficient identity.

## Final-packet status

The final theorem is now `R24_PROJECTIVE_INNER_SQUARE_PROOF.md`. The separate `R24_INCOMING_LOOP_INDEPENDENT_AUDIT.md` and `R24_RESTRICTED_COEFFICIENT_INDEPENDENT_AUDIT.md` supply the local paired-loop and coefficient premises isolated above. The final restricted argument uses three diagonal resolutions, not the earlier four-identity formulation; it requires neither a common decorated cubic phase nor any hat equation. My independent approval here remains the normalized crossing, projective normalizer, composition, and Ad(g) identification. Together with the separately audited local premise, that approved implication yields the stated absence of a projective inner square root.
