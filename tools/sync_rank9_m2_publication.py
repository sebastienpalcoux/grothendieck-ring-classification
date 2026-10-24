#!/usr/bin/env python3
"""Synchronize live aggregate metadata while retaining earlier case decisions."""
from pathlib import Path
import ast,hashlib,json,re,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];E=ROOT/'evidence/rank9_m2_20261024';DIST=ROOT/'site/dist'
sys.path.insert(0,str(ROOT/'site'))
from high_rank_publication import extend_document,extend_front,manuscript_index

def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def info(p):return{'sha256':sha(p),'bytes':p.stat().st_size}
def main():
 from research_continuation_20261024 import active as research_active
 if research_active(ROOT):
  from sync_research_revision import main as sync_latest
  return sync_latest()
 from audit_corrections_20261024 import active as audit_active
 if audit_active(ROOT):
  from sync_audit_revision import main as sync_current
  return sync_current()
 ledger=read(E/'ledger.json');summary=read(E/'summary.json');ids=[r['id']for r in ledger if r['status']=='unresolved'];assert len(ids)==18
 p=ROOT/'data/current_publication_revision.json';rev=read(p);rev['date']='2026-10-24';rev['remaining_ids']=sorted(set(rev['remaining_ids'])|set(ids),key=lambda x:tuple(map(int,re.findall(r'\d+',x))))
 assert len(rev['remaining_ids'])==25
 rev['current_unresolved_total']=25;rev['rank9_m2']={'input_count':2083,'excluded':2033,'unitarily_realized':32,'unresolved':18,'ledger':E.relative_to(ROOT).as_posix()+'/ledger.json',**info(E/'ledger.json'),'replay':{**info(E/'replay.zip'),'path':E.relative_to(ROOT).as_posix()+'/replay.zip'}}
 paper=ROOT/'publications/rank9-m2/paper'
 for f in paper.iterdir():
  if f.suffix in('.tex','.pdf'):rev['documents'][f.relative_to(ROOT).as_posix()]=info(f)
 rev['web_copies']['papers/rank9-m2.pdf']='publications/rank9-m2/paper/rank9-m2.pdf'
 write(p,rev);shutil.copy2(p,DIST/'data/current_publication_revision.json')
 pages_path=ROOT/'data/current_manuscript_page_counts.json';pages=read(pages_path);pdf=paper/'rank9-m2.pdf';n=int(re.search(r'^Pages:\s*(\d+)',subprocess.check_output(['pdfinfo',str(pdf)],text=True),re.M)[1]);title='Rank-nine multiplicity-two classification'
 pages['documents']=[x for x in pages['documents']if x['path']!=pdf.relative_to(ROOT).as_posix()]
 item={'title':title,'kind':'mathematical_manuscript','path':pdf.relative_to(ROOT).as_posix(),'pages':n,**info(pdf)}
 index=next(i for i,d in enumerate(pages['documents'])if d['path'].startswith('publications/rank11/'));pages['documents'].insert(index,item)
 pages['date']='2026-10-24'
 for kind in ('mathematical_manuscript','verification_guide','research_status_report'):pages['totals'][kind]=sum(d['pages']for d in pages['documents']if d['kind']==kind)
 pages['totals']['mathematical_manuscripts_and_guides']=pages['totals']['mathematical_manuscript']+pages['totals']['verification_guide'];pages['totals']['all_distinct_documents']=sum(d['pages']for d in pages['documents']);pages['document_counts']['mathematical_manuscripts']=sum(d['kind']=='mathematical_manuscript'for d in pages['documents'])
 write(pages_path,pages);shutil.copy2(pages_path,DIST/'downloads/current_manuscript_page_counts.json')
 # Refresh only the deliberately mutable global-document pointer.
 r11=DIST/'data/rank11_m1.json';r=read(r11);case_digest=hashlib.sha256(json.dumps(r['cases'],sort_keys=True,separators=(',',':')).encode()).hexdigest();old_sha=sha(r11)
 r['summary']['current_documents']={'path':'data/current_publication_revision.json','sha256':sha(p),'date':'2026-10-24'}
 r11.write_text(json.dumps(r,ensure_ascii=False,separators=(',',':'))+'\n')
 assert hashlib.sha256(json.dumps(read(r11)['cases'],sort_keys=True,separators=(',',':')).encode()).hexdigest()==case_digest
 r11receipt=DIST/'data/rank11_m1_build.json';r=read(r11receipt);r.setdefault('prior_mutable_aggregate_sha256',{})['site/dist/data/current_publication_revision.json']=r['legacy_sha256'].pop('site/dist/data/current_publication_revision.json',r.get('prior_mutable_aggregate_sha256',{}).get('site/dist/data/current_publication_revision.json'))
 r['mutable_aggregate_note']='The current publication aggregate includes the rank-nine M2 extension. All earlier per-case decisions and original proof ledgers retain their separate hash bindings.';write(r11receipt,r)
 m2receipt=DIST/'data/rank9_m2_build.json';r=read(m2receipt);r['legacy_case_sha256']={'rank11_m1.json':case_digest};r['mutable_metadata_updates']={'rank11_m1.json':{'before_sha256':old_sha,'after_sha256':sha(r11),'reason':'Refresh the current-document aggregate pointer; case records unchanged.'}};r['legacy_sha256']['rank11_m1.json']=sha(r11);write(m2receipt,r)
 m2=DIST/'data/rank9_m2.json';r=read(m2);r['summary']['current_documents']={'path':'data/current_publication_revision.json','sha256':sha(p),'date':'2026-10-24'};m2.write_text(json.dumps(r,ensure_ascii=False,separators=(',',':'))+'\n')
 # One current download contains all twenty-five open tensors; the old lower-rank module is retained.
 payloads=[read(DIST/'data/unresolved_cases.json')['cases'],read(DIST/'data/rank9_rank10_m1.json')['cases'],read(m2)['cases']]
 rows={r['id']:r for group in payloads for r in group if r['status']=='unresolved'};assert set(rows)==set(rev['remaining_ids'])
 tensors={rid:rows[rid]['fusion_tensor']for rid in rev['remaining_ids']};metadata={rid:{'rank':rows[rid]['rank'],'multiplicity':rows[rid]['multiplicity'],'tensor_sha256':rows[rid]['tensor_sha256'],'status':'unresolved'}for rid in rev['remaining_ids']}
 text='"""Current unresolved based rings; N[i][j][k], zero-based indices, unit X_0.\nGeneral complex categorification remains open for every listed tensor.\n"""\n\nMETADATA = '+repr(metadata)+'\n\nTENSORS = '+repr(tensors)+'\n';ast.parse(text);(ROOT/'data/current_remaining_cases.py').write_text(text);shutil.copy2(ROOT/'data/current_remaining_cases.py',DIST/'downloads/current_remaining_cases.py')
 readme=ROOT/'README.md';readme.write_text(extend_front(readme.read_text(),ROOT))
 for name in ('VERIFY','RESEARCH_STATUS','PROVENANCE','PREPUBLICATION_REVIEW','PROJECT_GUIDE'):
  f=ROOT/'docs'/(name+'.md');f.write_text(extend_document(f.read_text()))
 f=ROOT/'manuscripts/README.md';text=f.read_text();marker='<details><summary>Earlier lower-rank reading notes and research history</summary>';historical=text.split(marker,1)[1].rsplit('</details>',1)[0].strip()if marker in text else text;f.write_text(manuscript_index(ROOT,historical))
 # Regenerate evidence bindings after adding source tables/audit metadata.
 manifest=read(E/'source_manifest.json');manifest['files']={str(f.relative_to(E)):sha(f)for f in E.rglob('*')if f.is_file()and f.name!='source_manifest.json'};write(E/'source_manifest.json',manifest)
 for html in DIST.glob('*.html'):
  text=html.read_text()
  for asset in ('app.js','cases.js','catalogue.js','redirect.js','styles.css','cases.css'):
   text=re.sub(r'(\b(?:src|href)="\./'+re.escape(asset)+r')(?:\?v=[^"]*)?(")',lambda m:m[1]+'?v='+sha(DIST/asset)[:12]+m[2],text)
  if text!=html.read_text():html.write_text(text)
 print({'rank9_exact_M2':summary,'global_unresolved':25,'current_manuscript_pages':pages['totals']['mathematical_manuscript'],'new_manuscript_pages':n})
if __name__=='__main__':main()
