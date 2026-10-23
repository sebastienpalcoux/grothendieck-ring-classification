#!/usr/bin/env python3
"""Replay accepted R8_1_29 exclusion and explicit rank-eleven embeddings.

The categorical theorem is retained verbatim in prior_evidence. Its source
verifier checks its finite hypotheses. Embedding checks cover all 8^3 fusion
coefficients plus product and dual closure, without searching model catalogues.
"""
import hashlib
import importlib.util
import itertools
import json
from support import OUT, load, require, sha
from verify_baseline import embedded

def main():
    data=json.loads((OUT/'inherited_solvability.json').read_text())
    source=OUT/'prior_evidence/solvable_r29_certificate.json'
    proof=OUT/'prior_evidence/solvable_proofs.tex'
    verifier=OUT/'prior_evidence/verify_solvable_r29.py'
    for p,key in [(source,'source_record_sha256'),(proof,'source_proof_sha256'),(verifier,'source_verifier_sha256')]:
        require(hashlib.sha256(p.read_bytes()).hexdigest()==data[key],'accepted source hash: '+p.name)
    spec=importlib.util.spec_from_file_location('rank8_solvable_r29',verifier)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    source_record=json.loads(source.read_text());audit=module.verify_record(source_record)
    require(audit==data['source_audit'],'accepted source finite-hypothesis audit')
    S=source_record['tensor'];inputs={r['id']:r for r in load()};ids=[];count=0
    require(len(data['records'])==6,'six inherited exclusions')
    for row in data['records']:
        require(row['id'] not in ids,'unique ID');ids.append(row['id']);r=inputs[row['id']]
        require(r['tensor_sha256']==row['tensor_sha256'],'rank-eleven source hash')
        require(row['certificates'],'explicit inherited certificate')
        for c in row['certificates']:
            require(c['kind']=='accepted_excluded_subring' and c['source_id']=='R8_1_29' and c['subrank']==8,'accepted source criterion')
            require(c['source_tensor_sha256']==sha(S),'accepted source tensor hash')
            T=embedded(r['tensor'],c['subset']);p=c['basis_map_subring_to_source']
            require(len(T)==8 and p[0]==0 and sorted(p)==list(range(8)),'basis bijection')
            require(all(T[i][j][k]==S[p[i]][p[j]][p[k]] for i,j,k in itertools.product(range(8),repeat=3)),'all source embedding coefficients')
            count+=1
        print(row['id'],'PASS',flush=True)
    require(ids==data['excluded_ids'],'inherited exclusion inventory')
    report=dict(status='PASS',excluded_ids=ids,embedding_count=count,source_audit=audit)
    (OUT/'inherited_solvability_replay.json').write_text(json.dumps(report,indent=2)+'\n')
    print('COMPLETE',len(ids),'inherited exclusions')

if __name__=='__main__':main()
