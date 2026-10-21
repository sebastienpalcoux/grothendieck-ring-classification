#!/usr/bin/env python3
"""Refresh current report and website prose from the accepted M3 ledger."""
import json
import hashlib
import re
import subprocess
import sys
from html import escape
from pathlib import Path
from rank7_publication import summary as rank7_summary, remaining_ids
from rank8_publication import extension, summary, PUBLICATION_DATE_LONG, STATUS_REPORT, EVIDENCE, archive_path

ROOT = Path(__file__).resolve().parents[1]

def frontier_replay_scope(repo):
    """Describe completed canonical lanes without requiring an archive replay."""
    from rank8_frontier import commands, source_inventory, validate_ledger
    folder=repo/'evidence/rank8_frontier_20261021/publication'
    if not folder.is_dir():
        return ''
    manifest=folder/'source_manifest.json'
    digest=lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
    if source_inventory(repo)!=json.loads(manifest.read_text()):
        raise ValueError('Frontier source inventory differs from its frozen manifest')
    summary=validate_ledger(repo)
    required=commands(repo)
    def lane(name,optimized):
        report=json.loads((folder/name).read_text())
        if (report.get('status')!='PASS' or report.get('mathematical_replay_performed') is not True
                or report.get('optimized_python') is not optimized
                or report.get('source_manifest_sha256')!=digest(manifest)
                or report.get('ledger_sha256')!=summary['ledger_sha256']
                or [item.get('script') for item in report.get('sections',[])]!=required
                or any(item.get('returncode')!=0 for item in report['sections'])):
            raise ValueError('Incomplete or stale canonical frontier replay: '+name)
        for item in report['sections']:
            if digest(repo/item['log'])!=item['log_sha256']:
                raise ValueError('Canonical frontier replay log changed: '+item['log'])
    lane('replay_normal.json',False)
    if (folder/'replay_optimized.json').is_file():
        lane('replay_optimized.json',True)
        status=f'Canonical normal and optimized frontier replays each passed all {len(required)} checks.'
    else:
        status=f'The canonical normal frontier replay passed all {len(required)} checks. Its optimized replay is still pending.'
    return status+' Fresh replay after extraction from the publication archive is deferred.'


def center_replay_scope():
    return ('The separate center-pattern addendum passed all eight checks in canonical normal and optimized Python, '
            'including independent arithmetic reconstructions and positive controls. '
            'Fresh replay after extraction from the publication archive is deferred.')


def center_scope(repo):
    folder = repo/'evidence/rank8_center_followup_20261021'
    if not folder.is_dir():
        return ''
    run = subprocess.run([sys.executable,str(folder/'verify.py'),'--root',str(repo),
                          '--metadata-only'],cwd=repo,text=True,capture_output=True)
    if run.returncode or json.loads(run.stdout).get('status') != 'METADATA_PASS':
        raise ValueError('Separate center-pattern replay required:\n'+run.stdout+run.stderr)
    a = json.loads((folder/'r721_center_extension_receipt.json').read_text())
    b = json.loads((folder/'r1154_quartic_reconciliation.json').read_text())
    if a['pattern_exclusions']+a['remaining_Gram_patterns'] != 4:
        raise ValueError('R721 center-pattern partition')
    if b['height6_and_quartic_exclusion_union']+b['combined_remaining_patterns'] != b['common_cubic_pattern_domain']:
        raise ValueError('R1154 center-pattern partition')
    return (f"A separately verified fourth-moment and center-action refinement excludes {a['pattern_exclusions']} of the four necessary center patterns for R8_3_721, leaving {a['remaining_Gram_patterns']}. "
            f"For R8_3_1154, exact coordinate norm and interval bounds exclude {b['height6_and_quartic_exclusion_union']:,} of {b['common_cubic_pattern_domain']:,} patterns, leaving {b['combined_remaining_patterns']}. "
            'The surviving action matrices and patterns are necessary data only; no complete center fusion ring, associator or categorical model is constructed. Both source rings remain unresolved.')

def integer_scope(repo, extension):
    """Summarize the terminal finite searches without promoting numerical failure."""
    if not extension.get('frontier'):
        return ''
    evidence = repo/'evidence/rank8_frontier_20261021'
    parts = []
    if 'R8_3_928' in extension['remaining_ids']:
        cases = json.loads((evidence/'r928_semion_rotation/integer_counts.json').read_text())['cases']
        statuses = [case['result']['status'] for case in cases]
        allowed = {'exact_nonnegative_integer_witness', 'integer_feasibility_unresolved'}
        if set(statuses)-allowed:
            raise ValueError('Review the R928 integer-search publication summary')
        parts.append(f"R8_3_928 has {statuses.count('exact_nonnegative_integer_witness')} exact integer witnesses and {statuses.count('integer_feasibility_unresolved')} patterns with unresolved integer feasibility")
    if 'R8_3_941' in extension['remaining_ids']:
        record = json.loads((evidence/'review/r941_fusion_traces.json').read_text())
        retained = set(record['paired_surviving_allocations'])
        integral = set(record['retained_exact_integer_witness_allocations'])
        unresolved = set(record['retained_integer_feasibility_unresolved'])
        if record['status'] != 'exact_complete' or integral & unresolved or integral | unresolved != retained:
            raise ValueError('Review the R941 integer-search publication summary')
        parts.append(f"R8_3_941 retains {len(retained)} patterns, with {len(integral)} exact integer witnesses and {len(unresolved)} unresolved integer-feasibility questions")
    return ('In the final finite center-constraint systems, '+ '; '.join(parts)+
            '. These witnesses are necessary data, not categorical models; uncertified numerical failures are not exclusions.') if parts else ''

def main():
    ext = extension(ROOT)
    if ext is None:
        raise ValueError('Accepted M3 ledger required')
    receipts = [json.loads((ROOT/EVIDENCE/'pipeline'/name).read_text()) for name in
                ('continuation_replay.json', 'continuation_replay_optimized_invocation.json')]
    if any(r.get('status') != 'PASS' for r in receipts) or receipts[0]['ledger_digest'] != receipts[1]['ledger_digest']:
        raise ValueError('Matching complete normal and optimized replays required')
    frontier_note = frontier_replay_scope(ROOT) if ext.get('frontier') else ''
    integer_note = integer_scope(ROOT, ext)
    center_note = center_scope(ROOT)
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
        if ext['unitary_excluded_ids']:
            content['open_cases'][-1]['paragraphs'].append('Unitary categorification is excluded for '+', '.join(ext['unitary_excluded_ids'])+'. These scoped obstructions leave general complex categorification unresolved.')
        if 'R8_3_731' in ext['remaining_ids']:
            content['open_cases'][-1]['paragraphs'].append('Any categorification of R8_3_731 would be nonunitary and not weakly group-theoretical: its exact simple based ring and negative primary-three witness combine with the simple weakly group-theoretical classification. This conditional restriction supplies no categorification or general exclusion.')
    content['open_case_count'] = len(remaining_ids(ROOT))
    if ext.get('frontier') and ext['unresolved']:
        case=content['open_cases'][-1]
        case['paragraphs'].append('These remaining rings are extensively investigated exotic candidates in the operational sense: each survived the documented case-specific campaign of known and newly developed exclusions and model searches, including complete finite domains and specified unbounded construction families. This designation does not assert existence or novelty of a future realization.')
        case['paragraphs']=[p.replace('evidence/rank8_m3_20261021/pipeline/residual_attempts.json',ext['attempts_source']) for p in case['paragraphs']]
        if integer_note:
            case['paragraphs'].append(integer_note)
        if center_note:
            case['paragraphs'].append(center_note)
    heading = 'Rank eight: multiplicity-three extension'
    content['replay_sections'] = [x for x in content['replay_sections'] if x['heading']!=heading]
    content['replay_sections'].insert(0, {'heading':heading,'paragraphs':[
        'Fresh full normal and optimized aggregate replays passed for the accepted source-bound ledger. Their receipts bind the exact source tensors, historical decisions, accepted certificates, model constructors and proof-source files. Each referenced replay log is separately checksummed.',
        'Run supplements/rank8/software/verify_m3_continuation.py in normal and optimized Python with --output pointing to separate validation receipts, preserving the frozen baseline receipts. Assertion-based inherited checks run with assertions enabled. Metadata-only mode checks file identities and reconciliation with the full receipts; it does not repeat the mathematical computations. The release includes the repository-relative dependency tree.',
        'Exact replay checks the stated finite identities and certificates. Categorical reductions, complete enumeration and claims of mathematical novelty have separate proof obligations. Independent human verification and Lean formalization remain pending.']})
    heading = 'Rank-eight multiplicity-three continuation'
    content['theoretical_results'] = [x for x in content['theoretical_results'] if x['heading']!=heading]
    content['theoretical_results'].insert(0, {'heading':heading,'paragraphs':[
        'Unified exclusions combine negative-subring transfer, quadratic-compositum compression, weak-integral and biquadratic relative twist traces, complete signed lifting and convex central induction. Exact separation of an enlarged necessary-condition system gives a valid contradiction only after the hypotheses and complete lifting are established.',
        'Structural arguments use module-category ranks, split-module polynomial constraints, solvability, equivariantization and Morita transport. A unitary-only positivity obstruction becomes a general exclusion only when a separate theorem proves the relevant category must admit a unitary realization.',
        'The explicit models include near-group equivariantizations, a cyclic permutation equivariantization of three Fibonacci factors, exceptional subfactor constructions, a conformal-embedding Morita dual, ordinary groups and a twisted A6/A5 group-theoretical construction. All model identifications compare the full 512 multiplication coefficients. Existence does not imply uniqueness or categorical novelty.']})
    frontier_heading='Further rank-eight frontier investigation'
    content['replay_sections']=[x for x in content['replay_sections'] if x['heading']!=frontier_heading]
    content['theoretical_results']=[x for x in content['theoretical_results'] if x['heading']!=frontier_heading]
    if ext.get('frontier'):
        content['replay_sections'].insert(0,{'heading':frontier_heading,'paragraphs':[
            frontier_note,
            'The original M3 ledger and replay receipts are preserved. New decisions use a separate continuation ledger and source manifest. Run tools/verify_rank8_frontier.py in normal and optimized Python after the original M3 replay. Its strict metadata-only verification still requires both matching full continuation receipts.',
            'The per-ring audit records completed finite exclusion tests, exact feasible necessary-condition witnesses and excluded construction families. Each result keeps its precise hypotheses and search domain.']})
        content['theoretical_results'].insert(0,{'heading':frontier_heading,'paragraphs':[
            f"The original 34 unresolved M3 tensors now have {ext['frontier']['new_decisions']} additional general-complex exclusions. Their identifiers are "+', '.join(ext['frontier']['resolved_ids'])+'.',
            'The new arguments include simultaneous split-module representations, normal-matrix spectral support, a complete near-group TPE reduction, complete central-induction frame constraints, full character-labeled modular S and STS equations, a two-prime norm criterion for integral center objects, complete integer center decompositions and cubic Verlinde integrality, and integral Morita and relative-cohomology obstructions. Exact all-parameter filters exclude specified near-group construction routes for every original frontier tensor. General Galois-pseudo-unitarity reductions extend the scope of all seven noncommutative searches. Complete connected-algebra underlying-object filters and exact feasible center constraints describe the remaining construction possibilities; their survivors are not asserted algebras or categories.']})
    center_heading='Additional center-pattern refinement'
    content['replay_sections']=[x for x in content['replay_sections'] if x['heading']!=center_heading]
    content['theoretical_results']=[x for x in content['theoretical_results'] if x['heading']!=center_heading]
    if center_note:
        content['theoretical_results'].insert(0,{'heading':center_heading,'paragraphs':[
            'Fourth Verlinde moments couple all distinguished tensor-product decompositions to the same nonnegative integer restriction matrix. Exact minimum-norm projection and rank-one residual Grams yield coordinate obstructions. A complete cyclic-space and orthogonal-projector argument classifies the remaining distinguished center-action tuples for R8_3_721.',
            center_note]})
        content['replay_sections'].insert(0,{'heading':center_heading,'paragraphs':[
            center_replay_scope()+' Run evidence/rank8_center_followup_20261021/verify.py --root . in both modes.',
            'This refinement preserves the frozen frontier decision ledger and its original audit. Its precise pattern reductions and remaining domains are recorded separately; no new ring exclusion or categorical realization is asserted.']})
    path.write_text(json.dumps(content, indent=2, ensure_ascii=False)+'\n')
    path = ROOT/'site/dist/review.html'; html = path.read_text()
    html = re.sub(r'Research status · \d+ October 2026', 'Research status · '+PUBLICATION_DATE_LONG, html)
    html = re.sub(r'prepublication-review-2026-10-(?:19|20)\.pdf', STATUS_REPORT, html)
    html = re.sub(r'(?:19|20) October research-status report','21 October research-status report',html)
    panel = f'<div class="review-panel" id="review-outcome"><h2>Current classification · {len(remaining_ids(ROOT))} open questions</h2><p>{escape(summary(ROOT))}</p><p>{escape(rank7_summary(ROOT))}</p><p>The two rank-six cases <code>R6_4_155</code> and <code>R6_8_1660</code> remain open. The historical 38-case continuation has 36 decisions and retains its original scope.</p></div>'
    html, n = re.subn(r'<div class="review-panel" id="review-outcome">.*?</div>', panel, html, flags=re.S)
    if n != 1: raise ValueError('Unique current outcome panel required')
    block = ('<section id="rank-eight-m3"><h3>Rank eight · multiplicity three</h3><p>'+escape(summary(ROOT))+'</p>'
        '<p><a href="./papers/rank8.pdf">Updated manuscript</a> · <a href="./downloads/'+Path(archive_path(ROOT)).name+'">Proofs and exact verification</a> · <a href="./downloads/remaining_cases.py" download>Open fusion tensors</a> · <a href="./data/rank8_m3_attempts.json" download>Individual attempt records</a></p>'
        '<p>The census enumeration is complete according to producer records, with independent tensor and isomorphism audits. The categorification inventory separates proven exclusions, explicit constructions and individually investigated candidates. A candidate is not a proof of categorifiability or exotic existence. New arguments remain subject to independent human review.</p>'
        '<details><summary>Unresolved rank-eight identifiers</summary><p>'+', '.join('<code>'+escape(rid)+'</code>' for rid in ext['remaining_ids'])+'</p></details></section>')
    if integer_note:
        block=block.replace('</section>','<p>'+escape(integer_note)+'</p></section>')
    if center_note:
        block=block.replace('</section>','<p>'+escape(center_note)+'</p><p><a href="https://github.com/sebastienpalcoux/grothendieck-ring-classification/tree/main/evidence/rank8_center_followup_20261021">Center-pattern addendum and separate exact replays</a></p></section>')
    if frontier_note:
        block=block.replace('</section>','<p>'+escape(frontier_note)+'</p></section>')
    if center_note:
        block=block.replace('</section>','<p>'+escape(center_replay_scope())+'</p></section>')
    if ext['unitary_excluded_ids']:
        scoped='<p>Unitary categorification is excluded for '+', '.join('<code>'+escape(rid)+'</code>' for rid in ext['unitary_excluded_ids'])+'. General complex categorification remains unresolved.</p>'
        if 'R8_3_731' in ext['remaining_ids']:
            scoped+='<p>Any categorification of <code>R8_3_731</code> would also fail to be weakly group-theoretical. This is a conditional restriction, not an existence claim.</p>'
        block=block.replace('</section>',scoped+'</section>')
    html = re.sub(r'<section id="rank-eight-m3">.*?</section>\s*','',html,flags=re.S)
    html = html.replace('    <h2 id="rank-eight">','    '+block+'\n    <h2 id="rank-eight">')
    path.write_text(html)
    path = ROOT/'site/dist/index.html'
    html = re.sub(r'>\d+ OCT 2026<','>21 OCT 2026<',path.read_text())
    path.write_text(re.sub(r'prepublication-review-2026-10-(?:19|20)\.pdf',STATUS_REPORT,html))
    path = ROOT/'site/README.md'
    readme = path.read_text()
    current = ('The historical 38-case continuation records 36 decisions: 29 proposed general '
        'exclusions and seven unitary constructions. Its two rank-six questions, '
        '`R6_4_155` and `R6_8_1660`, remain open.\n\n'+rank7_summary(ROOT)+'\n\n'+summary(ROOT)+'\n\n'
        'The rank-eight candidate audit distinguishes completed necessary-condition tests, '
        'unsuccessful model searches, ineligible tests and time limits. Scoped unitary '
        'obstructions preserve the general complex question; these candidates are not '
        'asserted fusion categories or established exotic examples.\n\n')
    if frontier_note:
        current += frontier_note+'\n\n'
    if center_note:
        current += center_replay_scope()+'\n\n'
    readme, count = re.subn(r'The (?:historical 38-case continuation records|continuation records).*?(?=Ranks two, three and four)',
                            lambda _: current, readme, count=1, flags=re.S)
    if count != 1: raise ValueError('Unique website README classification block required')
    path.write_text(readme)
    print('Refreshed current M3 report source and static research-status page.')

if __name__ == '__main__': main()
