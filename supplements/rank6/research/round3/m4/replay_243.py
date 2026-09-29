import sys,json,time
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'))
import scipy.optimize as opt

def denied(*a,**k):raise RuntimeError('optimizer disabled in exact replay')
for name in ['linprog','milp','minimize','least_squares','lsq_linear']:
 if hasattr(opt,name):setattr(opt,name,denied)
import round3_verlinde as v
v.farkas=denied;v.M.farkas=denied
R=next(x['N'] for x in json.load(open(P/'data/census.json')) if x['id']=='R6_4_243');st=time.monotonic()
c=json.load(open(Path(__file__).with_name('R6_4_243_general.json')))['certificate'];rec=v.verify_general(R,c)
rec.update(id='R6_4_243',general=True,optimized=not __debug__,seconds=time.monotonic()-st)
Path(__file__).with_name('R6_4_243_exact_replay.json').write_text(json.dumps(rec,indent=2)+'\n');print(rec,flush=True)
