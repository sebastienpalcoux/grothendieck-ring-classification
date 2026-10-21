"""One serial queue for bounded global-convex candidate attempts."""
from pathlib import Path
import argparse,json,os,signal,subprocess,sys,time
HERE=Path(__file__).resolve().parent;BASE=HERE.parent
DEFAULT=[903,921,925,901,1463,926,982,985,986,1615,1617,1660,1661,1739]

def save(path,data):
    path.parent.mkdir(parents=True,exist_ok=True);temp=path.with_suffix('.tmp');temp.write_text(json.dumps(data,separators=(',',':'))+'\n');temp.replace(path)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--ids',type=int,nargs='*',default=DEFAULT);ap.add_argument('--budget',type=int,default=360);ap.add_argument('--memory-mb',type=int,default=3200);args=ap.parse_args()
    source={r['id']:r for r in json.loads((BASE/'pipeline/census_m3.json').read_text())};results=[]
    for index in args.ids:
        rid=f'R8_3_{index}';generic=index in (901,1463)
        script=BASE/'noncommutative/general_global_convex.py' if generic else HERE/'global_induction.py'
        dest=BASE/'noncommutative'/f'general_global_convex_{rid}.json' if generic else HERE/'advanced/global_family'/(rid+'.json')
        if dest.exists() and json.loads(dest.read_text()).get('status') in ('excluded','no_conclusion','pseudo_unitary_only'):
            results.append(json.loads(dest.read_text()));continue
        cmd=[sys.executable,str(script),'--ring',rid,'--height','4']+(['--q','3','--r','5'] if generic else ['--tag','global_family'])
        env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',RANK8_GLOBAL_MEMORY_MB=str(args.memory_mb));start=time.monotonic();print('START',rid,flush=True)
        process=subprocess.Popen(cmd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,start_new_session=True,env=env)
        try:
            output,_=process.communicate(timeout=args.budget)
            if dest.exists():row=json.loads(dest.read_text())
            else:row={'id':rid,'tensor_sha256':source[rid]['tensor_sha256'],'status':'error'}
            if process.returncode:
                row.update(status='resource_bound' if any(word in output for word in ('MemoryError','bad_alloc','Cannot allocate memory')) else 'error',returncode=process.returncode,stdout=output[-16000:])
        except subprocess.TimeoutExpired:
            os.killpg(process.pid,signal.SIGKILL);output,_=process.communicate()
            row=json.loads(dest.read_text()) if dest.exists() else {'id':rid,'tensor_sha256':source[rid]['tensor_sha256']}
            row.update(status='timeout',budget_seconds=args.budget,stdout=output[-16000:])
        row['memory_limit_mb']=args.memory_mb;row['seconds']=round(time.monotonic()-start,3);save(dest,row);results.append(row)
        save(HERE/'global_family_attempts.json',{'planned_ids':[f'R8_3_{i}' for i in args.ids],'attempts':results,'budget_seconds':args.budget})
        print(rid,row['status'],row['seconds'],flush=True)
if __name__=='__main__':main()
