# Independent audit: three positive rank-six models

Date: 2026-09-30.

**Accepted conclusion:** R6_4_22, R6_4_91 and R6_4_629 each admit a unitary
categorification. These are identifications of complete fusion tensors with
actual conformal-extension module categories. They do not depend on an inference
from a matching dimension list or hypothetical modular data.

The audit checks the categorical constructions and the exact finite calculations
used to identify their Grothendieck rings. It does not reprove the cited
conformal-embedding, center, or Frobenius--Schur indicator theorems.

## Shared existence and grading argument

A finite unitary conformal embedding supplies a connected commutative separable
algebra A in its unitary WZW category B. Thus B_A is an actual unitary fusion
category, and the local modules are the representation category of the larger
affine algebra at level one. This is stronger than merely displaying a modular
invariant. The conformal embeddings used here are published, with the branching
rules identified below.

In all three cases A is in the neutral part of the source parity grading.
For an A-module, its two homogeneous parts are A-submodules, so every simple
module has a definite parity. Relative tensor product preserves that parity;
free modules from odd source objects make the grading faithful. The neutral
component is consequently an actual unitary fusion subcategory.

The free-module tensor functor B -> B_A is central. We use centrality only for
its image in the Grothendieck ring. We do not assume B_A itself is braided.

## R6_4_22

Take B=C(B2,7) and the conformal embedding into (D7)_1. The vacuum algebra is

    A=(0,0)+(1,6)+(2,2)+(5,0).

The neutral component has source vertices {1,2,5,6,9,10}. Its local invertibles
include g at vertex2 and the two odd spinors z,z* at vertices11,12. The level-one
D7 fusion group is C4, so z^2=g and z*=gz. The free odd fundamental spinor s at
vertex3 is self-dual and central. Its product with z is one of the two even
simples x,y of the same dimension. Therefore duality on {x,y} is the action of
g, since (zs)*=s z*=gzs.

The published vector-action graph is the multiplication matrix of the simple
free object e. In order [1,9,10,2,5,6], its square gives e^2=1+g+2f. Testing the
two possible g-actions on x,y forces the interchange: the other action makes
N_f=(N_e^2-I-N_g)/2 nonintegral. Thus x*=y.

The source induction table also shows g=F(7,0), so both e and g are central.
It follows from 2f=e^2-1-g that f is central in the complexified fusion ring.
The exact reconstruction using these facts, the unit, and rigidity has rank36
in36 unknown matrix entries. Its unique solution recovers all216 tensor entries
of R6_4_22.

Independent replays passed: `extract_b2_7.py` (ordinary and optimized Python)
and `reconstruct_b2_7.py`. Source vertex order and exact tensor equality agree
with the certificate. No categorical assumption is inferred from the target
tensor in this argument.

Sources checked: Coquereaux--Rais--Tahri, arXiv:1001.5416, Section3.5,
Figure11(a), induction table and dimension list; the standard level-one D7
fusion group, with the supplied reference to Böckenhauer,
arXiv:hep-th/9507047, Theorem7.1.

## R6_4_629

Take B=C(B2,12) and the conformal embedding into (E8)_1. Its displayed vacuum
algebra A is Lagrangian, because the local category is Vec. Hence the full
module category E=B_A has Z(E) equivalent to B. The even vector-action component
has vertices {1,3,4,6,7,8} and rank6.

The central generator has characteristic polynomial

    t^2(t^4-5t^3+10t-5).

All eigenvalue multiplicities are at most2. In a semisimple complex algebra a
matrix summand of size n>=2 would contribute at least n^2>=4 to an eigenvalue
of multiplication by a central element. Therefore this fusion ring is
commutative. This justifies, rather than assumes, the commutativity constraints
in the tensor completion.

Only two basis permutations can be duality while fixing the unit and generator.
The nontrivial permutation forces coefficients 1/2 and3/2. For identity duality,
the exact linear completion has one parameter t, with nonnegative integrality
forcing t=1,2,3. All associativity identities are checked. The middle value
gives the entire target tensor. The outer values have formal codegrees3 and15.

The known center used to exclude those two values is obtained independently
from the constructed category. The faithful parity grading yields a canonical
Rep(C2) in Z(E)=B. B has a unique nontrivial invertible g=(12,0), which is a
boson, so this is the canonical grading subcategory. The center of the neutral
component is the de-equivariantization of its centralizer, namely

    Z(E_0) = (B_ad)_{<g>}.

The exact WZW dimensions of the49 even weights and the simple-current orbits
give35 simple dimensions:21 ordinary orbits and7 fixed points, each of the
latter splitting into two halves. Their squares sum to FPdim(E_0)^2. Neither
FPdim(E_0)/3 nor FPdim(E_0)/15 is present. The formal-codegree induction theorem
therefore excludes both outer tensor completions of this actual category.
The value t=2, and hence R6_4_629, is forced.

This reasoning is noncircular: the center comes from the conformal construction
and the grading theorem. The earlier rank35 center-data candidate is used only
as a redundant dimension-list cross-check.

Independent replays passed: `extract_graph.py` in ordinary and optimized Python,
`complete_from_generator.py` under optimized Python, and
`check_center_dimensions.py`. One harmless assertion implementation initially
retained symbolic0 in a set of associativity equations; the author corrected
this, and the frozen replay passed. There was no mathematical failure.

Sources checked: arXiv:1001.5416, Section3.6/Figure13; DMNO,
arXiv:1009.2117, Corollaries3.30 and4.1; the faithful-grading center theorem
(EGNO Proposition8.23.11); and the standard formal-codegree induction theorem.

## R6_4_91

Take B=C(C3,4), with the adjoint conformal embedding into (B10)_1=so(21)_1.
The vacuum algebra is

    A=(0,0,0)+(2,1,0)+(0,0,4)+(1,2,1).

The local category is the Ising category of so(21)_1. Its fermion branches as
(2,0,0)+(0,3,0)+(0,2,2)+(3,0,1), and its spinor as2(1,1,1).
The vacuum/vector branching is reconstructed from the8 abelian upper ideals
of the C3 positive roots. This is the published adjoint branching theorem,
not a modular-invariant guess. The spinor multiplicity follows from the
published spinor branching formula at rank3.

### Why the constructed neutral component really has six simples

The exact free-induction Gram matrix is computed from the source fusion rules
and A. Three columns are the known local simples1,psi,sigma. The free object
tau=F(0,1,0) has norm1 and is orthogonal to those three, so it is a fourth simple.
After subtracting these four columns, the residual Gram matrix is2vv^T.
The row for F(0,0,2) has norm2 and v-entry1. Thus that free object has exactly
two new distinct simple constituents x,y, with multiplicity1 each. Rank1 of the
residual forces their full restriction columns to be equal to v, and rules out
any additional simple. Dominance of free induction gives all simples.

The resulting induction matrix has rank5. Its five independent row classes are
central because they come from the free functor. A semisimple complex algebra
of dimension6 with center dimension at least5 is commutative: any noncommutative
matrix block contributes at least3 to the difference between algebra and center
dimensions. This proves the commutativity needed in the completion.

The local Ising simples are self-dual, and tau is free on a self-dual source
object. Therefore the only duality choices are x*=y or both x,y self-dual.
An exact small completion gives one non-self-dual tensor, agreeing in all216
entries with R6_4_91, and three self-dual tensors. The finite enumeration bounds
follow from the nonnegative affine coefficients; each free variable is between
0 and4. The final script evaluates these coefficients as exact integers over
fixed denominators, avoiding floating-point decisions.

### The symmetric-square indicator lemma

If x is a self-dual simple in a pivotal fusion category, choose f:x->x* with
pivotal transpose f^t=epsilon f, epsilon=nu_2(x) in {+1,-1}. Under the standard
dual-tensor identification, f tensor f is a nondegenerate self-duality of x^2.
Its transpose is epsilon^2(f tensor f), so it is symmetric. If a self-dual
simple y occurs in x^2 with multiplicity1, the isotypic decomposition restricts
this symmetric self-duality to a nondegenerate symmetric self-duality of y.
Consequently nu_2(y)=+1. No braiding is required.

For the middle self-dual completion, x^2=1+x+y+2tau. The lemma forces both
nu_2(x)=nu_2(y)=+1. But the exact indicator of the actual free object
F(0,0,2)=x+y is0, computed from the known center

    Z(B_A) = B tensor Ising^rev.

The center forgetful multiplicities come from the conformal branching, and the
indicator calculation uses exact arithmetic in Q(zeta32). This is a contradiction.

### The other two self-dual completions

Their formal-codegree polynomials have factor t^2-16t+32, giving
8+4sqrt2 and8-4sqrt2. The same source construction identifies the center of the
neutral component independently. J=(0,0,4) is a boson and F(J)=1, since J is an
invertible constituent of A. The canonical grading Rep(C2) in
B tensor Ising^rev is generated by (J,1). Its centralizer and de-equivariantization
therefore give

    Z((B_A)_0) = (B_ad)_{<J>} tensor Ising^rev.

The simple-current action is the involution

    J(a,b,c)=(b,a,4-a-b-c).

I independently checked all35 rows of its multiplication matrix against that
formula. The19 even weights have3 fixed points; the modularization has rank14,
and the center has rank42. The exact dimension spectrum omits both
FPdim((B_A)_0)/(8+4sqrt2) and FPdim((B_A)_0)/(8-4sqrt2). Thus the two outer
completions also contradict the formal-codegree induction theorem. Only the
non-self-dual target tensor remains.

Independent optimized replays passed for `exact_certificate.py` and
`complete_tensor.py`. Independently checked the rank5 free image, the simple
tau norm, the residual norm2, the two outer codegree factors, all simple-current
rows, and the completeness bounds. The source fusion rules are certified by
42,875 exact Weyl-character equations, not by their numerical proposal.

Primary branching sources checked: Cellini--Kac--Moseneder Frajria--Papi,
arXiv:math-ph/0506043v2, introduction/adjoint example, Theorem3.9 and
Proposition4.1. The conformal-extension and center interpretation is supported
by DMNO, arXiv:1009.2117, Sections6.1--6.2 and Corollary3.30.

## Scope of the accepted conclusions

All three constructions give existence and full based-ring identifications.
They do not classify all associators on those rings. Categorical identifications
of the known centers above do not, without a separate labelling/fixed-point
comparison, certify that a particular archived S,T file is already written in
the same basis as the WZW construction. None of these limitations affects the
three positive categorification conclusions.
