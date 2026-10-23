from itertools import product
import numpy as np,json
from scipy.optimize import milp,Bounds,LinearConstraint
from pathlib import Path
T=np.array(json.loads(Path(__file__).with_name('structure_receipt.json').read_text())['galois_transform'],dtype=int)
ix=[(i,j) for i in range(5) for j in range(i,5)]
def flatten(x):return [x[i,j] for i,j in ix]
def orbit(v,pure=False):
 out=[];u=np.array(v)
 while tuple(u) not in [tuple(w) for w in out]:
  out.append(u.copy());u=T@u
  if pure:u=-u
 return out
base=[]
for bits in product(range(2),repeat=4):
 v=np.zeros(10,dtype=int);v[1]=1
 for i,b in zip([0,2,3,4],bits):v[5+i]=b
 base.append((list(v),orbit(v)))
pures=[];seen=set()
for b in [1,2,5,10]:
 for v in product(range(4),repeat=5):
  if sum(v)!=b:continue
  o=orbit([0]*5+list(v),True);key=min(tuple(w) for w in o)
  if key in seen:continue
  seen.add(key)
  if any(sum(int(w[5+i])**2 for w in o)>10 for i in range(5)):continue
  pures.append((list(v),o))
cols=[]
for v,o in base+pures:
 G=sum((np.outer(w[5:],w[5:]) for w in o),start=np.zeros((5,5),dtype=int))
 cols.append(flatten(G))
A=np.array(cols,dtype=float).T
G0=np.zeros((5,5),dtype=int)
for bits in product(range(2),repeat=4):
 if sum(bits) in [0,1,3,4]:
  v=np.array([0]+list(bits));G0+=np.outer(v,v)
y=flatten(15*np.eye(5,dtype=int)+15*np.ones((5,5),dtype=int)-G0)
# base column count10, each allowed coordinate appears5; number0=number4 andnumber1=number3.
extra=[];rhs=[]
for row,rr in [(lambda v:1,10)]+[(lambda v,i=i:v[5+i],5) for i in [0,2,3,4]]+[(lambda v: int(sum(v[5:])==0)-int(sum(v[5:])==4),0),(lambda v: int(sum(v[5:])==1)-int(sum(v[5:])==3),0)]:
 extra.append([row(v) for v,o in base]+[0]*len(pures));rhs.append(rr)
extra.append([int(sum(v[5:])==0) for v,o in base]+[0]*len(pures));rhs.append(0)
A=np.vstack([A,extra]);y=np.array(y+rhs)
r=milp(np.zeros(A.shape[1]),integrality=np.ones(A.shape[1]),bounds=Bounds(0,np.inf),constraints=LinearConstraint(A,y,y),options={'time_limit':60})
print('status',r.message,'variables',A.shape[1])
if r.x is not None:
 x=np.rint(r.x).astype(int);assert np.array_equal(A@x,y)
 print('base',[(v,n) for (v,o),n in zip(base,x[:len(base)]) if n]);print('pure',[(v,n,len(o)) for (v,o),n in zip(pures,x[len(base):]) if n])
 Path(__file__).with_name('gram_probe_witness.json').write_text(json.dumps({'base':[(list(map(int,v)),int(n)) for (v,o),n in zip(base,x[:len(base)]) if n],'pure':[(v,int(n),len(o)) for (v,o),n in zip(pures,x[len(base):]) if n],'warning':'Necessary-condition witness only. Not a modular datum or categorification.'},indent=2))
