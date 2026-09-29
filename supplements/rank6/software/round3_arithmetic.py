"""Inert quadratic residue fields and complementary signed codegrees.

Tensor-only general necessary test. The local hypothesis identifies the signed
categorical dimension field by the etale algebra modulo two; complete finite
quadratic d-number and reciprocal-codegree enumeration then bounds its signed
Casimir trace. No pivotal or pseudo-unitary hypothesis is used in arithmetic().
"""
from fractions import Fraction
from itertools import combinations_with_replacement
import json, math
from pathlib import Path
import sympy as s
from exact import require, pc, t
from rings import dual, validate, codegree_factors, casimir
from new_module_spectral import perron_factor
from new_ramified_signed import mod_two_factors, magnitude_branches, enumerate_magnitude, original_characters
from signed import from_values, gauge_original


def hypotheses(R):
    n=len(R)
    if n!=6 or dual(R)!=list(range(n)) or any(R[i][j]!=R[j][i] for i in range(n) for j in range(n)):return None
    fs=codegree_factors(R)
    if any(f.degree()>2 for f,m in fs):return None
    ix,interval=perron_factor([f for f,m in fs]);f=fs[ix][0]
    if f.degree()!=2:return None
    A,B=-int(f.all_coeffs()[1]),int(f.TC())
    if B<=0:return None
    fac=s.factorint(B);q=math.prod(int(p) for p,e in fac.items() if e%2);scale=math.isqrt(B//q)
    if q<=1 or q%4!=1 or scale*scale*q!=B or A%(scale*q):return None
    # D/(scale sqrt(q)) has integral trace sqrt(discriminant)/(scale sqrt(q))
    # and norm -1, hence is an integral unit.
    v=(A*A-4*B)//q
    if v*q!=A*A-4*B or v<0:return None
    b=math.isqrt(v)
    if b*b!=v or b%scale:return None
    for g,m in fs:
        if g.degree()==2:
            disc=int(s.discriminant(g.as_expr(),t));sf=math.prod(int(p) for p,e in s.factorint(disc).items() if e%2)
            if sf!=q:return None
    local=mod_two_factors(R)
    even=[z for z in local if z['rank']%2==0]
    if q%8==5 and all(z['kind']=='unramified_field' for z in local) and len(even)==1 and even[0]['rank']==2:
        isolation='unique_inert_quadratic_factor'
    elif q%8==1 and sorted((z['rank'],z['kind']) for z in local)==[(1,'unramified_field'),(2,'dual_numbers'),(3,'unramified_field')]:
        # Signed character fields are cyclotomic and therefore abelian Galois.
        # The etale cubic completion belongs to a global cubic field: a degree
        # six Galois field would need another local degree-three factor, while
        # the remaining local blocks have ranks two and one. The complement
        # has rank three and contains the quadratic dimension field.
        isolation='cyclotomic_cubic_local_factor'
    else:return None
    validate(R)
    return {'quadratic_radicand':q,'scale':scale,'FP_polynomial':pc(f),
            'FP_isolating_interval':interval,'FP_unit_trace':b//scale,
            'local_factors':local,'Casimir_trace':int(s.trace(casimir(R))),
            'original_codegrees':[{'polynomial':pc(g),'multiplicity':m} for g,m in fs],
            'dimension_field_degree':2,'complementary_codegrees_rational':True,
            'field_isolation':isolation}


def reciprocal_tuples(divisors,k,target,maxsum):
    """Sorted positive divisor tuples; exact bounds and exact rational sums."""
    def rec(lo,remaining,need,budget,chosen):
        if remaining==0:
            if need==0:yield tuple(chosen)
            return
        for i in range(lo,len(divisors)):
            d=divisors[i]
            if remaining*d>budget:break
            if Fraction(remaining,d)<need:break
            rest=need-Fraction(1,d)
            if rest<0:continue
            yield from rec(i,remaining-1,rest,budget-d,chosen+[d])
    return list(rec(0,k,target,maxsum,[]))


def arithmetic(R):
    h=hypotheses(R)
    if h is None:return None
    q,scale,T=(h[k] for k in ('quadratic_radicand','scale','Casimir_trace'))
    ymax=(T-5)//(scale*q)
    if ymax>1000:raise TimeoutError('explicit inert quadratic trace-parameter budget')
    survivors=[];counts={'integral_totally_positive':0,'dnumber':0,'positive_reciprocal_remainder':0}
    # Delta=scale*(q*y+x*sqrt(q))/2, theta=(x+y*sqrt(q))/2 integral.
    for y in range(1,ymax+1):
        xmax=math.isqrt(q*y*y-1)
        for x in range(-xmax,xmax+1):
            if (x-y)%2:continue
            counts['integral_totally_positive']+=1
            normnumer=q*y*y-x*x
            if (4*q*y*y)%normnumer:continue
            counts['dnumber']+=1
            inverse_trace=Fraction(4*y,scale*normnumer)
            if inverse_trace>=1:continue
            counts['positive_reciprocal_remainder']+=1
            content=math.gcd(scale*(q*y-x)//2,scale*x)
            divisors=[int(d) for d in s.divisors(abs(content)) if d>1]
            for fs in reciprocal_tuples(divisors,4,1-inverse_trace,T-scale*q*y):
                # Necessary divisibility by ALL original rational codegrees.
                rational=[-int(s.Poly.from_list(z['polynomial'],t).TC())
                          for z in h['original_codegrees'] if len(z['polynomial'])==2]
                if any(content%c for c in rational):continue
                polynomial=s.Poly.from_list([1,-scale*q*y,scale*scale*q*normnumer//4],t)
                for f in fs:polynomial*=s.Poly(t-f,t)
                parity=[int(v)%2 for v in polynomial.all_coeffs()]
                expected=[int(v)%2 for v in casimir(R).charpoly(t).all_coeffs()]
                if parity!=expected:continue
                survivors.append({'theta_numerator':[x,y],'theta_denominator':2,
                    'dimension_numerator':[scale*q*y,scale*x],'dimension_denominator':2,
                    'dimension_trace':scale*q*y,'dimension_norm':scale*scale*q*normnumer//4,
                    'complementary_codegrees':list(fs),'signed_Casimir_trace':scale*q*y+sum(fs),
                    'Casimir_polynomial_mod2':parity})
    lower=min((z['signed_Casimir_trace'] for z in survivors),default=None)
    return {'kind':'inert_quadratic_signed_spectrum','scope':'general_complex_fusion_categories',
        'hypotheses':h,'trace_parameter_upper_bound':ymax,'counts':counts,'spectra':survivors,
        'signed_Casimir_lower_bound':lower,'excluded':not survivors,
        'deficit_budget':None if lower is None else T-lower}


def reduction(R,seconds=120):
    a=arithmetic(R)
    if a is None or a['excluded']:return None
    # Only attempt the rigorously bounded finite magnitude problem when saturated.
    if a['deficit_budget']!=0:return None
    original=original_characters(R)
    if original is None:return None
    p,domains=magnitude_branches(R,a);require(len(domains)==1,'saturation magnitude count')
    values,stats=enumerate_magnitude(R,p,domains[0],seconds)
    cases=[]
    for v in values:
        g=gauge_original(from_values(R,p,v),R)
        if g is None:return None
        cases.append({'values':list(v),'gauge_original':g})
    return {'kind':'inert_quadratic_general_to_pseudo','scope':'general_complex_fusion_categories',
        'arithmetic':a,'indicator_restrictions':False,'magnitudes':domains[0],
        'sign_gauges':p['gauges'],'statistics':stats,'signed_tables':cases,
        'original_characters':original,'claim':'Every categorification has a pseudo-unitary Galois conjugate.'}


def verify_reduction(R,c):
    require(c.get('kind')=='inert_quadratic_general_to_pseudo','wrong inert quadratic reduction kind')
    z=reduction(R)
    require(z is not None and z==c,'inert quadratic reduction differs from exact recomputation')
    return True


def certificate(R,pseudo=None):
    a=arithmetic(R)
    if a is None:return None
    if a['excluded']:return a
    if pseudo is None:return None
    r=reduction(R)
    if r is None:return None
    from oriented_extension import pseudo_check
    pseudo_check(R,pseudo)
    return {'kind':'inert_quadratic_pseudo_exclusion','scope':'general_complex_fusion_categories',
            'reduction':r,'pseudo':pseudo}


def verify(R,c):
    require(c.get('scope')=='general_complex_fusion_categories','wrong arithmetic scope')
    if c.get('kind')=='inert_quadratic_signed_spectrum':
        z=arithmetic(R);require(z is not None and z['excluded'] and z==c,'spectrum exclusion not reproduced');return True
    require(c.get('kind')=='inert_quadratic_pseudo_exclusion','wrong arithmetic exclusion kind')
    verify_reduction(R,c['reduction'])
    from oriented_extension import pseudo_check
    pseudo_check(R,c['pseudo'])
    return True

if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--all',action='store_true');ap.add_argument('--output',required=True);args=ap.parse_args()
    root=Path(__file__).resolve().parents[1]
    rows=json.load(open(root/'data'/('census.json' if args.all else 'unresolved_tensors.json')))
    out=[]
    for row in rows:
        a=arithmetic(row['N'])
        if a is not None:
            out.append({'id':row['id'],'arithmetic':a})
            print(row['id'],a['excluded'],a['deficit_budget'],flush=True)
    Path(args.output).write_text(json.dumps({'checked':len(rows),'applicable':out},indent=2)+'\n')
