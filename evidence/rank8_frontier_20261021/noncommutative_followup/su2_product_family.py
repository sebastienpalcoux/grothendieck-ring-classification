"""Complete all-level SU(2)/adjoint product and integer-scaling family filter.

Scope: a model-family exclusion, never arbitrary noncategorification.
The field-of-products lemma and Euler-phi bound are proved in SU2_FAMILY.md.
"""
from pathlib import Path
import argparse,hashlib,itertools,json,math,sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'noncommutative'))
import central_support as c
s=c.s;t=c.w.t;z,u=s.symbols('z u')

def possible_orders(degree):
    """All n>=3 with phi(n)/2 dividing degree; no level cutoff."""
    bound=2*degree
    primes=[p for p in range(2,bound+2) if s.isprime(p) and bound%(p-1)==0]
    powers=[]
    for p in primes:
        values=[1];a=1
        while s.totient(p**a)<=bound:
            values.append(p**a);a+=1
        powers.append(values)
    return sorted(n for n in (math.prod(v) for v in itertools.product(*powers))
                  if n>=3 and bound%int(s.totient(n))==0)

def adjoint_dimension_polynomial(n):
    cyclotomic=s.cyclotomic_poly(n,z)
    resultant=s.Poly(s.resultant(cyclotomic,z*z-u*z+1,z),u)
    factors=resultant.factor_list()[1]
    c.require(len(factors)==1 and factors[0][1]==2,'real cyclotomic resultant square')
    real=factors[0][0].monic();degree=real.degree()
    c.require(degree==int(s.totient(n))//2,'complete real cyclotomic degree')
    poly=s.Poly(s.cancel(t**degree*real.as_expr().subs(u,2-s.Rational(n)/t)),t).monic()
    c.require(poly.is_irreducible and all(x.q==1 for x in poly.all_coeffs()),'adjoint global dimension polynomial')
    return poly

def compute(source,target=None,require_exclusion=True):
    R=source['tensor'];a=c.w.spectral(R) if target is None else target
    K=a['K'];D=a['D'];embedding=a['embedding'];degree=a['factor'].degree()
    c.require(hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()==source['tensor_sha256'],'census tensor binding')
    primitive_roots=c.w.discover_roots(a['factor'],K)
    c.require(primitive_roots is not None,'target field is Galois')
    c.w.check_roots(a['factor'],K,primitive_roots)
    orders=possible_orders(degree);tests=[];allowed=[]
    for n in orders:
        poly=adjoint_dimension_polynomial(n)
        _,factors=s.Poly.from_list(poly.all_coeffs(),z,domain=K).rep.factor_list()
        factor_degrees=sorted([factor.degree(),multiplicity] for factor,multiplicity in factors)
        if any(d!=1 for d,m in factor_degrees):
            tests.append({'n':n,'level':n-2,'polynomial':list(map(str,poly.all_coeffs())),
                          'outcome':'field_not_contained','factor_degrees_over_target':factor_degrees})
            continue
        roots=c.w.discover_roots(poly,K);c.w.check_roots(poly,K,roots)
        maximum=roots[0]
        for root in roots:
            if embedding.sign(root-maximum)>0:maximum=root
        c.require(all(embedding.sign(root)>0 for root in roots),'totally positive source dimensions')
        if poly.degree()==1:
            c.require(maximum==K(int(poly.TC()*-1)) and embedding.sign(maximum-K.one)>=0,'rational dimensions absorbed into positive integer multiplier')
            tests.append({'n':n,'level':n-2,'outcome':'integer_factor_absorbed','dimension':c.ec(maximum)})
            continue
        c.require(embedding.sign(maximum-K.one)>0,'nontrivial source dimension exceeds one')
        exponent=0;power=K.one
        while embedding.sign(D-power*maximum)>=0:
            exponent+=1;power*=maximum
        c.require(embedding.sign(D-power)>=0 and embedding.sign(power*maximum-D)>0,'complete exact exponent bound')
        tests.append({'n':n,'level':n-2,'polynomial':list(map(str,poly.all_coeffs())),
                      'outcome':'allowed_factor','dimension':c.ec(maximum),'maximum_exponent':exponent,
                      'last_power':c.ec(power),'first_excluded_power':c.ec(power*maximum)})
        allowed.append((n,maximum,exponent))
    candidates=[];matches=[]
    for powers in itertools.product(*(range(bound+1) for n,dimension,bound in allowed)):
        product=K.one
        for exponent,(n,dimension,bound) in zip(powers,allowed):product*=dimension**exponent
        if embedding.sign(product-D)>0:continue
        quotient=D/product;coordinates=list(map(s.Rational,c.ec(quotient)))
        integer=len(coordinates)==1 and coordinates[0].q==1 and coordinates[0]>=1
        record={'exponents':list(powers),'quotient':list(map(str,coordinates)),'positive_integer':bool(integer)}
        candidates.append(record)
        if integer:matches.append(record)
    if require_exclusion:c.require(not matches,'a dimension-compatible model-family source remains')
    return {'id':source['id'],'tensor_sha256':source['tensor_sha256'],
            'scope':'specific_model_family_only','outcome':('dimension_compatible_not_model' if matches else 'family_excluded_by_exact_global_dimension'),
            'target_field_degree':degree,'target_global_dimension':c.ec(D),
            'complete_order_candidates':orders,'order_tests':tests,
            'allowed_order_sequence':[n for n,dimension,bound in allowed],
            'exponent_box_size':math.prod(bound+1 for n,dimension,bound in allowed),
            'dimension_bounded_product_count':len(candidates),'products':candidates,
            'positive_integer_scaling_matches':matches,
            'family':'All finite Deligne products of SU(2)_k and adjoint SU(2)_k, all k>=1; arbitrary positive integer dimension multipliers; all Morita duals.',
            'not_covered':'Other Lie types, arbitrary algebra condensation, dimension-decreasing de-equivariantization, or general categorifications.'}

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--write',action='store_true');args=ap.parse_args()
    census=json.loads((c.OLD.parent/'pipeline/census_m3.json').read_text())
    result=[compute(next(row for row in census if row['id']==rid)) for rid in ('R8_3_721','R8_3_928','R8_3_941','R8_3_1154')]
    path=HERE/'su2_product_family.json'
    if args.write:path.write_text(json.dumps(result,indent=2)+'\n')
    else:c.require(result==json.loads(path.read_text()),'complete SU2 product family replay')
    for row in result:print('PASS',row['id'],'orders',row['allowed_order_sequence'],row['dimension_bounded_product_count'],'complete bounded products; no integer dimension scaling')

if __name__=='__main__':main()
