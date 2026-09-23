"""Ordered, reproducible classification of the trusted rank-six census.

Run: python software/classify.py --jobs 4
No tensor enumeration is performed. Discovery budgets never imply exclusion:
each accepted certificate is checked by the exact dispatcher. Earlier proofs
are reusable witnesses, after all cheaper stages have actually been applied.
"""
import os
for variable in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):
    os.environ[variable]='1'
import argparse, collections, csv, hashlib, json, platform, signal, time, traceback,subprocess,sys
from concurrent.futures import ProcessPoolExecutor,ThreadPoolExecutor,as_completed
from pathlib import Path
P=Path(__file__).resolve().parents[1]

# The order prioritizes very cheap structural tests, then efficient arithmetic,
# and finally the finite character/sphericalization/induction calculations.
STAGES=[
 ('rank_two','Rank-two fusion subring',30),
 ('dnumber','Formal-codegree d-number',30),
 ('zero_spectrum','Zero-spectrum',30),
 ('lower_rank_subring','Closed lower-rank subring',30),
 ('involution_module','Involution module',30),
 ('subring','Subcategory dimension quotient',30),
 ('cyclotomic','Cyclotomicity',30),
 ('small_dimension_morita','Small-dimension Morita descent',30),
 ('field_automorphisms','Dimension-field automorphisms',30),
 ('weighted_induction','Noncommutative weighted induction',120),
 ('general_induction','Sphericalization/induction proof trees',180),
 ('dimension_order','Spherical dimension order',120),
 ('character','Character-aware central induction',120),
 ('tensor_rotation','Tensor-rotation traces',120),
 ('modular','Modular character induction',120),
 ('retained_completion','Deferred exact certificate checks',600)]

class DiscoveryBudget(Exception):pass
def stop(*_):raise DiscoveryBudget('finite per-ring discovery/checking allowance exhausted')

def discover(stage,row):
    R=row['N']
    if stage=='rank_two':
        for i in range(1,len(R)):
            m=R[i][i][i]
            if R[i][i][0]==1 and m>=2 and sum(R[i][i])==1+m:
                return {'kind':'rank_two','object':i,'multiplicity':m}
    elif stage=='dnumber' and row['commutative']:
        from rings import dnumber
        return dnumber(R)
    elif stage=='lower_rank_subring':
        from subring_descent import certificate
        return certificate(R)
    elif stage=='involution_module' and row['commutative']:
        from involution_module import certificate
        return certificate(R)
    elif stage=='subring' and row['commutative']:
        # Avoid constructing a character field when no proper subring exists.
        from subring_descent import closed_subrings
        if next(closed_subrings(R),None) is None:return None
        from proofs import subring_certificate
        return subring_certificate(R)
    elif stage=='cyclotomic' and row['commutative']:
        from proofs import cyclotomic_failure
        from rings import matrices,t
        return cyclotomic_failure([a.charpoly(t).as_poly() for a in matrices(R)])
    elif stage=='small_dimension_morita':
        from small_dimension_morita import certificate
        return certificate(R)
    elif stage=='field_automorphisms' and row['commutative']:
        from field_automorphisms import certificate
        return certificate(R)
    elif stage=='weighted_induction' and not row['commutative']:
        from weighted_induction import certificate
        return certificate(R)
    elif stage=='general_induction' and row['commutative']:
        from oriented_extension import certificate
        return certificate(R,height=6,timeout=90,integral=True)
    return None

def worker(task):
    stage,label,budget,row,cached,positive=task
    start=time.monotonic(); out={'id':row['id'],'m':row['m'],'stage':stage,'status':'survives'}
    signal.signal(signal.SIGALRM,stop); signal.alarm(budget)
    try:
        if stage=='general_induction' and cached is None and not positive and not row.get('_general_discover',True):
            out.update(status='retained_undecided',diagnostic='Previously unresolved tensor retained; general discovery targets the new source frontier, and the earliest residual receives the advanced passes.')
            return out
        if stage in ('dimension_order','character','tensor_rotation','modular') and not positive and not row.get('_advanced_repeat',True):
            out.update(status='retained_undecided',diagnostic='Earlier higher-multiplicity residual retained; this advanced discovery pass targets the source frontier and the smallest unresolved multiplicity only.')
            return out
        if positive and stage in ('weighted_induction','general_induction','dimension_order','character','tensor_rotation','modular'):
            out['diagnostic']='Exact positive model already available; no expensive negative search.'
            return out
        if stage in ('dimension_order','character','tensor_rotation','modular'):
            import advanced_criteria
            out['eligibility']=advanced_criteria.eligibility(row['N'],stage,height=6)
            if not out['eligibility']['eligible']:
                out['status']='ineligible'
                out['diagnostic']=out['eligibility']['reason']
                return out
            cert=cached or advanced_criteria.general_certificate(row['N'],mode=stage,timeout=60,height=6)
        else:cert=cached or discover(stage,row)
        if cert is not None:
            from check import verify
            # Certificate checking cannot use floating-point optimization.
            import scipy.optimize
            oldlp,oldmilp=scipy.optimize.linprog,scipy.optimize.milp
            def forbidden(*args,**kwargs):raise RuntimeError('numerical optimization is forbidden in exact checking')
            scipy.optimize.linprog=scipy.optimize.milp=forbidden
            try:verify(row['N'],cert)
            finally:scipy.optimize.linprog,scipy.optimize.milp=oldlp,oldmilp
            out.update(status='excluded',certificate=cert,exact_checked=True,witness_source='retained' if cached else 'discovered')
    except (DiscoveryBudget,TimeoutError,subprocess.TimeoutExpired) as exc:
        out.update(status='budget_exhausted',diagnostic=f'{type(exc).__name__}: {exc}')
        out['budget']={'type':type(exc).__name__,**{name:getattr(exc,name) for name in ('seconds','nodes','frames','timeout') if hasattr(exc,name)}}
    except Exception as exc:
        out.update(status='error',diagnostic=f'{type(exc).__name__}: {exc}',traceback=traceback.format_exc())
    finally:
        signal.alarm(0);out['seconds']=time.monotonic()-start
    return out

def hard_worker(task):
    """A wall-clock watchdog outside the numerical process and its children."""
    stage,label,budget,row,cached,positive=task;start=time.monotonic()
    cmd=[sys.executable]+([] if __debug__ else ['-O'])+[str(Path(__file__).resolve()),'--worker']
    with subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE,text=True,start_new_session=True) as process:
        try:
            stdout,stderr=process.communicate(json.dumps(task,separators=(',',':')),timeout=budget)
        except subprocess.TimeoutExpired:
            try:os.killpg(process.pid,signal.SIGKILL)
            except ProcessLookupError:pass
            stdout,stderr=process.communicate()
            return {'id':row['id'],'m':row['m'],'stage':stage,'status':'budget_exhausted',
                    'seconds':time.monotonic()-start,'budget':{'type':'hard_process_deadline','seconds':budget},
                    'diagnostic':'The independent process-group watchdog expired; partial output is not a certificate.'}
        if process.returncode!=0:
            return {'id':row['id'],'m':row['m'],'stage':stage,'status':'error',
                    'seconds':time.monotonic()-start,'returncode':process.returncode,
                    'diagnostic':'Unexpected classification subprocess exit','stderr':stderr[-12000:]}
        try:
            result=json.loads(stdout)
            if not isinstance(result,dict):raise ValueError('worker result must be an object')
            if result.get('id')!=row['id'] or result.get('stage')!=stage or result.get('m')!=row['m']:
                raise ValueError('worker result identity mismatch')
            if result.get('status') not in ('excluded','survives','budget_exhausted','error','ineligible','retained_undecided'):
                raise ValueError('worker result has an unknown status')
            if result['status']=='excluded' and (result.get('exact_checked') is not True or not isinstance(result.get('certificate'),dict)):
                raise ValueError('worker supplied an unchecked or malformed exclusion')
        except (ValueError,TypeError) as exc:
            return {'id':row['id'],'m':row['m'],'stage':stage,'status':'error',
                    'seconds':time.monotonic()-start,'diagnostic':'Malformed worker result: '+str(exc),
                    'stderr':stderr[-12000:]}
        result['process_wall_seconds']=time.monotonic()-start
        result['hard_deadline_seconds']=budget
        return result

def retained_stage(kind):
    if kind=='noncommuting_field_automorphisms':return 'field_automorphisms'
    if kind in {s[0] for s in STAGES}:return kind
    return 'general_induction'

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--jobs',type=int,default=4)
    ap.add_argument('--resume',action='store_true',help='reuse completed stages only when the source census matches')
    ap.add_argument('--advanced-all',action='store_true',help='also repeat advanced discovery on all older unresolved multiplicities')
    a=ap.parse_args()
    from import_repository import verify_source
    from existence import positive_registry
    rows=json.loads((P/'data/census.json').read_text());source=verify_source(rows)
    old=json.loads((P/'data/decisions.json').read_text());positive=positive_registry()
    witnesses={r['id']:r['certificate'] for r in old if r['status']=='excluded'}
    earliest=min((r['m'] for r in old if r['status']=='unresolved'),default=max(source['counts']))
    advanced_multiplicities=sorted(source['counts']) if a.advanced_all else sorted({max(source['counts']),earliest})
    remaining={r['id']:r for r in rows};exclusions={};stages=[]
    base=P/'verification/classification';base.mkdir(parents=True,exist_ok=True)
    ledgerpath=base/'attempts.jsonl';stagepath=base/'stages.json'
    fingerprint=hashlib.sha256((P/'data/census.json').read_bytes()).hexdigest()
    if a.resume and stagepath.exists():
        saved=json.loads(stagepath.read_text())
        if saved['census_sha256']!=fingerprint:raise ValueError('resume census changed')
        stages=saved['stages']
        for stage_record in stages:stage_record.setdefault('jobs',saved['jobs'])
        completed={z['stage'] for z in stages}
        for line in ledgerpath.read_text().splitlines():
            z=json.loads(line)
            if z['stage'] in completed and z['status']=='excluded':
                exclusions[z['id']]=z;remaining.pop(z['id'],None)
    else:
        ledgerpath.write_text('');completed=set()
    for stage,label,budget in STAGES:
        if stage in completed:continue
        start=time.monotonic();active=list(remaining.values());outputs=[]
        print('START',stage,'rings',len(active),flush=True)
        if stage=='zero_spectrum':
            import zero_spectrum
            batchstart=time.monotonic();certs=zero_spectrum.batch([r['N'] for r in active]);elapsed=time.monotonic()-batchstart
            for row,cert in zip(active,certs):
                z={'id':row['id'],'m':row['m'],'stage':stage,'status':'excluded' if cert else 'survives','seconds':elapsed/len(active)}
                if cert:z.update(certificate=cert,exact_checked=True,witness_source='discovered')
                outputs.append(z)
        else:
            tasks=[]
            progress=base/(stage+'.progress.jsonl')
            recovered={}
            if a.resume and progress.exists():
                lines=progress.read_text().splitlines()
                for position,line in enumerate(lines):
                    try:z=json.loads(line)
                    except json.JSONDecodeError:
                        if position==len(lines)-1:break
                        raise
                    if z.get('census_sha256')!=fingerprint or z.get('stage')!=stage or z.get('id') not in remaining:
                        raise ValueError('partial checkpoint does not match its source/stage/tensor')
                    if z.get('status')=='excluded' and not z.get('exact_checked'):
                        raise ValueError('partial checkpoint contains an unchecked exclusion')
                    recovered[z['id']]=z
                outputs.extend(recovered.values())
            for row in active:
                if row['id'] in recovered:continue
                c=witnesses.get(row['id']);c=c if c and (retained_stage(c['kind'])==stage or stage in ('general_induction','retained_completion')) else None
                payload=dict(row,_advanced_repeat=row['m'] in advanced_multiplicities,_general_discover=row['m']==max(source['counts']))
                tasks.append((stage,label,budget,payload,c,row['id'] in positive))
            expensive=stage in ('general_induction','dimension_order','character','tensor_rotation','modular','retained_completion')
            executor=ThreadPoolExecutor if expensive else ProcessPoolExecutor
            operation=hard_worker if expensive else worker
            with executor(max_workers=a.jobs) as ex,progress.open('w') as checkpoint:
                for z in recovered.values():checkpoint.write(json.dumps(z,separators=(',',':'))+'\n')
                checkpoint.flush()
                if stage in ('rank_two','dnumber'):
                    results=ex.map(worker,tasks,chunksize=8)
                else:
                    pending=[ex.submit(operation,task) for task in tasks]
                    results=(future.result() for future in as_completed(pending))
                for ix,z in enumerate(results):
                    z['census_sha256']=fingerprint
                    outputs.append(z)
                    checkpoint.write(json.dumps(z,separators=(',',':'))+'\n');checkpoint.flush()
                    if z['status'] in ('error','budget_exhausted') or (stage=='general_induction' and (ix+1)%10==0):
                        print(stage,ix+1,'/',len(active),z['id'],z['status'],z.get('diagnostic',''),flush=True)
        with ledgerpath.open('a') as f:
            for z in outputs:
                f.write(json.dumps(z,separators=(',',':'))+'\n')
                if z['status']=='excluded':
                    if z['id'] in positive:raise ValueError('positive/negative contradiction '+z['id'])
                    exclusions[z['id']]=z;remaining.pop(z['id'],None)
        per={str(m):{'entered':sum(r['m']==m for r in active),
                    'removed':sum(z['m']==m and z['status']=='excluded' for z in outputs),
                    'remaining':sum(r['m']==m for r in remaining.values())} for m in sorted(source['counts'])}
        report={'stage':stage,'label':label,'jobs':a.jobs,'entered':len(active),'removed':sum(z['status']=='excluded' for z in outputs),
                'remaining':len(remaining),'wall_seconds':time.monotonic()-start,
                'worker_seconds':sum(z['seconds'] for z in outputs),
                'errors':sum(z['status']=='error' for z in outputs),
                'budget_exhausted':sum(z['status']=='budget_exhausted' for z in outputs),'by_multiplicity':per}
        stages.append(report)
        stagepath.write_text(json.dumps({'source':source,'census_sha256':fingerprint,
            'python':platform.python_version(),'jobs':a.jobs,'advanced_multiplicities':advanced_multiplicities,'stages':stages},indent=2)+'\n')
        checkpoint_path=base/(stage+'.progress.jsonl')
        if checkpoint_path.exists():checkpoint_path.unlink()
        print('DONE',json.dumps(report),flush=True)
        # A completed-stage checkpoint also contains every accepted proof.
        (P/'certificates/classification.jsonl').write_text(''.join(json.dumps(exclusions[r['id']],separators=(',',':'))+'\n' for r in rows if r['id'] in exclusions))
    residual=[r['id'] for r in remaining.values() if r['id'] not in positive]
    missing_retained=sorted(set(witnesses)-set(exclusions))
    summary={'source':source,'census_sha256':fingerprint,'stages':len(stages),'excluded':len(exclusions),'positive':len(positive),'unresolved':len(residual),'unresolved_ids':residual,
             'advanced_multiplicities':advanced_multiplicities,'missing_retained_exclusions':missing_retained,
             'certificates_sha256':hashlib.sha256((P/'certificates/classification.jsonl').read_bytes()).hexdigest(),
             'errors':sum(s['errors'] for s in stages),'budget_exhausted':sum(s['budget_exhausted'] for s in stages),
             'interpretation':'Errors and exhausted discovery budgets are retained as diagnostics, never nonexistence certificates.'}
    (base/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))
    if missing_retained:
        raise RuntimeError('Previously certified exclusions still await a complete exact check: '+', '.join(missing_retained))

if __name__=='__main__':
    if '--worker' in sys.argv:
        print(json.dumps(worker(json.load(sys.stdin)),separators=(',',':')))
    else:main()
