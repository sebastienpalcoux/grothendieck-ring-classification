"""Read-only index reconciliation with the previously verified height-six campaign.

Uses the already-bound frozen certificate's labels; does not rerun its LP system.
"""
import argparse,hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
ap=argparse.ArgumentParser(description=__doc__)
ap.add_argument('--root',type=Path,default=HERE.parents[1]/'grothendieck-ring-classification')
args=ap.parse_args();root=args.root.resolve();P=root/'evidence/rank8_frontier_20261021'
def need(ok,msg):
    if not ok:raise RuntimeError(msg)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def object_digest(p):return hashlib.sha256(json.dumps(read(p),separators=(',',':')).encode()).hexdigest()
bp=HERE/'r1154_quartic_necessary_filters.json';pp=HERE/'r1154_quartic_coordinate_propagation.json';hp=P/'central_integrality/fixed_gram_rotation_1154_h6.json'
b=read(bp);p=read(pp);h=read(hp)
need(p['base_receipt_sha256']==digest(bp),'base receipt binding')
need(b['verifier_sha256']==digest(HERE/'r1154_quartic_necessary_filters.py'),'base verifier binding')
need(p['verifier_sha256']==digest(HERE/'r1154_quartic_coordinate_propagation.py'),'propagation verifier binding')
for name,expected in b['source_sha256'].items():need(digest(root/name)==expected,'source binding '+name)
need(h['metadata']['tensor_sha256']==b['tensor_sha256']==p['tensor_sha256'],'tensor binding')
need(h['metadata']['gram_domain_sha256']==object_digest(P/'central_integrality/integer_gram_1154.json'),'height6 Gram binding')
need(h['metadata']['filtered_domain_sha256']==object_digest(P/'noncommutative/central_integral_filters_1154.json'),'height6 cubic domain binding')
need(h['complete'] and not h['unresolved_indices'],'complete frozen classification')
full=set(h['metadata']['pattern_indices']);need(len(full)==1238,'full common domain')
covered=[];oldfail=[];oldpass=[]
for case in h['cases']:
    covered.extend(case['pattern_indices'])
    if case['kind']=='farkas_family':oldfail.extend(case['pattern_indices'])
    elif case['kind'] in ('individual_primal','primal_affine_family'):oldpass.extend(case['pattern_indices'])
    else:raise RuntimeError('unknown frozen case kind')
need(len(covered)==len(set(covered)) and set(covered)==full,'frozen disjoint complete partition')
oldfail=set(oldfail);oldpass=set(oldpass)
basefail={x['index'] for x in b['failures']};newfail={x['index'] for x in p['failures']};finalpass=set(p['survivor_indices'])
need(not(basefail&newfail) and basefail|newfail|finalpass==full and not((basefail|newfail)&finalpass),'new disjoint complete partition')
need(oldfail<=basefail,'old eight excluded at first coordinate stage')
result={'scope':'index-only reconciliation with a frozen independently verified height-six certificate; no rerun of its matrix system','id':b['id'],'tensor_sha256':b['tensor_sha256'],'common_cubic_pattern_domain':1238,'height6_excluded':len(oldfail),'height6_survived':len(oldpass),'height6_excluded_indices':sorted(oldfail),'quartic_stage1_excluded':len(basefail),'quartic_stage2_additional_excluded':len(newfail),'quartic_total_excluded':len(basefail|newfail),'height6_and_quartic_exclusion_intersection':len(oldfail&(basefail|newfail)),'height6_and_quartic_exclusion_union':len(oldfail|basefail|newfail),'new_exclusions_beyond_height6':len((basefail|newfail)-oldfail),'combined_remaining_patterns':len(oldpass&finalpass),'quartic_survivors_failing_height6':sorted(finalpass-oldpass),'combined_survivor_indices':sorted(oldpass&finalpass),'source_sha256':{str(hp.relative_to(root)):digest(hp)},'base_receipt_sha256':digest(bp),'propagation_receipt_sha256':digest(pp),'verifier_sha256':digest(Path(__file__))}
print(json.dumps(result,indent=2))
