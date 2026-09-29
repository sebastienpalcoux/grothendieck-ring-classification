# Independent audit: the split quadratic different-ideal obstruction

Audited sources: `research/round3/arithmetic/split_different_proof.md` and
`software/round3_split_arithmetic.py`. This is an audit of the tensor-only
profile used for `R6_8_6526`, not an assumption that a catalog identifier
determines a category. The underlying signed sphericalization and induction
lemmas are audited in `arithmetic_audit.md`.

## Different-ideal lemma

The lemma is valid for the commutative self-dual signed algebra. Distinct
embeddings of its dimension field give distinct real characters. Orthogonality
therefore identifies `sum d_i tensor d_i` with `Delta e_K`, where the first
factor acts on the separability idempotent. For each element `a` of the
codifferent, contraction by `Tr(a -)` gives `Delta a` in the ring of integers.
This is exactly `Delta` in the different. No positive pivotal structure on the
original category is assumed: the real positive squared norms arise in its
sphericalization.

The local trace-ideal formula can also be obtained directly from the
codifferent: `Tr(P^k)` is contained in `p^j` precisely when
`P^(k-ej)` is contained in `P^(-d)`. Thus its valuation is
`floor((k+d)/e)`. Setting `k=d` gives one at every tamely ramified prime and
two for a cyclic cubic conductor-nine extension (`e=3,d=4`). The global
trace ideal is obtained by summing the local component ideals, not multiplying
by the number of components. Consequently these divisibilities remain valid
when a prime is not totally ramified.

For the conductor-discriminant theorem the primary reference checked was
J. S. Milne, *Class Field Theory*, version 4.03, 2020,
<https://www.jmilne.org/math/CourseNotes/CFT.pdf>. The use here is the product
of the conductors of the nontrivial characters of an abelian extension.

## Exhaustive field list

The categorical dimension field contains `E=Q(sqrt(41))`; cyclotomicity of
signed characters makes it an abelian Galois field, of degree two, four, or
six. The mod-two algebra has four etale rank-one blocks and one rank-two
block. Its lifted rank-one blocks are `Q_2`. A degree-four or degree-six
Galois field with local degree two would need respectively two or three
rank-two local components, whereas only one is available. A larger local
degree cannot fit. Thus these fields split completely at two, including
absence of ramification there. This does not assert etaleness of the
rank-two order.

The original FP codegree is `18 sqrt(41)` times the norm-minus-one unit
`32+5 sqrt(41)`. Induction therefore gives
`theta=Delta/(18 sqrt(41))` integral. The relative trace to `E` shows
`738 | Tr_K Delta`. Positivity bounds this trace by 7416. The different
lemma restricts other ramified primes to three, five, and seven, and the
simultaneous occurrence of five and seven exceeds the trace bound.

Every positive odd fundamental discriminant supported on these primes and
within the trace budget is 1, 5, or 21. A biquadratic extension requires a
nontrivial such discriminant congruent to one modulo eight; none remains.
A cyclic quartic character squares to the conductor-41 quadratic character.
Its conductor-41 factor is even and takes value minus one at two; multiplying
by a real quadratic character therefore leaves exactly twists 5 and 21.
These give conductors 205 and 861. There is no omitted negative twist:
the conductor-41 quartic character is even, so a negative quadratic
discriminant would make the quartic field nonreal.

For degree six the cubic character can ramify only at seven or three, with
conductors seven and nine respectively. All cubic characters of conductor
seven or nine are nontrivial at two. For conductor 63 the two characters
trivial at two are conjugate and define one cubic field. The proof need not
use this uniqueness: its norm contradiction excludes either character.
Higher prime-power conductors do not occur, since the relevant character
orders divide four or six and the odd wild possibilities reduce to the
order-three character of conductor nine.

`split_different_audit.py` independently enumerates this finite character
list, verifies the value at two of a primitive quartic character modulo 41,
and constructs the order-four automorphism of both radical quartic fields.
It passes with Python optimization enabled.

## Sextic contradiction

The fields `E` and the cubic field have coprime discriminants. Their integer
rings tensor to the compositum's integer ring. Write
`theta=(a+b sqrt(41))/2`, with `a,b` integral in the cubic field and congruent
modulo two. Positivity of both extensions of each embedding gives `b>0`.
The only allowed trace is 5166, hence `Tr(b)=7`. At seven the cubic
different is `P_7^2`; multiplication by `18 sqrt(41)` is a unit locally.
Since `1,sqrt(41)` is an integral local basis at seven, different divisibility
forces both coefficients, and in particular `b`, into `P_7^2`. Its positive
norm is consequently at least 49. AM--GM gives at most `343/27`, a strict
contradiction. This argument does not require seven to split in `E`.

## Quartic identification and complete bounds

The displayed polynomials are irreducible and totally real. The map
`alpha -> beta` has square `alpha -> -alpha`, so each field is cyclic
quartic with quadratic subfield `E`. The module checks integral ring
multiplication and discriminant `41^3 M^2`. An added explicit mod-two check
finds four rank-one field factors in this order; its odd discriminant
therefore proves that the field splits at two. The audited field list and
the prime support of the order discriminant now identify the conductor
as `41M`. The conductor-discriminant theorem proves that the displayed
order has the full field discriminant and hence is maximal. This avoids
assuming that a polynomial with similar dimensions represents the desired
number field.

For fixed positive trace `T`, the coordinate `z_j` of `theta` equals
`sum_sigma sigma(Delta) sigma(b_j^*/(18 sqrt(41)))`. Its weights are strictly
positive and sum to `T`; the coordinate consequently lies between the
extreme displayed conjugate bounds. The software checks those bounds with
exact algebraic sign comparisons, then enumerates every integer point of
the trace hyperplane. There is no numerical-root cutoff. The totals are
28 and 216 positive candidates for twist five, and 16 for twist 21.
All fail a recorded d-number coefficient test. Applying this necessary
test to the full degree-four characteristic polynomial remains valid if
`Delta` happens to generate a proper subfield: each conjugate ratio is
still an algebraic unit, so every coefficient has the stated divisibility.

## Quadratic complements and final scope

When `K=E`, induction puts every signed codegree in `E`. The four other
codegrees form a Galois-stable multiset, hence are four rational integers,
two rational integers and one quadratic pair, or two quadratic pairs.
The enumeration covers all three options. In a quadratic pair the trace
is at most `7416-Tr(Delta)-3`: another pair has integer trace greater than
two, while two remaining rational codegrees have sum at least four. Thus
the code's bound on the radical coordinate is conservative and complete.
Both conjugate codegrees are required to divide `Delta` integrally.
The exact reciprocal identity leaves only the two saturated original
quadratic spectra, with four rational codegrees nine.

Signed Casimir saturation then forces all signed coefficient magnitudes to
equal the original magnitudes. The complete sign-table and original
character checks reduce to a pseudo-unitary Galois conjugate, and the
separate exact central-induction certificate excludes that possibility.
Subject to its recorded exact replay, this proves nonexistence of a complex
fusion categorification, rather than merely a spherical or pseudo-unitary
obstruction. The argument does not classify any case whose tensor fails
the explicit arithmetic profile.
