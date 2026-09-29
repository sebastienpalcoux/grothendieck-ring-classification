# Ramification and rational formal codegrees: three general exclusions

**The tensors `R6_7_3812`, `R6_8_6234`, and `R6_8_6509` do not admit complex
fusion categorifications. No pivotal, spherical, pseudo-unitary, or unitary
hypothesis is assumed.** The argument covers the dimension field of every
hypothetical sphericalization; it does not select one favorable character.

The canonical certificates are the three corresponding `*_general.json`
files. Their kind is `ramified_Casimir_trace_exclusion`, and the independent
tensor-based entry point is `software/new_ramified_signed.verify(R,c)`.
No census identifier is consulted by this verifier.

## 1. The signed order attached to an arbitrary categorification

All three rings are commutative and self-dual. Let C be a hypothetical
categorification and S its finite sphericalization. Choose one lift of each
simple, with the positive lift of the unit, and quotient the Grothendieck
ring by the relation epsilon = -1. This gives a rank-six signed order A with

\[
x_i x_j=\sum_k t_{ij}^k x_k,\qquad
t_{ij}^0=\delta_{ij},\quad
|t_{ij}^k|\le N_{ij}^k,\quad t_{ij}^k\equiv N_{ij}^k\pmod2.
\]

Both lifts of a self-dual object remain self-dual: duality preserves the
nonzero spherical dimension and therefore cannot interchange opposite
dimensions. Thus all the multiplication matrices M_i of A are real
symmetric and commute. A over Q is a commutative semisimple algebra, with
six real characters. In particular this covers all signed tables, without
enumerating or normalizing their indicator signs.

Let d_i be the dimensions of the chosen lifts, K their generated field,
and Delta = sum d_i² the global dimension of C. The dimension character
makes K a field factor of A over Q.

Every character of the original ring, with formal codegree f, pulls back to
a character of the sphericalization with formal codegree 2f. Central
induction associates a central simple of dimension

\[
\frac{\dim(S)}{2f}=\frac{\Delta}{f}.
\]

Forgetting it to S expresses this dimension as an integer combination of
the d_i and their negatives. Consequently **Delta/f belongs to K and is an
algebraic integer for every original formal codegree f**. This is the
central-induction theorem of Ostrik, *Pivotal fusion categories of rank 3*,
Theorem 2.13, applied to the spherical category S. The finite
sphericalization is supplied by Etingof–Nikshych–Ostrik, *An analogue of
Radford's S^4 formula*, Corollary 7.6; see also Ostrik, Section 5.1.

## 2. The dimension field is forced

For all three rings the FP global dimension is

\[
D=2260+150\sqrt{226},\qquad
D^2-4520D+22600=0.
\]

Taking f=D above shows D belongs to K, so Q(sqrt(226)) is contained in K.
Since A/2A equals R/2R, direct finite multiplication gives:

| Tensor | Modulo-two product decomposition |
|---|---|
| R6_7_3812 | F2[z]/(z²) × F4 × F2 × F2 |
| R6_8_6234 | F2[z]/(z²) × F4 × F2 × F2 |
| R6_8_6509 | F2[z]/(z²) × F2 × F2 × F2 × F2 |

The verifier checks this by exhausting all 64 elements, identifying every
primitive idempotent, checking orthogonality and their sum, and verifying
the multiplication in each factor. Every nonzero element in a claimed
field factor is checked to have an inverse; the remaining rank-two factor
has exactly one nonzero square-zero element. Exact idempotents and factor
elements are retained in the certificates.

Idempotents lift to A tensor Z2. A finite free factor with finite-field
reduction is finite etale over Z2, hence its generic fiber is unramified.
The only remaining factor has rank two. But Q2(sqrt(226)) is ramified
quadratic, by the Eisenstein polynomial X²-226. Every local component of K
tensor Q2 must contain this ramified field, so none can be supported on
an unramified factor. All of K tensor Q2 is therefore supported on the
single rank-two factor. Hence [K:Q] is at most two, and

\[
K=\mathbb Q(\sqrt{226}).
\]

This argument does not identify the signed order with a maximal order.
Only finite freeness, idempotent lifting, and unramified local factors are
used. In particular it applies to every possible signed order A.

## 3. The rational codegree 15 contradicts the Casimir trace

The ring of integers of K is Z[sqrt(226)]. Write

\[
d_i=\alpha_i+\beta_i\sqrt{226}\quad(1\le i\le5),\qquad
S=\sum_i\beta_i^2>0,\quad b=\sum_i\alpha_i\beta_i.
\]

The two conjugate dimension characters have orthogonal vectors, since
the M_i are commuting real symmetric matrices. Therefore

\[
1+\sum_i\alpha_i^2=226S,\qquad
\Delta=452S+2b\sqrt{226},\qquad
\Delta+\Delta'=904S.
\]

The complete original formal-codegree lists are:

| Tensor | Formal codegrees |
|---|---|
| R6_7_3812 | D, D', 3, 15, 5, 5 |
| R6_8_6234 | D, D', 3, 15, 5, 5 |
| R6_8_6509 | D, D', 3, 3, 15, 15 |

In every case Delta/15 is an algebraic integer. Its rational coefficient
452S/15 must be integral, and gcd(452,15)=1. Thus 15 divides S, so S≥15.

The Casimir matrix C_A=sum M_i² has the six signed formal codegrees as its
eigenvalues. The two dimension characters contribute 904S. Each of the
other four codegrees is strictly greater than one: a codegree of one
would force all five nonunit character values to vanish, contradicting
the unit coefficient in x_i². Since the trace is integral,

\[
\operatorname{Tr}(C_A)\ge904S+5\ge13565.
\]

On the other hand the coefficient bounds give

\[
\operatorname{Tr}(C_A)=\sum_{i,j,k}(t_{ij}^k)^2
\le\sum_{i,j,k}(N_{ij}^k)^2.
\]

The right sides are 4548, 4548, and 4556, respectively. Each is below
13565. This contradiction proves the three general exclusions.

No signed-table enumeration, selected dimension character, pentagon
search, floating-point feasibility result, or pseudo-unitary assumption
is needed for these canonical proofs.

## 4. Portable criterion and verification

`new_ramified_signed.py` implements the same argument for self-dual
rank-six tensors with a quadratic FP global-dimension field ramified at
two and exactly one non-etale modulo-two factor, of rank two. It computes
the exact lattice constraints on S and b from Delta/D and **all rational
original formal codegrees**. The positive projection step for S is
exhausted using divisors of the common denominator. A trace contradiction
then produces `ramified_Casimir_trace_exclusion` directly.

If the trace bound leaves room, the implementation can also exhaust the
bounded coefficient-magnitude patterns and their complete sign domains.
That branch provides a second proof of the general-to-pseudo-unitary
reduction for R6_7_3582. A separate field-containment branch supplies an
independent exclusion of R6_8_6940, where Q(sqrt(5)) cannot embed in the
forced field Q(sqrt(170)). These two rings are also handled by the
independently imported/extended criteria in this revision.

The canonical three certificates were checked in ordinary and optimized
Python. All 54 existing positive models fail the ramification hypotheses
and are preserved. The test suite regenerates and verifies each proof
after a nontrivial basis permutation; it also rejects six distinct
certificate corruptions and a corrupted tensor in both Python modes.

```sh
python research/round2_higher/verify_ramified.py --audit
python -O research/round2_higher/verify_ramified.py --audit
```

The development initially found the three exclusions through a longer
signed-magnitude reduction and pseudo-unitary induction. Those are
superseded by the direct rational-codegree trace contradiction above.
The experimental unrestricted CSP implementation is not a dependency of
any canonical certificate; its bounded timeout never supplies an
exclusion.

## References

- P. Etingof, D. Nikshych, V. Ostrik, *An analogue of Radford's S^4 formula
  for finite tensor categories*, https://arxiv.org/abs/math/0404504.
- V. Ostrik, *Pivotal fusion categories of rank 3*,
  https://arxiv.org/abs/1309.4822, Theorem 2.13 and Section 5.1.
- The preceding ramified-factor strategy for R6_7_3582 is preserved and
  independently checked in `research/round2_external/sources/`.
