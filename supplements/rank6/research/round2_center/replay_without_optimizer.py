"""Replay the complete proof with optimizer entry points disabled."""
import json,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'software'))
import scipy.optimize

def disabled(*args,**kwargs):raise RuntimeError('optimizer called during exact proof replay')
for name in ('linprog','milp','minimize','least_squares'):
    if hasattr(scipy.optimize,name):setattr(scipy.optimize,name,disabled)
from stabilizer_rotation import verify_general
record=json.loads((ROOT/'certificates/stabilizer_rotation_215.json').read_text())
R=next(r['N'] for r in json.loads((ROOT/'data/census.json').read_text()) if r['id']==record['id'])
started=time.monotonic();report=verify_general(R,record['certificate']);report.update(optimized_python=not __debug__,optimizer_disabled=True,seconds=time.monotonic()-started)
print(json.dumps(report,indent=2))
