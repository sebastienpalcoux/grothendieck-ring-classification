"""Render the current release overview from its verified ledger exports."""
import json
from pathlib import Path

P = Path(__file__).resolve().parents[1]

def main():
    counts = json.loads((P/'data/classification_counts.json').read_text())
    report = json.loads((P/'verification/release_summary.json').read_text())
    frontier = json.loads((P/'data/frontier_research_progress.json').read_text())
    source = json.loads((P/'provenance/repository_source.json').read_text())
    total = sum(r['classes'] for r in counts)
    if total != 25421 or counts[-1]['multiplicity'] != 9:
        raise ValueError('Complete multiplicity-nine exports are required')
    if set(report['unresolved_ids']) != {r['id'] for r in frontier['cases']}:
        raise ValueError('Frontier and release summary disagree')
    summary = f"**{total:,} rings: {report['excluded']:,} excluded, {report['positive']} realized, {report['unresolved']} unresolved.**"
    rows = ['| Exact multiplicity | Rings | Excluded | Models | Unresolved |',
            '|---:|---:|---:|---:|---:|']
    for r in counts:
        positive = r['unitarily_realized'] + r['spherically_realized_nonpseudounitary']
        rows.append(f"| {r['multiplicity']} | {r['classes']:,} | {r['excluded']:,} | {positive} | {r['unresolved']} |")
    rows.append(f"| **Total** | **{total:,}** | **{report['excluded']:,}** | **{report['positive']}** | **{report['unresolved']}** |")
    groups = {}
    for case in frontier['cases']:
        groups.setdefault(case['public_summary'], []).append(case['id'])
    cases = '\n'.join('- '+', '.join(f'`{rid}`' for rid in ids)+': '+description
                      for description, ids in groups.items())
    last = counts[-1]
    bands = ', '.join(str(r['multiplicity']) for r in counts if not r['unresolved'])
    text = f'''# Rank-six categorification through multiplicity nine

{summary}

[Manuscript](papers/manuscript.pdf) · [Verification guide](papers/verification_guide.pdf) · [Decision ledger](data/decisions.csv) · [Models](data/model_catalog.csv)

{chr(10).join(rows)}

The models comprise 56 unitary realizations and one spherical realization whose ring has no pseudo-unitary categorification. Every allocated exclusion applies to general complex fusion categories. The completed exact-multiplicity bands are {bands}.

All 8,809 rings of exact multiplicity nine are excluded for general complex fusion categories. The [completion proofs](research/exclusions/m9_completion/README.md) resolve the final eleven cases with standalone exact verifiers and frozen tensor inputs. All 16,612 earlier representatives, identifiers and decisions are preserved. The [new campaign](verification/m9/) records the actual criterion order, discovery budgets and independent exact certificate replays. Timeouts and surviving necessary systems establish neither exclusion nor existence.

## Remaining rings

{cases}

The [frontier index](research/frontier/README.md) gives the current evidence and distinguishes it from frozen historical stages. The [model catalogue](data/model_catalog.csv) identifies actual categorical constructions and all 216 tensor coefficients, including the three conformal-embedding models.

## Verification

```bash
python -m pip install -r requirements.txt
python check_manifest.py
python -O software/replay_m9.py --jobs 2
python -O software/replay_m9_structure.py
python -O software/replay_m9_completion.py
python -O software/m9_completion_controls.py
python -O software/conformal_models.py --verify
python -O software/release_consistency.py
python -O software/frontier_replay.py --check-receipts
python research/frontier/new_research/replay.py
```

The new certificate replay disables numerical optimizers. Historical proofs retain their original exact verification evidence; a receipt audit checks source hashes and predicates and does not rerun the mathematics. For a fresh full-ledger check, use `python -O verify.py --jobs 2 --out verification/current/full_recheck.jsonl`. The verification guide distinguishes these scopes and gives the remaining replay commands.

`data/decisions.json` is authoritative. Regenerate exports with `python software/release.py`, `python software/model_catalog.py`, `python software/build_paper_tables.py`, `python software/build_readme.py` and `python build_papers.py`. Release generation replays historical continuation certificates by default; `--retain-historical-replay` instead checks their frozen source-bound receipt.

The census is pinned to [Fusion Ring Census revision {source['published_data_commit']}](https://github.com/sebastienpalcoux/fusion-ring-census/tree/{source['published_data_commit']}). Enumeration completeness comes from that source; the import independently checks tensor validity, distinctness and exact correspondence. The [OEIS proposal](oeis/proposal.txt) counts all fusion rings, independently of categorifiability.
'''
    (P/'README.md').write_text(text)
    (P/'REVISION_NOTES.md').write_text(f'''# Current release: multiplicity nine

{summary}

All 8,809 exact-multiplicity-nine tensors are excluded generally. The final eleven exclusions are supplied by the separately replayed completion campaign; the two remaining open rings have multiplicities four and eight. Earlier decisions and mathematical certificates are preserved. The frontier research now determines a complete rank-26 modular candidate for R6_4_155 and reduces R6_8_1660 to three possible Morita-dual rings and 1669 labelled center profiles. Both rings remain unresolved. New certificates have independent exact replays; historical replay receipts remain explicitly historical.

The manuscript, ledger, proof allocation, frontier, source provenance and OEIS draft use this same census. Current evidence and required dependencies are retained; obsolete exploratory outputs are omitted.
''')
    print('Rendered README.md and REVISION_NOTES.md')

if __name__ == '__main__':
    main()
