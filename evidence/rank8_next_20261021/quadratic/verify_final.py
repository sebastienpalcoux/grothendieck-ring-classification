"""Re-run all exact stages and verify every mandatory regular-module control."""
import json,collections
from gram_discovery import HERE,require
from verify_sources import verify
from module_rows import run as module_rows
from morita_closure import run as morita_closure
from profile_closure import run as profile_closure
from trace_closure import run as trace_closure

def verify_final(replay=True):
 src=verify()
 if replay:
  module_rows();morita_closure();profile_closure();trace_closure()
 gram={(x['id'],x['candidate_index']):x for x in json.loads((HERE/'integral_gram.json').read_text())};final=json.loads((HERE/'profile_closure.json').read_text());traces=json.loads((HERE/'trace_closure.json').read_text());passed=[]
 for c in src['canonical_internal_end_positive_controls']:
  rid=c['id'];ai=c['candidate_index'];r=gram[(rid,ai)];B=c['induction_rows'];root=c['simple'];counts=collections.Counter(tuple(v)for i,v in enumerate(B)if i!=root)
  ns=[counts.get(tuple(v),0)for v in r['vectors']];require(sum(ns)==7,'every canonical row enumerated');fi=r['all_multiplicities'].index(ns)
  require(any(f['candidate_index']==ai and f['factor_index']==fi for f in final[rid]['surviving_factors']),'canonical factor survives final Morita closure')
  if rid in traces:require(any(f['candidate_index']==ai and f['factor_index']==fi and f['compatible_trace_assignment_indices']for p in traces[rid]['profiles']for f in p['factor_checks']),'canonical trace survives')
  passed.append({'id':rid,'simple':root,'candidate_index':ai,'factor_index':fi})
 summary={rid:{'initial_algebra_candidates':sum(k[0]==rid for k in gram),'final_algebra_candidates':r['surviving_algebras'],'final_induction_factors':r['factor_count'],'possible_module_dimension_profiles':r['profile_count'],'factors_with_complete_unique_fusion_actions':sum(f['full_rank_action']is not None for f in r['surviving_factors'])}for rid,r in final.items()}
 out={'general_complex_necessary_conditions_only':True,'no_new_ring_exclusion':True,'no_associator_or_algebra_structure_constructed':True,'all_exact_stages_replayed':replay,'canonical_controls_passed':passed,'summary':summary}
 (HERE/'verification.json').write_text(json.dumps(out,separators=(',',':'))+'\n');print(json.dumps(summary,indent=2));print('All 32 mandatory canonical internal-end controls survive.')
 return out
if __name__=='__main__':verify_final()
