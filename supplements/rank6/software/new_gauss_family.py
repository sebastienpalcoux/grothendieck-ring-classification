"""Exact all-orders quadratic Gauss obstruction for a rank-six tensor family.

The parameter and ordering are recovered from the full tensor, never from an
ID. Every possible low column and high column is exhausted with proven finite
bounds. See papers/chapters/gauss_family.tex for the categorical proof and the
all-orders root-of-unity length bound. No finite conductor cutoff is used.
"""
import itertools as it
import math
from fractions import Fraction as F
import sympy as s
from exact import require
from rings import validate,casimir,permute


def psd(rows):
    a=[list(map(F,row)) for row in rows]
    if any(a[i][i]<0 for i in range(len(a))):return False
    pivot=next((i for i in range(len(a)) if a[i][i]>0),None)
    if pivot is None:return all(x==0 for row in a for x in row)
    ix=[i for i in range(len(a)) if i!=pivot];q=a[pivot][pivot]
    return psd([[a[i][j]-a[i][pivot]*a[pivot][j]/q for j in ix] for i in ix])


def family(m):
    N=[[[0]*6 for _ in range(6)] for _ in range(6)]
    for i in range(6):
        for t in set(it.permutations((0,i,i))):N[t[0]][t[1]][t[2]]=1
    minus={(1,1,2),(1,1,3),(1,2,2),(2,2,3)}
    plus={(3,4,4),(3,5,5),(4,4,5),(4,5,5)}
    for a,b,c in it.combinations_with_replacement(range(1,6),3):
        value=m+int((a,b,c) in plus)-int((a,b,c) in minus)
        for i,j,k in set(it.permutations((a,b,c))):N[i][j][k]=value
    return N


def identify(R):
    if len(R)!=6:return None
    if any(len(a)!=6 or any(len(b)!=6 for b in a) for a in R):return None
    # The diagonal nonunit coefficients equal the parameter in this family.
    m=R[1][1][1]
    if type(m) is not int or m<3:return None
    if any(R[i][i][i]!=m for i in range(1,6)):return None
    target=family(m)
    for p in it.permutations(range(1,6)):
        q=[0]+list(p)
        if all(R[q[i]][q[j]][q[k]]==target[i][j][k] for i,j,k in it.product(range(6),repeat=3)):
            return m,q
    return None


def check_characters(R,m):
    n=25*m*m+4;r=s.sqrt(n);U=(5*m+r)/2;p=(1+s.sqrt(5))/2;q=(1-s.sqrt(5))/2
    C=s.Matrix([[1,U-1,U-1,U,U+1,U+1],[1,5*m-U-1,5*m-U-1,5*m-U,5*m-U+1,5*m-U+1],
                [1,p,q,-1,0,0],[1,q,p,-1,0,0],[1,0,0,1,-p,-q],[1,0,0,1,-q,-p]])
    require(s.simplify(C.det()+125*r)==0,'incomplete family character table')
    for h,i,j in it.product(range(6),repeat=3):
        require(s.simplify(C[h,i]*C[h,j]-sum(R[i][j][k]*C[h,k] for k in range(6)))==0,'family character identity')
    D=(5*n+25*m*r)/2
    require(all(s.simplify(sum(C[h,i]**2 for i in range(6))-[D,5*n-D,5,5,5,5][h])==0 for h in range(6)),'family codegrees')
    G=casimir(R);j=s.ones(5,1);delta=s.Matrix([-1,-1,0,1,1])
    require(G[0,0]==6 and G[1:,0]==5*m*j+delta,'family Casimir unit column')
    require(G[1:,1:]==5*s.eye(5)+(25*m*m+1)*j*j.T+5*m*(j*delta.T+delta*j.T)+delta*delta.T,'family Casimir block')
    require(int(s.trace(G))==125*m*m+40,'family trace')
    return G

# Twice the four codegree-five characters, in coordinates (1,sqrt(5)).
SMALL_CHARS=[[(2,0),(1,1),(1,-1),(-2,0),(0,0),(0,0)],
             [(2,0),(1,-1),(1,1),(-2,0),(0,0),(0,0)],
             [(2,0),(0,0),(0,0),(2,0),(-1,-1),(-1,1)],
             [(2,0),(0,0),(0,0),(2,0),(-1,1),(-1,-1)]]


def labellings(columns: list[tuple]) -> list[tuple]:
    values=[[tuple(sum(c[k]*row[k][a] for k in range(6)) for a in range(2)) for c in columns] for row in SMALL_CHARS]
    return [p for p in it.permutations(range(4)) if all(values[p[i]][j]==values[p[j]][i] for i,j in it.product(range(4),repeat=2))]


def low_branches(G: s.Matrix, m: int, report: dict) -> list[dict]:
    delta=(-1,-1,0,1,1)
    norm=lambda v:sum(x*x for x in v)
    ws=[v for v in it.product(range(-3,4),repeat=5) if sum(v)==0 and sum(delta[i]*v[i] for i in range(5))==1 and norm(v)<=10]
    require(len(ws)==32, 'number of bounded low deviations')
    stages=[0,0,0,0]; branches=[]
    for inds in it.combinations_with_replacement(range(len(ws)),4):
        w=[ws[i] for i in inds]
        if sum(map(norm,w))>16 or any(sum(v[i] for v in w)!=delta[i] for i in range(5)):continue
        stages[0]+=1
        cols=[(1,)+tuple(m+x for x in v) for v in w]
        labs=labellings(cols)
        if not labs:continue
        stages[1]+=1
        full=[(1,0,0,0,0,0),(1,m,m,m,m,m)]+cols
        Q=[[int(G[i,j])-sum(c[i]*c[j] for c in full) for j in range(6)] for i in range(6)]
        if any(x<0 for row in Q for x in row):continue
        stages[2]+=1
        if not psd(Q):continue
        stages[3]+=1
        branches.append({'columns':full,'labellings':labs,'Q':Q})
    require(stages==[59,11,11,3], 'exhaustive low-stage counts')
    report['low_enumeration']={'deviation_vectors':len(ws),'stages':stages,'stage_meanings':['sum and norm','modular reciprocity','entrywise Gram positivity','positive-semidefinite Gram'], 'branches':branches}
    return branches


def high_columns(branch: dict, m: int) -> tuple[list[tuple], list[int]]:
    Q=s.Matrix(branch['Q'])[1:,1:]; rank=Q.rank()
    ix=next(ii for ii in it.combinations(range(5),rank) if Q.extract(ii,ii).det()!=0)
    sub=Q.extract(ix,ix);adj=[[int(x) for x in row] for row in sub.adjugate().tolist()];det=int(sub.det())
    null=[]
    for z in Q.nullspace():
        den=math.lcm(*(int(x.q) for x in z));null.append([int(x*den) for x in z])
    entries=[[int(x) for x in row] for row in Q.tolist()]
    caps=[math.isqrt(entries[i][i]) for i in range(5)]
    da=math.isqrt(entries[0][0]+entries[1][1]-2*entries[0][1])
    de=math.isqrt(entries[3][3]+entries[4][4]-2*entries[3][4])
    require(Q*s.Matrix([1,1,-4,1,1])==s.zeros(5,1), 'common null equation')
    result=[];counts=[0,0,0]
    # The common null equation determines c; two difference inequalities
    # follow from Q-vv^T >=0. Thus this box includes EVERY possible column.
    for a,d,x,y in it.product(range(caps[0]+1),range(caps[3]+1),range(-da,da+1),range(-de,de+1)):
        b=a+x;e=d+y;total=a+b+d+e
        if not(0<=b<=caps[1] and 0<=e<=caps[4]) or total%4:continue
        c=total//4
        if c>caps[2]:continue
        v=(a,b,c,d,e)
        if not any(v):continue
        counts[0]+=1
        if any(sum(v[i]*z[i] for i in range(5)) for z in null):continue
        vv=[v[i] for i in ix]
        if sum(vv[i]*adj[i][j]*vv[j] for i,j in it.product(range(rank),repeat=2))>det:continue
        if any(v[i]*v[j]>entries[i][j] for i in range(5) for j in range(i,5)):continue
        counts[1]+=1
        n=25*m*m+4; A=5*n; B=25*m
        ar=sum(v[i]*(5*m+2*[-1,-1,0,1,1][i]) for i in range(5));br=sum(v)
        norm=ar*ar-n*br*br
        if norm==0:continue
        qr=F(A*ar-n*B*br,norm);qs=F(B*ar-A*br,norm)
        # D/dim(Y) is integral; trace/norm is an exact quadratic integrality test.
        if (2*qr).denominator!=1 or (qr*qr-n*qs*qs).denominator!=1:continue
        counts[2]+=1;result.append(v)
    return sorted(result),counts



def certificate(R):
    identified=identify(R)
    if identified is None:return None
    m,p=identified;validate(R);N=permute(R,p);G=check_characters(N,m)
    report={'kind':'quadratic_Gauss_family','scope':'pseudo_unitary','parameter':m,'permutation':p}
    branches=low_branches(G,m,report);j=s.ones(5,1);delta=s.Matrix([-1,-1,0,1,1]);E=[s.eye(5)[:,i] for i in range(5)]
    hs=[];counts=[]
    for branch in branches:
        high,stages=high_columns(branch,m);hs.append(high);counts.append(stages)
    if any(any(len(set(v))!=1 for v in hs[i]) for i in (0,2)):return None
    require(all(s.Matrix(branches[i]['Q'])[1:,1:].rank()==2 for i in (0,2)),'outer Gram rank')
    expected=[tuple(k*j) for k in (1,2)]
    expected += [tuple(k*j+sg*(E[a]-E[b])) for k in (1,2) for sg in (-1,1) for a,b in [(0,1),(3,4)]]
    expected += [tuple(k*j-E[a]+E[b]) for k in (m,2*m) for a in (0,1) for b in (3,4)]
    if not set(hs[1]).issubset(set(expected)):return None
    Q=s.Matrix(branches[1]['Q'])[1:,1:];u=E[0]-E[1];v=E[3]-E[4]
    bil=lambda x,y:int((x.T*Q*y)[0])
    identities=[bil(delta,delta),bil(delta,j),bil(u,u),bil(v,v),bil(delta,u),bil(delta,v),bil(u,v)]
    require(identities==[32,80*m,8,8,0,0,0],'Gram multiplicity identities')
    B=[m*j-E[a]+E[b] for a in (0,1) for b in (3,4)]
    L=12*m*m+2
    require(Q-2*sum((b*b.T for b in B),s.zeros(5))==L*j*j.T,'uniform Gram remainder')
    n=25*m*m+4;q=math.prod(int(a) for a,e in s.factorint(n).items() if e%2);b=math.isqrt(n//q)
    require(q>1 and b*b*q==n,'quadratic squarefree part')
    conductor=q if q%4==1 else 4*q;c=math.isqrt(conductor//q)
    require(c*c*q==conductor,'fundamental conductor')
    phi=int(s.totient(conductor));minimum=F(phi*m*b,2*c)
    if minimum<=L:return None
    U=(5*m+s.sqrt(n))/2;z=U**2;t=z+1;w=5*U
    require(s.simplify((-m*z-2*m*t)/w+(m*m+m*s.sqrt(n))/2)==0,'first twist moment')
    report.update(high_stage_counts=counts,high_columns=hs,Gram_identities=identities,
        B_multiplicities=[2,2,2,2],uniform_root_count=L,
        root_sum={'rational':str(F(-m*m,2)),'sqrt_coefficient':str(F(-m*b,2)),'radicand':q},
        Gauss={'fundamental_conductor':conductor,'phi':phi,'single_root_coefficient_bound':str(F(c,phi)),
               'minimum_root_count':str(minimum)},higher_indicators_used=False)
    # Roundtrip normalizes tuples and sympy integer entries for canonical JSON.
    import json
    return json.loads(json.dumps(report,default=int))


def verify(R,c):
    require(c.get('kind')=='quadratic_Gauss_family' and c.get('scope')=='pseudo_unitary','wrong Gauss family kind/scope')
    recomputed=certificate(R)
    require(recomputed is not None and recomputed==c,'incorrect complete quadratic Gauss certificate')
    return True
