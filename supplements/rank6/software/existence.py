"""Five independent existence columns with justified implications, not a unitary default."""
from pathlib import Path
import json
from exact import require
ROOT=Path(__file__).resolve().parents[1]
STRUCTURES=('general','pivotal','spherical','pseudo_unitary','unitary')
REGISTRIES=('constructed_positive_models','group_theoretical_models',
            'additional_positive_models','complete_positive_models','literature_positive_models','fermionic_product_models','exceptional_g2_models','inversion_models','through7_positive_models','residual_positive_models')
POSITIVE_STATUSES=('unitarily_realized','spherically_realized_nonpseudounitary')

def all_values(value):return {k:value for k in STRUCTURES}

def records():
    for fn in REGISTRIES:
        for r in json.loads((ROOT/f'data/{fn}.json').read_text()):
            yield fn,r

def model_existence(record):
    # Historical registries contain only explicitly constructed unitary models.
    e=dict(record.get('existence',all_values('yes')))
    require(set(e)==set(STRUCTURES) and all(x in ('yes','no','unknown') for x in e.values()),'invalid existence metadata')
    validate_implications(e)
    return e

def validate_implications(e):
    # Stronger existence -> weaker existence. Its contrapositive applies to no.
    for stronger,weaker in [('unitary','pseudo_unitary'),('pseudo_unitary','spherical'),('spherical','pivotal'),('pivotal','general')]:
        require(not(e[stronger]=='yes' and e[weaker]!='yes'),'invalid upward existence inference')
        require(not(e[weaker]=='no' and e[stronger]!='no'),'invalid downward nonexistence inference')

def positive_registry():
    result={}
    for fn,r in records():
        e=model_existence(r)
        if r['id'] in result:
            require(result[r['id']]['existence']==e,'conflicting categorical structure for a ring')
            result[r['id']]['models'].append(r['name'])
        else:result[r['id']]={'models':[r['name']],'existence':e}
    return result

def status_from_existence(e):
    if e['unitary']=='yes':return 'unitarily_realized'
    if e['spherical']=='yes' and e['pseudo_unitary']=='no':return 'spherically_realized_nonpseudounitary'
    raise ValueError('positive status is not yet represented by this release schema')

def structure_only_records():
    path=ROOT/'certificates/structure_only.json'
    if not path.exists():return []
    rows=json.loads(path.read_text());seen=set()
    for r in rows:
        require(r['id'] not in seen and r['structure']=='pseudo_unitary','invalid or duplicate structure-only claim')
        seen.add(r['id'])
    return rows

def unresolved_existence(rid):
    result=all_values('unknown')
    if rid in {r['id'] for r in structure_only_records()}:
        result['pseudo_unitary']=result['unitary']='no'
    return result

def verify_ledger(ledger):
    positive=positive_registry()
    claims={r['id'] for r in structure_only_records()}
    # A later general exclusion strengthens an earlier structure-only result;
    # retain the latter certificate as compatible provenance.
    require(claims<={d['id'] for d in ledger if d['status'] in ('unresolved','excluded')},'structure-only certificate contradicts a positive allocation')
    require(all(d['existence']['pseudo_unitary']=='no' for d in ledger if d['id'] in claims),'structure-only certificate contradicts the categorical existence fields')
    for d in ledger:
        if d['status']=='excluded':expected=all_values('no')
        elif d['status']=='unresolved':expected=unresolved_existence(d['id'])
        else:
            require(d['id'] in positive,'positive ledger entry has no constructor')
            expected=positive[d['id']]['existence']
            require(d['status']==status_from_existence(expected),'status conflates non-pseudo-unitarity and unitary existence')
        require(d.get('existence')==expected,'five-status ledger mismatch')
        validate_implications(expected)
    require(set(positive)=={d['id'] for d in ledger if d['status'] in POSITIVE_STATUSES},'positive ledger coverage mismatch')
    return True
