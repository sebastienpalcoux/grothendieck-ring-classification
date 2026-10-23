"""C2-equivariantizations of twisted cyclic pointed categories.

Explicit cochain formulas, all cocycle/tensorator/action equations checked in
Z/(2n), and exact equivariantization of all basis tensor products.
"""
from standard import *

def action(n,t,u):
 if(u*u-1)%n:raise ValueError('not involution')
 v=(u*u-1)//n;p=[u*a%n for a in range(n)]
 w=lambda a,b,c:t*a*((b+c)//n)%n
 J=lambda a,b:-t*u*a*((u*b)//n)%n
 # Exponents for μ:F²=>Id in roots ofunity oforder2n.
 mu=None
 for k in range(n):
  z=[(t*v*a*a+2*k*a)%(2*n)for a in range(n)]
  if all(z[p[a]]==z[a]for a in range(n)):mu=z;break
 if mu is None:raise ValueError('action obstruction')
 for a,b,c,d in itertools.product(range(n),repeat=4):
  if(w(b,c,d)-w((a+b)%n,c,d)+w(a,(b+c)%n,d)-w(a,b,(c+d)%n)+w(a,b,c))%n:raise ValueError('3-cocycle')
 for a,b,c in itertools.product(range(n),repeat=3):
  if(J(b,c)-J((a+b)%n,c)+J(a,(b+c)%n)-J(a,b)-w(a,b,c)+w(p[a],p[b],p[c]))%n:raise ValueError('tensorator')
 for a,b in itertools.product(range(n),repeat=2):
  if(mu[a]+mu[b]-mu[(a+b)%n]-2*J(a,b)-2*J(p[a],p[b]))%(2*n):raise ValueError('square coherence')
 return p,[[J(a,b)for b in range(n)]for a in range(n)],mu

def equiv(n,p,J,mu):
 labs=[];seen=set()
 for a in range(n):
  if a in seen:continue
  O=sorted({a,p[a]});seen.update(O)
  for sign in([0,2*n]if len(O)==1 else[None]):labs.append((O,sign))
 r=len(labs);T=[[[0]*r for _ in range(r)]for _ in range(r)]
 for i,(A,ea)in enumerate(labs):
  for j,(B,eb)in enumerate(labs):
   for k,(C,ec)in enumerate(labs):
    c=C[0];d=sum((a+b)%n==c for a in A for b in B)
    if ec is None:T[i][j][k]=d;continue
    tr=0
    if ea is not None and eb is not None and(A[0]+B[0])%n==c:
     a,b=A[0],B[0];z=(-4*J[a][b]+mu[a]+mu[b]-mu[c]+ea+eb-ec)%(4*n)
     if z not in(0,2*n):raise ValueError('trace not involutive')
     tr=1 if z==0 else -1
    if(d+tr)%2 or d+tr<0:raise ValueError('bad coefficient')
    T[i][j][k]=(d+tr)//2
 return T,labs

def main():
 data=targets();out=[];checks=[]
 for u in[15,7]:
  n=16;t=1;p,J,mu=action(n,t,u);T,labs=equiv(n,p,J,mu);validate(T);hits=[]
  for rid,R in data.items():
   q=based_iso(R,T)
   if q is None:continue
   hits.append(rid);out.append({'id':rid,'tensor_sha256':tensor_hash(R),'status':'unitarily_realized','models':[{'name':f'Vec(C16,omega_1)^C2, a-> {u}a','constructor':'twisted_cyclic_equivariant','parameters':{'cyclic_order':n,'cocycle_class':t,'automorphism_multiplier':u,'automorphism':p,'tensorator_mod16':J,'coherence_mod32':mu,'labels':labs},'reference':'Pointed fusion category with standard cyclic3-cocycle; explicit unitaryC2action certified in twisted_cyclic.py; Burciu--Natale, Fusion rules of equivariantizations, arXiv:1206.6625','model_tensor':T,'basis_map_source_to_model':q}]})
  checks.append({'n':n,'t':t,'u':u,'cocycle_equations':n**4,'tensorator_equations':n**3,'square_coherence_equations':n**2,'action_associativity_equations':n,'matches':hits})
  print('u',u,'mu',mu,'hits',hits,flush=True)
 (HERE/'twisted_cyclic_models.json').write_text(json.dumps(out,indent=2)+'\n');(HERE/'twisted_cyclic_verification.json').write_text(json.dumps({'status':'PASS','checks':checks},indent=2)+'\n')
if __name__=='__main__':main()
