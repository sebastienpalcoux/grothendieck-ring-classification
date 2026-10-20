# Independent audit of the complete R3895 reduction

The mathematical coverage of `models/sqrt5/verify_r3895_cyclic_chain.py`
passes this independent review, subject to its final strict replay gate.
This note is not a whole-ring exclusion certificate: every one of the
fifteen final conditional certificates must be complete and independently
replayed, and the dependency inventory must be frozen. A development
receipt labelled `INCOMPLETE` cannot establish the exclusion.

The audited source is the original tensor `R7_5_3895`, SHA-256
`590b613093643a1c3047e866213050ba7fd87c211a42906de823d0c613d11ad0`.
The wrapper reviewed after the cache repair has SHA-256
`1582cb62c22ff994f00b26e43b32e1e8d4df99c8a443a1711cdbbad5c5b125a8`;
`R3895_CHAIN_OBLIGATIONS.md` has SHA-256
`5aea6500957e69e201cdadbe309926ed0a95f42d6160e81ca1ef84af8019ab15`.
Subsequent edits require comparison with this reviewed version.

## General categorifications are covered

The initial reduction does not assume that the proposed category is
pivotal, spherical, pseudo-unitary, or a unitary tensor category. It applies
the repository's oriented sphericalization construction. The signed
structure constants satisfy the finite coefficient bounds, parity,
oriented cyclic/dual symmetries, and associativity imposed by
`oriented_signed.problem`. The enumeration does not impose commutativity
on the sphericalization. The generated exhaustive recursion must finish:
compilation failure, integer-range failure, or timeout raises an exception
and cannot return a partial successful list.

For this tensor the complete list has two signed quotients, both gauge
equivalent to the unsigned tensor. After changing the chosen lifts by the
gauge, each coefficient difference equals its unsigned coefficient sum.
Every opposite-lift multiplicity is therefore zero. The seven selected
lifts, including the tensor unit and the selected duals, form a tensor
subcategory of the sphericalization equivalent to the original category.
Its spherical structure restricts to this subcategory. This is why the
subsequent center is the center of a rank-seven category; it is not the
center of the rank-fourteen sphericalization.

The exact character calculation checks all seven characters. Outside the
FP Galois pair, a character vanishes on a simple object or is inconsistent
with spherical dual dimensions. A spherical dimension character is
nonzero on every simple and is dual-invariant, so it belongs to the FP
Galois pair. Passing to an algebraic form of the fusion and spherical data
and extending the appropriate number-field embedding makes these dimensions
the positive FP dimensions. Thus a hypothetical original categorification
has a pseudo-unitary Galois conjugate with the same unsigned based ring.
Excluding that conjugate excludes the original category. No claim that a
pseudo-unitary tensor category is itself unitary is needed: the normalized
center modular representation is unitary, has anomaly one, and satisfies
the congruence/Galois identities used below.

These steps use the existing sphericalization framework and induced-unit
formal-codegree theorem, as documented in `sqrt5_reduction/PROOF.md` and
the manuscript `full_I1_compression.tex`. The additional field obstruction
for R5039 in the shared reduction is irrelevant to R3895's two gauge
branches.

## Low frames, high rows, labels, and second indicators

The source dimension vector is

\[
(1,5+2\sqrt5,5+2\sqrt5,10+4\sqrt5,
  8+4\sqrt5,8+4\sqrt5,9+4\sqrt5),
\qquad D=720+320\sqrt5.
\]

The source ring is commutative, so its seven characters give seven distinct
simple summands of the induced unit, each with multiplicity one and
dimension `D/f_E`. All have twist one. The low enumeration uses these
dimensions, the forced Galois image of the unit, nonnegative integral
restriction coefficients, and the exact induction Gram matrix. Its bounds
follow from individual Gram entries and dimensions with nonnegative
quadratic coefficients. Sorting equal-dimension columns removes only
permutations, not categorical possibilities.

Every non-low central simple has unit restriction coordinate zero. Its
remaining coordinates are bounded by the diagonal induction Gram entries.
The condition `D/z` integral is necessary: the center formal codegree
`D^2/z^2` is integral, so `D/z` is integral over the algebraic integers and
is an algebraic integer. Since `D=80(9+4sqrt(5))` and the parenthesis is a
unit, the implemented test reduces to the exact integral-basis test on
`80/z`. Residual Gram positivity, its kernel, and individual rank-one
subtraction are further necessary conditions. The signed Galois transport
uses whichever of `T(v)` and `-T(v)` is nonnegative; mixed-sign or
nonintegral images cannot be restrictions of central simples. The domain
then closes under that actual transport and duality.

`verify_source_domains.run()` regenerates all 15 low frames and 163,766
bounded high rows. The exact character table is complete, with all products,
formal codegrees, and distinct characters checked. Its assignment recursion
tests every bijection allowed by `dim(A_E)=D/f_E` and the symmetric S-block
reciprocity equations. Precisely low frames 6 and 8 have assignments.

The second-indicator list is the complete list satisfying the existing
necessary odd-multiplicity orthogonal/symplectic constraints. All seven
canonical source objects are self-dual. The positive case is exactly
`[1,1,1,1,1,1,1]`; no zero indicators belong to this tensor. All four
negative-indicator labellings in each surviving frame are independently
covered by exact covectors, giving eight distinct alternatives. These
negative cases are not silently omitted when the later builder selects
positive cases.

The four positive labels of frame 8 fall into the two classes
`[[0,4],[2,6]]`. Within a class the same character is attached to the same
restriction row; only indistinguishable row positions have changed.
This is an exact identity of labelled data. Both representatives 0 and 2
are retained. Exhaustive source automorphisms do not identify the two
classes or their conductor-five signs.

## Why the four active allocations are exhaustive

The codegree-five character difference saturates the conductor-five
compression norm. The equality proof in
`Q5_SATURATION_INDEPENDENT_AUDIT.md` and `LOW_COMPRESSION_PROOF.md` is an
all-level statement: the extremal vectors in the universal induced
representation depend only on coordinates modulo five, and all other
local factors act trivially. Its generated representation therefore has
level five. The twist equation, or the independent finite level-five
calculation, fixes the primitive-fifth-root Legendre class. The known
induced-unit subspace already exhausts its twist-one component.
Consequently a high restriction row with `v4 != v5` has exactly the
prescribed primitive-fifth relative phase, and cannot have twist one.

The remaining squared-difference Gram budget is eight. The full
spectrally integral domain has 25 active orbit types of weight two, 27 of
weight eight, and six whose raw weight four is doubled by actual
fixed/dual transport. Hence every allocation is among
`binomial(28,4)+27+6 = 20,508` nonnegative integral multisets. The recursion
enumerates all of them without a degree or search cutoff. Necessary
residual Gram entry, kernel, and PSD tests leave 126 allocations in frame
6 and 166 in frame 8.

The inactive-lattice argument only needs a containing integer lattice.
The replay checks containment of every inactive column, then exact
membership of each candidate residual target. It does not trust a native
HNF computation as a proof of nonmembership. There are 32 survivors per
positive labelling. For each frame the exact Farkas records eliminate
28 of those 32 per label. Frame 6's remaining sixteen alternatives are
closed by sixteen complete integer trees with 775 exact leaves.

For frame 8 the wrapper cross-matches all 128 distinct `(label,allocation)`
records. The 112 exclusions leave exactly allocations `0,19,160,165` for
every positive labelling. An allocation is transferred into C8 by its
actual complete restriction-row orbit and actual multiplicity, not an
accidentally matching phase index. Both the producer and independent final
checker verify that every desired positive orbit occurs and that the
new packet unit divides its multiplicity. Every subsequent column removal
has a nonnegative Gram-entry or PSD obstruction.

## Arbitrary twist orders and signed phase transport

Categorical Cauchy restricts the prime divisors of the center exponent to
2 and 5, because `D` is 80 times an algebraic unit. Let
`F=Q(sqrt(5),zeta_8)`. For moments 1,2,4,8, relative trace over `F`
vanishes at every primitive fifth-primary order at least 25, and at
two-primary order `2^a` when `a>=7`. In the complement every order divides
320. Enumerating its roots gives 60 distinct nonzero moment tuples:
24 first-visible, then 12 each first visible at powers 2,4,8. Adding the
genuine-zero tuple gives 61. This is an exhaustive relative-moment
inventory, not a claim that actual twists have order dividing 320.

The source character field for R3895 is `Q(sqrt(5))`. Fixing the larger
field `L=Q(sqrt(5),sqrt(-2))` only weakens its necessary Galois restrictions.
The source-fixed square subgroup gives per-row cycles of size
`2^max(a-3,0) 5^max(b-1,0)`. These yield visible packet units 1,2,4,8
and genuine-zero units generated by 16 and 5. If the actual sign-corrected
sqrt(5) transport fixes the row or sends it to its dual, fifth-primary
inversion supplies a disjoint equal packet. The genuine-zero refinements
by exact fifth-primary part 1,5,at least25 are therefore 16,32,10 on
these rows (and 16,16,5 generally). The builder uses actual `+/-T`, never
the previously retracted unsigned positivity assertion.

Using a common relative phase throughout a row orbit is valid. A Galois
permutation acts on anomaly-one center twists by a square power; square
powers fix `F` and therefore preserve every relative moment tuple. Duality
preserves twists. Equal packet multiplicities per row follow from these
bijections. Hidden fifth-primary mass is split into separate variables;
the primary-projection relation is not imposed merely on visible phases.
The FP-difference vector gives total squared weight 160 and known low
contribution eight. Its audited local projection identity gives true
fifth-primary masses `c,4c,160-5c`, with `8<=c<=32`.

The independent Fraction/CRT verifier checks all 320 roots, the complete
fibres and units, and higher-order cancellation controls. The uniform
all-order argument is supplied by the proof, not inferred from those
finite controls.

## Rotation equations, word integrality, and the norm slack

The pivotal grouping identities are
`Tr(R8)=nu8(X)`, `Tr(R8^2)=nu4(X^2)`, and
`Tr(R8^4)=nu2(X^4)`, with `R8^8=1`. The full nonnegative integer
eigenspace variables are retained. The equations allow the half-integral
sqrt(2) coordinates of `Z[zeta8]`; they do not require indicators of
self-dual objects to be real. Unit contributions in `nu4(X^2)` and the
induction formulas are present. The same argument supplies the C4 block.
For source object 1, direct tensor multiplication gives
`dim Hom(1,X1^4)=11` and `nu2(X1^2)=7`, so its C4 multiplicities are
`(r,9-r,s,2-s)`, with all thirty choices `0<=r<=9,0<=s<=2` retained.

For every integral word in the low central objects, its unit multiplicity
is the spectral trace of that word. Its finite spectral order lies in a
product of rings of integers. Closure modulo the trace denominator
therefore produces necessary finite linear congruences. The implementation
checks weighted Galois invariance of each complete orbit and stabilizes
the generated order; it does not assume unsigned transport. Arbitrary
order-basis traces are constrained only to be integers. Nonnegativity is
used separately for actual fusion monomials and positive products.

The fusion-norm cut follows from `sum nY vY=F(A_E A_F)`,
`q=sum nY^2`, the exact discrete conjugate
`g*(t)=max_{n>=0 integer}(tn-n^2)`, and integer chord inequalities at
the seven known low simples. Its 26 half-integral orbit costs do require
attention: assigning an integer slack to a general rational inequality
would be invalid. Here the independent parity proof expresses twice
the orbit-cost parity as the sum of necessary all-word rows
`346,347,359,362,373,382,385,390`. It checks every phase and auxiliary
column and the even right side. The norm row 345 is excluded from this
argument. The remaining norm terms are actual integral fusion
multiplicities with integral coefficients. Thus the unscaled norm gap
really is an integer and the frozen slack is valid.

One concrete replay gap was found and repaired during this audit.
`search.prepare` originally loaded the filtered low-Verlinde coefficient
cache, whereas the earlier source verifier recomputed the larger old
domain. The wrapper now calls `coefficients(...,use_cache=False)`, compares
all 56 triples across the complete filtered domain, and replaces its
prepared table by the fresh result before rebuilding either C8 system.
The cache is consequently not an unverified mathematical premise.

## Exactly fifteen terminal obligations and the acceptance gate

The eight complete C4 split records each cover thirty ordered integer
pairs. Their 225 exact exclusions leave:

| label case | active allocation | remaining `(r,s)` |
|---|---|---|
| 0 | 0,19,160,165 | `(5,1)` and `(6,1)` for each |
| 2 | 0 | `(6,1)` |
| 2 | 19,160,165 | `(5,1)` and `(6,1)` for each |

This is eight plus seven, exactly fifteen, with no duplicated or omitted
case. The wrapper compares the freshly derived ordered list against this
inventory. `criteria/verify_r3895_probing.py` independently reconstructs
the source Gram, forced active counts, every one-packet removal, the C4
coordinates, and integer PSD orbit capacities. Rounding a capacity down
to the gcd of its available packet units is valid because the actual
orbit multiplicity is a sum of those units. Its split test partitions
all integers at each floor. Every discarded side and the final surviving
side must have an exact covector nonnegative on every augmented column
and strictly negative on the target. A numerical status is never a leaf.

The strict wrapper rejects a missing record, a partial record, or one
without `terminal_y` before claiming success. The independent final
checker again requires the complete status, matrix identity, input
hashes, all split leaves, and the terminal covector. Legacy generated
receipts are regenerated in memory; the wrapper does not read old PASS
statuses as proof. Imported source modules, finite inputs, and theorem
notes are included in the final dependency inventory. The final
acceptance run must remain read-only and pass normally and under `-O`
with numerical optimizers unavailable.

The companion `audit_r3895_chain_coverage.py` passes in normal and optimized
Python. It independently checks the original self-dual tensor and C4
values, all eight negative-case keys, identical-row label classes,
the Fraction/CRT phase inventory, norm parity, all 240 C4 record keys,
and the exact fifteen-case complement. Its receipt is
`r3895_chain_independent_coverage.json`, deliberately labelled
`PASS_coverage_checks_only`. Individual final-leaf arithmetic and the
strict whole-chain replay remain separate acceptance obligations.
