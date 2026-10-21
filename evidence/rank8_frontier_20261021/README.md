# Further investigation of the rank-eight frontier

This continuation investigates the 34 unresolved rings in the original exact-multiplicity-three release. The accepted inventory records **25 further general complex exclusions** and leaves **nine unresolved rings**. No additional categorification is asserted in this continuation; the original 14 unitary models in this band are retained.

The resulting exact-multiplicity-three partition is **3,504 excluded + 14 realized + 9 unresolved = 3,527**. Through multiplicity three, the partition is **4,400 excluded + 91 realized + 9 unresolved = 4,500**. The original ledger, source tensors, proof inputs and replay receipts remain unchanged. New decisions are recorded in [accepted.json](accepted.json) and reconciled into a separate publication ledger.

## Reading the results

- [Per-ring research audit](structural_models/per_ring_research_audit.md): every original frontier tensor, previous attempts, new domains, conclusions and limitations. Its [JSON version](structural_models/per_ring_research_audit.json) binds the exact sources.
- [Replay registry](research_checks.json): the mathematical checks and research controls required by the continuation verifier.
- [Current manuscript](../../manuscripts/rank8/paper/rank8.pdf): arguments, constructions from the original release, and the further exclusions and scoped investigations.
- [Accepted certificates](accepted.json): only these reviewed decisions change the mathematical ledger. A failed numerical search never supplies an exclusion.

The unified methods include full character-labeled central induction and modular symmetry, correlated relative twist traces and rotation equations, integer central Gram decompositions and cubic Verlinde coefficients, simultaneous Galois spectra, integral-center restrictions, source-unit product identities, exact global phase cuts, and module-category, Morita and cohomological arguments. General-complex exclusions include the required signed sphericalization and Galois reduction wherever a pseudo-unitary argument is used.

An [explicit pointed-category counterexample](review/FERMION_DIMENSION_CHARACTER_COUNTEREXAMPLE.md) disproves a tempting general dimension-character obstruction for a free central fermion. It is an exact control for the reasoning, not a model for `R8_3_941`.

Construction searches include complete finite tensor comparisons, based modules and possible underlying objects of connected algebras, and the all-level SU(2)/adjoint product family and specified unbounded generalized near-group families. An underlying object is not an algebra structure; a feasible center constraint system is not an associator or a category.

## Remaining cases

The remaining identifiers are `R8_3_65`, `R8_3_721`, `R8_3_928`, `R8_3_941`, `R8_3_982`, `R8_3_1154`, `R8_3_1768`, `R8_3_1795`, and `R8_3_3472`.

| Ring | Selected strongest outcomes and outstanding issue |
|---|---|
| `R8_3_65` | The displayed integer center pattern fails all four phase branches. An exact uniform phase cut rejects it, but the subsequent bounded integer search is inconclusive. The generalized free-orbit construction remains open. |
| `R8_3_721` | Four complete integer central patterns survive the stated joint-spectrum and rotation tests. Full comparison excludes the six known Asaeda–Haagerup Morita categories as models. |
| `R8_3_928` | The central semion constraints leave ten correlated moment patterns. Four have checked integer phase witnesses; six integer-feasibility questions remain unresolved. |
| `R8_3_941` | The central fermion, paired-phase, permutation and mixed-trace tests leave fourteen patterns. Eleven have checked integer phase witnesses; three integer-feasibility questions remain unresolved. |
| `R8_3_982` | All four low frames pass signed lattice membership. Two displayed integer patterns fail every allowed fixed-mass phase branch; the other frames have exact bounded rational primals. Other integer patterns are not excluded. |
| `R8_3_1154` | The complete integer Gram screen reduces 14,211 patterns to 1,238 cubic/spectral survivors; 1,230 survive the height-six rotation/STS test. The construction problem remains open. |
| `R8_3_1768` | Complete stated support, integer cubic, joint-spectrum and source-unit constraints are tested. Signed lattice membership does not settle bounded integer feasibility or categorification. |
| `R8_3_1795` | The strengthened integer central system passes exact box and modular checks. A 120-second Hermite cap and 210-second bounded proposal wall cap give no further exact conclusion; neither lattice membership nor integer feasibility is asserted. |
| `R8_3_3472` | Full-character support and the strengthened integer system pass the recorded exact box/modular screens. Bounded integer search is inconclusive; the larger-field STS domain is not claimed exhausted. |

After completion of the documented campaign, “extensively investigated exotic candidate” is used in the requested operational sense: a ring has survived many case-specific known and newly developed exclusion and construction attempts, including complete finite domains and specified unbounded families. This does **not** prove categorifiability or novelty. Arbitrary associators and unrestricted chains of constructions have not been exhausted. The explicit final screening assessment and each attempt's scope are in the per-ring audit.

## Reproducing the checks

From the repository root, after restoring packaged data and installing the recorded dependencies:

```sh
python tools/restore_data.py
python -m pip install -r supplements/rank7/requirements-m5.txt
python supplements/rank8/software/verify_m3_continuation.py --output frontier-validation/baseline_normal.json
python -O supplements/rank8/software/verify_m3_continuation.py --output frontier-validation/baseline_optimized.json
python tools/verify_rank8_frontier.py
python -O tools/verify_rank8_frontier.py
```

The explicit baseline output paths preserve the original published receipts. The continuation verifier checks all registered source-bound commands; its final integer-stage dispatcher runs the large domains sequentially. `--metadata-only` checks source and receipt identities without repeating the mathematics. `--prepare` creates a ledger and source manifest but certifies no mathematics.

The separate frontier archive preserves the original M3 package and records both continuation replay lanes. Its release builder additionally performs a fresh full normal-Python replay using only the extracted package, with separate receipt and logs. Computational replay validates the stated identities and certificates; independent human mathematical verification and Lean formalization are not asserted.
