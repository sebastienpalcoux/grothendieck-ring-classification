"""Exact ring inputs for the R1154 simple-center theorem; no optimizer."""
from pathlib import Path
import hashlib,json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]/'prior'
P=ROOT/'evidence/unresolved_retry_20261024/proofs/unresolved11_20261024/inputs/R8_3_1154.json'
J=json.loads(P.read_text()); R=J['fusion_tensor']; n=8
h=hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()
def require(x,msg):
 if not x: raise RuntimeError(msg)
require(h=='c399505be76a64c8aba65feaf2cd55125dc7132f5894b74e58b64473d1387e25','tensor identity')
def add(x,y): return x[0]+y[0],x[1]+y[1]
def mul(x,y): return x[0]*y[0]+5*x[1]*y[1],x[0]*y[1]+x[1]*y[0]
ds=[(1,0),(7,3),(7,3),(1,0),(6,3),(6,3),(7,3),(7,3)]
for i in range(n):
 for j in range(n):
  require(mul(ds[i],ds[j])==tuple(sum(R[i][j][k]*ds[k][l] for k in range(n)) for l in range(2)),'dimension multiplication')
dual=[next(j for j in range(n) if R[i][j][0]) for i in range(n)]
def closure(S):
 S=set(S)|{0}
 while True:
  T=S|{dual[i] for i in S}|{k for i in S for j in S for k in range(n) if R[i][j][k]}
  if S==T:return sorted(S)
  S=T
closures={i:closure([i]) for i in range(n)}
require(closures[3]==[0,3],'pointed subring')
require(all(closures[i]==list(range(n)) for i in (1,2,4,5,6,7)),'nonpointed generators')
adj=closure({k for i in range(n) for k in range(n) if R[i][dual[i]][k]})
require(adj==list(range(n)),'full adjoint')
require(R[3][1]!=R[1][3],'noncentral invertible')
require(R[3][3]==[1,0,0,0,0,0,0,0],'order-two invertible')
require(all(ds[i][1]>0 for i in (1,2,4,5,6,7)),'positive irrational coefficients')
D=tuple(sum(mul(x,x)[k] for x in ds) for k in range(2))
require(D==(540,240),'global dimension')
Z=mul(D,D)
# Optional inherited rank calculation is kept separate from the simple-center proof.
G=json.loads((ROOT/'evidence/rank8_frontier_20261021/central_integrality/integer_gram_1154.json').read_text())
ranks={str(i):len(G['low_columns'])+sum(G['completions'][i]) for i in (6971,8766,8772)}
require(ranks=={'6971':23,'8766':21,'8772':29},'frozen rank domain')
receipt={'tensor_sha256':h,'source':str(P.relative_to(ROOT)),'duals':dual,'single_object_fusion_closures':closures,'full_adjoint':adj,'gX1':R[3][1],'X1g':R[1][3],'dimensions_in_basis_1_sqrt5':ds,'global_dimension':D,'center_dimension':Z,'conditional_center_ranks':ranks,'status':'unresolved','note':'Checks ring inputs only; categorical proof is in SIMPLE_CENTER.md.'}
(HERE/'simple_center_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'verified':True,'tensor_sha256':h,'center_dimension':Z,'center_ranks':ranks,'status':'unresolved'}))
