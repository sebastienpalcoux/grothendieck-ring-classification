# Integral rank-nine frontier: four cases remain open in general

The four integral residual rings have received a fresh theoretical and
exact investigation. **None is newly excluded in general, and no new model
is established.** The new results restrict which categorifications could
exist; they must not be counted as general exclusions.

| Ring | FP dimension | Braided categorification | Group-theoretical categorification | General/unitary existence |
|---|---:|---|---|---|
| R9_2_12 | 120 | Excluded by the new central-S3 argument | Excluded by the complete relative-cocycle reduction | Unresolved |
| R9_2_941 | 504 | Excluded by simplicity and square-divisibility | Even weakly group-theoretical categorifications excluded | Unresolved |
| R9_2_959 | 120 | Excluded by the new central-S3 argument | Excluded by the invertible group after the complete profile reduction | Unresolved |
| R9_2_1965 | 168 | Already excluded by noncommutativity | Excluded by the complete profile and relative-cocycle reduction | Unresolved |

The new group-theoretical claims passed a separate independent audit,
recorded in `phase4/audit_integral_gt/AUDIT.md` and `audit_verdict.json`.
The exact replay checks also pass. Their scope remains group-theoretical.
Weak integrality gives the canonical pseudo-unitary
structure to any hypothetical categorification of all four rings; it does
not turn the exclusions of particular constructions into general exclusions.

## What was established

`BRAIDED_SCOPE_THEOREMS.md` proves a unified obstruction: a category of
type `(1^4,2^2,6^3)` cannot contain a central Tannakian Rep(S3). A putative
equivariantization would descend to dimension twenty with one of just
three dimension/orbit patterns, all impossible. The exact subring and
fixed-point data of R9_2_12 and R9_2_959 force this contradiction under
the additional hypothesis of a braiding. The Müger-center argument
explicitly handles the possible super-Tannakian issue.

`GROUP_THEORETICAL_OBSTRUCTIONS.md` treats every group-theoretical
presentation, including arbitrary associators and subgroup cochains. A
projective-character reduction examines all 47 groups of order 120 and
57 groups of order 168, together with all 3,182 subgroup conjugacy classes.
Only two presentations at each dimension survive. Exact cohomological
transfer and relative-cochain calculations finish the dimension-120
cases. The dimension-168 argument combines the new exhaustive reduction
with the previous fully checked PSL(2,7)/S4 relative-cocycle theorem.
The surviving dimension-120 rank-nine tensor is the already modeled
R9_2_92; it is not R9_2_12 or R9_2_959.

R9_2_941 is exactly the exotic simple dimension-504 ring explicitly left
open in Alekseyev--Bruns--Dong--Palcoux, arXiv:2507.07023v2, Sections 1.5
and 7.5. Its simplicity excludes braided categorification: a symmetric
realization would be a finite-group representation ring, while a modular
realization would require `49 | 504`. ENO Proposition 9.11 excludes
weakly group-theoretical realizations. A general realization would
therefore lie outside that entire class; the cited paper does not provide
one or prove that none exists.

## Exact replay and its limits

From any working directory, run these scripts by their paths in the
research archive:

```
python phase4/integral/verify_scope_refinements.py
python phase4/integral/verify_GT_records.py
```

The first verifies original-tensor hypotheses, all fusion subrings used
in the braided proofs, the published 504-tensor identification, and the
equivariant orbit bookkeeping. It uses the archive's existing common
utilities and NumPy. The second uses **only the Python standard library**
and the current research archive: the original compressed input, the
stored local receipts, and `phase2/group_models/matches.json`. It needs
no Git repository checkout, GAP installation, NumPy, or SymPy. Both must
be run without Python's `-O` flag.

The stored-record replay checks tensor identities and the complete listed
outcomes. It does not rerun the finite-group enumeration or replace the
categorical proofs. For a fresh regeneration, the optional GAP scripts
`all_twist_skeleton.g` and `a5c2_data.g`, and Python generator
`s5_transfer_search.py` (also run with `--a5c2`), are supplied. Their
coverage arguments and dependency boundaries are stated in the proof.

Outputs are `scope_refinements.json` and `GT_verification.json`, with
explicitly unchanged general status. No online repositories or website
files were edited by this integral-case investigation.
