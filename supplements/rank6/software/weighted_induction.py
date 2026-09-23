"""Multiplicity-weighted central induction for noncommutative rank six.

All spectral decisions use exact rational/algebraic arithmetic.  The one-
dimensional summand is computed independently as the common commutator kernel.
"""
import itertools,math
from fractions import Fraction as Q
from types import SimpleNamespace
import sympy as s
from exact import *
from rings import matrices,dual,casimir
from induction import low_failure
from higher_traces import build_system,indicator_choices,farkas,check_farkas

def spectral(R):
    n=len(R);require(n==6,'rank six required');N=matrices(R);du=dual(R)
    require(any(N[i]*N[j]!=N[j]*N[i] for i in range(n) for j in range(i)), 'noncommutative branch required')
    W=s.Matrix.vstack(*(N[i]*N[j]-N[j]*N[i] for i in range(n) for j in range(i))).nullspace()
    require(len(W)==2,'one-dimensional character subspace has wrong dimension')
    W=s.Matrix.hstack(*W);piv=list(W.T.rref()[1]);J=W.extract(piv,range(2)).inv()
    A=[J*(a*W).extract(piv,range(2)) for a in N]
    require(all(a*W==W*b for a,b in zip(N,A)),'noninvariant character subspace')
    for k in range(1,20):
        H=A[0]+sum((k**(i-1)*A[i] for i in range(1,n)),s.zeros(2));p=H.charpoly(t).as_poly()
        if s.gcd(p,p.diff()).degree()==0:break
    require(s.gcd(p,p.diff()).degree()==0,'nonseparating character element')
    V=s.Matrix.hstack(s.Matrix(list(s.eye(2))),s.Matrix(list(H)))
    coeff=[list(V.gauss_jordan_solve(s.Matrix(list(a)))[0]) for a in A]
    f,emb=max(((f,e) for f,m in p.factor_list()[1] for e in embeddings(f)),key=lambda z:z[1].hi)
    K=field(f);ds=[K(s.Poly.from_list(list(reversed(c)),t,domain=s.QQ).rem(f).all_coeffs()) for c in coeff]
    require(all(emb.sign(x)>0 for x in ds),'not a positive character')
    require(all(ds[i]*ds[j]==sum((K(R[i][j][k])*ds[k] for k in range(n)),K.zero) for i in range(n) for j in range(n)), 'dimension character failed')
    D=sum((ds[i]*ds[du[i]] for i in range(n)),K.zero)
    C=casimir(R);pcas=C.charpoly(t).as_poly()
    lin=[(g,m) for g,m in pcas.factor_list()[1] if g.degree()==1 and m>=4]
    require(len(lin)==1,'unique two-dimensional component not located')
    c=-s.Rational(lin[0][0].TC(),lin[0][0].LC());fe=c/2
    require(fe.q==1 and fe>0,'nonintegral matrix-block formal codegree')
    # The one-dimensional character formal codegrees, counted by characters.
    DC=sum((A[i]*A[du[i]] for i in range(n)),s.zeros(2));q=DC.charpoly(t).as_poly()
    roots=discover_roots(q,K);require(roots is not None,'character codegrees do not split in FP field')
    check_roots(q,K,roots);require(D in roots,'FP codegree absent');roots.remove(D)
    require(len(roots)==1,'wrong number of non-FP linear characters')
    require(pcas==s.Poly((t-c)**4,t)*q,'Casimir Wedderburn identity failed')
    B=s.zeros(n)
    for j,i in itertools.product(range(n),repeat=2):
        B[j,i]=sum(R[a][j][k]*R[k][du[a]][i] for a,k in itertools.product(range(n),repeat=2))
    require(B==B.T,'induction Gram not symmetric')
    return dict(n=n,N=N,du=du,W=W,A=A,generator=k,factor=f,K=K,ds=ds,D=D,embedding=emb,Casimir=C,Gram=B,codegrees=[D,roots[0],K(fe)],multiplicities=[1,1,2])

def restriction(ds,beta,r,K,B):
    n=len(ds);degree=K.mod.degree();tail=n-1
    A=s.Matrix.hstack(*(vector(d,degree) for d in ds[1:]));b=vector(beta-K(r),degree)
    rr,piv=A.row_join(b).rref()
    if tail in piv:return []
    free=[j for j in range(tail) if j not in piv]
    bounds=[min(int(B[0,i])//r,math.isqrt(int(B[i,i]))) for i in range(1,n)]
    out=[]
    for chosen in itertools.product(*(range(bounds[j]+1) for j in free)):
        v=[s.S.Zero]*tail
        for j,a in zip(free,chosen):v[j]=s.Integer(a)
        for row,j in enumerate(piv):v[j]=rr[row,tail]-sum(rr[row,k]*v[k] for k in free)
        if all(a.q==1 and 0<=a<=bounds[j] for j,a in enumerate(v)):out.append((r,)+tuple(map(int,v)))
    return sorted(out)

def data(R):
    a=spectral(R);n=a['n'];K=a['K'];f=a['factor'];ds=a['ds'];D=a['D'];B=a['Gram']
    require(f.degree() in (1,2),'rational/quadratic FP field required')
    cs=[restriction(ds,D/fc,r,K,B) for fc,r in zip(a['codegrees'][1:],a['multiplicities'][1:])]
    unit=(1,)+(0,)*(n-1);lows=[]
    for vs in itertools.product(*cs):
        if all(unit[i]+sum(r*v[i] for r,v in zip(a['multiplicities'][1:],vs))==int(B[0,i]) for i in range(n)):
            lows.append((unit,)+vs)
    if f.degree()==1:
        q=1;F=1
        coords=lambda x:(Q(str(ec(x)[0])),Q(0))
    else:
        co=list(map(int,f.all_coeffs()));disc=co[1]**2-4*co[2];q=math.prod(int(p) for p,e in s.factorint(disc).items() if e%2);h=math.isqrt(disc//q);F=q if q%4==1 else 4*q
        def coords(x):
            z=[Q(str(c)) for c in ec(x)];z=[Q(0)]*(2-len(z))+z
            return z[1]-Q(co[1],2)*z[0],Q(h,2)*z[0]
    d=list(map(coords,ds));dd=coords(D);norm=dd[0]**2-q*dd[1]**2
    require(norm.denominator==1,'nonintegral dimension norm')
    primes=sorted(map(int,s.factorint(abs(norm.numerator))))
    return dict(a, ch=SimpleNamespace(n=n,C=B,du=a['du']),q=q,conductor=F,dimensions=d,global_dimension=dd,primes=primes,columns=cs,lows=lows)

def gate(a):
    # All input hypotheses are checked from exact dimensions, never from labels.
    if len(set(tuple(ec(d)) for d in a['ds']))<=2:return 'two_fp_dimensions'
    if len(ec(a['D']))==1 and s.Rational(ec(a['D'])[0]).q==1:return 'weakly_integral'
    return None

def certificate(R,height=6):
    a=data(R);g=gate(a)
    if not g:return None
    branches=[]
    for cols in a['lows']:
        why=low_failure(cols,a['Gram'],a['ds'],a['D'],a['K'],a['embedding'],a['du'])
        b={'columns':[list(c) for c in cols]}
        if why:b['ordinary']=why
        else:
            L=s.Matrix.hstack(*map(s.Matrix,cols));cases=[]
            for ep in indicator_choices(R):
                A,v,meta=build_system(R,a,L,ep,height);y=farkas(A,v)
                if y is None:return None
                cases.append({'indicators':list(ep),'y':y,'column_count':meta['column_count'],'trace_types':meta['trace_types'],'order_bound':meta['order_bound'],'bTy':sum(x*z for x,z in zip(v,y))})
            b['higher']=cases
        branches.append(b)
    return {'kind':'weighted_induction','gate':g,'height':height,'q':a['q'],'conductor':a['conductor'],'primes':a['primes'],'column_counts':list(map(len,a['columns'])),'low_count':len(a['lows']),'branches':branches}

def verify(R,c):
    a=data(R);require(c['kind']=='weighted_induction' and gate(a)==c['gate'] and gate(a) is not None,'invalid general-to-positive gate')
    require(all(c[k]==a[k] for k in ['q','conductor','primes']),'weighted field metadata mismatch')
    require(c['column_counts']==list(map(len,a['columns'])) and c['low_count']==len(a['lows']) and len(c['branches'])==len(a['lows']),'weighted low enumeration incomplete')
    for cols,b in zip(a['lows'],c['branches']):
        require(b['columns']==[list(c) for c in cols],'weighted low branch changed')
        why=low_failure(cols,a['Gram'],a['ds'],a['D'],a['K'],a['embedding'],a['du'])
        if why:require(b.get('ordinary')==why,'ordinary obstruction invalid');continue
        eps=indicator_choices(R);cases=b['higher'];require([x['indicators'] for x in cases]==list(map(list,eps)),'indicator branches incomplete')
        L=s.Matrix.hstack(*map(s.Matrix,cols))
        for ep,case in zip(eps,cases):
            A,v,meta=build_system(R,a,L,ep,c['height']);check_farkas(A,v,case['y'])
            require(all(case[k]==meta[k] for k in ['column_count','trace_types','order_bound']),'weighted high system changed')
            require(case['bTy']==sum(x*z for x,z in zip(v,case['y'])),'separation value changed')
