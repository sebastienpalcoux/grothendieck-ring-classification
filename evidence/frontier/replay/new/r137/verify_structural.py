"""Short independent tensor/character/rotation checks; no optimizer."""
from pathlib import Path
import importlib.util,hashlib,json,itertools
from fractions import Fraction as Q
P=Path(__file__).resolve().parents[2]/'prior/data/current_remaining_cases.py'
spec=importlib.util.spec_from_file_location('data',P);data=importlib.util.module_from_spec(spec);spec.loader.exec_module(data)
R=data.TENSORS['R9_2_137'];n=9
sha=hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()
assert sha=='c509d23c9a638aaea8a624a6c5186ad3f0c1b6e6f432576b45300f6e630c56e6'
def mul(x,y):return (x[0]*y[0]+2*x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def closure(S):
 S=set(S)|{0}
 while True:
  T=S|{k for i in S for j in S for k in range(n) if R[i][j][k]}
  if T==S:return S
  S=T
chars=[]
for sg in [-1,1]:chars.append([(1,0),(1,0),(1,0),(4,sg*3),(4,sg*3),(4,sg*3),(4,sg*3),(1,0),(2,0)])
for sg in [-1,1]:chars.append([(1,0),(1,0),(1,0),(0,sg),(0,-sg),(0,-sg),(0,sg),(1,0),(-2,0)])
for sg in [-1,1]:chars.append([(1,0),(-1,0),(-1,0),(0,sg),(0,0),(0,0),(0,-sg),(1,0),(0,0)])
for sg in [-1,1]:chars.append([(1,0),(-1,0),(1,0),(0,0),(0,sg),(0,-sg),(0,0),(-1,0),(0,0)])
chars.append([(1,0),(1,0),(-1,0),(0,0),(0,0),(0,0),(0,0),(-1,0),(0,0)])
assert len({tuple(c)for c in chars})==9
for c in chars:
 for i,j in itertools.product(range(n),repeat=2):
  assert mul(c[i],c[j])==tuple(sum(R[i][j][k]*c[k][a]for k in range(n))for a in (0,1))
def div(x,y):
 den=y[0]*y[0]-2*y[1]*y[1]
 return (Q(x[0]*y[0]-2*x[1]*y[1],den),Q(x[1]*y[0]-x[0]*y[1],den))
for c in chars:
 f=tuple(sum(mul(z,z)[a]for z in c)for a in (0,1))
 ev=(1+sum(c[i][0]for i in [3,4,5,6]),sum(c[i][1]for i in [3,4,5,6]))
 assert ev==div(f,(f[0],-f[1]))
for i in [3,4,5,6]:
 assert closure([i])==set(range(n))
 assert R[i][i][0]==1 and sum(R[i][i][j]for j in [1,2,7])==1
 assert [R[i][i][j]for j in [3,4,5,6]]==[2]*4 and R[i][i][8]==0
 v=[1]+[0]*8
 for _ in range(4):v=[sum(v[a]*R[a][i][b]for a in range(n))for b in range(n)]
 assert v[0]==18
 assert sum(R[i][i])==10
# All semidirect-algebra block counts consistent with dimension18 and square trace10.
traces=set();counts=[]
for ap in range(10):
 for am in range(10):
  for b in range(10):
   if ap+am+b!=9 or 2*(ap-am)!=10:continue
   counts.append((ap,am,b))
   for parts in itertools.product([(1,1),(1,-1),(-1,1),(-1,-1)],repeat=b):
    traces.add((sum(x for x,y in parts),sum(y for x,y in parts)))
assert counts==[(5,0,4),(6,1,2),(7,2,0)]
assert traces==set(itertools.product(range(-4,5,2),repeat=2))
print(json.dumps({'source_sha256':sha,'forced_Galois_unit_column':[1,0,0,1,1,1,1,0,0],'complete_character_count':len(chars),'character_field':'Q(sqrt2)','large_objects_generate_full':True,'fourth_vacuum_dimension':18,'square_rotation_trace':10,'quartic_trace_grid':sorted(traces),'status':'EXACT_PASS'},indent=2))
