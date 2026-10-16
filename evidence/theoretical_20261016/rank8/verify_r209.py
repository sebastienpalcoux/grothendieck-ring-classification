import gzip,json,hashlib,itertools
from pathlib import Path
from fractions import Fraction as F
import argparse
parser=argparse.ArgumentParser()
parser.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[3])
base=parser.parse_args().repo.resolve()
flat=lambda R:tuple(v for a in R for b in a for v in b)
rows=[json.loads(x.replace('{','[').replace('}',']')) for x in gzip.open(base/'supplements/rank8/data/rank8_tables.txt.gz','rt')]
R=sorted([R for R in rows if max(flat(R))==2],key=flat)[208]
def need(v,msg):
 if not v:raise ValueError(msg)
sha=hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()
ledger={x['id']:x for x in json.load(open(base/'supplements/rank8/data/decisions.json'))}
need(sha==ledger['R8_2_209']['tensor_sha256'],'source')
ds=[(F(1),F(0))]*3+[(F(5,2),F(1,2)),(F(3,2),F(1,2)),(F(7,2),F(1,2)),(F(5,2),F(1,2)),(F(5,2),F(1,2))]
mul=lambda a,b:(a[0]*b[0]+29*a[1]*b[1],a[0]*b[1]+a[1]*b[0])
for i,j in itertools.product(range(8),repeat=2):need(mul(ds[i],ds[j])==tuple(sum(R[i][j][k]*ds[k][a] for k in range(8)) for a in (0,1)),'dimension character')
need(all(a>0 and b>=0 for a,b in ds),'positive dimensions')
for i,j in itertools.product(range(3),repeat=2):need(R[i][j][(i+j)%3]==1 and sum(R[i][j])==1,'C3 subcategory')
D=tuple(sum(mul(d,d)[a] for d in ds) for a in (0,1))
need(D==(F(145,2),F(25,2)),'global FPdim')
trace=2*D[0]/3;need(trace.denominator!=1,'nonintegral trace')
print(json.dumps({'status':'PASS','id':'R8_2_209','tensor_sha256':sha,'positive_dimension_vector':['1','1','1','d','d-1','d+1','d','d'],'d':'(5+sqrt29)/2','pointed_subcategory':[0,1,2],'global_FPdim':'(145+25sqrt29)/2','index_trace':str(trace),'categorical_scope':'general complex fusion category','criterion':'ENO Proposition8.15'},indent=2))
