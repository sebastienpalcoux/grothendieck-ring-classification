import itertools,json
import sympy as s
from sympy.matrices.normalforms import smith_normal_form
from pathlib import Path
P=Path(__file__).resolve().parent
for kind in ['P','Q']:
 R=[[[0]*4 for _ in range(4)] for _ in range(4)]
 for i in range(4):R[0][i][i]=R[i][0][i]=1
 for i in range(4):R[1][i][i^1]=R[i][1][i^1]=1
 for i in [2,3]:
  for j in [2,3]:
   R[i][j][(i^j)^(0 if kind=='P' else 1)]=1
   R[i][j][2]=R[i][j][3]=1
 dual=[next(j for j in range(4) if R[i][j][0]) for i in range(4)]
 V=[(a,b,c) for a,b,c in itertools.product(range(4),repeat=3) if a and b and R[a][b][c]];idx={v:i for i,v in enumerate(V)};rows=[];records=[]
 for a,b,c,d in itertools.product(range(4),repeat=4):
  E=[e for e in range(4) if R[a][b][e] and R[e][c][d]];F=[f for f in range(4) if R[b][c][f] and R[a][f][d]]
  for e in E:
   for f in F:
    reason='singleton' if len(E)==len(F)==1 else ('unit_intermediate' if e==0 or f==0 else None)
    if not reason:continue
    v=[0]*len(V)
    for t,sgn in [((a,b,e),1),((e,c,d),1),((b,c,f),-1),((a,f,d),-1)]:
     if t in idx:v[idx[t]]+=sgn
    if any(v):rows.append(v);records.append([a,b,c,d,e,f,reason])
 A=s.Matrix(rows);S=smith_normal_form(A,domain=s.ZZ);diag=[abs(S[i,i]) for i in range(min(S.shape)) if S[i,i]]
 print(kind,'vars',len(V),'rows',len(rows),'rank',A.rank(),'SNF',diag)
 (P/f'{kind}_soft_aut_support.json').write_text(json.dumps({'kind':kind,'tensor':R,'variables':V,'constraints':rows,'nonzero_F_support_used':records,'smith_invariants':list(map(int,diag))},indent=2)+'\n')
