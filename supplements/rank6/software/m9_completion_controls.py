"""Reject corrupted completion proof inputs and stale source-bound receipts."""
import copy
import json
from pathlib import Path
import shutil
import sys
import tempfile
import time
import m9_completion as proof

def main():
    start=time.monotonic();root=proof.ROOT
    rows=json.loads((root/'data/census.json').read_text())
    records=[json.loads(line) for line in (root/'certificates/m9_completion.jsonl').read_text().splitlines()]
    receipt=json.loads((root/'verification/m9/completion/replay_optimized.json').read_text())
    proof.validate_receipt(rows,records,receipt)
    row=next(r for r in rows if r['id']=='R6_9_1060')
    certificate=next(r['certificate'] for r in records if r['id']==row['id'])
    results=[]
    def rejected(name,operation):
        try:operation()
        except ValueError as error:results.append({'control':name,'rejected':True,'reason':str(error)})
        else:raise ValueError('negative control accepted: '+name)
    bad_tensor=copy.deepcopy(row['N']);bad_tensor[1][1][1]+=2
    rejected('altered_tensor',lambda:proof.validate_certificate(bad_tensor,certificate))
    bad=copy.deepcopy(certificate);bad['bundles']={}
    rejected('omitted_required_proof_bundle',lambda:proof.validate_certificate(row['N'],bad))
    bad=copy.deepcopy(certificate);bad['scope']='pseudo_unitary'
    rejected('scope_downgrade',lambda:proof.validate_certificate(row['N'],bad))
    for name,mutate in [
        ('incomplete_receipt',lambda r:r.update(complete=False)),
        ('nonoptimized_receipt',lambda r:r.update(optimized_python=False)),
        ('optimizer_not_disabled',lambda r:r.update(optimizer_disabled=False)),
        ('stale_checker_receipt',lambda r:r.update(checker_sha256='0'*64)),
        ('stale_proof_receipt',lambda r:r.update(proof_manifest_sha256='0'*64)),
        ('missing_bundle_replay',lambda r:r['bundles'].pop('case8785')),
        ('missing_child_checker',lambda r:r['bundles']['case8785']['runs'].pop()),
        ('duplicate_case_replay',lambda r:r['results'].__setitem__(0,copy.deepcopy(r['results'][1]))),
        ('altered_tensor_receipt',lambda r:r['results'][0].update(tensor_sha256='0'*64)),
        ('failed_finite_replay',lambda r:r['bundles']['involution_pair'].update(passed=False)),
    ]:
        altered=copy.deepcopy(receipt);mutate(altered)
        rejected(name,lambda altered=altered:proof.validate_receipt(rows,records,altered))
    manifest=proof.validate_manifest()
    with tempfile.TemporaryDirectory(prefix='m9_completion_controls_') as folder:
        temporary=Path(folder)
        files={proof.MANIFEST,'data/census.json','certificates/m9_completion.jsonl',*manifest['checker_files']}
        for bundle in manifest['bundles'].values():files.update(bundle['files'])
        for relative in files:
            destination=temporary/relative;destination.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(root/relative,destination)
        proof.validate_manifest(temporary)
        for name,relative in [
            ('altered_proof_text',proof.BASE+'/free_involution/PROOF.txt'),
            ('altered_integer_ray',proof.BASE+'/free_involution/certificate.json'),
            ('altered_checker_source','software/m9_completion.py'),
            ('altered_native_source',proof.BASE+'/involution_pair/gram_vectors_general.cpp')]:
            path=temporary/relative;original=path.read_bytes();path.write_bytes(original+b'\n ')
            rejected(name,lambda:proof.validate_manifest(temporary))
            path.write_bytes(original)
        path=temporary/proof.BASE/'involution_pair'/'gram_vectors_general'
        path.write_text('unbound executable')
        rejected('unbound_native_binary',lambda:proof.validate_manifest(temporary));path.unlink()
    report={'passed':True,'optimized_python':not __debug__,'count':len(results),'results':results,'seconds':time.monotonic()-start,
            'scope':'Binding and completion controls; exact arithmetic mutation controls are also retained in the proof bundles.'}
    destination=root/'verification/m9/completion'/('negative_controls_optimized.json' if not __debug__ else 'negative_controls_normal.json')
    destination.write_text(json.dumps(report,indent=2)+'\n')
    reports=[]
    for mode in ['normal','optimized']:
        path=destination.with_name('negative_controls_'+mode+'.json')
        if path.exists():reports.append(json.loads(path.read_text()))
    aggregate={'complete':len(reports)==2,'passed':len(reports)==2 and all(r['passed'] for r in reports),'modes':reports}
    destination.with_name('negative_controls.json').write_text(json.dumps(aggregate,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
