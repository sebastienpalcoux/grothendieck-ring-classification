"""Exact source hypotheses for cyclic-stabilizer/Morita exclusions260,380,673."""
import gzip,json,hashlib,itertools,argparse
from pathlib import Path
from fractions import Fraction as F
parser=argparse.ArgumentParser();parser.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[3]);base=parser.parse_args().repo.resolve()
flat=lambda R:tuple(v for a in R for b in a for v in b)
rows=[json.loads(x.replace('{','[').replace('}',']')) for x in gzip.open(base/'supplements/rank8/data/rank8_tables.txt.gz','rt')]
rows=sorted([R for R in rows if max(flat(R))==2],key=flat)
ledger={x['id']:x for x in json.load(open(base/'supplements/rank8/data/decisions.json'))}
def need(v,msg):
 if not v:raise ValueError(msg)
reports=[]
for index,g,E,ds in [(380,3,[0,3,4,5],[(1,0),(4,1),(4,1),(1,0),(2,0),(2,0),(3,2),(3,2)]),(673,1,[0,1,6,7],[(1,0),(1,0),(4,1),(3,2),(3,2),(4,1),(2,0),(2,0)])]:
 R=rows[index-1];id=f'R8_2_{index}';sha=hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest();need(sha==ledger[id]['tensor_sha256'],'source')
 mul=lambda a,b:(a[0]*b[0]+6*a[1]*b[1],a[0]*b[1]+a[1]*b[0])
 for i,j in itertools.product(range(8),repeat=2):need(mul(ds[i],ds[j])==tuple(sum(R[i][j][k]*ds[k][a] for k in range(8)) for a in (0,1)),'FP character')
 need(all(a>0 and b>=0 for a,b in ds),'positive')
 need(all(R[i][j][k]==0 for i in E for j in E for k in range(8) if k not in E),'subcategory')
 x,y=E[2:];need(R[g][g][0]==1 and sum(R[g][g])==1,'order2')
 for z in [x,y]:need(R[g][z][z]==R[z][g][z]==1 and sum(R[g][z])==sum(R[z][g])==1,'fixed dimension-two labels')
 need(R[x][x][0]==R[x][x][g]==R[x][x][y]==1 and sum(R[x][x])==3,'RepD5 X2')
 need(R[y][y][0]==R[y][y][g]==R[y][y][x]==1 and sum(R[y][y])==3,'RepD5 Y2')
 need(R[x][y][x]==R[x][y][y]==1 and sum(R[x][y])==2,'RepD5 XY')
 outside=[i for i in range(8) if i not in E];orbits=[]
 while outside:
  i=outside[0];j=R[g][i].index(1);need(j!=i and j in outside and R[i][g].index(1)==j,'free matching left/right orbit');need(ds[i]==ds[j],'equaldims');orbits.append([i,j]);outside.remove(i);outside.remove(j)
 need({ds[o[0]] for o in orbits}=={(4,1),(3,2)},'two dimensions')
 need(F(4*4-6,25)==F(2,5) and F(3*3-6*4,25)==F(-3,5),'norms')
 need(8%5!=0,'coefficient contradiction')
 reports.append({'id':id,'source_sha256':sha,'g':g,'E':E,'outside_orbits':orbits,'dual_group':'D10','dual_noninvertible_dimensions':['x','x','y','y'],'x':'4+sqrt6','y':'3+2sqrt6','norm_x_over5':'2/5','norm_y_over5':'-3/5','impossible_equation':'b+2c=8 with5 dividingb,c'})
# Direct R260 witness, independent of A4 identification.
R=rows[259];sha=hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest();need(sha==ledger['R8_2_260']['tensor_sha256'],'source260')
ds=[(1,0),(1,0),(1,0),(3,2),(3,2),(3,2),(3,2),(3,0)]
mul=lambda a,b:(a[0]*b[0]+3*a[1]*b[1],a[0]*b[1]+a[1]*b[0])
for i,j in itertools.product(range(8),repeat=2):need(mul(ds[i],ds[j])==tuple(sum(R[i][j][k]*ds[k][a] for k in range(8)) for a in (0,1)),'FP character260')
need(all(a>0 and b>=0 for a,b in ds),'positive260')
need(R[1][1][2]==R[1][2][0]==R[2][1][0]==R[2][2][1]==1,'C3 group260')
need(all(sum(R[g][h])==1 for g,h in itertools.product(range(3),repeat=2)),'invertible group260')
for g in range(3):need(R[g][3][3]==R[3][g][3]==1,'fixed260')
need(R[3][3][3]==2,'witness260')
need(F(9-12,9)==F(-1,3),'norm260')
reports.append({'id':'R8_2_260','source_sha256':sha,'cyclic_subgroup':[0,1,2],'X_Y_Z':3,'multiplicity':2,'required_divisor':3,'dimension':'3+2sqrt3','norm_dimension_over3':'-1/3'})
print(json.dumps({'status':'PASS','categorical_scope':'general complex categories; proof in CYCLIC_STABILIZER_DIVISIBILITY.md','cases':reports},indent=2))
