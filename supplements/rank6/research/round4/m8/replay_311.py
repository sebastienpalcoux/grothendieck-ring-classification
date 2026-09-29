import json,sys,time,hashlib
from pathlib import Path
import scipy.optimize as opt
def disabled(*a,**k):raise RuntimeError('numerical optimizer disabled in exact replay')
opt.linprog=disabled;opt.milp=disabled
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'))
import round4_m8_ising as M
R=next(x['N'] for x in json.load(open(P/'data/census.json')) if x['id']=='R6_8_311')
f=P/'research/round4/m8/R6_8_311_certificate.json';c=json.load(open(f));st=time.monotonic();v=M.verify_general(R,c)
q={'id':'R6_8_311','optimized_python':not __debug__,'certificate_sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'result':v,'seconds':time.monotonic()-st,'linprog_disabled':True,'milp_disabled':True}
(P/'research/round4/m8'/('311_replay_optimized.json' if not __debug__ else '311_replay_normal.json')).write_text(json.dumps(q,indent=2)+'\n');print(json.dumps(q),flush=True)
