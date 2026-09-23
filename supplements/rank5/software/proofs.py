"""Proof trees for the finite classification.

Discovery proposes witnesses. Checking recomputes every hypothesis and
covers every character, signed table, low matrix and indicator assignment.
"""
import itertools,math
from collections import Counter
from exact import *
from rings import *
from induction import *
from signed import *

def multiplication_matrix(a,K,f):
    u=K(s.Poly(t,t).rem(f).all_coeffs())
    return s.Matrix.hstack(*(vector(a*u**i,f.degree()) for i in range(f.degree())))

def subring_certificate(R):
    a=Characters(R);f,K,ds,D,pD,emb=a.fp();du=dual(R)
    for size in range(2,len(R)):
        for subset in itertools.combinations(range(1,len(R)),size-1):
            J=(0,)+subset
            if any(du[i] not in J for i in J):continue
            if any(R[i][j][k] for i in J for j in J for k in range(len(R)) if k not in J):continue
            S=sum((ds[i]*ds[du[i]] for i in J),K.zero)
            q=multiplication_matrix(D/S,K,f).charpoly(t).as_poly()
            if any(v.q!=1 for v in q.all_coeffs()):
                return {'kind':'subring','subset':list(J),'quotient_polynomial':pc(q)}
    return None

def check_subring(R,c):
    J=c['subset'];require(0 in J and 2<=len(J)<len(R) and len(set(J))==len(J),'invalid subring')
    a=Characters(R);f,K,ds,D,pD,emb=a.fp();du=a.du
    require(all(du[i] in J for i in J),'subring not dual closed')
    require(not any(R[i][j][k] for i in J for j in J for k in range(len(R)) if k not in J),'subring not closed')
    S=sum((ds[i]*ds[du[i]] for i in J),K.zero);q=multiplication_matrix(D/S,K,f).charpoly(t).as_poly()
    require(pc(q)==c['quotient_polynomial'] and any(v.q!=1 for v in q.all_coeffs()),'quotient integrality not excluded')

def sphere_certificate(R,pseudo_method=None):
    if pseudo_method is None:pseudo_method=pseudo_certificate
    a=Characters(R);fp=a.fp()[0];required=a.cf;branches=[];pseudo=None
    for f,m in a.components:
        K,ds,D,pD=a.component(f)
        why=None
        zero=next((i for i in range(len(R)) if not ds[i]),None)
        unequal=next((i for i in range(len(R)) if ds[i]!=ds[a.du[i]]),None)
        if zero is not None:why={'kind':'zero','object':zero}
        elif unequal is not None:why={'kind':'duality','object':unequal}
        else:
            why=norm_failure(pD,required)
            if not why:
                why=field_failure(f,required)
                if not why:why=spherical_global_moment(a,f)
            if not why:
                if f==fp:
                    if pseudo is None:pseudo=pseudo_method(R)
                    if pseudo:why={'kind':'galois_fp'}
        if why is None:return None
        branches.append({'factor':pc(f),'obstruction':why})
    return {'kind':'spherical','generator':a.k,'characters':branches,'pseudo':pseudo}

def check_sphere(R,c,pseudo_checker=None):
    if pseudo_checker is None:pseudo_checker=check_pseudo
    a=Characters(R,c['generator']);fp=a.fp()[0]
    require(len(a.components)==len(c['characters']),'missing character branches')
    pseudo_checked=False
    for (f,m),b in zip(a.components,c['characters']):
        require(pc(f)==b['factor'],'wrong character factor');K,ds,D,pD=a.component(f);v=b['obstruction'];kind=v['kind']
        if kind=='zero':require(not ds[v['object']],'dimension is nonzero')
        elif kind=='duality':require(ds[v['object']]!=ds[a.du[v['object']]],'dual dimensions agree')
        elif kind=='norm':check_norm(pD,a.cf,v)
        elif kind.startswith('field_'):check_field(f,a.cf,v)
        elif kind=='spherical_global_moment':
            require(spherical_global_moment(a,f)==v,'spherical global moment survives')
        elif kind=='galois_fp':
            require(f==fp,'not the FP Galois orbit')
            if not pseudo_checked:pseudo_checker(R,c['pseudo']);pseudo_checked=True
        else:raise VerificationError('unknown spherical obstruction')

def spherical_global_moment(a,f):
    """The same positive central-square measure for any spherical character.

    At each real embedding replace the unknown second indicators by the
    upper bound S=sum(abs(d_i)) over self-dual i. A violated necessary
    inequality at one embedding excludes the whole Galois orbit.
    """
    K,ds,D,pD=a.component(f);w=s.trace(a.C.inv()**2)
    for number,emb in enumerate(embeddings(f)):
        S=sum((K(emb.sign(ds[i]))*ds[i] for i in range(a.n) if a.du[i]==i),K.zero)
        h=K(w)*D*D
        gap=K(2)*(D-h)**2-(D*D-h)*(D*D+D*S-K(2)*h)
        if emb.sign(gap)>0:
            return {'kind':'spherical_global_moment','inverse_square_sum':str(w),
                    'embedding':number,'S':ec(S),'gap':ec(gap)}
    return None

def sign_moment_test(K,ds,delta,original_roots,signed_roots,f,du):
    """Universal central-sign moment test on one character component.

    All characters in that irreducible component are checked simultaneously.
    Indicator signs and twist signs remain the same under Galois conjugation.
    """
    weights=[delta/q for q in original_roots+signed_roots]
    if len(weights)!=2*len(ds) or K.one not in weights:return None
    anchor=weights.index(K.one);h=sum((a*a for a in weights),K.zero)
    embs=embeddings(f)
    if not embs:return {'indicator_choices':0,'twist_choices':0,'survivors':0}
    # Signed self-dual quotients have real embeddings. For non-self-dual
    # quotients, the chosen spherical character is equal on dual pairs.
    if any(e.sign(delta)<=0 or any(e.sign(w)<=0 for w in weights) for e in embs):return None
    twists=[]
    for eta in itertools.product((-1,1),repeat=len(weights)):
        if eta[anchor]!=-1:continue
        if sum((K(v)*a for v,a in zip(eta,weights)),K.zero):continue
        C=sum((K(v)*a*a for v,a in zip(eta,weights)),K.zero)
        twists.append((eta,C))
    sd=[i for i in range(1,len(ds)) if du[i]==i]
    survivors=0;indicator_count=0
    for signs in itertools.product((-1,1),repeat=len(sd)):
        indicator_count+=1
        S=K.one+sum((K(v)*ds[i] for v,i in zip(signs,sd)),K.zero)
        expressions=[K(2)*delta*delta-h, S-(h/delta-delta),delta-S]
        if any(e.sign(v)<0 for v in expressions for e in embs):continue
        for eta,C in twists:
            gap=(K(4)*delta*delta-K(2)*h)*(K(2)*delta*S+K(2)*delta*delta-K(2)*h)-(K(2)*delta-h-C)**2
            if all(e.sign(gap)>=0 for e in embs):survivors+=1
    if survivors:return None
    return {'indicator_choices':indicator_count,'twist_choices':len(twists),'survivors':0}

def signed_component_certificate(R,T,a,f,sphere):
    K,ds,delta,pD=a.component(f);required=codegree_factors(R)+a.cf
    zero=next((i for i in range(len(R)) if not ds[i]),None)
    if zero is not None:return {'kind':'zero','object':zero}
    unequal=next((i for i in range(len(R)) if ds[i]!=ds[a.du[i]]),None)
    if unequal is not None:return {'kind':'duality','object':unequal}
    n=norm_failure(pD,required)
    if n:return n
    n=field_failure(f,required)
    if n:return n
    rr=discover_roots(codegree_poly(R),K);tr=discover_roots(codegree_poly(T),K)
    if rr is None or tr is None:return None
    report=sign_moment_test(K,ds,delta,rr,tr,f,a.du)
    if report is None:return None
    return {'kind':'sign_moments','original_roots':[ec(v) for v in rr],
            'signed_roots':[ec(v) for v in tr],'report':report}

def signed_adjoint_parity(R,T):
    """A skew self-dual simple has even multiplicity in every Y*Y.

    Opposite lifts have opposite second indicators. For some nu_i=+/-1
    one must have R[j,j*,i]-nu_i*T[j,j*,i] divisible by four for every j.
    """
    du=dual(R)
    for i in range(1,len(R)):
        if du[i]!=i:continue
        bad=[]
        for nu in (-1,1):
            j=next((j for j in range(len(R)) if (R[j][du[j]][i]-nu*T[j][du[j]][i])%4),None)
            if j is None:break
            bad.append(j)
        if len(bad)==2:return {'kind':'signed_adjoint_parity','object':i,'failed_rows':bad}
    return None

def check_signed_component(R,T,a,f,c):
    K,ds,delta,pD=a.component(f);required=codegree_factors(R)+a.cf;kind=c['kind']
    if kind=='zero':require(not ds[c['object']],'nonzero signed dimension')
    elif kind=='duality':require(ds[c['object']]!=ds[a.du[c['object']]],'dual dimensions agree')
    elif kind=='norm':check_norm(pD,required,c)
    elif kind.startswith('field_'):check_field(f,required,c)
    elif kind=='sign_moments':
        rr=[K([s.Rational(x) for x in v]) for v in c['original_roots']]
        tr=[K([s.Rational(x) for x in v]) for v in c['signed_roots']]
        require(all(len(v)<=f.degree() for v in c['original_roots']+c['signed_roots']),'unreduced moment root')
        check_roots(codegree_poly(R),K,rr);check_roots(codegree_poly(T),K,tr)
        report=sign_moment_test(K,ds,delta,rr,tr,f,a.du)
        require(report is not None and report==c['report'],'sign-moment branches survive')
    else:raise VerificationError('unknown signed character obstruction')
