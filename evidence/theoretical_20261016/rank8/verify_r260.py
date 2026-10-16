import gzip,json,hashlib,itertools
from pathlib import Path
import argparse
parser=argparse.ArgumentParser()
parser.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[3])
base=parser.parse_args().repo.resolve()
flat=lambda R:tuple(v for a in R for b in a for v in b)
rows=[json.loads(x.replace('{','[').replace('}',']')) for x in gzip.open(base/'supplements/rank8/data/rank8_tables.txt.gz','rt')]
R=sorted([R for R in rows if max(flat(R))==2],key=flat)[259]
def need(v,msg):
 if not v:raise ValueError(msg)
sha=hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()
ledger={x['id']:x for x in json.load(open(base/'supplements/rank8/data/decisions.json'))}
need(sha==ledger['R8_2_260']['tensor_sha256'],'source')
ds=[(1,0)]*3+[(3,2)]*4+[(3,0)]
mul=lambda x,y:(x[0]*y[0]+3*x[1]*y[1],x[0]*y[1]+x[1]*y[0])
for i,j in itertools.product(range(8),repeat=2):
 need(mul(ds[i],ds[j])==tuple(sum(R[i][j][k]*ds[k][a] for k in range(8)) for a in (0,1)),'dimension character')
for i,j in itertools.product(range(3),repeat=2):need(R[i][j][(i+j)%3]==1 and sum(R[i][j])==1,'C3')
for g in range(3):
 for i in range(3,8):need(R[g][i][i]==R[i][g][i]==1 and sum(R[g][i])==sum(R[i][g])==1,'fixed on both sides')
E=[0,1,2,7]
need(all(R[i][j][k]==0 for i in E for j in E for k in range(8) if k not in E),'subcategory')
need(R[7][7]==[1,1,1,0,0,0,0,2],'C3+2')
need(mul((3,2),(3,2))==(21,12),'quadratic identity')
# All nontrivial alternating bicharacters of C3^2 are nondegenerate.
need(all(sum(1 for a,b in itertools.product(range(3),repeat=2) if all((c*(a*y-b*x))%3==0 for x,y in itertools.product(range(3),repeat=2)))==1 for c in [1,2]),'projective dimensions')
# A4 as even permutations; all order3 subgroups fail normality.
perms=list(itertools.permutations(range(4)))
sgn=lambda p:sum(p[i]>p[j] for i in range(4) for j in range(i+1,4))%2
G=[p for p in perms if sgn(p)==0];one=tuple(range(4))
pm=lambda a,b:tuple(a[b[i]] for i in range(4))
pi=lambda a:tuple(a.index(i) for i in range(4))
order3=[p for p in G if p!=one and pm(pm(p,p),p)==one]
need(len(order3)==8,'A4 3cycles')
need(all(any(pm(pm(h,p),pi(h)) not in {one,p,pm(p,p)} for h in G) for p in order3),'no normal C3')
print(json.dumps({'status':'PASS','id':'R8_2_260','source_sha256':sha,'scope':'general categorical implication subject to cited theorem audit','E':E,'pointed_subgroup':[0,1,2],'dimension':'3+2sqrt3','split_dimension_norm':'-1/3','dual_pointed_group':'A4','dual_noninvertible_count':4,'stabilizer_order':3,'contradiction':'no normal subgroup of order3 in A4'},indent=2))
