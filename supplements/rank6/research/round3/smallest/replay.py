import json,sys,time,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'software'))
import scipy.optimize

def prohibited(*args,**kw):raise RuntimeError('optimizer forbidden in exact replay')
scipy.optimize.linprog=prohibited
scipy.optimize.milp=prohibited
import round3_smallest as C
from exact import require
import higher_traces
higher_traces.farkas=prohibited;C.farkas=prohibited
rows={r['id']:r for r in json.load(open(ROOT/'data/census.json'))};out=[]
for fn in sys.argv[1:] or ['R6_4_6_certificate.json','R6_6_8_certificate.json','R6_8_10_certificate.json']:
 path=Path(__file__).parent/fn;rec=json.load(open(path));start=time.time()
 require(rec['outcome']=='general_excluded','certificate did not claim general exclusion')
 C.verify(rows[rec['id']]['N'],rec['certificate'])
 z=dict(id=rec['id'],passed=True,seconds=time.time()-start,optimizer_disabled=True,optimized=not __debug__,certificate_sha256=hashlib.sha256(path.read_bytes()).hexdigest())
 out.append(z);print(json.dumps(z),flush=True)
Path(__file__).with_name('replay_optimized.json' if not __debug__ else 'replay_normal.json').write_text(json.dumps(out,indent=2)+'\n')
