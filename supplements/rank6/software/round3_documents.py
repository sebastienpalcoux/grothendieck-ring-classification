"""Regenerate current release prose from the accepted third-continuation ledger."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def main():
 counts=json.load(open(ROOT/'data/classification_counts.json'))
 summary=json.load(open(ROOT/'verification/release_summary.json'))
 records=[json.loads(s) for s in (ROOT/'certificates/continuation_round3.jsonl').read_text().splitlines()]
 new=len(records);excluded=summary['excluded'];unresolved=summary['unresolved']
 lines=['| Exact multiplicity | Rings | Excluded | Models | Unresolved |','|---:|---:|---:|---:|---:|']
 for r in counts:
  values=[r['multiplicity'],r['classes'],r['excluded'],r['unitarily_realized']+r['spherically_realized_nonpseudounitary'],r['unresolved']]
  lines.append('| '+' | '.join(f'{v:,}' for v in values)+' |')
 lines.append(f'| **Total** | **16,612** | **{excluded:,}** | **54** | **{unresolved}** |');table='\n'.join(lines)
 complete=[r['multiplicity'] for r in counts if not r['unresolved']]
 bands=', '.join(map(str,complete))
 intro=f'''# Rank-six categorification through multiplicity eight

**{new} further general exclusions reduce the unresolved frontier from 22 to {unresolved}.**
General categorifiability remains completely classified through multiplicity
three. The exact multiplicity bands now fully classified are **{bands}**.
The 16,612 census tensors, identifiers and 54 positive-model identifications
are unchanged.

[Revised paper](papers/manuscript.pdf) ·
[Verification guide](papers/verification_guide.pdf) ·
[Decision ledger](data/decisions.csv) ·
[Model catalogue](data/model_catalog.csv)

{table}

All exclusions counted here apply to complex fusion categories without an
assumed pivotal, spherical or unitary structure. The 54 realized rings have
53 unitary models and one spherical model with no pseudo-unitary
categorification. Through multiplicity three, 531 of 577 rings are excluded
and 46 have spherical models, including 45 with unitary models.

## The new continuation

The smallest previous multiplicity-four case, `R6_4_6`, is excluded by a
forced nontrivial cyclic associator and fourth-indicator support, combined
with Clifford stabilizer rotation. This also completes the uniform cyclic
order-four family throughout the census.

Further multiplicity-four exclusions use full-character cyclotomic traces,
Galois compatibility, and low Verlinde and restriction-product constraints.
An integer congruence refinement of the Morita equations strengthens the
higher stabilizer argument. Local dimension-field isolation and signed
Casimir saturation settle dense multiplicity-eight cases. A complete split
between commutative and noncommutative signed sectors resolves the remaining
noncommutative frontier. Each pseudo-unitary obstruction is used for a
general conclusion only after its signed Galois reduction has been proved.

[Revision notes](REVISION_NOTES.md) list each accepted proof and its scope.
The complete input domain is frozen in
[`verification/round3/campaign_manifest.json`](verification/round3/campaign_manifest.json).
The [coverage report](research/round3/coverage.json) distinguishes full-census
scans, tests of the 22 residuals, model controls, surviving relaxations and
unfinished searches. A necessary-system witness is not a categorical model.

## Reproduce and inspect

Use Python with the pinned requirements and a C++17 compiler. Rebuilding the
PDFs also requires `pdflatex`. Check integrity before generating reports:

```bash
python -m pip install -r requirements.txt
python check_manifest.py
python -O software/round3_release.py --jobs 3
python software/model_catalog.py
python software/build_paper_tables.py
python software/round3_documents.py
python research/round3/coverage.py --require-canonical --output research/round3/coverage.json
python software/release_consistency.py
python -O software/release_consistency.py
python build_papers.py
```

The third-continuation release checker disables numerical optimizers and
reconstructs every accepted new proof. It retains the unchanged earlier
campaigns and their exact evidence. To replay every continuation, run
`python -O software/continuation_controls.py --jobs 3 --out verification/current/all_continuations.json`.
To replay the full inherited and extended negative catalogue, run
`python -O verify.py --jobs 2 --out verification/current/full_recheck.jsonl`.
Neither larger optional replay is represented as having been repeated for
this continuation.

`data/decisions.json` is authoritative. CSV files, paper tables and
`data/unresolved_tensors.json` are derived from it. General, pivotal,
spherical, pseudo-unitary and unitary existence are recorded separately.
The original campaign and earlier continuation certificate files remain
unchanged; the new allocation is `certificates/continuation_round3.jsonl`.
Historical reports retain their original inputs and dates and do not define
current classification status.

The census is inherited from the pinned
[Fusion Ring Census](https://github.com/sebastienpalcoux/fusion-ring-census/tree/b86eb6dc6eeeafe5fc5f6906d7b074e0322e9726).
Its source is bundled for offline replay. The [OEIS directory](oeis/README.md)
is a local counting proposal, not an online submission. No claim beyond
multiplicity eight is made.
'''
 (ROOT/'README.md').write_text(intro)
 names={
 'c4_associator_stabilizer':'Forced cyclic associator and Clifford rotation',
 'general_ambient_full_character_rotation':'Full-character cyclotomic rotation and signed Galois reduction',
 'general_low_verlinde_restriction':'Low Verlinde and restriction-product constraints; signed reduction',
 'general_integral_morita_rotation':'Integral Morita congruences and higher Clifford rotation',
 'inert_quadratic_pseudo_exclusion':'Local dimension-field isolation and signed-spectrum saturation',
 'split_quadratic_different_pseudo_exclusion':'Different ideal, abelian field exhaustion and signed saturation',
 'noncommutative_signed_exclusion':'Complete signed-sector exhaustion and weighted induction',
 }
 proofs=['| Tensor | General obstruction | Exact proof source |','|---|---|---|']
 for r in sorted(records,key=lambda r:(r['m'],int(r['id'].split('_')[-1]))):
  proofs.append(f"| `{r['id']}` | {names[r['certificate']['kind']]} | [`{r['source']}`]({r['source']}) |")
 notes=f'''# Revision notes — third continuation, 29 September 2026

## Result

This continuation adds **{new} general exclusions**, reducing the inherited
22-case frontier to **{unresolved} unresolved rings**. The complete ledger has
**{excluded:,} general exclusions and 54 realized rings**. The exact
multiplicity bands **{bands}** are complete. There are no new positive
identifications and no changes to the underlying census or identifiers.

{table}

## New accepted general exclusions

{chr(10).join(proofs)}

The canonical disjoint allocation is
`certificates/continuation_round3.jsonl`. Alternative proofs and new
confirmations of old exclusions are retained without double counting.
The first and second continuations contain 7 and 18 earlier exclusions;
their original files are unchanged.

## Mathematical advances

- **Cyclic associators:** the uniform cyclic order-four family forces an
  even parameter and a unique anticommuting module action. A trivial pointed
  associator is impossible in the positive cases at issue; its nontrivial
  class forces fourth-indicator support. Every remaining induction branch
  of the smallest multiplicity-four case is excluded. The realized parameter
  zero and two members are preserved.
- **Full character fields:** exact relative cyclotomic traces retain the
  character information lost by projecting to the FP field. Coupled Galois
  and modular equations settle `R6_4_211`; low Verlinde positivity and
  restriction products settle `R6_4_243`. Both include complete unrestricted
  signed reductions before the general conclusion.
- **Integral Morita equations:** an exact congruence annihilating every
  integer multiplicity column but not the right-hand side rejects branches
  that are feasible over the rationals. The remaining branches are covered
  by exhaustive higher Clifford-indicator certificates.
- **Local signed spectra:** central induction puts every original formal
  codegree in the categorical dimension field. Local factorization and
  cyclotomicity isolate that field, after which exact positive codegree
  enumeration saturates the signed Casimir bound. The split quadratic case
  additionally uses the different ideal and a finite abelian-field list.
- **Noncommutative sectors:** the remaining noncommutative inputs are split
  into both possible signed algebra types. The commutative sector is
  exhausted when necessary; the other sector has type C + C + M2(C).
  Its weighted codegree identity and trace bound force magnitude saturation,
  all sign tables are original gauges, and exact weighted induction rejects
  every pseudo-unitary branch.

The formal-codegree normalization in the reusable oriented helper was
corrected for a noncommutative source: a matrix block's Casimir eigenvalue
is twice its formal codegree. The audit confirms that every inherited
noncommutative exclusion already used the correctly weighted checker;
no old allocation changes. The new sector proof explicitly uses codegree12,
not the Casimir eigenvalue24.

## Coverage and the remaining frontier

`verification/round3/campaign_manifest.json` fixes all 22 starting tensors.
`research/round3/coverage.json` records the current allocation and the exact
scope of each scan. Tensor-family and arithmetic applicability scans include
all 16,612 census records. The expensive induction and Morita campaigns test
all 22 residuals and all 54 positive models, with eligibility, survival and
budget outcomes retained. Ineligible or unfinished positive controls are
reported explicitly and are not described as feasible witnesses.

The remaining tensors are exported in `data/unresolved_tensors.json`.
Exact strengthened witnesses for the two quartic multiplicity-four cases
show that those finite necessary systems survive; they do not construct a
category. Further field and induction reductions on other cases are retained
as research progress without changing classification status.

## Verification and revised deliverables

`verification/round3/release_replay.json` records exact checking of the new
canonical allocation with optimized Python and numerical optimizers disabled.
The criterion directories retain independent arithmetic audits, positive
controls, based relabelings and rejected certificate corruptions. The original
negative campaign and the preceding continuations retain their unchanged
source-bound evidence; the entire old catalogue is not claimed to have been
replayed again.

The JSON/CSV ledgers, residual tensors, derived counts, allocation tables,
main paper, verification guide and current documentation are regenerated.
`software/release_consistency.py` checks the agreement of the derived exports
with the authoritative ledger in normal and optimized Python modes. PDF
compilation and visual checks are separate from the mathematical certificate
replay. `SHA256SUMS` covers every archived file except itself; the ZIP receives
both CRC and complete manifest verification.

The previous notes are preserved in
`provenance/REVISION_NOTES_second_continuation.md` and
`provenance/REVISION_NOTES_first_continuation.md`. Historical logs remain
historical; use the current ledger for current status.
'''
 (ROOT/'REVISION_NOTES.md').write_text(notes)
 print('Updated current prose from',new,'accepted new certificates')

if __name__=='__main__':main()
