# Independent audit of the complete R5039 cyclic-rotation chain

The mathematical and branch-coverage audit passes. An independent optimized
Python execution of
`models/sqrt5/verify_r5039_cyclic_chain.py::verify` completed all 23 stages in
145 seconds, including both conductor-eight branch-two modular certificates
and all 48 branch-zero trees with 96 exact Farkas leaves. The receipt is
`criteria/r5039_chain_independent_optimized.json`. Final publication acceptance
and the frozen dependency manifest remain separate root-owned steps.

The final packaging gate also passes. The producer's final normal receipt
records two complete same-process replays, and its final optimized receipt
records one. Both cover the same 23 stages and have the identical 136-file
manifest, whose sorted compact-JSON SHA256 is
`370fe2a5e39572e188f9ef9f6f1ae45d5485531b4b21f7bb3491231ab5b5137f`.
Every bound file was independently compared with its current bytes. The
manifest includes the two legacy spec-loaded code dependencies that the
initial automatic inventory missed, and it is stable in warmed processes.
The final local tree replay uses only integer arithmetic and the standard
library; its branch and Farkas logic was independently reviewed against the
previously replayed formulation.

The canonical compact-JSON tensor digest is
`8606c63a2f02ea028185db755a4b055382073b94736d5040ee92f3eec07f450c`.

## Scope and completeness

The conclusion excludes a fusion category over the complex numbers with this
based Grothendieck ring. It assumes neither a pivotal structure nor
pseudo-unitarity initially. It makes no positive-characteristic assertion.

The following obligations were checked in the source, in the mathematical
notes, and in the replay rather than inferred from numerical solver output.

1. **General categorical scope.** Complete oriented sphericalization
   enumeration gives four signed quotients. The two nongauge cases require
   both `Q(sqrt(5))` and `Q(sqrt(11))` in the dimension field,
   although every possible signed dimension character has degree at most
   two. The other two cases give a spherical section. Every original
   character outside the Frobenius–Perron Galois orbit vanishes on a simple
   object or distinguishes a dual pair. Thus a suitable Galois conjugate is
   pseudo-unitary. The signed-character calculation uses component degrees
   and verifies commutativity; it does not apply unsigned dual formulas to
   the nongauge signed tensors.
2. **Complete restriction domain.** The induction Gram matrix, positive
   dimension vector, formal codegrees, character table and signed Galois
   row transport are reconstructed from the canonical tensor. Enumeration
   gives four low frames and 142,510 high row candidates. Character
   reciprocity leaves frames 1 and 3. Frame 1 violates the conductor-eight
   twist-one weight bound. Frame 3 has twelve label assignments, exactly
   the two classes `[0,2,4,6,8,10]` and `[1,3,5,7,9,11]`. Both classes are
   retained. The complete second-indicator choice is
   `(1,0,0,1,1,1,1)`.
3. **All twist orders.** The categorical Cauchy theorem restricts prime
   support to 2 and 5, since the dimension is 80 times a unit. Relative
   moments of powers 1, 2, 4 and 8 in
   `Q(sqrt(5),sqrt(2),i)` have exactly 61 types. The finite cyclotomic check
   is coupled to the prime-power proof: the zero type covers every order
   invisible at those moments. There is no assumed exponent cutoff.
   Source-fixed square-action packets, including the zero-packet refinements,
   use the full source field `Q(sqrt(5),sqrt(-2))`. Actual positive transport
   is `+T` or `-T`, as appropriate; no unsigned orbit-size claim is used.
4. **Complete conductor-eight split.** The exact primary masses are
   `c,c,2c,4c`, with `0<=c<=2`. Categorical duality makes `c` even, hence
   only 0 and 2 are possible. Independent row-fixed square cycles prove
   the finite active support used in both cases. For each label class,
   the branch-two covector annihilates all 1,700 columns modulo 256 but
   evaluates to 128 on the target.
5. **Complete branch-zero reductions.** Raw tensor Gram reconstruction
   verifies the aggregate allocations. One-sided inactive-lattice
   containment is sufficient for every recorded rejection; a trusted HNF
   result is not needed. The complete phase enumeration has 615 choices
   and leaves four. All five C4 characters for source object 1 are checked;
   only multiplicities `(3,1,0,0)` remain. The conductor-five squared
   difference budget then has 1,004 raw allocations and exactly 50
   nonnegative positive-semidefinite residual Grams. No allocation is
   dropped using a floating-point test. Exact separators leave respectively
   16 and 8 phase/allocation combinations in the two label classes.
6. **Forced eighth-moment packet.** Direct coefficient reconstruction shows
   that the unwanted `sqrt(10)` and `i sqrt(10)` coordinates receive
   inactive contributions only from order-320 packets on orbits 45 and 50.
   Their row vectors are independent. Exact Gram capacities permit at most
   one packet on orbit 45 and at most two on orbit 50. Cancellation forces
   zero on orbit 45 and exactly one on orbit 50, with two possible phases.
   Other phases on orbit 50 remain allowed. This is an exhaustive two-way
   refinement of each of the 24 preceding combinations.
7. **Final integer contradiction.** Every one of the resulting 48 trees is
   matched to its preceding phase, label and conductor-five allocation.
   Each residual matrix and orbit-capacity inequality is reconstructed
   from the raw Gram matrix. Integer capacities are rounded only by the
   gcd of actual remaining packet units. Every tree splits an integer
   variable into `x<=k` and `x>=k+1`, and each leaf is checked by integer
   dot products against every residual column. The two leaves of each
   tree cover every integer value. All 96 leaves pass.

The fourth/eighth cyclic equations were also previously checked by a separate
raw-tensor derivation and actual pointed-center controls. They retain complete
cyclotomic eigenspace multiplicities, including the allowed half-integral
coordinates in the quadratic-radical presentation of eighth roots.

## Minimal mathematical dependency families

A frozen manifest should bind the following logical families, together with
the exact code and finite inputs actually read by the verifier:

| Family | Main proof or verifier |
| --- | --- |
| Sphericalization and Galois reduction | `sqrt5_reduction/PROOF.md`, `verify_reduction.py` |
| Complete low/high character domain | `modules/verify_r5039_c2_domain.py`, source-domain builders |
| Galois row transport | `models/sqrt5/TRANSPORT_PROOF.md` |
| Low compression and conductor-five saturation | `models/sqrt5/LOW_COMPRESSION_PROOF.md`, `modules/Q5_SATURATION_INDEPENDENT_AUDIT.md` |
| Conductor-eight projections and complete split | `models/sqrt5/CONDUCTOR8_BUDGET_PROOF.md`, `modules/CHI_MINUS8_SIGN_SAFE_DICHOTOMY.md` |
| Prime-five exact primary masses | `modules/PRIME_PROJECTION_FP_WEIGHTS.md` |
| All-order moment and packet inventory | `models/sqrt5/POWER_MOMENT_PHASES_PROOF.md`, `verify_power_phase_inventory.py` |
| Center moments and cyclic rotations | `models/sqrt5/CYCLIC_ROTATION_OBSTRUCTION.md`, `modules/FOURTH_INDICATOR_INDEPENDENT_AUDIT.md`, `modules/EIGHTH_INDICATOR_SYSTEM.md` |
| Auxiliary integer fusion constraints | `models/sqrt5/INTEGRAL_FUSION_NORM_PROOF.md`, `modules/ALL_WORD_UNIT_FUNCTIONAL.md` |
| Finite phase/Gram/rotation/phi partitions | their source-bound enumeration and exact replay modules |
| Forced order-320 packet | `models/sqrt5/C0_FORCED_EIGHTH_PACKET.md`, `verify_c0_forced_eighth_packet.py` |
| Final capacities and integer trees | `modules/verify_c0_capacity_trees.py`, all 48 finite tree certificates |

The proof relies on exact mathematical inputs and finite certificates, not on
previous PASS receipts, discovery logs, or solver statuses. A dependency
manifest may contain more code than this logical list because importing a
shared module is a file dependency even when only one exact function is used.

## Suggested accepted-certificate interface

The publication adapter should require `kind = q5_cyclic_rotation_general`,
`scope = general_complex`, the exact identifier and tensor digest, and a
manifest of repository-relative paths and SHA256 values. The manifest should
bind the verifier entry point, all finite input files actually consumed, and
the mathematical notes above. It should be immutable during replay.

After checking the binding, the adapter should call `verify(id, tensor)` and
require the returned tensor digest, `status = PASS`, two branch-two
representatives, 48 complete branch-zero trees and 96 exact leaves. The
function must reconstruct coverage, not merely compare those counts. The
current verifier does reconstruct coverage and compares the exact final
branch set with the preceding unresolved set.

No accepted ledger, dispatcher, or publication file was changed in this audit.
