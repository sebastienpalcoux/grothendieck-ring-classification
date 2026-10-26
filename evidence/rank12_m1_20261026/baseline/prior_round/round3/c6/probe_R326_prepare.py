import json,itertools,ast
from pathlib import Path
import sympy as s
P=Path(__file__).resolve().parent
R=json.load(open('rank12-m1-offline-20261025/tensors.json'))['R12_1_326'];du=[next(j for j in range(12) if R[i][j][0]) for i in range(12)];G=[i for i in range(12) if sum(R[i][du[i]])==1]
B=s.Matrix(12,12,lambda j,i:sum(R[a][j][k]*R[k][du[a]][i] for a in range(12) for k in range(12)))
C=s.Matrix([[R[j][i][k]-R[i][j][k] for i in range(12)] for j in range(12) for k in range(12)]);Z=C.nullspace();assert len(Z)==6
sig={i:tuple(z[i] for z in Z) for i in range(12)};classes=[];rest=set(range(12))
while rest:
 i=min(rest);cl=[j for j in sorted(rest) if sig[j]==sig[i]];classes.append(cl);rest-=set(cl)
assert len(classes)==6 and classes[0]==[0]
assert all(C*s.Matrix([int(i in cl) for i in range(12)])==s.zeros(144,1) for cl in classes)
pc=[cl for cl in classes if cl[0] in G and cl[0]];nc=[cl for cl in classes if cl[0] not in G]
print(G,pc,nc)
for fn in ast.parse((P/'verify_local.py').read_text()).body:
 if isinstance(fn,ast.FunctionDef) and fn.name=='psd_witness':exec(ast.unparse(fn))
def choose(total,u):
 out=[]
 for v in itertools.product(*(range(total//len(cl)+1) for cl in nc)):
  if sum(len(cl)*k for cl,k in zip(nc,v))!=total:continue
  x=[0]*12;x[0]=u
  for cl,k in zip(nc,v):
   for j in cl:x[j]=k
  out.append(x)
 return out
out=[]
for vv in itertools.product(choose(6,1),choose(3,1),choose(3,1),choose(6,2),choose(6,2)):
 L=s.Matrix.hstack(s.eye(12)[:,0],*map(s.Matrix,vv))
 if L*s.Matrix([1,1,1,1,2,2])!=B[:,0]:continue
 Qm=B-L*L.T;w=psd_witness(Qm)
 if not w['psd']:
  v=s.Matrix([s.Rational(x) for x in w['vector']]);assert(v.T*Qm*v)[0]<0
 out.append({'columns':[[int(x) for x in col] for col in L.T.tolist()],**w})
(P/'R326_induction_low_exact.json').write_text(json.dumps({'G':G,'pointed_classes':pc,'nonpointed_classes':nc,'branches':out,'surviving_branches':sum(x['psd'] for x in out)},indent=2)+'\n')
print('low branches',len(out),'survivors',sum(x['psd'] for x in out))
