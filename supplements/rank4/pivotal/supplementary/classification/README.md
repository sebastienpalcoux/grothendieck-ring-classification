# Classification software

The principal guide is `../README.md`. This directory contains the producer,
certificate replay, reference model fusion data and exact arithmetic routines.
The certificate schema is 5.

| Stage | Excluded | Remaining |
| --- | ---: | ---: |
| Rank-two fusion subrings | 1,676 | 7,301 |
| Formal-codegree d-number condition | 6,541 | 760 |
| Spherical-character arithmetic | 595 | 165 |
| Published rank-four families | 90 | 75 |
| Central induction | 60 | 15 |

All 8,962 exclusions have computational certificates. The central stage uses
the second-, third- and fourth-indicator corollaries and the involution
proposition in Section 3. The S(2) and R2 examples there illustrate two of
these exclusions by hand.

Run from the package root:

```sh
python3 supplementary/classification/classify.py --workers 4
python3 supplementary/classification/verify.py --workers 4
```

`supplementary/stages.py` freshly recomputes and exactly verifies any selected
prefix: `rank-two`, `d-number`, `spherical`, `families`, `central`, then `models`.
The final command also replays all fifteen model certificates:

```sh
python3 supplementary/stages.py models --workers 4
```

The arithmetic stage checks every character orbit. Its cyclotomicity test
uses exact Galois groups of degree-three or degree-four irreducible Casimir
factors. The independent audit instead tests splitting in a root field.
Formal-codegree field containment and the earlier prime-ideal witness search
are not used. An unresolved calculation or null local witness never
constitutes an exclusion. Replay checks the stated witness rather than
requiring the producer's first discoverable witness.

Use `supplementary/check.py` for the full sequence, regressions and separate
audits. SymPy is required; `python-flint` acceleration is optional.
