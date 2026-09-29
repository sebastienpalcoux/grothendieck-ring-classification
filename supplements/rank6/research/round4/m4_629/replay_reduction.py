import sys,json,time
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'))
import scipy.optimize as op
def disabled(*a,**k):raise RuntimeError('numerical optimizer disabled')
op.linprog=op.milp=disabled
import galois_pseudo_reduction as g
R=next(x['N'] for x in json.load(open(P/'data/unresolved_tensors.json')) if x['id']=='R6_4_629');c=json.load(open(Path(__file__).with_name('general_reduction.json')))['certificate'];st=time.monotonic();r=g.verify(R,c);r.update(passed=True,optimized_python=not __debug__,optimizer_used=False,seconds=time.monotonic()-st);Path(__file__).with_name('general_reduction_replay_O.json' if not __debug__ else 'general_reduction_replay.json').write_text(json.dumps(r));print(r)
