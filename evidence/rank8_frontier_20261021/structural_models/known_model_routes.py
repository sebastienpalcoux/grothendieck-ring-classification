#!/usr/bin/env python3
"""Exact closure of specified near-group and SU2 model branches, not general exclusions."""
from pathlib import Path
import argparse
import hashlib
import itertools
import json
import math
import sympy as s
from verify_structural_scope import closure

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[2]


def need(c,m):
    if not c:raise ValueError(m)


def sha(R):return hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()


def crossed_tensor():
    """Known coherent inversion action on NG(C3,6); basis (a,e), index4e+a."""
    N=[[[0]*4 for _ in range(4)]for _ in range(4)]
    for a,b in itertools.product(range(3),repeat=2):N[a][b][(a+b)%3]=1
    for a in range(3):N[a][3][3]=N[3][a][3]=1
    N[3][3]=[1,1,1,6]
    theta=[0,2,1,3];R=[[[0]*8 for _ in range(8)]for _ in range(8)]
    for a,b,e,f in itertools.product(range(4),range(4),range(2),range(2)):
        for c,n in enumerate(N[a][theta[b]if e else b]):R[4*e+a][4*f+b][4*(e^f)+c]=n
    need(all(sum(R[i][j][a]*R[a][k][h]for a in range(8))==
             sum(R[j][k][a]*R[i][a][h]for a in range(8))
        for i,j,k,h in itertools.product(range(8),repeat=4)),'crossed associativity')
    need(all(not n or (i//4)^(j//4)==k//4 for i,j,k in itertools.product(range(8),repeat=3)
        for n in [R[i][j][k]]),'faithful C2 grading')
    return R


def run():
    sources={r['id']:r for r in json.loads((REPO/'evidence/rank8_m3_20261021/pipeline/census_m3.json').read_text())}
    su2_path=HERE.parent/'noncommutative_followup/su2_all_frontier.json'
    su2={r['id']:r for r in json.loads(su2_path.read_text())['records']}
    rank5=json.loads((HERE/'rank5_route_bindings.json').read_text())
    possible_duals=[r for r in rank5['records']if r['route_tensor'].startswith('S3_dual_')]
    need(len(possible_duals)==5 and
        [r['rank5_source_id']for r in possible_duals if r['status']=='known_unitary_based_ring']==['R5_3_40']and
        sum(r['status']=='general_complex_excluded'for r in possible_duals)==4,'complete conditional rank-five branch')
    cross=crossed_tensor();records=[]
    for ident in ['R8_3_439','R8_3_567']:
        row=sources[ident];R=row['tensor'];need(sha(R)==row['tensor_sha256'],'source hash')
        du=[next(j for j in range(8)if R[i][j][0])for i in range(8)]
        inv=[i for i in range(8)if sum(R[i][du[i]])==1]
        central=[i for i in inv if all(R[i][j]==R[j][i]for j in range(8))]
        seed=sorted({k for i in range(8)for k,n in enumerate(R[i][du[i]])if n})
        adjoint=closure(R,seed)
        need(len(inv)==6 and central==[0]and adjoint==list(range(8)),'trivial central-invertible and grading data')
        a=su2[ident]
        need(a['tensor_sha256']==row['tensor_sha256'],'SU2 receipt source binding')
        need(a['allowed_order_sequence']==[12]and
            a['positive_integer_scaling_matches']==[{'exponents':[1],'quotient':['2'],'positive_integer':True}],
            'complete retained SU2 dimension domain')
        need(max(v for M in cross for r in M for v in r)==6 and
             max(v for M in R for r in M for v in r)==3,'crossed tensor multiplicity mismatch')
        records.append({'id':ident,'tensor_sha256':row['tensor_sha256'],
            'invertibles':inv,'central_invertible_source_labels':central,
            'adjoint_seed':seed,'adjoint_closure':adjoint,
            'all_complex_categorifications_center_invertible_count':1,
            'complete_SU2_retained_dimension_branch':{'adjoint_level':10,'nonrational_exponent':1,'total_integer_multiplier':2},
            'SU2_family_outcome':'family_excluded_by_trivial_center_invertibles',
            'inversion_crossed_product_outcome':'full512_based_tensor_excluded_by_exact_multiplicity_and_grading_invariants',
            'conditional_full_S3_dual_remaining_based_ring':'R5_3_40',
            'conditional_full_S3_dual_cannot_be_known_equivariantization_category':True,
            'limitation':'A different associator on the same rank-five based ring, a nontrivial pointed S3 cocycle, arbitrary algebra condensation and unrelated construction families remain open.'})
    row=sources['R8_3_721'];R=row['tensor'];need(sha(R)==row['tensor_sha256'],'721 hash')
    q=s.sqrt(17);dims=[1,(3+q)/2,(3+q)/2,4+q,(5+q)/2,3+q,(5+q)/2,5+q]
    need(all(s.expand(dims[i]*dims[j]-sum(R[i][j][k]*dims[k]for k in range(8)))==0
        for i,j in itertools.product(range(8),repeat=2)),'721 positive dimension homomorphism')
    D=s.expand(sum(d*d for d in dims));need(D==136+32*q,'721 global FP dimension')
    trace=272;norm=1088;need(s.expand(D*(136-32*q))==norm,'721 norm')
    # For a near-group ring: D0=2n+m*d, d²=n+m*d.
    # Therefore Tr(D0)=4n+m² and Nm(D0)=n Tr(D0).
    # D=tD0 gives n=Nm(D)/(t Tr(D))=4/t and m²=256/t.
    branches=[]
    for t in [1,2,4]:
        n=4//t;m2=256//t;m=math.isqrt(m2)
        if m*m!=m2:
            branches.append({'integer_multiplier':t,'group_order':n,'multiplicity_square':m2,'outcome':'not_an_integer_multiplicity'})
            continue
        if n==1:
            need(m==8,'rank-two branch')
            branches.append({'integer_multiplier':t,'group_order':n,'multiplicity':m,
                'outcome':'excluded_by_Ostrik_unrestricted_rank_two_classification'})
        else:
            selected=[r for r in rank5['records']if r['route_tensor']in ['NG_C4_m16','NG_V4_m16']]
            need(n==4 and m==16 and len(selected)==2 and
                all(r['status']=='general_complex_excluded'for r in selected),'rank-five near-group proof inputs')
            branches.append({'integer_multiplier':t,'group_order':n,'multiplicity':m,
                'all_groups':['C4','V4'],'rank5_source_ids':[r['rank5_source_id']for r in selected],
                'outcome':'both_groups_excluded_by_fresh_frozen_rank5_proof_replay'})
    records.append({'id':row['id'],'tensor_sha256':row['tensor_sha256'],
        'global_FP_dimension':str(D),'trace':trace,'norm':norm,
        'all_possible_positive_integer_multipliers':[1,2,4],
        'complete_near_group_branches':branches,
        'outcome':'all_near_group_sources_with_positive_integer_scaling_and_Morita_duals_excluded',
        'limitation':'No dimension-decreasing de-equivariantization, arbitrary product of two nonintegral source categories, or unrelated algebra condensation is covered.'})
    return {'kind':'exact_scoped_closure_of_remaining_known_model_branches',
        'required_replays':['rank5_route_bindings.py','s3_full_condensation.py',
            '../noncommutative_followup/su2_all_frontier.py'],
        'records':records,'known_inversion_crossed_product_tensor':cross,
        'known_inversion_action_reference':'Izumi1512.04288v2 Lemma13.1, Example13.10, printed pp118,124-125; actual order-two gamma_(1,-id,R(pi/4)L)',
        'rank_two_reference':'Ostrik math/0203255, Main Theorem, printed p1',
        'proof':'KNOWN_MODEL_ROUTES.md',
        'conclusion':'All outcomes are exclusions of precisely specified construction families; none is a general noncategorification decision for439,567 or721.'}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');a=p.parse_args()
    actual=run();path=HERE/'known_model_routes.json'
    if a.write:path.write_text(json.dumps(actual,indent=2)+'\n')
    else:need(actual==json.loads(path.read_text()),'known model route receipt changed')
    print('PASS: complete SU2 model branches439/567 and all integer-scaled near-group branches721 excluded; no general decision.')
