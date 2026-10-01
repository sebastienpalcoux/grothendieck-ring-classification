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
M9_PATHS=(P/'certificates/m9_classification.jsonl',P/'certificates/m9_advanced.jsonl')
HISTORICAL_REPLAY=P/'verification/m9/retained_m8_release_summary.json'
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

def file_digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def certificate_digest(certificate):
    return hashlib.sha256(json.dumps(certificate,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def m9_structure_records(rows):
    """Check scoped nonexistence evidence without promoting it to general exclusion."""
    path=P/'certificates/m9_structure_only.json'
    if not path.exists():return [],None
    records=load(path)
    receipt_path=P/'verification/m9/structure_replay_optimized.json'
    receipt=json.loads(receipt_path.read_text())
    if (receipt.get('complete') is not True or receipt.get('passed') is not True
            or receipt.get('optimized_python') is not True or receipt.get('optimizer_disabled') is not True
            or receipt.get('count')!=len(records) or receipt.get('census_sha256')!=file_digest(P/'data/census.json')
            or receipt.get('certificates_sha256')!=file_digest(path)):
        raise ValueError('M9 structure-only exact-replay receipt is incomplete or stale')
    results=receipt.get('results',[]);by_id={r['id']:r for r in rows};seen=set()
    replay={r['id']:r for r in results}
    if len(replay)!=len(results) or set(replay)!={r.get('id') for r in records}:
        raise ValueError('M9 structure-only replay coverage mismatch')
    for rec in records:
        rid=rec.get('id')
        if (rid not in by_id or rid in seen or by_id[rid]['m']!=9 or rec.get('m')!=9
                or rec.get('structure') not in ('pivotal','spherical','pseudo_unitary')
                or not isinstance(rec.get('certificate'),dict)):
            raise ValueError('invalid M9 structure-only claim')
        result=replay[rid];tensor_hash=certificate_digest(by_id[rid]['N'])
        if (result.get('passed') is not True or result.get('m')!=9
                or result.get('structure')!=rec['structure']
                or result.get('tensor_sha256')!=tensor_hash or rec.get('tensor_sha256')!=tensor_hash
                or result.get('certificate_sha256')!=certificate_digest(rec['certificate'])):
            raise ValueError('M9 structure-only proof/tensor replay mismatch')
        seen.add(rid)
    return records,{'certificates':str(path.relative_to(P)),'certificates_sha256':file_digest(path),
        'replay':str(receipt_path.relative_to(P)),'replay_sha256':file_digest(receipt_path),
        'count':len(records),'ids':[r['id'] for r in records],
        'structures':{r['id']:r['structure'] for r in records},
        'scope':'Only the explicitly certified structure and stronger structures are excluded; no general nonexistence is inferred.'}

def historical_cohort(rows,summary):
    """Bind the unchanged historical campaign to its full original row objects."""
    counts={int(k):v for k,v in summary['source']['counts'].items()}
    cohort=[r for r in rows if r['m'] in counts]
    if dict(collections.Counter(r['m'] for r in cohort))!=counts:
        raise ValueError('historical census multiplicities changed')
    encoded=(json.dumps(cohort,separators=(',',':'))+'\n').encode()
    if len(cohort)!=summary['source']['tensors'] or hashlib.sha256(encoded).hexdigest()!=summary['census_sha256']:
        raise ValueError('historical census rows changed, including identifier or provenance metadata')
    return cohort

def m9_records(rows):
    """Accept only complete new campaigns with independent source-bound replay."""
    if max(r['m'] for r in rows)<9:return [],[]
    source_hash=file_digest(P/'data/census.json')
    by_id={r['id']:r for r in rows if r['m']==9}
    if len(by_id)!=sum(r['m']==9 for r in rows):
        raise ValueError('duplicate multiplicity-nine census identifier')
    records=[];seen=set();receipts=[]
    for kind,path in zip(('classification','advanced'),M9_PATHS):
        base=P/'verification/m9'/kind
        summary_path=base/'summary.json'
        if not path.exists() or not summary_path.exists():
            raise ValueError('new multiplicity-nine campaign is incomplete: '+kind)
        summary=json.loads(summary_path.read_text())
        current=load(path)
        if summary.get('complete') is not True or summary.get('census_sha256')!=source_hash:
            raise ValueError('M9 campaign is unfinished or bound to a different census: '+kind)
        if summary.get('certificates_sha256')!=file_digest(path) or summary.get('excluded')!=len(current):
            raise ValueError('M9 certificate file/count changed: '+kind)
        if kind=='classification':
            from classify_m9 import STAGES as M9_STAGES
            cohort=list(by_id.values())
            input_hash=hashlib.sha256(json.dumps(cohort,separators=(',',':')).encode()).hexdigest()
            if (summary.get('completed_stages')!=len(M9_STAGES) or summary.get('stages_total')!=len(M9_STAGES)
                    or summary.get('input_count')!=len(cohort) or summary.get('input_sha256')!=input_hash):
                raise ValueError('M9 original campaign input/stage mismatch')
            if (set(summary.get('unresolved_ids',[]))!=set(by_id)-{r.get('id') for r in current}
                    or summary.get('unresolved')!=len(summary.get('unresolved_ids',[]))):
                raise ValueError('M9 original campaign residual mismatch')
            replay_path=P/'verification/m9/replay/optimized_summary.json'
            replay=json.loads(replay_path.read_text())
            replay_records=load(P/'verification/m9/replay/optimized.jsonl')
            if (replay.get('complete') is not True or replay.get('failed')
                    or replay.get('passed')!=len(current) or replay.get('completed')!=len(current)
                    or replay.get('input_count')!=len(current) or replay.get('optimized_python') is not True
                    or replay.get('optimizer_disabled') is not True
                    or replay.get('census_sha256')!=source_hash
                    or replay.get('certificate_file_sha256')!=file_digest(path)):
                raise ValueError('M9 independent optimized replay is incomplete or stale')
        else:
            input_ids=summary.get('input_ids',[])
            if len(input_ids)!=len(set(input_ids)) or set(input_ids)!=set(by_id)-seen:
                raise ValueError('M9 advanced input does not match the complete standard residual')
            input_rows=[by_id[rid] for rid in input_ids]
            input_hash=hashlib.sha256(json.dumps(input_rows,sort_keys=True,separators=(',',':')).encode()).hexdigest()
            if summary.get('input_count')!=len(input_rows) or summary.get('input_sha256')!=input_hash:
                raise ValueError('M9 advanced input tensor hash mismatch')
            manifest=json.loads((base/'input_manifest.json').read_text())
            if any(manifest.get(k)!=summary.get(k) for k in ('census_sha256','input_count','input_ids','input_sha256')):
                raise ValueError('M9 advanced input manifest mismatch')
            if set(summary.get('unresolved_ids',[]))!=set(input_ids)-{r.get('id') for r in current}:
                raise ValueError('M9 advanced campaign residual mismatch')
            replay_path=base/'replay_optimized.json'
            replay=json.loads(replay_path.read_text())
            replay_records=replay.get('results',[])
            if (replay.get('complete') is not True or replay.get('passed') is not True
                    or replay.get('count')!=len(current) or replay.get('optimized_python') is not True
                    or replay.get('optimizer_disabled') is not True
                    or replay.get('census_sha256')!=source_hash
                    or replay.get('certificates_sha256')!=file_digest(path)):
                raise ValueError('M9 advanced independent optimized replay is incomplete or stale')
        replay_by={r['id']:r for r in replay_records}
        if len(replay_by)!=len(replay_records) or set(replay_by)!={r.get('id') for r in current}:
            raise ValueError('M9 independent replay does not cover exactly the accepted IDs')
        for rec in current:
            rid=rec.get('id')
            if (rid not in by_id or rid in seen or rec.get('m')!=9 or rec.get('status')!='excluded'
                    or rec.get('exact_checked') is not True or not isinstance(rec.get('certificate'),dict)
                    or not isinstance(rec.get('stage'),str) or not rec['stage']):
                raise ValueError('invalid or duplicate M9 negative: '+str(rid))
            result=replay_by[rid]
            if (result.get('passed') is not True or result.get('m')!=9
                    or result.get('optimized_python') is not True
                    or result.get('certificate_sha256')!=certificate_digest(rec['certificate'])):
                raise ValueError('M9 replay certificate mismatch: '+rid)
            if ((kind=='classification' and result.get('optimizer_disabled') is not True)
                    or (kind=='advanced' and result.get('optimizer_used') is not False)):
                raise ValueError('M9 exact replay did not disable numerical optimization: '+rid)
            if rec.get('census_sha256',source_hash)!=source_hash:
                raise ValueError('M9 per-record source mismatch: '+rid)
            if kind=='advanced':
                tensor_hash=hashlib.sha256(json.dumps(by_id[rid]['N'],separators=(',',':')).encode()).hexdigest()
                if result.get('tensor_sha256')!=tensor_hash or rec.get('tensor_sha256')!=tensor_hash:
                    raise ValueError('M9 advanced tensor mismatch: '+rid)
            seen.add(rid);records.append(rec)
        receipts.append({'campaign':kind,'certificates':str(path.relative_to(P)),
            'certificates_sha256':file_digest(path),'summary':str(summary_path.relative_to(P)),
            'summary_sha256':file_digest(summary_path),'replay':str(replay_path.relative_to(P)),
            'replay_sha256':file_digest(replay_path),'excluded':len(current)})
    return records,receipts

def m9_stage_reports(rows,decisions):
    """Reconstruct the new cohort's ordered sieve from committed attempts."""
    if max(r['m'] for r in rows)<9:return []
    accepted,_=m9_records(rows)
    accepted_by={r['id']:r for r in accepted}
    source_hash=file_digest(P/'data/census.json')
    live={r['id'] for r in rows if r['m']==9};reports=[]
    from classify_m9 import STAGES as NEW_STAGES
    for campaign in ('classification','advanced'):
        base=P/'verification/m9'/campaign
        summary=json.loads((base/'summary.json').read_text())
        attempts=load(base/'attempts.jsonl')
        if campaign=='classification':
            state=json.loads((base/'stages.json').read_text())
            if state['identity']['census_sha256']!=source_hash:
                raise ValueError('M9 stage report source mismatch')
            names=[x[0] for x in NEW_STAGES]
            labels={x[0]:x[1] for x in NEW_STAGES}
            if [s['stage'] for s in state['stages']]!=names:
                raise ValueError('M9 executed stage order mismatch')
            original={s['stage']:s for s in state['stages']}
        else:
            names=summary['requested_stages']
            labels={name:'Advanced: '+name.replace('_',' ') for name in names}
            original={}
            if set(summary['input_ids'])!=live or summary['input_count']!=len(live):
                raise ValueError('M9 advanced input is not the complete standard residual')
        if any(a.get('stage') not in names for a in attempts):
            raise ValueError('M9 attempts contain an unexecuted stage')
        for name in names:
            group=[a for a in attempts if a['stage']==name]
            if len(group)!=len(live) or {a['id'] for a in group}!=live:
                raise ValueError('M9 stage does not cover its exact live input: '+name)
            if name in original and original[name].get('attempts_sha256'):
                payload=''.join(json.dumps(a,separators=(',',':'))+'\n' for a in group).encode()
                if hashlib.sha256(payload).hexdigest()!=original[name]['attempts_sha256']:
                    raise ValueError('M9 committed stage digest mismatch: '+name)
            removed=set()
            for a in group:
                if a.get('m')!=9 or a.get('census_sha256',source_hash)!=source_hash:
                    raise ValueError('M9 attempt multiplicity/source mismatch')
                if a['status']=='excluded':
                    if (a['id'] not in accepted_by or a.get('exact_checked') is not True
                            or a.get('certificate')!=accepted_by[a['id']]['certificate']
                            or a['stage']!=accepted_by[a['id']]['stage']):
                        raise ValueError('M9 stage exclusion lacks the accepted proof')
                    removed.add(a['id'])
            report={'stage':name,'label':labels[name],'campaign':campaign,
                'entered':len(live),'removed':len(removed),'remaining':len(live)-len(removed),
                'worker_seconds':sum(a.get('seconds',a.get('wall_seconds',0)) for a in group),
                'errors':sum(a['status']=='error' for a in group),
                'budget_exhausted':sum(a['status'] in ('budget_exhausted','timeout') for a in group)}
            if name in original and any(report[k]!=original[name][k] for k in ('entered','removed','remaining','errors','budget_exhausted')):
                raise ValueError('M9 stage summary disagrees with recorded attempts: '+name)
            live-=removed
            reports.append(report)
        if set(summary['unresolved_ids'])!=live:
            raise ValueError('M9 campaign residual summary disagrees with attempts')
    expected={r['id'] for r in decisions if r['m']==9 and r['status']!='excluded'}
    if expected!=live:raise ValueError('M9 stages disagree with the release ledger')
    return reports

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

def retained_historical_continuation(rows=None):
    """Reuse unchanged M8 proofs only through their frozen exact-replay receipt."""
    rows=rows if rows is not None else json.load(open(P/'data/census.json'))
    original=json.load(open(P/'verification/classification/summary.json'))
    historical_cohort(rows,original)
    if not HISTORICAL_REPLAY.exists():
        current=P/'verification/release_summary.json'
        candidate=json.loads(current.read_text())
        if candidate.get('census_sha256')!=original['census_sha256']:
            raise ValueError('no frozen M8 replay receipt; the current report is not the historical release')
        HISTORICAL_REPLAY.parent.mkdir(parents=True,exist_ok=True)
        HISTORICAL_REPLAY.write_bytes(current.read_bytes())
    receipt=json.loads(HISTORICAL_REPLAY.read_text())
    records=continuation_records(rows,verify_certificates=False)
    hashes={str(path.relative_to(P)):file_digest(path) for path in CONTINUATION_PATHS if path.exists()}
    if (receipt.get('census_sha256')!=original['census_sha256']
            or receipt.get('original_certificates_sha256')!=file_digest(P/'certificates/classification.jsonl')
            or receipt.get('continuation_certificates_exactly_verified') is not True
            or receipt.get('continuation_files_sha256')!=hashes
            or receipt.get('continuation_excluded')!=len(records)
            or receipt.get('continuation_ids')!=[r['id'] for r in records]
            or receipt.get('original_campaign_excluded')!=original['excluded']):
        raise ValueError('frozen historical continuation exact-replay receipt does not match current proofs/source')
    return records,{'mode':'retained historical exact replay; not rerun for the M9 extension',
        'receipt':str(HISTORICAL_REPLAY.relative_to(P)), 'receipt_sha256':file_digest(HISTORICAL_REPLAY),
        'historical_census_sha256':original['census_sha256'],'certificates':len(records),
        'certificate_files_sha256':hashes}

def freeze_continuation():
    """Collect and replay new proofs; call after the continuation campaign ends."""
    rows=json.load(open(P/'data/census.json'));by_id={r['id']:r for r in rows}
    summary=json.load(open(P/'verification/classification/summary.json'))
    original_residual=set(summary['unresolved_ids']);out={}
    # Rebuilding the ledger shrinks unresolved_tensors.json. Preserve the exact
    # original continuation domain independently for future replay/resume.
    input_rows=[{k:r[k] for k in ('id','m','index','dual','commutative','N')}
                for r in rows if r['id'] in original_residual]
    historical_cohort(rows,summary)
    manifest={'original_census_sha256':summary['census_sha256'],
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
    by_id={d['id']:d for d in decisions}
    bound=max(map(int,original_stages[-1]['by_multiplicity']))
    if any(r['m']>bound for r in records):
        raise ValueError('historical continuation contains a tensor beyond its input bound')
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

def build(verified_continuation=None,retain_historical_replay=False):
    files=['classification.jsonl'];neg={};diagnostics={}
    canonical=P/'certificates/classification.jsonl'
    if not canonical.exists():raise ValueError('the canonical classification certificates are required; run software/classify.py first')
    from classify import STAGES
    summary_path=P/'verification/classification/summary.json'
    if not summary_path.exists():raise ValueError('classification campaign is incomplete; resume it before rebuilding the ledger')
    summary=json.loads(summary_path.read_text())
    if summary.get('stages')!=len(STAGES) or summary.get('missing_retained_exclusions'):
        raise ValueError('classification stages or previously certified exclusions are incomplete')
    rows=json.load(open(P/'data/census.json'))
    from import_repository import verify_source
    current_source=verify_source(rows)
    old_rows=historical_cohort(rows,summary)
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
    old_ids={r['id'] for r in old_rows}
    if len(neg)!=summary['excluded'] or not set(neg)<=old_ids:
        raise ValueError('original certificate coverage or historical input mismatch')
    historical_receipt=None
    if retain_historical_replay:
        if verified_continuation is not None:raise ValueError('choose retained historical or supplied fresh replay, not both')
        verified_continuation,historical_receipt=retained_historical_continuation(rows)
    continuation=continuation_records(rows,verify_certificates=verified_continuation is None)
    if verified_continuation is not None:
        if continuation!=verified_continuation:raise ValueError('continuation changed after the supplied exact replay')
        print('RETAINED_EXACT_CONTINUATION_REPLAY',len(continuation),flush=True)
    for rec in continuation:neg[rec['id']]=rec['certificate']
    if not {r['id'] for r in continuation}<=old_ids:
        raise ValueError('historical continuation exceeds its original cohort')
    new_records,new_receipts=m9_records(rows)
    scoped_records,scoped_receipt=m9_structure_records(rows)
    for rec in new_records:
        if rec['id'] in neg:raise ValueError('M9 proof overlaps historical catalogue')
        neg[rec['id']]=rec['certificate']
    for row in rows:
        if row['m']==9 and row['id'] not in neg:
            diagnostics[row['id']]='Recorded standard and advanced multiplicity-nine criteria did not yield a complete general exclusion; eligibility, budget and survivor outcomes are retained under verification/m9/.'
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
            if state['pivotal']=='no':
                detail='Pivotal, spherical, pseudo-unitary and unitary nonexistence certified; general existence remains unresolved.'
            elif state['spherical']=='no':
                detail='Spherical, pseudo-unitary and unitary nonexistence certified; general and pivotal existence remain unresolved.'
            elif state['pseudo_unitary']=='no':
                detail='Pseudo-unitary and unitary nonexistence certified; general, pivotal and spherical existence remain unresolved.'
            else:
                detail='No complete general resolution. '+diagnostics.get(r['id'],'No complete certificate is recorded.')
            o.update(status='unresolved',diagnostic=detail,existence=state)
        ledger.append(o)
    verify_ledger(ledger)
    if max(r['m'] for r in rows)>=9:
        m9_stage_reports(rows,ledger)
    (P/'data/decisions.json').write_text(json.dumps(ledger,separators=(',',':'))+'\n')
    counts=[{'multiplicity':m,'classes':sum(r['m']==m for r in rows),**{k:sum(r['m']==m and r['status']==k for r in ledger) for k in ['excluded','unitarily_realized','spherically_realized_nonpseudounitary','unresolved']}} for m in range(1,max(r['m'] for r in rows)+1)]
    (P/'data/classification_counts.json').write_text(json.dumps(counts,indent=2)+'\n')
    if CONTINUATION.exists():
        report={'census_sha256':hashlib.sha256((P/'data/census.json').read_bytes()).hexdigest(),
                'original_certificates_sha256':hashlib.sha256(canonical.read_bytes()).hexdigest(),
                'continuation_certificates_sha256':hashlib.sha256(CONTINUATION.read_bytes()).hexdigest(),
                'continuation_files_sha256':{str(p.relative_to(P)):hashlib.sha256(p.read_bytes()).hexdigest() for p in CONTINUATION_PATHS if p.exists()},
                'original_campaign_excluded':summary['excluded'],
                'source':current_source,
                'historical_campaign_census_sha256':summary['census_sha256'],
                'historical_campaign_bound':max(r['m'] for r in old_rows),
                'historical_campaign_tensors':len(old_rows),
                'm9_campaigns':new_receipts,
                'm9_excluded':len(new_records),
                'm9_structure_only_receipt':scoped_receipt,
                'original_campaign_unresolved':summary['unresolved'],
                'continuation_excluded':len(continuation),
                'continuation_ids':[r['id'] for r in continuation],
                'continuation_by_kind':dict(collections.Counter(r['certificate']['kind'] for r in continuation)),
                'continuation_by_multiplicity':{str(m):sum(r['m']==m for r in continuation) for m in range(1,max(r['m'] for r in rows)+1)},
                'excluded':len(neg),'positive':len(pos),
                'unresolved':sum(r['status']=='unresolved' for r in ledger),
                'unresolved_ids':[r['id'] for r in ledger if r['status']=='unresolved'],
                'counts':counts,'continuation_certificates_exactly_verified':True,
                'continuation_verification_mode':('retained historical exact replay, bound to immutable source and proof hashes'
                    if historical_receipt else 'retained preceding exact replay' if verified_continuation is not None else 'fresh exact replay'),
                'historical_continuation_receipt':historical_receipt,
                'interpretation':'The completed multiplicity-one-through-eight campaign is preserved unchanged, bound by the exact serialized historical census. The ledger is its disjoint union with verified continuation and independently replayed multiplicity-nine certificates. Unfinished searches remove nothing.'}
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
            verification_scope=('Historical continuation certificates retain their frozen exact-replay evidence, checked against unchanged source and proof-file hashes; they are not replayed for this extension. '
                if historical_receipt else 'Accepted historical continuation certificates are exactly replayed. ')+
                'Every new multiplicity-nine certificate has a complete independent optimized exact replay bound to its proof and source tensor. The unchanged original negative catalogue retains the original exact campaign evidence; this build does not repeat that entire replay.',
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
        report['current_revision']='2026-10-01-M9-v1'
        report['current_frontier']='data/frontier_summary.json'
        report['new_realizations']=[r['id'] for r in ledger if r['m']==9 and r['status'] not in ('excluded','unresolved')]
        report['new_exclusions']=[r['id'] for r in new_records]
        report['retained_structural_realizations']=['R6_4_22','R6_4_91','R6_4_629']
        report['retained_structural_exclusions']=['R6_5_1204']
        report['structural_exclusion_verification']='verification/current/center_integrality.json'
        report['conformal_model_verification']='verification/current/conformal_models.json'
        target=P/'verification/continuation/release_summary.json';target.parent.mkdir(parents=True,exist_ok=True)
        target.write_text(json.dumps(report,indent=2)+'\n')
        (P/'verification/release_summary.json').write_text(json.dumps(report,indent=2)+'\n')
    if max(r['m'] for r in rows)>=9:
        from frontier_m9 import build as build_frontier
        build_frontier()
    print(json.dumps(counts,indent=2));return ledger
if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    mode=ap.add_mutually_exclusive_group()
    mode.add_argument('--freeze-continuation',action='store_true',help='collect and exactly replay new proofs without rebuilding the release ledger')
    mode.add_argument('--freeze-and-build',action='store_true',help='collect, exactly replay, and build in one process without repeating the same certificate checks')
    mode.add_argument('--retain-historical-replay',action='store_true',help='reuse the frozen M8 exact-replay receipt only when all historical source and proof hashes still match')
    args=ap.parse_args()
    if args.freeze_continuation:freeze_continuation()
    elif args.freeze_and_build:build(verified_continuation=freeze_continuation())
    else:build(retain_historical_replay=args.retain_historical_replay)
