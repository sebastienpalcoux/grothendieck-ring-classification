"""Fermionic associative zest of an Ising/pointed matched-grading category.
Tensor product X_g * Y_h = (X tensor Y tensor psi^{e(g,h)})_{gh}.
Explicit e=y cup z and nu=i^{y_g z_h z_k}(-1)^{y_g y_h z_h z_k}.
"""
from pathlib import Path
import itertools,json,sys
HERE=Path(__file__).resolve().parent;OLD=HERE.parents[1]/'prior_round/round3/d32'
sys.path.insert(0,str(OLD));import ring_checks as common,bimodule
DATA=json.loads((HERE.parents[1]/'prior_round/prior_round/evidence/rank12-m1-offline-20261025/tensors.json').read_text())
def inu(a,b,c):
 if a<2 and b<2:return int(c==a^b)
 if(a==2)!=(b==2):return int(c==2)
 return int(c<2)
def flip(a,p):return a^p if a<2 else 2
def ifphase(a,b,c,d):
 common.require(not(a==b==c==2),'scalar Ising associator premise')
 if a==c==2 and b<2:return 4*b*d
 if a<2 and b==2 and c<2:return 4*a*c
 return 0

def source(U,mul,degree,y,z):
 e=lambda g,h:y(g)*z(h)
 nu=lambda g,h,k:(2*y(g)*z(h)*z(k)+4*y(g)*y(h)*z(h)*z(k))%8
 for g,h,k,l in itertools.product(U,repeat=4):
  common.require((nu(h,k,l)-nu(mul(g,h),k,l)+nu(g,mul(h,k),l)-nu(g,h,mul(k,l))+nu(g,h,k)-4*e(g,h)*e(k,l))%8==0,'exact Gu-Wen trivialization')
 labs=[(a,g)for a in range(3)for g in U if int(a==2)==degree(g)]
 R=[[[inu(a,b,flip(c,e(g,h)))*int(mul(g,h)==k)for c,k in labs]for b,h in labs]for a,g in labs]
 common.validate(R)
 def F(i,j,k,o):
  a,g=labs[i];b,h=labs[j];c,ell=labs[k];d,v=labs[o]
  p=e(g,h);q=e(mul(g,h),ell);r=e(h,ell);s=e(g,mul(h,ell));t=flip(d,p^q)
  xs=[x for x in range(3)if inu(a,b,x)and inu(x,c,t)]
  zs=[z0 for z0 in range(3)if inu(b,c,z0)and inu(a,z0,t)]
  common.require(len(xs)==len(zs)==1,'unique scalar transport channel');x=xs[0];z0=zs[0];yp=flip(d,q);yr=flip(d,s)
  L=(ifphase(x,p,c,yp)+(0 if not p or c==0 else 4 if c==1 else 6)-ifphase(x,c,p,yp)+ifphase(t,p,q,d))%8
  B=ifphase(a,b,c,t)
  Rt=(-ifphase(a,z0,r,yr)+ifphase(t,r,s,d))%8
  return(L+B-Rt+nu(g,h,ell))%8
 return R,labs,F

def main():
 # U=D8 x C2, r^4=s²=t²=1, srs=r^-1.
 U=list(itertools.product(range(4),range(2),range(2)));mul=lambda g,h:((g[0]+(-1)**g[1]*h[0])%4,g[1]^h[1],g[2]^h[2]);degree=lambda g:g[0]%2
 out=[]
 chars=[v for v in itertools.product(range(2),repeat=3)if any(v)]
 for yy,zz in itertools.product(chars,repeat=2):
  y=lambda g:sum(a*b for a,b in zip(yy,(g[0]%2,g[1],g[2])))%2
  z=lambda g:sum(a*b for a,b in zip(zz,(g[0]%2,g[1],g[2])))%2
  if y((0,1,0))*z((0,1,0)):continue
  # Need an actual nonsplit even group (otherwise this repeats known source families).
  if all((y(g)*z(h)-y(h)*z(g))%2==0 for g,h in itertools.product(U,repeat=2)if not degree(g)and not degree(h)):continue
  R,labs,F=source(U,mul,degree,y,z);c=labs.index((0,(0,1,0)))
  try:M,info=bimodule.construct(R,F,c,q=8)
  except Exception as ex:print('FAIL',yy,zz,repr(ex),flush=True);raise
  hits=[]
  if M:
   for rid,T in DATA.items():
    if common.coarse(T)!=common.coarse(M):continue
    p=common.based_iso(T,M)
    if p is not None:
     hits.append(rid);out.append(dict(id=rid,y=yy,z=zz,source_tensor=R,source_labels=labs,source_F=[[[[F(i,j,k,o)if sum(int(labs[a][0]==2)for a in(i,j,k))<=2 and any(R[i][j][x]*R[x][k][o]for x in range(len(R)))else None for o in range(len(R))]for k in range(len(R))]for j in range(len(R))]for i in range(len(R))],model_tensor=M,basis_map=p,bimodules=info['objects']))
  print(yy,zz,hits,flush=True)
  (HERE/'fermionic_zest_results.json').write_text(json.dumps(out,indent=2))
if __name__=='__main__':main()
