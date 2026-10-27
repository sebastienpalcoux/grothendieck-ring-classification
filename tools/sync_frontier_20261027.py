#!/usr/bin/env python3
"""Synchronize the accepted three-case transition and seven-case continuation."""
from pathlib import Path
from collections import Counter
import ast, csv, hashlib, json, re, shutil, sys
from pypdf import PdfReader
from frontier_20261027 import ROOT, DATE, EVIDENCE, LEDGER, REMAINING, COUNTS, apply_profiles, read, write, sha

D=ROOT/'site/dist'
def info(path):
 p=Path(path);return {'sha256':sha(p),'bytes':p.stat().st_size}
def main():
 apply_profiles(ROOT)
 receipt=read(D/'data/rank9_m2_build.json')
 receipt.update(counts=COUNTS,ledger_sha256=sha(ROOT/LEDGER),frontier_continuation=EVIDENCE)
 write(D/'data/rank9_m2_build.json',receipt)
 # Publish exactly seven tensors; the replay archive retains its original ten.
 module=ast.parse((ROOT/'data/current_remaining_cases.py').read_text())
 values={n.targets[0].id:ast.literal_eval(n.value)for n in module.body if isinstance(n,ast.Assign)}
 metadata={rid:values['METADATA'][rid]for rid in REMAINING}
 tensors={rid:values['TENSORS'][rid]for rid in REMAINING}
 text='"""Current unresolved fusion tensors. All seven general complex existence questions remain open.\nUnit X_0; N[i][j][k] is the coefficient of X_k in X_i*X_j.\n"""\n\nMETADATA = '+repr(metadata)+'\n\nTENSORS = '+repr(tensors)+'\n'
 (ROOT/'data/current_remaining_cases.py').write_text(text)
 shutil.copy2(ROOT/'data/current_remaining_cases.py',D/'downloads/current_remaining_cases.py')
 # Current all-rank table; the lower-rank historical export has no rank-nine row.
 p=ROOT/'data/classification_summary_all_ranks.json';v=read(p);v['date']=DATE
 band=next(r for r in v['rows']if r['rank']==9 and r['multiplicity']==2)
 band.update(excluded_general=2046,unresolved_general=1)
 write(p,v)
 with (ROOT/'data/classification_summary_all_ranks.csv').open('w',newline='')as stream:
  writer=csv.DictWriter(stream,fieldnames=list(v['rows'][0]),lineterminator='\n');writer.writeheader();writer.writerows(v['rows'])
 # Canonical mathematical PDF mirrors.
 for relative in ('rank6/papers/manuscript.pdf','rank8/paper/rank8.pdf'):
  shutil.copy2(ROOT/'manuscripts'/relative,ROOT/'supplements'/relative)
 shutil.copy2(ROOT/'manuscripts/rank8/paper/rank8.pdf',ROOT/'manuscripts/rank8/paper/rank8-reviewed.pdf')
 shutil.copy2(ROOT/'manuscripts/rank8/paper/rank8.pdf',ROOT/'supplements/rank8/paper/rank8-reviewed.pdf')
 low=read(ROOT/'data/current_document_revision.json');low['date']=DATE
 low['documents']={n:item for n,item in low['documents'].items()if'prepublication-review-2026-10-25.'not in n}
 for n in ('manuscripts/prepublication-review-2026-10-27.tex','manuscripts/prepublication-review-2026-10-27.pdf',
           'manuscripts/rank6/papers/chapters/pairing_morita_20261027.tex','supplements/rank6/papers/chapters/pairing_morita_20261027.tex',
           'manuscripts/rank8/paper/pairing_frontier_20261027.tex','supplements/rank8/paper/pairing_frontier_20261027.tex'):
  low['documents'][n]=info(ROOT/n)
 for n in low['documents']:low['documents'][n]=info(ROOT/n)
 low['web_copies']={k:v for k,v in low['web_copies'].items()if'prepublication-review-'not in k}
 low['web_copies']['papers/prepublication-review-2026-10-27.pdf']='manuscripts/prepublication-review-2026-10-27.pdf'
 low['frontier_continuation']=EVIDENCE+'/accepted.json';write(ROOT/'data/current_document_revision.json',low)
 high=read(ROOT/'data/current_publication_revision.json')
 high.update(date=DATE,remaining_ids=REMAINING,current_unresolved_total=7)
 high['documents']={n:item for n,item in high['documents'].items()if'prepublication-review-2026-10-25.'not in n}
 high['documents'].update(low['documents'])
 high['documents']['publications/rank9-m2/paper/galois_pairing_20261027.tex']=info(ROOT/'publications/rank9-m2/paper/galois_pairing_20261027.tex')
 for n in high['documents']:high['documents'][n]=info(ROOT/n)
 high['web_copies']={k:v for k,v in high['web_copies'].items()if'prepublication-review-'not in k}
 high['web_copies'].update(low['web_copies'])
 high['rank9_m2'].update(excluded=2046,unresolved=1,ledger=LEDGER,**info(ROOT/LEDGER))
 high['frontier_continuation']={'date':DATE,'accepted':EVIDENCE+'/accepted.json',
  'general_exclusions':['R9_2_1607','R9_2_1975','R9_2_1976'],'remaining_ids':REMAINING,
  'replay_archive':'site/dist/downloads/Seven-Fusion-Rings-Proofs-and-Checks.zip',
  'replay_archive_sha256':sha(D/'downloads/Seven-Fusion-Rings-Proofs-and-Checks.zip')}
 write(ROOT/'data/current_publication_revision.json',high)
 for name,v in [('current_document_revision.json',low),('current_publication_revision.json',high)]:
  shutil.copy2(ROOT/'data'/name,D/'data'/name)
  for web,source in v['web_copies'].items():
   (D/web).parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/source,D/web)
 # Refresh all existing page inventories from the actual compiled bytes.
 for name in ('manuscript_page_counts.json','current_manuscript_page_counts.json'):
  p=ROOT/'data'/name;v=read(p);v['date']=DATE
  for row in v['documents']:
   if row['kind']=='research_status_report':
    row['path']='manuscripts/prepublication-review-2026-10-27.pdf';row['title']='Seven unresolved rings: audit and theoretical continuation'
   file=ROOT/row['path'];row.update(info(file),pages=len(PdfReader(file).pages))
  totals=Counter()
  for row in v['documents']:totals[row['kind']]+=row['pages']
  v['totals'].update(dict(totals));v['totals']['all_distinct_documents']=sum(totals.values())
  v['totals']['mathematical_manuscripts_and_guides']=totals['mathematical_manuscript']+totals['verification_guide']
  write(p,v);shutil.copy2(p,D/'downloads'/name)
 pointer={'path':'data/current_publication_revision.json','sha256':sha(ROOT/'data/current_publication_revision.json'),'date':DATE}
 for name in ('rank9_m2.json','rank9_rank10_m1.json','rank11_m1.json','rank12_m1.json'):
  p=D/'data'/name;v=read(p);v['summary']['current_documents']=pointer
  if name=='rank9_m2.json':v['summary']['source_url']='https://github.com/sebastienpalcoux/grothendieck-ring-classification/tree/main/'+EVIDENCE
  write(p,v,compact=True)
 # Structural facts and tensors are unchanged; source records now have new proofs.
 sys.path.insert(0,str(ROOT/'site'))
 from build_ring_properties import build
 build()
 atlas=read(D/'data/atlas.json');atlas['snapshot']=DATE
 atlas['current_documents'].update(date=DATE,sha256=sha(ROOT/'data/current_document_revision.json'))
 atlas['current_publication_documents']=pointer
 atlas['frontier_continuation']={'date':DATE,'current_unresolved_total':7,'accepted':EVIDENCE+'/accepted.json'}
 atlas['reader_resources']['page_totals']=read(ROOT/'data/manuscript_page_counts.json')['totals']
 entry=atlas.get('rank6_release',{}).get('document_revision')
 if entry:
  source=ROOT/entry['source'];shutil.copy2(source,D/entry['path'])
  if source!=ROOT/entry['path']:shutil.copy2(source,ROOT/entry['path'])
  entry.update(date=DATE,sha256=sha(source))
 def refresh(value):
  if isinstance(value,dict):
   path=value.get('path')
   if isinstance(path,str)and(D/path).is_file()and'sha256'in value:
    value['sha256']=sha(D/path)
    if'bytes'in value:value['bytes']=(D/path).stat().st_size
   for child in value.values():refresh(child)
  elif isinstance(value,list):
   for child in value:refresh(child)
 refresh(atlas)
 for name in atlas.get('rank6_release',{}).get('documents',{}):atlas['rank6_release']['documents'][name]=sha(D/'papers'/name)
 write(D/'data/atlas.json',atlas);write(ROOT/'data/atlas.json',atlas)
 page=read(ROOT/'data/current_manuscript_page_counts.json');totals=page['totals']
 summary=f"{page['document_counts']['mathematical_manuscripts']} mathematical manuscripts: {totals['mathematical_manuscript']} pages; with the three verification guides: {totals['mathematical_manuscripts_and_guides']}; with the current research-status report: {totals['all_distinct_documents']}. Each distinct document is counted once."
 for p in D.glob('*.html'):
  s=p.read_text().replace('Current classification · 10 open questions','Current classification · 7 open questions')
  s=s.replace('All 10 open rings · Python tensors','All 7 open rings · Python tensors')
  s=s.replace('2,043 general exclusions, 36 unitary models and 4 unresolved','2,046 general exclusions, 36 unitary models and 1 unresolved')
  s=s.replace('papers/prepublication-review-2026-10-25.pdf','papers/prepublication-review-2026-10-27.pdf')
  s=s.replace('2,145 general exclusions, 76 unitary models and four unresolved cases','2,148 general exclusions, 76 unitary models and one unresolved case')
  s=s.replace('2,043 exclusions, 36 models and four unresolved','2,046 exclusions, 36 models and one unresolved')
  s=s.replace('The ten earlier open cases remain open.','That release had ten open cases; the 27 October continuation leaves seven.')
  s=re.sub(r'(<span id="manuscript-page-summary">).*?(</span>)',lambda m:m[1]+summary+m[2],s)
  s=re.sub(r'(<p class="scope-note" id="current-manuscript-page-summary">).*?(<a href=)',lambda m:m[1]+summary+' '+m[2],s,flags=re.S)
  if p.name=='index.html':
   note='<p class="scope-note" id="frontier-update">27 October: three further rank-nine exclusions; seven rings remain unresolved. The R1660–R941 construction is conditional, and every GH(C6,2) Morita route for R1768 is excluded. <a href="./review.html#frontier-20261027">Proofs and individual findings →</a></p>'
   s=re.sub(r'\s*<p class="scope-note" id="frontier-update">.*?</p>\s*','\n',s,flags=re.S)
   anchor='<p class="scope-note" id="fusion-census-status" hidden></p>';s=s.replace(anchor,anchor+'\n'+note)
  if p.name=='review.html':
   panel='<section class="review-panel" id="frontier-20261027"><h2>Audited continuation · 27 October 2026</h2><p>R9_2_1607, R9_2_1975 and R9_2_1976 are excluded over the complex numbers. Seven rings remain open: two at rank six, four at rank eight and one at rank nine. All three exclusions passed a fresh mathematical audit.</p><p>The seven-case continuation adds restrictions, with no additional model or full ring exclusion. In particular, a separable algebra 1+X in a hypothetical pseudo-unitary R1660 category would produce R941; neither is constructed. Every GH(C6,2) Morita construction of R1768 is ruled out, for any associator and algebra. Independent human verification remains pending.</p><p><a href="./papers/prepublication-review-2026-10-27.pdf">Current report · PDF</a> · <a href="https://github.com/sebastienpalcoux/grothendieck-ring-classification/blob/main/evidence/frontier_20261027/README.md">Individual proofs and exact replay ↗</a> · <a href="./downloads/Seven-Fusion-Rings-Proofs-and-Checks.zip" download>Frozen proofs and certificates · ZIP</a></p></section>'
   s=re.sub(r'\s*<section class="review-panel" id="frontier-20261027">.*?</section>\s*','\n',s,flags=re.S)
   at=s.find('</aside>',s.find('<main'))
   if at<0:raise ValueError('Missing review insertion point')
   s=s[:at+8]+'\n'+panel+'\n'+s[at+8:].lstrip()
   s=s.replace('Research status · 25 October 2026','Research status · 27 October 2026')
   s=s.replace('The ten open cases remain open.', 'The audit checkpoint had ten open cases; the subsequent three exclusions leave seven.')
   s=s.replace('For R1768 an actual twisted GH(C6,2) precursor now exists, but the required algebra 1+sigma remains unproved.', 'For R1768 the entire GH(C6,2) Morita family is excluded, for every associator and algebra; the twisted precursor is not a source-ring model.')
   s=s.replace('All 10 open fusion tensors','All 7 open fusion tensors')
   r9='<section id="rank-nine-m2"><details class="review-details"><summary>Rank nine · multiplicity two</summary><h3>Rank nine · multiplicity two</h3><p>All 2,083 supplied tensors have source-bound decisions: 2,046 general exclusions, 36 unitary models and one unresolved ring. The new exclusions are R9_2_1607, R9_2_1975 and R9_2_1976, each retained after a fresh audit.</p><p>Only R9_2_137 remains unresolved. Its forced nonpointed algebra returns to the known central-involution Morita module. Both TY signs retain exact feasible necessary-system witnesses after imposing the positive second indicators. These data do not construct compatible associators. General existence reduces to pseudo-unitary existence by the stated spherical/Galois step; braided existence is excluded.</p><p><a href="./papers/rank9-m2.pdf">Current manuscript</a> · <a href="./unresolved.html?rank=9&amp;m=2">One open case</a> · <a href="https://github.com/sebastienpalcoux/grothendieck-ring-classification/tree/main/evidence/frontier_20261027">Current proofs, audits and exact replay</a></p></details></section>'
   s=re.sub(r'<section id="rank-nine-m2">.*?</section>',lambda _:r9,s,flags=re.S)
  s=s.replace('Revised 26 October 2026: the classification through rank twelve, the constructions catalogue and all ten open cases.', 'The submitted 26 October overview covers classification through rank twelve and the constructions catalogue. Its ten-case frontier predates the three further exclusions; seven cases are currently open.')
  p.write_text(s)
 from version_catalogue import main as catalogue_version
 from version_assets import version_assets
 catalogue_version();version_assets()
 print('Synchronized three general exclusions, seven open cases, current manuscripts and source-bound website data.')

if __name__=='__main__':main()
