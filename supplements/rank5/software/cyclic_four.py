"""Cyclic-four central-support obstruction, independent of census labels.

The manuscript proves the finite central-support reduction. Discovery uses
linear programming only to propose integer separating vectors; verification
reconstructs every branch and checks the vectors with integer arithmetic.
"""
from fractions import Fraction as Q
from functools import lru_cache
import itertools, math
import sympy as s
from exact import require
from higher_traces import trace_types, mul, farkas, check_farkas


def parameter(R):
    if len(R)!=5:return None
    invertible=[]
    for i in range(5):
        ds=[j for j in range(5) if R[i][j][0]==1]
        if len(ds)==1 and R[i][ds[0]]==[1,0,0,0,0]:invertible.append(i)
    if len(invertible)!=4:return None
    x=next(i for i in range(5) if i not in invertible)
    def product(i,j):
        v=R[i][j]
        return v.index(1) if sum(v)==1 and 1 in v else None
    for gen in invertible:
        if gen==0:continue
        powers=[0]
        for _ in range(3):powers.append(product(powers[-1],gen))
        if None in powers or len(set(powers))!=4 or product(powers[-1],gen)!=0:continue
        m=R[x][x][x]
        if m<=0 or m%4:return None
        good=True
        for a,b in itertools.product(range(5),repeat=2):
            v=[0]*5
            if a==x and b==x:
                for g in invertible:v[g]=1
                v[x]=m
            elif a==x or b==x:v[x]=1
            else:v[powers[(powers.index(a)+powers.index(b))%4]]=1
            good=good and R[a][b]==v
        if good:return m//4
    return None


def branches(k):
    """Unordered single-support pairs; subgroup and involution constraints."""
    out=[]
    for u in itertools.product(range(k//2+1),repeat=3):
        zeros={0}|{r for r in (1,2,3) if u[r-1]==0}
        if zeros not in ({0},{0,2},{0,1,2,3}):continue
        h=len(zeros)
        if u[0]!=u[2]:continue
        for epsilon in (-1,1):
            out.append({'u':list(u),'h':h,'epsilon':epsilon})
    return out


def galois_failure(k,branch):
    # With a unique central invertible and three balanced pairs, the Galois
    # row of the unit gives N_AA^E=k^2/8 for each single-support E != 1,A.
    return (branch['h']==1 and all(2*u==k for u in branch['u'])
            and k*k%8!=0)


def _row_normalize(A,b):
    out=[];bb=[]
    for row,rhs in zip(A,b):
        den=math.lcm(rhs.denominator,*(v.denominator for v in row))
        r=[int(v*den) for v in row];v=int(rhs*den)
        g=math.gcd(v,*r) or 1
        out.append([x//g for x in r]);bb.append(v//g)
    return out,bb


@lru_cache(None)
def parameters(k,height):
    r=k*k+1
    q=math.prod(int(p) for p,e in s.factorint(r).items() if e%2)
    require(q>1,'rational near-group dimension is not supported')
    h=math.isqrt(r//q)
    d=(Q(2*k),Q(2*h));D=(Q(8*r),Q(8*k*h))
    primes=sorted(set([2]+list(map(int,s.factorint(r)))))
    types,bound=trace_types(q,primes,height)
    return q,d,D,types,bound


def system(k,branch,height):
    q,d,D,types,bound=parameters(k,height)
    u1,u2,u3=branch['u'];h=branch['h'];epsilon=branch['epsilon']
    L=[k*k]+[u*u+(k-u)*(k-u) for u in (u1,u2,u3)]
    total=8+10*k*k-sum(L)
    masses=[total] if h==1 else [4+6*k*k-sum(L),4+4*k*k]
    require(all(v>=0 for v in masses),'negative central mass')
    # (a,b,e) represents restriction dimension a+b*d and twist i^e.
    mixed=[]
    for r,u in enumerate((0,u1,u2,u3)):
        e=0 if r in (0,2) else 3
        mixed += [(1,u,e),(1,k-u,e)]
    mixed += [(2,k,0)]*3+[(2,k,2)]*2+[(2,k,1)]
    def known(j):
        aa=bb=0
        for a,b,e in mixed:
            cos=(1,0,-1,0)[(e*j)%4]
            aa+=a*b*cos;bb+=b*b*cos
        return (Q(aa)+bb*d[0],bb*d[1])
    knowns=[known(j) for j in range(1,height+1)]
    F=q if q%4==1 else 4*q
    rational=[j for j in range(3,height+1) if j%F]
    H={};alpha,beta=0,1
    for j in range(1,height+1):
        H[j]=alpha
        alpha,beta=beta,4*alpha+4*k*beta
    # Moment variables are weighted counts b_Z^2, relaxed to >=0 reals.
    variables=[]
    for pool in range(len(masses)):
        ts=types if pool==0 else sorted(set(tuple((Q(0),Q(0)) if j%2 else t for j,t in enumerate(tau,1)) for tau in types))
        for tau in ts:variables.append((pool,tau))
    nv=len(variables);A=[];b=[];slacks=[]
    def add(row,rhs,slack=False):
        A.append(list(map(Q,row)));b.append(Q(rhs))
        if slack:slacks.append(len(A)-1)
    for pool,mass in enumerate(masses):add([int(p==pool) for p,tau in variables],mass)
    for j in (1,2):
        target=(Q(0),Q(0)) if j==1 else (epsilon*D[0],epsilon*D[1])
        for c in range(2):add([mul(d,tau[j-1],q)[c] for p,tau in variables],target[c]-knowns[j-1][c])
    for j in rational:
        low=knowns[j-1]
        values=[mul(d,tau[j-1],q) for p,tau in variables]
        add([D[1]*v[0]-D[0]*v[1] for v in values],-(D[1]*low[0]-D[0]*low[1]))
        pmin=min(map(int,s.factorint(j)))
        add([v[0] for v in values],H[j]*D[0]-low[0],True)
        add([-v[0] for v in values],Q(H[j],pmin-1)*D[0]+low[0],True)
    for row in A:row.extend([Q(0)]*len(slacks))
    for offset,idx in enumerate(slacks):A[idx][nv+offset]=Q(1)
    A,b=_row_normalize(A,b)
    return A,b,{'q':q,'height':height,'order_bound':bound,'trace_types':len(types),'mass':masses,'rows':len(b),'columns':len(A[0])}


def certificate(R,height=6):
    k=parameter(R)
    if k is None:return None
    outcomes=[]
    for branch in branches(k):
        rec=dict(branch)
        if galois_failure(k,branch):rec['obstruction']={'kind':'galois_fusion_integrality','numerator':k*k,'denominator':8}
        else:
            A,b,meta=system(k,branch,height)
            y=farkas(A,b)
            if y is None:return None
            rec['obstruction']={'kind':'central_trace','y':y,'meta':meta,'bTy':sum(x*z for x,z in zip(b,y))}
        outcomes.append(rec)
    return {'kind':'cyclic_four_central','parameter':k,'height':height,'branches':outcomes}


def verify(R,cert):
    k=parameter(R);require(k is not None and k==cert['parameter'],'cyclic-four tensor mismatch')
    require(cert['kind']=='cyclic_four_central','wrong cyclic-four certificate')
    bb=branches(k);require(len(bb)==len(cert['branches']),'missing central-support branch')
    for branch,rec in zip(bb,cert['branches']):
        require(all(rec[x]==branch[x] for x in branch),'wrong central-support branch')
        why=rec['obstruction']
        if why['kind']=='galois_fusion_integrality':
            require(galois_failure(k,branch),'Galois fusion integrality survives')
            require(why['numerator']==k*k and why['denominator']==8,'wrong fusion coefficient')
        else:
            require(why['kind']=='central_trace','unknown cyclic-four test')
            A,b,meta=system(k,branch,cert['height'])
            require(meta==why['meta'],'different central trace system')
            check_farkas(A,b,why['y'])
            require(why['bTy']==sum(x*z for x,z in zip(b,why['y'])),'wrong separating value')
