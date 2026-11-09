# Separate implementations

The principal runner executes the following checks and saves their reports.
Run them separately from the package root with:

```sh
python3 supplementary/independent/independent_central_audit.py . --workers 4
python3 supplementary/independent/independent_fourth_audit.py .
python3 supplementary/independent/independent_models.py .
```

Each accepts `--output PATH`. The central audit covers all 655 spherical
records: 595 arithmetic exclusions and 60 central-induction exclusions.
It uses spectral-adjugate characters, resultant
norms, full integer boxes and all induction-row products before identifying
permutations of equal-formal-codegree rows. For a nonabelian-codegree
certificate it separately checks that the indicated degree-three or
degree-four factor fails to split in the field of one root. It imports no
production routines. Character-orbit and low-part counts are configuration
counts, not disjoint counts of fusion rings.

The fourth audit checks the two Laurent polynomials and the integer indicator
combination used by the fourth-indicator corollary. It checks R2's formal
codegrees, the low-weight bound `7+30*delta`, floor 16 and positive gap 44 in
the Section 3 example. It also replays every recorded R2 fourth witness using
explicit characters and full low-row boxes. Extra related-family identities
are consistency checks; individual certificates already exclude the relevant
census members. This audit also imports no production routines.

The model audit reconstructs the fifteen reference fusion rings separately
and checks explicit fusion-ring isomorphisms with the survivors. The cited
mathematical constructions, rather than this comparison, give existence of
the fusion categories.

The optional `--deep` runner additionally performs `unpruned_census_audit.py`,
`census/audit_small.py` and `census/audit_boundaries.py`. The principal guide
states which utilities these checks share with production. None of these
programs formalizes the categorical theorems or reconstructs associators.
