"""Build a disjoint ledger; identifiers are never passed to obstruction functions."""
import argparse,json,collections,hashlib
from existence import positive_registry,all_values,status_from_existence,verify_ledger,unresolved_existence
from pathlib import Path
P=Path(__file__).resolve().parents[1]
CONTINUATION=P/'certificates/continuation_20260929.jsonl'
ROUND2=P/'certificates/continuation_round2.jsonl'
ROUND3=P/'certificates/continuation_round3.jsonl'
ROUND4=P/'certificates/continuation_round4.jsonl'
STRUCTURAL=P/'certificates/structural_exclusions.jsonl'
CONTINUATION_PATHS=(CONTINUATION,ROUND2,ROUND3,ROUND4,STRUCTURAL)
CONTINUATION_LABELS={
    'continuation_center_integrality':'Continuation: center rotation integrality',
    'continuation_lower_rank_subring':'Continuation: rank-three subring',
    'continuation_involution_module':'Continuation: spectral module',
    'continuation_small_dimension_morita':'Continuation: order-six Morita',
    'continuation_character':'Continuation: character induction',
    'continuation_dimension_order':'Continuation: dimension order',
    'continuation_tensor_rotation':'Continuation: tensor rotation',
    'continuation_modular':'Continuation: modular induction',
    'continuation_general_induction':'Continuation: induction trees',
    'continuation_module_dual_gram':'Continuation: module Gram',
    'continuation_full_morita_gram':'Continuation: full Morita Gram',
    'continuation_stabilizer_rotation':'Continuation: stabilizer rotation',
    'continuation_ramified_dimension':'Continuation: ramified dimension field',
    'continuation_biquadratic_norm':'Continuation: biquadratic norm and trace',
    'continuation_trace_ideal':'Continuation: formal-codegree trace ideal',
    'continuation_c4_associator':'Continuation: forced cyclic associator',
    'continuation_signed_spectrum':'Continuation: local signed spectra',
    'continuation_noncommutative_spectrum':'Continuation: noncommutative signed spectra',
    'continuation_ambient_character':'Continuation: ambient character rotations',
    'continuation_integral_morita':'Continuation: integral Morita constraints',
    'continuation_subcategory_projection':'Continuation: subcategory center projection',
}

def load(path):
    if path.suffix=='.jsonl':
        out=[]
        for l in open(path):
            try:out.append(json.loads(l))
            except json.JSONDecodeError as e:raise ValueError(f"malformed frozen certificate record in {path}") from e
        return out
    o=json.load(open(path));return o if isinstance(o,list) else [o]

def continuation_records(rows=None,verify_certificates=True):
    """Read the independent continuation without modifying the original campaign."""
    paths=[p for p in CONTINUATION_PATHS if p.exists()]
    if not paths:return []
    rows=rows if rows is not None else json.load(open(P/'data/census.json'))
    by_id={r['id']:r for r in rows};seen=set();records=[r for path in paths for r in load(path)]
    original={r['id'] for r in load(P/'certificates/classification.jsonl')}
    from check import verify
    for rec in records:
        rid=rec.get('id')
        if rid not in by_id or rid in seen or rid in original:
            raise ValueError('invalid, repeated, or previously excluded continuation identifier: '+str(rid))
        if (rec.get('status')!='excluded' or rec.get('exact_checked') is not True
                or rec.get('m')!=by_id[rid]['m'] or not isinstance(rec.get('certificate'),dict)
                or not str(rec.get('stage','')).startswith('continuation_')):
            raise ValueError('malformed continuation certificate record: '+rid)
        if verify_certificates:
            print('VERIFY_CONTINUATION',rid,flush=True)
            verify(by_id[rid]['N'],rec['certificate'])
        seen.add(rid)
    return records

def freeze_continuation():
    """Collect and replay new proofs; call after the continuation campaign ends."""
    rows=json.load(open(P/'data/census.json'));by_id={r['id']:r for r in rows}
    summary=json.load(open(P/'verification/classification/summary.json'))
    original_residual=set(summary['unresolved_ids']);out={}
    # Rebuilding the ledger shrinks unresolved_tensors.json. Preserve the exact
    # original continuation domain independently for future replay/resume.
    input_rows=[{k:r[k] for k in ('id','m','index','dual','commutative','N')}
                for r in rows if r['id'] in original_residual]
    manifest={'original_census_sha256':hashlib.sha256((P/'data/census.json').read_bytes()).hexdigest(),
              'original_classification_certificates_sha256':summary['certificates_sha256'],
              'input_count':len(input_rows),'input_ids':[r['id'] for r in input_rows],
              'input_tensors_sha256':hashlib.sha256(json.dumps(input_rows,separators=(',',':')).encode()).hexdigest(),
              'inputs':input_rows,
              'interpretation':'Frozen original unresolved domain. Resume continuation searches from these tensors, not the shrinking current unresolved ledger.'}
    manifest_path=P/'verification/continuation/campaign_manifest.json'
    manifest_path.parent.mkdir(parents=True,exist_ok=True)
    if manifest_path.exists():
        if json.load(open(manifest_path))!=manifest:raise ValueError('the frozen continuation input manifest changed')
    else:manifest_path.write_text(json.dumps(manifest,indent=2)+'\n')
    sources=[
        ('certificates/new_rank3_subring.json','certificates','lower_rank_subring'),
        ('research/module_continuation/spectral_module_exclusions.json',None,'involution_module'),
        ('research/model_continuation/morita_order6_certificates.json','exclusions','small_dimension_morita'),
        ('verification/continuation/attempts.jsonl',None,None),
    ]
    from check import verify
    for filename,field,stage in sources:
        path=P/filename
        if not path.exists():raise ValueError('missing continuation proof source: '+filename)
        if field is None:records=load(path)
        else:records=json.load(open(path))[field]
        for rec in records:
            rid=rec['id']
            if rid not in original_residual or rid in out:continue
            if filename.endswith('attempts.jsonl'):
                if rec.get('status')!='excluded':continue
                if rec.get('exact_checked') is not True:
                    raise ValueError('unchecked attempted exclusion: '+rid)
            if not isinstance(rec.get('certificate'),dict):continue
            print('FREEZE_CONTINUATION',rid,flush=True)
            verify(by_id[rid]['N'],rec['certificate'])
            source_stage=stage or rec['stage']
            out[rid]={'id':rid,'m':by_id[rid]['m'],
                      'stage':'continuation_'+source_stage,'status':'excluded',
                      'certificate':rec['certificate'],'exact_checked':True,
                      'source':filename,'source_stage':source_stage,
                      'seconds':rec.get('seconds',None)}
    ordered=sorted(out.values(),key=lambda r:(list(CONTINUATION_LABELS).index(r['stage'])
                    if r['stage'] in CONTINUATION_LABELS else len(CONTINUATION_LABELS),
                    r['m'],by_id[r['id']]['index']))
    CONTINUATION.write_text(''.join(json.dumps(r,separators=(',',':'))+'\n' for r in ordered))
    print(json.dumps({'continuation_certificates':len(ordered),'ids':[r['id'] for r in ordered]},indent=2))
    # A later continuation has its own immutable proof file and input domain.
    # Include it in the returned replay, without rewriting either campaign.
    if ROUND2.exists():
        return continuation_records(rows,verify_certificates=True)
    return ordered

def continuation_stage_reports(rows,decisions,original_stages):
    """Append disjoint continuation rows while preserving the executed campaign."""
    records=continuation_records(rows,verify_certificates=False)
    if not records:return []
    if not original_stages:raise ValueError('continuation requires the original executed sieve')
    by_id={d['id']:d for d in decisions};bound=max(r['m'] for r in rows)
    remaining={str(m):original_stages[-1]['by_multiplicity'][str(m)]['remaining'] for m in range(1,bound+1)}
    groups={}
    for rec in records:
        decision=by_id.get(rec['id'])
        if decision is None or decision['status']!='excluded' or decision['certificate']!=rec['certificate']:
            raise ValueError('continuation tables require an up-to-date release ledger')
        groups.setdefault(rec['stage'],[]).append(rec)
    result=[]
    for stage,group in groups.items():
        removed=collections.Counter(r['m'] for r in group);per={}
        for m in range(1,bound+1):
            key=str(m);entered=remaining[key];remaining[key]-=removed[m]
            if remaining[key]<0:raise ValueError('continuation stage counter underflow')
            per[key]={'entered':entered,'removed':removed[m],'remaining':remaining[key]}
        result.append({'stage':stage,'label':CONTINUATION_LABELS.get(stage,stage.replace('_',' ')),
                       'continuation':True,'entered':sum(v['entered'] for v in per.values()),
                       'removed':len(group),'remaining':sum(remaining.values()),
                       'wall_seconds':None,'errors':0,'budget_exhausted':0,
                       'by_multiplicity':per})
    expected={str(m):sum(d['m']==m and d['status']!='excluded' for d in decisions) for m in range(1,bound+1)}
    if remaining!=expected:raise ValueError('union of original and continuation stages disagrees with the release ledger')
    return result

def build(verified_continuation=None):
    files=['classification.jsonl'];neg={};diagnostics={}
    canonical=P/'certificates/classification.jsonl'
    if not canonical.exists():raise ValueError('the canonical classification certificates are required; run software/classify.py first')
    from classify import STAGES
    summary_path=P/'verification/classification/summary.json'
    if not summary_path.exists():raise ValueError('classification campaign is incomplete; resume it before rebuilding the ledger')
    summary=json.loads(summary_path.read_text())
    if summary.get('stages')!=len(STAGES) or summary.get('missing_retained_exclusions'):
        raise ValueError('classification stages or previously certified exclusions are incomplete')
    if summary.get('census_sha256')!=hashlib.sha256((P/'data/census.json').read_bytes()).hexdigest():
        raise ValueError('classification summary does not match the current source import')
    if summary.get('certificates_sha256')!=hashlib.sha256(canonical.read_bytes()).hexdigest():
        raise ValueError('classification certificates changed since the completed campaign')
    diagnostics={rid:'The applicable recorded finite criteria did not produce a complete general exclusion; detailed eligibility and budget outcomes are in verification/classification/attempts.jsonl.' for rid in summary['unresolved_ids']}
    for fn in files:
        path=P/'certificates'/fn
        if not path.exists():continue
        for o in load(path):
            if 'certificate' in o and o.get('status') in (None,'excluded'):
                neg.setdefault(o['id'],o['certificate'])
            elif o.get('reason'):diagnostics[o['id']]=o['reason']
    rows=json.load(open(P/'data/census.json'))
    continuation=continuation_records(rows,verify_certificates=verified_continuation is None)
    if verified_continuation is not None:
        if continuation!=verified_continuation:raise ValueError('continuation changed after the supplied exact replay')
        print('RETAINED_EXACT_CONTINUATION_REPLAY',len(continuation),flush=True)
    for rec in continuation:neg[rec['id']]=rec['certificate']
    from conformal_models import verify as verify_conformal
    verify_conformal(fresh=False)
    pos=positive_registry()
    m1=[r for r in rows if r['m']==1];remain=[r for r in m1 if r['id'] not in neg]
    if len(m1)!=39 or len(remain)!=21:raise ValueError('multiplicity-one classification count mismatch')
    if {r['id'] for r in remain}!={r['id'] for r in m1 if r['id'] in pos}:raise ValueError('explicit multiplicity-one models do not cover the positive complement')
    if set(neg)&set(pos):raise ValueError('positive/negative contradiction: '+str(set(neg)&set(pos)))
    ledger=[]
    for r in rows:
        o={k:r[k] for k in ['id','m','index','source_label','dual','commutative']}
        if r['id'] in neg:o.update(status='excluded',certificate=neg[r['id']],existence=all_values('no'))
        elif r['id'] in pos:o.update(status=status_from_existence(pos[r['id']]['existence']),**pos[r['id']])
        else:
            state=unresolved_existence(r['id'])
            if state['pseudo_unitary']=='no':
                detail='Pseudo-unitary and unitary nonexistence certified; general, pivotal and spherical existence remain unresolved.'
            else:
                detail='No complete general resolution. '+diagnostics.get(r['id'],'No complete certificate is recorded.')
            o.update(status='unresolved',diagnostic=detail,existence=state)
        ledger.append(o)
    verify_ledger(ledger)
    (P/'data/decisions.json').write_text(json.dumps(ledger,separators=(',',':'))+'\n')
    counts=[{'multiplicity':m,'classes':sum(r['m']==m for r in rows),**{k:sum(r['m']==m and r['status']==k for r in ledger) for k in ['excluded','unitarily_realized','spherically_realized_nonpseudounitary','unresolved']}} for m in range(1,max(r['m'] for r in rows)+1)]
    (P/'data/classification_counts.json').write_text(json.dumps(counts,indent=2)+'\n')
    if CONTINUATION.exists():
        report={'census_sha256':hashlib.sha256((P/'data/census.json').read_bytes()).hexdigest(),
                'original_certificates_sha256':hashlib.sha256(canonical.read_bytes()).hexdigest(),
                'continuation_certificates_sha256':hashlib.sha256(CONTINUATION.read_bytes()).hexdigest(),
                'continuation_files_sha256':{str(p.relative_to(P)):hashlib.sha256(p.read_bytes()).hexdigest() for p in CONTINUATION_PATHS if p.exists()},
                'original_campaign_excluded':summary['excluded'],
                'original_campaign_unresolved':summary['unresolved'],
                'continuation_excluded':len(continuation),
                'continuation_ids':[r['id'] for r in continuation],
                'continuation_by_kind':dict(collections.Counter(r['certificate']['kind'] for r in continuation)),
                'continuation_by_multiplicity':{str(m):sum(r['m']==m for r in continuation) for m in range(1,max(r['m'] for r in rows)+1)},
                'excluded':len(neg),'positive':len(pos),
                'unresolved':sum(r['status']=='unresolved' for r in ledger),
                'unresolved_ids':[r['id'] for r in ledger if r['status']=='unresolved'],
                'counts':counts,'continuation_certificates_exactly_verified':True,
                'continuation_verification_mode':'retained preceding exact replay' if verified_continuation is not None else 'fresh exact replay',
                'interpretation':'The completed original campaign is preserved unchanged. The release ledger is its disjoint union with the separately replayed continuation certificates. Unfinished searches remove nothing.'}
        remaining=[r for r in ledger if r['status']=='unresolved']
        report.update(
            ledger_sha256=hashlib.sha256((P/'data/decisions.json').read_bytes()).hexdigest(),
            general_multiplicity_three_complete=not any(r['m']<=3 for r in remaining),
            complete_through_multiplicity=min((r['m'] for r in remaining),default=max(r['m'] for r in rows)+1)-1,
            first_unresolved=remaining[0]['id'] if remaining else None,
            first_continuation_excluded=len(load(CONTINUATION)),
            second_continuation_excluded=len(load(ROUND2)) if ROUND2.exists() else 0,
            third_continuation_excluded=len(load(ROUND3)) if ROUND3.exists() else 0,
            fourth_continuation_excluded=len(load(ROUND4)) if ROUND4.exists() else 0,
            original_release_summary='verification/original_release_summary.json',
            first_continuation_release_summary='verification/continuation/release_summary_before_round2.json',
            full_original_negative_replay_repeated=False,
            verification_scope='Accepted continuation certificates are exactly verified. The unchanged original negative catalogue retains the original exact campaign evidence; building this report does not repeat that entire replay.',
            current_consistency_checks=['verification/current/release_consistency_normal.json','verification/current/release_consistency_optimized.json'])
        if ROUND2.exists():
            report['second_continuation_replay']='verification/round2/release_replay.json'
            report['second_continuation_frozen_inputs']='verification/round2/campaign_manifest.json'
            report['document_checks']='verification/round2/document_qa.json'
        if ROUND3.exists():
            report['third_continuation_replay']='verification/round3/release_replay.json'
            report['third_continuation_frozen_inputs']='verification/round3/campaign_manifest.json'
            report['document_checks']='verification/round3/document_qa.json'
        if ROUND4.exists():
            report['fourth_continuation_replay']='verification/round4/release_replay.json'
            report['fourth_continuation_frozen_inputs']='verification/round4/campaign_manifest.json'
            report['document_checks']='verification/round4/document_qa.json'
        report['current_revision']='v6'
        report['current_frontier']='data/frontier_summary.json'
        report['new_realizations']=['R6_4_22','R6_4_91','R6_4_629']
        report['new_exclusions']=['R6_5_1204']
        report['structural_exclusion_verification']='verification/current/center_integrality.json'
        report['conformal_model_verification']='verification/current/conformal_models.json'
        target=P/'verification/continuation/release_summary.json';target.parent.mkdir(parents=True,exist_ok=True)
        target.write_text(json.dumps(report,indent=2)+'\n')
        (P/'verification/release_summary.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(counts,indent=2));return ledger
if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    mode=ap.add_mutually_exclusive_group()
    mode.add_argument('--freeze-continuation',action='store_true',help='collect and exactly replay new proofs without rebuilding the release ledger')
    mode.add_argument('--freeze-and-build',action='store_true',help='collect, exactly replay, and build in one process without repeating the same certificate checks')
    args=ap.parse_args()
    if args.freeze_continuation:freeze_continuation()
    elif args.freeze_and_build:build(verified_continuation=freeze_continuation())
    else:build()
