"""Exact spin-current C2 action on SU(2)_6 and its equivariantizations.

Uses the real unitary quantum-Racah gauge. Every transformed F entry is compared
by its exact square and rigorously determined sign in Q(2cos(pi/8)).
"""
from standard import *
import sympy as sy
from fractions import Fraction
from functools import lru_cache
U=sy.Symbol('u');K=sy.QQ.alg_field_from_poly(sy.Poly(U**4-4*U**2+2,U),alias='u');u=K.unit
Q=[K.zero,K.one]
for i in range(2,9):Q.append(u*Q[-1]-Q[-2])
FAC=[K.one]
for i in range(1,9):FAC.append(FAC[-1]*Q[i])
R=su2(6);sigma=[0,5,2,3,4,1,6]

def frac(x):return Fraction(int(x.numerator),int(x.denominator))
def sign(x):
 if not x:return 0
 co=[frac(c)for c in x.to_list()]
 lo,hi=Fraction(1847759,1000000),Fraction(1847760,1000000)
 if not(lo**2>2 and lo**4-4*lo**2+2<0<hi**4-4*hi**2+2):raise ValueError('invalid real-root isolation')
 def mul(A,B):
  v=[a*b for a in A for b in B];return(min(v),max(v))
 for _ in range(200):
  out=(Fraction(0),Fraction(0))
  for c in co:
   out=mul(out,(lo,hi));out=(out[0]+c,out[1]+c)
  if out[0]>0:return 1
  if out[1]<0:return -1
  mid=(lo+hi)/2
  if mid**4-4*mid**2+2<0:lo=mid
  else:hi=mid
 raise ValueError('sign isolation')

@lru_cache(None)
def delta(a,b,c):
 if not R[a][b][c]:return K.zero
 p=(a+b+c)//2
 return FAC[p-a]*FAC[p-b]*FAC[p-c]/FAC[p+1]

@lru_cache(None)
def Fdata(a,b,c,d,e,f):
 ds=delta(a,b,e)*delta(e,c,d)*delta(b,c,f)*delta(a,f,d)
 if not ds:return K.zero,0
 aa=[(a+b+e)//2,(e+c+d)//2,(b+c+f)//2,(a+f+d)//2]
 bb=[(a+b+c+d)//2,(a+c+e+f)//2,(b+d+e+f)//2]
 s=K.zero
 for z in range(max(aa),min(bb)+1):
  if any(not 0<=j<=7 for j in [z-h for h in aa]+[h-z for h in bb]):raise ValueError('root-of-unity denominator')
  if z>=7:continue # [8]=0; admissibility keeps denominator factors below8.
  den=K.one
  for j in aa:den*=FAC[z-j]
  for j in bb:den*=FAC[j-z]
  s+=(-1)**z*FAC[z+1]/den
 return Q[e+1]*Q[f+1]*ds*s*s,(-1)**((a+b+c+d)//2)*sign(s)


def solve_action():
 triples=[(a,b,c)for a,b,c in itertools.product(range(7),repeat=3)if R[a][b][c]and a and b];ix={k:i for i,k in enumerate(triples)};basis={};eqs=[];n=0;zeros=0
 def add(keys,rhs):
  mask=0
  for k in keys:
   if k in ix:mask^=1<<ix[k]
  eqs.append((mask,rhs))
  while mask:
   p=mask.bit_length()-1
   if p in basis:mask^=basis[p][0];rhs^=basis[p][1]
   else:basis[p]=mask,rhs;return
  if rhs:raise ValueError('tensorator inconsistent')
 for a,b,c,d,e,f in itertools.product(range(7),repeat=6):
  if not(R[a][b][e]and R[e][c][d]and R[b][c][f]and R[a][f][d]):continue
  q,s=Fdata(a,b,c,d,e,f);qq,ss=Fdata(*(sigma[z]for z in(a,b,c,d,e,f)))
  if q!=qq:raise ValueError(('magnitude changed',(a,b,c,d,e,f)))
  if not q:zeros+=1;continue
  n+=1;add([(a,b,e),(e,c,d),(b,c,f),(a,f,d)],int(s!=ss))
 val=0
 for p,(mask,rhs)in sorted(basis.items()):
  if((mask&val).bit_count()%2)^rhs:val|=1<<p
 J={k:(val>>ix[k])&1 if k in ix else 0 for k in itertools.product(range(7),repeat=3)if R[k[0]][k[1]][k[2]]}
 if not all(((mask&val).bit_count()%2)==rhs for mask,rhs in eqs):raise ValueError('tensorator replay')
 # μ:F²=>Id is a monoidal natural isomorphism and obeys μ_F=F(μ).
 mus=[]
 for tail in itertools.product(range(4),repeat=6):
  mu=[0]+list(tail)
  if any(mu[sigma[a]]!=mu[a]for a in range(7)):continue
  if all((mu[a]+mu[b]-mu[c]-2*(J[a,b,c]+J[sigma[a],sigma[b],sigma[c]]))%4==0 for a,b,c in J):mus.append(mu)
 if not mus:raise ValueError('no coherent C2 action')
 return J,mus,{'nonzero_F_equations':n,'zero_F_entries':zeros,'tensorator_variables':len(triples),'linear_rank':len(basis),'coherent_mu_solutions':len(mus),'q_integer_polynomial':'u^4-4u^2+2','chosen_u_interval':['1847759/1000000','1847760/1000000']}


def equiv(J,mu):
 # Orbit objects; each fixed simple has two choices u=+/-sqrt(μ).
 labs=[];seen=set()
 for a in range(7):
  if a in seen:continue
  O=sorted({a,sigma[a]});seen.update(O)
  if len(O)==1:labs.extend([(O,0),(O,4)])
  else:labs.append((O,None))
 n=len(labs);T=[[[0]*n for _ in range(n)]for _ in range(n)]
 for i,(A,ea)in enumerate(labs):
  for j,(B,eb)in enumerate(labs):
   for k,(C,ec)in enumerate(labs):
    c=C[0];dim=sum(R[a][b][c]for a in A for b in B)
    if ec is None:T[i][j][k]=dim;continue
    trace=0
    if ea is not None and eb is not None and R[A[0]][B[0]][c]:
     a,b=A[0],B[0]
     phase=(4*J[a,b,c]+mu[a]+mu[b]-mu[c]+ea+eb-ec)%8
     if phase not in(0,4):raise ValueError(('non-real involution',a,b,c,phase))
     trace=1 if phase==0 else -1
    if(dim+trace)%2 or(dim+trace)<0:raise ValueError('bad multiplicity')
    T[i][j][k]=(dim+trace)//2
 return T,labs

def main():
 J,mus,stats=solve_action();print(stats,flush=True);data=targets();out=[];seen=set()
 for mu in mus:
  T,labs=equiv(J,mu);validate(T)
  hits=[]
  for rid,S in data.items():
   p=based_iso(S,T)
   if p is None:continue
   hits.append(rid)
   if rid in seen:continue
   seen.add(rid);out.append({'id':rid,'tensor_sha256':tensor_hash(S),'status':'unitarily_realized','models':[{'name':'SU(2)_6 equivariantized by spin-current C2 action','constructor':'su2_spin_equivariant','parameters':{'level':6,'permutation':sigma,'tensorator_exponents_mod2':[[*k,v]for k,v in J.items()],'coherence_exponents_mod4':mu,'labels':labs,'q6j_validation':stats},'reference':'Unitary SU(2)_6 quantum-Racah associator; exact monoidal action and coherence certified here; equivariantization theorem','model_tensor':T,'basis_map_source_to_model':p}]})
  print('mu',mu,'matches',hits,flush=True)
 (HERE/'su2_spin_models.json').write_text(json.dumps(out,indent=2)+'\n');(HERE/'su2_spin_verification.json').write_text(json.dumps(stats|{'status':'PASS','modeled_ids':sorted(seen)},indent=2)+'\n')
if __name__=='__main__':main()
