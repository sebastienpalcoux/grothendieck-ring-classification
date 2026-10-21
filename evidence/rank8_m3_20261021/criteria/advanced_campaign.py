"""Bounded advanced search with completed exact proofs separated from attempts."""
from pathlib import Path
import argparse,concurrent.futures,hashlib,json,os,signal,subprocess,sys,time,traceback
for name in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[name]='1'
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path[:0]=[str(ROOT/'supplements/rank8/experimental_signed'),str(ROOT/'supplements/rank8/software'),str(HERE.parent/'noncommutative')]

def save(path,value):
    path.parent.mkdir(parents=True,exist_ok=True);temp=path.with_suffix('.tmp');temp.write_text(json.dumps(value,separators=(',',':'))+'\n');temp.replace(path)

def worker(row,mode,height,signed_timeout,dest):
    import advanced_criteria as advanced,rank8_signed_bridge
    rank8_signed_bridge.install();start=time.monotonic()
    out={'id':row['id'],'tensor_sha256':row['tensor_sha256'],'mode':mode,'height':height,'status':'no_conclusion','scope':'general_complex_fusion_category'}
    try:
        info=advanced.eligibility(row['tensor'],mode,height);out['eligibility']=info
        if info['eligible']:
            c=advanced.general_certificate(row['tensor'],mode=mode,timeout=signed_timeout,height=height)
            if c:
                c=json.loads(json.dumps(c));advanced.verify(row['tensor'],c);out.update(status='excluded',certificate=c,exact_checked=True)
        else:out['status']='ineligible'
    except Exception as exc:out.update(status='error',error=repr(exc),traceback=traceback.format_exc())
    out['seconds']=round(time.monotonic()-start,3);save(dest,out);print(row['id'],out['status'],out['seconds'],flush=True)

def task(row,args):
    dest=HERE/'advanced'/args.tag/(row['id']+'.json')
    if dest.exists() and not args.overwrite:return json.loads(dest.read_text())
    accepted=HERE/'accepted_exclusions.json'
    if accepted.exists() and not args.overwrite and any(r['id']==row['id'] for r in json.loads(accepted.read_text())):
        return {'id':row['id'],'status':'covered_by_verified_certificate'}
    start=time.monotonic();cmd=[sys.executable,str(Path(__file__).resolve()),'--worker',row['id'],'--mode',args.mode,'--height',str(args.height),'--signed-timeout',str(args.signed_timeout),'--tag',args.tag]
    process=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,start_new_session=True)
    try:
        output,_=process.communicate(timeout=args.budget)
        if process.returncode==0 and dest.exists():return json.loads(dest.read_text())
        out={'id':row['id'],'tensor_sha256':row['tensor_sha256'],'mode':args.mode,'status':'error','returncode':process.returncode,'stdout':output[-12000:]}
    except subprocess.TimeoutExpired:
        os.killpg(process.pid,signal.SIGKILL);output,_=process.communicate()
        out={'id':row['id'],'tensor_sha256':row['tensor_sha256'],'mode':args.mode,'status':'timeout','budget_seconds':args.budget,'stdout':output[-12000:]}
    out['seconds']=round(time.monotonic()-start,3);save(dest,out);return out

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--worker');ap.add_argument('--mode',choices=['dimension_order','character','tensor_rotation','modular'],default='dimension_order');ap.add_argument('--height',type=int,default=6);ap.add_argument('--signed-timeout',type=int,default=120);ap.add_argument('--budget',type=int,default=240);ap.add_argument('--jobs',type=int,default=4);ap.add_argument('--tag');ap.add_argument('--ids',nargs='*');ap.add_argument('--overwrite',action='store_true');args=ap.parse_args();args.tag=args.tag or args.mode
    rows=json.loads((HERE.parent/'pipeline/census_m3.json').read_text());byid={r['id']:r for r in rows}
    if args.worker:return worker(byid[args.worker],args.mode,args.height,args.signed_timeout,HERE/'advanced'/args.tag/(args.worker+'.json'))
    if args.ids:active=[byid[rid] for rid in args.ids]
    else:
        source=HERE/'survivors_after_subrings.json';active=json.loads((source if source.exists() else HERE.parent/'pipeline/survivors_m3.json').read_text())
        excluded=set()
        for source in [HERE/'quadratic_compression.json',HERE/'accepted_exclusions.json']:
            if source.exists():
                data=json.loads(source.read_text());excluded.update(r['id'] for r in (data if isinstance(data,list) else data['records']))
        models=HERE.parent/'models/consolidated_models.json'
        if models.exists():excluded.update(r['id'] for r in json.loads(models.read_text()))
        active=[r for r in active if r['id'] not in excluded and r['commutative']]
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
        for out in pool.map(lambda row:task(row,args),active):print(out['id'],out['status'],out.get('seconds'),flush=True)
if __name__=='__main__':main()
