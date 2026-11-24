"""Finite relative-trace obstructions for pseudo-unitary rational and quadratic fusion rings.

All matrices and certificates are rational/integral. SciPy is used only to
propose a separating functional; the verifier checks it with Python integers.
"""
import itertools, math, json
from fractions import Fraction as Q
import numpy as np
import sympy as s
from induction import *

def quadratic_data(R,gram_prune=False):
    ch=Characters(R);f,K,ds,D,pD,emb=ch.fp()
    if f.degree()==1:
        roots=discover_roots(codegree_poly(R),K)
        if roots is None:return None
        check_roots(codegree_poly(R),K,roots)
        rest=list(roots);rest.remove(D)
        cs=[restriction_columns(ds,D/r,K,ch.C) for r in rest]
        lows=low_matrices(cs,ch.C,gram_prune=gram_prune) if all(cs) else []
        d=[(Q(str(ec(x)[0])),Q(0)) for x in ds]
        dd=(Q(str(ec(D)[0])),Q(0))
        require(all(x[0].denominator==1 for x in d),'degree-one FP dimensions must be integral')
        primes=sorted(map(int,s.factorint(dd[0].numerator)))
        return {'ch':ch,'factor':f,'K':K,'ds':ds,'D':D,'embedding':emb,
                'q':1,'conductor':1,'dimensions':d,'global_dimension':dd,
                'primes':primes,'columns':cs,'lows':lows}
    if f.degree()!=2:return None
    co=list(map(int,f.all_coeffs()));disc=co[1]**2-4*co[2]
    if disc<=0:return None
    fac=s.factorint(disc);q=math.prod(int(p) for p,e in fac.items() if e%2)
    h=math.isqrt(disc//q);F=q if q%4==1 else 4*q
    def coords(x):
        z=[Q(str(c)) for c in ec(x)];z=[Q(0)]*(2-len(z))+z
        return (z[1]-Q(co[1],2)*z[0],Q(h,2)*z[0])
    d=list(map(coords,ds));dd=coords(D)
    if not dd[1]:return None
    roots=discover_roots(codegree_poly(R),K)
    if roots is None:return None
    check_roots(codegree_poly(R),K,roots)
    rest=list(roots);rest.remove(D);cs=[restriction_columns(ds,D/r,K,ch.C) for r in rest]
    lows=low_matrices(cs,ch.C,gram_prune=gram_prune) if all(cs) else []
    norm=dd[0]**2-q*dd[1]**2
    require(norm.denominator==1,"nonintegral global-dimension norm")
    primes=sorted(map(int,s.factorint(abs(norm.numerator))))
    return {'ch':ch,'factor':f,'K':K,'ds':ds,'D':D,'embedding':emb,'q':q,'conductor':F,
            'dimensions':d,'global_dimension':dd,'primes':primes,'columns':cs,'lows':lows}

def trace_types(q,primes,height):
    """All joint normalized traces to Q(sqrt(q)), including unbounded orders.

    Orders outside the displayed divisor box give the all-zero vector.
    A quadratic Gauss sum supplies the only nonrational component.
    """
    if q==1:
        bound=1
        for p in primes:
            e=0
            while p**(e+1)<=height:e+=1
            bound*=p**(1+e)
        out={tuple((Q(0),Q(0)) for _ in range(height))}
        for order in s.divisors(bound):
            out.add(tuple((Q(int(s.mobius(order//math.gcd(order,k))),int(s.totient(order//math.gcd(order,k)))),Q(0)) for k in range(1,height+1)))
        return sorted(out),bound
    conductor=q if q%4==1 else 4*q
    if any(p not in primes for p in s.factorint(conductor)):
        raise ValueError('dimension-field conductor outside exponent prime support')
    bound=1
    for p in primes:
        e=0
        while p**(e+1)<=height:e+=1
        c=0;ff=conductor
        while ff%p==0:ff//=p;c+=1
        bound*=p**(max(c,1)+e)
    out={tuple((Q(0),Q(0)) for k in range(height))}
    root_factor=math.isqrt(conductor//q)
    for order in s.divisors(bound):
        order=int(order)
        for sign in (-1,1):
            values=[]
            for k in range(1,height+1):
                g=math.gcd(order,k);n=order//g;phi=int(s.totient(n))
                a=Q(int(s.mobius(n)),phi);b=Q(0)
                if n%conductor==0:
                    z=n//conductor
                    if math.gcd(z,conductor)==1:
                        b=Q(sign*int(s.mobius(z))*int(s.kronecker_symbol(conductor,z))*
                            int(s.kronecker_symbol(conductor,k//g))*root_factor,phi)
                values.append((a,b))
            out.add(tuple(values))
    return sorted(out),bound

def mul(x,y,q):return (x[0]*y[0]+q*x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def integer_pair(x,q):return (2*x[0]).denominator==1 and (x[0]**2-q*x[1]**2).denominator==1

def high_columns(data,L):
    n=data['ch'].n;q=data['q'];d=data['dimensions'];D=data['global_dimension']
    B=data['ch'].C;Qm=(B-L*L.T).extract(range(1,n),range(1,n));rank=Qm.rank()
    if not rank:return Qm,[]
    ix=next(ii for ii in itertools.combinations(range(n-1),rank) if Qm.extract(ii,ii).det()!=0)
    sub=Qm.extract(ix,ix);adj=[[int(x) for x in row] for row in sub.adjugate().tolist()];det=int(sub.det());null=Qm.nullspace();cols=[]
    null=[[int(x*math.lcm(*(int(y.q) for y in z))) for x in z] for z in null]
    entries=[[int(x) for x in row] for row in Qm.tolist()]
    denominator=math.lcm(*(x.denominator for pair in d for x in pair))
    dimensions=[[int(x*denominator) for x in pair] for pair in d]
    if n==5 and rank==4 and not __import__('os').environ.get('RANK5_REFERENCE_GRAM'):
        from gram_vectors import native
        candidates=native(Qm)
    else:
        candidates=itertools.product(*(range(math.isqrt(int(Qm[i,i]))+1) for i in range(n-1)))
    for v in candidates:
        if not any(v):continue
        if any(v[i]*v[j]>entries[i][j] for i in range(n-1) for j in range(i,n-1)):continue
        if any(sum(v[i]*z[i] for i in range(n-1)) for z in null):continue
        vv=[v[i] for i in ix]
        if sum(vv[i]*adj[i][j]*vv[j] for i in range(rank) for j in range(rank))>det:continue
        z=tuple(Q(sum(v[i]*dimensions[i+1][j] for i in range(n-1)),denominator) for j in range(2));norm=z[0]**2-q*z[1]**2
        if not norm:continue
        quotient=( (D[0]*z[0]-q*D[1]*z[1])/norm, (D[1]*z[0]-D[0]*z[1])/norm )
        if not integer_pair(quotient,q):continue
        if z[1] and ((2*z[0])**2/norm).denominator!=1:continue
        cols.append((v,z))
    return Qm,cols

def indicator_choices(R):
    du=dual(R);out=[]
    for i in range(1,len(R)):
        if du[i]!=i:out.append([0])
        elif any(R[j][du[j]][i]%2 for j in range(len(R))):out.append([1])
        else:out.append([-1,1])
    return list(itertools.product(*out))

def build_system(R,data,L,indicators,height=6):
    n=len(R);tail=n-1;q=data['q'];d=data['dimensions'];D=data['global_dimension'];F=data['conductor']
    types,order_bound=trace_types(q,data['primes'],height)
    Qm,cols=high_columns(data,L);LL=L*L.T
    low=[tuple(sum((Q(int(LL[i,j]))*d[j][k] for j in range(n)),Q(0)) for k in range(2)) for i in range(1,n)]
    ij=list(itertools.combinations_with_replacement(range(tail),2));rational_orders=[k for k in range(3,height+1) if F==1 or k%F!=0]
    b=[Q(int(Qm[i,j])) for i,j in ij]
    b += [-x for z in low for x in z]
    b += [indicators[i]*D[k]-low[i][k] for i in range(tail) for k in range(2)]
    b += [-(D[1]*low[i][0]-D[0]*low[i][1]) for k in rational_orders for i in range(tail)]
    # Exact rotation-space dimensions H[i,j]=[X_i^j:1]. Only orders whose
    # indicator average is rational supply these coefficient-wise bounds.
    H={}
    for i in range(1,n):
        power=[int(a==0) for a in range(n)]
        for j in range(1,height+1):
            power=[sum(power[a]*R[a][i][b] for a in range(n)) for b in range(n)]
            H[i-1,j]=power[0]
    b += [bound*D[0]-sg*low[i][0]
          for j in rational_orders for i in range(tail)
          for sg,bound in [(1,Q(H[i,j])),(-1,Q(H[i,j],min(map(int,s.factorint(j)))-1))]]
    vectors=[];labels=[]
    for v,z in cols:
        for ti,ts in enumerate(types):
            moments=[[v[i]*x for i in range(tail) for x in mul(z,tt,q)] for tt in ts]
            col=[Q(v[i]*v[j]) for i,j in ij]+moments[0]+moments[1]
            col += [D[1]*moments[k-1][2*i]-D[0]*moments[k-1][2*i+1] for k in rational_orders for i in range(tail)]
            col += [sg*moments[j-1][2*i] for j in rational_orders for i in range(tail) for sg in (1,-1)]
            vectors.append(col);labels.append([list(v),ti])
    slack_count=2*tail*len(rational_orders)
    for j in range(slack_count):
        col=[Q(0)]*len(b);col[len(b)-slack_count+j]=Q(1);vectors.append(col)
    A=[[Q(v[i]) for v in vectors] for i in range(len(b))]
    # Primitive integer rows, exact scaling including the right side.
    for i in range(len(b)):
        den=math.lcm(b[i].denominator,*(x.denominator for x in A[i]));row=[int(x*den) for x in A[i]];bb=int(b[i]*den)
        g=math.gcd(bb,*row);g=g or 1;A[i]=[x//g for x in row];b[i]=bb//g
    return A,list(map(int,b)),{'column_count':len(cols),'trace_types':len(types),'order_bound':order_bound,'high_variables':len(labels),'rows':len(b),'labels':labels}

def farkas(A,b):
    """Find, then verify, an exact rational dual ray; never accept a float ray."""
    from scipy.optimize import linprog
    AA=np.array(A,dtype=float);bb=np.array(b,dtype=float);m=len(b)
    scale=np.maximum(1,np.maximum(np.max(abs(AA),axis=1),abs(bb)))
    scaled=AA/scale[:,None];rhs=bb/scale
    sol=linprog(np.ones(2*m),A_ub=np.r_[np.c_[-scaled.T,scaled.T],np.r_[rhs,-rhs][None,:]],
                b_ub=np.r_[np.zeros(AA.shape[1]),-1.],bounds=(0,None),method='highs')
    if not sol.success:return None
    y=(sol.x[:m]-sol.x[m:])/scale
    y/=max(abs(y))
    for threshold in (1e-8,1e-7,1e-6):
        support=np.flatnonzero(abs(y)>1e-9).tolist();active=np.flatnonzero(abs(AA.T@y)<threshold).tolist()
        C=s.Matrix([[A[i][j] for i in support] for j in active]+[[b[i] for i in support]])
        rhs=s.zeros(C.rows,1);rhs[-1]=-1;rr,piv=C.row_join(rhs).rref()
        if len(piv)!=len(support) or (piv and piv[-1]>=len(support)):continue
        zz=[rr[i,-1] for i in range(len(support))];den=math.lcm(*(int(z.q) for z in zz));out=[0]*m
        for i,z in zip(support,zz):out[i]=int(z*den)
        g=math.gcd(*out);out=[z//g for z in out]
        if check_farkas(A,b,out,raise_error=False):return out
    return None

def check_farkas(A,b,y,raise_error=True):
    okay=len(y)==len(b) and all(type(t) is int for t in y)
    okay=okay and all(sum(A[i][j]*y[i] for i in range(len(b)))>=0 for j in range(len(A[0])))
    okay=okay and sum(t*v for t,v in zip(b,y))<0
    if raise_error:require(okay,'higher-indicator Farkas certificate fails')
    return okay

def certificate(R,height=6,gram_prune=False):
    data=quadratic_data(R,gram_prune=gram_prune)
    if data is None:return None
    branches=[]
    for cols in data['lows']:
        why=low_failure(cols,data['ch'].C,data['ds'],data['D'],data['K'],data['embedding'],data['ch'].du)
        branch={'columns':[list(c) for c in cols]}
        if why:branch['ordinary']=why
        else:
            L=s.Matrix.hstack(*map(s.Matrix,cols));cases=[]
            for ep in indicator_choices(R):
                A,b,meta=build_system(R,data,L,ep,height);y=farkas(A,b)
                if y is None:return None
                cases.append({'indicators':list(ep),'y':y,'column_count':meta['column_count'],
                              'trace_types':meta['trace_types'],'order_bound':meta['order_bound'],
                              'bTy':sum(x*z for x,z in zip(b,y))})
            branch['higher']=cases
        branches.append(branch)
    return {'kind':'finite_indicator_traces','height':height,'gram_pruned':gram_prune,'q':data['q'],'conductor':data['conductor'],
            'primes':data['primes'],'column_counts':list(map(len,data['columns'])),'branches':branches}

def verify(R,cert):
    data=quadratic_data(R,gram_prune=cert.get('gram_pruned',False));require(data is not None,'not an eligible rational or quadratic ring')
    require(cert['kind']=='finite_indicator_traces','wrong certificate kind')
    require(cert['q']==data['q'] and cert['conductor']==data['conductor'] and cert['primes']==data['primes'],'wrong field or prime support')
    require(cert['column_counts']==list(map(len,data['columns'])),'incomplete low columns')
    require(len(cert['branches'])==len(data['lows']),'incomplete low matrices')
    for cols,branch in zip(data['lows'],cert['branches']):
        require(branch['columns']==[list(c) for c in cols],'wrong low matrix')
        why=low_failure(cols,data['ch'].C,data['ds'],data['D'],data['K'],data['embedding'],data['ch'].du)
        if why:require(branch.get('ordinary')==why,'incorrect ordinary low obstruction');continue
        L=s.Matrix.hstack(*map(s.Matrix,cols));cases=branch['higher'];eps=indicator_choices(R)
        require([c['indicators'] for c in cases]==list(map(list,eps)),'incomplete second indicators')
        for ep,case in zip(eps,cases):
            A,b,meta=build_system(R,data,L,ep,cert['height']);check_farkas(A,b,case['y'])
            require(all(case[k]==meta[k] for k in ['column_count','trace_types','order_bound']),'wrong finite trace system')
            require(case['bTy']==sum(x*z for x,z in zip(b,case['y'])),'wrong separating value')
