#!/usr/bin/env python3
"""Reconcile fourth-campaign domains, exact receipts, and canonical allocations.

This is an independent receipt/identity validator, not a mathematical verifier.
It never reads the current ledger to choose inputs, and never turns numerical
infeasibility, a timeout, a profile rejection, or a surviving point into a
categorical decision. --require-canonical binds every accepted certificate to
its source, frozen tensor domain, and optimized optimizer-disabled replay.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
PREFIX='research/round4/'
MANIFEST='verification/round4/campaign_manifest.json'
CANONICAL='certificates/continuation_round4.jsonl'
PROOF_SOURCES='verification/round4/proof_sources.json'
REPLAY='verification/round4/release_replay.json'
KINDS={
 'general_fibonacci_subfield_rotation':'fibonacci_projection',
 'general_ising_projection_rotation':'ising_projection',
 'general_cyclic_three_projection':'cyclic_three_projection',
 'general_half_e6_projection':'half_e6_projection',
 'general_half_e6_projection_rotation':'half_e6_projection',
 'general_half_e6_full_character_projection':'half_e6_projection',
}
CANDIDATE_SOURCES=[
 {'id':'R6_6_49','path':PREFIX+'higher/R6_6_49_general.json'},
 {'id':'R6_6_1035','path':PREFIX+'higher/R6_6_1035_general.json'},
 {'id':'R6_8_311','path':PREFIX+'m8/R6_8_311_certificate.json'},
 {'id':'R6_8_3664','path':PREFIX+'m8/R6_8_3664_certificate.json'},
]


def require(ok,message):
 if not ok:raise ValueError(message)


def order(rid):return tuple(map(int,rid.split('_')[1:]))
def histogram(rows):return dict(sorted(Counter(r['outcome'] for r in rows).items()))
def tensor_hash(N):return hashlib.sha256(json.dumps(N,separators=(',',':')).encode()).hexdigest()


class Sources:
 def __init__(self,root):self.root=Path(root);self.cache={};self.hashes={}
 def exists(self,path):return (self.root/path).is_file()
 def bind(self,path):
  raw=(self.root/path).read_bytes();digest=hashlib.sha256(raw).hexdigest()
  require(path not in self.hashes or self.hashes[path]==digest,'Source changed during aggregation: '+path)
  self.hashes[path]=digest;return raw
 def read(self,path):
  if path not in self.cache:
   raw=self.bind(path);self.cache[path]=[json.loads(x) for x in raw.splitlines() if x.strip()] if path.endswith('.jsonl') else json.loads(raw)
  return self.cache[path]
 def r(self,path):return self.read(PREFIX+path)
 def unchanged(self):
  for p,h in self.hashes.items():require(hashlib.sha256((self.root/p).read_bytes()).hexdigest()==h,'Source changed during aggregation: '+p)


def compact(row,source,outcome=None):
 r={'id':row['id'],'outcome':outcome or row.get('outcome','not_recorded'),'source':source}
 if outcome and row.get('outcome') and outcome!=row['outcome']:r['raw_outcome']=row['outcome']
 for k in ('reason','eligible','seconds','scope','height','conductor','tensor_sha256','input_kind','budget_seconds','wall_time_limit_seconds','exit_code','profile','rank','field','attempted_system','ising_labels','half_e6_subrings','cyclic_three_subrings'):
  if k in row:r[k]=row[k]
 return r


def build(root=ROOT,require_canonical=False):
 s=Sources(root);manifest=s.read(MANIFEST);ids=manifest['ids'];tensors=manifest['tensors']
 require(len(ids)==len(set(ids))==manifest['input_count']==10,'Expected frozen ten-input frontier')
 require({r['id'] for r in tensors}==set(ids) and len(tensors)==10,'Manifest tensor domain mismatch')
 census=s.read('data/census.json');require(len(census)==16612,'Unexpected census size');N={r['id']:r['N'] for r in census}
 require(all(r['N']==N[r['id']] for r in tensors),'Frozen full tensor differs from unchanged census')
 model=s.read('data/model_catalog.json');positive=[r['id'] for r in model]
 require(len(positive)==len(set(positive))==54 and not set(ids)&set(positive),'Invalid positive-control domain')
 domain=set(ids)|set(positive);allids=ids+positive
 prior=set()
 for p in ('certificates/classification.jsonl','certificates/continuation_20260929.jsonl','certificates/continuation_round2.jsonl','certificates/continuation_round3.jsonl'):
  prior.update(r['id'] for r in s.read(p) if r.get('status')=='excluded')
 require(not prior&set(ids),'Frozen input was already excluded before this campaign')
 previous=s.read('verification/round3/release_replay.json')
 require(previous['ledger_sha256']==manifest['previous_ledger_sha256'],'Manifest does not bind the preceding ledger')

 pending=[]
 source_index=s.read(PROOF_SOURCES) if s.exists(PROOF_SOURCES) else [r for r in CANDIDATE_SOURCES if s.exists(r['path'])]
 bysource={}
 for r in source_index:
  obj=s.read(r['path']);c=obj[r['field']] if r.get('field') else obj
  require(r['id'] in ids and isinstance(c,dict) and 'kind' in c,'Invalid proof-source entry')
  require(r['id'] not in bysource,'Repeated proof-source input')
  bysource[r['id']]=(r,c);pending.append({'id':r['id'],'kind':c['kind'],'source':r['path'],'criterion':KINDS.get(c['kind'],'unmapped_pending_kind')})
 allocated=[];frozen=s.exists(CANONICAL)
 require(frozen or not require_canonical,'Canonical fourth-campaign certificate file is not frozen')
 if frozen:
  records=s.read(CANONICAL)
  for r in records:
   require(r['id'] in ids and r.get('status')=='excluded' and r.get('exact_checked') is True,'Invalid canonical exclusion record')
   c=r['certificate'];kind=c['kind'];require(kind in KINDS,'Unmapped accepted certificate kind: '+kind)
   require(c.get('scope') in ('general','general_complex_fusion_categories'),'Canonical certificate is not general')
   require(r['id'] in bysource,'Canonical certificate has no independently listed proof source')
   source,original=bysource[r['id']];require(c==original,'Canonical proof differs from its complete source: '+r['id'])
   if r.get('source'):require(r['source']==source['path'],'Canonical source path mismatch')
   if r.get('source_sha256'):require(r['source_sha256']==s.hashes[source['path']],'Canonical source SHA-256 mismatch')
   if 'N' in r:require(r['N']==N[r['id']],'Canonical tensor mismatch')
   if r.get('tensor_sha256'):require(r['tensor_sha256']==tensor_hash(N[r['id']]),'Canonical tensor hash mismatch')
   allocated.append({'id':r['id'],'kind':kind,'criterion':KINDS[kind],'source':source['path'],'stage':r.get('stage')})
  require(len(allocated)==len({r['id'] for r in allocated}),'Repeated canonical allocation')
  require({r['id'] for r in allocated}==set(bysource),'Canonical/source domains differ')
  if require_canonical:require(s.exists(PROOF_SOURCES),'Missing independently frozen proof-source index')
 replay=None
 if frozen and s.exists(REPLAY):
  rr=s.read(REPLAY)
  require(rr.get('passed') is True and rr.get('optimized_python') is True and rr.get('optimizer_disabled') is True,'Unified exact replay did not pass under required conditions')
  require(rr['certificate_sha256']==s.hashes[CANONICAL],'Unified replay binds stale canonical bytes')
  require(set(rr['new_ids'])=={r['id'] for r in allocated} and rr['new_exclusions']==len(allocated),'Unified replay allocation domain mismatch')
  require(len(rr['replays'])==len(allocated) and {r['id'] for r in rr['replays']}==set(rr['new_ids']),'Unified replay has missing or duplicate records')
  for r in rr['replays']:
   require(r.get('passed') is True and r.get('optimized_python') is True and r.get('optimizer_disabled') is True,'Individual exact replay did not pass')
   require(r['kind']==next(a['kind'] for a in allocated if a['id']==r['id']),'Replay certificate kind mismatch')
  replay={k:rr[k] for k in ('passed','optimized_python','optimizer_disabled','certificate_sha256','new_exclusions','new_ids')}
 require(not require_canonical or replay is not None,'Missing complete exact canonical replay receipt')

 criteria=[]
 def add(key,title,application,rows,notes,**extra):
  require(len(rows)==len({r['id'] for r in rows}),'Duplicate effective input in '+key)
  require(all(r['id'] in domain for r in rows),'Criterion row outside frozen/control domain: '+key)
  for r in rows:
   if r.get('tensor_sha256'):require(r['tensor_sha256']==tensor_hash(N[r['id']]),'Wrong tensor hash in '+key)
  c={'id':key,'title':title,'application_domain':application,'effective_records':rows,
   'frontier_count':sum(r['id'] in ids for r in rows),'positive_count':sum(r['id'] in positive for r in rows),
   'frontier_outcomes':histogram([r for r in rows if r['id'] in ids]),'positive_outcomes':histogram([r for r in rows if r['id'] in positive]),
   'new_allocated_ids':[r['id'] for r in allocated if r['criterion']==key] if frozen else None,
   'pending_proof_ids':[r['id'] for r in pending if r['criterion']==key and r['id'] not in {a['id'] for a in allocated}],'notes':notes,**extra}
  criteria.append(c);return c
 def batch(key,title,path,notes,outcome_key='outcome',**extra):
  obj=s.r(path);raw=obj if isinstance(obj,list) else obj.get('records',obj.get('rows'))
  require(isinstance(raw,list) and len(raw)==64 and {r['id'] for r in raw}==domain,'Incomplete 10+54 domain: '+path)
  if isinstance(obj,dict) and 'complete' in obj:require(obj['complete'] is True,'Incomplete control receipt: '+path)
  rows=[compact(r,PREFIX+path,r.get(outcome_key,'not_recorded')) for r in raw]
  # A batch may report a discovered complete proof, but allocation remains canonical only.
  for r in rows:
   require(not (r['id'] in positive and r['outcome'] in ('excluded','general_exclusion','general_excluded','pseudo_unitary_excluded','general_proof_reported')),'Positive model falsely rejected in '+path)
   if r['outcome'] in ('general_exclusion','general_excluded'):r['raw_outcome']=r['outcome'];r['outcome']='general_proof_reported'
  return add(key,title,'all 10 frozen frontier tensors and all 54 positive controls',rows,notes,**extra)

 fib=batch('fibonacci_projection','Fibonacci subcategory projection and subfield traces','m8/controls.json',[
  'The 64-input batch checks implementation eligibility and bounded proof discovery; a general proof report is allocated only through the canonical file.',
  'The separate full-census screen detects a based Fibonacci subcategory only; it is not 16,612 exclusion runs.'])
 isi=batch('ising_projection','Ising twist support and projected masses','m8/ising_controls.json',[
  'targeted_campaign points to separate exact proofs or bounded searches; it is not a successful obstruction.',
  'The separate full-census screen is structural recognition only.'])
 for c,path,hitkey in [(fib,'m8/census_fibonacci_screen.json','fibonacci_based_subring_hits'),(isi,'m8/census_ising_screen.json','ising_based_subring_hits')]:
  z=s.r(path);require(z['screened']==16612 and len(z['rows'])==z[hitkey],'Incomplete census subcategory screen')
  require(len({r['id'] for r in z['rows']})==len(z['rows']) and all(r['id'] in N for r in z['rows']),'Invalid census recognition domain')
  c.update({'census_screened':16612,'structural_hits':z[hitkey],'structural_source':PREFIX+path,'structural_scope':z['scope'],'counts_by_multiplicity':z['counts_by_multiplicity']})

 half=batch('half_e6_mass','Half-E6 subcategory recognition and twist-resolved mass','higher/coverage.json',[
  'Subcategory recognition and full-character implementation eligibility are distinct.',
  'necessary_system_survives is a bounded discovery outcome; no exact primal point is inferred unless a separate receipt is cited.'],outcome_key='mass_outcome')
 if s.exists(PREFIX+'higher/e6_controls.json'):
  ec=s.r('higher/e6_controls.json');er=ec if isinstance(ec,list) else ec.get('records',ec.get('rows',[]))
  if len(er)==64:
   ep=batch('half_e6_projection','Full half-E6 projection and complex character moments','higher/e6_controls.json',[
    'This stronger criterion includes complete complex character/twist constraints beyond the separate coarse mass screen.',
    'Numerical survival or a budget interruption does not certify a primal point; the targeted general proof is separately replayed.'])
   if s.exists(PREFIX+'higher/e6_positive_retry.json'):
    retry=s.r('higher/e6_positive_retry.json')
    require(retry['id'] in positive and retry['outcome']=='necessary_system_survives','Unexpected half-E6 positive follow-up')
    ep['positive_followups']=[compact(retry,PREFIX+'higher/e6_positive_retry.json')]
    ep['notes'].append('The eligible positive R6_2_127 survives a separate 180-second follow-up; its original 20-second timeout remains recorded.')
 hc=s.r('higher/coverage.json');require(hc['false_positive_exclusions']==0,'A known positive model was rejected by the half-E6 control run')
 require(len(hc['cyclic_pointed_source_checks'])==6 and all(r['passed'] for r in hc['cyclic_pointed_source_checks']),'Incomplete cyclic associator/flux source validation')
 if s.exists(PREFIX+'higher/c3_controls.json'):
  z=s.r('higher/c3_controls.json');raw=z if isinstance(z,list) else z.get('records',z.get('rows',[]))
  if len(raw)==64:
   batch('cyclic_three_projection','Cyclic-three associators and projected twists','higher/c3_controls.json',[
    'All three pointed associators and their flux twist domains are retained.',
    'General exclusion is allocated only after the separate signed reduction and complete exact replay.'])
  else:
   rows=[compact(r,PREFIX+'higher/coverage.json','structurally_eligible' if r['cyclic_three_subrings'] else 'ineligible_no_subcategory') for r in hc['records']]
   add('cyclic_three_projection','Cyclic-three associators and projected twists','all 10+54 tensors screened structurally; full control run incomplete',rows,['The full discovery control file is still being completed.'],full_control_records_available=len(raw))
 else:
  rows=[compact(r,PREFIX+'higher/coverage.json','structurally_eligible' if r['cyclic_three_subrings'] else 'ineligible_no_subcategory') for r in hc['records']]
  add('cyclic_three_projection','Cyclic-three associators and projected twists','all 10+54 tensors screened structurally',rows,['Structural recognition is not a complete implementation/exclusion test.'])
 for key,title,path in [('complex_low_products','Complex low Verlinde and restriction products','m4_155/scan_controls.json'),('fourth_moments','Fourth moments and integer-square cuts','m4_155/scan_quartic_controls.json'),('central_invertible_transport','Central invertible transport','m4_155/scan_pointed_controls.json')]:
  batch(key,title,path,['Per-input discovery budgets are explicit. An exact rational control point certifies its equations, not a category.',
   'The dedicated R6_4_155 exact integral follow-ups supersede its short scan timeouts but do not alter the raw scan records.'])
 batch('odd_square_orbits','Squared-Galois orbit trace domain','m4_629/scan_orbit_scope.json',[
  'eligible_domain_constructed certifies construction of the finite trace domain only; it is not primal feasibility.',
  'This implementation requires odd dimension prime support; its two positive exact controls and target witness are separate.'])
 if s.exists(PREFIX+'quartic_front/applicability.json'):
  batch('quartic_profile_eligibility','Quartic full-character profile implementation eligibility','quartic_front/applicability.json',[
   'Eligibility requires a quartic FP field and a supported full-character cyclotomic realization of conductor at most 24.',
   'This scan constructs the eligible domain only. R6_8_1660 is eligible but its full profile enumeration was not executed; R6_8_311 is excluded by a separate criterion.',
   'Full low-frame profile certificates cover R6_4_22, R6_4_91, R6_4_629, and positive R6_4_322.'])

 # Exact survivor receipts are deliberately separate from proof allocations.
 w=s.r('m4_155/exact_primal_replay_optimized.json');wc=s.r('m4_155/exact_primal_certificates.json')
 require(w['passed'] and w['optimized_python'] and w['optimizer_used'] is False,'Failed complex exact survivor replay')
 require(len(w['records'])==len(wc['certificates'])==8 and all(r['passed'] and r['optimizer_used'] is False for r in w['records']),'Incomplete complex survivor replay')
 require(wc['tensor_sha256']==tensor_hash(N['R6_4_155']),'Complex survivor tensor hash mismatch')
 q=s.r('m4_155/quartic_exact_replay_optimized.json');qc=s.r('m4_155/quartic_exact_primal.json')
 require(q['passed'] and q['optimized_python'] and q['optimizer_used'] is False and q['all_coordinates_integral'],'Failed fourth-moment primal replay')
 require(qc['tensor_sha256']==tensor_hash(N['R6_4_155']) and qc['certificate']['rows']==q['equations'] and qc['certificate']['variables']==q['variables'],'Fourth-moment witness identity mismatch')
 add('complex_exact_survivors','Exact integral complex and fourth-moment survivors','one targeted input; nine exact witnesses',[
  {'id':'R6_4_155','outcome':'exact_integral_necessary_relaxation_survives','source':PREFIX+'m4_155/quartic_exact_primal.json','replay':PREFIX+'m4_155/quartic_exact_replay_optimized.json','equations':q['equations'],'variables':q['variables'],'relaxation_rank':q['center_rank'],'additional_witnesses':len(w['records'])}],
  ['All witnesses are checked with optimizers disabled under optimized Python. They are not complete center fusion rules, modular data, or a category.'])
 oddrows=[]
 for rid,path in [('R6_4_629','m4_629/probe_orbits_h3_replay_O.json'),('R6_1_11','m4_629/R6_1_11_orbit_h3_primal_replay.json'),('R6_5_17','m4_629/R6_5_17_orbit_h3_primal_replay.json')]:
  if not s.exists(PREFIX+path):continue
  z=s.r(path);require(z['passed'] and z.get('optimizer_used') is False,'Failed odd-orbit exact primal replay')
  oddrows.append({'id':rid,'outcome':'exact_necessary_relaxation_survives','source':PREFIX+path,'rows':z.get('rows'),'variables':z.get('variables'),'relaxation_rank':z.get('induction_rank')})
 add('odd_exact_survivors','Exact squared-orbit survivors','one targeted frontier input and two selected positive controls',oddrows,['These exact necessary-system points do not supply a complete modular datum or category.'])
 if s.exists(PREFIX+'m8/1660_witness_replay.json'):
  z=s.r('m8/1660_witness_replay.json');raw=s.r('m8/1660_necessary_witness.json')
  require(raw['exact_reconstruction_passed'] is True and z.get('passed') is True and z.get('optimizer_used') is False and z.get('optimized_python') is True,'R6_8_1660 exact primal reconstruction/replay failed')
  add('ising_exact_survivor','Exact rational Ising projected survivor','one targeted frontier input',[{'id':'R6_8_1660','outcome':'exact_rational_necessary_relaxation_survives','source':PREFIX+'m8/1660_necessary_witness.json','replay':PREFIX+'m8/1660_witness_replay.json','rows':raw['system']['equations'],'variables':raw['system']['variables']}],['The primal coordinates may be fractional. Their equations are exact; integral induction data and categorification are not asserted.'])

 if s.exists(PREFIX+'m8/1660_normalized_galois.json'):
  z=s.r('m8/1660_normalized_galois.json')
  require(z['outcome']=='exact_augmented_necessary_relaxation_survives' and z['existing_witness_failed_augmented_equations']==0,'Normalized-dimension witness balance failed')
  add('normalized_dimension_balance','Normalized squared-dimension Galois balance','one targeted frontier input',[{'id':'R6_8_1660','outcome':'exact_augmented_necessary_relaxation_survives','source':PREFIX+'m8/1660_normalized_galois.json','rows':z['equations'],'variables':z['variables'],'added_equations':z['added_equations']}],['These additional equations are checked exactly by the discovery/follow-up script. The separate optimizer-disabled replay covers the original 1,304-equation system.'])

 # Completed count-profile reductions have explicitly selected low frames.
 profrows=[]
 for rid in ('R6_4_22','R6_4_91'):
  p='quartic_front/'+rid+'_count_profiles.json';f='quartic_front/'+rid+'_filtered_profiles.json';ww='quartic_front/'+rid+'_word_profiles_h6.json'
  a=s.r(p);b=s.r(f);c=s.r(ww)
  require(a['complete'] is True and a['profiles']==len(a['counts']),'Incomplete selected-frame profile enumeration')
  require(all(r['input_profiles']==a['profiles'] for r in b),'Profile filter starts from wrong complete domain')
  require({tuple(r['lab']) for r in b}=={tuple(r['lab']) for r in c},'Labelled word-profile domain mismatch')
  row={'id':rid,'outcome':'finite_necessary_profiles_survive','source':PREFIX+ww,'enumeration_source':PREFIX+p,'initial_profiles':a['profiles'],'selected_low_frame_only':True,'labellings':[]}
  for r in c:
   prev=next(v for v in b if v['lab']==r['lab']);require({v['profile_index'] for v in r['survivors']} <= {v['profile_index'] for v in prev['accepted']},'Word filter adds a profile')
   row['labellings'].append({'labelling':r['lab'],'after_low_products':len(prev['accepted']),'after_words':len(r['survivors']),'word_height':r['height'],'surviving_indices':[v['profile_index'] for v in r['survivors']],'relaxation_ranks':sorted({v['rank'] for v in r['survivors']})})
  profrows.append(row)
 a=s.r('m4_629/profiles_summary.json');b=s.r('m4_629/filtered_profiles.json')
 require(a['complete'] is True and a['profiles']==b['complete_input_profiles'],'Odd profile enumeration incomplete')
 require(len(b['surviving_indices'])==len(b['counts']),'Odd profile survivors mismatch')
 profrows.append({'id':'R6_4_629','outcome':'finite_necessary_profiles_survive','source':PREFIX+'m4_629/filtered_profiles.json','enumeration_source':PREFIX+'m4_629/profiles_summary.json','initial_profiles':a['profiles'],'selected_low_frame_only':True,'low_frame':b['low_frame'],'labelling':b['lab'],'surviving_profiles':len(b['surviving_indices']),'surviving_indices':b['surviving_indices'],'depths':b['depths']})
 def profile_summary(c):
  require(c['kind']=='quartic_exact_induction_profiles' and c['categorification_claimed'] is False,'Wrong full profile certificate scope')
  cases=[]
  for ix,b in enumerate(c['branches']):
   if not b.get('cases'):continue
   require({tuple(v['labelling']) for v in b['cases']}=={tuple(v) for v in b['labellings']},'Missing full profile character labelling')
   count=len(b['gram_galois_profiles'])
   for v in b['cases']:
    require(len(v['rejected'])+len(v['survivors'])==count,'Full profile filter lost a branch')
    cases.append({'low_frame':ix,'labelling':v['labelling'],'initial_profiles':count,'surviving_profiles':len(v['survivors']),'relaxation_ranks':sorted({a['rank'] for a in v['survivors']})})
  return {'low_frames':len(c['branches']),'height':c['height'],'cases':cases}
 for row in profrows:
  if row['id']=='R6_4_629':
   path='m4_629/R6_4_629_exact_profiles.json';z=s.r(path);c=z['certificate']
   require(z['outcome']=='exact_necessary_profile_reduction' and z['optimized_python'] is True and z['optimizer_used'] is False,'Exact full profile reconstruction conditions missing')
   row['full_low_frame_receipt']={'source':PREFIX+path,**profile_summary(c),'optimizer_used':False,'optimized_python':True}
   rp='m4_629/fixed_twist_exact_replay_O.json';rr=s.r(rp)
   require(rr['passed'] is True and rr['optimized_python'] is True and rr['optimizer_used'] is False,'Odd-profile twist replay did not pass')
   labels={tuple(v['labelling']) for v in row['full_low_frame_receipt']['cases']}
   require({tuple(v['lab']) for v in rr['reports']}==labels and len(rr['reports'])==len(labels),'Odd twist replay misses character labelling')
   survivors=[];rejections=0;witnesses=0
   for r in rr['reports']:
    src='m4_629/'+r['file'];raw=s.r(src)
    require(raw['lab']==r['lab'] and set(raw['source_profiles'])==set(row['surviving_indices']),'Odd twist source profile domain differs')
    require(len(r['profiles'])==len(raw['branches'])==len(row['surviving_indices']),'Odd twist branch count mismatch')
    require({v['profile'] for v in r['profiles']}==set(raw['source_profiles']),'Odd twist replay profile identity mismatch')
    for v in r['profiles']:
     require(v['outcome'] in ('exact_linear_obstruction','exact_necessary_witness','no_exact_conclusion'),'Unrecognized odd twist outcome')
     if v['outcome']!='no_exact_conclusion':require(v['passed'] is True,'Unverified exact odd twist claim')
     if v['outcome']=='exact_linear_obstruction':rejections+=1
     else:
      witnesses+=v['outcome']=='exact_necessary_witness'
      survivors.append({'labelling':r['lab'],'profile_index':v['profile'],'rank':v['rank'],'outcome':v['outcome']})
   row['final_twist_refinement']={'source':PREFIX+rp,'rejected_labelled_profiles':rejections,'exact_necessary_witnesses':witnesses,'retained_labelled_profiles':survivors,'distinct_profile_count':len({v['profile_index'] for v in survivors}),'relaxation_ranks':sorted({v['rank'] for v in survivors}),'optimizer_used':False,'optimized_python':True}
  else:
   path='quartic_front/'+row['id']+'_frontier_certificate.json';z=s.r(path);c=z['certificate']
   require(c['kind']=='quartic_profile_frontier' and c['scope']=='general_necessary_profile_reduction' and c['categorification_claimed'] is False,'Invalid general profile frontier scope')
   rp='quartic_front/'+row['id']+'_frontier_replay_optimized.json'
   if not s.exists(PREFIX+rp):
    require(not require_canonical,'Missing optimized full-profile replay: '+row['id']);continue
   rr=s.r(rp)
   require(rr['passed'] is True and rr['optimizer_used'] is False and rr['optimized_python'] is True,'Full-profile frontier replay did not pass optimized and optimizer-free')
   require(rr['id']==row['id'] and rr['profile_report']['passed'] is True and rr['profile_report']['general_reduction']['galois_pseudo_unitary'] is True,'Full-profile replay identity/general scope mismatch')
   row['full_low_frame_receipt']={'source':PREFIX+path,**profile_summary(c['profiles']),'replay':PREFIX+rp,'optimizer_used':False,'optimized_python':True}
   expected={(v['low'],tuple(v['lab']),v['profile_index'],v['rank']) for v in c['cases'] if not any(k in v for k in ('congruence','ray'))}
   actual={(v['low'],tuple(v['labelling']),v['profile_index'],v['rank']) for v in rr['survivors']}
   require(expected==actual,'Profile frontier source/replay survivors differ')
   row['final_twist_refinement']={'source':PREFIX+rp,'preliminary_rays':rr['preliminary_rays'],'congruence_rejections':rr['congruence_rejections'],'branch_rejections':rr['branch_rejections'],'exact_necessary_witnesses':rr['exact_necessary_witnesses'],'retained_labelled_profiles':rr['survivors'],'distinct_profile_count':len({v['profile_index'] for v in rr['survivors']}),'relaxation_ranks':sorted({v['rank'] for v in rr['survivors']}),'optimizer_used':False,'optimized_python':True}
 if s.exists(PREFIX+'quartic_front/R6_4_322_control.json'):
  path='quartic_front/R6_4_322_control.json';z=s.r(path);require(z['id'] in positive and z['outcome']=='exact_necessary_profile_reduction','Invalid positive quartic control')
  ps=profile_summary(z['certificate']);require(any(v['surviving_profiles'] for v in ps['cases']),'Known positive quartic model lost all profiles')
  profrows.append({'id':z['id'],'outcome':'finite_necessary_profiles_survive','source':PREFIX+path,'full_low_frame_receipt':ps,'separate_optimizer_disabled_replay_claimed':False})
 add('finite_profiles','Exact finite count-profile reductions','three targeted frontier inputs and one positive control; complete low-frame domains',profrows,[
  'Historical experiments select a low frame. The later full_low_frame_receipt includes every low frame and compatible character labelling; final_twist_refinement retains only profiles not exactly rejected by the additional trace and congruence checks.',
  'A retained profile without an exact decision is not asserted feasible. R6_4_22 rank 30 and R6_4_629 rank 30 remain in this category.',
  'The positive R6_4_322 full-profile enumeration is an exact discovery control; no separate optimizer-disabled replay of that positive control is asserted.',
  'Individual integer-solver failures without independently checked proof certificates do not allocate exclusions.'])

 targeted=[]
 for path in ('higher/probe_1204_verlinde.json','higher/R6_6_1035_projection_mass.json','higher/R6_6_1035_projection_real_fast.json','higher/mass_verlinde_probe.json','m4_629/probe_orbits_h6_strong.json','m4_629/rank30_exact.json','m8/1660_ising_h6.json','m8/1660_ising_verlinde_h3_parity.json','m8/1660_integer_frames.json'):
  if s.exists(PREFIX+path):
   r=s.r(path)
   if isinstance(r,dict) and r.get('id') in ids:targeted.append(compact(r,PREFIX+path))
 # Preserve several experiments per input without violating effective-row uniqueness.
 rows=[]
 for rid in ids:
  runs=[r for r in targeted if r['id']==rid]
  if runs:rows.append({'id':rid,'outcome':'targeted_searches_recorded','source':runs[-1]['source'],'runs':runs})
 add('targeted_searches','Additional bounded refinements','selected frontier inputs; explicit per-experiment scope',rows,[
  'These search records are historical or exploratory even when another exact proof resolves the same tensor.',
  'resource_incomplete and budget_incomplete are not feasibility or nonexistence certificates.'])

 models=s.r('models/model_dimension_scan.json')
 require(models['manifest_sha256']==s.hashes[MANIFEST] and {r['id'] for r in models['frozen_inputs']}==set(ids),'Model audit uses wrong frozen frontier')
 require(models['constructors']==61 and models['distinct_model_ids']==54,'Model registry domain changed unexpectedly')
 for p,h in models['registry_sha256'].items():s.bind(p);require(s.hashes[p]==h,'Model constructor registry changed')
 add('model_comparison','Known-model and relative-center dimension comparisons','all ten frontier tensors; 61 constructors / 54 distinct model rings',[
  {'id':r['id'],'outcome':'no_match_in_tested_registry','source':PREFIX+'models/model_dimension_scan.json','tensor_sha256':r['tensor_sha256'],'proper_fusion_subsets':r['proper_fusion_subsets']} for r in models['frozen_inputs']],
  ['This is a dimension-level comparison with a specified registry, not a proof that no model exists.'],relative_center_dimension_checks=models['relative_center_dimension_checks'],matches=models['matches'])
 require(not models['matches'],'A positive match needs explicit coverage integration')
 morita=s.r('models/modular_morita_scope.json');require(morita['passed'],'Specific Morita-model check failed')
 other_audits=[]
 for p in sorted((s.root/PREFIX).rglob('*.json')):
  rel=str(p.relative_to(s.root))
  if rel in (PREFIX+'coverage.json',PREFIX+'coverage_structure.json'):continue
  if rel not in s.hashes:s.bind(rel);other_audits.append(rel)

 frontier=[]
 for rid in ids:
  evidence=[dict(r,criterion=c['id']) for c in criteria for r in c['effective_records'] if r['id']==rid]
  frontier.append({'id':rid,'tensor_sha256':tensor_hash(N[rid]),'canonical_allocation':next((r for r in allocated if r['id']==rid),None),'criterion_evidence':evidence})
 allocated_ids={r['id'] for r in allocated}
 bands=[{'multiplicity':m,'frozen_inputs':sum(order(r)[0]==m for r in ids),'canonical_new_exclusions':sum(order(r)[0]==m for r in allocated_ids) if frozen else None,'canonical_remaining':sum(order(r)[0]==m for r in set(ids)-allocated_ids) if frozen else None} for m in range(4,9)]
 report={'schema':'rank6-fourth-coverage/v1','status':'final' if require_canonical else 'interim','mathematical_replay_performed_by_aggregator':False,'canonical_allocation_available':frozen,'canonical_new_exclusions':len(allocated) if frozen else None,'canonical_remaining_count':len(ids)-len(allocated) if frozen else None,'canonical_remaining_ids':[r for r in ids if r not in allocated_ids] if frozen else None,'canonical_allocations':allocated,'unified_exact_replay':replay,'pending_proofs':pending,'pending_proof_count':len(pending),'frozen_input_ids':ids,'positive_control_ids':positive,'by_multiplicity':bands,'criteria':criteria,'frontier':frontier,'specific_morita_model_scope':{'source':PREFIX+'models/modular_morita_scope.json','scope':morita['scope'],'ids':[r['id'] for r in morita['cases']]},'additional_hashed_receipts':other_audits,'interpretation':[
  'The current decision ledger is not used to choose the campaign domain.',
  'Only canonical general certificates allocate exclusions; source, replay, and full-tensor identities are checked independently.',
  'Criterion counts overlap and must not be added to compute exclusions.',
  'Exact necessary-system points, finite surviving induction profiles, and modular-data candidates are different notions; none alone constructs a category.',
  'Structural recognition, implementation eligibility, bounded discovery, and complete proof replay are recorded separately.',
  'All additional JSON receipts in the fourth-round research directory are bound by SHA-256, including unsuccessful and interrupted attempts.']}
 report['submitted_proof_sources']=pending
 report['pending_proofs']=[r for r in pending if r['id'] not in allocated_ids]
 report['pending_proof_count']=len(report['pending_proofs'])
 report['source_sha256']=dict(sorted(s.hashes.items()));s.unchanged();return report


def markdown(r):
 lines=['# Fourth-continuation coverage','',f"**{r['status'].capitalize()} coverage report.** The domain is the frozen ten-tensor campaign manifest and 54 distinct positive controls; the current ledger is not used to select inputs.",'']
 if r['canonical_allocation_available']:
  lines+=[f"The canonical fourth-round file allocates **{r['canonical_new_exclusions']} new general exclusions**, leaving **{r['canonical_remaining_count']}** input rings unresolved. Only this canonical file supplies allocation counts.",'']
 else:lines+=[f"Canonical allocation is not yet frozen. The {r['pending_proof_count']} submitted proof sources are tracked separately and are not counted here as current classifications.",'']
 lines+=['Regenerate and independently validate the release receipts with:','','```sh','python research/round4/coverage.py --require-canonical','```','','The aggregator checks complete source/canonical equality, SHA-256 bindings, frozen full tensors, disjoint inherited allocations, complete input/control domains, and the optimized optimizer-disabled unified replay receipt. It does not rerun the mathematical checkers.','','| Multiplicity | Frozen inputs | New canonical exclusions | Remaining |','| ---: | ---: | ---: | ---: |']
 for b in r['by_multiplicity']:lines.append(f"| {b['multiplicity']} | {b['frozen_inputs']} | {b['canonical_new_exclusions'] if b['canonical_new_exclusions'] is not None else 'pending'} | {b['canonical_remaining'] if b['canonical_remaining'] is not None else 'pending'} |")
 def show(d):return '; '.join(k+': '+str(v) for k,v in d.items()) or 'outside this domain'
 lines+=['','## Criteria and application domains','','Counts from different criteria overlap. Structural screens are not full exclusion runs; a timeout is inconclusive.','','| Criterion | Domain | Frontier outcomes | Positive controls |','| --- | --- | --- | --- |']
 for c in r['criteria']:lines.append(f"| {c['title']} | {c['application_domain']} | {show(c['frontier_outcomes'])} | {show(c['positive_outcomes'])} |")
 lines+=['','## Finite reductions and exact survivors','','Full low-frame reconstructions and exact trace refinements leave the following necessary count profiles. Counts identify profiles independently of their character labellings; the JSON retains every labelled branch.','','| Input | Reduction | Remaining ranks | Exact necessary-system witnesses |','| --- | --- | --- | --- |','| `R6_4_22` | 93 → 3 by low products → 2 by words through degree six | 30, 36 | Rank 36; rank 30 undecided |','| `R6_4_91` | Low frame 0: 264 → 4, then all rejected by trace rays. Low frame 1: 524 → 6 → 2 by exact mod-2 constraints | 36, 42 | Both ranks |','| `R6_4_629` | 784 → 5 by low words → 3 by exact twist rays; one character labelling remains | 30, 35, 38 | Ranks 35 and 38; rank 30 undecided |','','These are reductions of necessary induction profiles, not exhaustive classifications of modular data. The positive control `R6_4_322` retains 24 profiles per labelling on its surviving low frame.','','`R6_4_155` has an exact integral rank-36 necessary-system point satisfying 7,764 equations in 9,982 variables, including fourth moments and central-invertible transport. The eight weaker integral witnesses and their exact optimized replays are retained. `R6_4_629` also has exact squared-orbit relaxation witnesses; `R6_8_1660` has an exact rational projected-Ising witness that satisfies 252 added normalized-dimension balance equations. None is asserted to be a fusion category.','','## Frozen frontier','','| Input | Canonical outcome | Recorded criterion domains |','| --- | --- | --- |']
 for f in r['frontier']:
  a=f['canonical_allocation'];out=a['kind'] if a else ('unresolved' if r['canonical_allocation_available'] else 'pending freeze')
  lines.append(f"| `{f['id']}` | {out} | {len(f['criterion_evidence'])} |")
 lines+=['','## Scope notes','']
 for c in r['criteria']:lines += ['**'+c['title']+'.** '+' '.join(c['notes']),'']
 lines += [f"The report binds {len(r['source_sha256'])} source files by SHA-256. Its inventory includes unsuccessful and interrupted experiments; these do not supply additional categorical allocations.",'']
 return '\n'.join(lines)


def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=ROOT);p.add_argument('--output',type=Path,default=Path(PREFIX+'coverage.json'));p.add_argument('--readme',type=Path,default=Path(PREFIX+'README.md'));p.add_argument('--require-canonical',action='store_true');a=p.parse_args();r=build(a.root,a.require_canonical)
 out=a.output if a.output.is_absolute() else a.root/a.output;readme=a.readme if a.readme.is_absolute() else a.root/a.readme;out.write_text(json.dumps(r,indent=2)+'\n');readme.write_text(markdown(r)+'\n');print(json.dumps({'status':r['status'],'canonical':r['canonical_allocation_available'],'new_exclusions':r['canonical_new_exclusions'],'criteria':len(r['criteria']),'sources':len(r['source_sha256'])},indent=2))
if __name__=='__main__':main()
