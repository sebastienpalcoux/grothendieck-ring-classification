#!/usr/bin/env python3
"""Independent, optimizer-free R350 audit; does not modify the C6 package."""
import hashlib,itertools,json,math
from fractions import Fraction as F
from pathlib import Path
import sympy as S

HERE=Path(__file__).resolve().parent
def need(p,m):
    if not p: raise ValueError(m)
FROZEN=json.loads((HERE/'frozen_R350.json').read_text())
need(FROZEN['ring']=='R12_1_350','wrong input ring')
R=FROZEN['tensor']
need(hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()=='c1fcaa5a2e3a0867276c5062959782de37347956ecfc1b3b9cf3f8315f5a3caf','original tensor digest')
du=[next(j for j in range(12) if R[i][j][0]) for i in range(12)]
G=[i for i in range(12) if sum(R[i][du[i]])==1]
O=[i for i in range(12) if i not in G]
def prod(a,b):
    need(sum(R[a][b])==1,'not a simple product')
    return R[a][b].index(1)
rho=next(x for x in O if all(R[x][g]==R[g][x] for g in G))
need(rho==11 and R[rho][rho]==[int(i==0 or i in O) for i in range(12)],'quadratic presentation')
need(len(G)==6 and any(prod(a,b)!=prod(b,a) for a in G for b in G),'pointed group S3')
mapping=G+[prod(g,rho) for g in G]
need(len(set(mapping))==12,'basis decomposition')
for a,b in itertools.product(G,repeat=2):
    p=prod(a,b)
    need(R[prod(a,rho)][b]==R[b][prod(a,rho)] if a==0 else True,'central rho')
    need(prod(prod(a,rho),b)==prod(p,rho),'rho right multiplication')
    need(R[prod(a,rho)][prod(b,rho)]==[int(i==p or i in O) for i in range(12)],'rho product')
classes=sorted(set(tuple(sorted({prod(prod(g,x),du[g]) for g in G})) for x in range(12)))
need(classes==[(0,),(1,2),(3,4),(5,8,10),(6,7,9),(11,)],'conjugacy classes')
tailclasses=[(1,2),(5,8,10),(3,4),(6,7,9),(11,)]
oclasses=tailclasses[2:]
B=S.Matrix(12,12,lambda i,j:sum(R[a][i][k]*R[k][du[a]][j] for a in range(12) for k in range(12)))
need(B==B.T and list(B[:,0])==[12,0,0,6,6,0,6,6,0,6,0,6],'induction Gram')
# Formal algebra: C[S3] with a central rho, rho^2=1+(sum_g g)rho.
# Its six irreducibles have degrees 1,1,1,1,2,2. The central Casimir is
# (240+/-72sqrt(10))/2 on trivial group characters and 12 on the rest;
# division by representation degree gives D,D',12,12,6,6.
casimir=sum((S.Matrix(R[a])*S.Matrix(R[du[a]]) for a in range(12)),S.zeros(12))
t=S.Symbol('t')
need(S.factor(casimir.charpoly(t).as_expr())==(t-12)**10*(t*t-240*t+1440),'Casimir spectrum')
def column(c,u):
    v=[0]*12;v[0]=u
    for cl,k in zip(oclasses,c):
        for j in cl:v[j]=k
    return S.Matrix(v)
def parts(m):
    return [(a,b,m-2*a-3*b) for a in range(m//2+1) for b in range(m//3+1) if 2*a+3*b<=m]
low=[]
for a,b,c,e,f in itertools.product(parts(6),parts(3),parts(3),parts(6),parts(6)):
    if all(a[i]+b[i]+c[i]+2*e[i]+2*f[i]==6 for i in range(3)):
        L=S.Matrix.hstack(S.eye(12)[:,0],column(a,1),column(b,1),column(c,1),column(e,2),column(f,2))
        low.append(((a,b,c,e,f),L))
saved=FROZEN['low_branches']
need(len(low)==len(saved)==30,'complete low branch count')
need([list(map(list,x[0])) for x in low]==[x['column_class_coefficients'] for x in saved],'low branch domain')
survivors=[]
for (co,L),rec in zip(low,saved):
    M=B-L*L.T
    # Independent exact characteristic-polynomial sign criterion for a
    # rational symmetric matrix: all eigenvalues >=0 iff coefficients
    # of det(tI+M) are all nonnegative.
    psd=all(x>=0 for x in (-M).charpoly().all_coeffs())
    need(psd==rec['psd'],'low PSD mismatch')
    if psd:survivors.append(L)
need(len(survivors)==4,'PSD survivor count')
ds=[(F(1),F(0)) if i in G else (F(3),F(1)) for i in range(12)]
D=(F(120),F(36))
def mult(x,y):return (x[0]*y[0]+10*x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def high(L):
    Q=B-L*L.T
    ix=[cl[0] for cl in tailclasses]
    W=Q.extract(ix,ix);rank=W.rank()
    piv=next(p for p in itertools.combinations(range(5),rank) if W.extract(p,p).det()!=0)
    inv=W.extract(piv,piv).inv();kernel=W.nullspace();out=[]
    bounds=[math.isqrt(int(W[i,i])) for i in range(5)]
    for cc in itertools.product(*(range(b+1) for b in bounds)):
        if not any(cc):continue
        if any(cc[i]*cc[j]>W[i,j] for i in range(5) for j in range(i,5)):continue
        if any(sum(cc[i]*v[i] for i in range(5)) for v in kernel):continue
        u=S.Matrix([cc[i] for i in piv])
        if (u.T*inv*u)[0]>1:continue
        v=[0]*12
        for cl,c in zip(tailclasses,cc):
            for j in cl:v[j]=c
        z=tuple(sum(v[i]*ds[i][j] for i in range(12)) for j in range(2))
        norm=z[0]*z[0]-10*z[1]*z[1]
        if norm==0:continue
        w=((D[0]*z[0]-10*D[1]*z[1])/norm,(D[1]*z[0]-D[0]*z[1])/norm)
        if (2*w[0]).denominator!=1 or (w[0]**2-10*w[1]**2).denominator!=1:continue
        if z[1] and (4*z[0]**2/norm).denominator!=1:continue
        out.append((tuple(v[1:]),z))
    return Q.extract(range(1,12),range(1,12)),out
def traces():
    out={tuple((F(0),F(0)) for j in range(6))}
    for order in S.divisors(7200):
        for sign in [-1,1]:
            row=[]
            for j in range(1,7):
                gcd=math.gcd(int(order),j);n=int(order)//gcd
                a=F(int(S.mobius(n)),int(S.totient(n)));b=F(0)
                if n%40==0 and math.gcd(n//40,40)==1:
                    b=F(2*sign*int(S.mobius(n//40))*int(S.kronecker_symbol(40,n//40))*int(S.kronecker_symbol(40,j//gcd)),int(S.totient(n)))
                row.append((a,b))
            out.add(tuple(row))
    return sorted(out)
types=traces();need(len(types)==45,'joint trace count')
opts=[]
for i in range(1,12):
    opts.append([0] if du[i]!=i else [1] if any(R[j][du[j]][i]%2 for j in range(12)) else [-1,1])
eps=list(itertools.product(*opts));need(len(eps)==8,'indicator domain')
def system(L,ep):
    Q,cols=high(L);LL=L*L.T
    ell=[tuple(sum(F(int(LL[i,j]))*ds[j][k] for j in range(12)) for k in range(2)) for i in range(1,12)]
    pairs=list(itertools.combinations_with_replacement(range(11),2))
    H={}
    for i in range(1,12):
        power=[int(j==0) for j in range(12)]
        for k in range(1,7):
            power=[sum(power[a]*R[a][i][b] for a in range(12)) for b in range(12)]
            H[i-1,k]=power[0]
    rhs=[F(Q[i,j]) for i,j in pairs]+[-a for v in ell for a in v]
    rhs += [ep[i]*D[k]-ell[i][k] for i in range(11) for k in range(2)]
    rhs += [D[0]*ell[i][1]-D[1]*ell[i][0] for j in range(3,7) for i in range(11)]
    rhs += [D[0]*bound-sign*ell[i][0] for j in range(3,7) for i in range(11) for sign,bound in [(1,F(H[i,j])),(-1,F(H[i,j],min(S.factorint(j))-1))]]
    columns=[]
    for v,z in cols:
        for ts in types:
            moments=[[[v[i]*a for a in mult(z,t)] for i in range(11)] for t in ts]
            col=[F(v[i]*v[j]) for i,j in pairs]
            col += [a for m in moments[:2] for xy in m for a in xy]
            col += [D[1]*moments[j-1][i][0]-D[0]*moments[j-1][i][1] for j in range(3,7) for i in range(11)]
            col += [sign*moments[j-1][i][0] for j in range(3,7) for i in range(11) for sign in (1,-1)]
            columns.append(col)
    for i in range(len(rhs)-88,len(rhs)):
        v=[F(0)]*len(rhs);v[i]=F(1);columns.append(v)
    A=list(map(list,zip(*columns)));b=[]
    for i,row in enumerate(A):
        den=math.lcm(rhs[i].denominator,*(v.denominator for v in row));rr=[int(v*den) for v in row];bb=int(rhs[i]*den);g=math.gcd(bb,*rr) or 1
        A[i]=[v//g for v in rr];b.append(bb//g)
    return A,b,len(cols)
cases=FROZEN['higher_cases']
need(len(cases)==32,'complete Farkas case count')
output=[]
for bi,L in enumerate(survivors):
    for ei,ep in enumerate(eps):
        rec=cases[8*bi+ei]
        need(rec['branch']==bi and rec['indicators']==list(ep) and rec['separated'],'case binding')
        A,b,nc=system(L,ep);y=rec['farkas']
        need(nc==rec['column_count'] and len(types)==rec['trace_types'] and len(A)==rec['rows'],'system metadata')
        need(len(y)==len(b) and all(type(a) is int for a in y),'ray integer format')
        products=[sum(a*c for a,c in zip(row,y)) for row in zip(*A)]
        dot=sum(a*c for a,c in zip(b,y))
        need(min(products)>=0 and dot<0 and dot==rec['bTy'],'exact Farkas inequality')
        output.append({'branch':bi,'indicator_index':ei,'high_columns':nc,'minimum_dual_entry':min(products),'bTy':dot})
        print(f'PASS branch {bi}, indicator {ei}, high columns {nc}',flush=True)
report={'status':'PASS','ring':'R12_1_350','tensor_sha256':hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest(),'low_branches':30,'PSD_survivors':4,'indicator_branches_per_survivor':8,'trace_types':45,'trace_box':7200,'cases':output,'optimizer_used':False,'rank6_imports_used':False}
(HERE/'verification_R350.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='cases'}))
