#!/usr/bin/env python3
import json,itertools
from pathlib import Path
import sympy as s
BASE=Path(__file__).resolve().parent
catalogue={r['id']:r for r in json.loads((BASE.parents[1]/'catalogue.json').read_text())['cases']}
def require(x,msg):
 if not x:raise RuntimeError(msg)
def build(k):
 r=catalogue[f'R10_1_{k}'];N=r['fusion_tensor'];G=[g for g in range(10) if all(sum(N[g][j])==1 for j in range(10))]
 h=next(g for g in G if g and sum(N[g][x][x] for x in range(10))==2);Y=[i for i in range(10) if N[h][i][i]];Z=[i for i in range(10) if i not in G+Y]
 require(all(sum(N[y][y][i] for i in G)==2 and sum(N[y][y][i] for i in Y)==2 and sum(N[y][y][i] for i in Z)==2 for y in Y),'collapsed y squared')
 require(all(sum(N[y][z][i] for i in G)==0 and sum(N[y][z][i] for i in Y)==1 and sum(N[y][z][i] for i in Z)==4 for y in Y for z in Z),'collapsed yz')
 require(all(sorted(N[g][Z[0]].index(1) for g in G)==sorted(Z) for g0 in [0]),'G transitive on Z')
 require(all(s.Matrix([[N[z][a][b] for b in Y] for a in Y]) in [s.eye(2),s.Matrix([[0,1],[1,0]])] for z in Z),'Z fixed sector parity')
 plus=[1 if i in G else 2 if i in Y else -1 for i in range(10)]
 minus=[(1 if i in [0,h] else -1) if i in G else 0 if i in Y else 1-2*N[i][Y[0]][Y[0]] for i in range(10)]
 for v in [plus,minus]:
  require(all(v[i]*v[j]==sum(N[i][j][t]*v[t] for t in range(10)) for i in range(10) for j in range(10)),'character')
 rho=[s.Matrix([[(plus[i]+minus[i])//2,(plus[i]-minus[i])//2],[(plus[i]-minus[i])//2,(plus[i]+minus[i])//2]]) for i in range(10)]
 free=[];used=set(Y)
 for i in range(10):
  if i in used:continue
  j=N[h][i].index(1);free.append([i,j]);used|={i,j}
 # indices 0..3 free; 4,5 splitsY0;6,7 splitsY1
 mats=[]
 for i in range(10):
  L=s.zeros(8)
  for j,orb in enumerate(free):
   x=orb[0]
   for a,o in enumerate(free):L[a,j]=sum(N[i][x][t] for t in o)
   for a,y in enumerate(Y):L[4+2*a,j]=L[5+2*a,j]=N[i][x][y]
  for j,y in enumerate(Y):
   for sign in range(2):
    col=4+2*j+sign
    for a,o in enumerate(free):L[a,col]=N[i][y][o[0]]
    for a,z in enumerate(Y):
     for outsign in range(2):L[4+2*a+outsign,col]=(N[i][y][z]+(1 if sign==outsign else -1)*rho[i][a,j])/2
  require(all(v.is_Integer and v>=0 for v in L),'nonnegative integer action')
  mats.append(L)
 dual=r['invariants']['dual_indices']
 require(all(mats[i].T==mats[dual[i]] for i in range(10)),'module duality')
 require(all(mats[i]*mats[j]==sum((N[i][j][t]*mats[t] for t in range(10)),s.zeros(8)) for i in range(10) for j in range(10)),'module fusion')
 # linear commutant, vectorization row major
 vars=s.symbols('b:64');B=s.Matrix(8,8,vars);eqs=[]
 for L in mats:eqs.extend(B*L-L*B)
 A,b=s.linear_eq_to_matrix(eqs,vars)
 null=A.nullspace()
 data={'id':r['id'],'h':h,'free_orbits':free,'fixed_Y':Y,'plus_character':plus,'minus_character':minus,'rho':[[list(map(int,row)) for row in M.tolist()] for M in rho],'module_matrices':[[list(map(int,row)) for row in M.tolist()] for M in mats],'commutant_dimension':len(null),'commutant_basis':[[str(x) for x in v] for v in null]}
 (BASE/f'{r["id"]}_module.json').write_text(json.dumps(data,indent=2)+'\n')
 return data,mats,null
if __name__=='__main__':
 for k in [21,114,115,152,153,179]:
  d,m,n=build(k);print(k,'commutant',len(n))
