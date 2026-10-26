from pathlib import Path
import sys,json,itertools,collections,time
HERE=Path(__file__).resolve().parent;BASE=HERE.parents[1]/'rank12-m1-offline-20261025'
sys.path[:0]=[str(BASE/'sources/work/models'),str(BASE/'sources/work/rank11')]
from match_models import ty,rep_dihedral
from zest_models import gradings,zest
import common
DATA=json.loads((BASE/'tensors.json').read_text());target={x['id']for x in json.loads((BASE.parent/'rank12-m1-round2-20261025/audit_models/d32/d32_summary.json').read_text())['records']}
I=ty((2,));out=[];attempts=[]
for name,B in [('Rep(D16)',rep_dihedral(8)),('Rep(Q16)',rep_dihedral(8,True))]:
 for degree in gradings(B):
  if len(B)+degree.count(0)!=12:continue
  labs=[(a,b)for a in range(3)for b in range(len(B))if int(a==2)==degree[b]]
  R=[[[I[a][c][e]*B[b][d][f]for e,f in labs]for c,d in labs]for a,b in labs]
  common.validate(R);h=labs.index((1,0));variants=[('base',R)]
  for h in range(1,len(R)):
   if R[h][h][0]!=1 or sum(R[h][h])!=1:continue
   for g in gradings(R):
    if g[h]==0:variants.append(('zest_h'+str(h)+'_'+str(g),zest(R,g,h)))
  for variant,M in variants:
   common.validate(M);hits=[]
   for rid,R0 in DATA.items():
    if common.coarse(R0)!=common.coarse(M):continue
    p=common.based_iso(R0,M)
    if p is not None:
     hits.append(rid);out.append(dict(id=rid,new=rid in target,constructor='Ising_graded_pullback',base_name=name,base_tensor=B,base_grading=degree,labels=labs,variant=variant,model_tensor=M,basis_map=p))
   print(name,degree,variant,hits,flush=True);attempts.append(dict(name=name,degree=degree,variant=variant,matches=hits))
(HERE/'pullback_results.json').write_text(json.dumps(dict(models=out,attempts=attempts),indent=2))
