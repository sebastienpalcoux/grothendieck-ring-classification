# Nonintegral extensions of the rank-six dimension-60 ring

Date: 24 October 2026. General-complex scope, with no braiding or
unitarity assumptions on the hypothetical categorification.

## Theorem

Let D be a fusion category with simple FP dimensions 1,1,2,2,5,5.
Assume:

1. D equals its adjoint subcategory (its universal grading is trivial).
2. The nontrivial invertible g fixes the two dimension-two simples and
   exchanges the two dimension-five simples.

Then every faithful finite-group extension of D is group-theoretical,
and in particular is integral.

### Step 1: D cannot be solvable

Suppose D were solvable. By ENO Proposition 4.4 it admits a construction
from Vec by successive extensions and equivariantizations by cyclic
groups of prime order. The last step cannot be an extension, since D
has no nontrivial faithful grading. Thus D = E^{C_p} for a fusion
category E, and the canonical central Rep(C_p) embeds into D under
forgetting its central structure. D has exactly two invertibles, so
p=2, and the nontrivial character has underlying object g.

De-equivariantize by this central Rep(C2), or equivalently take modules
over its regular central algebra A=1+g. This is a fusion category of
dimension 30. Its simple dimensions can be determined without knowing
any associator of D. The free orbit {1,g} gives one invertible; the free
orbit consisting of the two dimension-five objects gives one simple
of dimension five. Each fixed dimension-two object gives two distinct
simple A-modules of dimension one. Indeed, the endomorphism algebra
of its free module has dimension two and is semisimple, hence is C+C;
the two simple summands each have underlying object equal to the
original dimension-two object. FP dimension after passage to A-modules
is the underlying FP dimension divided by FPdim(A)=2. These six objects
exhaust the simples since every simple A-module is a summand of a free
module. Therefore the de-equivariantization has dimensions 1^5,5.

Its invertibles form the cyclic group C5. Writing z for its unique
noninvertible simple, rigidity and dimensions force

    hz=z=zh,    z^2 = sum_{h in C5} h + 4z.

But Etingof–Gelaki–Ostrik, Corollary 7.4, applies to arbitrary complex
fusion categories with n cyclic invertibles and one noninvertible of
dimension n. It forces n+1 to be a prime power. Here n=5 and 6 is not
a prime power. This contradiction proves that D is not solvable.

### Step 2: D is Morita equivalent to Vec_{A5}^omega

ENO Theorem 9.16 says that every fusion category of dimension 60 is
weakly group-theoretical. Hence D is categorically Morita equivalent
to a nilpotent fusion category N of the same dimension. Choose a
tower of faithful group extensions constructing N from Vec. The
product of the orders of the grading groups is 60.

If all grading groups are solvable, their normal series refine this
tower into cyclic-prime extensions; N and hence D are solvable,
contrary to Step 1. Thus at least one grading group is nonsolvable.
Every proper divisor of 60 is the order of only solvable finite
groups; the unique nonsolvable group of order 60 is A5. These standard
finite-group facts can also be expressed using the smallest
nonabelian simple group A5, of order 60, and a composition series.
The nonsolvable grading group therefore has order 60, and every other
extension step is trivial. Consequently N is a pointed category
Vec_{A5}^omega for some 3-cocycle omega. No value or trivialization of
omega is assumed.

### Step 3: all extensions of Vec_{A5}^omega are pointed

Let P=Vec_{A5}^omega, and let B be an invertible P-bimodule category.
As a left P-module category it has pointed dual (indeed the right
action identifies its dual with P, up to the harmless opposite
convention). By the classification of pointed-dual module categories,
Naidu–Nikshych Example 2.2, such a module category is described by a
normal abelian subgroup H of A5 and compatible cochain data. Since A5
has no nontrivial normal abelian subgroup, H={1}. Therefore B is the
regular left P-module category and has 60 simple objects, transitively
permuted by the 60 invertibles of P.

Each homogeneous component of a faithful group extension of P is an
invertible P-bimodule category. Consequently each component has these
60 simple objects, all with the same FP dimension d, because the
invertibles of P permute them transitively. A faithful homogeneous
component has total FP dimension FPdim(P)=60. Hence 60*d^2=60 and d=1.
Every simple object of the extension is invertible: the extension is
pointed. This argument applies to every omega and every coherent
extension, not merely to untwisted or preselected models.

### Step 4: transport the extension through Morita equivalence

If C is any faithful finite-group extension of D, ENO Lemma 3.4
constructs an extension of P which is Morita equivalent to C. It does
this by replacing D with its category of bimodules over an
indecomposable algebra and applying the same construction to C;
the grading survives because the algebra lies in the neutral
component. Step 3 makes the resulting category pointed. Thus C is
group-theoretical. Group-theoretical fusion categories are integral:
the standard double-coset description of simples gives dimensions

    [H : H intersect tHt^{-1}] * dim(projective irreducible representation),

which are integers. This proves the theorem.

## Application to two remaining rank-nine rings

Both tensors have global FP dimension 120. Their integral objects
form a dimension-60 fusion subring D and the other three objects
each have dimension 2*sqrt(5). The tensor verifies a faithful C2
grading with D as neutral component. In the notation (1,g,a,b,u,v)
of dimensions (1,1,2,2,5,5), the neutral labels are:

| Ring | Neutral labels (1,g,a,b,u,v) | Odd labels |
| --- | --- | --- |
| R9_2_585 | (0,1,7,8,3,4) | 2,5,6 |
| R9_2_1303 | (0,4,5,6,7,8) | 1,2,3 |

The neutral rules satisfy the theorem's two conditions. In particular
the adjoint closure is all six labels, while g fixes a,b and exchanges
u,v. A hypothetical categorification would therefore be an integral
extension by the theorem. Its three dimensions 2*sqrt(5) contradict
integrality.

**Conclusion: R9_2_585 and R9_2_1303 have no complex categorification.**

This proof does not assume that a fusion-ring match to a known
dimension-60 model classifies its categorifications. Step 2 establishes
the necessary Morita form for every hypothetical categorification.

## Exact certificate

`d120_tensors.json` contains the two unchanged full source tensors.
`verify_dimension120_obstruction.py` checks all fusion-ring axioms,
all FP dimension equations exactly in Q(sqrt(5)), the neutral
subcategory, faithful grading, its adjoint closure, and the complete
permutation of simples by g. Its output is
`dimension120_obstruction_certificate.json`.

## Primary references and theorem scopes

* P. Etingof, D. Nikshych and V. Ostrik, *Weakly group-theoretical and
  solvable fusion categories*, Adv. Math. 226 (2011), 176–205,
  arXiv:0809.3031v2. Definition 1.1; Proposition 4.4; Proposition 4.5;
  Theorem 9.16 (dimension 60); Lemma 3.4 (Morita transport of extensions).
  https://arxiv.org/pdf/0809.3031
* P. Etingof, S. Gelaki and V. Ostrik, *Classification of fusion
  categories of dimension pq*, IMRN 2004, no. 57, 3041–3056,
  arXiv:math/0304194v2, Corollary 7.4. The statement concerns all complex
  fusion categories and is not a unitary-only classification.
  https://arxiv.org/pdf/math/0304194
* D. Naidu and D. Nikshych, *Lagrangian subcategories and braided tensor
  equivalences of twisted quantum doubles of finite groups*, Commun.
  Math. Phys. 279 (2008), 845–872, arXiv:0705.0665v2, Example 2.2
  and Section 4.2. The normal-abelian-subgroup condition covers
  arbitrary 3-cocycles omega.
  https://arxiv.org/pdf/0705.0665

The theorem is proved here by combining the stated results. No claim
of priority or exhaustive literature novelty is made.
