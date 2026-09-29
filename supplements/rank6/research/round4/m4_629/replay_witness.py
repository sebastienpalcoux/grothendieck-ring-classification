import sys,json,time
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'))
import scipy.optimize as o
def disabled(*a,**k):raise RuntimeError('numerical optimizer disabled during exact replay')
o.linprog=disabled;o.milp=disabled
from round4_629_orbits import verify_witness
src=Path(__file__).with_name(sys.argv[1] if len(sys.argv)>1 else 'probe_orbits_h3.json');rec=json.load(open(src));R=next(x['N'] for x in json.load(open(P/'data/census.json')) if x['id']==rec['id']);st=time.monotonic();r=verify_witness(R,rec);r['seconds']=time.monotonic()-st;r['optimized_python']=not __debug__;src.with_name(src.stem+('_replay_O.json' if not __debug__ else '_replay.json')).write_text(json.dumps(r));print(r)
