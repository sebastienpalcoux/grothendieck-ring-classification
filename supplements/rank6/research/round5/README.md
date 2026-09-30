# Current exact research frontier

The ledger retains **6 unresolved rings**. Every result below is a necessary reduction; none constructs a categorification.

The shared criteria combine restriction and word Gram matrices, exact finite coefficient domains, common twist assignments, ribbon balancing, and finite fusion or modular reconstruction. Saturated dimension-block bounds also force twist support and exact finite-representation moment identities where their hypotheses hold. Subcategory projection supplies integral modular intertwiners and individual capacities; a verified disjoint-column condition permits subrepresentation subtraction. Large-prime indicator constraints apply when a full twist exponent is proved.

| Ring | Strongest verified necessary data | Evidence |
|---|---|---|
| `R6_4_22` | The remaining center has rank 36. Its necessary fusion ring and modular data are unique up to relabelling and complex conjugation; categorification remains open. | [certificate 1](fermion/R6_4_22_certificate.json), [certificate 2](quartic_pair/R6_4_22_center_reconstruction.json) |
| `R6_4_91` | Only center rank 42 remains: a forced Ising factor and a rank 14 centralizer with one fusion-ring orbit and two conjugate modular data. | [certificate 1](quartic_pair/R6_4_91_center_reconstruction.json) |
| `R6_4_155` | Six induction profiles remain, each with one forced pair of low fusion matrices in its semion centralizer. None is a categorification certificate. | [certificate 1](../round4/m4_155/reduction.json), [certificate 2](m4_155/frontier_certificate.json) |
| `R6_4_629` | Only center rank 35 remains, with one necessary fusion/modular datum up to conjugation and identical-column relabelling; categorical realization remains open. | [certificate 1](m4_629/modular_reduction_certificate.json), [certificate 2](m4_629/rank35_fusion_data.json) |
| `R6_5_1204` | A complete exact reduction leaves 171 induction profiles; the signed-gauge argument covers general categorifications. | [certificate 1](m5_1204/profile_certificate.json), [certificate 2](m5_1204/joint_domain_certificate.json), [certificate 3](m5_1204/remaining_profiles.json) |
| `R6_8_1660` | Actual-root induction and congruence cuts leave three branches with 168, 798 and 798 necessary profiles; the center twist exponent divides 48. | [certificate 1](../round4/m8/R6_8_1660_reduction.json), [certificate 2](m8_1660/low0_profiles.json), [certificate 3](m8_1660/low1_profiles.json), [certificate 4](m8_actual48/certificate.json) |

[Coverage and staged reductions](coverage.json) record the precise domains, canonical commands, receipts and source bindings. The [six-input manifest](../../verification/round5/campaign_manifest.json) stores the full tensors and their hashes.

Run from the package root:

```bash
python -O software/round5_replay.py --list
python -O software/round5_replay.py --check-receipts
python -O software/round5_replay.py --select controls
python -O software/round5_replay.py --select R6_5_1204,R6_4_629 --jobs 2
```

The receipt audit checks declared hashes and completion predicates only. It does **not** rerun mathematical proofs, and pending bindings fail that audit. Ordinary replay runs the selected verifiers under optimized Python with separate logs and fresh receipts, preserving the retained receipt files. Each command has a 15-minute deadline; use one job for the largest case. A timeout is incomplete and proves no exclusion.

Shared controls cover exact finite domains and the known centers of Vec(C2), Vec(C3), Rep(S3), Fibonacci and Ising. These are explicit controls, not a full-census or all-model rescreen. Earlier accepted proofs and source-bound receipts remain available in their original directories.

This index is generated from coverage.json by `python -O software/round5_replay.py --write-index`.
