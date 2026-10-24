#!/usr/bin/env python3
"""Regenerate the mutable current publication after the accepted theoretical continuation.

Old decision ledgers/receipts remain immutable. Derived displays and pointers
are regenerated from the corrected rank-eight ledger and current high ranks.
"""
from pathlib import Path
from collections import Counter
import ast,hashlib,json,re,runpy,shutil,sys
ROOT=Path(__file__).resolve().parents[1];DIST=ROOT/'site/dist';E=ROOT/'evidence/research_20261024'
sys.path.insert(0,str(ROOT/'site'))
import research_continuation_20261024 as correction
from audit_corrections_20261024 import refresh_scope_sources
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
 low_revision['remaining_ids']=['R6_4_155','R6_8_1660']+correction.REMAINING_IDS
 low_revision['rank8_m3_update']=extension(ROOT)
 for source in low_revision['documents']:low_revision['documents'][source]=info(ROOT/source)
 write(low,low_revision)
 # The active exported partition is derived from the corrected full ledger.
 p=ROOT/'data/classification_status.json';status=read(p)
 band=next(x for x in status['rows']if x['rank']==8 and x['multiplicity']==3)
 band.update(excluded_general=3507,unresolved_general=4,classification_coverage='partial_classification')
 status['inputs']['rank8'].update(file=correction.LEDGER,sha256=sha(ROOT/correction.LEDGER),ledger=correction.LEDGER,status_totals={'excluded':4403,'unitarily_realized':93,'unresolved':4},audit_correction='evidence/audit_20261024/accepted.json')
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
  if x['rank']==8:x.update(unresolved=4,note='Four general questions remain open; R8_3_436 is excluded by an independent spherical-equivariantization proof.')
 atlas['remaining_ids']=['R6_4_155','R6_8_1660']+correction.REMAINING_IDS
 write(DIST/'data/current_remaining_ids.json',atlas['remaining_ids'])
 atlas['remaining_ids_file']['sha256']=sha(DIST/'data/current_remaining_ids.json')
 # Current low-rank tensor module, still distinct from the complete high-rank download.
 (ROOT/'data/remaining_cases.py').write_text(render_tensors(ROOT));refresh_scope_sources(ROOT);shutil.copy2(ROOT/'data/remaining_cases.py',DIST/'downloads/remaining_cases.py')
 # Current per-ring audit has a new scope; old accepted source manifests are untouched.
 attempt=read(ROOT/correction.AUDIT);attempt['rows']=[r for r in attempt['rows']if r['id']in correction.REMAINING_IDS]
 attempt['display_scope']='Four current rank-eight open cases; complete historical research is preserved separately.'
 write(DIST/'data/rank8_m3_attempts.json',attempt)
 ext['attempts']={'path':'data/rank8_m3_attempts.json','sha256':sha(DIST/'data/rank8_m3_attempts.json'),'cases':4}
 write(DIST/'data/rank8_m3_update.json',ext)
 ext['metadata_path']='data/rank8_m3_update.json';ext['metadata_sha256']=sha(DIST/'data/rank8_m3_update.json')
 atlas['rank8_m3_update']=ext;write(p,atlas)
 # Rebuild the case dossiers from exact tensors, without repeating unrelated searches.
 from build_cases import build
 if rebuild_cases:build(ROOT)
 from unresolved_retry_20261024 import active as retry_active,apply_profiles,validate as retry_validate,LEDGER as retry_ledger,EVIDENCE as retry_evidence
 retry=retry_active(ROOT)
 if retry:apply_profiles(ROOT)
 expected_open=10 if retry else 11
 payloads=[read(DIST/'data/unresolved_cases.json')['cases']]+[read(DIST/'data'/name)['cases']for name in ('rank9_rank10_m1.json','rank11_m1.json','rank9_m2.json')]
 opened={r['id']:r for group in payloads for r in group if r['status']=='unresolved'}
 ids=sorted(opened,key=lambda x:tuple(map(int,re.findall(r'\d+',x))))
 if len(ids)!=expected_open:raise ValueError(f'Expected {expected_open} open cases after the accepted research continuation')
 tensors={rid:opened[rid]['fusion_tensor']for rid in ids};metadata={rid:{'rank':opened[rid]['rank'],'multiplicity':opened[rid]['multiplicity'],'tensor_sha256':opened[rid]['tensor_sha256'],'status':'unresolved'}for rid in ids}
 text='"""All current unresolved fusion tensors. Unit X_0; N[i][j][k].\nGeneral complex categorification remains open for every listed tensor.\n"""\n\nMETADATA = '+repr(metadata)+'\n\nTENSORS = '+repr(tensors)+'\n';ast.parse(text)
 (ROOT/'data/current_remaining_cases.py').write_text(text);shutil.copy2(ROOT/'data/current_remaining_cases.py',DIST/'downloads/current_remaining_cases.py')
 # Retain all current high-rank manuscript selections while refreshing modified sources.
 p=ROOT/'data/current_publication_revision.json';rev=read(p)
 rev.update(date='2026-10-24',remaining_ids=ids,current_unresolved_total=expected_open,rank8_m3_update=extension(ROOT),research_continuation=correction.validate(ROOT))
 if retry:
  rev['theoretical_retry']=retry_validate(ROOT)
  old=rev['research_continuation'];old['stage_open_cases']=old.pop('current_open_cases',11);old['superseded_by']=retry_evidence
  rev['rank9_rank10_m1']={'input_count':336,'excluded':238,'unitarily_realized':98,'unresolved':0,'ledger':retry_ledger,**info(ROOT/retry_ledger)}
  rev['rank10_m1_continuation']={'evidence':retry_evidence,'unresolved_ids':[],'realized_ids':['R10_1_189'],'ledger':retry_ledger}
 for name in rev['documents']:rev['documents'][name]=info(ROOT/name)
 for name in (ROOT/'publications/rank9-m2/paper').glob('*'):
  if name.suffix in ('.tex','.pdf'):rev['documents'][name.relative_to(ROOT).as_posix()]=info(name)
 rev['rank9_m2']={'input_count':2083,'excluded':2043,'unitarily_realized':36,'unresolved':4,'ledger':correction.R9+'/ledger.json',**info(ROOT/correction.R9/'ledger.json'),'replay':{'path':correction.R9+'/replay.zip',**info(ROOT/correction.R9/'replay.zip')}}
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
 refresh(atlas)
 for name in atlas.get('rank6_release',{}).get('documents',{}):
  atlas['rank6_release']['documents'][name]=sha(DIST/'papers'/name)
 write(DIST/'data/atlas.json',atlas)
 shutil.copy2(DIST/'data/atlas.json',ROOT/'data/atlas.json')
 current_pages=read(ROOT/'data/current_manuscript_page_counts.json');totals=current_pages['totals']
 summary=f"{current_pages['document_counts']['mathematical_manuscripts']} mathematical manuscripts: {totals['mathematical_manuscript']} pages; with the three verification guides: {totals['mathematical_manuscripts_and_guides']}; with the current research-status report: {totals['all_distinct_documents']}. Each distinct document is counted once."
 page=DIST/'index.html';page.write_text(re.sub(r'(<span id="manuscript-page-summary">).*?(</span>)',lambda m:m[1]+summary+m[2],page.read_text()))
 page=DIST/'index.html';content=page.read_text();content=re.sub(r'(<p class="scope-note" id="current-manuscript-page-summary">).*?(<a href=)',lambda m:m[1]+summary+' '+m[2],content,flags=re.S);content=content.replace('tree/main/evidence/rank9_m2_20261024\" target','tree/main/evidence/unresolved_retry_20261024\" target');page.write_text(content)
 from build_ring_properties import build as properties
 properties()
 page=DIST/'index.html';page.write_text(re.sub(r'All \d+ open rings · Python tensors',f'All {len(ids)} open rings · Python tensors',page.read_text()))
 from research_review_page import rewrite_review
 rewrite_review(ROOT)
 from version_assets import version_assets
 version_assets()
 # Current proof shelf and explicit replacements for mutable display metadata.
 shelf=ROOT/correction.R9;manifest=read(shelf/'source_manifest.json')
 manifest.update(archive_current_ledger='phase5/results/ledger.json',counts=read(shelf/'summary.json'),source_package={'path':'replay.zip',**info(shelf/'replay.zip')})
 manifest['files']={p.relative_to(shelf).as_posix():sha(p)for p in shelf.rglob('*')if p.is_file() and p.name!='source_manifest.json' and '__pycache__'not in p.parts}
 write(shelf/'source_manifest.json',manifest)
 before=read(E/'predecessor_site_sources.json');old=read(ROOT/'evidence/audit_20261024/derived_publication_replacements.json');replacements={}
 previous=read(E/'derived_publication_replacements.json') if (E/'derived_publication_replacements.json').is_file() else {'files':{}}
 for path,h in before.items():
  p=ROOT/path
  if p.is_file() and sha(p)!=h:
   prior=[h];entry=old['files'].get(path,{})
   for value in (entry.get('before_sha256'),entry.get('after_sha256'),*previous['files'].get(path,{}).get('prior_sha256',[]),previous['files'].get(path,{}).get('after_sha256')):
    if value and value not in prior:prior.append(value)
   replacements[path]={'prior_sha256':prior,'after_sha256':sha(p)}
 write(E/'derived_publication_replacements.json',{'schema':'research-derived-publication-replacements/v1','rank8_ledger':correction.LEDGER,'rank8_ledger_sha256':sha(ROOT/correction.LEDGER),'rank9_ledger':correction.R9+'/ledger.json','rank9_ledger_sha256':sha(ROOT/correction.R9/'ledger.json'),'files':replacements,'scope':'Only derived website metadata; all case changes separately reconcile against the accepted tensor-bound transitions.'})
 page=DIST/'review.html';text=page.read_text();text=text.replace('Current classification · 26 open questions',f'Current classification · {expected_open} open questions');page.write_text(text)
 print(f'Current accepted research: {expected_open} open cases; four at rank eight and four at rank nine; exact filters rebuilt.')
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--metadata-only',action='store_true');args=p.parse_args();main(not args.metadata_only)
