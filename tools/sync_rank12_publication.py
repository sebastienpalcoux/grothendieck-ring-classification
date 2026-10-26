#!/usr/bin/env python3
"""Refresh the current rank-twelve document selection without rewriting proofs."""
from pathlib import Path
from collections import Counter
import hashlib,json,shutil,sys
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'site/dist';REL='evidence/rank12_m1_20261026'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def main():
 E=ROOT/REL
 high=read(ROOT/'data/current_publication_revision.json');high['date']='2026-10-26'
 for name in ('rank12.tex','rank12.pdf'):
  p=ROOT/'publications/rank12/paper'/name
  high['documents'][p.relative_to(ROOT).as_posix()]={'sha256':sha(p),'bytes':p.stat().st_size}
 high['web_copies']['papers/rank12.pdf']='publications/rank12/paper/rank12.pdf'
 high['rank12_m1']=dict(date='2026-10-26',rank=12,multiplicity=1,rings=632,excluded_general=480,
  modeled=152,realized_unitary=151,realized_pseudo_unitary_unitarity_unproved=1,unresolved_general=0,
  ledger=REL+'/ledger.json',ledger_sha256=sha(E/'ledger.json'),
  proof_archive='site/dist/downloads/Rank12_M1_Completion_Evidence.zip',proof_archive_sha256=sha(D/'downloads/Rank12_M1_Completion_Evidence.zip'))
 write(ROOT/'data/current_publication_revision.json',high)
 shutil.copyfile(ROOT/'data/current_publication_revision.json',D/'data/current_publication_revision.json')
 shutil.copyfile(ROOT/'publications/rank12/paper/rank12.pdf',D/'papers/rank12.pdf')
 p=ROOT/'data/current_manuscript_page_counts.json';v=read(p);v['date']='2026-10-26'
 r=ROOT/'publications/rank12/paper/rank12.pdf'
 v['documents']=[d for d in v['documents']if d['path']!='publications/rank12/paper/rank12.pdf']
 v['documents'].append(dict(title='Rank twelve, multiplicity one',kind='mathematical_manuscript',path=r.relative_to(ROOT).as_posix(),pages=len(PdfReader(r).pages),bytes=r.stat().st_size,sha256=sha(r)))
 v['document_counts']['mathematical_manuscripts']=sum(d['kind']=='mathematical_manuscript'for d in v['documents'])
 c=Counter()
 for d in v['documents']:c[d['kind']]+=d['pages']
 v['totals']={**dict(c),'mathematical_manuscripts_and_guides':c['mathematical_manuscript']+c['verification_guide'],'all_distinct_documents':sum(c.values())}
 write(p,v);shutil.copyfile(p,D/'downloads/current_manuscript_page_counts.json')
 pointer=dict(path='data/current_publication_revision.json',sha256=sha(ROOT/'data/current_publication_revision.json'),date='2026-10-26')
 for name in ('rank9_rank10_m1.json','rank11_m1.json','rank9_m2.json'):
  p=D/'data'/name;x=read(p);x['summary']['current_documents']=pointer
  p.write_text(json.dumps(x,ensure_ascii=False,separators=(',',':'))+'\n')
 p=D/'data/atlas.json';x=read(p);x['current_publication_documents']=pointer
 p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
 write(ROOT/'data/rank12_classification.json',high['rank12_m1'])
 sys.path.insert(0,str(ROOT/'site'))
 from build_rank12 import build
 build()
 print('Current manuscript page totals:',v['totals'])
if __name__=='__main__':main()
