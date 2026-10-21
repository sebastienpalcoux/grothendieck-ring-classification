"""All34 applicability table for the existing generalized-near-group sieve.

The proof is quadratic/RESIDUAL_QUADRATIC_SEARCH.md. This source-bound
extension uses only its trace/norm equations and checks all six original
quadratic outputs. Integral targets are explicitly outside this quadratic
parameter exhaustion, and dimension matches are never models.
"""
from pathlib import Path
import argparse,hashlib,importlib.util,json,math
import sympy as s

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('frontier_ng_dimensions',HERE.parent/'structural_models/near_group_scaling.py')
old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
spec=importlib.util.spec_from_file_location('frontier_quadratic_models',HERE.parent/'quadratic/rank_two_and_models.py')
quadratic=importlib.util.module_from_spec(spec);spec.loader.exec_module(quadratic)
require=old.require

def parameters(polynomial):
    degree=len(polynomial)-1
    if degree==1:return {'outcome':'integral_target_outside_quadratic_parameter_exhaustion','families':[]}
    if degree>2:return {'outcome':'family_dimension_excluded_by_degree','families':[]}
    trace=-polynomial[1];norm=polynomial[2];order=s.cancel(norm/trace);families=[]
    if order.is_Integer and order>0:
        order=int(order)
        for multiplier in s.divisors(order):
            group_order=order//multiplier
            for stabilizer in s.divisors(group_order):
                orbit=group_order//stabilizer
                K2=s.cancel(trace/(multiplier*orbit)-4*stabilizer)
                if not K2.is_Integer or K2<0:continue
                K=math.isqrt(int(K2))
                if K*K!=K2:continue
                require(trace==multiplier*orbit*(4*stabilizer+K*K),'source trace equation')
                require(norm==multiplier**2*orbit**2*stabilizer*(4*stabilizer+K*K),'source norm equation')
                rank_two_excluded=group_order==orbit==stabilizer==1 and K>1
                families.append({'integer_dimension_multiplier':int(multiplier),
                                 'invertible_group_order':int(group_order),
                                 'stabilizer_order':int(stabilizer),
                                 'noninvertible_orbit_size':int(orbit),
                                 'total_noninvertible_multiplicity':K,
                                 'base_rank':int(group_order+orbit),
                                 'base_rank_two_classification_excludes':rank_two_excluded,
                                 'status':'impossible_rank_two_base' if rank_two_excluded else 'dimension_match_only_no_model_or_Morita_equivalence'})
    return {'outcome':'family_dimension_excluded' if not families else 'finite_family_dimension_matches_only',
            'forced_group_order_before_integer_multiplier':str(order),'families':families}

def compute_all():
    census={r['id']:r for r in json.loads((ROOT/'evidence/rank8_m3_20261021/pipeline/census_m3.json').read_text())}
    baseline=json.loads((ROOT/'evidence/rank8_m3_20261021/pipeline/residual_audit.json').read_text())['records']
    require(len(baseline)==34 and len({r['id'] for r in baseline})==34,'distinct baseline34')
    out=[]
    for row in baseline:
        source=census[row['id']];R=source['tensor']
        digest=hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()
        require(digest==source['tensor_sha256']==row['tensor_sha256'],'source binding')
        p,interval=old.fp_polynomial(R);record=parameters(list(map(s.Rational,p)))
        index=int(row['id'].split('_')[-1])
        if index in quadratic.TARGETS:
            previous=quadratic.generalized_near_group(quadratic.exact_dimensions(index))
            require(record['families']==previous['families'],'previous six-case theorem output cross-check')
        out.append({'id':row['id'],'tensor_sha256':digest,'global_dimension_minimal_polynomial':p,
                    'positive_root_interval':interval,'scope':'specific_model_family_only',**record})
    return {'proof':'../quadratic/RESIDUAL_QUADRATIC_SEARCH.md',
            'family':'One generalized-near-group source, arbitrary positive integer dimension multipliers and Morita equivalence; no division or products of distinct nonintegral sources',
            'records':out,'counts':{key:sum(r['outcome']==key for r in out) for key in sorted({r['outcome'] for r in out})}}

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--write',action='store_true');args=ap.parse_args()
    result=compute_all();path=HERE/'generalized_near_group_all_frontier.json'
    if args.write:path.write_text(json.dumps(result,indent=2)+'\n')
    else:require(result==json.loads(path.read_text()),'all34 generalized-near-group replay')
    print('PASS',result['counts'])
    for row in result['records']:
        if row['families']:print(row['id'],row['families'])

if __name__=='__main__':main()
