"""Exact regression of the multiplicity-three continuation and status boundaries."""
from pathlib import Path
from fractions import Fraction as Q
import copy,json,time,itertools,collections
from unittest.mock import patch
import sympy as s
from exact import require,VerificationError
from rings import validate,permute
from existence import verify_ledger,positive_registry,structure_only_records,unresolved_existence,all_values
from near_group_inversion import inversion_rules,action_audit,models,verify as verify_model
from modular_frontier import verify_record
from character_induction import reciprocity_data,pruned_system,check_farkas,verify as check_pu
P=Path(__file__).resolve().parents[1]
(P/'verification/current').mkdir(parents=True,exist_ok=True)

def reject(fn):
    try:fn()
    except (VerificationError,ValueError,KeyError,IndexError):return
    raise RuntimeError('corrupted continuation data accepted')

def run():
    start=time.monotonic();rows={r['id']:r['N'] for r in json.load(open(P/'data/census.json'))}
    # These tests prove finite tensor properties, not categorifiability at every n.
    for n in (1,3,5,7):validate(inversion_rules(n))
    for n in (0,2,4,True,3.5):reject(lambda n=n:inversion_rules(n))
    verify_model();reference=models()[0];audit=action_audit()
    require(audit['trace_on_noninvertible_multiplicity_space']==1 and audit['positive_eigenspace_dimension']==3 and audit['negative_eigenspace_dimension']==2,'wrong source multiplicity eigenspaces')
    registry=json.load(open(P/'data/inversion_models.json'));rec=registry[0]
    require(rec['id']=='R6_3_218' and permute(rec['N'],rec['basis_permutation'])==rows['R6_3_218'],'wrong complete source identification')
    mutations=[]
    for field in ('N','action'):
        bad=copy.deepcopy(reference)
        if field=='N':bad['N'][2][2][2]+=1
        else:bad['action']['trace_on_noninvertible_multiplicity_space']=3
        with patch('near_group_inversion.models',return_value=[bad]):reject(verify_model)
        mutations.append(field)
    for tail in itertools.permutations(range(1,6)):
        validate(permute(rows['R6_3_218'],(0,)+tail))
    # Check a proof-critical exact separation and reject its zero replacement.
    saved=json.load(open(P/'certificates/multiplicity_three.json'))
    require(len(saved)==1 and saved[0]['id']=='R6_3_132','unexpected general allocation')
    cert=saved[0]['certificate'];pseudo=cert['sphere']['pseudo']
    require(cert['kind']=='oriented_signed' and len(cert['branches'])==16,'signed table inventory')
    require(len(pseudo['branches'])==172 and sum(not b.get('labellings') for b in pseudo['branches'])==168,'low matrix inventory')
    data,tab=reciprocity_data(rows['R6_3_132'])
    branch=next(b for b in pseudo['branches'] if b.get('rotation'))
    L=s.Matrix.hstack(*map(s.Matrix,branch['columns']));wit=branch['rotation'][0]
    A,b,_=pruned_system(rows['R6_3_132'],data,L,tuple(wit['indicators']),6,branch['galois'])
    check_farkas(A,b,wit['y']);reject(lambda:check_farkas(A,b,[0]*len(wit['y'])))
    # Checking of new structure-only proofs and the feasible point must not call an optimizer.
    def forbidden(*args,**kwargs):raise RuntimeError('numerical optimizer called by exact continuation checker')
    with patch('scipy.optimize.linprog',forbidden),patch('scipy.optimize.milp',forbidden):
        claims=structure_only_records()
        require(all(r['id'] in rows and r['structure'] in ('pivotal','spherical','pseudo_unitary') for r in claims),'structure-only inventory')
        for item in claims:
            if item['id'].startswith('R6_9_'):
                from replay_m9_structure import verify_record as verify_new_scope
                verify_new_scope(rows[item['id']],item)
            else:check_pu(rows[item['id']],item['certificate'])
        witness=json.load(open(P/'systems/integral_frontier_215.json'))
        require(witness['id']=='R6_3_215','wrong residual witness')
        result=verify_record(rows[witness['id']],witness)
        require(result['equations']==230 and result['variables']==199 and result['formal_central_rank']==22,'frontier counts changed')
        bad=copy.deepcopy(witness);bad['solution'][0]='-1'
        reject(lambda:verify_record(rows[witness['id']],bad))
        bad=copy.deepcopy(witness);bad['formal_central_rank']='23'
        reject(lambda:verify_record(rows[witness['id']],bad))
        bad=copy.deepcopy(witness);bad['spectrum']={}
        reject(lambda:verify_record(rows[witness['id']],bad))
    now=json.load(open(P/'data/decisions.json'));verify_ledger(now);by={r['id']:r for r in now}
    for rid in [r['id'] for r in claims]:
        expected=all_values('no') if by[rid]['status']=='excluded' else unresolved_existence(rid)
        require(by[rid]['status'] in ('excluded','unresolved') and by[rid]['existence']==expected,'structure-only exclusion overclaimed')
    bad=copy.deepcopy(now);next(r for r in bad if r['status']=='unresolved')['existence']['general']='no';reject(lambda:verify_ledger(bad))
    require(by['R6_2_124']['existence']==dict(general='yes',pivotal='yes',spherical='yes',pseudo_unitary='no',unitary='no'),'Schopieray fields altered')
    remaining=[r['id'] for r in now if r['m']==3 and r['status']=='unresolved']
    return dict(passed=True,optimized_python=not __debug__,seconds=time.monotonic()-start,
        checked_general_certificate='R6_3_132',checked_unitary_model='R6_3_218',
        structure_only_no_PU=[r['id'] for r in claims],remaining_multiplicity_three=remaining,
        frontier=result,source_record_mutations_rejected=mutations,source_relabellings_checked=120,
        corrupt_feasible_coordinates_rejected=True,corrupt_Galois_metadata_rejected=True,
        false_general_promotion_rejected=True,zero_Farkas_vector_rejected=True,
        numeric_optimization_disabled_for_structure_and_frontier_checks=True)

if __name__=='__main__':
    result=run();name='categorical_scope_controls_optimized.json' if not __debug__ else 'categorical_scope_controls_normal.json'
    (P/'verification/current'/name).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
