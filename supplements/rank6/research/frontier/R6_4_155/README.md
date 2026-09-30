# R6_4_155

The generalized near-group ring R′(4) remains unresolved. Fermion fixed-point
traces and odd Gauss sums leave one induction profile, of center rank 52.
Its twist spectrum is forced, with exponent 24.

* [Center profile proof](center_cuts.md) and [exact replay](verify_center_cuts.py).
* [Forced twist spectrum](forced_twists.md) and [symbolic replay](verify_forced_twists.py).
* [Spherical reduction](structural_note.md).
* [No braided Morita representative](structural_reductions.md).
* [Canonical Ising extension](ising_final_reduction.md).

From the package root:

```bash
python -O research/frontier/R6_4_155/verify_center_cuts.py --verify
```

The retained [six-profile reduction](../../round5/m4_155/) supplies the
exhaustive input. These necessary conditions do not construct a category.
