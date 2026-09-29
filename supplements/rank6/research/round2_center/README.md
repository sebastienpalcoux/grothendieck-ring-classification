# Exhaustive stabilizer-rotation continuation

The final certificate combines the full involution-Morita Gram obstruction,
local stabilizer pair-insertion/rotation theorem, exhaustive third-indicator
central systems, and unrestricted general-to-Galois-pseudo-unitary reduction.
It excludes `R6_3_215` in general scope. It does not assume that its previously
constructed rank-22 central relaxation is the unique possible center.

Replay the complete certificate, including every prerequisite:

```bash
python software/stabilizer_rotation.py R6_3_215 --output certificates/stabilizer_rotation_215.json --verify
python -O software/stabilizer_rotation.py R6_3_215 --output certificates/stabilizer_rotation_215.json --verify
```

Both generic engines accept a tensor, with no census-label exceptions:
`stabilizer_rotation.verify_general(R, certificate)` and
`galois_pseudo_reduction.verify(R, reduction)`. The CLI label only selects the
input tensor and checks the external record's label.

The pseudo-unitary certificate reconstructs all 16 involution-module branches:
12 exact full-Gram Farkas obstructions, 2 rank obstructions, and 2 local
stabilizer-rotation branches. The latter share one conditional certificate
covering all 91 low induction frames, 50 character labellings across 31 frames,
and all 4 second-indicator choices: 200 exact Farkas rays through trace height
3. This conditional certificate alone says that no center can have
`nu3(b4)=nu3(b5)=-1`; the outer local theorem supplies that necessary condition.

The general reduction replays all 1,480 unrestricted signed quotient tables,
all sign orbits, every nongauge character rejection, and uniqueness of the FP
Galois orbit among nonzero original dimension characters. It uses no second
indicator normalization and no fixed dimension pattern.

Additional exploratory files retain the complete integral high-Gram search
and low Verlinde moment pruning. `all_frames.json` is a complete enumeration,
not a categorification certificate. These searches are **not needed** in the
final exclusion. Likewise, the earlier exact rank-22 modular/fusion witness
remains a valid feasible relaxation; it fails the new categorical stabilizer
rotation condition.

To reproduce the supplementary searches:

```bash
python research/round2_center/enumerate_frames.py
python research/round2_center/filter_moments.py
python research/round2_center/filter_joint.py
python research/round2_center/conditional_nu3.py --objects 4
python research/round2_center/conditional_nu3.py --objects 5
```

Both single-object negative-third-indicator searches also separate every
branch. The main stored proof uses the simultaneous constraint and is fully
replayed by the generic checker above.

Optimizer-free and negative-control replays:

```bash
python -O research/round2_center/replay_without_optimizer.py
python -O research/round2_center/mutation_controls.py
```

The frozen reports `general_replay_report.json`,
`optimized_replay_report.json`, and `mutation_report.json` record normal
verification, optimized-Python verification with optimizer entry points
disabled, and rejection of all nine proof mutations.

## Multiplicity-four continuation

The same generic local theorem gives a general exclusion of `R6_4_416`.
Its complete certificate is `certificates/stabilizer_rotation_416.json`
(and the release-discovery copy `R6_4_416_general.json`). Replay with:

```bash
python -O software/stabilizer_rotation_higher.py R6_4_416 --output certificates/stabilizer_rotation_416.json --verify
```

`general_replay_416_report.json` records the successful optimized-Python,
optimizer-disabled composite replay: 2 module branches, 895 low frames,
32 interval Farkas systems, 2,376 unrestricted signed quotients and 83 sign
orbits. `assemble_higher416.py` reproduces this assembly and full replay.
The tensor-parametric reduction additionally rejects the nonzero non-FP
original dimension character by the exact norm criterion at prime 5.

The files `galois_reduction_R6_4_22.json`, `galois_reduction_R6_4_91.json`,
`galois_reduction_R6_4_258.json`, and `galois_reduction_R6_4_325.json` contain
fully verified general-to-Galois-pseudo-unitary reductions for the quartic
continuation. These reductions alone do not assert nonexistence. The generic
reduction handles the noncommutative signed quotient occurring for `R6_4_91`
by replaying the existing exact noncommutative character calculation.

## Cyclotomic criterion positive controls

The canonical `software/cyclotomic_stabilizer_trace.py` API was called on
all 54 catalog model tensors under optimized Python. The catalog IDs were
checked to equal exactly the IDs of all `general=yes` decisions. Reproduce:

```bash
python -O research/round2_center/cyclotomic_positive_controls.py
```

The report `cyclotomic_positive_controls.json` records the criterion source
hash and each exact outcome: 41 fail the forced local stabilizer gate,
3 are noncommutative and outside the engine's scope, 8 fail the required
quartic FP/global-dimension field gate, `R6_2_127` has no supported ambient
cyclotomic embedding, and `R6_4_322` has conductor 24 and prime 3 in its
support, outside the rational-third-indicator gate. The canonical API
returns `None` or its explicit eligibility-guard exception in these cases.
All 54 completed without a time limit or an exclusion certificate.

This is an eligibility/nonexclusion control only: all 54 models are
ineligible for this specific new criterion. No trace system or Farkas
search was invoked, so these results do not claim feasible LP witnesses
inside its eligible quartic domain.
