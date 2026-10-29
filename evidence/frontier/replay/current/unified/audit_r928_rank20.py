#!/usr/bin/env python3
"""Independent exact audit of the proposed rank20 modular datum.

Reads only its exported S,T and integer tensor, never its reconstruction code.
SymPy constructs the cyclotomic minimal polynomial; arithmetic is exact.
"""
from pathlib import Path
from fractions import Fraction as Q
from collections import defaultdict
from itertools import product
from functools import lru_cache
import hashlib,json,time
import sympy as sp

HERE=Path(__file__).resolve().parent
P=HERE.parent/'r928'
start=time.monotonic()
def need(ok,msg):
    if not ok:raise ValueError(msg)
record=json.loads((P/'rank20_modular_data.json').read_text())
tensor_record=json.loads((P/'rank20_fusion_tensor.json').read_text())
N=tensor_record['tensor'];n=20
x=sp.Symbol('x');phi=sp.Poly(sp.cyclotomic_poly(288,x),x)
need(phi.degree()==96,'field degree')
roots=[]
for k in range(288):
    rem=sp.rem(sp.Poly(x**k,x),phi)
    roots.append(tuple(sorted((i,int(c)) for (i,),c in rem.terms() if c)))
ZERO=();ONE=roots[0]
def add(*zs):
    out=defaultdict(Q)
    for z in zs:
        for k,c in z:out[k]+=c
    return tuple(sorted((k,c) for k,c in out.items() if c))
def scale(c,z):return tuple((k,c*a) for k,a in z if c*a)
@lru_cache(None)
def mul(a,b):
    return add(*(scale(c*d,roots[(i+j)%288]) for i,c in a for j,d in b))
def gal(a,z):return add(*(scale(c,roots[(a*k)%288]) for k,c in z))
S=[[tuple((int(k),Q(c)) for k,c in entry) for entry in row] for row in record['S']]
phase=record['twist_exponents_mod288']
need(len(S)==n and all(len(row)==n for row in S),'S size')
need(len(N)==n and all(len(m)==n and all(len(row)==n for row in m) for m in N),'tensor size')
need(all(type(c)==int and c>=0 for m in N for row in m for c in row),'nonnegative integral tensor')
need(all(S[i][j]==S[j][i] and gal(287,S[i][j])==S[i][j] for i,j in product(range(n),repeat=2)),
     'real symmetric S')
for i,j in product(range(n),repeat=2):
    products=[mul(S[i][k],S[k][j]) for k in range(n)]
    need(add(*products)==(ONE if i==j else ZERO),'S squared identity')
    lhs=add(*(mul(z,roots[phase[k]]) for k,z in enumerate(products)))
    rhs=mul(S[i][j],roots[(36-phase[i]-phase[j])%288])
    need(lhs==rhs,'STS with correct anomaly')
need(all(N[0][j][k]==int(j==k) and N[j][k][0]==int(j==k) for j,k in product(range(n),repeat=2)),
     'unit and selfdual basis')
need(all(N[i][j][k]==N[j][i][k]==N[i][k][j] for i,j,k in product(range(n),repeat=3)),
     'commutativity and Frobenius reciprocity')

# Denominator-free spectral identities certify every Verlinde coefficient.
for i,j,l in product(range(n),repeat=3):
    lhs=mul(S[0][l],add(*(scale(N[i][j][k],S[k][l]) for k in range(n))))
    need(lhs==mul(S[i][l],S[j][l]),'8000 exact Verlinde identities')

# An independent integer check, not an inference from simultaneous diagonalization.
for i,j,k,l in product(range(n),repeat=4):
    need(sum(N[i][j][a]*N[a][k][l] for a in range(n))==
         sum(N[j][k][a]*N[i][a][l] for a in range(n)),'all160000 associativity identities')

prior=json.loads((P/'prior/spectral_reduction.json').read_text())
pattern=next(a for a in prior['patterns'] if a['pattern']==186)
r2=add(roots[36],roots[252]);r3=add(roots[24],roots[264]);r6=mul(r2,r3)
basis=(ONE,r2,r3,r6)
D=add(*(scale(q,b) for q,b in zip((144,96,80,56),basis)))
L=scale(Q(1,2),mul(D,r2))
dimensions=[add(*(scale(Q(q),b) for q,b in zip(ds,basis))) for ds in pattern['dimensions']]
need(all(mul(S[0][i],L)==dimensions[i] for i in range(n)),'exact dimension row')
need(all((sum(sp.Rational(q)*b for q,b in zip(ds,(1,sp.sqrt(2),sp.sqrt(3),sp.sqrt(6))))).is_positive
         for ds in pattern['dimensions']),'positive dimensions')
need(N[4]==pattern['N_W'],'inherited W multiplication')
for i,j in product(range(n),repeat=2):
    lhs=mul(S[i][j],roots[(phase[i]+phase[j])%288])
    rhs=add(*(scale(N[i][j][k],mul(S[0][k],roots[phase[k]])) for k in range(n)))
    need(lhs==rhs,'all400 balancing equations')

closures=[]
for q in range(1,n):
    closure={0,q}
    while True:
        enlarged=closure|{k for i in closure for j in closure for k,c in enumerate(N[i][j]) if c}
        if enlarged==closure:break
        closure=enlarged
    closures.append(len(closure))
need(closures==[20]*19,'simple fusion ring')

# Indicator formula written using normalized unit entries: no global-dimension
# inversion or source quartic helper is needed.
indicator_results={}
for m in (2,3,4):
    values=[]
    for k in range(n):
        val=add(*(scale(N[k][i][j],mul(mul(S[0][i],S[0][j]),roots[(m*(phase[i]-phase[j]))%288]))
                  for i,j in product(range(n),repeat=2) if N[k][i][j]))
        if m in (2,3):
            expected=record['second_indicators' if m==2 else 'third_indicators'][k]
            need(val==scale(expected,ONE),'all-simple second/third indicators')
        if m==4:
            need(all(e in (0,72) and c.denominator==1 for e,c in val),'all-simple fourth indicators in Z[i]')
        values.append([[e,str(c)] for e,c in val])
    indicator_results[str(m)]=values
receipt={
    'status':'PASS',
    'scope':'Exact modular datum and simple based fusion ring only; no category, algebra, Morita equivalence, or uniqueness claim',
    'rank':20,'field':'Q(zeta288); minimal polynomial independently generated by SymPy',
    'checks':['real symmetric S','S squared identity','STS with anomaly zeta8',
              '8000 denominator-free Verlinde identities','160000 integer associativity identities',
              'positive dimension row','unit and duality','all400 balancing identities',
              'simple based ring','inherited W matrix','all-simple indicators2,3,4'],
    'indicators':indicator_results,
    'input_sha256':{name:hashlib.sha256((P/name).read_bytes()).hexdigest()
                    for name in ('rank20_modular_data.json','rank20_fusion_tensor.json','prior/spectral_reduction.json')},
    'seconds':time.monotonic()-start,
}
(HERE/'audit_r928_rank20.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({k:v for k,v in receipt.items() if k!='indicators'}))
