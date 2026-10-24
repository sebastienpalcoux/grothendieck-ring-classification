# Cross-cutting finding: unsupported general-scope promotion for R8_3_436

Repository: `sebastienpalcoux/grothendieck-ring-classification`, commit `8f1a0b8184eb8d7bb44a666afd78552e33c02f42`.
Audit date: 24 October 2026 (UTC).

## Finding CC-01

**High priority: the current proof does not establish the recorded general-complex exclusion of `R8_3_436`.** Its crucial external input is stronger than the theorem supplied by the explicitly cited version of the near-group TPE paper. The existing unitary exclusion remains supported. This finding is a proof-scope gap; it is **not** a counterexample to the proposed noncategorifiability conclusion.

The missing claim is that **every** spherical `C3+3` category, after the stated dimension and indicator reductions, is gauge equivalent to a category with the displayed scalar tetrahedral table. Solving all scalar equations and reconstructing unitary categories from their solutions does not establish this claim about an arbitrary original category.

## Exact repository dependency

- `manuscripts/rank8/paper/m3_frontier.tex:124–125` asserts that every complex `C3+3` near-group category has a unitary Galois conjugate, and derives general noncategorifiability of `R8_3_436`.
- `m3_frontier.tex:132–133` invokes a complete spherical tetrahedral parameterization from Theorem 2.3, Proposition 2.7 and Theorem 4.12 of the TPE reference.
- `m3_frontier.tex:154–157` applies Corollary 5.5 to the original category's purported complete table. It correctly recognizes that an existence-only reconstruction cannot justify that inference.
- `manuscripts/rank8/paper/rank8.tex:592` explicitly pins that reference to **arXiv:2610.11652v1**.
- `evidence/rank8_frontier_20261021/structural_models/R436_GENERAL_TPE.md:57–63,124–131` repeats this same complete-table assertion, without independently proving the required nonunitary gauge-normalization theorem.
- `evidence/rank8_frontier_20261021/review/REVIEW.md:19–25` acknowledges that existence equivalence is insufficient, then accepts the stronger statement by citing the introductory setup and Theorem 4.12. It does not address Section 4's explicit unitary hypothesis.
- `evidence/rank8_frontier_20261021/structural_models/r436_general_tpe.py:145–152` records complete spherical parameterization as an external literature hypothesis. Its code does not prove it.

## What the pinned primary source supplies

Source: He–Liu–Lu–Palcoux–Ren, *Triangular prism equations for near-group categories: algebraic solutions and a unitary conjecture*, [arXiv:2610.11652v1](https://arxiv.org/pdf/2610.11652v1).

Theorem 2.3 (printed p.4) states existence equivalence. Proposition 2.7 simplifies the scalar system. Section 4 (printed p.15) explicitly says: **“Until the final subsection, C is a unitary near-group category”**. Theorem 4.12 (p.23) gives its normalized tetrahedral table within that scope. Section 4.7 (pp.25–27) starts with numerical scalar data and proves algebraic transport identities; it does not derive that table from an arbitrary spherical category. Theorem 5.4 (p.34) and Corollary 5.5 (p.35) reconstruct spherical and unitary categories from the data.

Section 3 begins with spherical categories, but the later, explicit restriction at Section 4 controls the derivation. Its final subsection removes Hermitian assumptions from the prescribed table's identities, which is different from proving completeness of that table for all spherical categories.

Primary-source files saved for review:

- `audit/crosscutting/2610.11652v1.pdf`
- `audit/crosscutting/2610.11652v1.txt` (layout-preserving text extraction)
- PDF SHA-256: `dacabea170e0b9ecb117807c13dca836915b9d4b7ffe0bd4be6f2fdd88c8fca0`

Useful local text lines: Theorem 2.3 at 224; Section 4 scope at 926–929; Theorem 4.12 at 1422; Section 4.7 at 1556–1668; Theorem 5.4 at 2160; Corollary 5.5 at 2169.

## Why the finite replay does not close the gap

I freshly ran:

```bash
python evidence/rank8_frontier_20261021/structural_models/r436_general_tpe.py
```

It passes. The source tensor match checks all 512 coefficients. The scalar calculation exhausts the nine cubic equations, both dimension roots, both bicharacters and the remaining scalar branches, and verifies the positive-root Hermitian relations exactly. These calculations support the conclusion for categories already known to be described by that scalar table.

The computation has no variables describing an arbitrary category's full associators and no gauge-equivalence construction from such associators to the scalar table. It therefore cannot establish the missing categorical completeness premise. The script's opening documentation and the Markdown proof's final paragraph correctly identify categorical theorems as external dependencies.

## Search for an independent repair

I read the manuscript proof, its separate `.tex` version, the full `R436_GENERAL_TPE.md`, its checker and certificate, the frontier review, the accepted decision and the current ledger entry. They all use the same TPE premise. No independent spherical gauge-completeness argument was found in those materials.

The older `evidence/rank8_m3_20261021/models/r436_inversion_attempt.json` explicitly records only `unitary_only`, with `general_complex_excluded: false`. It identifies the scope limitation of Izumi's C*-classification and says the Grossman–Jordan–Snyder input concerns known Izumi–Xu categories, rather than all complex near-group categories. Those older references do not automatically repair the promotion. The separate rank-seven/eight reviewer independently confirmed the new source-scope mismatch and checked for an older general classification.

A repair may be mathematically possible by adapting the normalization and representation arguments to bilinear spherical data. However, that adaptation has to prove the necessary statement for the **given** category, without assuming a Hermitian structure. Merely restating Theorem 2.3 or rerunning the scalar calculation is not a repair.

## Correct interim scope and ledger implications

The tensor forces an inversion autoequivalence of its neutral `C3+3` category. The established unitary classification and automorphism obstruction exclude this for a unitary category. More generally, the argument excludes a categorification whose neutral category is known to become unitary under Galois conjugation. The unsupported step is asserting that every complex categorification has this property.

The current accepted entry is `evidence/rank8_frontier_20261021/accepted.json:9–18`. The current consolidated entry is `supplements/rank8/output/exclusion_20261022/ledger.json`, array index 1408 (`id` at line 87063). Its sole general criterion is `near_group_C3_TPE_Galois_unitarity`; it separately retains the old unitary exclusion.

Until the missing theorem is supplied or an independent general exclusion is established, a conservative correction would return this entry to unresolved for general existence while retaining `unitary_status: excluded`. **If this were the only correction**, the counts would become:

| Scope | Current recorded counts | Provisional counts after this one correction |
|---|---:|---:|
| Rank 8, exact multiplicity 3 | 3,507 excluded; 16 realized; 4 unresolved | 3,506 excluded; 16 realized; 5 unresolved |
| Rank 8, through multiplicity 3 | 4,403 excluded; 93 realized; 4 unresolved | 4,402 excluded; 93 realized; 5 unresolved |
| Current rank 2–11 atlas open-case total | 7 | 8 |

These are conditional accounting implications, not a claim that the true mathematical answer has changed. Relevant outputs include `README.md:25`, `docs/PROVENANCE.md:51`, `docs/PROJECT_GUIDE.md:126`, `site/dist/data/rank8_m3_update.json`, the unresolved-case directory/tensor downloads, and derived website scope records. They should be regenerated from a corrected ledger rather than edited individually.

## Additional cross-cutting checks

The earlier rank-five nonvanishing wording issue is also present in `classification/manuscripts/rank5/papers/census.tex:23–38`, not only the census repository. Its proof requires each dimension-character value to be nonzero; categorical simple-object dimensions provide that condition, but an arbitrary nonzero unital character does not. No noncommutative signed based-ring counterexample was constructed, so this remains a hypothesis-clarity issue rather than a refuted theorem.

The sampled integral-to-pseudo-unitary reductions correctly use weak integrality. In particular, rank-six `chapters/03.tex` explicitly invokes that theorem, and rank-eight `m3_positivity.tex` uses weak group-theoreticity for the stronger unitarity conclusion. I found no additional unsupported inference that arbitrary integral fusion categories are unitary. The TPE gap above is the consequential new result of this pass.
