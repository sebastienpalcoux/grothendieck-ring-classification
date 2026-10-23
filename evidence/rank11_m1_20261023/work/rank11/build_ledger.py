"""Assemble rank-eleven statuses only from explicitly accepted evidence paths."""
from pathlib import Path
import collections,csv,json,hashlib
from common import read,sha,require,dump,HERE

def load(rel):return json.load(open(HERE/rel))
def main():
    T=read();P={r['id']:r for r in load('profile.json')['11']['rings']}
    E=collections.defaultdict(list);M=collections.defaultdict(list)
    def ex(rows,certificate,proof,verifier,field='certificates',label=None):
        for r in rows:
            cs=r.get(field)
            if not cs:continue
            require(r['tensor_sha256']==sha(T[r['id']]),'exclusion input identity')
            if not isinstance(cs,list):cs=[cs]
            E[r['id']].append(dict(criterion=label or ', '.join(c.get('kind','exact obstruction')for c in cs),scope='no fusion category over C',certificate=certificate,proof=proof,verifier=verifier))
    ex(load('arithmetic/arithmetic.json')['records'],'arithmetic/arithmetic.json','arithmetic/THEORY.md','python work/rank11/arithmetic/run.py --verify-only')
    ex(load('criteria_audit/cyclic_results.json')['records'],'criteria_audit/cyclic_results.json','criteria_audit/CRITERIA_AUDIT.md','python work/rank11/criteria_audit/verify_cyclic_independent.py',field='certificate')
    ex(load('structural/baseline.json')['records'],'structural/baseline.json','structural/THEORY.md','python work/rank11/structural/verify_baseline.py')
    for name in ['zero_spectrum','one_spectrum']:
        x=load('structural/'+name+'.json');rows=x['records']if isinstance(x,dict)else x
        ex(rows,'structural/'+name+'.json','structural/THEORY.md','python work/rank11/structural/verify_baseline.py',field='certificate',label=name)
    ex(load('structural/module_exclusions_verified.json')['records'],'structural/module_exclusions_verified.json','structural/THEORY.md','python work/rank11/structural/verify_modules_independent.py',field='certificate')
    if (HERE/'structural/noncomm_exclusions_verified.json').exists():
        ex(load('structural/noncomm_exclusions_verified.json')['records'],'structural/noncomm_exclusions_verified.json','structural/THEORY.md','python work/rank11/structural/verify_noncomm_independent.py',field='certificate')
    ex(load('structural/inherited_solvability.json')['records'],'structural/inherited_solvability.json','structural/THEORY.md','python work/rank11/structural/inherited_solvability.py')
    rows=load('nonintegral/lattice_replay.json')['results']
    ex(rows,'nonintegral/spherical_lattice.json','nonintegral/THEORY.md','python work/rank11/nonintegral/verify_reduction.py && python work/rank11/nonintegral/verify_spherical_lattice.py',field='checks',label='all-spherical-dimension lattice obstruction')
    rows=load('nonintegral/two_character_certificates.json')
    for r in rows:r['accepted']={'kind':'two-character central-restriction obstruction'}
    ex(rows,'nonintegral/two_character_certificates.json','nonintegral/THEORY.md','python work/rank11/nonintegral/verify_reduction.py && python work/rank11/nonintegral/verify_two_character.py',field='accepted')
    for file in ['standard_models.json','v4_zest_models.json','su2_spin_models.json','twisted_cyclic_models.json']:
        if not(HERE/'known_models'/file).exists():continue
        for r in load('known_models/'+file):
            require(r['tensor_sha256']==sha(T[r['id']]),'model input identity')
            for m in r['models']:
                M[r['id']].append(dict(model=m.get('name',m.get('model')),scope='unitary realization exists',certificate='known_models/'+file,proof='known_models/THEORY.md',verifier='python work/rank11/arithmetic/model_audit.py'))
    # Additional proofs enter only via an explicit root-reviewed manifest.
    if(HERE/'additional_accepted.json').exists():
        for r in load('additional_accepted.json'):
            require(r['tensor_sha256']==sha(T[r['id']]),'additional accepted input identity')
            require(r['status']in['excluded','unitarily_realized'],'accepted status')
            (E if r['status']=='excluded'else M)[r['id']].append(r['evidence'])
    require(not(set(E)&set(M)),f'contradictory statuses {set(E)&set(M)}')
    rows=[]
    for rid,R in T.items():
        p=P[rid];status='excluded'if rid in E else'unitarily_realized'if rid in M else'in_progress'
        rows.append(dict(id=rid,input_line=p['line'],rank=11,multiplicity=1,status=status,
          tensor_sha256_compact_json=sha(R),tensor_sha256_uint8_flattened=hashlib.sha256(bytes(v for a in R for b in a for v in b)).hexdigest(),
          commutative=p['commutative'],dual=p['dual'],fp_dimensions_approx=p['fp_dimensions_approx'],fp_dimension_approx=p['fp_dimension_approx'],
          exclusions=E.get(rid,[]),models=M.get(rid,[])))
    result=dict(input_count=182,counts=dict(collections.Counter(r['status']for r in rows)),records=rows)
    dump(HERE/'ledger.json',result)
    with open(HERE/'ledger.csv','w',newline='')as f:
        w=csv.writer(f);w.writerow(['id','input_line','status','evidence','proof','certificate','verifier','tensor_sha256_compact_json'])
        for r in rows:
            ev=(r['exclusions']or r['models']or[{}])[0]
            w.writerow([r['id'],r['input_line'],r['status'],ev.get('criterion',ev.get('model','')),ev.get('proof',''),ev.get('certificate',''),ev.get('verifier',''),r['tensor_sha256_compact_json']])
    print(result['counts']);print('Pending:',','.join(r['id']for r in rows if r['status']=='in_progress'))

if __name__=='__main__':main()
