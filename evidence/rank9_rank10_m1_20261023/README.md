# Rank-nine and rank-ten multiplicity-one classification

Research edition, 23 October 2026. AI-generated research; independent human verification and proof-assistant formalization remain pending.

| Rank | Inputs | Excluded over C | Unitary models | Unresolved |
|---|---:|---:|---:|---:|
| 9 | 142 | 102 | 40 | 0 |
| 10 | 194 | 131 | 57 | 6 |

Start with the [mathematical report](deliverable/report.pdf). The [complete CSV ledger](deliverable/ledger.csv) and [JSON ledger](deliverable/ledger.json) assign all 336 supplied input tables, with exact proof, certificate, and verifier paths. A unitary model is an existence result, not a classification of all associators. Unresolved entries carry no existence or nonexistence claim.

## Verify on Ubuntu

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python verify.py
```

The replay checks the release hashes, reconstructs the input audit, replays all accepted certificate families, and regenerates the entire ledger. It runs in a temporary copy so that the distributed evidence stays immutable. It writes `verification_report.json` and `verification_logs/`. Run without Python `-O`. No network is needed after installing the three Python dependencies. Use `python3 verify.py --manifest-only` for the file-integrity check alone.

## Read the evidence

| Material | Location |
|---|---|
| Main report and full source | `deliverable/report.pdf`, `deliverable/report.tex` |
| Original compressed tables and exact axiom audit | `inputs/`, `work/input_audit/` |
| Standard obstructions and signed reduction | `work/obstructions/`, `work/audit_signed/` |
| Established model audit | `work/audit_models/` |
| New family proofs and explicit data | `work/resolve_*/` |
| Independent construction and obstruction replays | `work/audit_new_models/` |
| Scope, primary references, census crosswalk | `work/literature/notes.md`, `work/literature/crosswalk.json` |

The six rank-ten cases `R10_1_114`, `R10_1_115`, `R10_1_152`, `R10_1_153`, `R10_1_179`, and `R10_1_189` are deferred to a later research phase. Experimental searches for these cases are not accepted evidence and are omitted from this release.

## Input identity and provenance

Identifiers use the original physical line number and the original zero-based tensor basis; the tensor unit is index 0. `tensor_sha256_compact_json` hashes compact JSON, whereas `tensor_sha256_uint8_flattened` hashes the flattened unsigned-byte tensor. The two encodings are intentionally distinct. The input audit verifies all fusion-ring axioms and pairwise based nonisomorphism. The crosswalk checks the supplied census against the AnyonWiki multiplicity-one database snapshot. This does not rerun the original census enumeration.

The exact replays verify finite calculations in the proofs. They do not replace the cited category-theoretic theorems or constitute formal verification of all mathematics. In particular, a surviving necessary-condition system is never used as a model, and an unsuccessful bounded search is never used as an exclusion.

To rebuild the PDF from the package root, run `cd deliverable` and then `latexmk -pdf report.tex`. The package keeps all relative proof paths intact.
