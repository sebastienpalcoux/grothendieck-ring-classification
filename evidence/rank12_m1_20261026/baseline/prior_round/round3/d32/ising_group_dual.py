from pathlib import Path
import json,itertools,sys,time
HERE=Path(__file__).resolve().parent;BASE=HERE.parents[1]/'rank12-m1-offline-20261025'
sys.path[:0]=[str(BASE/'sources/work/models'),str(BASE/'sources/work/rank11')]
from match_models import ty
import common,bimodule
DATA=json.loads((BASE/'tensors.json').read_text());I=ty((2,));out=[];attempts=[]
# D16, Q16, semidihedral, modular order16 presentations r^8=1,srs^-1=r^u,s²=r^v.
for u,v in [(7,0),(7,4),(3,0),(3,4),(5,0),(5,4),(1,0),(1,4)]:
 if ((u-1)*v)%8:continue
 E=list(itertools.product(range(8),range(2)));mul=lambda g,h:((g[0]+(u if g[1]else 1)*h[0]+v*g[1]*h[1])%8,(g[1]+h[1])%2)
 for grad in [(1,0),(0,1),(1,1)]:
  degree=lambda g:(g[0]*grad[0]+g[1]*grad[1])%2
  labs=[(a,g)for a in range(3)for g in E if int(a==2)==degree(g)]
  R=[[[I[a][b][c]*int(mul(g,h)==k)for c,k in labs]for b,h in labs]for a,g in labs]
  common.validate(R)
  def F(a,b,c,k):
   aa,bb,cc,kk=[labs[x][0]for x in (a,b,c,k)]
   if aa==cc==2 and bb!=2:return 2*bb*kk
   if aa!=2 and bb==2 and cc!=2:return 2*aa*cc
   if aa==bb==cc==2:raise ValueError('unused three-odd F')
   return 0
  for c,(a,g) in enumerate(labs):
   if not c or a==2 or g==(0,0) or mul(g,g)!=(0,0):continue
   if sum(h==mul(g,k)for h,k in zip(E,E))!=0:pass
   try:M,info=bimodule.construct(R,F,c)
   except Exception as exc:
    print('ERROR',u,v,grad,(a,g),repr(exc),flush=True);raise
   if M is None:continue
   hits=[]
   for rid,T in DATA.items():
    if common.coarse(T)!=common.coarse(M):continue
    p=common.based_iso(T,M)
    if p is not None:
     hits.append(rid);out.append(dict(id=rid,constructor='Ising_VecE_graded_pullback_C2_Morita_dual',parameters=dict(u=u,v=v,grading=grad,algebra_generator=(a,g)),source_labels=labs,source_tensor=R,model_tensor=M,basis_map=p,bimodules=info['objects']))
   print(u,v,grad,(a,g),hits,flush=True);attempts.append(dict(u=u,v=v,grading=grad,generator=(a,g),matches=hits))
   (HERE/'ising_group_dual_results.json').write_text(json.dumps(dict(models=out,attempts=attempts),indent=2))
