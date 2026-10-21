"""Read-only terminal ledger for the final noncommutative finite campaigns."""
from pathlib import Path
from collections import Counter
import argparse,hashlib,json
HERE=Path(__file__).resolve().parent;FRONTIER=HERE.parent

def need(ok,msg):
    if not ok:raise ValueError(msg)

def read(name):return json.loads((FRONTIER/name).read_text())

def compute():
    prefix='r928_semion_rotation/'
    first=read(prefix+'results.json');pairs=read(prefix+'pair_rotation.json');integer=read(prefix+'integer_counts.json');support=read(prefix+'integer_support_lattice.json')
    joint=read(prefix+'joint_spectrum.json');charged=read(prefix+'charged_joint_spectrum.json');quadratic=read('noncommutative_joint_spectrum/results.json')
    tally=lambda rows,key:dict(sorted(Counter(r[key]['status']for r in rows).items()))
    a=tally(first['cases'],'decision');b=tally(pairs['cases'],'decision');d=tally(integer['cases'],'result');e=tally(support['cases'],'result')
    need(a=={'exact_feasible_relaxation':10,'exact_infeasible_relaxation':5},'complete15 moment branches')
    need(b=={'exact_feasible_relaxation':10},'complete10 correlated pair branches')
    need(d==e=={'exact_nonnegative_integer_witness':4,'integer_feasibility_unresolved':6},'precise bounded integer terminal outcomes')
    need(len(charged['cases'])==len(charged['surviving_allocation_indices'])==93 and len(charged['surviving_pattern_indices'])==68,'complete corrected charged joint spectrum')
    for rec in joint['records']:need(rec['complete_pattern_count']==343 and len(rec['surviving_indices'])==255,'complete quartic joint spectrum')
    for rec in quadratic['records']:need(rec['complete_input_pattern_count']==len(rec['surviving_indices'])==({721:4,1154:1238}[int(rec['id'].split('_')[-1])]),'complete quadratic joint spectrum')
    files=sorted([p for folder in[HERE,FRONTIER/'noncommutative_joint_spectrum']for p in folder.iterdir()if p.suffix in('.py','.json')and p.name!='final_campaign.json'])
    return {'status':'all_planned_semion_attempts_finished','planned_ids':['R8_3_721','R8_3_928','R8_3_941','R8_3_1154'],
        'pending_attempts':[],'unresolved_integer_feasibility':6,
        'scope':'terminal ledger of these explicitly bounded finite attempts, not a claim that categorifiability or all associators have been resolved',
        'records':[
            {'id':'R8_3_721','joint_spectrum':{'status':'exact_complete','input_patterns':4,'surviving_patterns':4}},
            {'id':'R8_3_928','joint_spectrum':{'status':'exact_complete','input_patterns':343,'surviving_patterns':255},
             'semion_fixed_moments':{'status':'exact_complete','outcomes':a},'correlated_semion_pairs':{'status':'exact_complete','outcomes':b},
             'bounded_integer_search':{'status':'bounded_attempt_finished','outcomes':d,'exact_integer_witness_indices':[40,49,186,191],
                'uncertified_integer_indices':[44,58,196,243,245,248],'numeric_negative_is_exclusion':False},
             'supported_modular_lattices':{'status':'exact_finite_tests_complete','tested_primes':[2,3,5,7,11,13],'new_exclusions':0}},
            {'id':'R8_3_941','joint_spectrum':{'status':'exact_complete','input_patterns':343,'surviving_patterns':255},
             'charged_joint_spectrum':{'status':'exact_complete','input_allocations':93,'surviving_allocations':93,'surviving_patterns':68}},
            {'id':'R8_3_1154','joint_spectrum':{'status':'exact_complete','input_patterns':1238,'surviving_patterns':1238}}],
        'canonical_no_argument_verifiers':['r928_semion_rotation/verify_all.py','r928_semion_rotation/charged_joint_spectrum.py','noncommutative_joint_spectrum/verify.py','r928_semion_rotation/final_campaign.py'],
        'dependencies_sha256':{str(p.relative_to(FRONTIER)):hashlib.sha256(p.read_bytes()).hexdigest()for p in files}}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--write',action='store_true');args=p.parse_args();out=compute();path=HERE/'final_campaign.json'
    if args.write:path.write_text(json.dumps(out,indent=2)+'\n')
    else:need(out==json.loads(path.read_text()),'terminal finite-campaign ledger or dependency changed')
    print('PASS terminal NC research ledger: four exact R928 integer witnesses; six integer branches explicitly unresolved')
