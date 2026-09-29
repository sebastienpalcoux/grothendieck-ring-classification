"""Generate fourth-continuation release prose from its accepted ledger."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def main():
 summary=json.load(open(ROOT/'verification/release_summary.json'))
 records=[json.loads(s) for s in (ROOT/'certificates/continuation_round4.jsonl').read_text().splitlines()]
 n=len(records);ex=summary['excluded'];op=summary['unresolved']
 bands=', '.join(str(r['multiplicity']) for r in summary['counts'] if not r['unresolved'])
 lines=['| Exact multiplicity | Rings | Excluded | Models | Unresolved |','|---:|---:|---:|---:|---:|']
 for r in summary['counts']:
  v=[r['multiplicity'],r['classes'],r['excluded'],r['unitarily_realized']+r['spherically_realized_nonpseudounitary'],r['unresolved']]
  lines.append('| '+' | '.join(f'{x:,}' for x in v)+' |')
 lines.append(f'| **Total** | **16,612** | **{ex:,}** | **54** | **{op}** |')
 table='\n'.join(lines)
 common=f'''This continuation adds **{n} general exclusions**, reducing the ten-case
frontier to **{op} unresolved rings**. There are **{ex:,} general exclusions
and 54 realized rings** among the 16,612 census tensors. General
categorifiability remains completely classified through multiplicity three;
the exact multiplicity bands **{bands}** are complete. The census, identifiers
and positive-model identifications are unchanged.
'''
 progress='''A central object's projection onto a fusion subcategory retains its
twist. This gives necessary restrictions on individual induction columns
and exact twist-resolved dimension masses. Fibonacci, Ising, cyclic-three
and half-E6 subcategories give distinct refinements. Exact cyclotomic
subfield traces make larger conductors accessible without dropping the
character equations. Every accepted pseudo-unitary obstruction is combined
with its verified general reduction.

At multiplicity four, exhaustive Gram and Galois enumeration reduces
`R6_4_22` to three restriction profiles per character labelling, then
to two after word-multiplicity tests, and
`R6_4_91` to six, then to two by exact twist-system congruences
(center ranks 36 and 42). The corresponding reduction for `R6_4_629`
leaves five profiles, then three (ranks 30, 35 and 38) after exact
fixed-profile twist tests. These are finite necessary alternatives, not center fusion rings
or categorical models. For `R6_4_155`, fourth spectral moments,
integer-square inequalities and central-invertible transport yield a much
stronger exact surviving integral witness. None of these surviving systems
is counted as a categorification.

The new criteria are screened on all ten frozen residuals and all 54 known
positive rings. Eligibility, exact witnesses, numerical feasibility and
unfinished searches are recorded separately in the coverage report.
'''
 readme=f'''# Rank-six categorification through multiplicity eight

{common}
[Revised paper](papers/manuscript.pdf) ·
[Verification guide](papers/verification_guide.pdf) ·
[Decision ledger](data/decisions.csv) ·
[Model catalogue](data/model_catalog.csv)

{table}

The 54 realized rings have 53 unitary models and one spherical model with no
pseudo-unitary categorification. Through multiplicity three, 531 of 577
rings are excluded and 46 have spherical models, including 45 unitary models.
All exclusions in the table apply to complex fusion categories without an
assumed pivotal, spherical or unitary structure.

## Fourth continuation

{progress}
[Revision notes](REVISION_NOTES.md) list the accepted proofs and their scope.
The input tensors are frozen in
[`verification/round4/campaign_manifest.json`](verification/round4/campaign_manifest.json).
See the [criterion coverage](research/round4/coverage.json) and
[research guide](research/round4/README.md) for the remaining cases.

## Reproduce and inspect

Use the pinned Python requirements and a C++17 compiler. Rebuilding the
papers also requires `pdflatex`. Check integrity before generating reports:

```bash
python -m pip install -r requirements.txt
python check_manifest.py
python -O software/round4_release.py --jobs 3
python software/model_catalog.py
python software/build_paper_tables.py
python software/round4_documents.py
python research/round4/coverage.py --require-canonical --output research/round4/coverage.json
python software/release_consistency.py
python -O software/release_consistency.py
python build_papers.py
```

The fourth-continuation checker disables numerical optimizers and
reconstructs each new accepted proof. Earlier source-bound evidence is
retained. To replay every continuation, run
`python -O software/continuation_controls.py --jobs 3 --out verification/current/all_continuations.json`.
To replay the complete negative catalogue, run
`python -O verify.py --jobs 2 --out verification/current/full_recheck.jsonl`.
These larger optional replays are not claimed to have been repeated here.

`data/decisions.json` is authoritative. CSV files, paper tables, counts and
`data/unresolved_tensors.json` are derived from it. General, pivotal,
spherical, pseudo-unitary and unitary existence are recorded separately.
The new allocation is `certificates/continuation_round4.jsonl`; all earlier
accepted certificate files remain unchanged. Historical reports retain
their original inputs and do not define current classification status.

The census is inherited from the pinned
[Fusion Ring Census](https://github.com/sebastienpalcoux/fusion-ring-census/tree/b86eb6dc6eeeafe5fc5f6906d7b074e0322e9726).
Its source is bundled for offline replay. The [OEIS directory](oeis/README.md)
is a local counting proposal, not an online submission. No claim beyond
multiplicity eight is made.
'''
 (ROOT/'README.md').write_text(readme)
 names={'general_fibonacci_subfield_rotation':'Fibonacci center projection and cyclotomic subfield traces',
        'general_ising_projection_rotation':'Ising center projection and twist-resolved masses',
        'general_cyclic_three_projection':'Cyclic-three associator and center projection',
        'general_half_e6_projection':'Half-E6 center projection and twist-resolved masses'}
 proofs=['| Tensor | General obstruction | Exact proof source |','|---|---|---|']
 for r in records:proofs.append(f"| `{r['id']}` | {names.get(r['certificate']['kind'],r['certificate']['kind'])} | [`{r['source']}`]({r['source']}) |")
 notes=f'''# Revision notes — fourth continuation, 29 September 2026

{common}
{table}

## Accepted general exclusions

{chr(10).join(proofs)}

The canonical disjoint allocation is `certificates/continuation_round4.jsonl`.
The three preceding continuations retain their 7, 18 and 12 exclusions.
Alternative proofs are retained without double counting.

## Mathematical progress

{progress}
The manuscript proves twist-preserving subcategory projection and the
Fourier formula for twist-resolved masses. The new chapters also justify
complex low Verlinde products with duality, fourth spectral moments,
integral square cuts, finite restriction-profile enumeration and the
odd-conductor Galois-orbit divisibility criterion. The latter uses the
squared Galois action and is not asserted at even conductors.

Known-model searches remain separate from existence claims. All 61
constructors for the 54 known rings and 293 relative-center dimension
comparisons have been checked. Three tempting ADE or quantum-group Morita
models are ruled out by exact central-dimension mismatch. A mismatch with
these specific models is not a general nonexistence theorem.

## Verification and complete revision

`verification/round4/release_replay.json` records exact reconstruction of
every accepted new proof with optimized Python and numerical optimizers
disabled. The criterion directories retain independent audits, exact
surviving witnesses and controls. `research/round4/coverage.json` states the
actual scan domains and unfinished searches; they remove no rings.

The authoritative ledger, CSV exports, residual tensors, counts, paper
tables, manuscript, verification guide and current documentation are
regenerated. `software/release_consistency.py` checks their agreement in
normal and optimized Python modes. PDF compilation and visual checks are
separate from mathematical verification. The archive manifest covers every
file except itself, and every ZIP member is checked against it.

Earlier negative campaigns and their exact evidence remain unchanged; this
release does not claim to repeat the entire inherited catalogue. Earlier
revision notes are preserved in `provenance/`, including
`REVISION_NOTES_third_continuation.md`. Use the current ledger for status.
'''
 (ROOT/'REVISION_NOTES.md').write_text(notes)
 p=ROOT/'verification/README.md';v=p.read_text()
 v=v.replace('The current frontier has 10 tensors; exact multiplicity seven is complete.', 'At the end of the third continuation, ten tensors remained; exact multiplicity seven was complete.')
 a=v.find('`round4/` freezes')
 if a>=0:
  b=v.index('`current/` contains',a);v=v[:a]+v[b:]
 insert=f"""`round4/` freezes the next ten full tensors and the sources of {n} further
general exclusions. `software/round4_release.py` reconstructs every new
proof with optimizers disabled and preserves the earlier campaigns.
Its source-bound replay yields {ex:,} exclusions, 54 realized rings and
{op} unresolved cases. Exact completed multiplicity bands are {bands}.
The new criterion scans and all 54 model controls are reconciled in
`research/round4/coverage.json`; eligibility and budgets are explicit.
Finite restriction profiles and surviving integer or rational systems
are necessary conditions, not categorical models.

"""
 v=v.replace('`current/` contains',insert+'`current/` contains')
 v=v.replace('The second and third accepted JSONL files are disjoint extensions','The second, third and fourth accepted JSONL files are disjoint extensions')
 p.write_text(v)
 print('Updated fourth-continuation prose:',n,'accepted exclusions;',op,'unresolved')

if __name__=='__main__':main()
