"""Verify final D48 ledger and frozen proof/evidence bindings.

Pass --full to rerun both complete quotient reconstructions. The default
checks all source tensors and all56 branches plus frozen evidence hashes.
"""
from quotient_reconstruct import *
import sys

def main():
    if '--full' in sys.argv:
        import quotient_reconstruct,rank9_reconstruct
        quotient_reconstruct.main();rank9_reconstruct.main()
    result=json.loads((OUT/'results.json').read_text())
    manifest=json.loads((OUT/'accepted_manifest.json').read_text())
    require(result['status']==manifest['status']=='PASS','accepted status')
    require(result['new_exclusions']==IDS and not result['new_models'] and not result['remaining_unresolved'],'all20 source decisions')
    require(result['counts']==dict(new_exclusions=20,new_models=0,remaining_unresolved=0),'final counts')
    rows=source_branches();quot=json.loads((OUT/'quotient_reconstruction.json').read_text());rank9=json.loads((OUT/'rank9_reconstruction.json').read_text())
    require(quot['status']==rank9['status']=='PASS','complete reconstruction receipts')
    require(len(rows)==20 and sum(len(r['branches'])for r in rows)==56,'all20 sources/all56 involutions')
    qrows={r['id']:r for r in quot['source_binding']};ledger={r['id']:r for r in result['records']}
    r9={(r['id'],r['involution']):r for r in rank9['source_binding']}
    counts=collections.Counter()
    for row in rows:
        require(row['sha256']==ledger[row['id']]['source_sha256'],'decision source hash')
        require([b['involution']for b in row['branches']]==[b['involution']for b in ledger[row['id']]['branches']],'no omitted branch')
        qr={b['involution']:b for b in qrows[row['id']]['branches']}
        for b in row['branches']:
            saved=qr[b['involution']];counts[b['case']]+=1
            require(b['quotient_tensor']==saved['quotient_tensor'] and b['source_orbits']==saved['source_orbits'],'full orbit tensor binding')
            if b['case']=='rank12_m1_dimension24':require(set(saved['target_ids'])<={'R12_1_351','R12_1_513'} and saved['target_ids'],'rank12 closure')
            if b['case']=='rank9_dimension24_type_1_4_2_5':
                rr=r9[row['id'],b['involution']]
                require(rr['source_hash']==row['sha256'],'rank9 source binding')
                for rec in rank9['reconstruction_classes'][rr['reconstruction_class']]['reconstructions']:
                    require(rec['adjoint_closure']==list(range(9)) and rec['pointed_deequivariantization_dimension']==12,'rank9 categorical premise')
    for e in manifest['accepted_evidence']:
        require(hashlib.sha256((OUT/e['path']).read_bytes()).hexdigest()==e['sha256'],'accepted evidence hash '+e['path'])
    answer=dict(status='PASS',source_rings=20,central_involution_branches=56,branch_counts=dict(counts),new_exclusions=20,new_models=0,remaining_unresolved=0,full_reconstruction_replayed='--full'in sys.argv)
    (OUT/'verification_receipt.json').write_text(json.dumps(answer,indent=2)+'\n');print(json.dumps(answer))
if __name__=='__main__':main()
