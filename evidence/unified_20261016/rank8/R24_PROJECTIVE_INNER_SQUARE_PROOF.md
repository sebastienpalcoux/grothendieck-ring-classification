# A projective inner-square obstruction for R8_2_24

Status: accepted after independent categorical and arithmetic audits. Criterion: `projective_inner_square_obstruction`. This proof is theoretical. Its replay binds the source tensor and verifies only finite field/index arithmetic; the categorical theorem is established by the argument below.

The theorem is that **R8_2_24 admits no complex fusion categorification**. The argument proves a local projective symmetry obstruction for every pseudo-unitary categorification of the rank-four 2D2 ring. It does not assume such a category is unitary or classify all its associators.

## General scope and source tensor

The immutable tensor digest is
`2b4780441d9590e8e7269cd82b7675aa75cec11c39bd3e94bb372cca1ada6738`.
Its neutral basis(1,g,r,gr) is(0,7,5,6). The odd invertible a=1 has inverse2
and square g=7. Conjugation by a fixes each neutral simple label. The tensor
therefore supplies the actual tensor functor T=Ad(a) on the neutral category,
with coherent T² isomorphic to Ad(g). This is a categorical consequence of
inner conjugation, not an inference from a numerical ring automorphism.

The whole source ring has exactly two FP dimensions,1 and2+sqrt5. By
Schopieray, *Categorification of integral group rings extended by one dimension*,
Lemma3.1, any complex categorification is Galois conjugate to a pseudo-unitary
one. Apply that conjugation to the entire category and its inner functor. Its
neutral subcategory is then pseudo-unitary. It is enough to contradict the
required inner square in this setting.

## Indicators are forced generally

For the neutral category, d=2+sqrt5 and D=20+8sqrt5. Its four formal codegrees
are D,Dbar,4,4. In the center, the unit and its nontrivial quadratic Galois
partner give a twist-one difference vector whose exact compressed S eigenvalue
is

    1/D-1/Dbar=-1/sqrt5.

The primitive-character compression bound1/sqrt5 is saturated. The audited
conductor-equality lemma therefore puts every outside-I(1) central simple
with nonzero sqrt5-coordinate in dim(A)/D at twist order dividing5.

For completeness, the character-weighted Galois indicator consequence is the
following. If ell(z) is a rational coordinate in the quadratic character
component of z/D and supported twists divide conductor f, then for every k
coprime to f,

    sum_X ell(dim X)*nu_k(X)=chi_f(k)*ell(1).

To prove this, apply a cyclotomic automorphism tau of exponent k modulo f to
the first induction trace. If pi and epsilon are its modular Galois label
permutation and signs, then
z_(pi A)=epsilon_A(D/tau D)tau(z_A),
ell_(pi A)=epsilon_A chi_f(k)ell_A,
and theta_(pi A)=tau²(theta_A). Reindexing the transformed trace by pi replaces
the twist exponent k by its inverse modulo f and contributes chi_f(k).
Cancelling tau D yields the displayed identity, because inversion permutes the
units modulo f and preserves their quadratic character. This argument uses no
involutivity of pi and no unitarity of the underlying category.

Here ell can be scaled to source weights(2,2,-1,-1). Taking k=2 gives

    2+2nu2(g)-nu2(r)-nu2(gr)=-2.

All three indicators are signs, so necessarily nu2(g)=-1 and
nu2(r)=nu2(gr)=1. Taking k=3 gives nu3(r)+nu3(gr)=4. Each cubic invariant
space has dimension2, and a cubic rotation has root-of-unity eigenvalues.
Their sum has maximal possible real part, so every cubic-rotation eigenvalue is 1.
Only the ordinary r rotation will be used below.

## Hypotheses and spaces

The neutral category is pseudo-unitary with fusion ring

    g²=1, gr=rg, r²=1+2r+2gr,

dimension d=2+sqrt5, nu2(g)=-1, nu2(r)=nu2(gr)=1, and nu3(r)=2. Let

    H+=Hom(r²,r), J+=Hom(r²,gr),
    H-=Hom(r,r²), J-=Hom(gr,r²).

Each opposite pair has the nondegenerate composition pairing. Fix the oriented
self-duality generators and the normalized crossing of EIP Section3.1.1. The
crossing's pivotal one-click rotation is its inverse. Its bend parameter is
mu=nu2(gr)/nu2(r)=1.

## Explicit paired-space table

All transposes and form defects below are relative to the canonical pivotal structure of the functor Ad(g), not a naively chosen palindrome form on gXg. In particular the unit identification q_1=ev_g has form defect s_1=1. The identifications q_r=(id_r tensor ev_g)(c tensor id_g) and q_gr=id_g tensor q_r have defects s_r=mu and s_gr=mu*lambda_g: cancelling inverse crossings leaves the defining mu two-crossing diagram, with one additional reversed g form in the second case.

The outgoing loop K+ is the action of Ad(g), with the chosen identifications
on its source and target. The incoming loop K- is the action of that SAME
functor on the opposite Hom space, using the inverse identifications. Since a
functor preserves composition,

    <K+ f,K- h>=<f,h>,             K-=(K+)^(-t).

This is not the ordinary pivotal transpose of K+. In the diagram, the incoming
wrapping loop is the dual of the inverse outgoing loop. Cancelling the adjacent
g-evaluation/coevaluation identifies it with the incoming loop used in the
partial-bend covariance equations.

The right bends R+ and R- are linear maps between opposite Hom spaces. Their
theta pairings are symmetric because the incident simple objects r and gr
have second indicator+1. The loop/bend isotopies give

    K_H+ R_H = R_H K_H-,        (K_H+)²=-I,
    K_J+ R_J = -R_J K_J-,      (K_J+)²= I.

Consequently one may choose paired eigenbases with

    K_H+=diag(i,-i), K_H-=diag(-i,i),
    K_J+=diag(1,-1), K_J-=diag(1,-1),
    R_H+=R_H-=R_J+=R_J-=E,    E=[[0,1],[1,0]].

For example K_H+ E=E K_H- and K_J+ E=-E K_J-. The hyperbolic pairings are
nondegenerate and pair the opposite eigenlines, so each eigenvalue occurs once.
Residual gauges are diag(u,u^-1) on H and diag(v,v^-1) on J.

On H the cubic rotation is the identity because its dimension and trace are2.
Thus L_H+=L_H-=E. On J we do not fix the left-bend matrices or compare
incoming and outgoing cubic rotations. Loop covariance merely makes the
outgoing cubic rotation diagonal, with two eigenphases omega_alpha,0 and
omega_alpha,1, each a third root of unity. No equality of those phases is
assumed or needed.

All noninvertible incident objects have equal dimension d, so the above partial
bends have no dimension-ratio factors. The unit-channel cup normalization is
kept separately and produces the explicit 1/d terms in the resolutions.

## Tetrahedral coefficient slots

FG Lemma3.13(ii), Proposition3.22, and Corollary4.9 apply. For the A and D
tetrahedra, inserting the above bend matrices gives the odd dual-slot flip

    p(i,j,k,l)=(k,1-j,i,1-l).

It has scalar factor lambda_r^(j+l)=1. The even maps are

    c(i,j,k,l)=(j,1-k,1-i,l),
    q(i,j,k,l)=(1-k,1-l,1-i,1-j).

Their relations are

    A_v=A_c(v)=A_q(v),
    D_1111=-D_0000,       D_1010=-D_0101.

Only those two diagonal D instances of the even flip are used. In each,
i=k, so the decorated phase cancels separately as
omega_alpha,i cubed=1. Loop covariance kills all odd-parity coefficients.
These eight zero equations and two diagonal relations leave exactly six D
parameters. Together with A's full even symmetries, their complete solution is

    A = [[r0,0,0,A],[0,r0,r0,0],[0,r0,r0,0],[a,0,0,r0]],
    D = [[x,0,0,Z],[0,X,y,0],[0,Y,-X,0],[z,0,0,-x]].

The composition-dual slot is obtained by p. Thus a and A, x and X, y and Y,
z and Z are paired coefficients, initially independent. No scalar complex
conjugation is asserted. The finite slot table is checked in
`verify_r24_projective_inner_square.py`; its proof uses no value or equality of the decorated cubic phases.

## The corner parameter has two possibilities

The source fusion-ring corner acts on its four-dimensional annular module
A_(1,r). In EIP's ordered two-trivalent-space basis, the g and r matrices are

    P=[[0,I],[I,0]],       R=[[phi,phi0],[phi0,phi]].

Tetrahedral A symmetry makes phi=2r0 I. On the P=+1 subspace the eigenvalues
of R belong to {d,dbar}, where dbar=2-sqrt5. The d-character corresponds to the central unit,
which has no r in its forgetful image. It is therefore absent from A_(1,r), so

    phi+phi0=dbar I.

On the P=-1 subspace, the source relation R²=I+2R+2PR reduces to R²=I.
Consequently

    (phi-phi0)²=I,       (4r0-dbar)²=1,
    r0=(2-sqrt5+tau)/4, tau in{+1,-1}.

This is ordinary semisimple corner-character theory, not a C*-representation
argument.

## Only three diagonal resolutions are needed

Apply the first double-tree resolution on published EIP p539 at
(k,l,k',l')=(0,0,0,0). The A terms are two copies of r0², and the D terms are
two copies of xX. The unit channel contributes1/d=sqrt5-2. Thus

    1=2r0²+2xX+(sqrt5-2),
    r0²+xX=(3-sqrt5)/2.                         (1)

Apply the third resolution at(0,0,0,0), respectively(0,1,0,1). Each contraction
is with the composition-dual tree basis. The two equations are

    xX+zZ=1/2,             xX+yY=1/2.           (2)

Only diagonal contractions are used, so a phase on a vertex is paired with its
reciprocal phase on its dual; each unknown decorated phase cancels individually with its dual.
Equations(1)--(2) and the two values of r0 give

    yY=zZ=(sqrt5-1)/8       if tau=+1,
    yY=zZ=(3sqrt5-5)/8      if tau=-1.

Both values are nonzero. Thus y and z are nonzero in every possible branch.
The second/fourth indexed displays, every hat off-diagonal coefficient, all
fourth indicators, and the full reduced scalar ideal are unnecessary.

## Projective square contradiction

The two nonzero coefficients have residual gauge weights u^-2 v² and
u^-2 v^-2. A label-fixing tensor auto preserves the normalized crossing up to
lambda=±1. Its H action is antidiagonal if lambda=-1, so its square is scalar.
If lambda=+1, it preserves both loop eigenspace pairs, acts by the diagonal
gauges above, and preservation of y,z forces u^4=1. Its H square is again
scalar. But Ad(g) acts projectively by diag(i,-i), which is not scalar.
Therefore no such auto can square to Ad(g), contradicting the extension
required by R24.

## Primary sources and independent checks

- Edie-Michell--Izumi--Penneys, *Classification of Z/2Z-quadratic unitary fusion categories*, Quantum Topology16(2025),493--568, [published PDF](https://ems.press/content/serial-article-files/51094). The local generators and bends are onpp506--507, the general spherical tube construction and corner action onpp512--515, the tetrahedral slots onpp528--530, and the three selected resolutions onp539. Their unitary classification theorem is not invoked.
- Fuchs--Groesfjeld, *Tetrahedral symmetry of6j-symbols in fusion categories*, [arXiv2106.16186](https://arxiv.org/abs/2106.16186), Lemma3.13(ii), Proposition3.22 and Corollary4.9. These supply the linear tetrahedral action with the explicit incoming/outgoing frame above.
- A. Schopieray, *Categorification of integral group rings extended by one dimension*, J. London Math. Soc. 108 (2023), 1617–1641, published Lemma 3.1, [DOI 10.1112/jlms.12789](https://doi.org/10.1112/jlms.12789). The published Galois-conjugacy formulation is used.
- The local [conductor-equality lemma](../compression/CONDUCTOR_EQUALITY_LEMMA.md), with its [independent audit](../compression/CONDUCTOR_EQUALITY_INDEPENDENT_AUDIT.md), and [character-weighted saturated indicator lemma](SATURATED_CHARACTER_INDICATORS.md), with its [independent audit](SATURATED_CHARACTER_INDICATORS_INDEPENDENT_AUDIT.md), supply the generally forced signs; no known-2D2 center is assumed.

Independent audits cover incoming-loop orientation, a second independent
paired-loop check, restricted tetrahedral coefficients and corner arithmetic,
source/annular-corner binding, and the projective normalizer argument. The
portable verifier checks the source hash, neutral fusion rules and inner-square
labels, complete neutral characters, saturation arithmetic, both nonzero scalar
branches, and the exact finite coefficient-slot substitutions.


## Packet and replay

Run from the repository root:

```sh
python evidence/unified_20261016/rank8/verify_r24_projective_inner_square.py --repo .
python -O evidence/unified_20261016/rank8/verify_r24_projective_inner_square.py --repo .
```

The normal and optimized receipts are `r24_projective_inner_square_normal.json` and `r24_projective_inner_square_optimized.json`. The proof components have distinct independent audits:

- `R24_INCOMING_LOOP_INDEPENDENT_AUDIT.md`: oriented incoming loop and functor action.
- `R24_PAIRED_LOOP_INDEPENDENT_AUDIT.md`: canonical pivotal form defects and three selected diagonal contractions.
- `R24_RESTRICTED_COEFFICIENT_INDEPENDENT_AUDIT.md`: coefficient slots, restricted phase cancellation, corner and nonzero entries.
- `R24_SOURCE_CORNER_INDEPENDENT_AUDIT.md`: immutable source and independent annular-corner argument.
- `R24_SOURCE_SCALAR_INDEPENDENT_AUDIT.md`: independently replayed full finite index and scalar checks, with receipt `r24_source_scalar_independent_optimized.json`.
- `R24_PROJECTIVE_NORMALIZER_INDEPENDENT_AUDIT.md`: projective functor action and no-inner-square argument.

The independently written source checker is `verify_r24_inner_square.py`; its optimized receipt is `r24_inner_square_independent_optimized.json`. The separate scalar expansion is retained in `r24_minimal_scalar_independent.json`. These finite checkers do not replace the categorical diagram arguments recorded above.
