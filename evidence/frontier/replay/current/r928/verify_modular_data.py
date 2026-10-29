#!/usr/bin/env python3
"""Exact rank20 S,T and fusion tensor. This does not construct a category."""
from pathlib import Path
from fractions import Fraction as Q
import sys,json,hashlib,time
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE));from cyclotomic288 import root,RT,ONE,add,scale,mul,sqrt2,sqrt3,sqrt6,need
sys.path.insert(0,str(HERE/'prior'));import quartic as quart
start=time.monotonic();n=20;Z=();r2=scale(Q(1,2),sqrt2);u=scale(Q(1,6),sqrt6);v=scale(Q(1,3),sqrt3);a=scale(Q(1,6),sqrt3)
neg=lambda x:scale(-1,x)
S4=[[neg(u),v,v,u],[v,u,u,neg(v)],[v,u,neg(u),v],[u,neg(v),v,u]]
S6=[[neg(a),u,u,a,u,v],[u,a,a,neg(u),neg(v),u],[u,a,a,neg(u),v,neg(u)],
    [a,neg(u),neg(u),neg(a),u,v],[u,neg(v),v,u,Z,Z],[v,u,neg(u),v,Z,Z]]
S2=[[neg(r2),r2],[r2,r2]];SS=[[r2,r2],[r2,neg(r2)]]
def vec(d):return {i:scale(c,ONE) for i,c in d.items() if c}
def pair(i,j,s=1):return {i:r2,j:scale(s,r2)}
e=vec({0:Q(1,2),1:Q(1,2),2:Q(1,2),3:Q(1,2)})
f=vec({0:Q(1,2),1:Q(-1,2),2:Q(-1,2),3:Q(1,2)})
aa=vec({0:Q(1,2),1:Q(1,2),2:Q(-1,2),3:Q(-1,2)})
bb=vec({0:Q(1,2),1:Q(-1,2),2:Q(1,2),3:Q(-1,2)})
E4=[aa,pair(5,19),pair(11,12),vec({13:1})]
E6=[bb,{5:neg(r2),19:r2},pair(6,7),vec({8:1}),pair(9,10),vec({18:1})]
E2=[pair(6,7,-1),pair(11,12,-1)];Es=[e,vec({4:1})]
S=[[Z for j in range(n)] for i in range(n)]
def outer(x,y,c=ONE):
 for i,a in x.items():
  for j,b in y.items():S[i][j]=add(S[i][j],mul(c,mul(a,b)))
def block(B,M):
 for i,row in enumerate(M):
  for j,c in enumerate(row):
   if c:outer(B[i],B[j],c)
for B,M in [(E4,S4),(E6,S6),(E2,S2),(Es,SS)]:block(B,M)
k=vec({i:Q(1,2) for i in range(14,18)});l=vec({14:Q(1,2),15:Q(-1,2),16:Q(1,2),17:Q(-1,2)});g=pair(9,10,-1)
outer(f,k);outer(k,f);outer(g,l);outer(l,g)
c=scale(Q(1,2),add(RT[18],RT[-18]));sine=scale(Q(1,2),mul(RT[-72],add(RT[18],neg(RT[-18]))))
block([pair(14,16,-1),pair(15,17,-1)],[[c,neg(sine)],[neg(sine),neg(c)]])
need(all(S[i][j]==S[j][i] for i in range(n) for j in range(n)),'S symmetry')
phase=[0,0,0,0,72,192,48,48,144,252,252,120,120,216,27,99,171,243,156,192]
xi=RT[36]
for i in range(n):
 for j in range(n):
  need(add(*(mul(S[i][k],S[k][j]) for k in range(n)))==(ONE if i==j else Z),'S squared')
  lhs=add(*(mul(mul(S[i][k],S[k][j]),RT[phase[k]]) for k in range(n)))
  rhs=mul(mul(xi,S[i][j]),RT[(-phase[i]-phase[j])%288])
  need(lhs==rhs,'STS')
source=HERE/'prior/spectral_reduction.json';p=next(p for p in json.load(open(source))['patterns'] if p['pattern']==186)
ds=[tuple(map(Q,d)) for d in p['dimensions']];L=quart.mul(quart.D,quart.inv((Q(0),Q(1),Q(0),Q(0))))
def encq(d):return add(*(scale(a,b) for a,b in zip(d,(ONE,sqrt2,sqrt3,sqrt6))))
inv0=[encq(quart.mul(L,quart.inv(d))) for d in ds]
for i in range(n):need(mul(S[0][i],inv0[i])==ONE,'exact positive dimension row')
# The integer tensor proposed by the numerical guide is accepted only after
# every entry of every diagonalization identity has been proved exactly.
tensor_path=HERE/'rank20_fusion_tensor.json';N=json.load(open(tensor_path))['tensor']
need(len(N)==n and all(len(M)==n and all(len(r)==n for r in M) for M in N),'tensor shape')
need(all(type(z) is int and z>=0 for M in N for row in M for z in row),'nonnegative integral tensor')
need(all(N[0][j][k]==int(j==k) for j in range(n) for k in range(n)),'tensor unit')
need(all(N[i][j][0]==int(i==j) for i in range(n) for j in range(n)),'self duality')
lams=[[mul(S[i][l],inv0[l]) for l in range(n)] for i in range(n)]
for i in range(n):
 for j in range(n):
  for l in range(n):
   need(add(*(scale(N[i][j][k],S[k][l]) for k in range(n)))==mul(S[j][l],lams[i][l]),'complete Verlinde diagonalization')
need(N[4]==p['N_W'],'inherited W matrix')
# Every Anderson--Moore--Vafa determinant identity, using symmetry of
# the self-dual fusion tensor. The pair tables avoid repeated arithmetic.
need(all(N[i][j][k]==N[j][k][i] for i in range(n) for j in range(n) for k in range(n)), 'Frobenius symmetry')
pairs=[(i,j) for i in range(n) for j in range(i,n)]
pidx={pair:k for k,pair in enumerate(pairs)}
ix=lambda i,j:pidx[(min(i,j),max(i,j))]
rows=[N[i][j] for i,j in pairs]
counts=[[sum(x*y for x,y in zip(u,vv)) for vv in rows] for u in rows]
weighted=[[sum(phase[r]*u[r]*vv[r] for r in range(n)) for vv in rows] for u in rows]
for i in range(n):
 for j in range(n):
  for k in range(n):
   for l in range(n):
    mass=counts[ix(i,j)][ix(k,l)]
    rhs=weighted[ix(i,j)][ix(k,l)]+weighted[ix(i,k)][ix(j,l)]+weighted[ix(i,l)][ix(j,k)]
    need(((phase[i]+phase[j]+phase[k]+phase[l])*mass-rhs)%288==0, 'all 160000 Vafa equations')
# Connected generated fusion subrings: each nonunit simple generates everything.
closures=[]
for x in range(1,n):
 found={0,x}
 while True:
  nxt=found|{k for i in found for j in found for k,z in enumerate(N[i][j]) if z}
  if nxt==found:break
  found=nxt
 closures.append(len(found))
need(closures==[n]*(n-1),'simple based ring')
# All-simple second and third indicators, exact in Q(zeta288).
dims=[encq(d) for d in ds];D2=encq(quart.mul(quart.D,quart.D));DD=[[mul(x,y) for y in dims] for x in dims]
expected={2:[1]*20,3:[1,2,3,5,5,1,2,2,2,2,2,3,3,3,3,3,3,3,4,4]}
for m,values in expected.items():
 for k in range(n):
  z=add(*(scale(2*N[k][i][j],mul(DD[i][j],RT[(m*(phase[i]-phase[j]))%288])) for i in range(n) for j in range(n) if N[k][i][j]))
  need(z==scale(values[k],D2),'all simple higher indicators')
  if m==3:
   cube=N[k][k][k];q,r=divmod(cube-values[k],3)
   need(r==0 and q>=0 and q+values[k]>=0,'third rotation eigenspace multiplicities')
# Store exact S entries as sparse rational coordinates in the certified
# cyclotomic basis; no floating-point number enters this artifact.
enc=lambda z:[[i,str(q)] for i,q in z]
result={'status':'PASS','scope':'Complete rank20 modular datum and simple fusion ring; not a categorical construction',
 'field':'Q(zeta288), Phi=x^96-x^48+1','S':[[enc(z) for z in row] for row in S],
 'twist_exponents_mod288':phase,'linear_normalization_gamma_exponent_mod288':12,
 'fusion_tensor_sha256':hashlib.sha256(tensor_path.read_bytes()).hexdigest(),
 'prior_spectral_data_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
 'second_indicators':expected[2],'third_indicators':expected[3],
 'checks':['symmetric S','S squared identity','STS relation','exact positive dimension row',
 'all 8000 Verlinde diagonalization identities','all 160000 Anderson-Moore-Vafa identities','nonnegative integral tensor','unit and self-dual basis',
 'simple based ring','all-simple second and third indicators'], 'seconds':time.monotonic()-start}
(HERE/'rank20_modular_data.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS: exact rank20 modular datum; all 8000 tensor entries verified; no category claimed.',time.monotonic()-start)
