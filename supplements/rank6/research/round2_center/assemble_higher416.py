"""Assemble and replay the full general Clifford-rotation exclusion for R416."""
import json,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'software'))
import scipy.optimize

def disabled(*args,**kwargs):raise RuntimeError('optimizer called during exact composite replay')
for name in ('linprog','milp','minimize','least_squares'):
 if hasattr(scipy.optimize,name):setattr(scipy.optimize,name,disabled)
from stabilizer_rotation_higher import verify_general
from exact import require
pu=json.loads((ROOT/'research/round2_theory/R6_4_416_higher.json').read_text());require(pu['outcome']=='pseudo_unitary_excluded','no pseudo-unitary exclusion')
reduction=json.loads(Path(__file__).with_name('galois_reduction_416.json').read_text())['certificate']
c={'kind':'general_stabilizer_rotation_higher','version':1,'scope':'general','pseudo':pu['certificate'],'reduction':reduction}
R=next(r['N'] for r in json.loads((ROOT/'data/census.json').read_text()) if r['id']=='R6_4_416')
started=time.monotonic();verify_general(R,c)
record={'id':'R6_4_416','status':'excluded','scope':'general','certificate':c}
(ROOT/'certificates/stabilizer_rotation_416.json').write_text(json.dumps(record,separators=(',',':'))+'\n')
report={'id':'R6_4_416','general_exclusion':True,'optimized_python':not __debug__,'optimizer_disabled':True,'seconds':time.monotonic()-started,'module_branches':len(c['pseudo']['branches']),'conditional_certificates':len(c['pseudo']['conditionals']),'signed_quotients':len(reduction['all_values']),'sign_orbits':len(reduction['branches'])}
Path(__file__).with_name('general_replay_416_report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report),flush=True)
