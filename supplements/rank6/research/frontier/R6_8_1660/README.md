# R6_8_1660

The ring is free of rank two over its Ising fusion subring and remains unresolved.
The [relative-center construction](relative_center/relative_center_note.tex)
first gives14 necessary based-ring representatives. The
[central Frobenius–Schur and invertible-lift argument](relative_center/central_fs_note.tex)
reduces these to a single representative, up to exchanging the Ising factors.

From the package root:

```bash
python -O research/frontier/R6_8_1660/relative_center/verify_relative_reduction.py
python -O research/frontier/R6_8_1660/relative_center/verify_structural_cuts.py
```

The second check reads the first certificate and all4,764 raw restriction
profiles in the [retained finite domain](../../round5/m8_1660/).
The remaining based ring is a necessary condition, not a categorification.

The [fermion and second-indicator reduction](fermion_profiles/) leaves 1727 of
the 1764 retained labelled full-center profiles.
