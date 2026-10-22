# Galois Gram bounds and both rank-two Morita branches of R3472

These are **conditional restrictions on Morita constructions**, not a general
exclusion of `R8_3_3472`. Neither of its two recorded rank-two based modules is
known to lift to a module category. No new category is constructed here.

The first branch's ten previously retained dual dimension spectra reduce to
**seven**. The other branch, previously left without a complete finite
dimension domain, has **400,478 arithmetic spectra**, of which the
order-seven orbit obstruction removes one. The remaining 400,477 are only
arithmetic possibilities; no fusion multiplication or associator is supplied.

## A uniform Galois Gram bound

Let R be a fusion ring, let d_i be its Frobenius--Perron dimensions, let
K=Q(d_i : i), and let D=sum_i d_i^2. If h is the sum of d_i^2 over the
integer-dimensional basis elements, then

    h <= 1 / Tr_(K/Q)(1/D).

This assertion requires neither categorification nor pivotality. The
integer-dimensional objects need not be assumed to form a fusion subring.

Here is a direct proof. The field K is totally real: every conjugate of d_i^2
is an eigenvalue of the positive semidefinite integer matrix N_i N_(i*) and
is nonnegative, so every conjugate of d_i is real. For distinct embeddings
sigma,tau:K -> R, the dimension characters sigma(d_i) and tau(d_i) are
distinct. Applying tau to the canonical regular element
sum_i sigma(d_i) X_i shows

    sum_i sigma(d_i) tau(d_i) = 0.

Indeed this sum is annihilated by every scalar
sigma(d_j)-tau(d_j), one of which is nonzero. Thus the Gram matrix of all
conjugate dimension rows is diag(sigma(D)). Integer-dimensional basis
elements contribute h times the all-ones matrix. The residual Gram matrix
is positive semidefinite. Applying its quadratic form to the vector
(1/sigma(D)) gives S-h*S^2 >= 0, where S=Tr(1/D)>0, proving the bound.

There is also an equality criterion: if h=1/S, every nonintegral d_i obeys

    Tr_(K/Q)(d_i/D)=0.

This follows because a sum of nonnegative squares vanishes in that quadratic
form. These Gram and equality arguments supply a reusable arithmetic filter
for proposed Morita-dual dimension spectra.

## Common data of the two branches

Write r=sqrt(2) and D=700+490r, so Norm(D)=9800 and Tr(D)=1400.
Let C categorify R3472 and assume that one specified rank-two based module
lifts to an indecomposable C-module category M. Write B for its dual category.
Morita invariance gives FPdim(B)=D. Every B-action matrix commutes with the
specified C-action matrix. The regular FP-dimension element acts with rank
one on M: its second eigenvalue is zero.

The original source matrices, up to swapping the module simples, are

    first:  [[7,7],[7,5]],     second: [[11,5],[5,1]].

Their full integral commutants, not a smaller selected sublattice, are

    first:  [[s+t,7t],[7t,s-t]],   d_Y=s+5t*r;
    second: [[s+t,t],[t,s-t]],     d_Y=s+t*r.

In either case nonnegativity gives integers t>=0 and s>=t. Distinct simple
objects may have the same action matrix; their multiplicities are unrestricted.
The dual need not have a commutative fusion ring. These observations apply to
every simple Y of B, including non-self-dual simples.

The dimensions have field Q(r), so the uniform Gram bound gives h<=7.
Here the integral-dimensional objects do form a fusion subcategory: all
radical coefficients are nonnegative, so a product with radical coefficient
zero cannot contain a nonintegral summand. Categorical Lagrange integrality
of D/h requires 1400/h and 9800/h^2 to be integers. Therefore

    h in {1,2,5,7}.

This subcategory is pointed. For h=1,2 this is immediate. At h=5, the only
nonpointed integer dimension multiset is {1,2}; its dimension-2 square would
require 4=1+2n. At h=7 the only nonpointed multiset is {1,1,1,2}; the three
invertibles fix the unique dimension-2 simple, so its product with its dual
would require 4=3+2n. Both are impossible. Hence h=g is the number of
invertibles, and its group is cyclic because g is 1 or prime.

## Three further first-branch spectrum exclusions

The frozen previous receipt has eleven arithmetic spectra, one already
excluded by an order-seven orbit argument. We additionally exclude its
zero-based spectrum indices 0, 3 and 5:

| g | Nonintegral dimensions, with multiplicity |
|---|---|
| 1 | (6+5r)^2, (9+5r)^1, (14+10r)^1 |
| 1 | (5+5r)^1, (8+5r)^2, (14+10r)^1 |
| 2 | (7+5r)^2, (9+5r)^1, (13+10r)^1 |

Each row has exactly two duality possibilities, up to permuting simples of
the same dimension: the repeated pair is either self-dual or exchanged.
For every possibility, there is no nonnegative integer multiplication even
satisfying the unit, Frobenius reciprocity, duality, and dimension equations.
Associativity is not needed for these exclusions.

To verify this claim define m_(i,j,k)=[1:X_i X_j X_k]. Frobenius reciprocity
and duality identify its cyclic rotations and the reverse dual triple
(k*,j*,i*). The unit fixes all triples containing zero. One variable per
remaining orbit gives a nonnegative integer linear system A x=b, with two
dimension equations for each ordered product. The cyclic subgroup products
are also fixed. `product_equations.py` builds these systems with integer
coefficients only; no commutativity of the prospective dual is assumed.

`exact_integer.py` exhausts the entire finite solution box. Every variable
has a finite upper bound from a positive-coefficient dimension equation.
It repeatedly tightens interval bounds, rejects impossible row intervals
and exact gcd congruences, and otherwise branches over every integer of one
remaining interval. There is no time, node, or coefficient cutoff. The six
empty searches take respectively 72,22,39,11,380,79 nodes. Numerical MILP
was used only in `product_probe.py` for discovery; its statuses are not
accepted as proof. The input R3472 tensor is an exact positive control for
the equation builder.

The retained first-branch spectrum indices are 1,2,4,6,7,8,10, so seven
necessary spectra remain. This does not assert that those seven have
fusion multiplications.

## The complete second-branch arithmetic domain

The regular-element identities for d_Y=s_Y+t_Y*r give

    sum s_Y^2=350,   sum t_Y^2=175,   sum s_Y t_Y=245.

Put u_Y=s_Y-t_Y>=0. After removing the g invertibles, the nonintegral
simples, including repeated dimensions, satisfy precisely

    sum u_Y^2=35-g,   sum u_Y t_Y=70,   sum t_Y^2=175,
    u_Y>=0, t_Y>=1 integral.

These equations give complete bounds u<=5 and t<=13. For fixed g, count
nonnegative multiplicities of all types (u,t) with u>0 and then complete
the u=0 types by integer square partitions of the unused t^2 sum.
The recursive state is (type index, remaining u^2, remaining ut,
remaining t^2). Every multiplicity from zero to the exact residual bound
is visited. Cauchy pruning V^2<=U*W is necessary for every remaining state.
This counts each dimension multiset once, rather than counting labelings.

| g | Complete number of arithmetic spectra |
|---|---:|
| 1 | 272,348 |
| 2 | 124,228 |
| 5 | 3,900 |
| 7 | 2 |
| Total | 400,478 |

When g=7 the uniform bound is an equality. It forces 5s=7t, hence every
noninvertible dimension is k*d, where d=7+5r and k>=1 is integral.
The two spectra are 1^7,d^7 and 1^7,d^3,(2d)^1. For a d-dimensional simple,
d^2=1+14d forces exactly one invertible in XX*, so its stabilizer among
the seven invertibles is trivial. Its orbit has size seven. The spectrum
with just three d-dimensional simples is impossible. This leaves 400,477
arithmetic possibilities; further product tests were not completed for
this entire domain.

## Construction interpretation and limitations

The g=7 profile has seven invertibles and seven noninvertibles of dimension
d=7+5r, with a free transitive action on the noninvertibles. This is a
generalized-near-group profile with trivial stabilizer and total
noninvertible coefficient 14 in XX*. It is **not** a near-group category
with a single noninvertible of dimension d. In particular d^2=1+14d,
not 7+14d. Uniform coefficient two on the orbit would give the familiar
higher-multiplicity generalized Haagerup shape, but neither that uniformity
nor an associator is supplied by this spectrum calculation.

An ordinary C2 de-equivariantization of a generalized Haagerup C14 parent
would have the right scalar global dimension. The construction discussion
in Grossman--Izumi, Section 6, does not provide such a model: its known
examples have the relevant sign epsilon_n(1)=-1, which makes the order-two
lift fermionic for n=7, whereas that de-equivariantization requires a boson.
The paper labels this sign property as holding in known examples, not as a
universal theorem. Thus this observation neither constructs the desired
parent nor excludes all possible C14 parents or all generalized-near-group
categorifications. No general existence conclusion is drawn from it.

## Replay and primary references

From the repository root:

```sh
python3 evidence/rank8_creative_20261022/r3472/verify.py
python3 -O evidence/rank8_creative_20261022/r3472/verify.py
```

The standard-library-only verifier replays all six finite integer exclusions,
recounts both-branch arithmetic restrictions, and checks the source tensor
control and SHA256 input identities. `verification.json` records the exact
scope. Discovery files are explicitly separate and are not verification
dependencies.

* Etingof--Gelaki--Nikshych--Ostrik, *Tensor Categories*, Corollary 7.16.7,
  Exercise 7.16.8 and Theorem 7.17.6:
  https://math.mit.edu/~etingof/egnobookfinal.pdf . The last is the categorical
  Lagrange theorem; this corrects the citation to Corollary 3.3.16 in the
  frozen predecessor note, without changing its mathematical argument.
* Grossman--Izumi, *Drinfeld centers of fusion categories arising from
  generalized Haagerup subfactors*, Quantum Topology 13 (2022), Section 6:
  https://ems.press/content/serial-article-files/36923 . Its additional
  Q-system hypothesis and the limitation to known signs are retained here.

R3472 remains unresolved. Necessary dual dimensions, integer product data,
and based modules are not categorical realizations.
