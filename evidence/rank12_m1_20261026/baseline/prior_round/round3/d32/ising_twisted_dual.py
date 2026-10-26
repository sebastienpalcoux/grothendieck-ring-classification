from pathlib import Path
import json,itertools,sys
HERE=Path(__file__).resolve().parent;BASE=HERE.parents[1]/'rank12-m1-offline-20261025'
sys.path[:0]=[str(BASE/'sources/work/models'),str(BASE/'sources/work/rank11')]
from match_models import ty
import common,bimodule
DATA=json.loads((BASE/'tensors.json').read_text());I=ty((2,));out=[];attempts=[]
E=list(itertools.product(range(8),range(2)))
for u in [3,5,1]:
 mul=lambda g,h:((g[0]+(u if g[1]else 1)*h[0])%8,(g[1]+h[1])%2)
 for grad in [(1,0),(0,1),(1,1)]:
  degree=lambda g:(g[0]*grad[0]+g[1]*grad[1])%2
  labs=[(a,g)for a in range(3)for g in E if int(a==2)==degree(g)]
  R=[[[I[a][b][c]*int(mul(g,h)==k)for c,k in labs]for b,h in labs]for a,g in labs]
  gens=[]
  for c,(aa,g) in enumerate(labs):
   if not c or aa==2 or g==(0,0) or mul(g,g)!=(0,0):continue
   # Geometry alone determines resulting rank.
   odd=[j for j,(a,h)in enumerate(labs)if a==2]
   if any(len({h,mul(g,h),mul(h,g),mul(mul(g,h),g)})!=4 for a,h in [labs[j]for j in odd]):continue
   if any(aa==a and any(mul(mul(x,g),(((-u if x[1]else -1)*x[0])%8,x[1]))==h for x in E if degree(x)==0)for a,h in [labs[t]for t in gens]):continue
   gens.append(c)
  if not gens:continue
  for rot,bits in itertools.product(range(8)if u==7 else [0],itertools.product(range(2),repeat=3)):
   def omega(g,h,k):
    a,b=g;c,d=h;e,f=k
    carry=(c+(-1)**d*e-(c+(-1)**d*e)%8)//8
    return (rot*a*(-1)**b*carry+4*(bits[0]*(a%2)*(c%2)*(e%2)+bits[1]*b*d*f+bits[2]*(a%2)*d*f))%8
   if rot==1 and bits==(0,0,0):
    assert all((omega(h,k,l)-omega(mul(g,h),k,l)+omega(g,mul(h,k),l)-omega(g,h,mul(k,l))+omega(g,h,k))%8==0 for g,h,k,l in itertools.product(E,repeat=4))
   def F(a,b,c,k):
    aa,bb,cc,kk=[labs[x][0]for x in (a,b,c,k)];phase=omega(labs[a][1],labs[b][1],labs[c][1])
    if aa==cc==2 and bb!=2:return (phase+4*bb*kk)%8
    if aa!=2 and bb==2 and cc!=2:return (phase+4*aa*cc)%8
    if aa==bb==cc==2:raise ValueError('unused three-odd F')
    return phase
   for c in gens:
    if F(c,c,c,c):continue
    M,info=bimodule.construct(R,F,c,q=8)
    if M is None:continue
    hits=[]
    for rid,T in DATA.items():
     if common.coarse(T)!=common.coarse(M):continue
     p=common.based_iso(T,M)
     if p is not None:
      hits.append(rid)
      if rid not in [t['id']for t in out]:out.append(dict(id=rid,constructor='Ising_twisted_VecE_graded_pullback_C2_Morita_dual',parameters=dict(u=u,grading=grad,rotation_cocycle=rot,abelian_cubes=bits,algebra_generator=labs[c]),source_labels=labs,source_tensor=R,model_tensor=M,basis_map=p,bimodules=info['objects']))
    print(u,grad,rot,bits,labs[c],hits,flush=True);attempts.append(dict(u=u,grading=grad,rotation_cocycle=rot,abelian_cubes=bits,generator=labs[c],matches=hits))
    (HERE/'ising_twisted_other_results.json').write_text(json.dumps(dict(models=out,attempts=attempts),indent=2))
