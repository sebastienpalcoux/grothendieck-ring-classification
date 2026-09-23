"""Source- and construction-based positive models added at multiplicities 6 and 7.

The model tensors are constructed without reading the census. Existence of
AH1 is a cited subfactor input. The order-72 model is an explicit finite group.
"""
import itertools,json
from pathlib import Path
from functools import lru_cache
from fractions import Fraction as Q
from exact import require
from rings import validate,permute
from prepare import key
from existence import all_values
P=Path(__file__).resolve().parents[1]

@lru_cache(None)
def asaeda_haagerup():
 # Grossman--Snyder, arXiv:1202.4396v2, p.27, Table 1.
 # Source order (1,psi,chi,sigma,zeta,tau); Lambda=psi+chi+sigma+zeta+tau.
 n=6;R=[[[0]*n for _ in range(n)] for _ in range(n)]
 for i in range(n):R[0][i][i]=R[i][0][i]=1
 upper=[
  (1,1,[1,1,0,0,1,0]),(1,2,[0,0,1,0,0,1]),
  (1,3,[0,0,0,0,1,1]),(1,4,[0,1,0,1,1,1]),(1,5,[0,0,1,1,1,2]),
  (2,2,[1,1,1,0,0,1]),(2,3,[0,0,0,1,1,1]),(2,4,[0,0,0,1,1,2]),(2,5,[0,1,1,1,2,2]),
  (3,3,[1,0,1,1,1,1]),(3,4,[0,1,1,1,1,2]),(3,5,[0,1,1,1,2,3]),
  (4,4,[1,1,1,1,2,3]),(4,5,[0,1,2,2,3,4]),(5,5,[1,2,2,3,4,6])]
 for i,j,v in upper:R[i][j]=v[:];R[j][i]=v[:]
 validate(R);return R

def mm(a,b):return tuple(sum(a[2*i+k]*b[2*k+j] for k in range(2))%3 for i in range(2) for j in range(2))
def mv(a,v):return tuple(sum(a[2*i+k]*v[k] for k in range(2))%3 for i in range(2))

@lru_cache(None)
def frobenius72():
 E=(1,0,0,1);I=(0,1,2,0);J=(1,1,1,2);H={E};queue=[E]
 while queue:
  x=queue.pop()
  for y in (I,J):
   z=mm(x,y)
   if z not in H:H.add(z);queue.append(z)
 H=sorted(H);require(len(H)==8,'quaternion matrix group size');Z=mm(I,I)
 require(Z==mm(J,J) and mm(Z,Z)==E and mm(J,I)==mm(Z,mm(I,J)),'quaternion relations')
 V=list(itertools.product(range(3),repeat=2))
 require(all(len({mv(h,v) for h in H})==8 for v in V if v!=(0,0)),'action not regular on nonzero vectors')
 elements=list(itertools.product(V,H));ix={x:i for i,x in enumerate(elements)}
 def mul(x,y):
  v,h=x;w,k=y;u=mv(h,w)
  return (tuple((v[a]+u[a])%3 for a in range(2)),mm(h,k))
 multiplication=[[ix[mul(x,y)] for y in elements] for x in elements];unit=ix[((0,0),E)]
 require(all(multiplication[unit][i]==multiplication[i][unit]==i for i in range(72)),'group unit')
 require(all(any(multiplication[i][j]==multiplication[j][i]==unit for j in range(72)) for i in range(72)),'inverse absent')
 require(all(multiplication[multiplication[i][j]][k]==multiplication[i][multiplication[j][k]] for i in range(72) for j in range(72) for k in range(72)),'group associativity')
 parity={E:(0,0),Z:(0,0),I:(1,0),mm(Z,I):(1,0),J:(0,1),mm(Z,J):(0,1),mm(I,J):(1,1),mm(Z,mm(I,J)):(1,1)}
 require(len(parity)==8 and all(tuple((parity[h][a]+parity[k][a])%2 for a in range(2))==parity[mm(h,k)] for h in H for k in H),'abelianization signs')
 chars=[]
 for signs in [(0,0),(1,0),(0,1),(1,1)]:chars.append([(-1)**sum(a*b for a,b in zip(signs,parity[h])) for v,h in elements])
 chars.append([2 if h==E else -2 if h==Z else 0 for v,h in elements])
 chars.append([8 if v==(0,0) and h==E else -1 if h==E else 0 for v,h in elements])
 require(all(sum(chars[a][j]*chars[b][j] for j in range(72))==72*int(a==b) for a in range(6) for b in range(6)),'character orthogonality')
 require(sum(c[unit]**2 for c in chars)==72,'character degree-square sum')
 R=[]
 for a in range(6):
  rows=[]
  for b in range(6):
   coeff=[Q(sum(chars[a][j]*chars[b][j]*chars[c][j] for j in range(72)),72) for c in range(6)]
   require(all(x.denominator==1 and x>=0 for x in coeff),'nonintegral tensor product')
   rows.append(list(map(int,coeff)))
  R.append(rows)
 validate(R);return R

def examples():
 yield 'Asaeda-Haagerup AH1',asaeda_haagerup(),'Grossman--Snyder, arXiv:1202.4396v2, Table 1 (p.27)',all_values('yes')
 yield 'Rep((C3 x C3) semidirect Q8)',frobenius72(),'Explicit matrix semidirect product and little-group character construction',all_values('yes')

def build_records():
 census=json.loads((P/'data/census.json').read_text());idx={key(r['N']):r for r in census};out=[]
 for name,R,ref,e in examples():
  target=idx.get(key(R));require(target is not None,'constructed model absent from census')
  permutations=[(0,)+p for p in itertools.permutations(range(1,6)) if permute(R,(0,)+p)==target['N']]
  require(permutations,'model permutation absent')
  out.append(dict(id=target['id'],name=name,N=R,reference=ref,existence=e,census_permutation=list(permutations[0])))
 (P/'data/through7_positive_models.json').write_text(json.dumps(out,separators=(',',':'))+'\n')
 return out

def verify():
 stored=json.loads((P/'data/through7_positive_models.json').read_text());built={name:(R,ref,e) for name,R,ref,e in examples()};idx={r['id']:r['N'] for r in json.loads((P/'data/census.json').read_text())}
 require(len(stored)==len(built)==2 and {r['name'] for r in stored}==set(built),'new registry incomplete')
 for rec in stored:
  R,ref,e=built[rec['name']];require(R==rec['N'] and ref==rec['reference'] and e==rec['existence'],'model source/structure mismatch')
  require(permute(R,tuple(rec['census_permutation']))==idx[rec['id']],'full-tensor model mismatch')
 return {'passed':True,'new_models':len(stored),'checked_structure_constants':216*len(stored),'explicit_group_order':72}
if __name__=='__main__':print(json.dumps(build_records(),indent=2))
