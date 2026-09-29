"""Freeze the second continuation and build the disjoint release ledger.

Proof sources may grow during discovery. Only general certificates which
replay exactly on a tensor in the frozen 40-input domain are accepted.
The original campaign and the first continuation are not rewritten.
"""
import argparse
import hashlib
import json
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
KINDS={
    'general_stabilizer_rotation':'continuation_stabilizer_rotation',
    'general_stabilizer_rotation_higher':'continuation_stabilizer_rotation',
    'general_cyclotomic_stabilizer_trace':'continuation_stabilizer_rotation',
    'ramified_signed_pseudo_exclusion':'continuation_ramified_dimension',
    'ramified_signed_arithmetic_exclusion':'continuation_ramified_dimension',
    'ramified_Casimir_trace_exclusion':'continuation_ramified_dimension',
    'biquadratic_spherical_trace':'continuation_biquadratic_norm',
    'formal_codegree_trace_ideal':'continuation_trace_ideal',
    'trace_ideal_signed_pseudo_exclusion':'continuation_trace_ideal',
}

def sources():
    yield ROOT/'certificates/stabilizer_rotation_215.json',None
    yield ROOT/'certificates/biquadratic_exclusions.json','certificates'
    for folder in ('round2_higher','round2_theory','round2_external','round2_center','round2_literature'):
        for path in sorted((ROOT/'research'/folder).glob('*_general.json')):
            yield path,None

def replay_record(payload):
    rid,R,c=payload
    started=time.monotonic()
    import scipy.optimize
    def forbidden(*args,**kwargs):
        raise RuntimeError('optimizer forbidden during release certificate replay')
    scipy.optimize.linprog=scipy.optimize.milp=forbidden
    from check import verify
    verify(R,c)
    return {'id':rid,'kind':c['kind'],'passed':True,
            'seconds':time.monotonic()-started,'optimized_python':not __debug__,
            'optimizer_disabled':True}

def freeze_and_build(jobs=1):
    import scipy.optimize
    def forbidden(*args,**kwargs):
        raise RuntimeError('optimizer forbidden during release certificate replay')
    scipy.optimize.linprog=scipy.optimize.milp=forbidden
    from exact import require
    from check import verify
    from release import ROUND2,CONTINUATION,load,build,continuation_records
    rows=json.loads((ROOT/'data/census.json').read_text());by_id={r['id']:r for r in rows}
    manifest=json.loads((ROOT/'verification/round2/campaign_manifest.json').read_text())
    domain={r['id']:r for r in manifest['inputs']}
    require(set(domain)==set(manifest['input_ids']) and len(domain)==manifest['input_count'],
            'invalid second-continuation input manifest')
    require(all(r['N']==by_id[rid]['N'] for rid,r in domain.items()),'frozen input tensor changed')
    selected={};alternatives=[]
    for path,field in sources():
        require(path.exists(),'missing round-two source: '+str(path))
        obj=json.loads(path.read_text());records=obj[field] if field else [obj]
        for rec in records:
            c=rec.get('certificate');rid=rec.get('id')
            require(rid in domain and isinstance(c,dict),'proof source outside frozen input domain')
            require(c.get('kind') in KINDS,'source is not an accepted general proof kind')
            if rid in selected:
                # Keep one allocation, while every independently supplied proof
                # is still checked below against exactly the same input tensor.
                alternatives.append((rid,by_id[rid]['N'],c))
                continue
            selected[rid]={'id':rid,'m':by_id[rid]['m'],'status':'excluded',
                          'stage':KINDS[c['kind']],'certificate':c,'exact_checked':True,
                          'source':str(path.relative_to(ROOT)),
                          'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                          'seconds':rec.get('seconds')}
    ordered=sorted(selected.values(),key=lambda r:(list(dict.fromkeys(KINDS.values())).index(r['stage']),
                                                   r['m'],by_id[r['id']]['index']))
    first=load(CONTINUATION)
    require(not ({r['id'] for r in first}&set(selected)),'continuations overlap')
    work=[(rec['id'],by_id[rec['id']]['N'],rec['certificate']) for rec in first+ordered]+alternatives
    replays=[]
    if jobs==1:
        for payload in work:
            print('VERIFY_CONTINUATION',payload[0],payload[2]['kind'],flush=True)
            replays.append(replay_record(payload))
    else:
        with ProcessPoolExecutor(max_workers=jobs) as pool:
            futures=[pool.submit(replay_record,payload) for payload in work]
            for future in as_completed(futures):
                result=future.result();replays.append(result)
                print('VERIFIED_CONTINUATION',result['id'],round(result['seconds'],2),flush=True)
    # Discovery reports may acquire replay metadata while this independent
    # replay is running. Mathematical payloads must remain identical.
    for path,field in sources():
        obj=json.loads(path.read_text());records=obj[field] if field else [obj]
        for record in records:
            rid=record.get('id')
            if rid in selected and selected[rid]['source']==str(path.relative_to(ROOT)):
                require(record['certificate']==selected[rid]['certificate'],
                        'source certificate changed during replay: '+rid)
                selected[rid]['source_sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
    ROUND2.write_text(''.join(json.dumps(r,separators=(',',':'))+'\n' for r in ordered))
    combined=continuation_records(rows,verify_certificates=False)
    require(combined==first+ordered,'frozen continuation union changed')
    ledger=build(verified_continuation=combined)
    report={'passed':True,'optimized_python':not __debug__,'optimizer_disabled':True,
            'new_exclusions':len(ordered),'new_ids':[r['id'] for r in ordered],
            'jobs':jobs,'replays':sorted(replays,key=lambda r:(r['id'],r['kind'])),
            'first_continuation_replayed':len(first),'certificate_file':str(ROUND2.relative_to(ROOT)),
            'certificate_sha256':hashlib.sha256(ROUND2.read_bytes()).hexdigest(),
            'ledger_sha256':hashlib.sha256((ROOT/'data/decisions.json').read_bytes()).hexdigest()}
    (ROOT/'verification/round2/release_replay.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2),flush=True)
    return ledger

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--jobs',type=int,default=1)
    args=parser.parse_args()
    if args.jobs<1:parser.error('--jobs must be positive')
    freeze_and_build(args.jobs)
