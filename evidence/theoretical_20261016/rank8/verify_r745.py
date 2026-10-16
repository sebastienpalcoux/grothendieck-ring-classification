import gzip,json,hashlib,itertools
from pathlib import Path
import argparse
parser=argparse.ArgumentParser()
parser.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[3])
base=parser.parse_args().repo.resolve()
flat=lambda R:tuple(v for a in R for b in a for v in b)
rows=[json.loads(x.replace('{','[').replace('}',']')) for x in gzip.open(base/'supplements/rank8/data/rank8_tables.txt.gz','rt')]
R=sorted([R for R in rows if max(flat(R))==2],key=flat)[744]
def need(v,msg):
 if not v:raise ValueError(msg)
sha=hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()
ledger={x['id']:x for x in json.load(open(base/'supplements/rank8/data/decisions.json'))}
need(sha==ledger['R8_2_745']['tensor_sha256'],'source')
ds=[(1,0),(1,0),(1,1),(1,1),(2,0),(2,0),(2,2),(2,2)]
mul=lambda x,y:(x[0]*y[0]+2*x[1]*y[1],x[0]*y[1]+x[1]*y[0])
for i,j in itertools.product(range(8),repeat=2):
 need(mul(ds[i],ds[j])==tuple(sum(R[i][j][k]*ds[k][a] for k in range(8)) for a in (0,1)),'dimension character')
need([row.index(1) for row in R[1]]==[1,0,3,2,4,5,6,7],'left action')
need([R[i][1].index(1) for i in range(8)]==[1,0,3,2,4,5,6,7],'right action')
for subset in [[0,1,2,3],[0,1,4,5]]:
 need(all(R[i][j][k]==0 for i in subset for j in subset for k in range(8) if k not in subset),'closed subring')
need(R[2][2]==[1,0,1,1,0,0,0,0],'PSU6 square')
need(R[4][4]==[1,1,0,0,0,1,0,0] and R[5][5]==[1,1,0,0,1,0,0,0] and R[4][5]==[0,0,0,0,1,1,0,0],'RepD5')
# Fixed-object V4-projective blocks: four 1D or one 2D.
counts=[2+4*a+4*b for a,b in itertools.product([0,1],repeat=2)]
need(sorted(set(counts))==[2,6,10],'count alternatives')
need([a for a in counts if a%10==0]==[10],'free orbit divisibility')
# D10 = pairs (rotation mod5, reflection mod2); no normal order2 subgroup.
G=list(itertools.product(range(5),range(2)))
def gm(x,y):return ((x[0]+(-1)**x[1]*y[0])%5,(x[1]+y[1])%2)
def gi(x):return next(y for y in G if gm(x,y)==(0,0))
ord2=[x for x in G if x!=(0,0) and gm(x,x)==(0,0)]
need(len(ord2)==5,'reflections')
need(all(any(gm(gm(y,x),gi(y))!=x for y in G) for x in ord2),'no normal C2')
print(json.dumps({'status':'PASS','id':'R8_2_745','source_sha256':sha,'scope':'general categorical implication subject to cited theorem audit','D':[0,1,2,3],'E':[0,1,4,5],'g':1,'initial_dimensions':['1','1','d','d','2','2','2d','2d'],'d':'1+sqrt2','dual_d_count_alternatives':sorted(set(counts)),'surviving_dual_d_count':10,'dual_pointed_group':'D10','contradiction':'adjoint invertibles would form normal order2 subgroup of D10'},indent=2))
