import sys,json,time,signal,hashlib
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'));import scipy.optimize as so

def blocked(*a,**k):raise RuntimeError('optimizer disabled in exact replay')
so.linprog=so.milp=blocked
import round4_higher_e6 as m
rid='R6_6_1035';R=next(r['N']for r in json.load(open(P/'data/census.json'))if r['id']==rid);p=Path(__file__).with_name(rid+'_general.json');c=json.loads(p.read_text());st=time.monotonic()
def stop(*a):raise TimeoutError('840-second exact replay budget')
signal.signal(signal.SIGALRM,stop);signal.alarm(840)
ans=m.verify_general(R,c);signal.alarm(0);ans.update(id=rid,seconds=time.monotonic()-st,python_optimized=not __debug__,certificate_sha256=hashlib.sha256(p.read_bytes()).hexdigest());out=Path(__file__).with_name(rid+('_replay_optimized.json'if not __debug__ else '_replay.json'));out.write_text(json.dumps(ans,indent=2)+'\n');print(ans)
