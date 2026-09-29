import sys,json,time
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'))
import scipy.optimize as opt

def denied(*a,**k):raise RuntimeError('optimizer disabled in exact replay')
for name in ['linprog','milp','minimize','least_squares','lsq_linear']:
 if hasattr(opt,name):setattr(opt,name,denied)
import round3_m4 as m
m.farkas=denied;m.cached_farkas=denied
R=next(x['N'] for x in json.load(open(P/'data/census.json')) if x['id']=='R6_4_211');st=time.monotonic()
p=Path(__file__).with_name('R6_4_211_general.json')
if p.exists():
 c=json.load(open(p))['certificate'];rec=m.verify_general(R,c)
else:
 c=json.load(open(Path(__file__).with_name('R6_4_211_ambient_h3.json')));rec=m.verify(R,c)
rec.update(id='R6_4_211',general='reduction' in rec,optimized=not __debug__,seconds=time.monotonic()-st)
Path(__file__).with_name('R6_4_211_exact_replay.json').write_text(json.dumps(rec,indent=2)+'\n');print(rec,flush=True)
