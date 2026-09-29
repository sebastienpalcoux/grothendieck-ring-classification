import sys,json,time
from pathlib import Path
import scipy.optimize as opt
def fail(*a,**k):raise RuntimeError('optimizer disabled in exact primal replay')
opt.linprog=opt.milp=fail
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'))
import round4_m8_ising_verlinde as M
R=next(x['N'] for x in json.load(open(P/'data/census.json')) if x['id']=='R6_8_1660');c=json.load(open(P/'research/round4/m8/1660_necessary_witness.json'));st=time.monotonic();o=M.verify_witness(R,c);o.update(optimized_python=not __debug__,seconds=time.monotonic()-st)
(P/'research/round4/m8/1660_witness_replay.json').write_text(json.dumps(o,indent=2)+'\n');print(o,flush=True)
