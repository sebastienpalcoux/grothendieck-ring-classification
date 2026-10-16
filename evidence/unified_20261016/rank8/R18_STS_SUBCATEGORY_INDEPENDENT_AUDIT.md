# Independent audit of the general R8_1_18 obstruction

Status: PASS. Independent optimized replay of the complete source-bound
verifier passes all 24 branches. This audit was performed by the rank8
subcategory agent, independently of the proof/certificate author.

## Categorical and arithmetic premises

1. General complex scope is reduced to the pseudo-unitary case by the
   established two-FP-dimension Galois pseudo-unitarity theorem. The source
   tensor has dimensions 1 and d=2+sqrt(5), with d²=1+4d and
   D=8+16d. No unitarity assumption is made.

2. The actual character correspondence, not an arbitrary bijection between
   equal-dimensional objects, gives S(A_chi,Z)=chi(FZ)/f_chi for every
   central simple Z. I independently reopened Ostrik arXiv:1309.4822,
   Example 2.9 and the definition before Theorem 2.13. The full modular
   identity on the twist-one low block gives

       sum_Z theta_Z v_Z v_Z^t = B^t conjugate(Cmat).

   The separate `R18_STS_INDEPENDENT_AUDIT.md` derives this identity in
   detail. Its separate standard-library verifier independently enumerates
   all eight low assignments and checks all 392 nonunit target entries.
   The normalized K-trace is 4-d on the nonpointed block and zero on the
   remaining nonunit entries.

3. I independently reopened Bruillard--Ng--Rowell--Wang arXiv:1310.7050,
   Theorem 3.9, including its proof's passage to arbitrary spherical
   fusion categories. It does not require integral global dimension.
   Since Norm_K(D)=320=2^6*5, every prime dividing FSexp is 2 or 5.
   For moment powers 1,2,4, any root with fifth-adic exponent at least
   two or 2-adic exponent at least four has all three relative traces
   zero. All remaining triples arise from fortieth roots. The 13 triples
   used in the verifier therefore cover every possible root, with no
   assumption FSexp divides 40.

4. The fourth indicator is the trace of an operator whose fourth power is
   identity. It belongs to Z[i]; normalized trace to K=Q(sqrt(5)) is an
   integer, since K is real and disjoint from Q(i). Therefore the fourth
   induction trace, after relative trace, belongs to D*Q. The rational
   functional ell(a+bd)=2a-b annihilates it. This argument does not assume
   that the fourth indicator itself is real, or use an unproved claim
   about third indicators.

5. The cyclic Fourier bound is the already independently audited R9
   lemma and applies to every pointed C4 associator class. The exact
   pointed induction Gram is 8I4, so coefficients at a and a^-1 in every
   high row are at most one. The pointed twist triples used for k=0,
   k=2 and k odd follow from theta^4=nu4(a) and theta²=nu2(a²).
   The two odd classes have identical relative triples and may be grouped.

6. The quadratic transport, extra Q(zeta8) automorphism, and duality
   preserve the high-row domain. The extra permutation is independently
   source-character verified. Galois-related central objects have equal
   normalized relative moments because their twists differ by sigma²,
   whose restriction to the quadratic field K is the identity. Duality
   preserves twists. Consequently full row-orbit multiplicities and
   relative moment histograms are equal. Summing one copy of each distinct
   row in an orbit is a necessary PSD subtraction even when an actual
   central Galois orbit has larger fibers.

## Finite domain and replay

I read the complete final verifier. It binds all 512 source coefficients
through the immutable SHA and explicit model multiplication, verifies
the six distinct non-FP characters and their formal codegrees, enumerates
all eight reciprocal/dual low assignments, and reconstructs the STS
target in each. The high domain is exhaustive: diagonal Gram bounds,
cyclic Fourier bounds, integral D/dim(Z), integral signed quadratic
transport, full Galois/duality closure, and entrywise/PSD orbit subtraction.
PSD is tested by rational Schur complements; a zero pivot with a nonzero
remaining row is rejected, which is the correct semidefinite condition.

Every resulting column is an exact integer vector after scaling moments
by eight. No optimization result or numerical PSD pruning enters the
verifier. Each of the three stored integer covectors pairs nonnegatively
with every generated column and pairs to -256 with every applicable
target. The independent optimized replay gives:

| Pointed class | Low frames | Full row orbits per frame | Columns per frame | Minimum column pairing | Target pairing |
|---|---:|---:|---:|---:|---:|
| 0 | 8 | 25 | 167 | 0 | -256 |
| 1 or 3 | 8 | 25 | 145 | 0 | -256 |
| 2 | 8 | 25 | 153 | 0 | -256 |

Receipt: `r18_sts_moments_subcategory_independent_optimized.json`.

The identity, finite-domain completeness, and exact separation therefore
establish nonexistence of a general complex categorification of R8_1_18.
