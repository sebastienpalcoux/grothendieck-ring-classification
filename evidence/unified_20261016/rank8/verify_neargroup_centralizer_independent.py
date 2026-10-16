"""Independent integer derivation from Evans--Gannon Proposition 7(b)."""
import gzip,json,itertools,hashlib,argparse
from pathlib import Path

def require(ok,msg):
 if not ok:raise ValueError(msg)
flat=lambda r:tuple(x for a in r for row in a for x in row)
ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);root=ap.parse_args().repo.resolve()
rows=[json.loads(l.replace('{','[').replace('}',']')) for l in gzip.open(root/'supplements/rank8/data/rank8_tables.txt.gz','rt')]
source=sorted([r for r in rows if max(flat(r))==2],key=flat)
results=[]
for group,j in [('C3xC3',820),('C9',869)]:
 if group=='C3xC3':
  elements=list(itertools.product(range(3),repeat=2));zero=(0,0)
  add=lambda a,b:tuple((x+y)%3 for x,y in zip(a,b));neg=lambda a:tuple(-x%3 for x in a)
 else:
  elements=list(range(9));zero=0;add=lambda a,b:(a+b)%9;neg=lambda a:-a%9
 reps=sorted({min(a,neg(a)) for a in elements if a!=zero})
 def sum3(a,b,c):return add(add(a,b),c)
 def coeff(i,j,k):
  x=sorted([i,j,k])
  if x[0]==0:return int(x[1]==x[2])
  if x[0]==1:
   if x[1]==1:return 1
   if x[1]<4 and x[2]<4:return 1+int(x[1]==x[2])
   if x[1]<4:return 1
   return 1-int(x[1]==x[2])
  if x[0]<4:
   if x[2]<4:
    a,b,c=[y-1 for y in x]
    return 1+sum(int((a+sb*b+sc*c)%5==0) for sb in [1,-1] for sc in [1,-1])
   return 1
  a,b,c=[reps[y-4] for y in x]
  return 1-sum(int(sum3(a,b if sb==1 else neg(b),c if sc==1 else neg(c))==zero) for sb in [1,-1] for sc in [1,-1])
 model=[[[coeff(i,j,k) for k in range(8)] for j in range(8)] for i in range(8)]
 require(all(x>=0 for x in flat(model)),'positivity')
 require(all(sum(model[a][b][e]*model[e][c][d] for e in range(8))==sum(model[b][c][e]*model[a][e][d] for e in range(8)) for a,b,c,d in itertools.product(range(8),repeat=4)),'associativity')
 target=source[j-1];maps=[]
 digest=hashlib.sha256(json.dumps(target,separators=(',',':')).encode()).hexdigest()
 require(digest=={820:'88d4e0d03d1f45b727bb5d973ee4c47ef114ff4870f397d9f08342d5db1d0373',869:'6fd67687c6a4590e43cf539442042092ebc28973b626127f40d6f27fb66de112'}[j],'immutable source digest')
 for tail in itertools.permutations(range(1,8)):
  p=(0,)+tail
  if all(model[i][k][h]==target[p[i]][p[k]][p[h]] for i,k,h in itertools.product(range(8),repeat=3)):maps.append(p)
 require(maps,'source identification')
 results.append({'status':'PASS','group_prime':group,'source_id':'R8_2_'+str(j),'tensor_sha256':hashlib.sha256(json.dumps(target,separators=(',',':')).encode()).hexdigest(),'gamma_representatives':reps,'model_basis':['a0','b0','c_1,-1','c_2,-2']+['d_0,'+str(x) for x in reps],'model_to_source_map':maps[0],'number_of_basis_maps':len(maps),'coefficient_source':'Evans--Gannon 1208.1500 Proposition7(b) printed all-lowered fusion coefficients; all eight centralizer objects self-dual'})
print(json.dumps(results,indent=2))
