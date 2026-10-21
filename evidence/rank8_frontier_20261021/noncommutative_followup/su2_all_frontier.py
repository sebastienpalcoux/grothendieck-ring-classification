"""Complete SU(2)/adjoint integer-scaled product audit of all34 baseline frontiers.

This extends the independently reviewed four-case arithmetic without imposing
the C^4+M2 Wedderburn condition: only the exact positive scalar character is
needed. Dimension matches remain matches, never categorical constructions.
"""
import argparse,json
import su2_product_family as family

HERE=family.HERE;c=family.c

def compute_all():
    census={r['id']:r for r in json.loads((c.OLD.parent/'pipeline/census_m3.json').read_text())}
    baseline=json.loads((c.OLD.parent/'pipeline/residual_audit.json').read_text())['records']
    c.require(len(baseline)==34 and len({r['id'] for r in baseline})==34,'baseline34 distinct records')
    result=[]
    for row in baseline:
        source=census[row['id']]
        c.require(source['tensor_sha256']==row['tensor_sha256'],'baseline tensor binding')
        a=c.w.ScalarCharacters(source['tensor'])
        f,K,ds,D,pD,emb=a.fp()
        target={'factor':f,'K':K,'D':D,'embedding':emb}
        record=family.compute(source,target,require_exclusion=False)
        record['positive_scalar_character_verified']=True
        record['target_global_dimension_minimal_polynomial']=list(map(str,pD.all_coeffs()))
        result.append(record)
        print(source['id'],record['outcome'],record['dimension_bounded_product_count'],flush=True)
    return {'scope':'specific_model_family_only; all34 baseline frontier rings',
            'proof':'SU2_FAMILY.md','records':result,
            'excluded_count':sum(not r['positive_integer_scaling_matches'] for r in result),
            'dimension_match_count':sum(bool(r['positive_integer_scaling_matches']) for r in result)}

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--write',action='store_true');args=ap.parse_args()
    result=compute_all();path=HERE/'su2_all_frontier.json'
    if args.write:path.write_text(json.dumps(result,indent=2)+'\n')
    else:c.require(result==json.loads(path.read_text()),'all34 complete SU2 family replay')
    print('PASS',result['excluded_count'],'family exclusions;',result['dimension_match_count'],'dimension matches, not models')

if __name__=='__main__':main()
