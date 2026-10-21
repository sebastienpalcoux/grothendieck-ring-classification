"""Exact cubic Verlinde obstruction for the forced centerless R439 dual.

Read-only default: reconstruct the complete low/S domain, all 58 integer
Gram completions by two independent algorithms, and their nonintegral
cubic coefficients. No numerical optimizer is used by this verifier.
"""
from pathlib import Path
from collections import Counter
from fractions import Fraction
import argparse,hashlib,importlib.util,json
import verify as base

HERE=Path(__file__).resolve().parent
FRONTIER=HERE.parent
spec=importlib.util.spec_from_file_location('r439_integer_gram',FRONTIER/'rank5_integer_gram/verify.py')
gram=importlib.util.module_from_spec(spec);spec.loader.exec_module(gram)
need=base.need


def integral_nonnegative(x):
    c=x.to_list()
    return len(c)<=1 and (not c or (c[0].denominator==1 and c[0]>=0))


def coefficient(K,D,fc,character,cols,high,multiplicities,dimensions):
    """N(A,A;A), with A self-dual and S_A,Z=D/f chi(FZ)."""
    total=K.zero
    for col,m in [(v,1)for v in cols]+[((0,)+v,m)for(v,z),m in zip(high,multiplicities)]:
        dim=sum((K(v)*d for v,d in zip(col,dimensions)),K.zero)
        total+=K(m)*base.value(character,col,K)**3/dim
    return D/fc**3*total


def fibonacci_control():
    """The actual modular center Fib x Fib^rev has N_(X,X)^3=1."""
    s=base.s;x=s.Symbol('x');K=s.QQ.alg_field_from_poly(s.Poly(x*x-x-1,x),alias='phi')
    phi=K.unit;D=K(2)+phi;f=K(3)-phi;dims=[K.one,phi];chi=[K.one,K.one-phi]
    cols=[(1,0),(1,1)]
    total=sum((base.value(chi,col,K)**3/sum((K(v)*d for v,d in zip(col,dims)),K.zero)for col in cols),K.zero)
    total+=K(2)*chi[1]**3/phi
    result=D/f**3*total
    need(result==K.one,'known Fibonacci-center cubic positive control')
    return {'source':'Fibonacci fusion category','distinguished_restrictions':[[1,0],[1,1]],
            'high_restriction':[0,1],'high_multiplicity':2,'cubic_fusion_coefficient':1}


def run():
    R=base.source();a=base.h.quadratic_data(R);K=a['K'];fc,chars=base.spectral(R,a)
    need(a['ch'].du==list(range(5)),'all rank-five source simples self-dual')
    frames=[];survivors=[]
    for index,cols in enumerate(a['lows']):
        fail=base.h.low_failure(cols,a['ch'].C,a['ds'],a['D'],K,a['embedding'],a['ch'].du)
        assignments=[]if fail else base.assignments(a,fc,chars,cols)
        frames.append({'index':index,'ordinary_obstruction':fail,'symmetric_S_assignments':[list(p)for p in assignments]})
        survivors.extend((index,cols,p)for p in assignments)
    need([index for index,cols,p in survivors]==[12,12],'complete full-S low domain')
    index,cols,perm=survivors[0]
    need(all(p[1]==1 for i,c,p in survivors),'conjugate-FP character labels the same A in every assignment')
    Q,high,bad,center=base.high_filter(a,fc,chars,cols)
    integer_data=gram.run()
    saved_integer=json.loads((FRONTIER/'rank5_integer_gram/results.json').read_text())
    need(json.loads(json.dumps(integer_data,default=int))==saved_integer,'independent complete integer-Gram receipt')
    need(integer_data['high_vectors']==[list(v)for v,z in high],'high-vector ordering')
    need(integer_data['low_columns']==[list(v)for v in cols],'unique low frame binding')
    need(integer_data['solution_count']==58,'complete 58-pattern domain')
    values=[];histogram=Counter()
    for pattern,m in enumerate(integer_data['solutions']):
        value=coefficient(K,a['D'],fc[1],chars[1],cols,high,m,a['ds'])
        polynomial=base.multiplication_matrix(value,K,a['factor']).charpoly().all_coeffs()
        need(not integral_nonnegative(value),'a centerless integer-Gram pattern passed the cubic obstruction')
        key=tuple(str(c)for c in value.to_list());histogram[key]+=1
        values.append({'pattern_index':pattern,'cubic_coefficient_power_basis':base.h.ec(value),
            'coefficient_characteristic_polynomial':list(map(str,polynomial)),
            'obstruction':'irrational'if len(value.to_list())>1 else'nonintegral_rational'})
    expected={('-1/144','35/24'):16,('1/3',):16,('-5/288','37/16'):16,
              ('-1/72','31/12'):6,('1/36','-5/6'):4}
    need(dict(histogram)==expected,'complete exact cubic histogram')
    dependencies=[]
    for relative in ['r439_centerless_rank5/verify.py','rank5_integer_gram/verify.py','rank5_integer_gram/results.json',
        'review/INTEGRAL_CENTER_SUBCATEGORY.md','review/integral_center_subcategory.py','review/integral_center_subcategory.json',
        'structural_models/pointed_s3_scope.py','structural_models/pointed_s3_scope.json',
        'structural_models/s3_full_condensation.py','structural_models/s3_full_condensation.json',
        'structural_models/rank5_route_bindings.py','structural_models/rank5_route_bindings.json',
        'structural_models/known_model_routes.py','structural_models/known_model_routes.json',
        'noncommutative_followup/additional_scope_gates.py','noncommutative_followup/additional_scope_gates.json']:
        p=FRONTIER/relative
        dependencies.append({'path':str(p.relative_to(HERE.parents[2])),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
    return {'target':'R8_3_439','kind':'general_exclusion_via_forced_centerless_rank5_dual',
        'rank5_source_id':'R5_3_40','rank5_tensor_sha256':base.TENSOR_SHA,'source_archive_sha256':base.ARCHIVE_SHA,
        'power_basis_polynomial':base.h.pc(a['factor']),
        'global_dimension_power_basis':base.h.ec(a['D']),
        'distinguished_formal_codegree_power_basis':base.h.ec(fc[1]),
        'distinguished_character_power_basis':[base.h.ec(x)for x in chars[1]],
        'all_low_frames':frames,'unique_low_frame_index':12,'low_columns':[list(v)for v in cols],
        'complete_symmetric_S_assignments':[list(p)for i,c,p in survivors],
        'integer_Gram_pattern_count':58,'cubic_checks':values,
        'coefficient_histogram':[{'descending_power_basis':list(k),'pattern_count':n}for k,n in sorted(histogram.items())],
        'known_model_control':fibonacci_control(),'dependencies':dependencies,
        'scope':'general_complex_fusion_categories: first use independently certified Galois-pseudo-unitary and full-S3 Morita reductions; then a single distinguished cubic Verlinde coefficient excludes every remaining integer Gram completion',
        'outcome':'general_exclusion'}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--write',action='store_true');args=parser.parse_args()
    actual=json.loads(json.dumps(run(),default=int));path=HERE/'verlinde_exclusion.json'
    if args.write:path.write_text(json.dumps(actual,indent=2)+'\n')
    else:need(actual==json.loads(path.read_text()),'complete exact Verlinde exclusion receipt')
    print('PASS: all58 complete integer Gram patterns have a nonintegral cubic Verlinde coefficient; R8_3_439 generally excluded.')
