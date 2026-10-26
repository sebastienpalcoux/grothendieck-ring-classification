"""Independent exact arithmetic audit of the first-round negative decisions.

This file imports no first-round implementation.  It constructs the Casimir
through the based-ring element sum(b b*), uses prime valuations for d-numbers,
checks quadratic fields by square-free discriminants, and independently
enumerates all oriented signed tables for the inherited rank-eight source.
"""
from pathlib import Path
from collections import Counter
from fractions import Fraction
from itertools import product
import gzip, hashlib, json, math, time
import numpy as np
import sympy as s

HERE=Path(__file__).resolve().parent
BASE=HERE.parents[1]/'rank12-m1-offline-20261025'
t=s.Symbol('t')
checks=Counter()

def require(v,m):
    if not v:raise ValueError(m)

def dual(R):return [next(j for j in range(len(R))if R[i][j][0])for i in range(len(R))]
def casimir(R):
    n=len(R);du=dual(R)
    coefficients=[sum(R[a][du[a]][k]for a in range(n))for k in range(n)]
    return s.Matrix(n,n,lambda i,j:sum(coefficients[k]*R[k][i][j]for k in range(n)))

cp_cache={}
def cp(R):
    key=json.dumps(R,separators=(',',':'))
    if key not in cp_cache:cp_cache[key]=casimir(R).charpoly(t).as_poly()
    return cp_cache[key]

def polynomial(c):return s.Poly.from_list(list(map(s.Rational,c)),t)

def arithmetic(R,c):
    n=len(R);kind=c['kind'];du=dual(R)
    if kind=='casimir_dnumber':
        f=polynomial(c['factor']);require(f.is_irreducible and cp(R).rem(f).is_zero,'Casimir minimal factor')
        a=f.all_coeffs();d=f.degree();j=c['index'];norm=abs(int(a[-1]));bad=[]
        for p,v in s.factorint(norm).items():
            b=abs(int(a[j]));w=0
            if b==0:continue
            while b%p==0:w+=1;b//=p
            if d*w<j*v:bad.append(int(p))
        require(bool(bad),'d-number prime valuation')
    elif kind=='generalized_near_group_divisibility':
        G=[i for i in range(n)if sum(R[i][du[i]])==1];X=set(range(n))-set(G);x=c['object']
        require({R[g][x].index(1)for g in G}==X,'two orbit hypothesis')
        h=sum(R[g][x][x]for g in G);r=sum(R[x][du[x]][i]for i in X)
        require(math.isqrt(r*r+4*h)**2!=r*r+4*h and r%h!=0,'irrational two-value divisibility')
    elif kind=='near_group_small_m':
        G=[i for i in range(n)if sum(R[i][du[i]])==1];x=c['object']
        require(len(G)==n-1 and all(R[i][j]==R[j][i]for i in range(n)for j in range(n)),'commutative near-group hypothesis')
        require(all(R[x][x][g]==1 and R[g][x][x]==R[x][g][x]==1 for g in G),'near-group fusion')
        require(0<R[x][x][x]<len(G)-1,'small multiplicity')
    elif kind in ('integral_drinfeld','noncomm_integral_drinfeld'):
        d=c['dims'];require(d[0]==1 and all(type(v)is int and v>0 for v in d),'positive integral character')
        require(all(sum(R[i][j][k]*d[k]for k in range(n))==d[i]*d[j]for i,j in product(range(n),repeat=2)),'dimension character')
        D=sum(v*v for v in d);q=polynomial(c['failed_factor']);require(q.is_irreducible and cp(R).rem(q).is_zero,'central factor')
        if q.degree()>1:pass
        elif kind=='integral_drinfeld':
            require(all(R[i][j]==R[j][i]for i,j in product(range(n),repeat=2)),'commutative scope')
            require(D%int(-q.TC())!=0,'integer center dimension')
        else:
            m=c['multiplicity'];require(cp(R).rem(q**m).is_zero and not cp(R).rem(q**(m+1)).is_zero,'regular multiplicity')
            lam=int(-q.TC());es=[e for e in range(1,math.isqrt(m)+1)if lam%e==0 and D%(lam//e)==0]
            reachable=[True]+[False]*m
            for k in range(1,m+1):reachable[k]=any(k>=e*e and reachable[k-e*e]for e in es)
            require(not reachable[m],'regular square-degree partition')
    else:raise ValueError(kind)
    checks[kind]+=1

def cyclic(R,c):
    n=len(R);g=c['g'];x,y,z=(c[k]for k in ('X','Y','Z'));du=dual(R)
    require(R[g][du[g]][0]==1 and sum(R[g][du[g]])==1,'invertible g')
    u=0;order=0
    while True:
        require(sum(R[u][g])==1,'single invertible product');u=R[u][g].index(1);order+=1
        if not u:break
        require(order<=n,'finite order')
    require(order==c['order'],'exact cyclic order')
    basis=lambda i:[int(i==j)for j in range(n)]
    require(R[g][x]==basis(x)and R[y][g]==basis(y)and R[g][z]==R[z][g]==basis(z),'fixedness')
    m=R[x][y][z];require(m==c['multiplicity']>0,'occurring isotypic summand')
    p=s.Matrix(R[z]).charpoly(t).as_poly();f=polynomial(c['dimension_polynomial']);lo,hi=p.intervals(eps=s.Rational(1,10**12))[-1][0]
    require(f.is_irreducible and p.rem(f).is_zero,'irreducible Perron factor')
    require(f.eval(lo)==0 if lo==hi else f.count_roots(lo,hi)==1,'Perron root bound')
    q=order//math.gcd(order,m);scaled=s.Poly(f.as_expr().subs(t,q*t)/q**f.degree(),t)
    require(any(v.q!=1 for v in scaled.all_coeffs()),'nonintegral normalized dimension')
    checks['cyclic']+=1

def sf(n):return math.prod(p for p,v in s.factorint(abs(int(n))).items()if v%2)

def central(R,r,c):
    n=len(R);f=polynomial(r['field_polynomial']);require(f.degree()==2 and f.is_irreducible,'quadratic source field')
    alpha=s.CRootOf(f,1);ds=[s.Poly.from_list(list(map(s.Rational,co)),t).eval(alpha)for co in r['dimensions_in_field']]
    K=s.QQ.algebraic_field(alpha);dds=[K.from_sympy(v)for v in ds]
    require(dds[0]==K.one and all(v.evalf()>0 for v in ds),'positive field character')
    require(all(sum((R[i][j][k]*dds[k]for k in range(n)),K.zero)==dds[i]*dds[j]for i,j in product(range(n),repeat=2)),'exact quadratic dimension character')
    require(len(set(dds))==2,'published two-dimension Galois PU bridge')
    q=polynomial(c['casimir_factor']);require(q.is_irreducible and cp(R).rem(q).is_zero,'exact Casimir factor')
    if c['kind']=='central_dimension_field':
        require(q.degree()==2,'quadratic required field')
        require(sf(s.discriminant(q))!=sf(s.discriminant(f)),'distinct quadratic fields')
    else:
        require(all(R[i][j]==R[j][i]for i,j in product(range(n),repeat=2)),'one-dimensional irreps')
        d=next(v for v in dds if v!=K.one);D=sum((v*v for v in dds),K.zero);beta=D/K(-q.TC())
        # The lattice is Z + Z*d. Solve in the power basis directly,
        # independently of the original HNF implementation.
        def col(v):
            co=list(reversed(v.to_list()));return s.Matrix(co+[0]*(2-len(co)))
        coords=s.Matrix.hstack(col(K.one),col(d)).inv()*col(beta)
        require(any(v.q!=1 for v in coords),'not in the integer dimension span')
    checks[c['kind']]+=1

def primary(R,c):
    n=len(R);sq=c['squared_dimensions'];d=list(map(math.isqrt,sq))
    require(all(a*a==q for a,q in zip(d,sq)),'these six examples are integral')
    require(all(sum(R[i][j][k]*d[k]for k in range(n))==d[i]*d[j]for i,j in product(range(n),repeat=2)),'integral dimension vector')
    D=sum(sq);require(D==216 and len(s.factorint(D))==2,'solvability/unitarity gate')
    # Prove every intermediate int64 accumulation is within range, then
    # use a matrix flattening order distinct from the stored einsum replay.
    V=np.array(c['vector'],dtype=np.int64).reshape((n,n,n));vmax=max(map(abs,c['vector']))
    bound=n**6*vmax*vmax;require(bound<2**63,'no integer overflow possible')
    def act(A,T,axis):
        a=np.moveaxis(T,axis,0);shape=a.shape
        return np.moveaxis((A@a.reshape((n,-1))).reshape(shape),0,axis)
    coefficients=[]
    for row in R:
        A=np.array(row,dtype=np.int64);T=V
        for axis in range(3):T=act(A,T,axis)
        coefficients.append(int(np.sum(V*T)))
    require(coefficients==c['coefficients'],'independent primary contraction')
    value=sum((Fraction(a,b)for a,b in zip(coefficients,d)),Fraction())
    require(value<0,'exact rational negative value')
    checks['primary_exact_rational']+=1
    return str(value)

def rank8_signed():
    z=json.loads((BASE/'lower_rank8_signed.json').read_text());R=z['source_record']['tensor'];n=len(R);du=dual(R)
    unseen=set(product(range(1,n),repeat=3));orbits=[]
    while unseen:
        a,b,c=min(unseen);orb={(a,b,c),(b,c,a),(c,a,b),(du[c],du[b],du[a]),(du[b],du[a],du[c]),(du[a],du[c],du[b])}
        unseen.difference_update(orb)
        if R[a][b][du[c]]:orbits.append(sorted(orb))
    require(len(orbits)==13,'rank-eight finite sign-box size')
    template=np.zeros((n,n,n),dtype=np.int64)
    for i in range(n):template[0,i,i]=template[i,0,i]=template[i,du[i],0]=1
    survivors=[]
    for bits in product((-1,1),repeat=len(orbits)):
        T=template.copy()
        for value,orb in zip(bits,orbits):
            for i,j,k in orb:T[i,j,du[k]]=value
        L=np.einsum('ijm,mkl->ijkl',T,T,optimize=True)
        Q=np.einsum('jkm,iml->ijkl',T,T,optimize=True)
        if np.array_equal(L,Q):survivors.append(T)
    gauges=[]
    for tail in product((-1,1),repeat=n-1):
        g=(1,)+tail
        if any(g[i]!=g[du[i]]for i in range(n)):continue
        gauges.append(np.array([[[g[i]*g[j]*g[k]*R[i][j][k]for k in range(n)]for j in range(n)]for i in range(n)]))
    require(all(any(np.array_equal(T,U)for U in gauges)for T in survivors),'every associative oriented signed table is an original sign gauge')
    checks['rank8_unrestricted_signed_signboxes']=2**len(orbits)
    checks['rank8_unrestricted_associative_signed_tables']=len(survivors)
    return dict(variables=len(orbits),full_sign_boxes=2**len(orbits),associative_tables=len(survivors),all_gauge_original=True,
                note='No positive-indicator restriction is needed for this stronger independent check.')

def main():
    start=time.monotonic();data=json.loads((BASE/'tensors.json').read_text());accepted=set();primary_values={}
    with gzip.open(BASE/'input/rank12_M1_verified/FusionRingMultiplicationTables.txt.gz','rt')as f:
        lines=f.readlines()
    require(len(lines)==632,'source cardinality')
    for i,line in enumerate(lines,1):
        R=json.loads(line.replace('{','[').replace('}',']'))
        require(R==data[f'R12_1_{i}'],'physical input binding')
    checks['source_physical_lines']=632
    for r in json.loads((BASE/'arithmetic.json').read_text()):
        for c in r['certificates']:arithmetic(data[r['id']],c);accepted.add(r['id'])
    for r in json.loads((BASE/'cyclic.json').read_text())['records']:
        if r['certificate']:cyclic(data[r['id']],r['certificate']);accepted.add(r['id'])
    for r in json.loads((BASE/'field_checks.json').read_text())['records']:
        for c in r['certificates']:central(data[r['id']],r,c);accepted.add(r['id'])
    for r in json.loads((BASE/'primary_full.json').read_text())['records']:
        if r['certificate']:primary_values[r['id']]=primary(data[r['id']],r['certificate']);accepted.add(r['id'])
    signed=rank8_signed()
    out=dict(status='PASS',checks=dict(checks),distinct_direct_exclusions_independently_recomputed=len(accepted),primary_quadratic_values=primary_values,rank8_signed=signed,elapsed_seconds=time.monotonic()-start)
    (HERE/'independent_audit.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
    return accepted

if __name__=='__main__':main()
