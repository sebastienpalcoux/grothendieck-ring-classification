"""Bounded central-induction certificates with polynomial object inequalities.

Each candidate vector is one row M[a,i]=[F(Z_a):X_i], indexed by i.
The low part L consists of center-indexed rows and its Gram matrix is L.T*L.
Certificate schema keys ``columns`` and ``column_counts`` are retained stable
identifiers: their values are respectively low rows and candidate-row counts.
``polynomial_row`` denotes the second-indicator inequality for the simple
object i; ``third_indicator_row`` denotes the third-indicator inequality.
``fourth_indicator_row`` records the integer floor in the fourth-indicator
inequality, certified by exact signs at the Frobenius--Perron embedding.
"""
import itertools,math
import sympy as s
from exact import *
from rings import *

def induction_rows(ds,beta,K,B):
    """Enumerate all (1,v1,v2,v3) of prescribed dimension in the Gram bounds."""
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

def low_matrices(row_sets,B,roots):
    """Canonical low parts under permutations of equal-formal-codegree rows."""
    unit=(1,0,0,0);target=tuple(int(B[0,i])-unit[i] for i in range(4))
    last=set(row_sets[2]);out=[]
    for a,b in itertools.product(row_sets[0],row_sets[1]):
        c=tuple(target[i]-a[i]-b[i] for i in range(4))
        if c not in last:continue
        v=(a,b,c)
        if any(roots[i]==roots[j] and v[i]>v[j] for i in range(3) for j in range(i+1,3)):continue
        out.append((unit,)+v)
    return out

def low_data(rows,B,ds,K):
    """For center-indexed rows, compute Q=B-L.T*L and W=L.T*L*d."""
    L=s.Matrix(rows);G=L.T*L;Q=B-G
    W=[sum((K(int(G[i,j]))*ds[j] for j in range(4)),K.zero) for i in range(4)]
    return Q,W

def row_gap(i,W,ds,D,K,du):
    return K(3)*W[i]-D*ds[i] if du[i]!=i else K(9)*W[i]-D*(K(3)*ds[i]+K(2))

def third_indicator_gap(i,W,ds,D,K,du,R):
    """Gap in 36 W_i <= D(10 d_i + 8 + 2 N_ii^{i*})."""
    return K(36)*W[i]-D*(K(10)*ds[i]+K(8)+K(2*R[i][i][du[i]]))

def algebraic_floor(value,K,emb):
    """Floor a real algebraic element using exact sign comparisons only."""
    lo,hi=-1,1
    while emb.sign(value-K(lo))<0:lo*=2
    while emb.sign(value-K(hi))>=0:hi*=2
    while hi-lo>1:
        mid=(lo+hi)//2
        if emb.sign(value-K(mid))>=0:lo=mid
        else:hi=mid
    return lo

def fourth_indicator_bound(i,ds,K,du,R):
    """The real algebraic expression whose integer floor is required."""
    return (K(10)*ds[i]+K(71*int(du[i]==i))+K(30*R[i][i][du[i]]))/K(9)

def fourth_indicator_gap(i,W,ds,D,K,m):
    """Gap in 32 W_i <= D(7 d_i + m), for the certified floor m."""
    return K(32)*W[i]-D*(K(7)*ds[i]+K(m))

def low_failure(cols,B,ds,D,K,emb,du,R):
    Q,W=low_data(cols,B,ds,K)
    for i in range(1,4):
        gap=row_gap(i,W,ds,D,K,du)
        if emb.sign(gap)>0:
            return {'kind':'polynomial_row','object':i,'nonselfdual':du[i]!=i,'gap':ec(gap)}
    for g in range(1,4):
        if du[g]!=g or ds[g]!=K.one or Q[g,g]!=2:continue
        if emb.sign(W[g])<=0 or D/K(2)-W[g]!=K.one:continue
        for i in range(1,4):
            if i==g:continue
            gap=K(2)*W[i]+D*K(int(Q[g,i]))-D*(ds[i]+K.one)
            if emb.sign(gap)>0:
                return {'kind':'involution_moment','involution':g,'object':i,'gap':ec(gap)}
    for i in range(1,4):
        gap=third_indicator_gap(i,W,ds,D,K,du,R)
        if emb.sign(gap)>0:
            return {'kind':'third_indicator_row','object':i,'gap':ec(gap)}
    # Preserve the discovery preference for every previously available witness.
    for i in range(1,4):
        m=algebraic_floor(fourth_indicator_bound(i,ds,K,du,R),K,emb)
        gap=fourth_indicator_gap(i,W,ds,D,K,m)
        if emb.sign(gap)>0:
            return {'kind':'fourth_indicator_row','object':i,'floor':m,'gap':ec(gap)}
    return None

def check_low_witness(cols,B,ds,D,K,emb,du,c,R):
    """Validate the proposed witness, without rediscovering the first failure."""
    require(isinstance(c,dict),'low obstruction not verified: null or malformed witness')
    kind=c.get('kind');i=c.get('object')
    require(type(i) is int and 1<=i<4,'invalid row object')
    Q,W=low_data(cols,B,ds,K)
    if kind=='polynomial_row':
        require(c['nonselfdual']==(du[i]!=i),'incorrect duality claim')
        gap=row_gap(i,W,ds,D,K,du)
    elif kind=='third_indicator_row':
        gap=third_indicator_gap(i,W,ds,D,K,du,R)
    elif kind=='fourth_indicator_row':
        m=c.get('floor')
        require(type(m) is int,'invalid fourth-indicator floor')
        bound=fourth_indicator_bound(i,ds,K,du,R)
        require(emb.sign(bound-K(m))>=0 and emb.sign(K(m+1)-bound)>0,
                'incorrect fourth-indicator floor')
        gap=fourth_indicator_gap(i,W,ds,D,K,m)
    elif kind=='involution_moment':
        g=c.get('involution')
        require(type(g) is int and 1<=g<4 and g!=i,'invalid involution object')
        require(du[g]==g and ds[g]==K.one and Q[g,g]==2
                and emb.sign(W[g])>0 and D/K(2)-W[g]==K.one,
                'involution hypotheses not met')
        gap=K(2)*W[i]+D*K(int(Q[g,i]))-D*(ds[i]+K.one)
    else:raise VerificationError('unknown low obstruction')
    require(c.get('gap')==ec(gap) and emb.sign(gap)>0,'low obstruction not verified: false strict gap')

def pseudo_certificate(R,a=None):
    if a is None:a=Characters(R)
    f,K,ds,D,pD,emb=a.fp()
    roots=a.codegree_roots(f)
    require(roots is not None,'unresolved codegree splitting; no induction exclusion')
    rest=list(roots);require(D in rest,'FP codegree absent');rest.remove(D)
    cs=[induction_rows(ds,D/r,K,a.C) for r in rest]
    lows=low_matrices(cs,a.C,rest) if all(cs) else []
    failures=[]
    for cols in lows:
        why=low_failure(cols,a.C,ds,D,K,emb,a.du,R)
        if why is None:return None
        failures.append({'columns':[list(c) for c in cols],'obstruction':why})
    return {'kind':'induction','generator':a.k,'fp_factor':pc(f),
            'roots':[ec(r) for r in roots],
            'column_counts':[len(v) for v in cs],
            'low_count':len(lows),'failures':failures}

def check_pseudo(R,c,a=None):
    require(isinstance(c,dict) and c.get('kind')=='induction','missing or unknown pseudo-unitary proof')
    if a is None:a=Characters(R,c['generator'])
    require(a.k==c['generator'],'inconsistent separating element')
    f,K,ds,D,pD,emb=a.fp()
    require(pc(f)==c['fp_factor'],'wrong FP factor')
    require(all(len(r)<=f.degree() for r in c['roots']),'unreduced root vector')
    roots=[K([s.Rational(v) for v in r]) for r in c['roots']]
    check_roots(a.cp,K,roots)
    rest=list(roots);require(D in rest,'missing FP codegree');rest.remove(D)
    cs=[induction_rows(ds,D/r,K,a.C) for r in rest]
    lows=low_matrices(cs,a.C,rest) if all(cs) else []
    require([len(v) for v in cs]==c['column_counts'] and len(lows)==c['low_count'],'incomplete low enumeration')
    require(len(c['failures'])==len(lows),'missing low-matrix branches')
    for cols,branch in zip(lows,c['failures']):
        require([list(v) for v in cols]==branch['columns'],'wrong low rows')
        check_low_witness(cols,a.C,ds,D,K,emb,a.du,branch['obstruction'],R)
