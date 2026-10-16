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
    for size in (2,3):
        for subset in itertools.combinations(range(1,4),size-1):
            J=(0,)+subset
            if any(du[i] not in J for i in J):continue
            if any(R[i][j][k] for i in J for j in J for k in range(4) if k not in J):continue
            S=sum((ds[i]*ds[du[i]] for i in J),K.zero)
            q=multiplication_matrix(D/S,K,f).charpoly(t).as_poly()
            if any(v.q!=1 for v in q.all_coeffs()):
                return {'kind':'subring','subset':list(J),'quotient_polynomial':pc(q)}
    return None

def check_subring(R,c):
    J=c['subset'];require(0 in J and len(J) in (2,3) and len(set(J))==len(J),'invalid subring')
    a=Characters(R);f,K,ds,D,pD,emb=a.fp();du=a.du
    require(all(du[i] in J for i in J),'subring not dual closed')
    require(not any(R[i][j][k] for i in J for j in J for k in range(4) if k not in J),'subring not closed')
    S=sum((ds[i]*ds[du[i]] for i in J),K.zero);q=multiplication_matrix(D/S,K,f).charpoly(t).as_poly()
    require(pc(q)==c['quotient_polynomial'] and any(v.q!=1 for v in q.all_coeffs()),'quotient integrality not excluded')

def sphere_certificate(R):
    a=Characters(R);fp=a.fp()[0];required=a.cf;branches=[];pseudo=None
    for f,m in a.components:
        K,ds,D,pD=a.component(f)
        why=None
        zero=next((i for i in range(4) if not ds[i]),None)
        unequal=next((i for i in range(4) if ds[i]!=ds[a.du[i]]),None)
        if zero is not None:why={'kind':'zero','object':zero}
        elif unequal is not None:why={'kind':'duality','object':unequal}
        else:
            why=norm_failure(pD,required)
            if not why:
                if f==fp:
                    if pseudo is None:pseudo=pseudo_certificate(R)
                    if pseudo:why={'kind':'galois_fp'}
                if not why:why=field_failure(f,required)
                if not why:why=spherical_global_moment(a,f)
        if why is None:return None
        branches.append({'factor':pc(f),'obstruction':why})
    return {'kind':'spherical','generator':a.k,'characters':branches,'pseudo':pseudo}

def check_sphere(R,c):
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
            if not pseudo_checked:check_pseudo(R,c['pseudo']);pseudo_checked=True
        else:raise VerificationError('unknown spherical obstruction')

def spherical_global_moment(a,f):
    """The same positive central-square measure for any spherical character.

    Adjoint parity fixes an indicator to +1 whenever an adjoint product
    contains that simple with odd multiplicity. At each real embedding
    bound the remaining terms by their absolute values. A violated
    necessary inequality at one embedding excludes the Galois orbit.
    """
    K,ds,D,pD=a.component(f);w=s.trace(a.C.inv()**2)
    for number,emb in enumerate(embeddings(f)):
        S=sum((ds[i] if i==0 or any(a.R[j][a.du[j]][i]%2 for j in range(4))
               else K(emb.sign(ds[i]))*ds[i]
               for i in range(4) if a.du[i]==i),K.zero)
        h=K(w)*D*D
        gap=K(2)*(D-h)**2-(D*D-h)*(D*D+D*S-K(2)*h)
        if emb.sign(gap)>0:
            return {'kind':'spherical_global_moment','inverse_square_sum':str(w),
                    'embedding':number,'S':ec(S),'gap':ec(gap)}
    return None

def sign_moment_test(K,ds,delta,original_roots,signed_roots,f,du,allowed=None):
    """Determined-sign test; one indicator assignment at every embedding.

    Ordinary translates have twist +1, signed translates twist -1.
    Equal codegrees retain their provenance and multiplicity.
    """
    if len(original_roots)!=4 or len(signed_roots)!=4 or delta not in signed_roots:
        return None
    if any(not q for q in original_roots+signed_roots):
        return None
    u=sum((K.one/(q*q) for q in original_roots),K.zero)
    v=sum((K.one/(q*q) for q in signed_roots),K.zero)
    if (sum((K.one/q for q in original_roots),K.zero)!=K.one or
        sum((K.one/q for q in signed_roots),K.zero)!=K.one):
        return None
    embs=embeddings(f)
    if not embs:return None
    if any(e.sign(delta)<=0 or any(e.sign(delta/q)<=0 for q in original_roots+signed_roots)
           for e in embs):return None
    sd=[i for i in range(1,4) if du[i]==i]
    choices=[allowed[i] if allowed is not None else (-1,1) for i in sd]
    indicator_count=0
    for signs in itertools.product(*choices):
        indicator_count+=1
        S=K.one+sum((K(nu)*ds[i] for nu,i in zip(signs,sd)),K.zero)
        expressions=(K(2)-u-v, S/delta-(u+v-K.one),
                     K.one-S/delta,
                     (K(2)-u-v)*(K.one-u-v+S/delta)-(u-K.one/delta)**2)
        if all(e.sign(expression)>=0 for expression in expressions for e in embs):
            return None
    return {'method':'determined_translate_twists_v1','indicator_choices':indicator_count,
            'twist_choices':1,'survivors':0}


def signed_component_certificate(R,T,a,f,sphere):
    K,ds,delta,pD=a.component(f);required=codegree_factors(R)+a.cf
    zero=next((i for i in range(4) if not ds[i]),None)
    if zero is not None:return {'kind':'zero','object':zero}
    unequal=next((i for i in range(4) if ds[i]!=ds[a.du[i]]),None)
    if unequal is not None:return {'kind':'duality','object':unequal}
    n=norm_failure(pD,required)
    if n:return n
    n=field_failure(f,required)
    if n:return n
    rr=discover_roots(codegree_poly(R),K);tr=discover_roots(codegree_poly(T),K)
    if rr is None or tr is None:return None
    report=sign_moment_test(K,ds,delta,rr,tr,f,a.du,signed_indicator_choices(R,T))
    if report is None:return None
    return {'kind':'sign_moments','original_roots':[ec(v) for v in rr],
            'signed_roots':[ec(v) for v in tr],'report':report}

def signed_adjoint_parity(R,T):
    """A skew self-dual simple has even multiplicity in every Y*Y.

    Opposite lifts have opposite second indicators. For some nu_i=+/-1
    one must have R[j,j*,i]-nu_i*T[j,j*,i] divisible by four for every j.
    """
    du=dual(R)
    for i in range(1,4):
        if du[i]!=i:continue
        bad=[]
        for nu in (-1,1):
            j=next((j for j in range(4) if (R[j][du[j]][i]-nu*T[j][du[j]][i])%4),None)
            if j is None:break
            bad.append(j)
        if len(bad)==2:return {'kind':'signed_adjoint_parity','object':i,'failed_rows':bad}
    return None

def signed_indicator_choices(R,T):
    """Keep parity constraints when the same indicators enter the moments."""
    du=dual(R)
    return {i:tuple(nu for nu in (-1,1)
                    if all((R[j][du[j]][i]-nu*T[j][du[j]][i])%4==0 for j in range(4)))
            for i in range(1,4) if du[i]==i}

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
        report=sign_moment_test(K,ds,delta,rr,tr,f,a.du,signed_indicator_choices(R,T))
        require(report is not None and report==c['report'],'sign-moment branches survive')
    else:raise VerificationError('unknown signed character obstruction')

def signed_certificate(R,search):
    A,basis,kind=canonical_duality(R)
    if kind=='sd':
        # Basis choice changes search cost but never the necessary criterion.
        # Each of the three choices of the first nonunit object is compared.
        candidates=[]
        for p in ((0,1,2,3),(0,2,1,3),(0,3,1,2)):
            B=permute(R,p);M=sd_tuple(B)
            cost=sum(math.prod(len(box[k]) for k in (1,2,3,4,5))
                     for box in parity_domain_boxes(M,gauges(M)))
            candidates.append((cost,p,B))
        _,permutation,A=min(candidates,key=lambda item:(item[0],item[1]));basis=list(permutation)
    N=sd_tuple(A) if kind=='sd' else ns_tuple(A)
    require((sd_tensor(N) if kind=='sd' else ns_tensor(N))==A,'nonstandard tensor form')
    images=gauge_images(N) if kind=='sd' else {ns_gauge(N)}
    required=codegree_factors(A);branches=[];sphere=None
    required_primes=sorted({int(q) for f,m in required for q in s.factorint(abs(int(f.TC())))})
    if kind=='sd':
        if search.global_catalog is not None:tables,enumeration=search.global_selfdual(N,required_primes)
        else:tables,enumeration=search.filtered_selfdual(N,required_primes)
    else:tables=search.nonselfdual(N);enumeration=None
    universal_checked=enumeration is not None and enumeration['method']=='global_signed_catalog_v3'
    for p in tables:
        T=sd_tensor(p) if kind=='sd' else ns_tensor(p)
        # Eigenvalue norms must contain every required rational prime.
        det=casimir_determinant(T)
        missing=next((q for q in required_primes if det%q),None)
        if missing is not None:
            why={'kind':'det_prime','prime':missing}
        else:
            dn=None if universal_checked else dnumber(T)
            cy=None if universal_checked or dn else cyclotomic_failure([M.charpoly(t).as_poly() for M in matrices(T)])
            ff=codegree_factors(T);norms=[norm_failure(f,required+ff) for f,m in ff]
            if dn:why={'kind':'signed_dnumber','certificate':dn}
            elif cy:why={'kind':'signed_cyclotomic','certificate':cy}
            elif all(n is not None for n in norms):
                why={'kind':'all_norms','factors':[{'factor':pc(f),'witness':n} for (f,m),n in zip(ff,norms)]}
            elif p in images:
                if sphere is None:sphere=sphere_certificate(A)
                if sphere is None:return None,{'stage':'spherical','tuple':list(p)}
                why={'kind':'unsigned_gauge'}
            else:
                why=signed_adjoint_parity(A,T)
                if why is None:
                    ch=Characters(T);cc=[]
                    for f,m in ch.components:
                        v=signed_component_certificate(A,T,ch,f,sphere)
                        if v is None:return None,{'stage':'signed_character','tuple':list(p),'factor':pc(f)}
                        cc.append({'factor':pc(f),'obstruction':v})
                    why={'kind':'signed_characters','generator':ch.k,'characters':cc}
        branches.append({'tuple':list(p),'obstruction':why})
    certificate={'kind':'signed','basis':basis,'duality_type':kind,'tables':branches,'spherical':sphere}
    if enumeration is not None:certificate['enumeration']=enumeration
    return certificate,None

def check_signed(R,c,search):
    require(tuple(c['basis']) in PERMS,'invalid basis permutation')
    A=permute(R,c['basis']);kind=c['duality_type'];N=sd_tuple(A) if kind=='sd' else ns_tuple(A)
    require((sd_tensor(N) if kind=='sd' else ns_tensor(N))==A,'wrong signed presentation')
    if 'enumeration' in c:
        require(kind=='sd','compressed search requires self-duality')
        required=codegree_factors(A)
        primes=sorted({int(q) for f,m in required for q in s.factorint(abs(int(f.TC())))})
        if c['enumeration']['method']=='global_signed_catalog_v3':tables,enumeration=search.global_selfdual(N,primes)
        else:tables,enumeration=search.filtered_selfdual(N,primes,c['enumeration']['method'])
        require(enumeration==c['enumeration'],'signed exhaustive replay differs')
    else:tables=search.selfdual(N) if kind=='sd' else search.nonselfdual(N)
    require([list(p) for p in tables]==[b['tuple'] for b in c['tables']],'signed enumeration incomplete')
    images=gauge_images(N) if kind=='sd' else {ns_gauge(N)};required=codegree_factors(A);sphere_done=False
    for p,b in zip(tables,c['tables']):
        T=sd_tensor(p) if kind=='sd' else ns_tensor(p);why=b['obstruction'];tag=why['kind']
        if tag=='det_prime':
            q=why['prime'];require(s.isprime(q),'nonprime determinant witness')
            require(any(int(f.TC())%q==0 for f,m in required),'irrelevant prime')
            require(casimir_determinant(T)%q!=0,'determinant prime divides')
        elif tag=='all_norms':
            ff=codegree_factors(T);require(len(ff)==len(why['factors']),'missing signed norm factor')
            for (f,m),v in zip(ff,why['factors']):
                require(pc(f)==v['factor'],'wrong signed norm factor');check_norm(f,required+ff,v['witness'])
        elif tag=='unsigned_gauge':
            require(p in images,'not a sign gauge of original')
            if not sphere_done:check_sphere(A,c['spherical']);sphere_done=True
        elif tag=='signed_characters':
            a=Characters(T,why['generator']);require(len(a.components)==len(why['characters']),'missing signed character')
            for (f,m),v in zip(a.components,why['characters']):
                require(pc(f)==v['factor'],'wrong signed character factor');check_signed_component(A,T,a,f,v['obstruction'])
        elif tag=='signed_adjoint_parity':
            require(signed_adjoint_parity(A,T)==why,'signed adjoint parity not violated')
        elif tag=='signed_dnumber':check_dnumber(T,why['certificate'])
        elif tag=='signed_cyclotomic':check_cyclotomic([M.charpoly(t).as_poly() for M in matrices(T)],why['certificate'])
        else:raise VerificationError('unknown signed branch')
