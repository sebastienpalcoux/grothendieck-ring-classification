"""Independent exact source and formal-codegree audit for R12_1_332.

No previous rank-six exclusion implementation is used. The categorical
action and exhaustive equivariantization argument are in audit_R332.md.
"""
from pathlib import Path
import json,hashlib,itertools
import sympy as s
HERE=Path(__file__).resolve().parent
BASE=HERE.parents[1]/'prior_round'
FIRST=BASE/'prior_round/evidence/rank12-m1-offline-20261025'
def need(x,m):
    if not x:raise ValueError(m)
R=json.loads((FIRST/'tensors.json').read_text())['R12_1_332']
digest=hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()
row=next(r for r in json.loads((BASE/'ledger.json').read_text())['records'] if r['id']=='R12_1_332')
need(row['tensor_sha256']==digest,'source binding')
n=len(R);du=[next(j for j in range(n) if R[i][j][0]) for i in range(n)]
G=[i for i in range(n) if sum(R[i][du[i]])==1]
need(G==[0,3,4,5,6,7],'invertibles')
mul=lambda i,j:R[i][j].index(1)
a,b,rho=3,5,9
aa=mul(a,a);need(mul(a,aa)==0 and mul(b,b)==0 and mul(mul(b,a),b)==aa,'S3 generators')
J=[0,a,aa,rho,mul(a,rho),mul(aa,rho)]
need(len(set(J))==6 and all(du[j] in J for j in J),'neutral dual-closed basis')
need(all(not R[i][j][k] for i,j in itertools.product(J,repeat=2) for k in range(n) if k not in J),'neutral product closure')
need(R[rho][rho]==[int(k in [0]+J[3:]) for k in range(n)],'Haagerup rho square')
need(mul(rho,a)==mul(aa,rho) and mul(rho,aa)==mul(a,rho),'Haagerup crossed commutation')
action=[J.index(mul(mul(b,j),b)) for j in J]
need(action==[0,2,1,3,5,4],'actual Ad_b orbit pattern')
t=s.Symbol('t');p=s.Poly(t*t-3*t-1,t);lo,hi=p.intervals(eps=s.Rational(1,10**8))[-1][0]
need(lo>0 and p.is_irreducible,'strict positive irrational root')
ds=[s.Poly(1 if i in G else t,t) for i in range(n)]
need(all((ds[i]*ds[j]-sum((R[i][j][k]*ds[k] for k in range(n)),s.Poly(0,t))).rem(p).is_zero for i,j in itertools.product(range(n),repeat=2)),'exact two-value source FP character')
# This table is independently derived from the orbit pattern and the single
# rho_+^2 choice proved in the companion note, not copied from a rank-six file.
T=[[[0]*6 for _ in range(6)] for _ in range(6)]
def put(i,j,terms):
    for k,c in terms.items():T[i][j][k]=T[j][i][k]=c
for i in range(6):put(0,i,{i:1})
put(1,1,{0:1});put(1,2,{2:1});put(1,3,{4:1});put(1,4,{3:1});put(1,5,{5:1})
put(2,2,{0:1,1:1,2:1});put(2,3,{5:1});put(2,4,{5:1});put(2,5,{3:1,4:1,5:1})
put(3,3,{0:1,3:1,5:1});put(4,4,{0:1,3:1,5:1});put(3,4,{1:1,4:1,5:1})
put(3,5,{2:1,3:1,4:1,5:2});put(4,5,{2:1,3:1,4:1,5:2})
put(5,5,{0:1,1:1,2:1,3:2,4:2,5:4})
need(all(sum(T[i][j][m]*T[m][k][l] for m in range(6))==sum(T[j][k][m]*T[i][m][l] for m in range(6)) for i,j,k,l in itertools.product(range(6),repeat=4)),'derived equivariant table associative')
need(all(T[i][j][0]==int(i==j) for i,j in itertools.product(range(6),repeat=2)),'all equivariant simples selfdual')
forget=[[0]*6 for _ in range(6)]
for i,support in enumerate([[0],[0],[1,2],[3],[3],[4,5]]):
    for j in support:forget[i][j]=1
Q=[[[R[J[i]][J[j]][J[k]] for k in range(6)] for j in range(6)] for i in range(6)]
need(all(sum(T[i][j][k]*forget[k][z] for k in range(6))==sum(forget[i][x]*forget[j][y]*Q[x][y][z] for x,y in itertools.product(range(6),repeat=2)) for i,j,z in itertools.product(range(6),repeat=3)),'every forgetting coefficient')
q=s.Poly(t*t-t-1,t);chars=[s.Poly(x,t) for x in [1,-1,0,t,-t,0]]
need(all((chars[i]*chars[j]-sum((T[i][j][k]*chars[k] for k in range(6)),s.Poly(0,t))).rem(q).is_zero for i,j in itertools.product(range(6),repeat=2)),'two entire formal characters')
f=sum((v*v for v in chars),s.Poly(0,t)).rem(q)
need(f==s.Poly(4+2*t,t),'formal codegree 5 plus or minus sqrt5')
D=s.Poly(12+18*t,t).rem(p) # twice (3+3*d^2)
need(s.resultant(p.as_expr(),D.as_expr(),t)==468,'norm of total equivariant dimension')
need(s.resultant(q.as_expr(),f.as_expr(),t)==20,'norm of formal codegree')
norm=s.Rational(468**2,20**2);need(norm==s.Rational(13689,25) and norm.q>1,'nonintegral biquadratic norm')
report={'status':'PASS','id':'R12_1_332','source_tensor_sha256':digest,'neutral_basis':J,'alpha':a,'involution_b':b,'rho':rho,'Ad_b_permutation':action,'two_FP_values_minimal_polynomial':[1,-3,-1],'equivariant_basis':['1','g','U','rho_plus','rho_minus','V'],'equivariant_tensor':T,'dimension':'39+9*sqrt(13)','formal_codegrees':['5+sqrt(5)','5-sqrt(5)'],'norm_dimension':468,'norm_codegree':20,'biquadratic_norm_ratio':str(norm),'scope':'Arbitrary complex categorification via published two-value Galois-pseudounitarity; coherent action and exhaustive orbit reasoning in audit_R332.md.'}
(HERE/'audit_R332.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS R332: exact source/orbits, complete equivariant tensor, formal character, nonintegral norm',norm)
