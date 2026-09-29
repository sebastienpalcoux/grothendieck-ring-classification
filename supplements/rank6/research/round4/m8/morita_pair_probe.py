import json,sys,itertools
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'))
from full_morita_gram import *
from prepare import key
C={r['id']:r['N'] for r in json.load(open(P/'data/census.json'))};keys={key(C[r]):r for r in ('R6_8_311','R6_8_1660')}
for rid in keys.values():
 R=C[rid];g=invs(R)[0];fixed,seed,nodes,reps=anti_representations(R,g)
 for T in reps:
  labels,M=module_matrices(R,g,fixed,T);r=len(labels);G=full_gram(M);counts=Counter(first_columns(M,g));V=s.Matrix.hstack(*G.columnspace());allcs=set()
  for c in counts:
   for row in counts:
    for x in image_candidates(G,V,c,row):
     B=s.Matrix(r,r,x)
     if all(B*m==m*B for m in M):allcs.add(x)
  I=tuple(int(i==j) for i in range(r) for j in range(r));allcs=sorted(allcs);allcs.remove(I);allcs=[I]+allcs;X=s.Matrix.hstack(*map(s.Matrix,allcs));print(rid,'candidates',len(allcs),'rank',X.rank(),'gram',X*X.T==G,flush=True)
  if X*X.T!=G:continue
  B=list(map(lambda x:s.Matrix(r,r,x),allcs));D=[]
  for A in B:
   rr=[]
   for Z in B:
    v,pars=X.gauss_jordan_solve(s.Matrix(list(A*Z)));require(not pars.rows,'right-action multiplication not unique');rr.append(list(map(int,v)))
   D.append(rr)
  print('dual',keys.get(key(D),'different tensor'),D,flush=True)
