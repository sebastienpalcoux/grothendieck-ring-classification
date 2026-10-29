"""Short exact check of necessary module structures; no categorification claim."""
from pathlib import Path
import hashlib,json,runpy
import sympy as s
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
def check(x,label):
 if not x:raise ValueError(label)
G=[(0,0),(1,0),(0,1),(1,1)]
P=[]
for h,g in G:
 q=s.zeros(6)
 for j,(a,b) in enumerate(G):q[G.index((a^h,b^g)),j]=1
 for j in (4,5):q[4+((j-4)^g),j]=1
 P.append(q)
x1=s.Matrix([[1,1,1,1,1,2],[1,1,1,1,1,2],[1,1,1,1,2,1],[1,1,1,1,2,1],[2,2,1,1,2,2],[1,1,2,2,2,2]])
x2=s.Matrix([[2,2,2,2,0,1],[2,2,2,2,0,1],[2,2,2,2,1,0],[2,2,2,2,1,0],[1,1,0,0,0,0],[0,0,1,1,0,0]])
d=4+3*s.sqrt(2);out=[]
for k,x in [(1,x1),(2,x2)]:
 y=x.T
 check(x*y==P[0]+P[1]+4*(x+y),'XY rule')
 check(x*x==P[2]+P[3]+4*(x+y),'XX rule')
 for p in P:check(p*x==x*p,'pointed commutation')
 check(P[1]*x==x and P[2]*x==y,'pointed action')
 ratio=3*d/(1+2*d) if k==1 else d/(1+4*d)
 v=s.Matrix([1,1,1,1,ratio,ratio])
 check(all(s.simplify(t)==0 for t in x*v-d*v),'Perron dimensions')
 out.append({'k':k,'rank':6,'X_action':[[int(t) for t in row] for row in x.tolist()], 'trace_X':int(s.trace(x)), 'module_dimension_ratio':str(s.simplify(ratio))})
q=s.simplify(d*d/(1+2*d))
check(q==2+4*s.sqrt(2)/3,'nonintegral internal end dimension')
t=s.Symbol('t');check(s.minpoly(q,t)==9*t*t-36*t+4,'minimal polynomial')
T=runpy.run_path(str(ROOT/'data/current_remaining_cases.py'))['TENSORS']['R6_4_155']
sha=hashlib.sha256(json.dumps(T,separators=(',',':')).encode()).hexdigest()
check(sha=='012ef716d19b96a2a800d7bcbb33f3ae5e99e3c6a223f6e14bcd20144d4072a3','source identity')
receipt={'source_sha256':sha,'necessary_modules':out,'excluded_gram_branch_internal_end_dimension':str(q),'scope':'Necessary algebra/module reduction; R155 unresolved'}
(HERE/'r155_algebra_reduction_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('PASS: both necessary based modules, source hash, nonintegral branch obstruction')
