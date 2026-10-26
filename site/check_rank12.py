#!/usr/bin/env python3
"""Validate all rank-twelve case pages against the frozen accepted research."""
from pathlib import Path
from collections import Counter
import ast,hashlib,json,sys,zipfile
from check_cases import check_tensor,check_browser_integers
from build_rank12 import safe
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'site/dist';E=ROOT/'evidence/rank12_m1_20261026'
def need(v,m):
 if not v:raise ValueError(m)
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check():
 ledger=read(E/'ledger.json');rows=ledger['records'];by={r['id']:r for r in rows}
 data=read(D/'data/rank12_m1.json');summary=data['summary'];cases=data['cases']
 need([r['id']for r in cases]==['R12_1_'+str(i)for i in range(1,633)],'Physical input order')
 need(Counter(r['status']for r in cases)=={'excluded':480,'unitarily_realized':151,'pseudo_unitarily_realized':1},'Classification partition')
 need(summary['ledger_sha256']==sha(E/'ledger.json'),'Ledger binding')
 need(summary['remaining_ids']==[],'No unresolved rank-twelve input')
 check_browser_integers(data,'rank12_m1')
 flags=read(D/'data/ring_property_flags.json')
 for r in cases:
  rid=r['id'];check_tensor(r,D,require_character_presentation=False)
  need(r['research'][0]['data']==safe(by[rid]),'Complete original decision: '+rid)
  need(r['tensor_sha256']==by[rid]['tensor_sha256'],'Tensor binding: '+rid)
  need(flags['records'][rid]['tensor_sha256']==r['tensor_sha256'],'Structural flags: '+rid)
  levels=r['categorification_scope']['level_status']
  expected={k:('excluded'if r['status']=='excluded'else'realized')for k in ('general','pivotal','spherical','pseudo_unitary','unitary')}
  if rid=='R12_1_623':expected['unitary']='unresolved'
  need(levels==expected,'Categorical scope: '+rid)
  need(r['investigation_deferred']is False and r['summary']and r['evidence'],'Incomplete result: '+rid)
  for item in r['evidence']:need(sha(ROOT/item['path'])==item['sha256'],'Evidence identity: '+item['path'])
 model=next(r for r in cases if r['id']=='R12_1_623')
 need(model['existence']=='pseudo-unitary'and 'not established'in model['summary'],'R623 unitarity label')
 need((ROOT/'publications/rank12/paper/rank12.pdf').read_bytes()==(D/'papers/rank12.pdf').read_bytes(),'Canonical manuscript copy')
 manifest=read(ROOT/'data/current_publication_revision.json')
 for name in ('rank12.tex','rank12.pdf'):
  rel='publications/rank12/paper/'+name
  need(manifest['documents'][rel]['sha256']==sha(ROOT/rel),'Current manuscript identity')
 archive=D/'downloads/Rank12_M1_Completion_Evidence.zip'
 need(summary['archive']['sha256']==sha(archive),'Proof archive identity')
 with zipfile.ZipFile(archive)as z:
  need(z.testzip()is None,'Archive CRC')
  prefix='Rank12_M1_Final_Resolution_2026-10-26/'
  for line in z.read(prefix+'MANIFEST.sha256').decode().splitlines():
   h,path=line.split('  ',1)
   need(hashlib.sha256(z.read(prefix+path)).hexdigest()==h,'Archived evidence: '+path)
 print('Rank twelve PASS: all 632 case/tensor bindings, all exact evidence, 480 general exclusions, 151 unitary and one additional pseudo-unitary model; unitarity of R623 unproved.')
if __name__=='__main__':check()
