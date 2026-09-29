import sys,json,time,signal
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'software'))
import tensor_rotation as T
name=sys.argv[1];R=next(r['N']for r in json.load(open(ROOT/'data/census.json'))if r['id']==name)
def end(*_):raise TimeoutError('900-second exact discovery budget')
signal.signal(signal.SIGALRM,end);signal.alarm(890);start=time.monotonic();row={'id':name}
try:
 c=T.certificate(R,height=6);row.update(outcome='candidate' if c else 'not_excluded',certificate=c)
except Exception as e:row.update(outcome='incomplete',reason=str(e),certificate=None)
finally:signal.alarm(0)
row['seconds']=time.monotonic()-start;(Path(__file__).parent/(name+'_rotation.json')).write_text(json.dumps(row)+'\n');print({k:v for k,v in row.items()if k!='certificate'},flush=True)
