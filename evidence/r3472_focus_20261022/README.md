# Focused R8_3_3472 continuation — 22 October 2026

**General complex categorification remains unresolved.** No associator,
categorification, or general noncategorification theorem is supplied here.
The rank-eight totals remain 3,506 exclusions, 16 unitary models and five
unresolved cases at exact multiplicity three (4,402 / 93 / 5 cumulatively).

## Results and scope

| Result | Scope | Evidence |
| --- | --- | --- |
| Every simple dimension of every Morita partner lies in Z[sqrt(2)] with nonnegative coefficients; its integral subcategory is pointed of order 1 or 7 | Every complex categorification, without a pivotality or module-lift assumption | `morita/manuscript.tex`, `morita/verify.py` |
| Order 7 forces profile 1^7,(7+5sqrt(2))^7 and exactly two candidate based rings | Necessary Morita data; neither candidate is constructed as a category | `constructions/constructions.tex`, the two tensor JSON files |
| Direct ordinary quotients of Radchenko–Wheeler matrix parents cannot yield the target dimension, even with arbitrary pointed tensor factors | All such matrix inputs; not all near-group categorifications or arbitrary Morita constructions | `constructions/CONSTRUCTIONS.md`, `constructions/verify_constructions.py` |
| The hypothetical center is simple and every nonunit central simple has irrational FP dimension | Uses the previously certified source sphericalization and Galois reduction | `center/center.tex`, `center/verify_structure.py` |
| Every nonunit simple has third indicator 2 and identity trivalent rotation | The pseudo-unitary Galois form | `independent/THIRD_INDICATORS.md`, `independent/verify_third_indicators.py` |
| The 3,347-equation / 13,242-variable center relaxation has an exact nonnegative integer witness | Integer feasibility of this relaxation only; neither complete modular data nor categorical existence | `center/rational_witness.py`, `center/integer_witness.json` |

The first conditional rank-two Morita branch now has four surviving dimension
spectra, reduced from seven. The second branch now has 272,349 surviving arithmetic dimension multisets
under these filters: 272,348 with one invertible and the unique seven-invertible
profile. This reduces the preceding count of 400,477 by eliminating all order-2
and order-5 profiles, without assuming either rank-two based module lifts.

The existing height-four phase witness already satisfies the maximal third
indicators. The integer center witness now has a compatible rational extension satisfying
all indicator and rotation moments through order four: 80 exact equations,
391 variables, and 40 positive entries. The verifier reconstructs the complete
37-type relative-trace domain with no categorical twist-order cutoff. This
extension does not impose complete complex STS equations or actual twist
assignments. Neither an associator nor a category is constructed.

`independent/verify_phase_extension.py` and `independent/phase_certificate.json`
check this linked relaxation against the source-verified restriction labels
of the integer center witness.

## Reproducibility repair

The preceding release omitted `r3472/second_branch_count.py`. The reconstructed
helper reproduces all four arithmetic counts exactly. The three original
mathematical scripts are unchanged. Only cache-state diagnostics in the old
receipt change. Original source bindings and receipts are preserved under
`reproducibility/`, with an independent generating-function recount and
normal/optimized replay. No failed assertion was removed or weakened.

## Replay and review

From the repository root, the current accepted-stage replay includes this
continuation:

```sh
python tools/verify_rank8_creative_20261022.py
python -O tools/verify_rank8_creative_20261022.py
```

The coordinator keeps all mathematical child assertions enabled in both
lanes. Individual scripts under this directory also provide exact local
checks. Review notes are in `review/`; they record independent agent checks,
not human peer review or formal proof verification. Primary mathematical
sources and precise theorem hypotheses are cited in the manuscript fragments.
