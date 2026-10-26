from pathlib import Path
import json,itertools,sys
HERE=Path(__file__).resolve().parent;BASE=HERE.parents[1]/'rank12-m1-offline-20261025'
sys.path.insert(0,str(BASE/'sources/work/rank11'));import common,bimodule
from r240_model import build
D=json.loads((BASE/'tensors.json').read_text());E=list(itertools.product(range(8),range(2)))
I=lambda a,b,c:int(c==a^b)if a<2 and b<2 else int(c==2)if (a==2)!=(b==2)else int(c<2)
out=[]
for u in [3,5]:
 mul=lambda g,h:((g[0]+u**g[1]*h[0])%8,(g[1]+h[1])%2)
 for rot in [2,4,6]:
  zcoef=(-(rot*((u*u-1)//8)//2)*pow(u,-1,8))%8
  def omega(g,h,k):
   a,b=g;c,d=h;e,f=k;carry=(c+u**d*e-(c+u**d*e)%8)//8
   return(a*u**b*(rot*carry+zcoef*d*e))%8
  for g,h,k,l in itertools.product(E,repeat=4):common.require((omega(h,k,l)-omega(mul(g,h),k,l)+omega(g,mul(h,k),l)-omega(g,h,mul(k,l))+omega(g,h,k))%8==0,'semidirect even-rotation cocycle')
  if u==5:continue
  labs=[(a,g)for a in range(3)for g in E if int(a==2)==g[0]%2];R=[[[I(a,b,c)*int(mul(g,h)==k)for c,k in labs]for b,h in labs]for a,g in labs]
  def F(a,b,c,k):
   aa,bb,cc,kk=[labs[x][0]for x in(a,b,c,k)];v=omega(labs[a][1],labs[b][1],labs[c][1])
   if aa==cc==2 and bb!=2:v+=4*bb*kk
   if aa!=2 and bb==2 and cc!=2:v+=4*aa*cc
   return v%8
  for a in [0,1]:
   c=labs.index((a,(0,1)));M,info=bimodule.construct(R,F,c,q=8);hits=[]
   if M:
    for rid,T in D.items():
     if common.coarse(T)!=common.coarse(M):continue
     p=common.based_iso(T,M)
     if p is not None:hits.append(rid);out.append(dict(id=rid,u=u,rotation=rot,zcoef=zcoef,model_tensor=M,basis_map=p))
   print(u,rot,a,hits,flush=True)
(HERE/'semidihedral_even_results.json').write_text(json.dumps(out,indent=2))
