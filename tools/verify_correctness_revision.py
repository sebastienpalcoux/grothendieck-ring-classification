#!/usr/bin/env python3
"""Validate the applied correction overlay and current exact publication.

Metadata-only validates source/receipt/document identities and unchanged
partitions. Default additionally recomputes every exact structural flag.
Use the separately named replay commands for mathematical proof executions.
"""
from pathlib import Path
import argparse,contextlib,hashlib,io,json,sys
from correctness_publication import EVIDENCE,DATE,MODELS
from rank12_publication import publication_matches
ROOT=Path(__file__).resolve().parents[1];DIST=ROOT/'site/dist'
def need(c,m):
    if not c:raise ValueError(m)
def read(p):return json.loads(Path(p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main(metadata_only=False):
    manifest=read(ROOT/EVIDENCE/'revision.json')
    need(manifest['schema']=='correctness-revision/v1'and manifest['date']==DATE,'correction release identity')
    need(manifest['classification_status_changes']==[],'this release must not change a decision')
    for rel,h in manifest['files'].items():
        p=ROOT/rel;need(p.resolve().is_relative_to(ROOT)and p.is_file()and publication_matches(rel,h,ROOT),'Correction source/artifact changed: '+rel)
    for rel,h in manifest['immutable_decisions'].items():need(sha(ROOT/rel)==h,'Classification input or decision changed: '+rel)
    # Frozen proof inputs and corrected reusable copies have separate identities.
    # Neither a new publication manifest nor a cache correction may relax them.
    for entry in read(ROOT/EVIDENCE/'frozen-source-overlays.json'):
        need(sha(ROOT/entry['historical_path'])==entry['historical_sha256'],'Frozen source context changed: '+entry['historical_path'])
        need(sha(ROOT/entry['corrected_path'])==entry['corrected_sha256'],'Corrected source overlay changed: '+entry['corrected_path'])
    for rid in ('R7_5_3895','R7_5_5039'):
        proof=read(ROOT/f'evidence/rank7_m5_20261020/accepted/{rid}_cyclic_rotation_certificate.json')
        for rel,h in proof['proof_inputs'].items():need(sha(ROOT/rel)==h,'Cyclic-rotation proof input changed: '+rel)
    validated={}
    for label,entry in manifest['validation'].items():
        value=read(ROOT/entry['path']);need(sha(ROOT/entry['path'])==entry['sha256'],'Validation identity: '+label)
        need(value.get('status')=='PASS' or value.get('passed')is True,'Incomplete correction validation: '+label)
        validated[label]=value
    need({'models','kernels','guards','rank6','rank9','immutable-m9','baseline','pdf-layout','documentation-overlays','publication'}<=set(validated),'Missing correction replay component')
    need(len(validated['models']['runs'])==17 and validated['models']['normal_and_optimized_semantics_agree'],'Incomplete exact model repairs')
    r6=validated['rank6']
    need(r6['original_raw_rows']==r6['effective_exclusions']==25362 and r6['complete_reference_backend_retries']==7 and r6['immutable_source_completions']==11 and r6['all_source_states_fixed'],'Incomplete rank-six composite')
    need(validated['immutable-m9']['count']==len(validated['immutable-m9']['ids'])==11,'Incomplete immutable proof inventory')
    need(validated['rank9']['partition']=={'excluded':2043,'unitarily_realized':36,'unresolved':4} and len(validated['rank9']['stages'])==5,'Incomplete all-phase rank-nine route')
    artifacts=read(ROOT/EVIDENCE/'validation/artifact-index.json')['files']
    need(artifacts['rank6/original-results.jsonl']['sha256']==r6['original_results_sha256']==artifacts['rank6-original-invocation/original-results.jsonl']['sha256'],'Complete raw stream not preserved')
    public=read(ROOT/'data/correctness_revision.json')
    for key in ('replay_archive','original_audit_archive'):
        entry=public[key];need(sha(DIST/entry['path'])==entry['sha256'],'Replay archive identity: '+key)
    from current_publication import validate_documents
    validate_documents(ROOT,check_web=True)
    # This unchanged transition checker retains its complete old source/ledger
    # checks. Only its current-document date accepts the new dated edition.
    from verify_research_revision import main as predecessor_metadata
    with contextlib.redirect_stdout(io.StringIO()):predecessor_metadata(metadata_only=True)
    sys.path.insert(0,str(ROOT/'site'))
    from build_ring_properties import SOURCES,derive
    all_records={}
    for name in SOURCES:
        value=read(DIST/'data'/name)
        for r in value.get('records',value.get('cases',[])):all_records[r['id']]=r
    index=read(DIST/'data/ring_properties.json')
    for rid,record in all_records.items():
        tensor=record.get('fusion_tensor',record.get('tensor'))
        h=hashlib.sha256(json.dumps(tensor,separators=(',',':')).encode()).hexdigest()
        need(index['records'][rid]['tensor_sha256']==h,'property tensor identity: '+rid)
        if not metadata_only:
            expected=derive(tensor);entry=index['records'][rid]
            need(entry['properties']==expected['properties']and entry['certificate']==expected['certificate'],'exact structural properties: '+rid)
    realized=read(DIST/'data/realized_rings.json')['records'];realized={r['id']:r for r in realized}
    for rid,(note,_)in MODELS.items():need(realized[rid]['construction_proof_file']==EVIDENCE+'/'+note,'current model proof pointer: '+rid)
    need((ROOT/'data/correctness_revision.json').read_bytes()==(DIST/'data/correctness_revision.json').read_bytes(),'web correction summary')
    for prefix in ('site/dist/data/',):
        replacements=read(ROOT/EVIDENCE/'derived_publication_replacements.json')
        for name,entry in replacements['files'].items():need(name.startswith(prefix)and publication_matches(name,entry['after_sha256'],ROOT),'derived publication identity: '+name)
    from frontier_20261027 import active as latest_active
    if latest_active(ROOT):
        from verify_frontier_20261027 import main as verify_latest
        verify_latest(metadata_only=True)
    print(json.dumps({'status':'METADATA_PASS'if metadata_only else'PASS','date':DATE,'scope':'Preserved proof/code correction identities and receipts, current documents and structural properties; the separately accepted latest transition is checked independently. Mathematical replay scope is specified by each receipt.','exact_properties_recomputed':not metadata_only,'individual_record_count':len(all_records),'historical_correction_status_changes':0,'latest_status_changes':3 if latest_active(ROOT)else 0,'current_open_cases':len(read(ROOT/'data/current_publication_revision.json')['remaining_ids']),'correction_manifest_sha256':sha(ROOT/EVIDENCE/'revision.json')},indent=2))
if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--metadata-only',action='store_true');a=ap.parse_args();main(a.metadata_only)
