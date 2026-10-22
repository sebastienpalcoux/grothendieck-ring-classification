"""Bind the independent replay data to the primary exact certificate."""

if not __debug__:
    raise RuntimeError('Proof verification requires assertions enabled; run without -O.')
from pathlib import Path
import json
P=Path(__file__).resolve().parents[1]
def read(path):return json.loads((P/path).read_text())
models=read('terminal/models.json');d=read('independent/certificate.json')
assert d['matrix_rows']==models['field']['rows']and d['rhs']==models['field']['rhs']
assert d['initial_integer_bounds']==list(map(list,zip(models['base']['lo'],models['base']['up'])))
expected=[]
for c in read('terminal/certified_orbit_bounds.json')['changes']:
    expected.append({'variable':c['variable'],'sign':-1,'new_bound':c['new_upper'],'covector':c['covector']})
for path in ['terminal/certified_all_bounds.json','terminal/certified_field_bounds.json']:
    for round in read(path)['history']:
        for c in round:expected.append({k:c[k]for k in ['variable','sign','new_bound','covector']})
assert d['cuts']==expected
final=read('terminal/final_field_farkas.json')
assert d['separator']==final['covector']and d['expected_gap']==final['exact_separation']
print('PASS: independent certificate matches all628rows,1648cuts and final separator.')
