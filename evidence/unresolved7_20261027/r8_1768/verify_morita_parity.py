"""Exact parity filter on the complete saved R1768 module factor list.

This is not a categorifiability test for R1768. It checks the finite part
of the theorem that its nonregular Morita representatives have no
quaternionic invertible simple.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib, importlib.util, json

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
def need(v,m):
    if not v: raise ValueError(m)
sources={
 'evidence/rank8_next_20261021/quadratic/profile_closure.json':
 '6b48256765fb6380a3080669b0d6b5c20f924f3c8277308aa036cc47c1e28140',
 'evidence/rank8_research_20261022/pointed_followup/r1768_modules/verification.json':
 'bf9cc03425acae958b9fe9a7a521350600614b5d3e8e44fbde424925edfcb11d'}
for p,h in sources.items():
    need(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h,'source binding '+p)
spec=importlib.util.spec_from_file_location('cases',ROOT/'data/current_remaining_cases.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
R=mod.TENSORS['R8_3_1768']
tensor_hash=hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()
need(tensor_hash=='240509807c67da437c86f2a51efeb831364734feb93ed18a1d2f32087ebc1af0','tensor hash')
d=[(1,0),(1,0),(5,1),(6,1),(7,1),(7,1),(6,1),(5,1)]
def mul(x,y):return (x[0]*y[0]+37*x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def div(x,y):
    n=y[0]**2-37*y[1]**2
    a,b=mul(x,(y[0],-y[1]));return F(a,n),F(b,n)
def dim(row):return tuple(sum(row[k]*d[k][j] for k in range(8)) for j in range(2))
for i in range(8):
    for j in range(8):
        need(mul(d[i],d[j])==dim(R[i][j]),'dimension character')
read=lambda p:json.loads((ROOT/p).read_text())
factors=read('evidence/rank8_next_20261021/quadratic/profile_closure.json')['R8_3_1768']['surviving_factors']
previous=read('evidence/rank8_research_20261022/pointed_followup/r1768_modules/verification.json')
keep={(f['candidate_index'],f['factor_index']) for f in previous['factor_filter'] if f['survives']}
need(len(keep)==21,'complete saved residual count')
results=[]
for f in factors:
    key=(f['candidate_index'],f['factor_index'])
    if key not in keep:continue
    B=f['B'];a=B[0];D=dim(a)
    need(D==tuple(map(int,f['root_dimension'])),'root dimension')
    need(all(sum(B[t][i]*B[t][j] for t in range(len(B)))==sum(a[k]*R[i][k][j] for k in range(8))
             for i in range(8) for j in range(8)),'induction Gram')
    ends=[div(mul(dim(row),dim(row)),D) for row in B]
    need(all(x.denominator==1 for pair in ends for x in pair),'integral quadratic dimensions')
    odd=[i for i,(_,b) in enumerate(ends) if b.numerator%2]
    units=[i for i,v in enumerate(ends) if v==(1,0)]
    need(bool(odd) != bool(units),'exact dichotomy')
    results.append({'candidate_index':key[0],'factor_index':key[1],'module_rank':len(B),
                    'internal_end_dimensions':[[int(x),int(y)] for x,y in ends],
                    'odd_coefficient_positions':odd,'unit_internal_end_positions':units,
                    'consequence': 'no quaternionic invertible in dual' if odd else 'regular module category'})
regular=[(r['candidate_index'],r['factor_index']) for r in results if r['unit_internal_end_positions']]
need(len(results)==21 and len(regular)==4,'result count')
need(regular==[(0,0),(26,15),(42,0),(46,19)],'regular positions')
# Source weighted total: 1-1 plus all six positive noninvertibles.
need(tuple(sum(d[k][j] for k in range(2,8)) for j in range(2))==(36,6),'T2=6u')
out={'result':'PASS','tensor_sha256':tensor_hash,'source_sha256':sources,
     'factors_checked':21,'nonregular_factors_forbid_quaternionic_invertibles':17,
     'regular_factors':4,'records':results,
     'categorical_conclusion':'No category with GH(C6,2) fusion rules is Morita equivalent to a categorification of R8_3_1768',
     'census_status':'unresolved'}
(HERE/'morita_parity_receipt.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS: 17 factors forbid quaternionic invertibles; 4 force regular modules; R1768 remains unresolved')
