from extra_models import *
from functools import lru_cache
import sympy as sy
E=48
X=sy.Symbol('x');K=sy.QQ.alg_field_from_poly(sy.Poly(sy.cyclotomic_poly(E,X),X),alias='zeta48');root=K.unit
RO=[root**i for i in range(E)]
def abelian(G,H):return all(G[a][b]==G[b][a]for a,b in itertools.product(H,repeat=2))
def linear_exponents(G,H):
 n=len(H);closure={0};gens=[]
 for a in H:
  if a in closure:continue
  gens.append(a)
  while True:
   new=closure|{G[x][g]for x in closure for g in gens}
   if new==closure:break
   closure=new
 for vals in itertools.product(*[range(0,E,E//element_order(G,g))for g in gens]):
  mp={0:0};queue=[0];good=True
  for x in queue:
   for a,b in zip(gens,vals):
    y,z=G[x][a],(mp[x]+b)%E
    if y in mp:
     if mp[y]!=z:good=False;break
    else:mp[y]=z;queue.append(y)
   if not good:break
  if good and len(mp)==n:yield mp

def chars(G,H):
 H=sorted(H);inv=[row.index(0)for row in G]
 if abelian(G,H):return[{a:RO[e]for a,e in c.items()}for c in linear_exponents(G,H)]
 # find abelian index2 subgroup
 B=None
 for chi in linear_exponents(G,H):
  if set(chi.values())=={0,E//2}:
   B=[a for a in H if chi[a]==0]
   if abelian(G,B):break
   B=None
 if B is None:
  if len(H)==12:
   # A4: three linears and standarddim3.
   L=[{a:RO[e]for a,e in c.items()}for c in linear_exponents(G,H)]
   if len(L)==3:
    L.append({a:K(3 if a==0 else -1 if element_order(G,a)==2 else 0)for a in H});return L
  raise ValueError('characters unsupported '+str(len(H)))
 t=next(a for a in H if a not in B);seen=set();out=[]
 for chi in linear_exponents(G,B):
  sig=tuple(chi[a]for a in B)
  if sig in seen:continue
  conj={a:chi[G[G[inv[t]][a]][t]]for a in B};sig2=tuple(conj[a]for a in B);seen|={sig,sig2}
  if sig!=sig2:out.append({a:RO[chi[a]]+RO[conj[a]]if a in B else K.zero for a in H})
  else:
   e=chi[G[t][t]];assert e%2==0
   for add in [0,E//2]:
    v={a:RO[chi[a]]if a in B else RO[(e//2+add+chi[G[inv[t]][a]])%E]for a in H};out.append(v)
 one=next(c for c in out if all(c[a]==K.one for a in H));out.remove(one);out.insert(0,one)
 assert sum(int(c[0].to_list()[0])**2 for c in out)==len(H)
 assert all(sum((a[x]*b[inv[x]]for x in H),K.zero)==K(len(H)*int(i==j))for i,a in enumerate(out)for j,b in enumerate(out))
 return out

def fusion(G,H):
 n=len(G);inv=[row.index(0)for row in G];H=sorted(H);hs=set(H);objects=[];seen=set()
 for z in range(n):
  if z in seen:continue
  orb={G[G[u][z]][inv[v]]:(u,v)for u in H for v in H};seen|=set(orb)
  stab=[a for a in H if G[G[inv[z]][a]][z]in hs]
  for chi in chars(G,stab):objects.append((z,stab,chi,orb))
 seen=set();cos=[]
 for x in range(n):
  if x not in seen:cos.append(x);seen|={G[x][h]for h in H}
 @lru_cache(None)
 def val(i,x,a,b):
  z,stab,chi,orb=objects[i]
  if x not in orb or G[a][x]!=G[x][b]:return K.zero
  u,v=orb[x];return chi[G[G[inv[u]][a]][u]]
 r=len(objects);R=[[[0]*r for _ in range(r)]for _ in range(r)]
 for k,(z,stab,chi,orb)in enumerate(objects):
  for i,j in itertools.product(range(r),repeat=2):
   result=K.zero
   for a in stab:
    b=G[G[inv[z]][a]][z];tr=K.zero
    for x in cos:
     h=G[G[inv[x]][a]][x]
     if h in hs:tr+=val(i,x,a,h)*val(j,G[inv[x]][z],h,b)
    result+=chi[inv[a]]*tr
   result/=K(len(stab));co=result.to_list()
   assert len(co)<=1 and(not co or co[0].denominator==1 and co[0]>=0)
   R[i][j][k]=int(co[0])if co else 0
 return R

def gl2f3():
 els=[(1,0,0,1)]+[a for a in itertools.product(range(3),repeat=4)if a!=(1,0,0,1)and(a[0]*a[3]-a[1]*a[2])%3]
 ix={a:i for i,a in enumerate(els)}
 return[[ix[tuple(sum(a[2*i+k]*b[2*k+j]for k in range(2))%3 for i in range(2)for j in range(2))]for b in els]for a in els]
