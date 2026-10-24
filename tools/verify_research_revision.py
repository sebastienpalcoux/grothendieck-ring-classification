#!/usr/bin/env python3
"""Check current audit correction, documents, downloads and exact property data.

This is publication validation and exact ring arithmetic, not a fresh replay of
all categorical exclusions or a proof of external categorical hypotheses.
"""
from pathlib import Path
from collections import Counter
import ast,csv,hashlib,json,re,sys
ROOT=Path(__file__).resolve().parents[1];DIST=ROOT/'site/dist'
sys.path.insert(0,str(ROOT/'site'))
from research_continuation_20261024 import validate,LEDGER,replay
from current_frontier import identifiers
from build_ring_properties import derive,SOURCES

def need(x,message):
 if not x:raise ValueError(message)
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def documents():
 for name in ('current_document_revision.json','current_publication_revision.json'):
  data=read(ROOT/'data'/name)
  need(data['date']=='2026-10-24','Stale current document date')
  for source,item in data['documents'].items():
   p=ROOT/source;need(sha(p)==item['sha256']and p.stat().st_size==item['bytes'],'Document identity: '+source)
   if source.startswith('manuscripts/'):
    mirror=source.replace('manuscripts/','supplements/',1)
    if mirror in data['documents']:need(data['documents'][mirror]==item,'Supplement mirror: '+mirror)
  for web,source in data['web_copies'].items():need((DIST/web).read_bytes()==(ROOT/source).read_bytes(),'Canonical PDF copy: '+web)
  need((ROOT/'data'/name).read_bytes()==(DIST/'data'/name).read_bytes(),'Web document manifest: '+name)
 return True

def main(metadata_only=False):
 report=validate(ROOT);need(documents(),'Document validation')
 ids=identifiers(ROOT);revision=read(ROOT/'data/current_publication_revision.json')
 need(len(ids)==11 and revision['remaining_ids']==ids and revision['current_unresolved_total']==11,'Global accepted-ledger frontier')
 module=ast.parse((ROOT/'data/current_remaining_cases.py').read_text());constants={n.targets[0].id:ast.literal_eval(n.value)for n in module.body if isinstance(n,ast.Assign)}
 need(set(constants['TENSORS'])==set(ids),'Current open-tensor inventory')
 all_records={};index=read(DIST/'data/ring_properties.json')
 for name in SOURCES:
  p=DIST/'data'/name;need(index['source_sha256'][name]==sha(p),'Property source binding: '+name)
  data=read(p)
  for r in data.get('records',data.get('cases',[])):all_records[r['id']]=r
 need(set(index['records'])==set(all_records),'Exact property coverage')
 flags=read(DIST/'data/ring_property_flags.json');need(flags['source_sha256']==index['source_sha256']and flags['records']=={rid:{'tensor_sha256':r['tensor_sha256'],'properties':r['properties']}for rid,r in index['records'].items()},'Browser/exact property projection')
 for i,(rid,r)in enumerate(all_records.items()):
  tensor=r.get('fusion_tensor',r.get('tensor'));entry=index['records'][rid]
  need(hashlib.sha256(json.dumps(tensor,separators=(',',':')).encode()).hexdigest()==entry['tensor_sha256'],'Property tensor binding: '+rid)
  if not metadata_only:
   expected=derive(tensor);need(entry['properties']==expected['properties']and entry['certificate']==expected['certificate'],'Exact ring properties: '+rid)
  if i and i%500==0:print('Recomputed exact properties:',i,flush=True)
 opened={rid:r for rid,r in all_records.items()if r.get('status')=='unresolved'}
 need(set(opened)==set(ids),'Catalogue/global frontier')
 r=all_records['R8_3_436'];need(r['existence']=={'general':'excluded','unitary':'excluded'},'R436 scope')
 need(r['categorification_scope']['level_status']['unitary']=='excluded'and r['categorification_scope']['level_status']['general']=='excluded','R436 structure levels')
 for rid,tensor in constants['TENSORS'].items():need(tensor==opened[rid]['fusion_tensor'],'Open-tensor download: '+rid)
 need((ROOT/'data/current_remaining_cases.py').read_bytes()==(DIST/'downloads/current_remaining_cases.py').read_bytes(),'Current open download copy')
 status=read(ROOT/'data/classification_status.json');rank8=[r for r in status['rows']if r['rank']==8]
 need(sum(r['excluded_general']for r in rank8)==4403 and sum(r['unresolved_general']for r in rank8)==4,'Exported rank-eight partition')
 realized=read(ROOT/'data/grothendieck_counts.json')['rows']
 need(len(realized)==len(status['rows']),'Realized-count band coverage')
 for count,band in zip(realized,status['rows']):
  need((count['rank'],count['multiplicity'])==(band['rank'],band['multiplicity']),'Realized-count band order')
  need(count['unresolved_general']==band['unresolved_general'] and count['unassessed']==band['unassessed'],'Realized-count open partition')
  expected=sum(band[k]for k in ('realized_unitary','realized_other_or_unspecified','realized_spherical_nonpseudounitary'))
  relation='unknown'if band['classification_coverage']=='census_only'else'lower_bound'if band['unresolved_general']or band['unassessed']else'exact'
  need(count['known_realized']==expected and count['count_relation']==relation,'Realized-count interpretation')
 with (ROOT/'data/grothendieck_counts.csv').open(newline='')as stream:
  exported=list(csv.DictReader(stream))
 need(exported==[{k:str(v)for k,v in row.items()}for row in realized],'Realized-count CSV projection')
 for name in ('grothendieck_counts.json','classification_status.json','classification_status.csv'):
  need((ROOT/'data'/name).read_bytes()==(DIST/'data'/name).read_bytes(),'Published count copy: '+name)
 need(f'All {len(ids)} open rings · Python tensors'in(DIST/'index.html').read_text(),'Open-tensor download label')
 with (DIST/'data/grothendieck_counts.csv').open(newline='')as stream:
  web_counts=list(csv.DictReader(stream))
 expected_counts=[{'rank':str(row['rank']),'multiplicity':str(row['multiplicity']),'rings':str(row['known_realized']),'is_lower_bound':str(row['count_relation']=='lower_bound')}for row in realized if row['known_realized']]
 need(web_counts==expected_counts,'Legacy website CSV count projection')
 pages=read(ROOT/'data/current_manuscript_page_counts.json');totals=pages['totals'];manuscripts=(ROOT/'manuscripts/README.md').read_text()
 need(f"{pages['document_counts']['mathematical_manuscripts']} mathematical manuscripts, {totals['mathematical_manuscript']} pages"in manuscripts,'Manuscript index mathematical page total')
 need(f"With three verification guides: {totals['mathematical_manuscripts_and_guides']} pages"in manuscripts and f"With the current research-status report: {totals['all_distinct_documents']} pages"in manuscripts,'Manuscript index complete page totals')
 need(f'Current classification through rank eleven: {len(ids)} unresolved rings'in manuscripts,'Manuscript index global frontier')


 for name in ('rank5/papers/automatic.tex','rank5/papers/verification_guide.tex','rank7/papers/manuscript.tex','rank8/paper/m3_frontier.tex','rank8/paper/m3_center_followup.tex'):
  need((ROOT/'manuscripts'/name).read_bytes()==(ROOT/'supplements'/name).read_bytes(),'Current TeX mirror: '+name)
 checks=[] if metadata_only else replay(ROOT)
 result={'new_mathematical_replays':checks,'status':'METADATA_PASS'if metadata_only else 'PASS','exact_properties_recomputed':not metadata_only,'scope':'Current publication, exact ring properties, accepted transition reconciliation, and the stated new finite replays; no independent human or formal categorical verification.','current_open_cases':len(ids),'exact_property_records':len(all_records),'rank8':report}
 print(json.dumps(result,indent=2))
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--metadata-only',action='store_true');args=p.parse_args();main(args.metadata_only)
