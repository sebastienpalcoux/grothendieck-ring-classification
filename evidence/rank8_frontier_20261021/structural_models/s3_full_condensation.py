#!/usr/bin/env python3
"""Conditional full-S3 Morita branch for439/567; no categorical identification."""
from pathlib import Path
import argparse
import hashlib
import itertools
import json
import zipfile
import sympy as s

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[2]


def need(c,m):
    if not c:raise ValueError(m)


def rank5(paired,a):
    b=6-a;R=[[[0]*5 for _ in range(5)]for _ in range(5)]
    for i in range(5):R[0][i][i]=R[i][0][i]=1
    def put(i,j,v):R[i][j]=v[:];R[j][i]=v[:]
    put(1,1,[1,0,0,0,0]);put(1,2,[0,0,1,0,0])
    put(1,3,[0,0,0,0,1]);put(1,4,[0,0,0,1,0])
    put(2,2,[1,1,1,0,0]);put(2,3,[0,0,0,1,1]);put(2,4,[0,0,0,1,1])
    put(3,3,[int(not paired),int(paired),1,a,b])
    put(4,4,[int(not paired),int(paired),1,a,b])
    put(3,4,[int(paired),int(not paired),1,b,a])
    return R


def valid(R):
    dual=[next(j for j in range(5)if R[i][j][0])for i in range(5)]
    if not all(R[i][j][k]==R[dual[i]][k][j]==R[k][dual[j]][i]
        for i,j,k in itertools.product(range(5),repeat=3)):return False
    return all(sum(R[i][j][a]*R[a][k][h]for a in range(5))==
               sum(R[j][k][a]*R[i][a][h]for a in range(5))
        for i,j,k,h in itertools.product(range(5),repeat=4))


def run():
    sources={r['id']:r for r in json.loads((REPO/'evidence/rank8_m3_20261021/pipeline/census_m3.json').read_text())}
    previous=json.loads((HERE/'c3_morita_dual.json').read_text())
    records=[]
    for row in previous['records']:
        source=sources[row['id']];R=source['tensor'];sha=hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()
        need(sha==source['tensor_sha256']==row['tensor_sha256'],'source tensor hash')
        left=list(map(s.Matrix,row['left_module_matrices']))
        h=row['source_generators']['h'];g=row['source_generators']['g'];x=row['source_generators']['X']
        U=s.Matrix(row['right_dual_opposite_matrices'][h])
        need(U*U==s.eye(8)and all(U*M==M*U for M in left),'right involution')
        perm=[next(i for i in range(8)if U[i,j])for j in range(8)]
        need(all(perm[i]!=i for i in range(8)),'free right involution')
        orbits=sorted({tuple(sorted([i,perm[i]]))for i in range(8)})
        B=s.Matrix(8,4,lambda i,j:int(i in orbits[j]))
        mats=[s.Matrix(4,4,lambda i,j:sum(M[orbits[i][0],k]for k in orbits[j]))for M in left]
        need(all(L*B==B*M for L,M in zip(left,mats)),'exact module quotient')
        for i,j in itertools.product(range(8),repeat=2):
            need(mats[i]*mats[j]==sum((R[i][j][k]*mats[k]for k in range(8)),s.zeros(4)), 'all source quotient fusion rules')
        expected=s.Matrix([[0,1,1,1],[1,2,2,2],[1,2,2,2],[1,2,2,2]])
        need(mats[x]==expected,'full S3 module noninvertible matrix')
        groupmats={tuple(M)for i,M in enumerate(mats)if sum(R[i][next(j for j in range(8)if R[i][j][0])])==1}
        need(len(groupmats)==6 and mats[g][0,0]==mats[h][0,0]==1,'S3 fixes free pointed module')
        need({next(i for i in range(4)if s.Matrix(4,4,M)[i,1])for M in groupmats}=={1,2,3},'transitive triple')
        records.append({'id':row['id'],'tensor_sha256':sha,
            'hypothesis':'pointed S3 associator class is trivial; not proved or assumed for general classification',
            'right_S3_module_rank':4,'right_S3_module_basis_orbits':[list(o)for o in orbits],
            'left_source_action_matrices':[[list(M.row(i))for i in range(4)]for M in mats],
            'left_S3_module_orbits':[[0],[1,2,3]],'left_S3_stabilizers':['S3','C2'],
            'conditional_dual_rank':5,'conditional_dual_dimensions':['1','1','2','3+2sqrt(3)','3+2sqrt(3)'],
            'outcome':'conditional_rank_five_Morita_branch_survives; no_model_or_exclusion',
            'limitation':'The pointed C2 part of H3(S3,C*) is not trivialized by a C3-fixed simple. Same rank/dimensions or a possible same based ring do not identify associators or imply centrality.'})
    candidates=[];raw=[]
    archive=REPO/'evidence/prepublication_20261017/rank5/rank5_current_replay.zip'
    archive_sha='264fd1b7f1851cbce142ea248a19bc2d0196ba44f350b2f5852e1e77a647a92d'
    need(hashlib.sha256(archive.read_bytes()).hexdigest()==archive_sha,'pinned rank-five archive')
    with zipfile.ZipFile(archive)as z:
        member=next(n for n in z.namelist()if n.endswith('/data/positive_models.json'))
        known=next(r['tensor']for r in json.loads(z.read(member))if r['name']=='Izumi C3+6 equivariantization')
    # The only possible nonintegral coefficients sum to six. Interchanging
    # the two d-dimensional simples exchanges a and6-a.
    for paired in [False,True]:
        for a in range(7):
            R=rank5(paired,a)
            if not valid(R):continue
            raw.append([paired,a])
            if a>3:continue
            d=3+2*s.sqrt(3);dims=[1,1,2,d,d]
            need(all(s.expand(dims[i]*dims[j]-sum(R[i][j][k]*dims[k]for k in range(5)))==0
                for i,j in itertools.product(range(5),repeat=2)),'candidate dimension equations')
            candidates.append({'noninvertibles_are_dual_pair':paired,'a':a,'b':6-a,'tensor':R,
                'all125_coefficients_equal_known_Izumi_equivariantization':R==known})
    need(raw==[[False,a]for a in range(7)]+[[True,3]],'complete rank-five tensor domain')
    need(len(candidates)==5 and sum(r['all125_coefficients_equal_known_Izumi_equivariantization']for r in candidates)==1,
        'known based-ring comparison')
    return {'kind':'conditional_full_S3_condensation_and_complete_rank5_based_tensor_domain',
        'required_previous_replay':'c3_morita_dual.py',
        'records':records,'rank_five_candidates_up_to_swapping_noninvertibles':candidates,
        'raw_based_tensor_count':8,'based_tensor_isomorphism_representatives':5,
        'conclusion':'One possible dual based ring has a known realization. No equivalence to that realization, model for439/567, or general exclusion follows.'}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');a=p.parse_args()
    actual=json.loads(json.dumps(run(),default=int));path=HERE/'s3_full_condensation.json'
    if a.write:path.write_text(json.dumps(actual,indent=2)+'\n')
    else:need(actual==json.loads(path.read_text()),'full-S3 conditional receipt changed')
    print('PASS:439/567 conditional full-S3 rank-four module; five complete possible dual based tensors; no categorical identification.')
