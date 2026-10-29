#!/usr/bin/env python3
"""Finite exact checks for the conditional R1154 algebra route; no category constructed."""
import hashlib, itertools, json, sys
from pathlib import Path
import sympy as s

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent))
from current_remaining_cases import R8_3_1154 as T, DUALS

def need(ok,message):
    if not ok: raise ValueError(message)

def coeff(x):
    return s.simplify(x)

need(hashlib.sha256(json.dumps(T,separators=(',',':')).encode()).hexdigest()==
     'c399505be76a64c8aba65feaf2cd55125dc7132f5894b74e58b64473d1387e25','source tensor')
L=[s.Matrix(x).T for x in T]
du=DUALS['R8_3_1154']
B=s.Matrix([[1,0,0,0,1,0,0,0],[0,0,0,1,0,1,0,0],
 [0,1,1,0,1,1,1,1],[0,1,1,0,1,1,1,1],
 [0,1,0,0,0,0,1,0],[0,0,1,0,0,0,0,1]])
need(B.T*B==s.Matrix(8,8,lambda i,j:int(i==j)+T[i][4][j]),'induction Gram')
need(B.rank()==5,'induction rank')
z=s.Matrix([0,0,1,-1,0,0]);P=z*z.T/2
chi4=[1,0,0,-1,1,-1,0,0];chi20=[1,-2,-2,-1,-1,1,2,2]
r5=s.sqrt(5);a=6+3*r5;delta=(a-1)/2;D=540+240*r5;Dp=540-240*r5
d=[1,a+1,a+1,1,a,a,a+1,a+1];dc=[s.sympify(x).subs(r5,-r5) for x in d]
dimsM=s.Matrix([1,1,delta,delta,2,2]);branches=[]
for chi in [chi4,chi20]:
    M=[B*Li*B.pinv()+v*P for Li,v in zip(L,chi)]
    need(all(x.is_Integer and x>=0 for X in M for x in X),'integral nonnegative module')
    for i,j in itertools.product(range(8),repeat=2):
        need(M[i]*M[j]==sum((T[i][j][k]*M[k] for k in range(8)),s.zeros(6)), 'all module products')
    for i in range(8):
        need(M[i].T==M[du[i]],'module dual transpose')
        need(s.simplify(M[i]*dimsM-d[i]*dimsM)==s.zeros(6,1),'module dimensions')
    need(M[3]==s.Matrix(6,6,lambda i,j:int(i==(j^1))),'free g action')
    multiplicities=[len(s.Matrix.vstack(*[X-v*s.eye(6) for X,v in zip(M,c)]).nullspace()) for c in [d,dc,chi4,chi20]]
    branches.append((M,multiplicities))
need(branches[0][1]==[1,1,2,0] and branches[1][1]==[1,1,1,1],'source character multiplicities')
M=branches[0][0]

# Exact commutant and canonical trace under the stated full-center premise.
t,u,b,c,h,q,r=s.symbols('t u b c h q r')
K=s.Matrix([[t,r-t,b,h-b,q,q],[r-t,t,h-b,b,q,q],
 [c,h-c,u,5*h+4*q+r-u,h,h],[h-c,c,5*h+4*q+r-u,u,h,h],
 [q,q,h,h,q+r,2*q],[q,q,h,h,2*q,q+r]])
need(all(X*K==K*X for X in M),'symbolic commutation')
xx=s.symbols('z:36');Z=s.Matrix(6,6,xx)
equations=s.Matrix.vstack(*[s.Matrix(list(X*Z-Z*X)) for X in M])
need(equations.jacobian(xx).rank()==29,'complete seven-dimensional commutant')
Ps=[]
for ch in [d,dc,chi4]:
    f=sum(x*x for x in ch)
    Ps.append(s.simplify(sum((v*X for v,X in zip(ch,M)),s.zeros(6))/f))
Pr=s.eye(6)-sum(Ps,s.zeros(6))
def tau(X):
    return s.simplify(s.trace(Ps[0]*X)/D+s.trace(Ps[1]*X)/Dp+s.trace(Ps[2]*X)/4+s.trace(Pr*X)/10)
need(tau(K)==(t+u-3*h)/2,'canonical trace')
def norm(v):
    hh,bb,cc,qq,rr,tt=v
    return bb*bb-bb*hh+cc*cc-cc*hh+hh*hh-4*hh*qq-hh*rr-hh*tt+9*qq*qq+4*qq*rr+4*qq*tt+rr*rr+2*tt*tt
need(s.simplify(tau(K*K.T).subs(u,3*h-t)-norm((h,b,c,q,r,t)))==0,'norm polynomial')
need(33**2>1077 and s.simplify(1077-D)>0 and s.simplify(delta-s.Rational(29,5))>0,'complete coefficient bounds')
ans=[]
for hh,qq,rr in itertools.product(range(6),range(9),range(33)):
    if hh==qq==rr==0:continue
    for tt in range(rr+1):
        if not 0<=3*hh-tt<=5*hh+4*qq+rr:continue
        for bb,cc in itertools.product(range(hh+1),repeat=2):
            v=(hh,bb,cc,qq,rr,tt)
            if norm(v)==1:ans.append(v)
need(len(ans)==12,'all norm-one candidates')
def inner(v,w):return s.Rational(norm(tuple(x+y for x,y in zip(v,w)))-norm(v)-norm(w),2)
bases=[ids for ids in itertools.combinations(range(12),6) if all(inner(ans[i],ans[j])==0 for i,j in itertools.combinations(ids,2))]
need(bases==[(1,4,6,7,10,11),(2,3,5,8,10,11)],'all orthonormal bases')
def matrix(v):
    hh,bb,cc,qq,rr,tt=v
    return K.subs({h:hh,b:bb,c:cc,q:qq,r:rr,t:tt,u:3*hh-tt})
out=[]
for ids in bases:
    matrices=[s.eye(6)]+[matrix(ans[i]) for i in ids]
    V=s.Matrix.hstack(*[s.Matrix(list(X)) for X in matrices]);inverse=(V.T*V).inv()*V.T
    N=[[list(inverse*s.Matrix(list(X*Y))) for Y in matrices] for X in matrices]
    good=all(x.is_Integer and x>=0 for row in N for col in row for x in col)
    out.append(good)
    if good:
        tensor=[[[int(x) for x in col] for col in row] for row in N]
        need(tensor==json.loads((HERE/'rank7_dual_1.json').read_text()),'saved rank-seven tensor')
        dimensions=[1,delta,delta,delta+1,delta+1,2*delta+1,4*delta+4]
        need(s.simplify(sum(x*x for x in dimensions)-D)==0,'dual global dimension')
        dual=[next(j for j in range(7) if tensor[i][j][0]) for i in range(7)]
        need(dual==[0,1,2,4,3,5,6],'rank-seven duality')
        for i,j,k,l in itertools.product(range(7),repeat=4):
            need(sum(tensor[i][j][z]*tensor[z][k][l] for z in range(7))==sum(tensor[j][k][z]*tensor[i][z][l] for z in range(7)),'associativity')
        for x in range(1,7):
            cl={0,x,dual[x]}
            while True:
                new=cl|{k for i in cl for j in cl for k,v in enumerate(tensor[i][j]) if v}
                if new==cl:break
                cl=new
            need(len(cl)==7,'simple based ring')
        need(any(tensor[i][j]!=tensor[j][i] for i,j in itertools.product(range(7),repeat=2)),'noncommutativity')
        need([tensor[i][i][dual[i]] for i in range(7)]==[1,1,1,1,1,2,19],'cubic vacuum dimensions')
need(out==[True,False],'exactly one integral fusion basis')
need(s.simplify((1/D+1/Dp)**2)==s.Rational(9,100),'dimension-block trivial character')
need(s.simplify((1/D-1/Dp)**2)==s.Rational(4,45),'dimension-block nontrivial character')
payload={'status':'PASS','scope':'Conditional algebra/module route only. No algebra or categorification constructed. Full-center/module-character premise separately reviewed.',
 'module_branch_scalar_multiplicities':[x[1] for x in branches], 'norm_one_candidates':len(ans), 'orthonormal_bases':len(bases),
 'integral_based_rings':1,'conditional_dual_rank':7,'conditional_dual_multiplicity':19,'R8_3_1154_status':'unresolved'}
(HERE/'conditional_rank7_receipt.json').write_text(json.dumps(payload,indent=2)+'\n')
print(json.dumps(payload))
