#!/usr/bin/env python3
"""Synchronize the dated proof correction without changing any decision ledger."""
from pathlib import Path
from collections import Counter
import argparse,hashlib,json,re,shutil,sys
from correctness_publication import EVIDENCE,DATE,MODELS,update_models,revise_document
ROOT=Path(__file__).resolve().parents[1];DIST=ROOT/'site/dist'
def read(p):return json.loads(Path(p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def info(p):return {'sha256':sha(p),'bytes':Path(p).stat().st_size}
def write(p,v):Path(p).parent.mkdir(parents=True,exist_ok=True);Path(p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def main():
 sys.path.insert(0,str(ROOT/'site'))
 from current_publication import document_paths
 # The low-rank current-manuscript inventory is separate from historical sources.
 low=read(ROOT/'data/current_document_revision.json');low['date']=DATE
 low['documents']={n:info(ROOT/n)for n in sorted(document_paths(ROOT))}
 low['web_copies']={k:v for k,v in low['web_copies'].items()if'prepublication-review-'not in k}
 low['web_copies']['papers/prepublication-review-2026-10-25.pdf']='manuscripts/prepublication-review-2026-10-25.pdf'
 low['correctness_revision']=EVIDENCE+'/revision.json';write(ROOT/'data/current_document_revision.json',low)
 high=read(ROOT/'data/current_publication_revision.json');high['date']=DATE
 for n in list(high['documents']):
  if 'prepublication-review-2026-10-24.' in n:del high['documents'][n]
 for n in low['documents']:high['documents'][n]=low['documents'][n]
 for p in (ROOT/'publications').rglob('*'):
  if p.is_file()and p.suffix in('.tex','.pdf'):high['documents'][p.relative_to(ROOT).as_posix()]=info(p)
 high['documents']['manuscripts/prepublication-review-2026-10-25.tex']=info(ROOT/'manuscripts/prepublication-review-2026-10-25.tex')
 high['web_copies']={k:v for k,v in high['web_copies'].items()if'prepublication-review-'not in k}
 high['web_copies'].update(low['web_copies']);high['correctness_revision']=EVIDENCE+'/revision.json'
 for n in high['documents']:high['documents'][n]=info(ROOT/n)
 write(ROOT/'data/current_publication_revision.json',high)
 for name,manifest in [('current_document_revision.json',low),('current_publication_revision.json',high)]:
  shutil.copy2(ROOT/'data'/name,DIST/'data'/name)
  for web,source in manifest['web_copies'].items():shutil.copy2(ROOT/source,DIST/web)
 # Update the mathematical model pointers; tensor and status fields are preserved.
 p=DIST/'data/realized_rings.json';data=read(p);update_models(data['records']);p.write_text(json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n')
 for name in ('resolved_cases.json','rank9_rank10_m1.json','rank11_m1.json','rank9_m2.json'):
  p=DIST/'data'/name;v=read(p)
  if name=='resolved_cases.json':
   update_models(v['cases'])
   for r in v['cases']:
    if r['id'] in MODELS:r['summary']=MODELS[r['id']][1]
  if 'summary'in v:v['summary']['current_documents']={'path':'data/current_publication_revision.json','sha256':sha(ROOT/'data/current_publication_revision.json'),'date':DATE}
  p.write_text(json.dumps(v,ensure_ascii=False,separators=(',',':'))+'\n')
 # Exact property values are unchanged, but bind their refreshed source records.
 from build_ring_properties import build
 build()
 from pypdf import PdfReader
 for name in ('manuscript_page_counts.json','current_manuscript_page_counts.json'):
  v=read(ROOT/'data'/name);v['date']=DATE
  for d in v['documents']:
   if d['kind']=='research_status_report':d['path']='manuscripts/prepublication-review-2026-10-25.pdf'
   p=ROOT/d['path'];d.update(info(p),pages=len(PdfReader(p).pages))
  counts=Counter()
  for d in v['documents']:counts[d['kind']]+=d['pages']
  v['totals'].update(dict(counts));v['totals']['all_distinct_documents']=sum(counts.values());v['totals']['mathematical_manuscripts_and_guides']=counts['mathematical_manuscript']+counts['verification_guide'];write(ROOT/'data'/name,v);shutil.copy2(ROOT/'data'/name,DIST/'downloads'/name)
 atlas=read(DIST/'data/atlas.json');atlas['snapshot']=DATE
 atlas['current_documents'].update(date=DATE,sha256=sha(ROOT/'data/current_document_revision.json'))
 atlas['current_publication_documents']={'path':'data/current_publication_revision.json','sha256':sha(ROOT/'data/current_publication_revision.json'),'date':DATE}
 atlas['correctness_revision']={'path':'data/correctness_revision.json','date':DATE,'classification_changed':False}
 atlas['reader_resources']['page_totals']=read(ROOT/'data/manuscript_page_counts.json')['totals']
 release=atlas.get('rank6_release',{})
 if release.get('document_revision'):
  entry=release['document_revision'];source=ROOT/entry['source'];shutil.copy2(source,DIST/entry['path'])
  if source!=ROOT/entry['path']:shutil.copy2(source,ROOT/entry['path'])
  entry.update(date=DATE,sha256=sha(source))
 for name in release.get('documents',{}):release['documents'][name]=sha(DIST/'papers'/name)
 def refresh(value):
  if isinstance(value,dict):
   p=value.get('path')
   if isinstance(p,str)and(DIST/p).is_file()and'sha256'in value:
    value['sha256']=sha(DIST/p)
    if'bytes'in value:value['bytes']=(DIST/p).stat().st_size
   for v in value.values():refresh(v)
  elif isinstance(value,list):
   for v in value:refresh(v)
 refresh(atlas);write(DIST/'data/atlas.json',atlas);write(ROOT/'data/atlas.json',atlas)
 pages=read(ROOT/'data/current_manuscript_page_counts.json');totals=pages['totals'];summary=f"{pages['document_counts']['mathematical_manuscripts']} mathematical manuscripts: {totals['mathematical_manuscript']} pages; with the three verification guides: {totals['mathematical_manuscripts_and_guides']}; with the current research-status report: {totals['all_distinct_documents']}. Each distinct document is counted once."
 p=DIST/'index.html';s=p.read_text();s=re.sub(r'(<span id="manuscript-page-summary">).*?(</span>)',lambda m:m[1]+summary+m[2],s);s=re.sub(r'(<p class="scope-note" id="current-manuscript-page-summary">).*?(<a href=)',lambda m:m[1]+summary+' '+m[2],s,flags=re.S)
 s=re.sub(r'<p class="scope-note" id="correctness-update">.*?</p>\s*','',s,flags=re.S)
 note='<p class="scope-note" id="correctness-update">25 October correctness revision: exact proof repairs and replay corrections; classification counts are unchanged. <a href="./review.html#correctness-20261025">Audit findings and corrected proofs →</a></p>'
 anchor='<p class="scope-note" id="fusion-census-status" hidden></p>';s=s.replace(anchor,anchor+'\n      '+note);p.write_text(s)
 p=DIST/'review.html';s=p.read_text();s=re.sub(r'<section class="review-panel" id="correctness-20261025">.*?</section>\s*','',s,flags=re.S)
 panel='''<section class="review-panel" id="correctness-20261025"><h2>Correctness revision · 25 October 2026</h2><p>The current classification is unchanged. Exact replacement arguments identify R6_2_143, R8_2_820 and R8_2_869; a direct completion identifies R8_3_721 without census completeness. The revised manuscripts include these proofs. Code and replay defects are corrected and their scope is documented.</p><p><a href="https://github.com/sebastienpalcoux/grothendieck-ring-classification/blob/main/evidence/correctness_20261025/README.md">Findings, corrected proofs and exact commands ↗</a> · <a href="./downloads/correctness-audit-2026-10-25.zip" download>Original audit evidence · ZIP</a></p><details class="review-details"><summary>Verification scope and remaining limits</summary><p>All 1,433,410 supplied rank‑3–11 tensors passed exact fusion axioms and based-isomorphism checks. The original audit reviewed 11 main mathematical manuscripts, their operative criteria and model code, and all accepted routes. Three identification gaps were repaired rather than inferred from successful scalar calculations. The rank-nine command now covers the accepted baseline and phases two–five, with the omitted certificates supplied.</p><p>Historical failures and source identities are preserved. The original rank-six audit used a disclosed partly log-derived composite; the current correction route retains raw results and compatible immutable proof contexts. Complete upstream census enumeration and independent reproof of every external categorical theorem are not claimed. The ten open cases remain open. Independent human verification and formalization remain pending.</p></details></section>'''
 anchor='</aside>';at=s.find(anchor,s.find('<main'))
 if at<0:raise RuntimeError('review-page panel anchor missing')
 s=s[:at+len(anchor)]+'\n'+panel+s[at+len(anchor):]
 s=s.replace('Research status · 24 October 2026','Research status · 25 October 2026').replace('papers/prepublication-review-2026-10-24.pdf','papers/prepublication-review-2026-10-25.pdf')
 s=re.sub(r'<details class="review-details"><summary>Rank-six computational coverage</summary>.*?</details>',lambda _: '<details class="review-details"><summary>Rank-six computational coverage</summary><p>The current correction route retains all original raw exclusion verdicts, complete reference-backend retries and the exact post-loop checks. The eleven immutable multiplicity-nine proofs run in their source-compatible frozen context, with current tensor and certificate identities checked. This is an explicitly source-bound combined campaign, not a single uniform-backend invocation.</p><p>The original pre-revision audit had partly log-derived coverage after raw-output loss. That limitation and the initial failures remain preserved. <a href="https://github.com/sebastienpalcoux/grothendieck-ring-classification/blob/main/evidence/correctness_20261025/README.md">Current commands, receipts and scope ↗</a></p></details>',s,count=1,flags=re.S)
 s=s.replace('https://github.com/sebastienpalcoux/grothendieck-ring-classification/blob/main/evidence/audit_20261024/README.md\">Audit corrections and current verification', 'https://github.com/sebastienpalcoux/grothendieck-ring-classification/blob/main/evidence/correctness_20261025/README.md\">Audit corrections and current verification')
 p.write_text(s)
 # Apply the dated note to hand-maintained pages as well as generated guides.
 for name in ('evidence/rank9_m2_20261024/README.md','manuscripts/README.md'):
  p=ROOT/name;p.write_text(revise_document(name,p.read_text(),ROOT))
 from version_assets import version_assets
 version_assets()
 print('Synchronized correctness revision, current PDFs, model proof pointers and exact property source identities.')
if __name__=='__main__':main()
