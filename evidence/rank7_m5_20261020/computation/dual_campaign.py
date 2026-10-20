"""Bounded discovery/replay using exact dual-variable substitution."""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[key]='1'
import argparse,hashlib,json,signal,subprocess,sys,time
from pathlib import Path
import deep_campaign as dc
HERE=Path(__file__).resolve().parent


def worker(args):
    dc.install_runtime(args.budget-30,fast=not args.replay)
    import dual_reduction as dr
    dr.install(discovery=not args.replay)
    start=time.monotonic()
    if args.replay:
        candidate=json.loads(args.replay.read_text())
        for relative,digest in candidate['sources'].items():
            if hashlib.sha256((dc.ROOT/relative).read_bytes()).hexdigest()!=digest:
                raise ValueError('changed bound proof source '+relative)
        row=next(r for r in json.loads(dc.LEDGER.read_text()) if r['id']==candidate['id'])
        row['certificate']=candidate['certificate']
        from verify_m5 import verify_new
        verify_new(row)
        result={'status':'PASS','id':row['id'],'candidate_sha256':hashlib.sha256(args.replay.read_bytes()).hexdigest(),
                'optimized_python':not __debug__,'seconds':time.monotonic()-start,
                'method':'All original retained columns checked against a full lifted integer ray; no numerical optimization or dual quotient used in replay.'}
        target=args.replay.with_name(args.replay.stem+('_optimized' if not __debug__ else '_normal')+'_replay.json')
    else:
        for name in ('dual_reduction_controls.json','dual_reduction_controls_optimized.json'):
            controls=json.loads((HERE/name).read_text())
            if controls['status']!='PASS' or controls['source_hashes']!=dr.source_hashes():
                raise ValueError('stale dual elimination controls')
        row=next(r for r in json.loads(dc.LEDGER.read_text()) if r['id']==args.ring)
        def progress(ix,ep):dc.emit('branch',index=ix,indicators=ep)
        import character_induction as ci
        pseudo=ci.certificate(row['tensor'],args.height,progress)
        cert=ci.lift_general(row['tensor'],pseudo,timeout=args.budget-30) if pseudo else None
        result={'id':row['id'],'stage':'dual_character','height':args.height,'status':'candidate_exclusion' if cert else 'no_certificate',
                'scope':'unreviewed_candidate' if cert else 'no_conclusion','certificate':cert,
                'seconds':time.monotonic()-start,'sources':dr.source_hashes(),
                'accepted_ledger_sha256':dc.PIN}
        target=HERE/(args.ring+'_dual_character_h'+str(args.height)+'.json')
    target.write_text(json.dumps(result,separators=(',',':'))+'\n')
    dc.emit('result',**{k:v for k,v in result.items() if k not in ('certificate','sources')})


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--ring',default='R7_5_5039');ap.add_argument('--height',type=int,default=3)
    ap.add_argument('--budget',type=int,default=1200);ap.add_argument('--replay',type=Path)
    ap.add_argument('--worker',action='store_true');args=ap.parse_args()
    if hashlib.sha256(dc.LEDGER.read_bytes()).hexdigest()!=dc.FRONTIER_SHA:raise ValueError('source frontier changed')
    if args.worker:return worker(args)
    modes=[False,True] if args.replay else [False]
    for optimized in modes:
        stem=args.replay.stem+('_optimized' if optimized else '_normal') if args.replay else args.ring+'_dual_character_h'+str(args.height)
        target=HERE/(stem+'.log')
        with target.open('w') as out:
            command=[sys.executable]+(['-O'] if optimized else [])+[str(Path(__file__).resolve()),'--worker','--budget',str(args.budget),'--height',str(args.height),'--ring',args.ring]
            if args.replay:command+=['--replay',str(args.replay.resolve())]
            process=subprocess.Popen(command,stdout=out,stderr=out,text=True,start_new_session=True)
            try:code=process.wait(timeout=args.budget)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid,signal.SIGKILL);process.wait()
                dc.emit('budget_exhausted',id=args.ring,stage='dual_character',height=args.height,budget=args.budget)
                return
        if code:raise RuntimeError('worker failed; see '+str(target))
        dc.emit('worker_complete',log=target.name)


if __name__=='__main__':main()
