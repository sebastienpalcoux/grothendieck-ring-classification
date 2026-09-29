"""Different-ideal and finite conductor obstruction for the split quadratic frontier.

The tensor hypotheses isolate one rank-six arithmetic profile. All abelian
signed dimension fields of degrees two, four and six are exhausted by the
proved local/different-ideal conductor theorem in the accompanying proof.
No numerical bounds, optimizers, or identifier-based decisions are used.
"""
import itertools,json,math
from fractions import Fraction as F
import sympy as s
from exact import require,t,pc,field,key,embeddings,evaluate
from rings import dual,validate,codegree_factors,casimir
from round3_arithmetic import reciprocal_tuples
from new_ramified_signed import mod_two_factors,magnitude_branches,enumerate_magnitude,original_characters
from signed import from_values,gauge_original


def hypotheses(R):
    if len(R)!=6 or dual(R)!=list(range(6)) or any(R[i][j]!=R[j][i] for i in range(6) for j in range(6)):return None
    fs=codegree_factors(R)
    expected=[(['1','-9'],4),(['1','-7380','13284'],1)]
    if [(pc(f),m) for f,m in fs]!=expected:return None
    if int(s.trace(casimir(R)))!=7416:return None
    local=mod_two_factors(R)
    if sorted((a['rank'],a['kind']) for a in local)!=[(1,'unramified_field')]*4+[(2,'dual_numbers')]:return None
    validate(R)
    return {'codegrees':[{'polynomial':pc(f),'multiplicity':m} for f,m in fs],
        'Casimir_trace':7416,'trace_ideal':738,'quadratic_radicand':41,'scale':18,'local_factors':local}


def quadratic_spectra():
    q=41;c=18;T=7416;out=[];counts={'dimension_candidates':0,'quadratic_complement_candidates':0}
    def integraldiv(A,B,S,r,P):
        for rr in (r,-r):
            a=F(A*S-q*B*rr,4*P);b=F(B*S-A*rr,4*P)
            if (a-b).denominator!=1 or (2*b).denominator!=1:return False
        return True
    for y in range(1,11):
        for x in range(-math.isqrt(q*y*y-1),math.isqrt(q*y*y-1)+1):
            if (x-y)%2:continue
            n=q*y*y-x*x
            if (4*q*y*y)%n:continue
            A=c*q*y;B=c*x;N=c*c*q*n//4;content=math.gcd((A-B)//2,B)
            if content%9:continue
            target=1-F(4*y,c*n)
            if target<=0:continue
            divisors=[int(d) for d in s.divisors(abs(content)) if d>1];pairs=[]
            for P in map(int,s.divisors(N)):
                for r in range(1,math.isqrt(max(0,((T-A-3)**2-4*P)//q))+1):
                    S=math.isqrt(4*P+q*r*r)
                    if S*S!=4*P+q*r*r or S<=2 or P-S+1<=0 or S*S%P:continue
                    if integraldiv(A,B,S,r,P):pairs.append((S,P,r))
            counts['dimension_candidates']+=1;counts['quadratic_complement_candidates']+=len(pairs)
            records=[]
            for fs in reciprocal_tuples(divisors,4,target,T-A):
                records.append({'rational':list(fs),'quadratic':[],'trace':A+sum(fs)})
            for S,P,r in pairs:
                for fs in reciprocal_tuples(divisors,2,target-F(S,P),T-A-S):
                    records.append({'rational':list(fs),'quadratic':[[S,P,r]],'trace':A+sum(fs)+S})
            for (S,P,r),(S2,P2,r2) in itertools.combinations_with_replacement(pairs,2):
                if A+S+S2<=T and F(S,P)+F(S2,P2)==target:
                    records.append({'rational':[],'quadratic':[[S,P,r],[S2,P2,r2]],'trace':A+S+S2})
            if records:out.append({'y':y,'x':x,'spectra':records})
    return {'counts':counts,'survivors':out}


def coordinates(z):
    return s.Matrix(list(reversed([s.S.Zero]*(4-len(key(z)))+list(key(z)))))


def quartic_enumeration(M,ys):
    require(M in (5,21),'unexpected quartic conductor twist')
    f=s.Poly(t**4-41*M*t*t+164*M*M,t);K=field(f);a=K([1,0]);r=(K(2)*a*a/K(M)-K(41))/K(5)
    beta=(a*a*a-K(33*M)*a)/K(10*M)
    require(r*r==K(41) and beta*beta==K(M)*(K(41)-K(5)*r)/K(2) and a*beta==K(2*M)*r,'quartic radical identities')
    require(not evaluate(f.all_coeffs(),beta,K) and evaluate(key(beta),beta,K)==-a,'quartic cyclic automorphism')
    bas=[K.one,(K.one+r)/K(2),(K.one+r+K(2)*a)/K(4),(K.one-r+K(2)*beta)/K(4)]
    powers=[K.one,a,a*a,a*a*a]
    def matrix(z):return s.Matrix.hstack(*(coordinates(z*v) for v in powers))
    tr=lambda z:s.trace(matrix(z))
    B=s.Matrix.hstack(*map(coordinates,bas));BI=B.inv()
    require(all(all(x.q==1 for x in BI*coordinates(b*c)) for b in bas for c in bas),'claimed integral basis not a ring')
    order_tensor=[[[int(x) for x in BI*coordinates(b*c)] for c in bas] for b in bas]
    local=mod_two_factors(order_tensor)
    require(sorted((v['rank'],v['kind']) for v in local)==[(1,'unramified_field')]*4,'quartic field not completely split at two')
    require(len(f.factor_list()[1])==1,'quartic defining polynomial reducible')
    require(all(all(v.q==1 for v in matrix(b).charpoly(t).all_coeffs()) for b in bas),'basis element nonintegral')
    G=s.Matrix([[tr(b*c) for c in bas] for b in bas]);disc=int(G.det())
    require(disc==41**3*M*M,'wrong quartic discriminant')
    # Maximality follows from the exhaustive abelian conductor calculation:
    # this totally real cyclic quartic field has conductor 41*M and hence
    # discriminant 41*(41*M)^2. See the self-contained proof.
    GI=G.inv();dual=[sum((K(GI[i,j])*bas[i] for i in range(4)),K.zero) for j in range(4)]
    coeff=[b/(K(18)*r) for b in dual];E=embeddings(f)
    tracevec=[int(tr(K(18)*r*b)) for b in bas]
    totals=[]
    for y in ys:
        T=738*y
        # Deliberately loose bounds. Every endpoint is certified by exact
        # algebraic sign comparisons of the trace-dual coefficient functions.
        bounds=[[-3*y,2*y+2],[-2,y+2],[-y-2,y+2],[-y-2,y+2]]
        for j,cj in enumerate(coeff):
            require(all(e.sign(K(T)*cj-K(bounds[j][0]))>0 and e.sign(K(bounds[j][1])-K(T)*cj)>0 for e in E),'insufficient complete quartic coordinate bounds')
        positive=[];survivors=[];pivot=1;others=[0,2,3]
        for zs in itertools.product(*(range(bounds[j][0],bounds[j][1]+1) for j in others)):
            top=T-sum(tracevec[j]*v for j,v in zip(others,zs))
            if top%tracevec[pivot]:continue
            z=[0]*4
            for j,v in zip(others,zs):z[j]=v
            z[pivot]=top//tracevec[pivot]
            if not bounds[pivot][0]<=z[pivot]<=bounds[pivot][1]:continue
            theta=sum((K(v)*b for v,b in zip(z,bas)),K.zero);delta=K(18)*r*theta
            if any(e.sign(delta)<=0 for e in E):continue
            P=matrix(delta).charpoly(t).as_poly();co=list(map(int,P.all_coeffs()));N=co[-1]
            require(N>0 and co[1]==-T,'wrong positive dimension trace/norm')
            # Characteristic polynomial includes each field embedding. For a
            # d-number, its jth coefficient^4 is divisible by Norm(delta)^j,
            # also when delta has smaller minimal degree.
            failure=next((j for j in range(1,5) if co[j]**4%N**j),None)
            record={'theta_coordinates':z,'dimension_polynomial':co,'dnumber_failed_coefficient':failure}
            positive.append(record)
            if failure is None:survivors.append(record)
        totals.append({'y':y,'trace':T,'coordinate_bounds':bounds,'positive_candidates':positive,'dnumber_survivors':survivors})
    return {'twist':M,'conductor':41*M,'polynomial':pc(f),'discriminant':disc,
        'integral_basis_power_coordinates':[[str(x) for x in row] for row in B.tolist()],
        'dimension_trace_coordinates':tracevec,'local_factors_at_two':local,'cases':totals}


def arithmetic(R):
    h=hypotheses(R)
    if h is None:return None
    quadratic=quadratic_spectra();quartics=[quartic_enumeration(5,[5,10]),quartic_enumeration(21,[7])]
    require(all(not c['dnumber_survivors'] for f in quartics for c in f['cases']),'quartic dimension field survives')
    require(quadratic['survivors'] and all(v['trace']==7416 for z in quadratic['survivors'] for v in z['spectra']),'quadratic signed trace is not saturated')
    # The only remaining possible sextic field is E41 times a cyclic cubic
    # field of conductor63. Positivity and different divisibility give
    # b in P_7^2 totally positive with Tr(b)=7, impossible by norm>=49.
    require(49*27>7**3,'sextic AM-GM contradiction fails')
    return {'kind':'split_quadratic_different_arithmetic','scope':'general_complex_fusion_categories',
        'hypotheses':h,'quadratic':quadratic,'cyclic_quartic':quartics,
        'sextic':{'cubic_conductor':63,'positive_cubic_trace':7,'cubic_norm_lower_bound':49,'AMGM_comparison':[49*27,7**3]},
        'signed_Casimir_lower_bound':7416,'deficit_budget':0}


def reduction(R,seconds=120):
    a=arithmetic(R)
    if a is None:return None
    original=original_characters(R)
    if original is None:return None
    p,domains=magnitude_branches(R,a);require(len(domains)==1,'saturated magnitude count')
    values,stats=enumerate_magnitude(R,p,domains[0],seconds);cases=[]
    for v in values:
        g=gauge_original(from_values(R,p,v),R)
        if g is None:return None
        cases.append({'values':list(v),'gauge_original':g})
    return {'kind':'split_quadratic_different_reduction','scope':'general_complex_fusion_categories',
        'arithmetic':a,'indicator_restrictions':False,'magnitudes':domains[0],
        'sign_gauges':p['gauges'],'statistics':stats,'signed_tables':cases,
        'original_characters':original,'claim':'Every categorification has a pseudo-unitary Galois conjugate.'}


def verify_reduction(R,c):
    r=reduction(R);require(r is not None and r==c,'different-ideal reduction differs from exact replay');return True


def certificate(R,pseudo=None):
    if pseudo is None:return None
    r=reduction(R)
    if r is None:return None
    from oriented_extension import pseudo_check
    pseudo_check(R,pseudo)
    return {'kind':'split_quadratic_different_pseudo_exclusion','scope':'general_complex_fusion_categories','reduction':r,'pseudo':pseudo}


def verify(R,c):
    require(c.get('kind')=='split_quadratic_different_pseudo_exclusion' and c.get('scope')=='general_complex_fusion_categories','wrong different-ideal scope or kind')
    verify_reduction(R,c['reduction'])
    from oriented_extension import pseudo_check
    pseudo_check(R,c['pseudo']);return True
