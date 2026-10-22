# R8_3_1768: saturated prime-sector and Galois restrictions

**Status: unresolved.** The new theory determines the entire irrational-ratio
sector outside the two distinguished objects up to two possible size patterns.
All these objects have primitive-37 twists. It also determines the restriction
of the distinguished Galois image of the unit. The resulting necessary cone
still has an exact rational solution.

The proof is [GALOIS_FIBRES.md](GALOIS_FIBRES.md). It uses the saturated-conductor
and signed-prime theorems in `../unified/`, plus the frozen general-to-spherical,
pseudo-unitary Galois, and nontrivial pointed-associator results.

The accepted replay is read-only:

```sh
python evidence/rank8_creative_20261022/r1768/verify.py
python -O evidence/rank8_creative_20261022/r1768/verify.py
```

It reconstructs the complete frozen atomic domain; checks the source character
arithmetic, complement involution, unique Galois-unit column and five complete
Gram branches; and verifies all forty indicator/Gram combinations exactly.
Thirty-nine have exact separating certificates. The remaining combination has
`V=4` and all six noninvertible second indicators positive. An exact rational
witness remains after forcing the unique Galois-unit restriction.

| Accepted file | Role |
| --- | --- |
| `verify.py`, `verify_all.py`, `verification.json` | Read-only entry point, shared replay, result receipt |
| `verify_arithmetic.py`, `arithmetic_verification.json` | Source and finite-domain arithmetic |
| `finite_fibres_cone.py`, `finite_fibres_cone.json` | All five Gram branches and forty indicator cases |
| `unit_orbit_cone.py`, `unit_orbit_cone.json` | Unique Galois-unit restriction and final surviving witness |
| `GALOIS_FIBRES.md` | Mathematical derivation and precise scope |

The remaining scripts and logs document discovery. In particular,
`integer_gram_probe.json` contains an exactly checked integral solution of a
weaker Gram and rational-character symmetry relaxation. It does not solve
modular data or pentagon equations and is not needed for the accepted replay.
Neither rational nor integral feasibility is a construction of a fusion
category.
