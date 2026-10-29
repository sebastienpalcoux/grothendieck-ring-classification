from itertools import product
import numpy as np
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent

def power(t):
 t%=40; sign=1
 if t>=20:t-=20;sign=-1
 v=np.zeros(16,dtype=np.int64)
 if t<16:v[t]=sign
 else:
  for s,c in [(4,1),(8,-1),(12,1),(16,-1)]:v[t-s]=sign*c
 return v

def dimtw(a,b,t):return (a+3*b)*power(t)+2*b*power(t+8)+2*b*power(t+32)
D=dimtw(10,20,0)

def indicators(states):
 out=np.zeros((3,5,16),dtype=np.int64)
 for a,v,t in states:
  for n in range(1,4):
   dt=dimtw(a,sum(v),n*t)
   for i,m in enumerate(v):out[n-1,i]+=m*dt
 return out

def shifted(v,j):return tuple(v[(i-j)%5] for i in range(5))

def mixed(q,c):
 out=[]
 base=[([0]*5,0),([0,1,1,1,1],0)]
 for l in range(1,5):
  i=l*c%5
  base += [(tuple(int(k==i) for k in range(5)),l),(tuple(int(k not in [0,i]) for k in range(5)),l)]
 for v,l in base:
  for j in range(5):out.append((1,shifted(v,j),8*((q*j*j+l*j)%5)))
 return out

def gorbit(v,t,q):return [(0,shifted(v,j),(t+8*q*j*j)%40) for j in range(5)]

target=np.zeros((3,5,16),dtype=np.int64)
for i in range(1,5):target[2,i]=D
sol=[];first=0
for q,c in product(range(1,5),repeat=2):
 M=indicators(mixed(q,c))
 P1=[indicators(gorbit([1,0,0,0,0],5*a,q)) for a in range(8)]
 P5=[indicators(gorbit([1,1,1,1,1],5*b,q)) for b in range(8)]
 P2={(h,r):indicators(gorbit([0,1,0,0,1],5*h+8*r,q)+gorbit([0,0,1,1,0],5*h-8*r,q)) for h,r in product(range(8),range(5))}
 for a,b,h,r in product(range(8),range(8),range(8),range(5)):
  V=M+P1[a]+P5[b]+P2[h,r]
  if np.any(V[0]):continue
  first+=1
  if np.any(V[2]!=target[2]) or np.any(V[1,1:]):continue
  eps=next((e for e in [-1,1] if np.array_equal(V[1,0],e*D)),None)
  if eps is None:continue
  sol.append(dict(q=q,c=c,epsilon1=a,epsilon5=b,epsilon2=h,r=r,nu2_x=eps))
print('nu1 passes',first,'solutions',len(sol));print(sol)
(HERE/'central_metric_probe_results.json').write_text(json.dumps({'warning':'Necessary data, not categorical models.','nu1_passes':first,'solutions':sol},indent=2)+'\n')
