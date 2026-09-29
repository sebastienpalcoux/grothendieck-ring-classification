import sys,json,time,signal
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'software'))
import tensor_rotation as T
rows=json.load(open(ROOT/'data/unresolved_tensors.json'));out=[]
def end(*_):raise TimeoutError('45-second per-input exploratory budget')
signal.signal(signal.SIGALRM,end)
for r in rows:
 name=r['id'];row={'id':name};start=time.monotonic();signal.alarm(45)
 try:
  c=T.certificate(r['N'],height=6);row.update(outcome='candidate'if c else 'not_excluded',certificate=c)
 except Exception as e:row.update(outcome='incomplete',reason=str(e),certificate=None)
 finally:signal.alarm(0)
 row['seconds']=time.monotonic()-start;out.append(row);(Path(__file__).parent/'rotation_all22.json').write_text(json.dumps(out)+'\n');print({k:v for k,v in row.items()if k!='certificate'},flush=True)
