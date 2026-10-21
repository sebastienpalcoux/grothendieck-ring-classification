#!/usr/bin/env python3
"""Bind new model-route tensors to the frozen exact rank-five replay archive."""
from pathlib import Path
import argparse
import hashlib
import itertools
import json
import subprocess
import sys
import tempfile
import zipfile
from s3_full_condensation import rank5

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[2]
ARCHIVE=REPO/'evidence/prepublication_20261017/rank5/rank5_current_replay.zip'
ARCHIVE_SHA='264fd1b7f1851cbce142ea248a19bc2d0196ba44f350b2f5852e1e77a647a92d'


def need(c,m):
    if not c:raise ValueError(m)


def digest(R):return hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()


def permute(R,p):return [[[R[p[i]][p[j]][p[k]]for k in range(5)]for j in range(5)]for i in range(5)]


def canonical(R):
    return min(tuple(v for M in permute(R,(0,)+p)for row in M for v in row)
        for p in itertools.permutations(range(1,5)))


def near_group(cyclic):
    R=[[[0]*5 for _ in range(5)]for _ in range(5)]
    for g,h in itertools.product(range(4),repeat=2):R[g][h][(g+h)%4 if cyclic else g^h]=1
    for g in range(4):R[g][4][4]=R[4][g][4]=1
    R[4][4]=[1,1,1,1,16]
    return R


def run():
    need(hashlib.sha256(ARCHIVE.read_bytes()).hexdigest()==ARCHIVE_SHA,'frozen rank-five archive changed')
    specs=[('NG_C4_m16',near_group(True)),('NG_V4_m16',near_group(False))]
    specs += [(f'S3_dual_selfdual_a{a}',rank5(False,a))for a in range(4)]
    specs += [('S3_dual_pair_a3',rank5(True,3))]
    targets={canonical(R):name for name,R in specs}
    need(len(targets)==7,'distinct target tensor classes')
    with zipfile.ZipFile(ARCHIVE)as z:
        paths=z.namelist()
        prefix=next(n.rsplit('data/current/classification_tensors.json',1)[0]for n in paths
            if n.endswith('data/current/classification_tensors.json'))
        rows=json.loads(z.read(prefix+'data/current/classification_tensors.json'))
        exclusions=json.loads(z.read(prefix+'data/current/exclusions.json'))
        positives=json.loads(z.read(prefix+'data/positive_models.json'))
        selected={}
        for row in rows:
            if row['m']not in [3,4,5,6,16]:continue
            R=row['N']
            # All targets have a nontrivial invertible and at least rank-three
            # proper integral support; only the multiplicity bound is needed
            # for completeness, so no heuristic profile filter is imposed.
            can=canonical(R)
            if can in targets:
                need(targets[can]not in selected,'duplicate source class')
                selected[targets[can]]=row
        need(len(selected)==7,'missing exact source tensors')
        records=[];verification=[]
        for name,R in specs:
            row=selected[name];source=row['N'];sha=digest(source)
            mapping=next((0,)+p for p in itertools.permutations(range(1,5))if permute(R,(0,)+p)==source)
            certificate=exclusions.get(sha)
            positive=next((p['name']for p in positives if canonical(p['tensor'])==canonical(R)),None)
            need((certificate is None)!=(positive is None),'classification partition')
            record={'route_tensor':name,'constructor_tensor':R,
                'constructor_sha256':digest(R),'rank5_source_id':f"R5_{row['m']}_{row['j']}",
                'rank5_source_tensor':source,'rank5_source_sha256':sha,
                'basis_map_source_to_constructor':list(mapping),'fusion_coefficients_matched':125,
                'status':'general_complex_excluded'if certificate else'known_unitary_based_ring',
                'certificate':certificate,'known_model_name':positive}
            records.append(record)
            if certificate:verification.append({'name':name,'tensor':source,'certificate':certificate})
        with tempfile.TemporaryDirectory(prefix='rank5-route-replay-')as tmp:
            folder=Path(tmp)
            for n in paths:
                if n.startswith(prefix+'software/')and not n.endswith('/'):
                    (folder/Path(n).name).write_bytes(z.read(n))
            worker="import json,sys;sys.path.insert(0,sys.argv[1]);from unified import verify\nfor r in json.load(sys.stdin):\n verify(r['tensor'],r['certificate'])\n print('PASS',r['name'],flush=True)"
            cmd=[sys.executable]+(['-O']if sys.flags.optimize else[])+['-c',worker,str(folder)]
            replay=subprocess.run(cmd,input=json.dumps(verification),capture_output=True,text=True,check=True)
            need(len(replay.stdout.splitlines())==len(verification),'not all frozen proofs replayed')
    need(all(r['status']=='general_complex_excluded'for r in records if r['route_tensor'].startswith('NG_')),
        'near-group route not excluded')
    need(sum(r['status']=='known_unitary_based_ring'for r in records)==1,'rank-five positive alternative count')
    return {'kind':'fresh_frozen_rank5_certificate_binding_for_model_routes',
        'archive':str(ARCHIVE.relative_to(REPO)),'archive_sha256':ARCHIVE_SHA,
        'verified_general_exclusion_count':len(verification),'records':records,
        'conclusion':'Both order-four multiplicity16 near-group categories are impossible over C. In the conditional full-S3 rank-five branch only the known self-dual a=b=3 based ring remains; its associator is not identified.'}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');a=p.parse_args()
    actual=run();path=HERE/'rank5_route_bindings.json'
    if a.write:path.write_text(json.dumps(actual,indent=2)+'\n')
    else:need(actual==json.loads(path.read_text()),'rank-five route bindings changed')
    print('PASS: seven full125 rank-five tensor bindings; six frozen general exclusions freshly replayed; one possible known based ring remains.')
