"""Necessary mod-four associativity constraints on multiplicity-one lifts.

No categorical exclusion from this scan alone.  Linear sign equations are
computed independently of the frozen signed engine, without changing it.
"""
from pathlib import Path
import itertools,json,sys,time
BASE=Path(__file__).resolve().parents[2]/'rank12-m1-offline-20261025'
sys.path.insert(0,str(BASE/'sources/work/rank11'))
import common

def system(R,normalize_indicators=False):
 n=len(R);du=common.dual(R);unseen=set(itertools.product(range(1,n),repeat=3));orbits=[];mapping={}
 while unseen:
  tri=min(unseen);a,b,c=tri;rev=(du[c],du[b],du[a]);orb=sorted({tri,(b,c,a),(c,a,b),rev,(rev[1],rev[2],rev[0]),(rev[2],rev[0],rev[1])});unseen.difference_update(orb)
  if not R[a][b][du[c]]:continue
  v=len(orbits);orbits.append(orb)
  for i,j,k in orb:mapping[i,j,du[k]]=v
 def bit(i,j,k):
  v=mapping.get((i,j,k));return 0 if v is None else 1<<v
 eqs=set()
 for i,j,k,l in itertools.product(range(n),repeat=4):
  eq=0
  for p in range(n):
   if R[i][j][p] and R[p][k][l]:eq^=bit(i,j,p)^bit(p,k,l)
   if R[j][k][p] and R[i][p][l]:eq^=bit(j,k,p)^bit(i,p,l)
  if eq:eqs.add(eq)
 if normalize_indicators:
  for i in range(1,n):
   if du[i]!=i:continue
   for j in range(1,n):
    if R[j][du[j]][i]:eqs.add(bit(j,du[j],i))
 piv={}
 for row in sorted(eqs):
  while row:
   v=row.bit_length()-1
   if v in piv:row^=piv[v]
   else:piv[v]=row;break
 free=[v for v in range(len(orbits))if v not in piv];basis=[]
 for v in free:
  x=1<<v
  for w,row in sorted(piv.items()):
   if (row&x).bit_count()%2:x^=1<<w
  common.require(all((row&x).bit_count()%2==0 for row in eqs),'kernel check');basis.append(x)
 # Every change of signs of simple basis elements is a valid associative lift.
 gauge=[];gpiv={};seen_orbits=set()
 for i in range(1,n):
  if i in seen_orbits:continue
  label_orbit={i,du[i]};seen_orbits.update(label_orbit)
  x=0
  for v,orb in enumerate(orbits):
   a,b,c=orb[0]
   if sum(z in label_orbit for z in (a,b,c))%2:x|=1<<v
  gauge.append((x,sum(1<<j for j in label_orbit)))
 for x,eps in gauge:
  while x:
   j=x.bit_length()-1
   if j in gpiv:x^=gpiv[j][0];eps^=gpiv[j][1]
   else:gpiv[j]=(x,eps);break
 gauge_witnesses=[]
 for original in basis:
  x=original;eps=0
  while x:
   j=x.bit_length()-1
   if j not in gpiv:break
   x^=gpiv[j][0];eps^=gpiv[j][1]
  if x:gauge_witnesses.append(None)
  else:
   signs=[-1 if eps>>j&1 else 1 for j in range(n)]
   common.require(all(bool(original>>v&1)==(signs[a]*signs[b]*signs[c]==-1)for v,orb in enumerate(orbits)for a,b,c in orb),'gauge witness')
   gauge_witnesses.append(signs)
 return dict(variable_count=len(orbits),equation_count=len(eqs),rank=len(piv),kernel_dimension=len(free),normalized_indicators=normalize_indicators,kernel_basis=[hex(x)for x in basis],kernel_in_basis_gauges=all(v is not None for v in gauge_witnesses),gauge_witnesses=gauge_witnesses),(orbits,mapping,eqs,piv,basis)

if __name__=='__main__':
 data=json.loads((BASE/'tensors.json').read_text());out=[]
 for i in (63,64,215,365,332,350,561,623,628):
  for normalize in (False,True):
   start=time.monotonic();q,_=system(data[f'R12_1_{i}'],normalize);q.update(id=f'R12_1_{i}',seconds=time.monotonic()-start);out.append(q);print({k:v for k,v in q.items()if k!='kernel_basis'},flush=True)
 (Path(__file__).resolve().parent/'signed_mod4.json').write_text(json.dumps(out,indent=2)+'\n')
