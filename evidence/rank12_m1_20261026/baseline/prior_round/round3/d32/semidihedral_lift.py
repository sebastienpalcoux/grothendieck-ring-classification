"""Bounded exact mod16 lift of an explicit semidihedral rotation cocycle."""
from pathlib import Path
import itertools,json,time,sys
HERE=Path(__file__).resolve().parent;BASE=HERE.parents[1]/'rank12-m1-offline-20261025'
sys.path.insert(0,str(BASE/'sources/work/rank11'));import common,bimodule
E=list(itertools.product(range(8),range(2)));nz=E[1:];keys=list(itertools.product(nz,repeat=3));ind={x:i for i,x in enumerate(keys)};n=len(keys)
mul=lambda g,h:((g[0]+3**g[1]*h[0])%8,(g[1]+h[1])%2)
def phi(g,h,k):
 a,b=g;c,d=h;e,f=k;t=c+3**d*e;return a*3**b*(2*((t-t%8)//8)+5*d*e)%16
start=time.monotonic();piv={};bad=False
for g,h,k,l in itertools.product(nz,repeat=4):
 terms=[(h,k,l),(mul(g,h),k,l),(g,mul(h,k),l),(g,h,mul(k,l)),(g,h,k)]
 rhs=(phi(*terms[0])-phi(*terms[1])+phi(*terms[2])-phi(*terms[3])+phi(*terms[4]))%16
 common.require(rhs%8==0,'base mod8 cocycle');mask=0;b=rhs//8
 for t in terms:
  if t in ind:mask^=1<<ind[t]
 while mask:
  j=mask.bit_length()-1
  if j not in piv:piv[j]=(mask,b);break
  m,c=piv[j];mask^=m;b^=c
 if not mask and b:bad=True;break
print('LIFT',not bad,'rank',len(piv),'seconds',time.monotonic()-start,flush=True)
if bad:
 (HERE/'semidihedral_lift_results.json').write_text(json.dumps(dict(lift_exists=False,scope='This chosen Z8 cocycle has no Z16 coefficient lift; no categorification exclusion.')));raise SystemExit
x=0
for j,(mask,b)in sorted(piv.items()):
 if (mask&x).bit_count()%2!=b:x^=1<<j
cor={k:8*((x>>i)&1)for k,i in ind.items()}
def omega(g,h,k):return(phi(g,h,k)+cor.get((g,h,k),0))%16
for g,h,k,l in itertools.product(E,repeat=4):common.require((omega(h,k,l)-omega(mul(g,h),k,l)+omega(g,mul(h,k),l)-omega(g,h,mul(k,l))+omega(g,h,k))%16==0,'lifted cocycle')
I=lambda a,b,c:int(c==a^b)if a<2 and b<2 else int(c==2)if (a==2)!=(b==2)else int(c<2)
labs=[(a,g)for a in range(3)for g in E if int(a==2)==g[0]%2];R=[[[I(a,b,c)*int(mul(g,h)==k)for c,k in labs]for b,h in labs]for a,g in labs]
def F(a,b,c,k):
 aa,bb,cc,kk=[labs[x][0]for x in(a,b,c,k)];v=omega(labs[a][1],labs[b][1],labs[c][1])
 if aa==cc==2 and bb!=2:v+=8*bb*kk
 if aa!=2 and bb==2 and cc!=2:v+=8*aa*cc
 return v%16
D=json.loads((BASE/'tensors.json').read_text());out=[]
for a in [0,1]:
 c=labs.index((a,(0,1)))
 if F(c,c,c,c):print('NONTRIVIAL ALGEBRA RESTRICTION',flush=True);continue
 M,info=bimodule.construct(R,F,c,q=16);hits=[]
 if M:
  for rid,T in D.items():
   if common.coarse(T)!=common.coarse(M):continue
   p=common.based_iso(T,M)
   if p is not None:hits.append(rid);out.append(dict(id=rid,source_labels=labs,source_tensor=R,source_omega=[[[omega(g,h,k)for k in E]for h in E]for g in E],generator=labs[c],model_tensor=M,basis_map=p,bimodules=info['objects']))
 print('MODEL',a,hits,flush=True)
(HERE/'semidihedral_lift_results.json').write_text(json.dumps(dict(lift_exists=True,models=out),indent=2))
