# Dependency review of the withdrawn R24 exclusion

Date: 17 October 2026. This is an AI review, not human verification or formal proof.

**No other accepted classification decision was found to depend on the withdrawn general R24 exclusion or its unsupported six-slot diagonal-phase reduction.** The required correction is to R8_2_24 and aggregate completeness/count statements. The scope and checks supporting that conclusion are below.

## Ledger and reference checks

All 30,595 rank-six, rank-seven and rank-eight ledger records were scanned for the R24 ID, criterion, proof/verifier paths, and theorem labels. Only R8_2_24 referenced `projective_inner_square_obstruction`, `R24_PROJECTIVE_INNER_SQUARE_PROOF.md`, or `verify_r24_projective_inner_square.py`.

The manuscript, evidence proof notes, and verifier sources were searched for these names, `lem:2d2-no-inner-square`, `thm:r24-inner-square`, the decorated-phase language, and the particular diagonal-slot identities. Matches outside the R24 proof/audit bundle were classification summaries, historical registers, scoped R24 discussion, or the independent indicator lemma supplying premises to R24. No reverse dependency on the withdrawn conclusion was found.

This is a bounded textual and mathematical dependency check, not a machine-verified dependency graph. It does not independently validate every accepted theorem.

## Related arguments inspected substantively

| Argument | Dependency direction and conclusion |
|---|---|
| Character-weighted saturated indicator lemma | `SATURATED_CHARACTER_INDICATORS.md` proves its signed Galois identity independently, then supplies second-indicator signs and ordinary cubic rotations to R24. It explicitly does not establish R24 or assume its coefficient bridge. Withdrawing R24 does not withdraw that premise lemma. |
| Four general 2D2 exclusions, R152/R153/R166/R495 | `FOUR_2D2_GENERAL_PROOF.md` and the corresponding manuscript section use the particular module graph, module traces, an algebraic graph-planar-algebra embedding, and separate polynomial ideals. They do not use the R24 projective-square theorem or six-slot D matrix. |
| R7_4_2053 and R8_1_18 | The Morita endpoint is R18 and its independent STS-moment obstruction. The frozen root audit explicitly separates that conclusion from R24. |
| Earlier scoped R24 obstruction | The known unitary 2D2 category's tensor-auto-equivalence group and the odd invertible square yield a unitary obstruction, also covering the stated Galois-conjugate scope. This does not use the new general coefficient-frame lemma. The manuscript's later sentences claiming that R24's general theorem removes this scope must be corrected. |
| Earlier `verify_scoped.py` application | This checks the source neutral subring/grading and records a unitary scope. It neither applies the later general R24 theorem to another case nor changes a general ledger decision. |

## Presentation consequences

The current classification must list R8_2_24 as generally unresolved, retain the earlier scoped result separately, and remove the resulting claim of full rank-eight categorification classification through multiplicity two. Historical October 16 proof/audit bundles remain historical evidence and need a visible superseding notice; their old PASS labels are not a justification for keeping the withdrawn decision.

The initially observed manuscript references requiring correction were `rank8.tex`'s opening and concluding completeness statements, the inclusion of `r24_inner_square.tex`, and the general-upgrade sentences in `scoped_obstructions.tex`. These are presentation consequences, not additional dependent classification decisions.
