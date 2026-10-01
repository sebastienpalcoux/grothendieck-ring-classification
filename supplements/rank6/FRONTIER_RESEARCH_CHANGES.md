# Frontier research integration — 1 October 2026

The classification is unchanged: 25,421 rings, 25,362 general exclusions,
57 realized rings, and the two unresolved rings R6_4_155 and R6_8_1660.
All 8,809 exact-multiplicity-nine rings remain generally excluded.

## Mathematical additions

- R6_4_155: the complete unique necessary rank-26 semion-centralizer modular
  datum, exact integral nonnegative Verlinde coefficients (maximum 9), ten
  self-dual centralizer objects and twenty full-center objects; the stated
  finite full-data Vafa and indicator checks.
- R6_4_155: three possible connected-étale underlying objects, the obstruction
  to dimension-eight condensation from the three new order-32 near-group
  centers, and the canonical intermediate condensation analysis.
- R6_8_1660: uniform module rank six; full-center saturation and faithful
  Morita-dual action; exhaustive bounded integral Gram reduction and weighted
  second-indicator exclusion leaving three possible Morita-dual based rings.
- R6_8_1660: the signed Galois–fermion four-divisibility obstruction excludes
  raw profile 133 in low frame zero, reducing 1670 to 1669 profiles in branches
  163, 753, 753.

None of these necessary data constructs or excludes either original ring.
The three Morita-dual ring alternatives are a separate domain from the one
retained relative-center based ring.

## Editorial and integrity decisions

The existing restriction-profile, low-row, sphericality, twist and relative-
center foundations are retained. Four new manuscript source files give the
new proofs in full. Their equation labels are unique and use the manuscript's
section numbering. Earlier partial-data and duality statements in the
manuscript are explicitly stage-qualified and forward-referenced.

The current status source is `data/frontier_research_progress.json` and the
README generator consumes it. The current frontier index, indicator audit,
verification guide and per-ring `CURRENT_STATUS.md` pages state the new results.
The older `data/frontier_summary.json`, `research/frontier/coverage.json`,
source-bound per-ring `README.md` files and R155 `MODELS_IDENTIFICATION.md`
remain byte-for-byte historical-stage evidence. Current pages label them as
such and supersede their old partial-data descriptions. No historical adapter,
mathematical verifier, certificate, ledger or census entry is changed.

The allocation table uses a smaller font on a dedicated float page, correcting
an inherited oversized-float warning without changing any entry; the table
generator preserves this formatting when rebuilt.

## Verification scope

Both manuscript and verification guide compile with three LaTeX passes.
The new manuscript pages were visually inspected. The final build has no
LaTeX warnings, undefined references, duplicate labels or overfull boxes.
The frozen source package passes its 678-file manifest check. The retained
99-file frontier source audit, `frontier_m9.py --check-current`, and optimized
`release_consistency.py` all pass. Census and decision-ledger bytes are unchanged.

The separate new-research replay records each exact computation and its scope;
both ordinary and optimized twenty-job replays pass. The included integration
receipt and changed-file list are in `verification/current/`. The package
manifest binds the final included files.
No GitHub or website publication is performed by this integration step.
