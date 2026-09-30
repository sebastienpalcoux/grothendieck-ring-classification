# Exact quartic center reconstruction

These are complete necessary-data reductions, not categorical constructions.

- **R6_4_91:** the center-rank-36 profile has no fusion completion. The center-rank-42 profile forces an Ising factor and a rank-14 centralizer. The centralizer has eight labelled fusion tensors, one based-ring orbit, and two compatible conjugate modular data.
- **R6_4_22:** the rank-36 profile has five complete quadratic/cubic word-Gram count patterns and ten possible dualities. Full regular-action completion leaves one central fusion ring and one modular datum for each of the two conjugate low labellings. All twists are forced by balancing with the six low twist-one objects. The separate rank-30 exclusion is in `../fermion/R6_4_22_certificate.json`.

The main records are `R6_4_91_center_reconstruction.json` and `R6_4_22_center_reconstruction.json`. The implementations reconstruct every finite domain from the original census tensor and frozen round-four frontier. Python assertions and numerical optimization are unnecessary.

Run from the package root:

```sh
OPENBLAS_NUM_THREADS=1 python -O software/round5_quartic_pair.py --verify --replay-inherited --output research/round5/quartic_pair/R6_4_91_center_reconstruction.json
OPENBLAS_NUM_THREADS=1 python -O software/round5_regular_completion.py --verify --output research/round5/quartic_pair/R6_4_22_center_reconstruction.json
OPENBLAS_NUM_THREADS=1 python -O software/round5_modular_checks.py --verify --output research/round5/quartic_pair/modular_checks.json
```

The last command checks every surviving modular variant: all coprime higher Gauss sums are positive real; Galois acts by the required signed permutations and squares the twists; every generalized rotation eigenspace at tensor powers 2 through 16 has a nonnegative integral dimension. These further checks survive and do not establish an associator, braiding, or the required induction algebra.

The proofs are in `papers/chapters/frontier_quartic.tex`, with the common Gram, adjunction and regular-action criteria in `papers/chapters/unified_gram.tex`. Superseded discovery scripts, incomplete searches, numeric probes and large intermediate systems are not needed for replay and have been removed from this package.

The categorical positive control `modular_control.py` runs the same generalized composite-rotation checker on `Z(Vec(C3))`, including nonselfdual objects. Run it with `python -O research/round5/quartic_pair/modular_control.py`. The replay receipt `replay_O.json` records the three full verification commands and hashes their input and implementation files.

The two saturated dimension-field characters in each quartic case are complex quartic characters. `conductor_intertwiner.py` checks their full finite-level cyclic representations directly: exact equivariant quotients of the prescribed induced module have dimensions 36 to 18 for R22 and 24 to 24 for R91. Every S/T generator edge and the opposite-character compression identity are checked. Hence valid universal conductor moment and spectral identities already hold on the completed data; the real-character-only shortcut is not used. Replay with:

```sh
python -O research/round5/quartic_pair/conductor_intertwiner.py --verify --output research/round5/quartic_pair/conductor_intertwiner.json
```

The separate receipt is `conductor_intertwiner_replay_O.json`.

The full modular subcategory projection is checked in `subcategory_projection.py`: for the pointed rank-two subcategory of R22 and the Ising subcategory of R91, every nonnegative integral column allowed by twists and forgetting is enumerated. The full S equations have ranks five and seven in the respective five and seven splitting variables. Each conjugate modular variant has exactly one integral projection matrix, recorded in `subcategory_projection.json`; all S, T, forgetful and unit equations are checked directly. This adds no categorical construction or exclusion. The generic theorem and categorical subgroup controls are in `papers/chapters/subcategory_projection.tex` and `research/round5/unification/subcategory_intertwiner_control.py`.

```sh
OPENBLAS_NUM_THREADS=1 python -O research/round5/quartic_pair/subcategory_projection.py --verify
```

Its source-bound exact replay receipt is `subcategory_projection_replay_O.json`.
