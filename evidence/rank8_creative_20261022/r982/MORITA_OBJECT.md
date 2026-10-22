# Regular module representations force the canonical center object

Every complex categorification of R8_3_982 has the following additional
necessary property: **every fusion category in its categorical Morita class
has a commutative Grothendieck ring of rank eight and the same formal
codegrees**. Under the center equivalence induced by any indecomposable
module category, the two canonical Lagrangian algebras have isomorphic
underlying objects. Their algebra structures need not agree.

This excludes constructions of R8_3_982 by categorical Morita equivalence
from a noncommutative fusion ring, including R8_3_928 and R8_3_941 despite
their shared quartic dimension field. The argument here does not itself
construct a categorification. The separate `E21_MODEL.md` now identifies
an actual unitary model, including an algebra structure on `1+X5` and
both nonregular based module types.

## General theorem

Let C be a pseudo-unitary complex fusion category and M an indecomposable
semisimple left C-module category. Put R=K0(C) tensor C, and suppose that
K0(M) tensor C is isomorphic to the left regular R-module. Let D=C*_M,
and transport I_D(1) to Z(C) using the center equivalence determined by M.
Call this transported object A_M, and put A_C=I_C(1).

Then A_M is isomorphic to A_C as an object of Z(C). In particular,
K0(D) tensor C and K0(C) tensor C are isomorphic complex algebras.

### Proof

The canonical spherical structure of C admits a compatible trace on M;
this also equips D with a pivotal structure. See Schaumann, *Traces on
Module Categories over Fusion Categories*, Proposition 5.8 and Theorem
4.5, [arXiv:1206.5716v3](https://arxiv.org/pdf/1206.5716).
The trace gives a pivotal structure on M: its nondegenerate pairing on
internal Hom objects identifies M with its relative Serre functor, and
trace compatibility gives the required pivotal module compatibility.

Write A_C as a direct sum of pairwise distinct center simples Z_j with
positive multiplicities e_j. Its endomorphism algebra is

    E = End_Z(C)(A_C) = direct_sum_j Mat_(e_j)(C).

Shimizu, *Further Results on the Structure of (Co)Ends in Finite Tensor
Categories*, Theorem 5.4, Lemma 5.9 and Theorem 5.11 with its following
semisimple-case observation identify R with E and K0(M) tensor C with
Hom_Z(C)(A_M,A_C) as left E-modules. Corollary 5.13 identifies
K0(D) tensor C with End_Z(C)(A_M). The transported-object identification
is in Theorems 3.13–3.14; see
[arXiv:1801.02493v2](https://arxiv.org/pdf/1801.02493).

Let m_j be the multiplicity of Z_j in A_M. The jth matrix block acts on
Hom(A_M,A_C) with multiplicity m_j of its standard e_j-dimensional
module. Its multiplicity in the regular E-module is e_j. The assumed
regular-module isomorphism therefore forces m_j=e_j for every j.
Thus A_M contains A_C as a direct summand. Both are canonical Lagrangian
objects, so both have Frobenius–Perron dimension FPdim(C). Every nonzero
object in a fusion category has strictly positive Frobenius–Perron
dimension. The complementary summand must vanish. This proves the
object isomorphism and then the endomorphism-algebra conclusion.

For commutative R of rank r, every e_j is one, so A_M is multiplicity-free
with r simple summands. The dual Grothendieck algebra is consequently
C^r. Its formal codegrees are the same: in a pseudo-unitary category with
commutative Grothendieck ring, the corresponding center-simple dimensions
are FPdim(C)/f_j. The center equivalence preserves FP dimensions, as does
Morita equivalence of C and D.

The theorem uses regularity as a complex representation. It does not
require an integral based-module isomorphism. This distinction makes it
applicable to the two nonregular based modules below.

## Application to R8_3_982

The frozen, complete calculation in
`../../rank8_research_20261022/r982/MODULE_TYPES.md` proves that every
indecomposable semisimple module category has one of exactly three
necessary based-module types. Each has rank eight, and its source action
is simultaneously conjugate over Q to the regular action by an invertible
induction matrix. Thus every actual module category satisfies the theorem.

The source ring is commutative. Its formal-codegree multiset is the root
multiset of

    (t^2-32t+128)^2 (t^4-576t^3+11520t^2-73728t+147456).

Every categorification has a pseudo-unitary Galois conjugate by the
independent general sphericalization gate in the preceding stage.
Conjugating C, M, and its module associators together preserves all
Grothendieck and based-module data. The conclusions established in the
pseudo-unitary conjugate therefore apply to every complex categorification.

## Exact receipt and limitations

`morita_object.py` binds the canonical tensor and complete module receipt
by SHA256. For each of the three classes it constructs an invertible
integral matrix W and checks all eight identities N_i W = W M_i over Q.
It also checks the regular characters independently, source commutativity,
the exact formal-codegree polynomial, and explicit noncommuting products
for the other named cases. Default replay only reads files:

```sh
python3 evidence/rank8_creative_20261022/r982/morita_object.py
python3 -O evidence/rank8_creative_20261022/r982/morita_object.py
```

The finite certificate checks the inputs of the categorical proof. It
does not substitute for that proof. This argument alone does not imply
equivalence of C and D or uniqueness of their Lagrangian algebra
structures. The additional lattice argument in `MORITA_RING.md` proves
identity of their based fusion rings, including fusion multiplicities.
The separate construction in `E21_MODEL.md` realizes both nonregular
based module types and the algebra `1+X5`; uniqueness of their algebra
or module associators is not asserted.
