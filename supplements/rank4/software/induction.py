"""Uniform finite central-induction certificates, including dependent dimensions."""
import itertools,math
import sympy as s
from exact import *
from rings import *

def root_length_certificate(R):
    c=root_family(R)
    if not c:return None
    n=c['n'];fac=s.factorint(9*n*n+4)
    d=math.prod(int(p) for p,v in fac.items() if v%2)
    w=math.prod(int(p)**(int(v)//2) for p,v in fac.items())
    f=d if d%4==1 else 4*d;k=math.isqrt(f//d)
    lam=s.Rational(int(s.totient(f))-abs(int(s.mobius(f))),k)
    terms=4*n*n+2;lower=(n*n+n*w*lam)/2
    if lower>terms or n==2:
        c.update({'squarefree':d,'square_factor':w,'conductor':f,'lambda':str(lam),
                  'terms':terms,'lower_bound':str(lower),'boundary':n==2})
        return c
    return None

def check_root_length(R,c):
    actual=root_length_certificate(R)
    require(actual is not None and actual==c,'quadratic root-length hypotheses fail')

def restriction_columns(ds,beta,K,B):
    """All columns (1,v1,v2,v3) with the required dimension.

    The bounds vi<=B[0,i] and vi^2<=B[i,i] are necessary consequences of
    M M^T=B. Rational row reduction eliminates all dependent equations.
    """
    degree=K.mod.degree()
    A=s.Matrix.hstack(*(vector(d,degree) for d in ds[1:]))
    b=vector(beta-K.one,degree)
    rr,piv=A.row_join(b).rref()
    if 3 in piv:return []
    free=[j for j in range(3) if j not in piv]
    bounds=[min(int(B[0,i]),math.isqrt(int(B[i,i]))) for i in range(1,4)]
    out=[]
    for chosen in itertools.product(*(range(bounds[j]+1) for j in free)):
        v=[s.S.Zero]*3
        for j,a in zip(free,chosen):v[j]=s.Integer(a)
        for row,j in enumerate(piv):v[j]=rr[row,3]-sum(rr[row,k]*v[k] for k in free)
        if all(a.q==1 and 0<=a<=bounds[j] for j,a in enumerate(v)):
            out.append((1,)+tuple(map(int,v)))
    return sorted(out)

def low_matrices(column_sets,B):
    unit=(1,0,0,0);target=tuple(int(B[0,i])-unit[i] for i in range(4))
    last=set(column_sets[2]);out=[]
    for a,b in itertools.product(column_sets[0],column_sets[1]):
        c=tuple(target[i]-a[i]-b[i] for i in range(4))
        if c in last:out.append((unit,a,b,c))
    return out

def low_failure(cols,B,ds,D,K,emb,du):
    L=s.Matrix.hstack(*(s.Matrix(c) for c in cols));Q=B-L*L.T
    for i in range(4):
        for j in range(i,4):
            if Q[i,j]<0:return {'kind':'gram_entry','coordinates':[i,j]}
    for size in range(1,4):
        for ix in itertools.combinations(range(1,4),size):
            if Q.extract(ix,ix).det()<0:return {'kind':'gram_minor','coordinates':list(ix)}
    for i in range(1,4):
        low=sum((K(int((L*L.T)[i,j]))*ds[j] for j in range(4)),K.zero)
        gap=(K(3)*low-D*ds[i]) if du[i]!=i else ((K(3)*ds[i]+K.one)*low-D*ds[i]*(ds[i]+K.one))
        if emb.sign(gap)>0:return {'kind':'moment','object':i,'nonselfdual':du[i]!=i,'gap':ec(gap)}
    # Uniform propagation from an invertible involution. The Gram residual
    # determines the two additional columns of I(g), without a named ring.
    masses=[sum((K(int((L*L.T)[i,j]))*ds[j] for j in range(4)),K.zero) for i in range(4)]
    for g in range(1,4):
        if du[g]!=g or ds[g]!=K.one or Q[g,g]!=2:continue
        W=masses[g]
        if emb.sign(W)<=0 or emb.sign(D/K(2)-W)<=0:continue
        if D/K(2)-W!=K.one:continue
        for i in range(1,4):
            if i==g:continue
            gap=K(2)*masses[i]+D*K(int(Q[g,i]))-D*(ds[i]+K.one)
            if emb.sign(gap)>0:
                return {'kind':'involution_moment','involution':g,'object':i,'gap':ec(gap)}
    return None

def pseudo_certificate(R):
    q=root_length_certificate(R)
    if q:return q
    a=Characters(R);f,K,ds,D,pD,emb=a.fp();p=codegree_poly(R)
    roots=discover_roots(p,K)
    if roots is None:return global_moment_certificate(R,a)
    check_roots(p,K,roots)
    rest=list(roots);require(D in rest,'FP codegree absent');rest.remove(D)
    B=a.C;cs=[restriction_columns(ds,D/r,K,B) for r in rest]
    lows=low_matrices(cs,B) if all(cs) else []
    failures=[]
    for cols in lows:
        why=low_failure(cols,B,ds,D,K,emb,a.du)
        if why is None:return global_moment_certificate(R,a)
        failures.append({'columns':[list(c) for c in cols],'obstruction':why})
    return {'kind':'induction','generator':a.k,'fp_factor':pc(f),
            'roots':[ec(r) for r in roots],
            'column_counts':[len(v) for v in cs],
            'low_count':len(lows),'failures':failures}

def check_pseudo(R,c):
    if c['kind']=='root_length':check_root_length(R,c);return
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
    lows=low_matrices(cs,a.C) if all(cs) else []
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
    if a is None:a=Characters(R)
    f,K,ds,D,pD,emb=a.fp()
    w=s.trace(a.C.inv()**2)
    S=sum((ds[i] for i in range(4) if a.du[i]==i),K.zero)
    h=K(w)*D*D
    gap=K(2)*(D-h)**2-(D*D-h)*(D*D+D*S-K(2)*h)
    if emb.sign(gap)<=0:return None
    return {'kind':'global_codegree_moment','generator':a.k,'fp_factor':pc(f),
            'inverse_square_sum':str(w),'S':ec(S),'gap':ec(gap)}
