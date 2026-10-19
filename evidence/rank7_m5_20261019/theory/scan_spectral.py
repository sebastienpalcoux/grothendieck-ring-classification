import json,sys,time,signal,concurrent.futures
from pathlib import Path
P=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(P/'supplements/rank6/software'))
import new_module_spectral as m

def timeout(a,b):raise TimeoutError('spectral module budget 25s')
def job(r):
 start=time.monotonic();signal.signal(signal.SIGALRM,timeout);signal.alarm(25)
 try:
  c=m.certificate(r['tensor']);status='survives'
  if c:
   signal.alarm(25);m.verify(r['tensor'],c);status='excluded'
  out={'id':r['id'],'status':status,'certificate':c}
 except Exception as e:out={'id':r['id'],'status':'incomplete','error':str(e)}
 finally:signal.alarm(0)
 out['seconds']=time.monotonic()-start
 return out
if __name__=='__main__':
 rows=json.load(open(P/'supplements/rank7/output/m5/survivors.json'))
 with concurrent.futures.ProcessPoolExecutor(max_workers=2) as ex,Path(__file__).with_name('spectral_module_results.jsonl').open('w') as f:
  for out in ex.map(job,rows):
   f.write(json.dumps(out)+'\n');f.flush();print(out['id'],out['status'],round(out['seconds'],2),flush=True)
