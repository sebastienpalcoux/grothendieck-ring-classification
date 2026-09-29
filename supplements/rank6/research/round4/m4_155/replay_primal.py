import sys,json,time,hashlib
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'))
import scipy.optimize

def disabled(*a,**kw):raise RuntimeError('numerical optimizers disabled for exact replay')
scipy.optimize.linprog=disabled;scipy.optimize.milp=disabled
import round4_155 as V
from exact import require
base=Path(__file__).parent;r=json.load(open(base/'exact_primal_certificates.json'));R=next(x['N'] for x in json.load(open(P/'data/census.json')) if x['id']==r['id']);require(hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()==r['tensor_sha256'],'wrong input tensor');out=[];st=time.monotonic()
for c in r['certificates']:
 a=time.monotonic();z=V.verify_primal(R,c);z.update({'source':c['source'],'F':c['F'],'height':c['height'],'pointed_subgroup':c.get('pointed_subgroup'),'seconds':time.monotonic()-a});out.append(z);print(z,flush=True)
report={'passed':True,'optimized_python':not __debug__,'optimizer_used':False,'seconds':time.monotonic()-st,'records':out};(base/('exact_primal_replay_optimized.json' if not __debug__ else 'exact_primal_replay.json')).write_text(json.dumps(report,indent=2)+'\n')
