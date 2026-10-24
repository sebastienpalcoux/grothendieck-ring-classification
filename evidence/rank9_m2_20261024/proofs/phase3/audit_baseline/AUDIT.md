# Baseline audit: structural dependency error found and bounded

The baseline's substantive error is the omission of the known unitary rank3 half-E6 category from `lower_positive_registry.json`. The structural pass treated absence from that registry as an exclusion. This invalidates26 structural certificate claims:10 primary proofs and16 secondary proofs. The primary IDs are71,79,96,97,98,499,1218,1266,1489,2020. An invalid subring proof does not itself determine the ambient ring's categorifiability; the parent pass is reclassifying these records and removing all26 invalid claims.

The omitted ring is C2+2: g²=1, gx=x, x²=1+g+2x. Its categorical realization is classical and is explicitly present as R3_2_1 in the project's public realized-ring atlas and in `manuscripts/rank3.tex`. An exact comparison with every atlas realization of ranks2–8, multiplicities1–2 found no other missing lower positive ring. `invalid_half_E6_subrings.json`, `missing_lower_models.json`, and `all_invalid_registry_uses.json` record the full tensors and based bijections.

## All structural claims audited

There are588 structural uses,189 primary and399 secondary, involving108 exact subtensors. Primary rank counts are: rank3 14, rank4 8, rank5 24, rank6 61, rank7 80, rank8 2.

All454 rank6–8 uses have now been matched coefficient by coefficient to explicit lower-rank negative ledger entries:85 unique subtensors, all excluded, with no unresolved or realized matches. The lower decisions, their actual certificates, source tensor and exact transport bijections are in `structural_crosswalk.json`. Rank6 and rank7 ledgers and the rank6 source census were fetched from the existing public repository's compressed payloads; every payload-part SHA256 and uncompressed-file SHA256 was checked against `large_files_manifest.json`. Rank8 is bound by each decision's exact tensor hash rather than by assuming table order agrees with old IDs.

The original structural pass additionally stored166 direct d-number or near-group certificates (38 unique subtensors). Every such direct witness was replayed exactly by `scope_and_identity_audit.py`; no failure occurred. The near-group test explicitly enforces commutativity and 0<kappa<|G|−1, matching Schopieray Proposition3.2. Its pseudounitarity input is supplied by the two-FP-dimension theorem, so no structure assumption is silently added.

For rank3, the corrected five-ring list includes half-E6. All non-half-E6 rank3 structural subtensors are outside that complete list. Their scope is the project's unrestricted rank3 theorem and its five-ring corollary, not merely the older pivotal classification. The small-rank audit binds the exact subtensors to this statement. The remaining24 non-direct rank4/5 uses involve just three unique subtensors and have fresh direct certificates independently supplied and replayed by the parent in `phase3/audit_small_subrings/verification.json` (PASS: three subtensors,24 exact transfers). They are accepted on those proofs, not absence from a positive catalog.

## Weighted induction and scope checks

The three primary noncommutative weighted-induction exclusions are1375,1376,1798. For each, independent exact spectral reconstruction verifies the Wedderburn degrees1,1,1,1,1,2, formal codegrees obtained from the matrix-block Casimir eigenvalue divided by2, and the correct identities

dim(A_E)=D/f_E,  [I(1):A_E]=[F(A_E):1]=dim(E),
Σ_E dim(E)dim(A_E)=D.

The implementation's Gram matrix is the genuine induction matrix for Σ_b b X b*, not left multiplication by the Casimir in a noncommutative ring. Both its unit column and row are multiplicity weighted. The residual Gram contribution uses each distinct central simple once, as required. All three accepted exclusions have integral global FP dimension, hence their pseudo-unitary gate is valid. The ungated result1377 is retained only as a scoped obstruction in the baseline. The positive-coefficient interval inequalities are outward relaxations, so interval rounding cannot create a false exclusion.

For the other primary criterion families, the code review found their declared scope matched their enforced hypotheses: Casimir d-numbers allow the integer representation-degree scaling; integral Drinfeld tests use integral FP dimensions; cyclotomic tests require commutativity; indices are checked by exact algebraic integrality; low induction is promoted only under weak integrality or the two-FP-value theorem; module criteria impose the relevant commutative hypotheses; incomplete signed searches are not promoted. The parent is independently rerunning all baseline certificate solvers. This review is additional scope and dependency checking, not a replacement for those full replays.

## Original multiplicity-one crosswalk

All142 M1 records were compared directly with the separately supplied original M1 archive using the recorded unit-fixing basis transport. All103,518 multiplication-coefficient equalities pass and every old ID is retained. There are128 identity transports and14 nonidentity transports, all explicitly recorded and verified. Thus “IDs retained” is correct; a claim that every basis is literally unchanged would be too strong. `scope_and_identity_audit.json` records every hash and transport outcome.

## Prevention

A subring transfer should carry an exact lower census ID, full basis transport, negative decision scope and certificate dependency, or a direct certificate on the subring. Absence from a positive registry must never be the sufficient acceptance condition. Positive-registry completeness should also be checked against the complete realized atlas, including small-rank exceptional models.
