"""Transparent per-residual effort inventory; computational limits stay limits.

Coverage labels are operational review aids, never nonexistence proofs or
automatic novelty claims. The mathematical classification remains unresolved.
"""
import collections,json
from pathlib import Path
from m3_campaign import REPO,OUT,require
BASELINE={'near_group','rank_two','zero_spectrum','lower_rank_subring','rank7_certified_subring','dnumber','noncomm_dnumber','integral_drinfeld','cyclotomic','involution_module','field_automorphisms','subring_dimension','primitive_codegree','one_spectrum','one_spectrum_m3'}

def bucket(a):
 outcome=str(a.get('outcome',a.get('status','unspecified'))).lower();scope=str(a.get('scope','')).lower();kind=a.get('attempt_kind','exclusion');stage=a.get('stage','')
 if 'ineligible' in outcome:return 'implementation_ineligible'
 if 'inapplicable' in outcome or outcome=='not_applicable':return 'scope_inapplicable'
 if a.get('completed') is False or 'interrupt' in outcome:return 'interrupted_incomplete'
 if any(x in outcome for x in ('timeout','budget_exhaust','time_limit')):return 'timeout'
 if any(x in outcome for x in ('memory','resource_limit','resource_bound','out_of_memory')) or a.get('exit_code') in (137,-9):return 'resource_limit'
 if 'budget' in outcome:return 'incomplete_enumeration_budget'
 if outcome in ('error','failed','exception'):return 'error'
 if 'eligib' in stage or outcome=='eligible':return 'eligibility_only'
 if kind!='construction' and ('unitary_primary3' in stage or scope in ('unitary','unitary_only')):
  if outcome in ('excluded','unitary_excluded'):return 'unitary_only_proved_obstruction'
  return 'heuristic_unitary_search'
 if kind!='construction' and scope=='pseudo_unitary_only' and a.get('effective_scope')!='general_complex_via_weak_integrality':
  if outcome in ('pseudo_unitary_obstruction','excluded'):return 'pseudo_unitary_only_proved_obstruction'
  if outcome in ('no_conclusion','no_obstruction','feasible_relaxation','no_exclusion','no_contradiction'):return 'completed_pseudo_unitary_exclusion_search'
  return 'other_pseudo_unitary_outcome'
 if kind=='construction':
  if 'heuristic' in scope or 'heuristic' in outcome or 'wzw' in stage.lower():return 'heuristic_model_search'
  if 'abstract' in outcome or 'uncategorified' in outcome or 'ring_lead' in outcome:return 'abstract_ring_lead_without_model'
  if outcome in ('no_conclusion','no_match','not_matched','negative','no_model','family_excluded','excluded','checked','completed','not_in_family','no_categorification_provided','no_match_in_tested_family','not_identified','no_ordinary_group_model','no_model_from_either_tested_family') or any(w in outcome for w in ('reject','exclude','no_match','not_realized','family_filter')):return 'completed_scoped_model_search_or_filter'
  return 'construction_attempt_with_explicit_scope'
 if outcome in ('excluded','certified_excluded'):return 'unintegrated_discovery_exclusion'
 if outcome in ('no_conclusion','survives','pass','checked','completed','no_obstruction','feasible_relaxation','feasible','no_exclusion','no_negative_witness','no_witness','no_contradiction') or 'no_conclusion' in outcome:return 'completed_scoped_exclusion_search'
 return 'other_recorded_outcome'

def audit(pending,attemptrows):
 profiles={r['id']:r for r in json.loads((OUT/'survivor_profiles.json').read_text())};attempts={r['id']:r for r in attemptrows};out=[]
 for row in pending:
  rid=row['id'];require(rid in profiles and rid in attempts,'missing residual profile/attempt identity');p=profiles[rid];a=attempts[rid]['attempts'];bins=collections.defaultdict(list)
  for item in a:bins[bucket(item)].append(item)
  completed={x['stage'] for x in bins['completed_scoped_exclusion_search']};new=completed-BASELINE;known=completed&BASELINE;pseudo={x['stage'] for x in bins['completed_pseudo_unitary_exclusion_search']};advanced={s for s in new if any(x in s for x in ('dimension','rotation','character','modular','convex','weighted','biquadratic','moment','spectrum','module'))}
  models=bins['completed_scoped_model_search_or_filter']+bins['construction_attempt_with_explicit_scope'];modelstages={x['stage'] for x in models+bins['abstract_ring_lead_without_model']};thin=[]
  if len(completed)<6:thin.append('fewer_than_six_completed_scoped_exclusion_methods')
  if len(new)<2:thin.append('fewer_than_two_completed_new_exclusion_methods')
  if len(modelstages)<4:thin.append('fewer_than_four_recorded_construction_methods')
  if bins['unintegrated_discovery_exclusion']:thin.append('discovery_claim_needs_accepted_manifest_reconciliation')
  notes=[]
  if not p['commutative']:notes.append('Noncommutative: commutative character/rotation criteria do not apply without an explicit reduction; scalar/weighted/central attempts are recorded separately.')
  if p.get('integral'):notes.append('Integral FP dimension '+str(p['global_dimension'])+'. An ordinary representation-ring scan only excludes that construction family, not all group-theoretical categories.')
  if row.get('unitary_status')=='excluded':notes.append('A source-bound obstruction excludes unitary categorification only. By Galindo-Hong-Rowell Theorem5.20, weakly group-theoretical fusion categories are completely unitary; hence any categorification here would also be non-weakly-group-theoretical. General complex existence remains unresolved.')
  if rid=='R8_3_731':
   require(row.get('unitary_status')=='excluded' and not p['proper_subrings'] and p.get('global_dimension')==660,'R731 conditional conclusion lacks required exact inputs')
   notes.append('The exact primary-three witness excludes unitary categorification. The tensor has no proper nontrivial closed based subring. ENO Proposition9.11 forces any weakly group-theoretical categorification to be Rep of a nonabelian finite simple group, hence unitary. Thus any complex categorification would be nonunitary and non-weakly-group-theoretical. General existence remains unresolved.')
  out.append({'id':rid,'tensor_sha256':row['tensor_sha256'],'classification_status':'unresolved','review_label':'broad_recorded_search_coverage_for_exotic_candidate_review' if not thin else 'further_coverage_or_reconciliation_needed','commutative':p['commutative'],'invertible_count':p['invertible_count'],'fp_dimensions_approx':p['fp_dimensions_approx'],'global_dimension_approx':p['global_dimension_approx'],**({'fp_dimensions':p['fp_dimensions'],'global_dimension':p['global_dimension']} if p.get('integral') else {}),'proper_subring_ranks':sorted({x['rank'] for x in p['proper_subrings']}),'attempt_count':len(a),'bucket_counts':dict(sorted((k,len(v)) for k,v in bins.items())),'completed_known_exclusion_methods':sorted(known),'completed_new_exclusion_methods':sorted(new),'completed_pseudo_unitary_exclusion_methods':sorted(pseudo),'completed_new_scoped_exclusion_methods':sorted(new|pseudo),'completed_advanced_exclusion_methods':sorted(advanced),'exact_tensor_models_compared':max([int(x.get('tested_tensors') or 0) for x in a if x.get('attempt_kind')=='construction']+[0]),'recorded_construction_methods':sorted(modelstages),'heuristic_construction_methods':sorted({x['stage'] for x in bins['heuristic_model_search']}),'thin_coverage_flags':thin,'family_notes':notes,'attempt_references':[{'stage':x['stage'],'source':x['source'],'outcome':x['outcome'],'bucket':bucket(x),'scope':x.get('scope'),'effective_scope':x.get('effective_scope')} for x in a],'limitations':['A timeout, interruption, implementation ineligibility or numerical no-negative result is not a passed exact criterion.','Failure of a bounded construction family is not a general construction obstruction.','Exotic-candidate review does not establish existence or novelty.']})
 return {'scope':'per-residual recorded research effort; general complex existence remains unresolved','records':out,'residual_count':len(out),'thin_coverage_ids':[x['id'] for x in out if x['thin_coverage_flags']],'no_completed_advanced_attempt_ids':[x['id'] for x in out if not x['completed_advanced_exclusion_methods']]}

def main():
 from finalize_m3 import reconcile,attempts
 ledger,summary=reconcile();pending=[r for r in ledger if r['multiplicity']==3 and r['status']=='unresolved'];rows=attempts(pending)
 require(rows==json.loads((OUT/'residual_attempts.json').read_text()),'saved residual attempts differ from original sources')
 current=audit(pending,rows);require(current==json.loads((OUT/'residual_audit.json').read_text()),'saved residual effort audit differs')
 print('PASS residual effort audit',len(pending),'records;',len(current['thin_coverage_ids']),'explicit coverage flags')
if __name__=='__main__':main()
