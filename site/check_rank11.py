#!/usr/bin/env python3
"""Check the complete source-bound rank-eleven publication and every download."""
import ast,hashlib,json,zipfile
from collections import Counter
from pathlib import Path
from check_cases import check_tensor,check_browser_integers

ROOT=Path(__file__).resolve().parent.parent;DIST=ROOT/'site/dist'
def require(test,message):
    if not test:raise ValueError(message)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def check():
    data=json.loads((DIST/'data/rank11_m1.json').read_text());summary=data['summary']
    receipt=json.loads((DIST/'data/rank11_m1_build.json').read_text())
    source=ROOT/summary['release'];base=source/'work/rank11'
    ledger=json.loads((base/'ledger.json').read_text());rows=data['cases']
    expected={f'R11_1_{i}' for i in range(1,183)}
    require(len(rows)==182 and {r['id'] for r in rows}==expected,'Incomplete rank-eleven cases')
    require([r['id'] for r in rows]==[f'R11_1_{i}' for i in range(1,183)],'Physical input order changed')
    require(dict(Counter(r['status'] for r in rows))=={'unitarily_realized':27,'excluded':155},'Wrong classification partition')
    require(summary['totals']==ledger['counts'] and summary['remaining_ids']==[],'Ledger/summary differs')
    require(sha(base/'ledger.json')==summary['ledger_sha256']==receipt['ledger_sha256'],'Stale ledger binding')
    check_browser_integers(data,'rank11_m1')
    original={r['id']:r for r in ledger['records']}
    evidence={}
    for ring in rows:
        check_tensor(ring,DIST,require_character_presentation=False)
        tensor=ast.literal_eval((DIST/'downloads/fusion-tensors'/(ring['id']+'.txt')).read_text())
        require(tensor==ring['fusion_tensor'],'Wrong downloadable tensor: '+ring['id'])
        require(hashlib.sha256(json.dumps(tensor,separators=(',',':')).encode()).hexdigest()==original[ring['id']]['tensor_sha256_compact_json']==ring['tensor_sha256'],'Tensor identity changed')
        require(ring['status']==original[ring['id']]['status'],'Published status changed')
        require(ring['research'][0]['data']==original[ring['id']],'Published proof receipt differs')
        require(not ring['investigation_deferred'] and ring['evidence'] and ring['summary'],'Incomplete result')
        wanted='realized' if ring['status']=='unitarily_realized' else 'excluded'
        require(set(ring['categorification_scope']['level_status'].values())=={wanted},'Wrong general/unitary scope')
        for item in ring['evidence']:evidence[item['path']]=item
    for path,item in evidence.items():require(sha(ROOT/path)==item['sha256'],'Missing or changed evidence: '+path)
    for path,digest in receipt['legacy_sha256'].items():require(sha(ROOT/path)==digest,'Older ledger changed: '+path)
    canonical=ROOT/'publications/rank11/paper/rank11.pdf'
    require(canonical.read_bytes()==(DIST/'papers/rank11.pdf').read_bytes(),'Website manuscript is not canonical')
    manifest=json.loads((ROOT/'data/current_publication_revision.json').read_text())
    new_document_paths={p.relative_to(ROOT).as_posix() for folder in ('publications/rank9-rank10','publications/rank11')
                        for p in (ROOT/folder).rglob('*') if p.is_file() and p.suffix in ('.tex','.pdf')}
    declared_new={p for p in manifest['documents'] if p.startswith(('publications/rank9-rank10/','publications/rank11/'))}
    require(new_document_paths==declared_new,'Incomplete high-rank manuscript inventory')
    for path in declared_new:
        require(sha(ROOT/path)==manifest['documents'][path]['sha256'],'Manuscript source hash: '+path)
    require(manifest['web_copies']['papers/rank11.pdf']=='publications/rank11/paper/rank11.pdf','Missing current manuscript selection')
    require(manifest['documents']['publications/rank11/paper/rank11.pdf']['sha256']==sha(canonical),'Wrong current manuscript hash')
    archive=DIST/'downloads/Rank11_Multiplicity1_2026-10-23.zip'
    require(summary['archive']['sha256']==sha(archive),'Wrong verification archive hash')
    with zipfile.ZipFile(archive) as z:
        require(z.testzip() is None,'Corrupt verification archive')
        prefix='rank11_m1_20261023/'
        for line in z.read(prefix+'SHA256SUMS').decode().splitlines():
            digest,path=line.split('  ',1)
            require(hashlib.sha256(z.read(prefix+path)).hexdigest()==digest,'Archived member changed: '+path)
    for name in ('index.html','case.html','unresolved.html','rank11.html'):
        require('src="./rank11.js' in (DIST/name).read_text(),'Missing rank-eleven integration: '+name)
    print('Rank eleven: all 182 case records/tensors, 155 general exclusions, 27 unitary models; all evidence hashes and archived files verified.')

if __name__=='__main__':check()
