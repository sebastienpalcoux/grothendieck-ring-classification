def _audit_require(ok, message):
    if not ok: raise AssertionError(message)

from pathlib import Path
import json,runpy,sys,io,contextlib,time,argparse
import numpy as np
parser=argparse.ArgumentParser(description='Check the frozen forgetful matrix against the complete rank-26 fusion ring.')
parser.add_argument('--package',type=Path,required=True)
parser.add_argument('--reconstruction',type=Path,default=Path(__file__).resolve().parents[2]/'r155_modular/reconstruction.json')
args=parser.parse_args()
p=args.package.resolve()
sys.argv=['verify_forced_twists.py','--package',str(p)]
t=time.monotonic()
with contextlib.redirect_stdout(io.StringIO()):
 ns=runpy.run_path(str(p/'research/frontier/R6_4_155/verify_forced_twists.py'))
r=json.loads(args.reconstruction.read_text())
W=np.array(ns['W'],dtype=np.int64);R=np.array(ns['R'],dtype=np.int64);N=np.array(r['fusion_rules'],dtype=np.int64)
lhs=np.einsum('ijk,ka->ija',N,W)
rhs=np.einsum('ia,jb,abc->ijc',W,W,R)
bad=np.argwhere(lhs!=rhs).tolist()
_audit_require(not bad, bad)
_audit_require(W[r['unit']].tolist()==[1,0,0,0,0,0], 'Exact audit check failed')
counts={}
for i in range(26):
 f=W[i].tolist(); key=str(f); counts[key]=counts.get(key,0)+1
out={'passed':True,'all_26_squared_forgetful_product_identities':True,'all_4056_integer_coefficients_match':True,'unit_preserved':True,'forgetful_matrix':W.tolist(),'seconds':time.monotonic()-t,'scope':'fusion-ring homomorphism of the candidate B to R155; not a tensor functor construction'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print({k:v for k,v in out.items()if k!='forgetful_matrix'})
