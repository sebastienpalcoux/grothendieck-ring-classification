"""Replay the inherited unrestricted general-to-pseudo-unitary reduction."""
import sys,json,hashlib
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'))
import scipy.optimize

def denied(*_,**__):raise RuntimeError('optimizer disabled during sphericalization replay')
scipy.optimize.linprog=scipy.optimize.milp=denied
import galois_pseudo_reduction as G
R=next(x['N'] for x in json.load(open(P/'data/census.json')) if x['id']=='R6_8_1660');f=P/'research/round4/m8/R6_8_1660_reduction.json';c=json.load(open(f));G.require(c['outcome']=='proved_reduction' and c['id']=='R6_8_1660','wrong inherited reduction');result=G.verify(R,c['certificate']);G.require(result==c['verification'],'inherited reduction summary mismatch');out=dict(passed=True,optimizer_used=False,optimized_python=not __debug__,source_sha256=hashlib.sha256(f.read_bytes()).hexdigest(),**result)
paths={Path(__file__).resolve(),f.resolve(),(P/'data/census.json').resolve()}
for module in list(sys.modules.values()):
 name=getattr(module,'__file__',None)
 if name:
  q=Path(name).resolve()
  if q.is_relative_to(P.resolve()) and q.suffix=='.py':paths.add(q)
out['files_sha256']={str(q.relative_to(P.resolve())):hashlib.sha256(q.read_bytes()).hexdigest() for q in sorted(paths)}
Path(__file__).with_name('reduction_replay.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='files_sha256'}))
