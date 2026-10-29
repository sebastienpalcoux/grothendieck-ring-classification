"""Exact optimized replay of the inherited R6_4_1 exclusion; no optimizer."""
from pathlib import Path
import hashlib,json,sys,time
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]/'online_revision/grothendieck-ring-classification'
sys.path.insert(0,str(ROOT/'supplements/rank6/software'))
import scipy.optimize
def forbidden(*a,**k):raise RuntimeError('Optimizer forbidden in exact replay')
for name in ('linprog','milp','minimize','least_squares'):setattr(scipy.optimize,name,forbidden)
import oriented_extension
p=HERE.parent/'rank9_noncommutative/R6_4_1_dependency.json'
x=next(x for x in json.loads(p.read_text())['rows'] if x['id']=='R6_4_1')
start=time.monotonic()
if x['decision']['existence']['general']!='no':raise ValueError('Wrong scope')
if x['decision']['certificate']['kind']!='oriented_pseudo_gate':raise ValueError('Wrong gate')
oriented_extension.verify(x['N'],x['decision']['certificate'])
out={'status':'PASS','id':x['id'],'scope':'general complex fusion categories via two-FP-value Galois-PU gate','kind':x['decision']['certificate']['kind'],'inner_kind':x['decision']['certificate']['pseudo']['kind'],'complete_low_frames':len(x['decision']['certificate']['pseudo']['branches']),'tensor_sha256':hashlib.sha256(json.dumps(x['N'],separators=(',',':')).encode()).hexdigest(),'dependency_file_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'optimizer_disabled':True,'python_optimized':not __debug__,'seconds':time.monotonic()-start}
(HERE/'audit_R6_4_1_dependency.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out),flush=True)
