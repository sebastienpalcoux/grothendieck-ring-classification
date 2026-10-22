# Independent review of the construction restrictions

Reviewed on 22 October 2026 by a separate audit agent. This review covers
`../constructions/CONSTRUCTIONS.md`, `../constructions/constructions.tex`,
the exact verifier, and the two saved rank-14 tensors. The TeX fragment
retains the same hypotheses, conclusions, and scope as the reviewed note.
This review does not independently establish the Morita-dimension
theorem or the common-center properties used as inputs to Section 1.

**Verdict: accepted with the scope stated in the construction note.** No
substantive mathematical gap was found. The result is a necessary-condition
classification and an obstruction to one construction route; it is not a
categorification, a Morita identification, or a general nonexistence theorem
for R8_3_3472.

## 1. The two seven-invertible tensors

The classification is exhaustive for hypothetical Morita partners satisfying
all of the following inputs: dimensions `1^7,(7+5sqrt(2))^7`, a
pseudo-unitary realization after Galois transport, common-center simple FP
dimensions in `Q(sqrt(2))`, and no nontrivial common-center invertibles.
It is not an unconditional classification of based rings with that dimension
list.

Write `delta=7+5sqrt(2)`, so `delta^2=1+14delta`. Comparing rational and
irrational coefficients in `X X*` makes both invertible stabilizers trivial.
The left and right actions on the seven noninvertibles are therefore regular.
With `Xg=g^a X` and the unique invertible summand of `X^2` equal to `g^b`,
associativity gives `a^2=1`. The formula `X*=g^(-b)X` is valid: reciprocity
from `g^b` in `XX` gives both `X*=g^(-b)X` and `X*=Xg^(-b)`. Applying
duality twice, or comparing these two expressions, yields `b=ab`. Thus the
normalization to a self-dual `X` is legitimate in both action cases.

For the inversion action, associating `X^2g` gives `X^2g=gX^2`.
The resulting shift-by-two invariance of the seven coefficients makes them
all equal to 2. For the identity action, duality gives a symmetric coefficient
polynomial `m(g)`, whose coefficients sum to 14.

The formal-codegree restriction is valid under the stated categorical inputs.
The induction formula is `FPdim(A_E)=D/f_E`, while `dim(E)` is the
multiplicity of `A_E` in `I(1)`; there is no additional `dim(E)` factor in
the dimension formula. For the commutative ring, a nontrivial seventh-root
character extends by `x^2-tx-1=0`, and its formal codegree is
`7(1+x^2)`. Therefore `t^2` lies in both the real cubic cyclotomic field and
`Q(sqrt(2))`, hence in `Q`. A real cubic field has no quadratic subfield,
so `t` itself is rational. Divisibility by `Phi_7` then leaves exactly
`(m_0,m_1,...,m_6)=(A,B,...,B)`, with `(A,B)=(14,0),(8,1),(2,2)`.

The middle case has codegree polynomial `f^2-371f+2597`, discriminant
`49^2*53`, and violates the field restriction. The first case can be excluded
using the common-center hypothesis alone: for a nontrivial character of
`C7`, the extension `x=delta` has codegree `D`, giving a central simple of
FP dimension 1 distinct from the tensor unit. Thus the alternative appeal
to the rank-two categorification theorem is not needed for this exclusion.

Both displayed uniform-coefficient rings are associative based fusion rings.
They are distinct because exactly one is commutative. Their existence at
the based-ring level supplies neither associators nor a Morita equivalence.

## 2. The half-braiding constraint is nonunitary-safe

I checked the input identities directly against the local text extraction of
Radchenko--Wheeler, *Real quadratic fields and finite quantum dilogarithms I*,
arXiv:2609.21892v2, Section 5.4, equations (46)--(47), the paragraph
"Compositions with alpha_g", and the simple-intertwiner calculation preceding
Theorem 12. The paper realizes the category in endomorphisms of a Leavitt
algebra; no C*-structure is needed for these identities.

For the convention `c_(g,Y):alpha_g Y -> Y alpha_g`, the identities
`alpha_h rho=rho` and `rho alpha_g=Ad(U_g)rho` make
`c_(g,rho)=lambda U_g` for a nonzero scalar `lambda`. Write
`c_(g,alpha_h)=beta(g,h)`. The strict half-braiding hexagon then says
`lambda U_g=alpha_h(lambda U_g) beta(g,h)`, so
`beta(g,h)=chi(h,g)^(-1)`. This gives precisely the claimed self-braiding
`q(g)=chi(g,g)^(-1)` and uses only one-dimensional intertwiner spaces and
the algebraic identities in the source.

The kernel of the forgetful homomorphism on central invertibles consists of
tensor automorphisms of the identity. It vanishes because the universal
grading is trivial: the occurrence of `rho` in `rho^2` forces the degree of
`rho` to be the identity, and the occurrence of every `alpha_g` in that
square forces all remaining degrees to be the identity. Consequently the
central-invertible group embeds in `(G,q)`; surjectivity is neither proved nor
used. In particular the proof never assumes that every parent invertible
has a central lift.

## 3. The two-primary argument covers every input matrix

For `N=4s^2` with `s` odd, nondegeneracy of `chi` makes the radical of
`chi^(-2)` exactly `G[2]`. Since the RW group has at most two generators and
2-primary order 4, the only cases are cyclic order 4 and the Klein four
group. In the latter case the integral presentation matrix is `2A`.
The formulas `tr(A)=2s^2` and `det(A)=-s^2` follow from
`gamma=I+2A`, `det(gamma)=1`, and the required trace.

The rows of `A` give a basis of the order-two subgroup: the map from row
vectors `w mod 2` to `wA mod Z^2(2A)` is injective and has four elements.
Using the paper's bicharacter formula and `det(A)=-s^2` gives

`chi(wA,vA)=exp(-pi*i*omega(wA,v))`.

Thus the two diagonal values are `(-1)^b` and `(-1)^c` for
`A=[[a,b],[c,d]]`. If both were 1, then `b,c` would be even; odd
determinant would force `a,d` odd; trace 2 modulo 4 would force `ad=1`
modulo 4. This contradicts determinant 3 modulo 4. The radical quadratic
form is therefore a nontrivial sign character, with kernel of size 2.
The cyclic case already has radical of size 2. This is an argument for
all admissible integral matrices, not an extrapolation from sampled inputs.

## 4. Arbitrary pointed stabilization and the dimension factor

The proof correctly uses `P` of FP dimension `m` for the proposed parent,
and `Z(P)` of FP dimension `m^2` only for central-invertible control.
There is no double counting of these factors.

For an ordinary central de-equivariantization with fully faithful
forgetful image of `Rep(K)`, each irreducible representation has a simple
image. Tensor functors preserve FP dimensions, so its integer dimension
forces that image to be invertible: all other parent simple dimensions
are the irrational near-group dimension. Thus `K` is abelian and the
central lifts form an isotropic subgroup `H` of order `h=|K|`.

Let `L=Inv Z(P)` have order `k`, with polarization radical of order `t`.
The pointed subcategory of `Z(P)` has dimension `k`. Its centralizer has
dimension `m^2/k` and contains its pointed radical, proving `kt<=m^2`.
This uses nondegeneracy of the Drinfeld center, not nondegeneracy of its
pointed subcategory. It remains valid when the underlying pointed category
has nonabelian grading group.

The subgroup `H` embeds into `G x L`. In the Klein four case the radical
quadratic form on `G[2] x rad(L)` is nontrivial because it is already
nontrivial on `G[2] x {1}`. A quadratic form restricted to its polarization
radical is a homomorphism with values in `{+1,-1}`. Its kernel therefore
has order `2t`; in the cyclic case the whole radical has order `2t`.
Hence `|H intersect rad|<=2t` in either case.

For completeness, the finite premetric-group identity used here is
`|H^perp|=|A||H intersect rad(A)|/|H|`. It follows by taking the
perfect pairing on `A/rad(A)` and restricting characters to the image of
`H`. Isotropy gives `H subset H^perp`, and therefore

`h^2 <= |G| k (2t) <= 8s^2 m^2`.

The dimension of the RW parent is `4s D_s`. Ordinary de-equivariantization
divides dimension by `h`, so a target of dimension `D_s` requires
`h=4sm`. Its square `16s^2m^2` contradicts the bound by a factor of 2.
For the target in question, `s=7`, the required coefficient is `28^2=784`
and the upper bound is `2*196=392`.

The added uniqueness argument for the parent order is also correct. For
an `NG(N,N)` parent, its global dimension `E_N=N(2+d_N)` has trace
`N(N+4)` and norm `N^2(N+4)`. The ratio of trace squared to norm is
therefore `N+4`, invariant under rational scaling. For `D=700+490sqrt(2)`
the ratio is 200, forcing `N=196` whenever `E_N` is a rational multiple
of `D`. The dimension is genuinely quadratic for every positive `N`;
the strict bounds on `N(N+4)` in the note prove this directly.

The accepted conclusion excludes every RW gamma-input parent of the
required dimension scale, including noncyclic parents, tensored with any
pointed fusion category, followed by a direct ordinary central
de-equivariantization to the required global dimension. A subsequent
Morita change cannot change global dimension. The proof does not cover a
prior Morita change of the parent, arbitrary near-group associator data,
generalized Haagerup parents, or arbitrary sequences of constructions.

## 5. Reproduction and verification boundary

I independently ran both commands successfully:

```
python evidence/r3472_focus_20261022/constructions/verify_constructions.py
python -O evidence/r3472_focus_20261022/constructions/verify_constructions.py
```

The verifier checks the saved receipts and raw tensors against its exact
calculations. Each tensor has 38,416 associativity equations checked,
together with nonnegative integrality, the unit, duality, Frobenius
reciprocity, and the exact `Q(sqrt(2))` dimension character. It also checks
all 256 residue matrices modulo 4 (12 satisfy the trace and determinant
conditions; none has both off-diagonal entries even), the codegree
discriminant, and the numerical quotient-bound contradiction. Its checks
use explicit exceptions and survive Python optimization.

Canonical compact-tensor SHA-256 digests agree with the saved receipt:

- Identity action:
  `93f18db4efecd452ae52fefd638b6f770a68643698d496ce2adc9864b2ec27f1`.
- Inversion action:
  `dedba160c6a2cb2b4a3bfa24bf6f6228db3aa2f0453b09d84ae7a21f01edc2af`.

These finite calculations certify the based-ring and arithmetic components.
The categorical steps were reviewed mathematically above and should not be
described as proved solely by the verifier. General categorification of
R8_3_3472 remains unresolved.
