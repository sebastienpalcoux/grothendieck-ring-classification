"""Explicit finite cochain check of the Shapiro projection used in the proof."""
from pathlib import Path
import itertools,json
import ring_checks as common
HERE=Path(__file__).resolve().parent

def span_add(span,v):
 while v:
  k=v.bit_length()-1
  if k not in span:span[k]=v;return True
  v^=span[k]
 return False

def main():
 E=list(itertools.product(range(8),range(2)));zero=(0,0);nz=E[1:];pairs=list(itertools.product(nz,nz,range(2)));ind={k:i for i,k in enumerate(pairs)};out=[]
 for u in[7,3]:
  mul=lambda g,h:((g[0]+u**g[1]*h[0])%8,g[1]^h[1]);piv={}
  def bit(g,h,j):return 0 if zero in(g,h)else 1<<ind[g,h,j]
  for g,h,k,j in itertools.product(nz,nz,nz,range(2)):
   row=bit(h,k,j^(g[0]%2))^bit(mul(g,h),k,j)^bit(g,mul(h,k),j)^bit(g,h,j);span_add(piv,row)
  Z=[]
  for a in range(len(pairs)):
   if a in piv:continue
   v=1<<a
   for k,row in sorted(piv.items()):
    if(row&v).bit_count()%2:v^=1<<k
   Z.append(v)
  one=list(itertools.product(nz,range(2)));oi={k:i for i,k in enumerate(one)};B=[0]*len(one)
  for a,(g,h,j)in enumerate(pairs):
   for term in[(h,j^(g[0]%2)),(mul(g,h),j),(g,j)]:
    if term in oi:B[oi[term]]^=1<<a
  span={}
  for b in B:span_add(span,b)
  brank=len(span);H=[]
  for v in Z:
   if span_add(span,v):H.append(v)
  common.require(len(H)==3,'H2(U,swap module) dimension3');parameters=[]
  for bits in itertools.product(range(2),repeat=3):
   f=0
   for b,v in zip(bits,H):
    if b:f^=v
   def val(g,h):return 0 if zero in(g,h)else(f>>ind[g,h,0])&1
   r=(2,0);s=(0,1);r2=mul(r,r);r3=mul(r2,r);a=val(r,r)^val(r2,r)^val(r3,r);c=val(s,s);b=val(s,r)^val(mul(s,r),s)^c^val(r,r3);parameters.append([a,b,c])
  common.require(len({tuple(p)for p in parameters})==8,'Shapiro projection detects every central-extension class')
  out.append(dict(u=u,normalized_2cochain_variables=len(pairs),cocycle_rank=len(piv),cocycle_dimension=len(Z),coboundary_rank=brank,H2_dimension=3,central_extension_parameters=parameters,cohomology_representatives_hex=[hex(v)for v in H]))
 (HERE/'shapiro_check.json').write_text(json.dumps(dict(status='pass',records=out),indent=2)+'\n');print([(r['u'],r['H2_dimension'],r['central_extension_parameters'])for r in out])
if __name__=='__main__':main()
