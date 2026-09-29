"""General ramification/Casimir obstructions and signed reductions.

For a self-dual commutative ring, sphericalization gives a signed order A
with A/2A=R/2R. If this reduction has exactly one non-etale factor of rank
two and the FP dimension field is quadratic ramified at two, central
induction isolates the dimension field. Integrality bounds the Casimir
deficit. A negative deficit proves general nonexistence immediately.
Otherwise every remaining coefficient magnitude and every sign table can
be exhausted, with no indicator normalization.
"""
import itertools
import math
from pathlib import Path
import re
import subprocess
import tempfile
import sympy as s
from exact import require,pc,poly,norm_failure,field_failure,check_norm,check_field
from rings import Characters,dual,validate,codegree_factors
from signed import signed_problem,from_values,gauge_original
from proofs import positive_sign_embedding,signed_component_certificate,check_signed_component


def mod_two_factors(R):
    n=len(R);vectors=list(itertools.product((0,1),repeat=n));zero=(0,)*n
    def mul(a,b):
        return tuple(sum(a[i]*b[j]*R[i][j][k] for i in range(n) for j in range(n))%2
                     for k in range(n))
    idems=[v for v in vectors if v!=zero and mul(v,v)==v]
    primitive=[v for v in idems if not any(w!=v and mul(v,w)==w for w in idems)]
    require(tuple(sum(v[i] for v in primitive)%2 for i in range(n))==(1,)+(0,)*(n-1),
            'primitive idempotents do not sum to the unit')
    require(all(mul(v,w)==zero for v,w in itertools.combinations(primitive,2)),
            'primitive idempotents are not orthogonal')
    factors=[]
    for e in primitive:
        space=[v for v in vectors if mul(e,v)==v]
        rank=(len(space)).bit_length()-1
        require(len(space)==2**rank,'mod-two factor does not have power-of-two order')
        nonzero=[v for v in space if v!=zero]
        field=all(any(mul(v,w)==e for w in nonzero) for v in nonzero)
        nil=[v for v in nonzero if mul(v,v)==zero]
        kind='unramified_field' if field else 'dual_numbers' if rank==2 and len(nil)==1 else 'other'
        factors.append({'unit':list(e),'rank':rank,'kind':kind,
                        'elements':[list(v) for v in space],
                        'square_zero_nonzero':[list(v) for v in nil]})
    require(sum(f['rank'] for f in factors)==n,'incomplete mod-two decomposition')
    return factors


def arithmetic(R):
    n=len(R)
    if n!=6 or dual(R)!=list(range(n)) or any(R[i][j]!=R[j][i] for i in range(n) for j in range(n)):
        return None
    validate(R)
    a=Characters(R);f,K,ds,D,pD,emb=a.fp()
    if pD.degree()!=2:return None
    aa,bb,cc=map(s.Rational,pD.all_coeffs());A=-bb/(2*aa);norm=cc/aa
    disc=s.discriminant(pD)
    if disc<=0 or disc.q!=1:return None
    q=math.prod(int(p) for p,e in s.factorint(int(disc)).items() if e%2)
    if q<=1 or q%4 not in (2,3):return None
    B=s.sqrt((A*A-norm)/q)
    if A.is_Integer is not True or B.is_Integer is not True or B<=0:return None
    A,B=int(A),int(B);norm=A*A-q*B*B
    factors=mod_two_factors(R)
    bad=[v for v in factors if v['kind']!='unramified_field']
    if len(bad)!=1 or bad[0]['kind']!='dual_numbers':return None
    # Delta=2q*S+2*b*sqrt(q). Delta/D must lie in Z[sqrt(q)].
    L=[[s.Rational(2*q*A,norm),s.Rational(-2*q*B,norm)],
       [s.Rational(-2*q*B,norm),s.Rational(2*A,norm)]]
    rational_codegrees=[]
    # Every character of R pulls back to a character of sphericalization
    # with twice its codegree. Central induction therefore makes Delta/c
    # integral for EVERY original codegree c, not only the FP codegree D.
    for factor,multiplicity in codegree_factors(R):
        if factor.degree()!=1:continue
        value=-s.Rational(factor.TC(),factor.LC())
        require(value>0 and value.q==1,'rational formal codegree is not a positive integer')
        rational_codegrees.append(int(value))
        L.extend([[s.Rational(2*q,value),s.S.Zero],
                  [s.S.Zero,s.Rational(2,value)]])
    modulus=math.lcm(*(int(v.q) for row in L for v in row))
    if modulus>100000:raise TimeoutError('ramification divisibility modulus budget')
    H=[[int(v*modulus) for v in row] for row in L]
    step=None;witness=None;failed=[]
    # Admissible S form a subgroup of Z containing modulus*Z. Its positive
    # generator divides modulus, so checking these divisors is exhaustive.
    for candidate in sorted(map(int,s.divisors(modulus))):
        b=next((b for b in range(modulus) if all((h[0]*candidate+h[1]*b)%modulus==0 for h in H)),None)
        if b is not None:step=candidate;witness=b;break
        failed.append(candidate)
    require(step is not None,'no admissible norm lattice')
    trace=sum(v*v for row in R for cell in row for v in cell)
    # The other n-2 characters each have formal codegree strictly greater
    # than one. Thus the integral trace is at least 4*q*step+n-1.
    lower=4*q*step+n-1;budget=trace-lower
    return {'quadratic_radicand':q,'FP_dimension':[A,B],
            'FP_dimension_polynomial':pc(pD),'mod_two_factors':factors,
            'rational_formal_codegrees':rational_codegrees,
            'integrality_matrix':[[str(v) for v in row] for row in L],
            'modulus':modulus,'S_step':step,'S_residue_witness':witness,
            'failed_divisor_steps':failed,'original_Casimir_trace':trace,
            'signed_Casimir_trace_lower_bound':lower,'deficit_budget':budget}


def magnitude_branches(R,data):
    p=signed_problem(R,adjoint_parity=False,positive_indicators=False)
    bounds=[max(map(abs,d)) for d in p['domains']]
    weights=[len(set(itertools.permutations(orb[0]))) for orb in p['active']]
    out=[]
    def rec(i,remaining,values):
        if len(out)>10000:raise TimeoutError('signed magnitude branch budget')
        if i==len(bounds):out.append(values);return
        bound=bounds[i]
        for v in range(bound,-1,-2):
            cost=weights[i]*(bound*bound-v*v)
            if cost<=remaining:rec(i+1,remaining-cost,values+[v])
    if data['deficit_budget']>=0:rec(0,data['deficit_budget'],[])
    return p,out


def enumerate_magnitude(R,p,magnitudes,seconds=60):
    """Independent original DFS backend, restricted only by proved magnitudes."""
    source=p['source']
    for i,bound in enumerate(magnitudes):
        domain=[v for v in p['domains'][i] if abs(v)==bound]
        require(domain,'empty signed magnitude domain')
        pattern=r'for\(int x:vector<int>\{[^}]+\}\)\{v\['+str(i)+r'\]=x;'
        replacement='for(int x:vector<int>{'+','.join(map(str,domain))+'}){v['+str(i)+']=x;'
        source,count=re.subn(pattern,replacement,source)
        require(count==1,'signed DFS loop reconstruction failed')
    with tempfile.TemporaryDirectory() as td:
        cpp=Path(td)/'enum.cpp';exe=Path(td)/'enum';cpp.write_text(source)
        subprocess.run(['g++','-std=c++17','-O3',str(cpp),'-o',str(exe)],check=True,capture_output=True)
        run=subprocess.run([str(exe)],capture_output=True,text=True,check=True,timeout=seconds)
    stats=re.fullmatch(r'nodes (\d+) solutions (\d+)\s*',run.stderr)
    require(stats is not None,'missing signed enumeration completion report')
    values=sorted(tuple(map(int,line.split())) for line in run.stdout.splitlines())
    require(len(values)==int(stats[2]) and len(set(values))==len(values),'signed solution count')
    for v in values:
        require(len(v)==len(magnitudes) and all(abs(x)==m and x in dom for x,m,dom in zip(v,magnitudes,p['domains'])),
                'signed solution outside exhaustive domain')
        validate(from_values(R,p,v),nonnegative=False)
    return values,{'nodes':int(stats[1]),'solutions':int(stats[2]),'complete':True}


def original_characters(R):
    a=Characters(R);fp=a.fp()[0];out=[]
    for f,m in a.components:
        K,ds,D,pD=a.component(f)
        zero=next((i for i,d in enumerate(ds) if not d),None)
        unequal=next((i for i,d in enumerate(ds) if d!=ds[a.du[i]]),None)
        why=({'kind':'zero','object':zero} if zero is not None else
             {'kind':'duality','object':unequal} if unequal is not None else
             norm_failure(pD,a.cf) or field_failure(f,a.cf) or
             ({'kind':'galois_fp'} if f==fp else positive_sign_embedding(R,f,ds)))
        if why is None:return None
        out.append({'factor':pc(f),'obstruction_or_reduction':why})
    return {'generator':a.k,'characters':out}


def reduction(R,seconds=60):
    data=arithmetic(R)
    if data is None:return None
    original=original_characters(R)
    if original is None:return None
    p,domains=magnitude_branches(R,data);branches=[]
    for magnitude in domains:
        values,stats=enumerate_magnitude(R,p,magnitude,seconds)
        cases=[]
        for v in values:
            T=from_values(R,p,v);gauge=gauge_original(T,R)
            case={'values':list(v)}
            if gauge is not None:case['gauge_original']=gauge
            else:
                a=Characters(T);chars=[]
                for f,m in a.components:
                    why=signed_component_certificate(R,T,a,f,{})
                    if why is None:return None
                    chars.append({'factor':pc(f),'obstruction':why})
                case.update(generator=a.k,characters=chars)
            cases.append(case)
        branches.append({'magnitudes':magnitude,'statistics':stats,'cases':cases})
    return {'kind':'ramified_signed_reduction','arithmetic':data,
            'indicator_restrictions':False,'sign_gauges':p['gauges'],
            'magnitude_branches':branches,'original_characters':original,
            'claim':'Every categorification has a pseudo-unitary Galois conjugate.'}


def verify_reduction(R,c):
    require(c['kind']=='ramified_signed_reduction','wrong ramified reduction kind')
    data=arithmetic(R)
    require(data is not None and c['arithmetic']==data,'incorrect ramification or trace hypotheses')
    require(c['indicator_restrictions'] is False,'indicator restrictions were introduced')
    p,domains=magnitude_branches(R,data)
    require(c['sign_gauges']==p['gauges'],'incorrect certified sign gauges')
    require([b['magnitudes'] for b in c['magnitude_branches']]==domains,'missing magnitude branch')
    for magnitude,branch in zip(domains,c['magnitude_branches']):
        values,stats=enumerate_magnitude(R,p,magnitude,120)
        require(branch['statistics']==stats,'incorrect complete enumeration statistics')
        require([x['values'] for x in branch['cases']]==[list(v) for v in values],'missing signed table')
        for v,case in zip(values,branch['cases']):
            T=from_values(R,p,v)
            if 'gauge_original' in case:
                require(gauge_original(T,R)==case['gauge_original'],'incorrect original sign gauge')
            else:
                a=Characters(T,case['generator'])
                require(len(a.components)==len(case['characters']),'missing signed character')
                for (f,m),cc in zip(a.components,case['characters']):
                    require(pc(f)==cc['factor'],'wrong signed character orbit')
                    check_signed_component(R,T,a,f,cc['obstruction'])
    original=c['original_characters'];a=Characters(R,original['generator']);fp=a.fp()[0]
    require(len(a.components)==len(original['characters']),'missing original character')
    for (f,m),cc in zip(a.components,original['characters']):
        require(pc(f)==cc['factor'],'incorrect original character orbit')
        K,ds,D,pD=a.component(f);why=cc['obstruction_or_reduction'];kind=why['kind']
        if kind=='zero':require(not ds[why['object']],'zero-dimension obstruction failed')
        elif kind=='duality':require(ds[why['object']]!=ds[a.du[why['object']]],'duality obstruction failed')
        elif kind=='norm':check_norm(pD,a.cf,why)
        elif kind.startswith('field_'):check_field(f,a.cf,why)
        elif kind=='galois_fp':require(f==fp,'character is not the FP orbit')
        elif kind=='galois_fp_signs':require(positive_sign_embedding(R,f,ds)==why,'invalid positive tensor-sign twist')
        else:require(False,'unknown original character obstruction')
    require(c['claim']=='Every categorification has a pseudo-unitary Galois conjugate.','incorrect claim')
    return True


def certificate(R,pseudo=None,seconds=60):
    data=arithmetic(R)
    if data is not None and data['deficit_budget']<0:
        return {'kind':'ramified_Casimir_trace_exclusion','arithmetic':data}
    c=reduction(R,seconds)
    if c is None:return None
    if not any(cc['obstruction_or_reduction']['kind'].startswith('galois_fp')
               for cc in c['original_characters']['characters']):
        return {'kind':'ramified_signed_arithmetic_exclusion','reduction':c}
    if pseudo is None:return None
    from oriented_extension import pseudo_check
    pseudo_check(R,pseudo)
    return {'kind':'ramified_signed_pseudo_exclusion','reduction':c,'pseudo':pseudo}


def field_certificate(R):
    data=arithmetic(R)
    if data is None:return None
    f=poly([1,0,-data['quadratic_radicand']])
    why=field_failure(f,codegree_factors(R))
    if why is None:return None
    return {'kind':'ramified_dimension_field_exclusion','arithmetic':data,
            'dimension_field_polynomial':pc(f),'field_obstruction':why}


def verify(R,c):
    if c['kind']=='ramified_Casimir_trace_exclusion':
        data=arithmetic(R)
        require(data is not None and data==c['arithmetic'],'incorrect ramification or trace arithmetic')
        require(data['deficit_budget']<0,'signed Casimir trace does not contradict the coefficient bound')
        return True
    if c['kind']=='ramified_dimension_field_exclusion':
        data=arithmetic(R)
        require(data is not None and data==c['arithmetic'],'incorrect ramified dimension field')
        f=poly([1,0,-data['quadratic_radicand']])
        require(pc(f)==c['dimension_field_polynomial'],'incorrect dimension field polynomial')
        check_field(f,codegree_factors(R),c['field_obstruction'])
        return True
    if c['kind']=='ramified_signed_arithmetic_exclusion':
        verify_reduction(R,c['reduction'])
        require(not any(cc['obstruction_or_reduction']['kind'].startswith('galois_fp')
                        for cc in c['reduction']['original_characters']['characters']),
                'an original dimension character remains unrejected')
        return True
    require(c['kind']=='ramified_signed_pseudo_exclusion','wrong general exclusion kind')
    verify_reduction(R,c['reduction'])
    from oriented_extension import pseudo_check
    pseudo_check(R,c['pseudo'])
    return True
