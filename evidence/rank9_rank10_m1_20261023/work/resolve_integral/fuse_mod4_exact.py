"""Exact equivariantizations of Vec(F16_add) by tensor actions of D10.
No numerical or conjectural categorification input is used.
"""
from pathlib import Path
import itertools,json,hashlib
ROOT=Path(__file__).resolve().parents[2]
import sympy as s

def tensor_hash(R):
 return hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()

def fm(a,b):
 c=0
 while b:
  if b&1:c^=a
  a<<=1
  if a&16:a^=19
  b>>=1
 return c
def fp(a,k):
 c=1
 for _ in range(k):c=fm(c,a)
 return c
def tr(a):
 v=a^fp(a,2)^fp(a,4)^fp(a,8)
 assert v in [0,1]
 return v
H=list(itertools.product(range(5),range(2)));hi={x:i for i,x in enumerate(H)}
def hm(a,b):return((a[0]+(-1)**a[1]*b[0])%5,a[1]^b[1])
def inv(a):return next(b for b in H if hm(a,b)==(0,0))
a=fp(2,3)
def act(h,v):return fm(fp(a,h[0]),fp(v,4**h[1]))
K=s.QQ.algebraic_field(s.sqrt(5),s.sqrt(2),s.I);I=K.from_sympy(s.I);Z=K.from_sympy((1+s.I)/s.sqrt(2))
rr=[K(2),K.from_sympy((s.sqrt(5)-1)/2),K.from_sympy((-s.sqrt(5)-1)/2),K.from_sympy((-s.sqrt(5)-1)/2),K.from_sympy((s.sqrt(5)-1)/2)]

def fuse_action(J,qvals):
 def B(x,y):return J[x][y]
 def q(x):return qvals[x]
 objs=[]
 for sign in [1,-1]:objs.append({'rep':0,'support':{0},'label':'sign'+str(sign),'trace':{h:K(sign**h[1]) for h in H}})
 for k in[1,2]:objs.append({'rep':0,'support':{0},'label':'D10two'+str(k),'trace':{h:rr[k*h[0]%5] if h[1]==0 else K.zero for h in H}})
 seen={0}
 for u in range(1,16):
  if u in seen:continue
  orb={act(h,u) for h in H};seen|=orb
  for sign in [1,-1]:objs.append({'rep':u,'support':orb,'label':f'orbit{u}_sign{sign}','lambda':K(sign)*Z**q(u)})
 def trace(ob,x,h):
  if x not in ob['support'] or act(h,x)!=x:return K.zero
  if x==0:return ob['trace'][h]
  return ob['lambda']**h[1]
 R=[[[0]*len(objs) for _ in objs] for _ in objs]
 for k,ob in enumerate(objs):
  z=ob['rep'];stab=[h for h in H if act(h,z)==z]
  for i,j in itertools.product(range(len(objs)),repeat=2):
   val=K.zero
   for h in stab:
    chi=trace(ob,z,h)
    # Values are roots of unity or real D10 characters; inverse-element
    # projective conjugation is achieved by field embedding i -> -i.
    chistar=chi if z==0 or h[1]==0 else K.one/chi
    vv=sum((trace(objs[i],x,h)*trace(objs[j],x^z,h)*I**(-h[1]*B(x,x^z)) for x in objs[i]['support'] if x^z in objs[j]['support']),K.zero)
    val+=chistar*vv
   val/=K(len(stab));vv=val.to_list();assert len(vv)<=1 and (not vv or vv[0].denominator==1 and vv[0]>=0),(i,j,k,vv)
   R[i][j][k]=int(vv[0]) if vv else 0
 return R,[{'representative':ob['rep'],'support':sorted(ob['support']),'label':ob['label']} for ob in objs]
