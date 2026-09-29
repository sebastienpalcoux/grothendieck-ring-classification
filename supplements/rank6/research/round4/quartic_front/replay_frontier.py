import sys,json,time,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'software'))
import scipy.optimize
from exact import require
import round4_quartic_twists as T

def denied(*_,**__):raise RuntimeError('numerical optimizers are disabled')
scipy.optimize.linprog=scipy.optimize.milp=denied
rid=sys.argv[1];path=Path(__file__).with_name(rid+'_frontier_certificate.json');R=next(x['N'] for x in json.load(open(ROOT/'data/census.json')) if x['id']==rid);record=json.load(open(path));require(record['id']==rid,'wrong tensor id');st=time.monotonic();report=T.verify(R,record['certificate']);report.update(id=rid,seconds=time.monotonic()-st,optimized_python=not __debug__,certificate_sha256=hashlib.sha256(path.read_bytes()).hexdigest());Path(__file__).with_name(rid+'_frontier_replay_optimized.json').write_text(json.dumps(report,indent=2)+'\n');print(report,flush=True)
