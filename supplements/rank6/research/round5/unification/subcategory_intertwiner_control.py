"""Exact nontrivial subgroup controls for modular central projection.

For Vec(H) inside Vec(S3), construct double characters by finite group sums
and central projection multiplicities by restriction to the H-graded fibres.
H=C2 gives a full-rank rectangular intertwiner. H=C3 demonstrates that its
rank need not equal the rank of Z(H), so full subrepresentation subtraction
must never be assumed from a fusion-subcategory inclusion alone.
"""
import hashlib,itertools,json,sys
from pathlib import Path
import sympy as s
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'software'))
from exact import field,evaluate,require


def main():
 C=field(s.Poly(s.cyclotomic_poly(6,s.Symbol('t')),s.Symbol('t')));z=C.unit
 bar=lambda x:evaluate(x.to_list(),z**5,C)
 G=list(itertools.permutations(range(3)));one=(0,1,2);trans=(1,0,2);cycle=(1,2,0)
 mul=lambda a,b:tuple(a[b[i]] for i in range(3))
 inv=lambda a:tuple(a.index(i) for i in range(3))
 def power(g,r):
  v=one
  for _ in range(r):v=mul(v,g)
  return v
 reps=[one,trans,cycle];centralizers=[[h for h in G if mul(g,h)==mul(h,g)]for g in reps]
 def chi(a,k,h):
  require(h in centralizers[a],'centralizer character domain')
  if a==0:
   if k==0:return C.one
   if k==1:return C((-1)**sum(h[i]>h[j]for i in range(3)for j in range(i+1,3)))
   return C(sum(h[i]==i for i in range(3))-1)
  m=len(centralizers[a]);r=next(r for r in range(m)if power(reps[a],r)==h)
  return z**((6//m)*k*r)
 objects=[(a,k)for a,m in enumerate((3,2,3))for k in range(m)]
 S=[]
 for a,k in objects:
  row=[];g=reps[a]
  for b,l in objects:
   h=reps[b];value=C.zero
   for x in G:
    hx=mul(mul(x,h),inv(x))
    if mul(g,hx)!=mul(hx,g):continue
    gx=mul(mul(inv(x),g),x);value+=bar(chi(a,k,hx))*bar(chi(b,l,gx))
   row.append(value/C(len(centralizers[a])*len(centralizers[b])))
  S.append(row)
 dims=[C(6)*S[0][j]for j in range(len(objects))]
 twists=[chi(a,k,reps[a])/chi(a,k,one)for a,k in objects]
 controls=[]
 for generator,m in ((trans,2),(cycle,3)):
  H=[power(generator,r)for r in range(m)];HO=list(itertools.product(range(m),repeat=2))
  def eta(k,h):return z**((6//m)*k*H.index(h))
  SH=[[bar(eta(k,H[q]))*bar(eta(l,H[r]))/C(m)for q,l in HO]for r,k in HO]
  TH=[eta(k,H[r])for r,k in HO];B=[]
  for r,k in HO:
   h=H[r];row=[]
   for a,l in objects:
    x=next((x for x in G if mul(mul(x,reps[a]),inv(x))==h),None)
    value=C.zero if x is None else sum((bar(eta(k,u))*chi(a,l,mul(mul(inv(x),u),x))for u in H),C.zero)/C(m)
    co=value.to_list();require(not co or(len(co)==1 and co[0].denominator==1 and co[0]>=0),'nonintegral central restriction multiplicity')
    row.append(int(co[0])if co else 0)
   B.append(row)
  require(all(sum((SH[i][j]*C(B[j][k])for j in range(len(HO))),C.zero)==sum((C(B[i][j])*S[j][k]for j in range(len(objects))),C.zero)for i in range(len(HO))for k in range(len(objects))),'rectangular normalized S intertwiner')
  require(all(C(B[i][j])*TH[i]==C(B[i][j])*twists[j]for i in range(len(HO))for j in range(len(objects))),'T intertwiner')
  require([row[0]for row in B]==[int(i==0)for i in range(len(HO))],'unit column')
  require(all(sum((C(a)*b for a,b in zip(row,dims)),C.zero)==C(s.Rational(6,m))for row in B),'individual central-simple mass')
  rank=s.Matrix(B).rank();require(rank==(4 if m==2 else 5),'restriction rank control')
  bad=[list(row)for row in B];bad[0][0]+=1
  failures=sum(sum((SH[i][j]*C(bad[j][k])for j in range(len(HO))),C.zero)!=sum((C(bad[i][j])*S[j][k]for j in range(len(objects))),C.zero)for i in range(len(HO))for k in range(len(objects)))
  require(failures>0,'mutation did not violate S intertwining')
  controls.append(dict(subgroup_order=m,center_rank=m*m,projection_matrix=B,projection_rank=int(rank),S_equations=len(HO)*len(objects),T_equations=len(HO)*len(objects),individual_mass=str(s.Rational(6,m)),mutation_S_failures=failures))
 files=[Path(__file__).resolve(),ROOT/'software/exact.py']
 out=dict(passed=True,optimizer_used=False,optimized_python=not __debug__,ambient='Vec(S3)',modular_data_source='finite centralizer character sums',projection_source='centralizer character restriction on subgroup-graded fibres',controls=controls,full_projection_rank_not_assumed=True,files_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()for p in files})
 Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out),flush=True)

if __name__=='__main__':main()
