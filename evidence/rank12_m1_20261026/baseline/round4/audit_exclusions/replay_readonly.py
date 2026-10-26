"""Replay an audited original checker, redirecting all receipt writes locally."""
from pathlib import Path
import runpy,sys
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
BASE=HERE.parents[1]/'prior_round'
SOURCE=BASE/'prior_round/evidence/rank12-m1-round2-20261025/audit_exclusions'
ALLOWED={'audit_all_exclusions','audit_quadratic_signed','audit_c9_morita','audit_d40_sources','audit_d8_cohomology','audit_d40_duals','audit_pointed_stabilizers','stabilizer_square','liptrap_independent'}
name=sys.argv[1]
if name not in ALLOWED:raise ValueError('unreviewed replay target')
oldopen=Path.open
def guarded_open(path,mode='r',*args,**kwargs):
    p=path.resolve()
    if any(c in mode for c in 'wxa+'):
        if p.is_relative_to(BASE):
            p=HERE/'replayed'/p.relative_to(BASE);p.parent.mkdir(parents=True,exist_ok=True)
        elif not p.is_relative_to(HERE):raise ValueError('write outside new audit directory')
    return oldopen(p,mode,*args,**kwargs)
Path.open=guarded_open
sys.path.insert(0,str(SOURCE))
runpy.run_path(str(SOURCE/(name+'.py')),run_name='__main__')
