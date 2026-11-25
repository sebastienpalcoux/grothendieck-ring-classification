from math import isqrt
from fractions import Fraction as F

from half24 import DISCS
S=10**60
rad=[isqrt(d*S*S) for d in DISCS]
def emb24(t):
    out=[]
    for j,k in ((1,1),(1,-1),(-1,1),(-1,-1)):
        v=[t[1]*j,t[2]*k,t[3]*j*k];lo=t[0]*S+sum(a*(r+(a<0)) for a,r in zip(v,rad));out.append((lo,lo+sum(abs(a) for a in v)))
    return out



def emb16(t):
 a,b,c,d=t;rt=isqrt(2*S*S);y=isqrt((2*S+rt)*S);z=isqrt((2*S-rt-1)*S)
 zz=[(y,y+2),(z,z+2),(-y-2,-y),(-z-2,-z)];ans=[]
 for i in range(4):
  lo=a*S;hi=a*S
  for v,(l,h) in ((b*(-1)**i,(rt,rt+1)),(c,zz[i]),(d,zz[(i+1)%4])):
   lo+=min(v*l,v*h);hi+=max(v*l,v*h)
  ans.append((lo,hi))
 return ans

def moments16(x,z):
 from half16 import mul
 t=z[0];y=x
 for e in range(2,6):
  y=mul(x,y)
  if mul(y,z)[0]%(2*t)!=t:return False
 return True

def moments24(x,z):
 from half24 import DISCS,CROSS
 def times(u,v):
  a,*y=u;b,*w=v
  return tuple([a*b+sum(d*c*f for d,c,f in zip(DISCS,y,w))]+[a*w[i]+b*y[i]+CROSS[i]*(y[(i+1)%3]*w[(i+2)%3]+y[(i+2)%3]*w[(i+1)%3]) for i in range(3)])
 t=z[0];y=x
 for e in range(2,6):
  y=times(x,y);den=4**e*t
  if times(y,z)[0]%(2*den)!=den:return False
 return True

def process(data,c):
 tally=[0]*4;bad=[]
 for x,z in data:
  fun=emb24 if c==24 else emb16
  xx=fun(x);zz=fun(z);i=min(range(4),key=lambda j:xx[j][0]);assert all(xx[i][1]<xx[k][0] for k in range(4) if i!=k)
  if any(zz[k][1]<zz[i][0] or zz[k][1]*xx[k][1]<zz[i][0]*xx[i][0] for k in range(4)):continue
  tally[0]+=1
  if not (moments24 if c==24 else moments16)(x,z):continue
  tally[1]+=1
  if c==24 and 24**2*z[3]**2>16*z[0]**2:continue # Q24=z3 sqrt24/z0, bound Q24^2 <=16/24.
  if c==16:
   from half16 import mul
   w=mul(z,x)
   if 2*(w[2]**2+w[3]**2)>w[0]**2:continue
  tally[2]+=1;bad.append([x,z]);
 return tally,bad
