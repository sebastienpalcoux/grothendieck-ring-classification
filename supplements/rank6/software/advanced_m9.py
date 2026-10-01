"""Source-bound extra M9 criteria; bounded discovery is never exclusion.

Outputs are separate from the release ledger. Each successful certificate is
replayed with numerical optimization forbidden. No inherited files are edited.
"""
import os
for name in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):
    os.environ[name]='1'
import argparse, collections, hashlib, importlib, json, signal, subprocess, sys
import time, traceback
from concurrent.futures import ThreadPoolExecutor,wait,FIRST_COMPLETED
from pathlib import Path

DIRECT={
 'trace_ideal':('new_trace_ideal',60),
 'ramified_field':('new_ramified_signed',60),
 'ramified_signed':('new_ramified_signed',180),
 'biquadratic':('new_biquadratic_trace',120),
 'inert_spectrum':('round3_arithmetic',120),
 'noncommutative_spectrum':('round3_noncommutative',180),
 'full_morita':('full_morita_gram',180),
 'c4_associator':('round3_smallest',300),
}
PU={
 'stabilizer':('stabilizer_rotation','general_stabilizer_rotation',600),
 'higher_stabilizer':('stabilizer_rotation_higher','general_stabilizer_rotation_higher',600),
 'integral_morita':('round3_integral_morita','general_integral_morita_rotation',600),
 'low_verlinde':('round3_verlinde','general_low_verlinde_restriction',600),
 'cyclotomic_stabilizer':('cyclotomic_stabilizer_trace','general_cyclotomic_stabilizer_trace',600),
}
SPECIAL={'gauss_family':300,'cyclotomic_extended':60}

def sha(value):
    return hashlib.sha256(json.dumps(value,separators=(',',':'),sort_keys=True).encode()).hexdigest()

def worker(task):
    root,row,stage=task
    sys.path.insert(0,str(Path(root)/'software'))
    out=dict(id=row['id'],m=row['m'],stage=stage,status='survives',tensor_sha256=sha(row['N']))
    R=row['N'];comm=all(R[i][j]==R[j][i] for i in range(len(R)) for j in range(len(R)))
    started=time.monotonic()
    try:
        if stage in DIRECT:
            mod=importlib.import_module(DIRECT[stage][0]);out['module']=mod.__name__
            if stage=='noncommutative_spectrum':
                if comm:out.update(status='ineligible',diagnostic='commutative tensor');return out
                hyp=mod.hypotheses(R,allow_even_commutators=True)
                if hyp is None:out.update(status='ineligible',diagnostic='weighted quadratic spectrum gate');return out
                cs=None
                if hyp[1]['requires_commutative_sector_exclusion']:
                    import round3_commutative_sector
                    cs=round3_commutative_sector.commutative_signed_sector_certificate(R,seconds=60)
                    if cs is None:out.update(diagnostic='commutative signed sector survives');return out
                cert=mod.certificate(R,commutative_sector=cs)
            elif not comm:
                out.update(status='ineligible',diagnostic='commutative tensor required');return out
            elif stage=='ramified_field':cert=mod.field_certificate(R)
            elif stage=='ramified_signed':cert=mod.certificate(R,pseudo=None,seconds=60)
            elif stage=='full_morita':cert=mod.certificate(R,node_limit=2000000)
            elif stage=='c4_associator':
                if mod.family(R) is None:out.update(status='ineligible',diagnostic='uniform C4 quadratic family absent');return out
                cert=mod.certificate(R,height=4)
            elif stage=='biquadratic':
                if mod.tensor_data(R) is None:out.update(status='ineligible',diagnostic='biquadratic trace family absent');return out
                cert=mod.certificate(R)
            elif stage=='inert_spectrum':
                if mod.hypotheses(R) is None:out.update(status='ineligible',diagnostic='local quadratic signed-spectrum gate');return out
                cert=mod.certificate(R,pseudo=None)
            else:cert=mod.certificate(R,pseudo=None,seconds=60)
            verifier=mod.verify
        elif stage=='cyclotomic_extended':
            if not comm:
                out.update(status='ineligible',diagnostic='commutative tensor required');return out
            import exact
            from rings import matrices,t
            polys=[m.charpoly(t).as_poly() for m in matrices(R)]
            cert=exact.cyclotomic_failure(polys,limit=10000)
            from check import verify as verifier
            out.update(module='exact',prime_search_limit=10000)
        elif stage=='gauss_family':
            import new_gauss_family as mod
            out['module']=mod.__name__
            if mod.identify(R) is None:
                out.update(status='ineligible',diagnostic='full Gauss family tensor absent');return out
            pseudo=mod.certificate(R)
            if pseudo is None:return out
            out['pseudo_certificate']=pseudo
            import new_trace_ideal,new_ramified_signed,round3_arithmetic
            cert=None
            for reduction_module in (new_trace_ideal,new_ramified_signed,round3_arithmetic):
                candidate=reduction_module.certificate(R,pseudo=pseudo)
                if candidate is not None:cert=candidate;verifier=reduction_module.verify;break
            if cert is None:
                import character_induction,oriented_extension
                cert=character_induction.lift_general(R,pseudo,timeout=90)
                verifier=oriented_extension.verify
            if cert is None:
                out.update(status='pseudo_only',diagnostic='Gauss exclusion lacks complete general reduction');return out
        elif stage in PU:
            modname,kind,_=PU[stage];mod=importlib.import_module(modname);out['module']=modname
            if not comm:out.update(status='ineligible',diagnostic='commutative tensor required');return out
            from involution_module import invs
            if stage!='low_verlinde' and not invs(R):
                out.update(status='ineligible',diagnostic='no invertible involution');return out
            if stage=='cyclotomic_stabilizer':pseudo=mod.certificate(R)
            else:pseudo=mod.certificate(R,height=3 if stage in ('stabilizer','higher_stabilizer') else 6)
            if pseudo is None:return out
            # A failed or timed-out reduction never promotes PU nonexistence.
            out['pseudo_certificate']=pseudo
            if stage=='higher_stabilizer':
                from rings import Characters
                reduction={'kind':'two_fp_values'} if len(set(Characters(R).fp()[2]))==2 else None
            else:reduction=None
            if reduction is None:
                import galois_pseudo_reduction
                reduction=galois_pseudo_reduction.certificate(R,timeout=120)
            if reduction is None:
                out.update(status='pseudo_only',diagnostic='complete general-to-PU reduction unavailable');return out
            cert=dict(kind=kind,version=1,scope='general',reduction=reduction,pseudo=pseudo)
            verifier=mod.verify_general
        else:raise ValueError('unknown stage '+stage)
        if cert is not None:
            import scipy.optimize as opt
            def denied(*a,**kw):raise RuntimeError('numerical optimization forbidden in exact replay')
            old=(opt.linprog,opt.milp);opt.linprog=opt.milp=denied
            try:verifier(R,cert)
            finally:opt.linprog,opt.milp=old
            out.pop('pseudo_certificate',None)
            out.update(status='excluded',certificate=cert,exact_checked=True,
                       verifier=verifier.__module__+'.'+verifier.__name__,scope='general')
    except (TimeoutError,subprocess.TimeoutExpired) as exc:
        out.update(status='budget_exhausted',diagnostic=str(exc))
    except Exception as exc:
        if type(exc).__name__=='Ineligible':out.update(status='ineligible',diagnostic=str(exc))
        elif type(exc).__name__=='Survives':out.update(status='survives',diagnostic=str(exc))
        else:out.update(status='error',diagnostic=type(exc).__name__+': '+str(exc),traceback=traceback.format_exc())
    finally:out['seconds']=time.monotonic()-started
    return out

def bounded(task,seconds):
    start=time.monotonic();root,row,stage=task
    with subprocess.Popen([sys.executable,str(Path(__file__).resolve()),'--worker'],
          stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,start_new_session=True) as proc:
        try:
            stdout,stderr=proc.communicate(json.dumps(task),timeout=seconds)
            if proc.returncode:raise RuntimeError('worker exit '+str(proc.returncode)+': '+stderr[-3000:])
            result=json.loads(stdout)
            if result.get('id')!=row['id'] or result.get('stage')!=stage:raise ValueError('worker identity mismatch')
            if result['status']=='excluded' and not result.get('exact_checked'):raise ValueError('unchecked worker exclusion')
        except subprocess.TimeoutExpired:
            os.killpg(proc.pid,signal.SIGKILL);proc.communicate()
            result=dict(id=row['id'],m=row['m'],stage=stage,status='budget_exhausted',
                        diagnostic='independent process-group deadline; no exclusion',tensor_sha256=sha(row['N']))
        except Exception as exc:
            result=dict(id=row['id'],m=row['m'],stage=stage,status='error',diagnostic=str(exc),tensor_sha256=sha(row['N']))
    result.update(wall_seconds=time.monotonic()-start,deadline_seconds=seconds)
    return result

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root',type=Path,required=True);ap.add_argument('--input',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True);ap.add_argument('--jobs',type=int,default=2)
    ap.add_argument('--seconds',type=int,default=840);ap.add_argument('--stages',nargs='+',default=list(DIRECT))
    ap.add_argument('--reuse',type=Path,action='append',default=[],help='Reuse source-bound attempts only for current input tensors')
    args=ap.parse_args();start=time.monotonic();end=start+args.seconds
    if not 1<=args.seconds<=840 or args.jobs<1:ap.error('seconds in 1..840; positive jobs')
    if any(s not in DIRECT and s not in PU and s not in SPECIAL for s in args.stages):ap.error('unknown stage')
    rows=json.loads(args.input.read_text());byid={r['id']:r for r in rows}
    if any(r['m']!=9 for r in rows):raise ValueError('new multiplicity-nine tensors only')
    args.output.mkdir(parents=True,exist_ok=True);path=args.output/'attempts.jsonl'
    modules={x[0] for x in DIRECT.values()}|{x[0] for x in PU.values()}|{
        'exact','rings','check','proofs','induction','extension','oriented_extension','oriented_signed',
        'character_induction','higher_traces','module_dual_gram','new_signed_csp','signed',
        'new_gauss_family','galois_pseudo_reduction','round3_commutative_sector'}
    source_hashes={m+'.py':hashlib.sha256((args.root/'software'/(m+'.py')).read_bytes()).hexdigest() for m in sorted(modules)}
    identity=dict(input_sha256=sha(rows),input_count=len(rows),input_ids=[r['id'] for r in rows],
                  census_sha256=hashlib.sha256((args.root/'data/census.json').read_bytes()).hexdigest(),software_directory='software',implementation_sha256=source_hashes,
                  criteria_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    manifest=args.output/'input_manifest.json'
    if manifest.exists() and json.loads(manifest.read_text())!=identity:raise ValueError('source or driver changed; use fresh output')
    manifest.write_text(json.dumps(identity,indent=2)+'\n')
    completed={};excluded={}
    reusable={}
    for directory in args.reuse:
        prior=json.loads((directory/'input_manifest.json').read_text())
        for key in ('census_sha256','criteria_sha256','implementation_sha256'):
            if prior[key]!=identity[key]:raise ValueError('reusable attempt source mismatch: '+key)
        for line in (directory/'attempts.jsonl').read_text().splitlines():
            z=json.loads(line)
            if z['id'] not in byid:continue
            if z['tensor_sha256']!=sha(byid[z['id']]['N']):raise ValueError('reusable tensor mismatch')
            if z['status']=='excluded' and not z.get('exact_checked'):raise ValueError('unchecked reusable exclusion')
            reusable[z['id'],z['stage']]=dict(z,reused_from=str(directory.relative_to(args.root)) if directory.is_relative_to(args.root) else str(directory))
    if path.exists():
        for line in path.read_text().splitlines():
            z=json.loads(line)
            if z['id'] not in byid or z['tensor_sha256']!=sha(byid[z['id']]['N']):raise ValueError('checkpoint tensor mismatch')
            completed[z['id'],z['stage']]=z
            if z['status']=='excluded':excluded[z['id']]=z
    with path.open('a') as stream:
        for stage in args.stages:
            budget=(DIRECT[stage][1] if stage in DIRECT else PU[stage][2] if stage in PU else SPECIAL[stage])
            for row in rows:
                key=row['id'],stage
                if row['id'] in excluded or key in completed or key not in reusable:continue
                z=reusable[key];completed[key]=z
                if z['status']=='excluded':excluded[z['id']]=z
                stream.write(json.dumps(z,separators=(',',':'))+'\n');stream.flush()
            tasks=iter([(str(args.root.resolve()),r,stage) for r in rows if r['id'] not in excluded and (r['id'],stage) not in completed])
            with ThreadPoolExecutor(max_workers=args.jobs) as pool:
                pending={}
                def submit():
                    if time.monotonic()+budget+5>=end:return
                    task=next(tasks,None)
                    if task is not None:pending[pool.submit(bounded,task,budget)]=task
                for _ in range(args.jobs):submit()
                while pending:
                    done,_=wait(pending,return_when=FIRST_COMPLETED)
                    for future in done:
                        pending.pop(future);z=future.result();completed[z['id'],stage]=z
                        if z['status']=='excluded':excluded[z['id']]=z
                        stream.write(json.dumps(z,separators=(',',':'))+'\n');stream.flush()
                        print(z['id'],stage,z['status'],round(z['wall_seconds'],2),flush=True);submit()
            if time.monotonic()+budget+5>=end:break
    certificate_text=''.join(json.dumps(excluded[k],separators=(',',':'))+'\n' for k in sorted(excluded))
    complete=all(r['id'] in excluded or all((r['id'],s) in completed for s in args.stages) for r in rows)
    summary=dict(identity,attempts=len(completed),excluded_ids=sorted(excluded),excluded=len(excluded),complete=complete,
                 requested_stages=args.stages,certificates_sha256=hashlib.sha256(certificate_text.encode()).hexdigest(),
                 statuses=dict(collections.Counter(z['status'] for z in completed.values())),
                 stage_statuses={s:dict(collections.Counter(z['status'] for z in completed.values() if z['stage']==s)) for s in args.stages},
                 unresolved_ids=[r['id'] for r in rows if r['id'] not in excluded],wall_seconds=time.monotonic()-start)
    (args.output/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    (args.output/'certificates.jsonl').write_text(certificate_text)
    print(json.dumps(summary,indent=2),flush=True)

if __name__=='__main__':
    if '--worker' in sys.argv:print(json.dumps(worker(json.load(sys.stdin))))
    else:main()
