# R3895 complete-chain obligations

This is a proof-coverage checklist and replay design, not an exclusion claim.
The canonical tensor is `R7_5_3895`, SHA-256
`590b613093643a1c3047e866213050ba7fd87c211a42906de823d0c613d11ad0`.
Numerical infeasibility, interrupted probing, and previously written PASS
receipts are not premises of the intended final replay.

1. **General scope.** `sqrt5_reduction/verify_reduction.py::run()` regenerates
   the complete signed-quotient enumeration and its exact obstructions. The
   accompanying proof establishes sphericality and a pseudo-unitary Galois
   conjugate for a hypothetical categorification of this original rank-seven
   tensor. Sphericalization is an intermediate proof device; the subsequent
   center is that of the rank-seven category.
2. **Every induction frame and row.**
   `integral_gram/verify_source_domains.py::run()` regenerates all 15 low
   frames and 163,766 high restriction rows, including signed Galois transport
   and duality. Exact character reciprocity leaves precisely frames 6 and 8.
   It regenerates both full orbit domains, all eight positive-indicator
   integer systems, and every saturated conductor-five allocation.
3. **All second-indicator and frame-6 alternatives.**
   `negative_indicators.py` checks the covector covering all eight negative
   indicator labellings. `verify_frame6.py::run()` also covers 20,508 raw
   active allocations, 126 positive Gram allocations, 32 lattice survivors
   per labelling, 112 rational Farkas exclusions and 16 complete integer trees
   with 775 leaves. No frame-6 alternative remains.
4. **Complete frame-8 phase allocation coverage.** Its 20,508 raw active
   allocations leave 166 positive Gram allocations. Exact inactive-lattice
   containment leaves 32 for each positive labelling. Replaying the 128
   records in `R7_5_3895_branch_farkas_8.json` eliminates 112; the only
   remaining allocation indices are `0,19,160,165`. Branch-specific Gram
   pruning is checked separately and cannot silently remove an allocation.
5. **Both label classes.** Exhaustive character-to-row assignment gives
   `[[0,4],[2,6]]` for the positive frame-8 labels. Equality here means the
   same character is attached to the same restriction row. The two classes
   are not identified by a source automorphism. Both representatives 0 and 2
   must be replayed, with their own conductor-five sign.
6. **All-order phase and rotation premises.** The independently checked
   61-record inventory over `Q(sqrt(5),zeta_8)` covers moments 1,2,4,8 for
   arbitrary twist orders with prime factors 2 and 5. The full source field
   of this ring is `Q(sqrt(5))`; the common larger field
   `Q(sqrt(5),sqrt(-2))` may be fixed to obtain the weaker, valid packet
   restrictions used in the builder. The proof uses actual sign-normalized
   row transport, never the retracted assertion that raw transport is
   nonnegative. Cyclic fourth/eighth multiplicities follow from pivotal
   rotation and its grouping identities; conductor-five saturation and
   primary-order budgets have their separate audited representation-theory
   hypotheses.
7. **Exact full systems.** Rebuild both C8 systems from the raw tensor,
   complete domain, exact character table and phase inventory. Regenerate
   all 56 low-Verlinde coefficients on the filtered C8 orbit domain with
   caching disabled and compare the entire cached payload. Regenerate the
   finite all-word congruences, and independently recompute the integral
   fusion-norm inequality. The frozen norm row has half-integral orbit
   costs: its integer slack is justified only after the separate parity
   proof using all-word rows `346,347,359,362,373,382,385,390`; row 345 itself
   is not used to prove that parity.
8. **All C4 alternatives after phase restriction.** Map each of the four
   old allocations to the C8 columns by actual restriction-row orbit, and
   reconstruct every Gram removal. The first nonunit source object has
   C4 multiplicities `(r,9-r,s,2-s)`, so all 30 pairs
   `0<=r<=9, 0<=s<=2` occur. The eight complete exact rotation-split records
   eliminate 225 of their 240 alternatives. Exactly the following 15 remain:

   | label case | phase allocation | remaining `(r,s)` |
   |---|---|---|
   | 0 | 0,19,160,165 | (5,1), (6,1), for each allocation |
   | 2 | 0 | (6,1) |
   | 2 | 19,160,165 | (5,1), (6,1), for each allocation |

9. **Each final branch.**
   `criteria/verify_r3895_probing.py::verify(case,allocation,r,s)` independently
   reconstructs the raw induction Gram, active counts, one-packet removals,
   fixed C4 coordinates, and integer orbit capacities by a direct finite
   scan. It replays every discarded side of every integer split and the
   terminal exact Farkas covector. Only the status
   `complete_conditional_exclusion` with a terminal covector closes a branch.
   The intended wrapper must fail if any of the 15 records is missing or
   incomplete, and must cross-match the complete branch inventory rather
   than trust a discovery log.

The final receipt must bind the tensor, all finite domain/certificate inputs,
all actual verifier modules, and the theorem notes. Generated receipts and
discovery logs must not become mathematical premises. The callable should be
read-only, deterministic after warmed imports, and independently replayed
under normal and optimized Python with numerical optimizers unavailable.
