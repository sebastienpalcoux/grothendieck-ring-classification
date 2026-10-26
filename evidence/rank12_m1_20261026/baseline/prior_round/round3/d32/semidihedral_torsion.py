"""All F2 third-cohomology twists of the accepted semidihedral cocycle lift."""
from pathlib import Path
import json,itertools
import semidihedral_lift as S
import ring_checks as common
import bimodule
HERE=Path(__file__).resolve().parent
# Exact quotient of the normalized mod2 cocycle space by mod2 coboundaries.
pairs=list(itertools.product(S.nz,repeat=2));pi={k:i for i,k in enumerate(pairs)};B=[0]*len(pairs)
for j,(g,h,k)in enumerate(S.keys):
 for p in [(h,k),(S.mul(g,h),k),(g,S.mul(h,k)),(g,h)]:
  if p in pi:B[pi[p]]^=1<<j
span={}
def reduce(v):
 while v:
  j=v.bit_length()-1
  if j not in span:break
  v^=span[j]
 return v
for v in B:
 v=reduce(v)
 if v:span[v.bit_length()-1]=v
brank=len(span);basis=[]
for j in range(S.n):
 if j in S.piv:continue
 x=1<<j
 for k,(mask,b)in sorted(S.piv.items()):
  if(mask&x).bit_count()%2:x^=1<<k
 v=reduce(x)
 if v:basis.append(x);span[v.bit_length()-1]=v
print('B3 rank',brank,'H3 F2 dimension',len(basis),flush=True)
common.require(len(basis)<6,'bounded tiny cohomology parameter set');out=[];attempts=[]
for bits in itertools.product(range(2),repeat=len(basis)):
 co=0
 for bit,v in zip(bits,basis):
  if bit:co^=v
 def omega(g,h,k):return(S.omega(g,h,k)+8*((co>>S.ind[g,h,k])&1)if(g,h,k)in S.ind else S.omega(g,h,k))%16
 for g,h,k,l in itertools.product(S.E,repeat=4):common.require((omega(h,k,l)-omega(S.mul(g,h),k,l)+omega(g,S.mul(h,k),l)-omega(g,h,S.mul(k,l))+omega(g,h,k))%16==0,'cohomology twist cocycle')
 def F(a,b,c,k):
  aa,bb,cc,kk=[S.labs[x][0]for x in(a,b,c,k)];v=omega(S.labs[a][1],S.labs[b][1],S.labs[c][1])
  if aa==cc==2 and bb!=2:v+=8*bb*kk
  if aa!=2 and bb==2 and cc!=2:v+=8*aa*cc
  return v%16
 c=S.labs.index((0,(0,1)))
 if F(c,c,c,c):continue
 M,info=bimodule.construct(S.R,F,c,q=16);hits=[]
 for rid,T in S.D.items():
  if common.coarse(T)!=common.coarse(M):continue
  p=common.based_iso(T,M)
  if p is not None:
   hits.append(rid)
   if rid not in [r['id']for r in out]:out.append(dict(id=rid,cohomology_bits=bits,source_labels=S.labs,source_tensor=S.R,source_omega=[[[omega(g,h,k)for k in S.E]for h in S.E]for g in S.E],generator=S.labs[c],model_tensor=M,basis_map=p,bimodules=info['objects']))
 print('TWIST',bits,hits,flush=True);attempts.append(dict(bits=bits,matches=hits))
 (HERE/'semidihedral_torsion_results.json').write_text(json.dumps(dict(models=out,attempts=attempts,mod2_cohomology_dimension=len(basis)),indent=2))
