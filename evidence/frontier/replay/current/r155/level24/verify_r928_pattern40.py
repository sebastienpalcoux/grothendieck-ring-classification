#!/usr/bin/env python3
"""Exact branch-obstruction certificate; categorical input is stated in the note."""
from pathlib import Path
import json,itertools,runpy,hashlib
import sympy as s
HERE=Path(__file__).resolve().parent
def need(ok,msg):
 if not ok:raise ValueError(msg)
# Recompute all spectrum decompositions from the frozen complete character tables.
ns=runpy.run_path(str(HERE/'r928_spectrum.py'))
result=next(x for x in ns['results'] if x['pattern']==40)
need(len(result['solutions'])==4,'complete spectral decomposition count')
target=[result['target'].get(i,0) for i in range(24)]
eligible=[r for r in ns['allreps'] if all(a<=b for a,b in zip(r['T'],target))]
need(len(eligible)==12,'all eligible irreducibles')
def linear1(T):return 2*T[20]-T[23]-T[11]+T[17]
def linear2(T):return 2*T[12]-T[3]-T[15]+T[9]
for r in eligible:
 need(linear1(r['T'])==2*int(r['indices'] in [[1,1],[1,5]]),'first exact spectral functional')
 need(linear2(r['T'])==2*int(r['indices'] in [[1,2],[1,5]]),'second exact spectral functional')
need(linear1(target)==0 and linear2(target)==6,'target spectral functionals force sign multiplicity three')
for decomp in result['solutions']:
 sign=[x for x in decomp if x['indices']==[1,2]]
 need(len(sign)==1 and sign[0]['multiplicity']==3,'three sign copies in every decomposition')
 need(sign[0]['degree']==1 and sign[0]['T']==[int(i==12) for i in range(24)],'sign spectrum')

# The tiny conductor-reduction kernel is linear, not a new large group search.
def mul(g,h,n):
 a,b,c,d=g;e,f,u,v=h
 return ((a*e+b*u)%n,(a*f+b*v)%n,(c*e+d*u)%n,(c*f+d*v)%n)
def inv(g,n):a,b,c,d=g;return(d,-b%n,-c%n,a)
def mpow(x,k,n):
 out=(1,0,0,1)
 for _ in range(k):out=mul(out,x,n)
 return out
T24=(1,24,0,1);U8=mpow(T24,3,32)
need(U8==(1,8,0,1),'T24 cubed gives U8')
S=(0,31,1,0);L=(1,0,1,1)
gens=[U8,mul(mul(S,U8,32),inv(S,32),32),mul(mul(L,U8,32),inv(L,32),32)]
coords=[]
for a,b,c,d in gens:
 need((a-1)%8==b%8==c%8==(d-1)%8==0,'kernel matrix shape')
 coords.append(((a-1)//8%4,b//8%4,c//8%4))
span={tuple(sum(k*g[i] for k,g in zip(coeff,coords))%4 for i in range(3)) for coeff in itertools.product(range(4),repeat=3)}
need(len(span)==64,'normal conjugates span entire reduction kernel')

# G_5 on the sign representation, from DLN Theorem II(iv), b=77 mod96.
need(5*77%96==1,'inverse mod96')
sign_G5=(-1)**5*(-1)*(-1)**77*(-1)*(-1)**5*(-1)
need(sign_G5==1,'sign character fixed by G5')

# Sigma5 reverses sqrt(3): sqrt(3)=zeta12+zeta12^-1.
x=s.Symbol('x');phi=s.Poly(s.cyclotomic_poly(12,x),x)
need(s.rem(s.Poly(x**5+x**7+x+x**11,x),phi).is_zero,'Galois sqrt3 sign')
maxfixed=0
for p in itertools.permutations(range(4)):
 P=s.Matrix(4,4,lambda i,j:int(i==p[j]))
 fixed=4-(P+s.eye(4)).rank()
 maxfixed=max(maxfixed,fixed)
need(maxfixed==2,'negative permutation fixed-space bound')
need(3>maxfixed,'dimension contradiction')

payload=dict(status='PASS',conclusion='R928 pattern40 is impossible under the independently derived phase/block hypotheses.',
 scope='Branch exclusion only; pattern186 and R8_3_928 remain unresolved.',
 spectral_decompositions=4,forced_sign_copies=3,t_minus_one_fiber=4,
 spectral_functional_values=[0,6],eligible_irreducibles=12,
 G5_fixed_vectors_at_least=3,negative_permutation_fixed_vectors_at_most=2,
 conductor_kernel_order=64,normal_conjugate_span=64,
 hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [HERE/'sl2_8.json',HERE/'sl2_3.json',HERE/'r928_spectrum.py']})
(HERE/'pattern40_obstruction_receipt.json').write_text(json.dumps(payload,indent=2)+'\n')
print(json.dumps(payload))
