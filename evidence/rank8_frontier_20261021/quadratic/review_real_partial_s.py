"""Independent exact review of the real-quadratic partial-S adapter.

Checks full character rows independently from source H interpolation,
and tests integrality using multiplication matrices in the defining
power basis instead of radical-coordinate trace/norm formulas.
"""
from pathlib import Path
import argparse
import hashlib
import json
import sys
import sympy as s

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'global_induction'))
import partial_s as ps
from rank_two_and_models import need


def field_vector(value,degree):
    co=[s.Rational(c.numerator,c.denominator) for c in value.to_list()]
    return s.Matrix(list(reversed([s.Rational(0)]*(degree-len(co))+co)))


def multiplication_integrality(K,value,degree):
    z=K([1,0]);basis=[z**i for i in range(degree)]
    operator=s.Matrix.hstack(*(field_vector(value*b,degree) for b in basis))
    coefficients=operator.charpoly().all_coeffs()
    return all(c.q==1 for c in coefficients),list(map(str,coefficients))


def independent_characters(T,profile):
    K=T.K;q=profile['FP_quadratic_radicand'];rad=T.basis[1]
    need(rad*rad==K(q),'incorrect field radical')
    rows=[]
    for f in profile['factorization_over_FP_quadratic_field']:
        need(f['degree']==1,'incomplete independent character coverage')
        expr=-s.sympify(f['monic_coefficients'][1]);b=s.expand(expr).coeff(s.sqrt(q));a=s.simplify(expr-b*s.sqrt(q))
        need(a.is_Rational and b.is_Rational,'nonquadratic root expression')
        root=K(a)+K(b)*rad
        row=tuple(sum((K(s.Rational(c))*root**j for j,c in enumerate(co)),K.zero)
                  for co in profile['basis_polynomial_coordinates_in_H'])
        rows.append(row)
    need(set(rows)==set(T.characters),'independent full character tables disagree')
    return rows


def audit(R,a,profile=None,control=False):
    T=ps.RealTable(R,a);K=T.K;need(T.degree==2,'review is scoped to quadratic fields')
    if profile is not None:independent_characters(T,profile)
    if control:
        root=T.basis[1];phi=(K.one+root)/K(2)
        rows=[tuple((K(-1) if (g&h).bit_count()%2 else K.one)*(v if f else K.one)
              for f in range(2) for g in range(4)) for v in [phi,K.one-phi] for h in range(4)]
        need(set(rows)==set(T.characters),'Fibonacci times V4 character table mismatch')
        need(multiplication_integrality(K,phi,2)[0] and not multiplication_integrality(K,K(s.Rational(1,2)),2)[0],
             'integral closure positive/negative control failed')
        central=[]
        for g in range(4):
            for u,v in [(1,0),(0,1),(1,1)]:
                column=[0]*8;column[g]=u;column[g+4]=v;central.append(column)
                need(T.failure(column) is None,'known Fibonacci times V4 center column rejected')
        return {'known_model':'Fibonacci tensor Vec(C2 times C2)',
                'all_eight_explicit_characters_match':True,'known_center_restriction_columns_retained':central,
                'half_integral_algebraic_integer_control':True,'rational_noninteger_control':True}
    candidates=[tuple(c)for group in a['columns']for c in group]+[(0,)+tuple(v)for v,z in a['high']]
    cache={};failed=0;examples=[]
    for v in candidates:
        dim=sum((K(n)*d for n,d in zip(v,T.ds)),K.zero);need(dim!=K.zero,'zero column')
        failures=[]
        for E,(row,beta) in enumerate(zip(T.characters,T.beta)):
            value=beta*sum((K(n)*ch for n,ch in zip(v,row)),K.zero)/dim
            key=tuple(map(str,value.to_list()))
            if key not in cache:cache[key]=multiplication_integrality(K,value,2)
            okay,poly=cache[key]
            if not okay:failures.append((E,poly))
        actual=T.failure(v)
        need((actual is None)==(not failures),'radical formula disagrees with multiplication-operator integrality')
        if failures:
            failed+=1
            need(actual['character']==failures[0][0] and actual['multiplication_characteristic_polynomial']==failures[0][1],
                 'nonintegrality certificate mismatch')
            if len(examples)<3:examples.append({'column':list(v),'independent_failure':actual})
    return {'total_low_and_high_candidates_checked':len(candidates),'nonintegral_candidates':failed,
            'distinct_exact_field_values_checked':len(cache),'all_eight_independent_characters_match':True,
            'independent_failure_examples':examples}


def run():
    coverage=json.loads((HERE/'character_field_coverage_results.json').read_text())
    records=[]
    for index in [1768,1795,3258]:
        row=ps.st.load_ring(f'R8_3_{index}');R=row['tensor']
        profile=next(r for r in coverage['records']if r['id']==row['id'])
        digest=hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()
        need(digest==profile['tensor_sha256']==row['tensor_sha256'],'source tensor mismatch')
        a=ps.st.old.setup(R)
        records.append({'id':row['id'],'tensor_sha256':digest,**audit(R,a,profile)})
    R=[[[0]*8 for _ in range(8)]for _ in range(8)]
    for i in range(8):
        for j in range(8):
            f,g=divmod(i,4);h,k=divmod(j,4)
            for z in ([0,1]if f==h==1 else[f+h]):R[i][j][4*z+(g^k)]+=1
    control=audit(R,ps.st.old.setup(R),control=True)
    return {'kind':'independent_real_quadratic_partial_S_review',
            'adapter_source_sha256':hashlib.sha256((HERE.parent/'global_induction/partial_s.py').read_bytes()).hexdigest(),
            'categorical_scope':'pseudo-unitary center modular-eigenvalue integrality; arithmetic review does not extend the scope',
            'records':records,'positive_control':control}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--write',action='store_true');a=p.parse_args()
    actual=run();path=HERE/'review_real_partial_s_results.json'
    if a.write:path.write_text(json.dumps(actual,indent=2)+'\n')
    else:need(json.loads(path.read_text())==actual,'independent partial-S review receipt changed')
    print('PASS: independent full-character and multiplication-integrality review of three quadratic rings and positive control')
