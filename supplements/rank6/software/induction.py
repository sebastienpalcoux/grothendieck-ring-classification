"""Rank-independent application of the low-induction and moment tests of [DP]."""
from native_build import ensure_native
import itertools,math,subprocess,tempfile
from pathlib import Path
import sympy as s
from exact import *
from rings import *

def restriction_columns(ds,beta,K,B):
    """All columns (1,v1,v2,v3) with the required dimension.

    The bounds vi<=B[0,i] and vi^2<=B[i,i] are necessary consequences of
    M M^T=B. Rational row reduction eliminates all dependent equations.
    """
    n=len(ds);tail=n-1
    degree=K.mod.degree()
    A=s.Matrix.hstack(*(vector(d,degree) for d in ds[1:]))
    b=vector(beta-K.one,degree)
    rr,piv=A.row_join(b).rref()
    if tail in piv:return []
    free=[j for j in range(tail) if j not in piv]
    bounds=[min(int(B[0,i]),math.isqrt(int(B[i,i]))) for i in range(1,n)]
    out=[]
    for chosen in itertools.product(*(range(bounds[j]+1) for j in free)):
        v=[s.S.Zero]*tail
        for j,a in zip(free,chosen):v[j]=s.Integer(a)
        for row,j in enumerate(piv):v[j]=rr[row,tail]-sum(rr[row,k]*v[k] for k in free)
        if all(a.q==1 and 0<=a<=bounds[j] for j,a in enumerate(v)):
            out.append((1,)+tuple(map(int,v)))
    return sorted(out)

_low_cache={}
_low_temp=None
def low_matrices(column_sets,B,gram_prune=False):
    n=B.rows;unit=(1,)+(0,)*(n-1);target=tuple(int(B[0,i])-unit[i] for i in range(n))
    if not column_sets:return []
    if gram_prune and n!=5:
        require(2<=n<=6 and len(column_sets)==n-1,'rank-six Gram shape')
        import os
        exe=Path(__file__).with_name('low_generic')
        source=Path(__file__).with_name('low_generic.cpp')
        ensure_native(source,exe,flags=('-O3', '-std=c++17'))
        require(all(abs(int(x))<=10**6 for x in B),'native Gram integer bound')
        values=[n-1,len(column_sets)]+list(target[1:])+[int(B[i,j]) for i in range(1,n) for j in range(1,n)]
        for cols in column_sets:
            values.append(len(cols));values.extend(x for col in cols for x in col[1:])
        run=subprocess.run([str(exe)],input=' '.join(map(str,values)),capture_output=True,text=True,check=True,timeout=60)
        return sorted((unit,)+tuple(column_sets[i][j] for i,j in enumerate(map(int,line.split()))) for line in run.stdout.splitlines())
    if gram_prune:
        require(n==5 and len(column_sets)==4,'native Gram pruning is rank five')
        require(all(abs(int(x))<=10**6 for x in B),'native Gram input exceeds checked integer range')
        global _low_temp
        key=(tuple(tuple(cols) for cols in column_sets),tuple(map(int,B)))
        if key in _low_cache:return _low_cache[key]
        if _low_temp is None:
            _low_temp=tempfile.TemporaryDirectory();exe=Path(_low_temp.name)/'low'
            subprocess.run(['g++','-O3','-std=c++17',str(Path(__file__).with_name('low_completion.cpp')),'-o',str(exe)],check=True,capture_output=True)
        exe=Path(_low_temp.name)/'low'
        values=list(target[1:])+[int(B[i,j]) for i in range(1,n) for j in range(1,n)]
        for cols in column_sets:
            values.append(len(cols));values.extend(x for col in cols for x in col[1:])
        run=subprocess.run([str(exe)],input=' '.join(map(str,values)),capture_output=True,text=True,check=True)
        out=sorted((unit,)+tuple(column_sets[i][j] for i,j in enumerate(map(int,line.split()))) for line in run.stdout.splitlines())
        _low_cache[key]=out;return out
    if len(column_sets)==4:
        # Exact meet-in-the-middle row sums.  The output order agrees with
        # the direct Cartesian enumeration, including repeated codegrees.
        partitions=[((0,1),(2,3)),((0,2),(1,3)),((0,3),(1,2))]
        left,right=min(partitions,key=lambda p:math.prod(len(column_sets[i]) for i in p[0])+math.prod(len(column_sets[i]) for i in p[1]))
        if math.prod(len(column_sets[i]) for i in left)>math.prod(len(column_sets[i]) for i in right):left,right=right,left
        buckets={}
        for a,b in itertools.product(*(column_sets[i] for i in left)):
            if column_sets[left[0]]==column_sets[left[1]] and a>b:continue
            key=tuple(x+y for x,y in zip(a,b))
            if any(x>t for x,t in zip(key,target)):continue
            buckets.setdefault(key,[]).append((a,b))
        out=[]
        for a,b in itertools.product(*(column_sets[i] for i in right)):
            if column_sets[right[0]]==column_sets[right[1]] and a>b:continue
            key=tuple(t-x-y for t,x,y in zip(target,a,b))
            for c,d in buckets.get(key,[]):
                cols=[None]*4;cols[left[0]]=c;cols[left[1]]=d;cols[right[0]]=a;cols[right[1]]=b
                if any(column_sets[i]==column_sets[j] and cols[i]>cols[j] for i in range(4) for j in range(i+1,4)):continue
                out.append((unit,)+tuple(cols))
        return sorted(out)
    last=set(column_sets[-1]);out=[]
    for cols in itertools.product(*column_sets[:-1]):
        c=tuple(target[i]-sum(v[i] for v in cols) for i in range(n))
        if c in last:
            allcols=cols+(c,)
            if any(column_sets[i]==column_sets[j] and allcols[i]>allcols[j] for i in range(len(allcols)) for j in range(i+1,len(allcols))):continue
            out.append((unit,)+allcols)
    return out

def low_failure(cols,B,ds,D,K,emb,du):
    n=len(ds)
    LL=[[sum(c[i]*c[j] for c in cols) for j in range(n)] for i in range(n)]
    Q=[[int(B[i,j])-LL[i][j] for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(i,n):
            if Q[i][j]<0:return {'kind':'gram_entry','coordinates':[i,j]}
    for size in range(1,n):
        for ix in itertools.combinations(range(1,n),size):
            if size==1:det=Q[ix[0]][ix[0]]
            elif size==2:
                i,j=ix;det=Q[i][i]*Q[j][j]-Q[i][j]*Q[j][i]
            elif size==3:
                i,j,k=ix;det=Q[i][i]*(Q[j][j]*Q[k][k]-Q[j][k]*Q[k][j])-Q[i][j]*(Q[j][i]*Q[k][k]-Q[j][k]*Q[k][i])+Q[i][k]*(Q[j][i]*Q[k][j]-Q[j][j]*Q[k][i])
            else:det=s.Matrix([[Q[i][j] for j in ix] for i in ix]).det()
            if det<0:return {'kind':'gram_minor','coordinates':list(ix)}
    for i in range(1,n):
        low=sum((K(LL[i][j])*ds[j] for j in range(n)),K.zero)
        gap=(K(3)*low-D*ds[i]) if du[i]!=i else ((K(3)*ds[i]+K.one)*low-D*ds[i]*(ds[i]+K.one))
        if emb.sign(gap)>0:return {'kind':'moment','object':i,'nonselfdual':du[i]!=i,'gap':ec(gap)}
    return None

def pseudo_certificate(R,gram_prune=False):
    n=len(R)
    a=Characters(R);f,K,ds,D,pD,emb=a.fp();p=codegree_poly(R)
    early=global_moment_certificate(R,a)
    if early is not None:return early
    roots=discover_roots(p,K)
    if roots is None:return global_moment_certificate(R,a)
    check_roots(p,K,roots)
    rest=list(roots);require(D in rest,'FP codegree absent');rest.remove(D)
    B=a.C;cs=[restriction_columns(ds,D/r,K,B) for r in rest]
    lows=low_matrices(cs,B,gram_prune=gram_prune) if all(cs) else []
    failures=[]
    for cols in lows:
        why=low_failure(cols,B,ds,D,K,emb,a.du)
        if why is None:return global_moment_certificate(R,a)
        failures.append({'columns':[list(c) for c in cols],'obstruction':why})
    return {'kind':'induction','generator':a.k,'fp_factor':pc(f), 'gram_pruned':gram_prune,
            'roots':[ec(r) for r in roots],
            'column_counts':[len(v) for v in cs],
            'low_count':len(lows),'failures':failures}

def check_pseudo(R,c):
    if c['kind']=='global_codegree_moment':
        a=Characters(R,c['generator'])
        require(global_moment_certificate(R,a)==c,'global codegree moment not excluded')
        return
    require(c['kind']=='induction','unknown pseudo-unitary proof')
    a=Characters(R,c['generator']);f,K,ds,D,pD,emb=a.fp()
    require(pc(f)==c['fp_factor'],'wrong FP factor')
    roots=[K([s.Rational(v) for v in r]) for r in c['roots']]
    require(all(len(r)<=f.degree() for r in c['roots']),'unreduced root vector')
    check_roots(codegree_poly(R),K,roots)
    rest=list(roots);require(D in rest,'missing FP codegree');rest.remove(D)
    cs=[restriction_columns(ds,D/r,K,a.C) for r in rest]
    lows=low_matrices(cs,a.C,gram_prune=c.get('gram_pruned',False)) if all(cs) else []
    require([len(v) for v in cs]==c['column_counts'] and len(lows)==c['low_count'],'incomplete low enumeration')
    require(len(c['failures'])==len(lows),'missing low-matrix branches')
    for cols,branch in zip(lows,c['failures']):
        require([list(v) for v in cols]==branch['columns'],'wrong low columns')
        require(low_failure(cols,a.C,ds,D,K,emb,a.du)==branch['obstruction'],'low obstruction not verified')

def global_moment_certificate(R,a=None):
    """Squared central dimensions, with the twist-one mass of I(1) removed.

    Cauchy--Schwarz gives 2(D-h)^2 <= (D^2-h)(D^2+D*S-2h),
    where h=D^2*trace(C^-2) and S sums only the self-dual FP dimensions.
    No splitting-field assumption or numerical sign decision is used.
    """
    n=len(R)
    if a is None:a=Characters(R)
    f,K,ds,D,pD,emb=a.fp()
    w=s.trace(a.C.inv()**2)
    S=sum((ds[i] for i in range(n) if a.du[i]==i),K.zero)
    h=K(w)*D*D
    gap=K(2)*(D-h)**2-(D*D-h)*(D*D+D*S-K(2)*h)
    if emb.sign(gap)<=0:return None
    return {'kind':'global_codegree_moment','generator':a.k,'fp_factor':pc(f),
            'inverse_square_sum':str(w),'S':ec(S),'gap':ec(gap)}
