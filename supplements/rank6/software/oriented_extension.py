"""General categorification sieve using all oriented signed quotients."""
from extension import *
from oriented_signed import enumerate_all,from_values,validate_general
import integer_gram
import balanced_traces

def linear_data(T):
    N=matrices(T);n=len(T);du=dual(T);W=s.Matrix.vstack(*(N[i]*N[j]-N[j]*N[i] for i in range(n) for j in range(i))).nullspace()
    require(n==6 and len(W)==2,'unexpected noncommutative signed algebra')
    W=s.Matrix.hstack(*W);piv=list(W.T.rref()[1]);J=W.extract(piv,range(2)).inv();A=[J*(a*W).extract(piv,range(2)) for a in N]
    require(all(a*W==W*b for a,b in zip(N,A)),'character space not invariant')
    for k in range(1,32):
        H=A[0]+sum((k**(i-1)*A[i] for i in range(1,n)),s.zeros(2));p=H.charpoly(t).as_poly()
        if s.gcd(p,p.diff()).degree()==0:break
    require(s.gcd(p,p.diff()).degree()==0,'signed character separation failed')
    V=s.Matrix.hstack(s.Matrix(list(s.eye(2))),s.Matrix(list(H)));co=[list(V.gauss_jordan_solve(s.Matrix(list(a)))[0]) for a in A]
    C=casimir(T);cp=C.charpoly(t).as_poly();lin=[(g,m) for g,m in cp.factor_list()[1] if g.degree()==1 and m>=4];require(len(lin)==1,'matrix summand not found')
    ev=-s.Rational(lin[0][0].TC(),lin[0][0].LC());fe=ev/2;require(fe.q==1 and fe>0,'invalid two-dimensional codegree')
    q=sum((A[i]*A[du[i]] for i in range(n)),s.zeros(2)).charpoly(t).as_poly();require(cp==s.Poly((t-ev)**4,t)*q,'weighted spectral identity')
    cf=list(q.factor_list()[1])+[(s.Poly(t-fe,t,domain=s.QQ),1)]
    return p,co,q,fe,cf

def nc_certificate(R,T):
    p,co,q,fe,cf=linear_data(T);required=list(codegree_factors(R))+cf;out=[];du=dual(T)
    for f,m in p.factor_list()[1]:
        K=field(f);ds=[K(s.Poly.from_list(list(reversed(c)),t,domain=s.QQ).rem(f).all_coeffs()) for c in co];delta=sum((ds[i]*ds[du[i]] for i in range(6)),K.zero)
        pD=multiplication_matrix(delta,K,f).charpoly(t).as_poly().sqf_part();why=None
        zero=next((i for i,d in enumerate(ds) if not d),None);uneq=next((i for i,d in enumerate(ds) if d!=ds[du[i]]),None)
        if zero is not None:why={'kind':'zero','object':zero}
        elif uneq is not None:why={'kind':'duality','object':uneq}
        else:
            why=norm_failure(pD,required) or field_failure(f,required)
        if not why:return None
        out.append({'factor':pc(f),'obstruction':why})
    return {'kind':'noncommutative_signed','characters':out}

def pseudo_check(R,c):
    if c['kind']=='modular_character_induction':
        import modular_character_induction
        modular_character_induction.verify(R,c);return
    if c['kind']=='character_induction':
        import character_induction
        character_induction.verify(R,c);return
    if c['kind']=='tensor_rotation_traces':
        import tensor_rotation
        tensor_rotation.verify(R,c);return
    if c['kind']=='balanced_indicator_traces':balanced_traces.verify(R,c)
    elif c['kind']=='integral_gram_traces':integer_gram.verify(R,c)
    else:check_extended_pseudo(R,c)

def pseudo_discover(R,height,integral):
    c=extended_pseudo(R,height)
    if c:return c
    c=balanced_traces.certificate(R,height)
    if c or not integral:return c
    return integer_gram.certificate(R,height,seconds=15,limit_frames=6000)

def certificate(R,height=6,timeout=30,integral=False):
    a=Characters(R);f,K,ds,D,pD,e=a.fp();gate='weak_integrality' if pD.degree()==1 else 'two_FP_values' if len(set(ds))==2 else None
    if gate:
        c=pseudo_discover(R,height,integral)
        return None if c is None else {'kind':'oriented_pseudo_gate','gate':gate,'pseudo':c}
    sphere=sphere_certificate(R,lambda R:pseudo_discover(R,height,integral))
    if sphere is None:return None
    vals,p,stats=enumerate_all(R,timeout);branches=[]
    for v in vals:
        T=from_values(R,p,v);b={'values':list(v)};why=signed_adjoint_parity(R,T);g=gauge_original(T,R)
        if why:b['obstruction']=why
        elif g:b['obstruction']={'kind':'gauge_original','signs':g}
        elif any(T[i][j]!=T[j][i] for i in range(6) for j in range(6)):
            c=nc_certificate(R,T)
            if c is None:return None
            b['noncommutative']=c
        else:
            aa=Characters(T);cc=[{'factor':pc(ff),'obstruction':signed_component_certificate(R,T,aa,ff,sphere)} for ff,_ in aa.components]
            if any(c['obstruction'] is None for c in cc):return None
            b['characters']=cc;b['generator']=aa.k
        branches.append(b)
    return {'kind':'oriented_signed','sphere':sphere,'branches':branches}

def verify(R,c):
    if c['kind']=='oriented_pseudo_gate':
        a=Characters(R);f,K,ds,D,pD,e=a.fp();require((c['gate']=='weak_integrality' and pD.degree()==1) or (c['gate']=='two_FP_values' and len(set(ds))==2),'wrong oriented pseudo gate');pseudo_check(R,c['pseudo']);return
    require(c['kind']=='oriented_signed','wrong oriented certificate kind');check_sphere(R,c['sphere'],pseudo_check)
    vals,p,stats=enumerate_all(R,120);require([list(v) for v in vals]==[b['values'] for b in c['branches']],'incomplete oriented signed enumeration')
    for v,b in zip(vals,c['branches']):
        T=from_values(R,p,v);validate_general(T)
        if 'obstruction' in b:
            w=b['obstruction']
            if w['kind']=='gauge_original':require(gauge_original(T,R)==w['signs'],'wrong gauge')
            else:require(signed_adjoint_parity(R,T)==w,'wrong parity')
        elif 'noncommutative' in b:require(nc_certificate(R,T)==b['noncommutative'],'noncommutative character obstruction failed')
        else:
            aa=Characters(T,b['generator']);require(len(aa.components)==len(b['characters']),'missing signed characters')
            for (ff,m),cc in zip(aa.components,b['characters']):require(pc(ff)==cc['factor'],'wrong signed factor');check_signed_component(R,T,aa,ff,cc['obstruction'])
