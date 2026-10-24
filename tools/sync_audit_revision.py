#!/usr/bin/env python3
"""Regenerate the mutable current publication after the 24 October audit.

Old decision ledgers/receipts remain immutable. Derived displays and pointers
are regenerated from the corrected rank-eight ledger and current high ranks.
"""
from pathlib import Path
from collections import Counter
import ast,hashlib,json,re,runpy,shutil,sys
ROOT=Path(__file__).resolve().parents[1];DIST=ROOT/'site/dist';E=ROOT/'evidence/audit_20261024'
sys.path.insert(0,str(ROOT/'site'))
import audit_corrections_20261024 as correction
from rank8_publication import extension
from reader_resources import render_tensors,build_pages

def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def info(p):return{'sha256':sha(p),'bytes':p.stat().st_size}
def main(rebuild_cases=True):
 correction.validate(ROOT);ext=extension(ROOT);rows=read(ROOT/correction.LEDGER)
 # Bind compiled current documents before refreshing their derived displays.
 # The historical base-manifest receipt in the high-rank publication remains
 # a separate archive-context reference, with its original digest and scope.
 low=ROOT/'data/current_document_revision.json';low_revision=read(low)
 for source in low_revision['documents']:low_revision['documents'][source]=info(ROOT/source)
 write(low,low_revision)
 # The active exported partition is derived from the corrected full ledger.
 p=ROOT/'data/classification_status.json';status=read(p)
 band=next(x for x in status['rows']if x['rank']==8 and x['multiplicity']==3)
 band.update(excluded_general=3506,unresolved_general=5,classification_coverage='partial_classification')
 status['inputs']['rank8'].update(file=correction.LEDGER,sha256=sha(ROOT/correction.LEDGER),ledger=correction.LEDGER,status_totals={'excluded':4402,'unitarily_realized':93,'unresolved':5},audit_correction='evidence/audit_20261024/accepted.json')
 from generate_classification import write_export
 write_export(status,ROOT/'data')
 runpy.run_path(str(ROOT/'tools/export_grothendieck_counts.py'),run_name='__main__')
 for csv_path in (ROOT/'data').glob('*.csv'):
  if csv_path.name in ('classification_status.csv','grothendieck_counts.csv'):
   csv_path.write_bytes(csv_path.read_bytes().replace(b'\r\n',b'\n'))
 shutil.copy2(p,DIST/'data/classification_status.json')
 shutil.copy2(ROOT/'data/grothendieck_counts.json',DIST/'data/grothendieck_counts.json')
 if (ROOT/'data/classification_status.csv').exists():shutil.copy2(ROOT/'data/classification_status.csv',DIST/'data/classification_status.csv')
 p=DIST/'data/atlas.json';atlas=read(p);atlas['snapshot']='2026-10-24';atlas['classification_commit']=None;atlas['rank8_m3_update']=ext
 for x in atlas.get('classification_rows',[]):
  if x['rank']==8 and x['multiplicity']==3:x.update(band)
 for x in atlas['scope']:
  if x['rank']==8:x.update(unresolved=5,note='Five general questions remain open; R8_3_436 retains its unitary exclusion.')
 atlas['remaining_ids']=['R6_4_155','R6_8_1660']+correction.REMAINING_IDS
 write(DIST/'data/current_remaining_ids.json',atlas['remaining_ids'])
 atlas['remaining_ids_file']['sha256']=sha(DIST/'data/current_remaining_ids.json')
 # Current low-rank tensor module, still distinct from the complete high-rank download.
 (ROOT/'data/remaining_cases.py').write_text(render_tensors(ROOT));correction.refresh_scope_sources(ROOT);shutil.copy2(ROOT/'data/remaining_cases.py',DIST/'downloads/remaining_cases.py')
 # Current per-ring audit has a new scope; old accepted source manifests are untouched.
 attempt=read(ROOT/correction.AUDIT);attempt['rows']=[r for r in attempt['rows']if r['id']in correction.REMAINING_IDS]
 attempt['display_scope']='Five current rank-eight open cases; complete historical research is preserved separately.'
 write(DIST/'data/rank8_m3_attempts.json',attempt)
 ext['attempts']={'path':'data/rank8_m3_attempts.json','sha256':sha(DIST/'data/rank8_m3_attempts.json'),'cases':5}
 write(DIST/'data/rank8_m3_update.json',ext)
 ext['metadata_path']='data/rank8_m3_update.json';ext['metadata_sha256']=sha(DIST/'data/rank8_m3_update.json')
 atlas['rank8_m3_update']=ext;write(p,atlas)
 # Rebuild the case dossiers from exact tensors, without repeating unrelated searches.
 from build_cases import build
 if rebuild_cases:build(ROOT)
 payloads=[read(DIST/'data/unresolved_cases.json')['cases']]+[read(DIST/'data'/name)['cases']for name in ('rank9_rank10_m1.json','rank11_m1.json','rank9_m2.json')]
 opened={r['id']:r for group in payloads for r in group if r['status']=='unresolved'}
 ids=sorted(opened,key=lambda x:tuple(map(int,re.findall(r'\d+',x))))
 if len(ids)!=26:raise ValueError('Expected 26 current open cases after preserving the rank-nine M2 continuation')
 tensors={rid:opened[rid]['fusion_tensor']for rid in ids};metadata={rid:{'rank':opened[rid]['rank'],'multiplicity':opened[rid]['multiplicity'],'tensor_sha256':opened[rid]['tensor_sha256'],'status':'unresolved'}for rid in ids}
 text='"""All current unresolved fusion tensors. Unit X_0; N[i][j][k].\nGeneral complex categorification remains open for every listed tensor.\n"""\n\nMETADATA = '+repr(metadata)+'\n\nTENSORS = '+repr(tensors)+'\n';ast.parse(text)
 (ROOT/'data/current_remaining_cases.py').write_text(text);shutil.copy2(ROOT/'data/current_remaining_cases.py',DIST/'downloads/current_remaining_cases.py')
 # Retain all current high-rank manuscript selections while refreshing modified sources.
 p=ROOT/'data/current_publication_revision.json';rev=read(p)
 rev.update(date='2026-10-24',remaining_ids=ids,current_unresolved_total=26,rank8_m3_update=extension(ROOT),audit_correction=correction.validate(ROOT))
 for name in rev['documents']:rev['documents'][name]=info(ROOT/name)
 rev['documents']['manuscripts/prepublication-review-2026-10-24.tex']=info(ROOT/'manuscripts/prepublication-review-2026-10-24.tex')
 rev['documents']['manuscripts/prepublication-review-2026-10-24.pdf']=info(ROOT/'manuscripts/prepublication-review-2026-10-24.pdf')
 for web in list(rev['web_copies']):
  if 'prepublication-review-'in web:del rev['web_copies'][web]
 rev['web_copies']['papers/prepublication-review-2026-10-24.pdf']='manuscripts/prepublication-review-2026-10-24.pdf'
 write(p,rev);shutil.copy2(p,DIST/'data/current_publication_revision.json')
 for web,source in rev['web_copies'].items():shutil.copy2(ROOT/source,DIST/web)
 for name in ('rank11_m1.json','rank9_m2.json'):
  p=DIST/'data'/name;data=read(p);data['summary']['current_documents']={'path':'data/current_publication_revision.json','sha256':sha(ROOT/'data/current_publication_revision.json'),'date':'2026-10-24'};p.write_text(json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n')
 # Update both page inventories by actual PDF bytes, keeping their existing scope.
 from pypdf import PdfReader
 for name in ('manuscript_page_counts.json','current_manuscript_page_counts.json'):
  p=ROOT/'data'/name;pages=read(p)
  for x in pages['documents']:
   if x['kind']=='research_status_report':x['path']='manuscripts/prepublication-review-2026-10-24.pdf'
   path=ROOT/x['path'];x.update(info(path),pages=len(PdfReader(path).pages))
  kinds=Counter()
  for x in pages['documents']:kinds[x['kind']]+=x['pages']
  pages['totals'].update(dict(kinds))
  pages['totals']['all_distinct_documents']=sum(kinds.values())
  pages['totals']['mathematical_manuscripts_and_guides']=kinds['mathematical_manuscript']+kinds['verification_guide']
  pages['document_counts']={key:sum(x['kind']==kind for x in pages['documents'])for key,kind in [('mathematical_manuscripts','mathematical_manuscript'),('verification_guides','verification_guide'),('research_status_reports','research_status_report')]}
  write(p,pages);shutil.copy2(p,DIST/'downloads'/name)
 # Refresh reader-resource bindings already exposed in the atlas.
 atlas=read(DIST/'data/atlas.json')
 low=ROOT/'data/current_document_revision.json'
 shutil.copy2(low,DIST/'data/current_document_revision.json')
 atlas['current_documents'].update(date='2026-10-24',sha256=sha(low))
 atlas['reader_resources']['page_totals']=read(ROOT/'data/manuscript_page_counts.json')['totals']
 entry=atlas['rank6_release'].get('document_revision')
 if entry:
  source=ROOT/entry['source'];shutil.copy2(source,DIST/entry['path'])
  if source!=ROOT/entry['path']:shutil.copy2(source,ROOT/entry['path'])
  entry.update(date=read(source)['date'],sha256=sha(source))
 def refresh(value):
  if isinstance(value,dict):
   path=value.get('path')
   if path and isinstance(path,str)and (DIST/path).is_file() and 'sha256'in value:
    value['sha256']=sha(DIST/path)
    if 'bytes'in value:value['bytes']=(DIST/path).stat().st_size
   for child in value.values():refresh(child)
  elif isinstance(value,list):
   for child in value:refresh(child)
 refresh(atlas);write(DIST/'data/atlas.json',atlas)
 shutil.copy2(DIST/'data/atlas.json',ROOT/'data/atlas.json')
 current_pages=read(ROOT/'data/current_manuscript_page_counts.json');totals=current_pages['totals']
 summary=f"{current_pages['document_counts']['mathematical_manuscripts']} mathematical manuscripts: {totals['mathematical_manuscript']} pages; with the three verification guides: {totals['mathematical_manuscripts_and_guides']}; with the current research-status report: {totals['all_distinct_documents']}. Each distinct document is counted once."
 page=DIST/'index.html';page.write_text(re.sub(r'(<span id="manuscript-page-summary">).*?(</span>)',lambda m:m[1]+summary+m[2],page.read_text()))
 from build_ring_properties import build as properties
 properties()
 page=DIST/'index.html';page.write_text(re.sub(r'All \d+ open rings · Python tensors',f'All {len(ids)} open rings · Python tensors',page.read_text()))
 from version_assets import version_assets
 version_assets()
 print('Current audited publication: 26 open cases, including five at rank eight; source-bound exact filters rebuilt.')
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--metadata-only',action='store_true');args=p.parse_args();main(not args.metadata_only)
