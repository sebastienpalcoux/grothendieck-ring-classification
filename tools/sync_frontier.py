#!/usr/bin/env python3
"""Synchronize the current accepted frontier, manuscripts and website metadata."""
from pathlib import Path
from collections import Counter
import argparse,ast,csv,json,shutil,subprocess,sys
from pypdf import PdfReader
from frontier import ROOT,DATE,EVIDENCE,LEDGER,EXACT_LEDGER,REMAINING,R8_REMAINING,FINDINGS,read,write,sha,apply_profiles,publication_extension,restriction_metadata
D=ROOT/'site/dist'
def info(p):
 p=Path(p);return {'sha256':sha(p),'bytes':p.stat().st_size}
def csvcopy(path,rows):
 with path.open('w',newline='')as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
def profiles():
 # Preserve original frozen source data in the proof inputs, publish six tensors.
 module=ast.parse((ROOT/EVIDENCE/'replay/prior/data/current_remaining_cases.py').read_text())
 v={n.targets[0].id:ast.literal_eval(n.value)for n in module.body if isinstance(n,ast.Assign)}
 s='"""Current unresolved fusion tensors. General complex existence remains open.\nUnit X_0; N[i][j][k] is the coefficient of X_k in X_i times X_j.\n"""\n\n'
 s+='METADATA = '+repr({rid:{**v['METADATA'][rid],'unit_index':0}for rid in REMAINING})+'\n\n'
 s+='DUALS = '+repr({rid:[next(j for j in range(len(v['TENSORS'][rid]))if v['TENSORS'][rid][i][j][0])for i in range(len(v['TENSORS'][rid]))]for rid in REMAINING})+'\n\n'
 for rid in REMAINING:s+=rid+' = '+repr(v['TENSORS'][rid])+'\n\n'
 s+='TENSORS = '+repr({rid:v['TENSORS'][rid]for rid in REMAINING})+'\n'
 (ROOT/'data/current_remaining_cases.py').write_text(s);shutil.copy2(ROOT/'data/current_remaining_cases.py',D/'downloads/current_remaining_cases.py')
 (ROOT/'data/remaining_cases.py').write_text(s);shutil.copy2(ROOT/'data/current_remaining_cases.py',D/'downloads/remaining_cases.py')
 write(D/'data/current_remaining_ids.json',REMAINING)
 # Reader documentation has current hashes; frozen mathematical evidence does not change.
 def documentation_bindings(v):
  if isinstance(v,dict):
   path=v.get('path')
   if isinstance(path,str)and ((path.startswith(('site/','docs/'))and path.endswith('.md'))or path in('site/categorification_scope.json','data/remaining_cases.py','data/current_remaining_cases.py'))and (ROOT/path).is_file()and 'sha256'in v:v['sha256']=sha(ROOT/path)
   for x in v.values():documentation_bindings(x)
  elif isinstance(v,list):
   for x in v:documentation_bindings(x)
 sp=ROOT/'site/categorification_scope.json';sc=read(sp);documentation_bindings(sc);write(sp,sc)
 for name in ('unresolved_cases.json','resolved_cases.json','rank9_m2.json','realized_rings.json'):
  p=D/'data'/name;v=read(p);documentation_bindings(v);write(p,v,True)
 apply_profiles(ROOT)
 # The sole decision transition changes only the rank-eight M3 partition.
 for name in ('classification_status.json','classification_summary_all_ranks.json'):
  p=ROOT/'data'/name;v=read(p)
  for row in v['rows']:
   if row['rank']==8 and row['multiplicity']==3:row.update(excluded_general=3508,unresolved_general=3)
  if name=='classification_status.json':
   v['inputs']['rank8'].update(file=LEDGER,sha256=sha(ROOT/LEDGER),status_totals={'excluded':4404,'unitarily_realized':93,'unresolved':3})
  else:v['date']=DATE;csvcopy(p.with_suffix('.csv'),v['rows'])
  write(p,v)
  if (D/'data'/name).exists():shutil.copy2(p,D/'data'/name)
 subprocess.run([sys.executable,str(ROOT/'tools/export_grothendieck_counts.py')],check=True,cwd=ROOT)
 for name in ('grothendieck_counts.json','grothendieck_counts.csv'):shutil.copy2(ROOT/'data'/name,D/'data'/name)
 attempts=read(ROOT/EVIDENCE/'rank8_research_audit.json')
 write(D/'data/rank8_m3_attempts.json',attempts,True)
 item=publication_extension(ROOT);item['attempts']={'path':'data/rank8_m3_attempts.json','sha256':sha(D/'data/rank8_m3_attempts.json'),'cases':3}
 write(D/'data/rank8_m3_update.json',item)
 item['metadata_path']='data/rank8_m3_update.json';item['metadata_sha256']=sha(D/'data/rank8_m3_update.json')
 # Current row properties and tensor identities remain unchanged.
 sys.path.insert(0,str(ROOT/'site'))
 from build_ring_properties import build
 build()
 atlas=read(D/'data/atlas.json');atlas['snapshot']=DATE;atlas['remaining_ids']=REMAINING
 atlas['remaining_ids_file']={'path':'data/current_remaining_ids.json','sha256':sha(D/'data/current_remaining_ids.json')}
 atlas['rank8_m3_update']=item
 for row in atlas['scope']:
  if row['rank']==8:row.update(unresolved=3)
 atlas['frontier_continuation']={'date':DATE,'current_unresolved_total':6,'new_general_exclusions':['R8_3_1768'],'new_models':0,'accepted':EVIDENCE+'/accepted.json'}
 write(D/'data/atlas.json',atlas,True);write(ROOT/'data/atlas.json',atlas,True)
def documents():
 # Replace old research-status reports in the current inventory.
 report='manuscripts/frontier/Fusion_Ring_Frontier.pdf'
 for p in (ROOT/'manuscripts').glob('prepublication-review-*'):
  if p.suffix in ('.tex','.pdf'):p.unlink()
 for p in (D/'papers').glob('prepublication-review-*.pdf'):p.unlink()
 for name in ('current_document_revision.json','current_publication_revision.json'):
  p=ROOT/'data'/name;v=read(p);v['date']=DATE
  v['remaining_ids']=REMAINING if name.startswith('current_publication')else[r for r in REMAINING if not r.startswith('R9')]
  v['rank8_m3_update']=publication_extension(ROOT)
  v['documents']={n:info(ROOT/n)for n in v['documents']if (ROOT/n).is_file()and not Path(n).name.startswith('prepublication-review-')}
  for n in ('manuscripts/frontier/Fusion_Ring_Frontier.tex',report,'publications/rank9-m2/paper/r137_restrictions.tex'):
   if name.startswith('current_publication')or not n.startswith('publications/'):v['documents'][n]=info(ROOT/n)
  # All authored rank-six/rank-eight chapter additions are current sources.
  if name.startswith('current_document'):
   from current_publication import document_paths
   v['documents']={n:info(ROOT/n)for n in sorted(document_paths(ROOT))}
  v['web_copies']={k:s for k,s in v['web_copies'].items()if s in v['documents']and not Path(s).name.startswith('prepublication-review-')}
  v['web_copies']['papers/frontier.pdf']=report
  v['frontier_continuation']={'date':DATE,'accepted':EVIDENCE+'/accepted.json','remaining_ids':REMAINING,'new_general_exclusions':['R8_3_1768'],'new_models':0,'replay_archive':'site/dist/downloads/Fusion-Ring-Frontier-Proofs-and-Checks.zip'}
  v['frontier_continuation']['current_restrictions']=restriction_metadata()
  if name.startswith('current_publication'):
   v['current_unresolved_total']=6
   low=read(ROOT/'data/current_document_revision.json')
   v['documents'].update(low['documents']);v['web_copies'].update(low['web_copies'])
   v['base_document_manifest']={'path':'data/current_document_revision.json',**info(ROOT/'data/current_document_revision.json'),'scope':'Current lower-rank manuscript and website-copy identities.'}
  write(p,v);shutil.copy2(p,D/'data'/name)
  for web,source in v['web_copies'].items():
   dest=D/web;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/source,dest)
 # Count distinct current documents, not mirrored PDFs.
 for name in ('manuscript_page_counts.json','current_manuscript_page_counts.json'):
  p=ROOT/'data'/name;v=read(p);v['date']=DATE
  for row in v['documents']:
   if row['kind']=='research_status_report':row.update(path=report,title='Current categorification frontier')
   file=ROOT/row['path'];row.update(info(file),pages=len(PdfReader(file).pages))
  counts=Counter()
  for row in v['documents']:counts[row['kind']]+=row['pages']
  v['totals']={**dict(counts),'mathematical_manuscripts_and_guides':counts['mathematical_manuscript']+counts['verification_guide'],'all_distinct_documents':sum(counts.values())}
  write(p,v);shutil.copy2(p,D/'downloads'/name)
 pointer={'path':'data/current_publication_revision.json','sha256':sha(ROOT/'data/current_publication_revision.json'),'date':DATE}
 for name in ('rank9_m2.json','rank9_rank10_m1.json','rank11_m1.json','rank12_m1.json'):
  p=D/'data'/name;v=read(p);v['summary']['current_documents']=pointer;write(p,v,True)
 # Source JSON changed only metadata; refresh exact ring-property source bindings.
 sys.path.insert(0,str(ROOT/'site'));from build_ring_properties import build
 build()
 atlas=read(D/'data/atlas.json');atlas['current_documents'].update(date=DATE,sha256=sha(ROOT/'data/current_document_revision.json'))
 atlas['current_publication_documents']=pointer;atlas['reader_resources']['page_totals']=read(ROOT/'data/manuscript_page_counts.json')['totals']
 atlas['frontier_continuation']['current_restrictions']=restriction_metadata()
 atlas['frontier_continuation'].update(report='papers/frontier.pdf',archive='downloads/Fusion-Ring-Frontier-Proofs-and-Checks.zip')
 entry=atlas.get('rank6_release',{}).get('document_revision')
 if entry:
  src=ROOT/entry['source'];dest=D/entry['path'];shutil.copy2(src,dest)
  if src!=ROOT/entry['path']:shutil.copy2(src,ROOT/entry['path'])
  entry.update(date=DATE,sha256=sha(src))
 def refresh(v):
  if isinstance(v,dict):
   path=v.get('path')
   if isinstance(path,str)and(D/path).is_file()and'sha256'in v:
    v['sha256']=sha(D/path)
    if 'bytes'in v:v['bytes']=(D/path).stat().st_size
   for value in v.values():refresh(value)
  elif isinstance(v,list):
   for value in v:refresh(value)
 refresh(atlas)
 for name in atlas.get('rank6_release',{}).get('documents',{}):
  file=D/'papers'/name
  if file.exists():atlas['rank6_release']['documents'][name]=sha(file)
 write(D/'data/atlas.json',atlas,True);write(ROOT/'data/atlas.json',atlas,True)
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--profiles-only',action='store_true');a=p.parse_args()
 profiles()
 if not a.profiles_only:documents()
 # Every property-source update must invalidate the browser's shared catalogue.
 sys.path.insert(0,str(ROOT/'site'))
 from version_catalogue import main as version_catalogue
 version_catalogue()
 print('Current frontier synchronized: one new exclusion, no new models, six unresolved.')
if __name__=='__main__':main()

