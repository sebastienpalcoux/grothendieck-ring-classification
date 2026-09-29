"""Replay exact biquadratic exclusions, known models, and negative controls."""
import copy
import hashlib
import itertools
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'software'))
import new_biquadratic_trace as b
from exact import VerificationError,require

rows=json.load(open(ROOT/'data/census.json'));byid={r['id']:r for r in rows}
manifest=ROOT/'verification/round2/campaign_manifest.json'
residuals=json.load(open(manifest))['inputs'] if manifest.exists() else json.load(open(ROOT/'data/unresolved_tensors.json'))
records=[];applicable=[]
for row in residuals:
    c=b.calculate(row['N'])
    if c is not None:
        applicable.append({'id':row['id'],'certificate':c})
        if c['excluded']:
            b.verify(row['N'],c)
            records.append({'id':row['id'],'certificate':c})
positive_ids=[r['id'] for r in json.load(open(ROOT/'data/decisions.json')) if r['existence']['general']=='yes']
require(len(positive_ids)==54,'positive control set changed')
for id in positive_ids:
    require(b.certificate(byid[id]['N']) is None,'known positive falsely excluded: '+id)
permutations=[];mutations=[]
for rec in records:
    id=rec['id'];R=byid[id]['N'];c=rec['certificate'];perm=[0,5,3,1,4,2]
    T=[[[R[perm[i]][perm[j]][perm[k]] for k in range(6)] for j in range(6)] for i in range(6)]
    require(b.calculate(T)==c,'nonportable tensor certificate')
    b.verify(T,c);permutations.append({'id':id,'basis_permutation':perm,'verified':True})
    for label,mutator in [('trace',lambda z:z['data'].__setitem__('casimir_trace',z['data']['casimir_trace']+1)),
                          ('field',lambda z:z['data'].__setitem__('p',z['data']['p']+2)),
                          ('claim',lambda z:z.__setitem__('excluded',False))]:
        bad=copy.deepcopy(c);mutator(bad)
        try:b.verify(R,bad)
        except VerificationError:mutations.append({'id':id,'mutation':label,'rejected':True})
        else:raise RuntimeError('tampered certificate accepted')
    badR=copy.deepcopy(R);badR[1][1][0]=0
    try:b.verify(badR,c)
    except VerificationError:mutations.append({'id':id,'mutation':'tensor_unit_pairing','rejected':True})
    else:raise RuntimeError('tampered tensor accepted')
# Independent imported regression: the audited B13 proof enumerates exactly1129.
B=json.load(open(ROOT/'research/round2_external/sources/B13_General_Exclusion/tensor.json'))
c=b.calculate(B)
require(c['totally_positive_candidates']==1129 and c['excluded'],'B13 regression failed')
require(len(c['norm_survivors'])==1 and c['norm_survivors'][0]['delta_numerator']==[14900,0,0,0],'B13 global dimension mismatch')
result={'scope':'general_complex_fusion_categories','residuals_checked':len(residuals),
        'input_ids':[r['id'] for r in residuals],
        'census_sha256':hashlib.sha256((ROOT/'data/census.json').read_bytes()).hexdigest(),
        'new_exclusions':[r['id'] for r in records],
        'positive_controls':positive_ids,'positive_controls_passed':len(positive_ids),
        'basis_permutation_controls':permutations,'tampering_controls':mutations,
        'B13_regression':{'totally_positive_candidates':1129,'norm_survivors':1,'excluded':True}}
(ROOT/'research/round2_external/biquadratic_trace_audit.json').write_text(json.dumps(result,indent=2)+'\n')
(ROOT/'certificates/biquadratic_exclusions.json').write_text(json.dumps({'certificates':records},indent=2)+'\n')
(ROOT/'research/round2_external/biquadratic_trace_scan.json').write_text(json.dumps({'checked':len(residuals),'applicable':applicable},indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['positive_controls','tampering_controls','input_ids','basis_permutation_controls']},indent=2))
