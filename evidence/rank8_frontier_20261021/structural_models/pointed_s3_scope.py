#!/usr/bin/env python3
"""Source-bound bridge from exact forced indicators to the pointed S3 cocycle."""
from pathlib import Path
import argparse
import hashlib
import itertools
import json

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[2]
NC=HERE.parent/'noncommutative_followup'


def need(c,m):
    if not c:raise ValueError(m)


def run():
    census={r['id']:r for r in json.loads((REPO/'evidence/rank8_m3_20261021/pipeline/census_m3.json').read_text())}
    gate={r['id']:r for r in json.loads((NC/'additional_scope_gates.json').read_text())}
    central={r['id']:r for r in json.loads((NC/'additional_central_constraints.json').read_text())}
    rotations=json.loads((NC/'additional_joint_rotation_h6.json').read_text())
    dual={r['id']:r for r in json.loads((HERE/'s3_full_condensation.json').read_text())['records']}
    routes={r['id']:r for r in json.loads((HERE/'known_model_routes.json').read_text())['records']}
    records=[]
    for row in rotations:
        ident=row['id'];need(ident in ['R8_3_439','R8_3_567'],'two S3 targets')
        source=census[ident];R=source['tensor'];sha=hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()
        need(sha==source['tensor_sha256']==row['tensor_sha256']==gate[ident]['tensor_sha256']==
            central[ident]['tensor_sha256']==dual[ident]['tensor_sha256']==routes[ident]['tensor_sha256'],'all dependency source hashes')
        need(gate[ident]['outcome']=='Galois_pseudo_unitary_reduction','general scope reduction')
        need(central[ident]['full_S_surviving_count']==1 and row['low_index']==2 and row['height']==6,'full low domain and height')
        need(len(row['cases'])==8 and len({tuple(a['indicators'])for a in row['cases']})==8,'complete recorded indicator domain')
        survivors=[a for a in row['cases']if a['decision']['status']=='exact_feasible_relaxation']
        excluded=[a for a in row['cases']if a['decision']['status']=='exact_infeasible_relaxation']
        need(len(survivors)==1 and len(excluded)==7,'seven exact exclusions and one necessary survivor')
        expected=[0,0,1,1,1,1,1]if ident.endswith('_439')else[0,0,0,0,-1,-1,-1]
        need(survivors[0]['indicators']==expected,'forced complete indicator tuple')
        du=[next(j for j in range(8)if R[i][j][0])for i in range(8)]
        inv=[i for i in range(8)if sum(R[i][du[i]])==1]
        need(len(inv)==6,'pointed S3 group order')
        mul=lambda i,j:next(k for k,n in enumerate(R[i][j])if n)
        involutions=[i for i in inv if i!=0 and mul(i,i)==0]
        c3=[0]+[i for i in inv if i!=0 and mul(mul(i,i),i)==0]
        need(len(involutions)==3 and len(c3)==3 and
             all(mul(g,h)in c3 for g,h in itertools.product(c3,repeat=2)),'Sylow subgroups')
        noninv=sorted(set(range(8))-set(inv))
        need(all(R[g][x][x]==R[x][g][x]==1 and sum(R[g][x])==sum(R[x][g])==1
             for g,x in itertools.product(c3,noninv)),'fixed simple rank-one C3 pointed module')
        signs=[expected[g-1]for g in involutions]
        need(len(set(signs))==1,'common Sylow2 pointed sign')
        untwisted=signs[0]==1
        records.append({'id':ident,'tensor_sha256':sha,'scope':'general_complex_after_proved_Galois_PU_reduction',
            'forced_PU_indicators':expected,'pointed_C3_indices':c3,'pointed_order_two_indices':involutions,
            'C3_fixed_noninvertible_indices':noninv,'restriction_to_C3':'trivial_by_rank_one_module_pentagon',
            'restriction_to_C2':'trivial'if untwisted else'nontrivial',
            'restriction_corestriction_indices':[2,3],
            'full_S3_subgroup_algebra_exists_in_every_categorification':untwisted,
            'outcome':('every_categorification_has_rank5_R5_3_40_Morita_dual_with_nonstandard_associator'
                if untwisted else'pointed_S3_associator_has_nontrivial_C2_restriction_full_S3_algebra_impossible'),
            'no_known_rank5_equivariantization_model':routes[ident]['conditional_full_S3_dual_cannot_be_known_equivariantization_category'],
            'limitation':'These are necessary categorical structure constraints; no existence, novelty or general exclusion is proved.'})
    need({r['id']for r in records}=={'R8_3_439','R8_3_567'},'both source records')
    return {'kind':'exact_pointed_S3_cocycle_scope_bridge',
        'required_replays':['../noncommutative_followup/additional_scope_gates.py',
            '../noncommutative_followup/additional_central_constraints.py',
            '../noncommutative_followup/additional_joint_rotation.py',
            'c3_morita_dual.py','s3_full_condensation.py','rank5_route_bindings.py','known_model_routes.py'],
        'proof':'POINTED_S3_SCOPE.md','records':records}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');a=p.parse_args()
    actual=run();path=HERE/'pointed_s3_scope.json'
    if a.write:path.write_text(json.dumps(actual,indent=2)+'\n')
    else:need(actual==json.loads(path.read_text()),'pointed S3 scope receipt changed')
    print('PASS:439 pointed class trivial and rank5 Morita branch necessary;567 pointed C2 class nontrivial; no existence claim.')
