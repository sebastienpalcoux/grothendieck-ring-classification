#!/usr/bin/env python3
"""Verify the three accepted transitions, seven-case frontier and source bindings."""
from pathlib import Path
from collections import Counter
import argparse, ast, hashlib, json, sys
from frontier_20261027 import ROOT, EVIDENCE, LEDGER, EXCLUDED, REMAINING, COUNTS, read, sha

def need(ok,message):
 if not ok:raise ValueError(message)

def main(metadata_only=False):
 accepted=read(ROOT/EVIDENCE/'accepted.json')
 need(accepted['schema']=='frontier-20261027/v1'and accepted['date']=='2026-10-27','Accepted stage identity')
 old=read(ROOT/'evidence/rank9_m2_20261024/ledger.json');new=read(ROOT/LEDGER)
 need(len(old)==len(new)==2083,'Rank-nine exact census coverage')
 changed=[]
 for a,b in zip(old,new):
  need(a['id']==b['id']and a['tensor_sha256']==b['tensor_sha256'],'Source tensor/order identity')
  if a!=b:
   changed.append(b['id']);need(a['status']=='unresolved'and b['status']=='excluded','Permitted decision transition')
   for key in set(a)|set(b):
    if key not in ('status','exclusion_certificates'):need(a.get(key)==b.get(key),'Unexpected ledger change: '+key)
 need(sorted(changed)==sorted(EXCLUDED),'Exactly three accepted transitions')
 need(dict(Counter(r['status']for r in new))==COUNTS,'Rank-nine exact partition')
 for item in accepted['transitions']:
  need(item['id']in EXCLUDED and sha(ROOT/item['proof'])==item['proof_sha256'],'Transition proof binding')
 archive=accepted['replay_archive'];need(sha(ROOT/archive['path'])==archive['sha256'],'Frozen replay identity')
 replay=accepted.get('exact_replay')
 if replay:
  need(sha(ROOT/replay['path'])==replay['sha256'],'Exact replay receipt identity')
  receipt=read(ROOT/replay['path'])
  need(receipt['status']=='PASS'and len(receipt['checks'])==14 and receipt['archive_sha256']==archive['sha256'],
       'Complete fourteen-check replay receipt')
 for name,h in accepted.get('source_sha256',{}).items():need(sha(ROOT/name)==h,'Accepted source binding: '+name)
 rows={}
 for name in ('unresolved_cases.json','rank9_m2.json'):
  for r in read(ROOT/'site/dist/data'/name)['cases']:rows[r['id']]=r
 need(sorted(rid for rid,r in rows.items()if r['status']=='unresolved')==sorted(REMAINING),'Exactly seven open cases')
 byid={r['id']:r for r in new}
 for rid in EXCLUDED:
  r=rows[rid];need(r['status']=='excluded'and set(r['categorification_scope']['level_status'].values())=={'excluded'},'General-complex scope: '+rid)
  decision=next(v for v in r['research']if v.get('title')=='Current accepted case decision')
  need(decision['data']==byid[rid],'Accepted per-case ledger identity: '+rid)
 high=read(ROOT/'data/current_publication_revision.json')
 need(high['remaining_ids']==REMAINING and high['current_unresolved_total']==7,'Publication frontier')
 tree=ast.parse((ROOT/'data/current_remaining_cases.py').read_text())
 values={n.targets[0].id:ast.literal_eval(n.value)for n in tree.body if isinstance(n,ast.Assign)}
 need(sorted(values['TENSORS'])==sorted(REMAINING),'Seven-case download')
 for rid,tensor in values['TENSORS'].items():need(rows[rid]['fusion_tensor']==tensor,'Current tensor download: '+rid)
 for manifest in ('current_document_revision.json','current_publication_revision.json'):
  v=read(ROOT/'data'/manifest)
  for path,item in v['documents'].items():
   p=ROOT/path;need(p.is_file()and sha(p)==item['sha256']and p.stat().st_size==item['bytes'],'Current document: '+path)
  for web,path in v['web_copies'].items():need((ROOT/path).read_bytes()==(ROOT/'site/dist'/web).read_bytes(),'Web PDF: '+web)
  need((ROOT/'data'/manifest).read_bytes()==(ROOT/'site/dist/data'/manifest).read_bytes(),'Web manifest: '+manifest)
 if not metadata_only:
  sys.path.insert(0,str(ROOT/'site'));from build_ring_properties import SOURCES,derive
  index=read(ROOT/'site/dist/data/ring_properties.json')
  for name in SOURCES:
   value=read(ROOT/'site/dist/data'/name);need(index['source_sha256'][name]==sha(ROOT/'site/dist/data'/name),'Property source binding: '+name)
   for r in value.get('records',value.get('cases',[])):
    T=r.get('fusion_tensor',r.get('tensor'));entry=index['records'][r['id']];expected=derive(T)
    need(entry['properties']==expected['properties']and entry['certificate']==expected['certificate'],'Exact ring properties: '+r['id'])
 result={'status':'METADATA_PASS'if metadata_only else'PASS','new_general_exclusions':3,'new_models':0,'unresolved':7,'scope':'Accepted transitions, current documents/tensors and exact structural properties; finite exclusion proofs replay separately in the frozen source context.'}
 print(json.dumps(result,indent=2));return result

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--metadata-only',action='store_true');a=p.parse_args();main(a.metadata_only)
