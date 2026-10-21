#!/usr/bin/env python3
"""Refresh current report and website prose from the accepted M3 ledger."""
import json
import re
from html import escape
from pathlib import Path
from rank7_publication import summary as rank7_summary, remaining_ids
from rank8_publication import extension, summary, PUBLICATION_DATE_LONG, STATUS_REPORT, EVIDENCE

ROOT = Path(__file__).resolve().parents[1]

def main():
    ext = extension(ROOT)
    if ext is None:
        raise ValueError('Accepted M3 ledger required')
    receipts = [json.loads((ROOT/EVIDENCE/'pipeline'/name).read_text()) for name in
                ('continuation_replay.json', 'continuation_replay_optimized_invocation.json')]
    if any(r.get('status') != 'PASS' for r in receipts) or receipts[0]['ledger_digest'] != receipts[1]['ledger_digest']:
        raise ValueError('Matching complete normal and optimized replays required')
    status = json.loads((ROOT/'data/classification_status.json').read_text())
    totals = status['inputs']['rank8']['status_totals']
    path = ROOT/'docs/prepublication_review_content.json'
    content = json.loads(path.read_text())
    content['date'] = PUBLICATION_DATE_LONG
    content['version'] = 'Rank-eight multiplicity-three continuation and current verification scope'
    content['summary'] = summary(ROOT)+' '+rank7_summary(ROOT)+' The two earlier rank-six questions remain open. The historical 38-case inventory keeps its original scope.'
    next(r for r in content['rank_counts'] if r['rank']==8).update(bound=3, rings=4500,
        excluded=totals['excluded'], models=totals.get('unitarily_realized',0)+totals.get('pseudo_unitarily_realized',0), open=totals.get('unresolved',0))
    content['coverage_notes'] = [s for s in content['coverage_notes'] if not s.startswith(('Rank eight is complete', 'The rank-eight M3'))]
    content['coverage_notes'].append('The rank-eight M3 extension preserves all 973 earlier records and adds 3,527 exact-multiplicity-three tensors. Source identities, tensor axioms and based-isomorphism audits are independently checked. Enumeration completeness relies on producer completion records. The supplied optimized source matches the producer source hashes for both the rank-seven M5 and rank-eight M3 runs; the exhaustive enumerations were not independently rerun.')
    content['open_cases'] = [x for x in content['open_cases'] if not x['id'].startswith('Rank eight:')]
    if ext['unresolved']:
        content['open_cases'].append({'id':f"Rank eight: {ext['unresolved']} rings",'heading':'Exact multiplicity three',
            'paragraphs':[f"The new band contains {ext['excluded']:,} recorded general exclusions, {ext['unitarily_realized']} unitary models and {ext['unresolved']} unresolved tensors. Each remaining tensor has an individual attempt record, distinguishing completed necessary-condition tests, unsuccessful model searches, ineligible tests and time limits.",
            'These are investigated categorification candidates, not asserted fusion categories or established exotic examples. Passing necessary conditions supplies no associator. Failing to find a model does not prove nonexistence. Exact tensors are in data/remaining_cases.py; the per-case record is evidence/rank8_m3_20261021/pipeline/residual_attempts.json.']})
    content['open_case_count'] = len(remaining_ids(ROOT))
    heading = 'Rank eight: multiplicity-three extension'
    content['replay_sections'] = [x for x in content['replay_sections'] if x['heading']!=heading]
    content['replay_sections'].insert(0, {'heading':heading,'paragraphs':[
        'Fresh full normal and optimized aggregate replays passed for the accepted source-bound ledger. Their receipts bind the exact source tensors, historical decisions, accepted certificates, model constructors and proof-source files. Each referenced replay log is separately checksummed.',
        'Run supplements/rank8/software/verify_m3_continuation.py in normal and optimized Python. Assertion-based inherited checks run with assertions enabled. Metadata-only mode checks file identities and reconciliation with the full receipts; it does not repeat the mathematical computations. The release includes the repository-relative dependency tree.',
        'Exact replay checks the stated finite identities and certificates. Categorical reductions, complete enumeration and claims of mathematical novelty have separate proof obligations. Independent human verification and Lean formalization remain pending.']})
    heading = 'Rank-eight multiplicity-three continuation'
    content['theoretical_results'] = [x for x in content['theoretical_results'] if x['heading']!=heading]
    content['theoretical_results'].insert(0, {'heading':heading,'paragraphs':[
        'Unified exclusions combine negative-subring transfer, quadratic-compositum compression, weak-integral and biquadratic relative twist traces, complete signed lifting and convex central induction. Exact separation of an enlarged necessary-condition system gives a valid contradiction only after the hypotheses and complete lifting are established.',
        'Structural arguments use module-category ranks, split-module polynomial constraints, solvability, equivariantization and Morita transport. A unitary-only positivity obstruction becomes a general exclusion only when a separate theorem proves the relevant category must admit a unitary realization.',
        'The explicit models include near-group equivariantizations, a cyclic permutation equivariantization of three Fibonacci factors, exceptional subfactor constructions, a conformal-embedding Morita dual, ordinary groups and a twisted A6/A5 group-theoretical construction. All model identifications compare the full 512 multiplication coefficients. Existence does not imply uniqueness or categorical novelty.']})
    path.write_text(json.dumps(content, indent=2, ensure_ascii=False)+'\n')
    path = ROOT/'site/dist/review.html'; html = path.read_text()
    html = re.sub(r'Research status · \d+ October 2026', 'Research status · '+PUBLICATION_DATE_LONG, html)
    html = re.sub(r'prepublication-review-2026-10-(?:19|20)\.pdf', STATUS_REPORT, html)
    html = re.sub(r'(?:19|20) October research-status report','21 October research-status report',html)
    panel = f'<div class="review-panel" id="review-outcome"><h2>Current classification · {len(remaining_ids(ROOT))} open questions</h2><p>{escape(summary(ROOT))}</p><p>{escape(rank7_summary(ROOT))}</p><p>The two rank-six cases <code>R6_4_155</code> and <code>R6_8_1660</code> remain open. The historical 38-case continuation has 36 decisions and retains its original scope.</p></div>'
    html, n = re.subn(r'<div class="review-panel" id="review-outcome">.*?</div>', panel, html, flags=re.S)
    if n != 1: raise ValueError('Unique current outcome panel required')
    block = ('<section id="rank-eight-m3"><h3>Rank eight · multiplicity three</h3><p>'+escape(summary(ROOT))+'</p>'
        '<p><a href="./papers/rank8.pdf">Updated manuscript</a> · <a href="./downloads/rank8-certified-through-m3.zip">Proofs and exact verification</a> · <a href="./downloads/remaining_cases.py" download>Open fusion tensors</a> · <a href="./data/rank8_m3_attempts.json" download>Individual attempt records</a></p>'
        '<p>The census enumeration is complete according to producer records, with independent tensor and isomorphism audits. The categorification inventory separates proven exclusions, explicit constructions and individually investigated candidates. A candidate is not a proof of categorifiability or exotic existence. New arguments remain subject to independent human review.</p>'
        '<details><summary>Unresolved rank-eight identifiers</summary><p>'+', '.join('<code>'+escape(rid)+'</code>' for rid in ext['remaining_ids'])+'</p></details></section>')
    html = re.sub(r'<section id="rank-eight-m3">.*?</section>\s*','',html,flags=re.S)
    html = html.replace('    <h2 id="rank-eight">','    '+block+'\n    <h2 id="rank-eight">')
    path.write_text(html)
    path = ROOT/'site/dist/index.html'
    html = re.sub(r'>\d+ OCT 2026<','>21 OCT 2026<',path.read_text())
    path.write_text(re.sub(r'prepublication-review-2026-10-(?:19|20)\.pdf',STATUS_REPORT,html))
    print('Refreshed current M3 report source and static research-status page.')

if __name__ == '__main__': main()
