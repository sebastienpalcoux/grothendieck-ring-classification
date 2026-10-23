import json,itertools
from pathlib import Path
import sympy as s
from sympy.matrices.normalforms import smith_normal_form
P=Path(__file__).resolve().parent
D=json.loads((P/'Q_soft_aut_support.json').read_text());R=D['tensor'];V=list(map(tuple,D['variables']));idx={v:i for i,v in enumerate(V)};A=s.Matrix(D['constraints']);rank=A.rank()
# rows onlyneedbasis forsmall exact smith computations
basis=s.Matrix.hstack(*A.T.columnspace()).T
for a,b,c,d in itertools.product(range(1,4),repeat=4):
 E=[e for e in range(4) if R[a][b][e] and R[e][c][d]];F=[f for f in range(4) if R[b][c][f] and R[a][f][d]]
 if len(E)<2:continue
 types=[]
 for e in E:
  row=[]
  for f in F:
   v=[0]*len(V)
   for t,sgn in [((a,b,e),1),((e,c,d),1),((b,c,f),-1),((a,f,d),-1)]:
    if t in idx:v[idx[t]]+=sgn
   W=A.col_join(s.Matrix([v]));r=W.rank()
   if r==rank:typ=0
   else:
    S=smith_normal_form(W,domain=s.ZZ);di=[abs(S[i,i]) for i in range(min(S.shape)) if S[i,i]];typ=max(di)
   row.append(int(typ))
  types.append(row)
 perms=list(itertools.permutations(range(len(F))));bad=[p for p in perms if all(types[i][p[i]]!=1 for i in range(len(E)))]
 print((a,b,c,d),E,F,types,'forcedprimitive',not bad,flush=True)
