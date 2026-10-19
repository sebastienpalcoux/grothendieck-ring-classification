"""Assemble the current rank-seven ledger while preserving all M<=4 records."""
import collections,gzip,hashlib,json
from pathlib import Path
P=Path(__file__).resolve().parents[1];ROOT=P.parents[1];OUT=P/'output/m5'
def dump(p,obj,indent=None):p.write_text(json.dumps(obj,indent=indent,separators=None if indent else (',',':'))+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    old=json.loads((P/'output/rank7_ledger_through_m4.json').read_text())
    new=json.loads((OUT/'ledger.json').read_text())
    byid={r['id']:r for r in new}
    for a in json.loads((OUT/'additions.json').read_text()):
        if byid[a['id']]['status']=='unresolved':byid[a['id']].update(a)
    for r in new:
        if r['status']=='excluded':r['existence']={k:'no' for k in ('general','pivotal','spherical','pseudo_unitary','unitary')}
        elif r['status']=='unresolved':
            r['existence']={k:'unknown' for k in ('general','pivotal','spherical','pseudo_unitary','unitary')}
            r['diagnostic']='No general exclusion or complete categorical model has been certified. Failed searches and exhausted budgets are not nonexistence certificates.'
    allrows=old+new;dump(P/'output/rank7_ledger.json',allrows);dump(OUT/'ledger.json',new);dump(OUT/'survivors.json',[r for r in new if r['status']=='unresolved'])
    oldsummary=P/'output/rank7_summary_through_m4.json'
    if not oldsummary.exists():oldsummary.write_bytes((P/'output/rank7_summary.json').read_bytes())
    summary=json.loads(oldsummary.read_text());source=P/'provenance/rank7_M5_verified/FusionRingMultiplicationTables.txt.gz'
    oldbytes=gzip.decompress((P/'data/rank7_tables_through_m4.txt.gz').read_bytes())
    newbytes=[]
    for line in gzip.decompress(source.read_bytes()).splitlines(keepends=True):
        R=json.loads(line.decode().replace('{','[').replace('}',']'))
        if max(x for A in R for row in A for x in row)==5:newbytes.append(line)
    packed=P/'data/rank7_tables.txt.gz';packed.write_bytes(gzip.compress(oldbytes+b''.join(newbytes),mtime=0))
    summary['historical_source']={'source_sha256':summary['source_sha256'],'source_commit':summary['source_commit'],'path':'data/rank7_tables_through_m4.txt.gz'}
    summary.update(source_sha256=sha(packed),source_commit='4e81914a6772ccd5aa2a2b5fe1b6e2cd06e2d700',max_multiplicity=5)
    summary['new_source']={'path':'provenance/rank7_M5_verified/FusionRingMultiplicationTables.txt.gz','sha256':sha(source),'source_commit':summary['source_commit'],'uploaded_complete_census_claim':True,'independent_full_enumeration_recomputed':False,'coverage':'All 5805 supplied exact-multiplicity-five representatives classified to the recorded scope.'}
    summary['ring_counts']['5']=5805;summary['status_counts']['5']=dict(collections.Counter(r['status'] for r in new))
    stagecounts=collections.Counter(r['criterion'] for r in new if r['status']=='excluded')
    for criterion,count in stagecounts.items():
        if criterion not in summary['stage_order']:summary['stage_order'].append(criterion)
        summary['stage_counts'].setdefault(criterion,{})['5']=count
    summary['model_count']=sum(r['status']=='unitarily_realized' for r in allrows)
    summary['notes']='All earlier 4201 decision records are preserved exactly. New-band exclusions have checked exact certificates with stated categorical scope; unresolved records remain open. Source completeness is producer-reported, not independently re-enumerated in this continuation.'
    summary['multiplicity5_update']='evidence/rank7_m5_20261019/README.md';dump(P/'output/rank7_summary.json',summary,2)
    catalogpath=P/'output/rank7_model_catalog.json';catalog=json.loads((P/'data/model_catalog.json').read_text());catalog=[r for r in catalog if r['id']!='R7_5_5678']
    receipt=json.loads((ROOT/'evidence/rank7_m5_20261019/models/frobenius42_match.json').read_text());model=byid['R7_5_5678']
    catalog.append({'id':model['id'],'rank':7,'multiplicity':5,'name':receipt['model'],'source_construction':receipt['presentation'],'source_reference':receipt['primary_reference'],'source_url':receipt['primary_url'],'basis_permutation_model_to_census':receipt['match']['basis_permutation_model_to_census'],'tensor':model['tensor'],'existence':model['existence'],'verification':'evidence/rank7_m5_20261019/models/verify_frobenius42.py'})
    if {r['id'] for r in catalog}!={r['id'] for r in allrows if r['status']=='unitarily_realized'}:raise ValueError('model catalogue does not cover every realized ledger ID')
    dump(catalogpath,catalog,2);(P/'data/model_catalog.json').write_bytes(catalogpath.read_bytes())
    report={'new_rings':5805,'new_status_counts':summary['status_counts']['5'],'new_criterion_counts':dict(stagecounts),'unresolved_ids':[r['id'] for r in new if r['status']=='unresolved'],'old_records_preserved':4201,'total_rings':10006,'source_sha256':sha(source),'ledger_sha256':sha(P/'output/rank7_ledger.json'),'scope':'All complex fusion categories unless explicitly labeled otherwise; unresolved means no complete negative or positive conclusion.'}
    dump(OUT/'summary.json',report,2);print(json.dumps(report,indent=2))
if __name__=='__main__':main()
