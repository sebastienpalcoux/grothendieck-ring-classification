#!/usr/bin/env python3
"""Exact small restriction checks for the symmetric-etale-summand parity test."""
import json
from pathlib import Path
import sympy as s
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
r=json.loads((HERE/'r1154_character_check.json').read_text())['rings'][1]
C=s.Matrix([[s.sympify(x) for x in row] for row in r['characters']])
f=[s.sympify(x) for x in r['formal_codegrees']]
sigma=lambda z:s.expand(z).subs(s.sqrt(5),-s.sqrt(5))
galois=[1,0,0,0,2,2,2,2,4,4]
assert all(s.simplify(sum(C[i,j]*galois[j] for j in range(10))-f[i]/sigma(f[i]))==0 for i in range(10))
low=[
 ('unit',[1,0,0,0,0,0,0,0,0,0]),
 ('Galois-unit',galois),
 ('real-f8',[1,0,0,0,2,2,1,1,4,3]),
 ('f10-first',[1,1,0,0,1,1,2,2,2,3]),
 ('f10-second',[1,1,0,0,1,1,2,2,2,3]),
 ('f40',[1,0,0,0,0,0,1,1,0,1]),
]
source=json.loads((ROOT/'evidence/rank8_frontier_20261021/central_integrality/integer_gram_1154.json').read_text())['low_columns']
def forget(v):
 # 1,u ->1; v,uv ->g; x,ux ->X4; vx,uvx ->X5; y ->X1+X2; vy ->X6+X7.
 return [v[0]+v[1],v[8],v[8],v[2]+v[3],v[4]+v[5],v[6]+v[7],v[9],v[9]]
for (name,v),idx in zip(low,[0,1,2,4,4,3]):
 assert forget(v)==source[idx],name
 assert all(v[j]%2==0 for j in [2,3,8]),name
 assert v[4]==v[5] and v[6]==v[7]
quartic=[]
for case in ['R8_3_928','R8_3_941']:
 p=ROOT/'evidence/unresolved_retry_20261024/proofs/unresolved11_20261024/inputs'/f'{case}.json'
 rec=json.loads(p.read_text());N=rec['fusion_tensor'];d=rec['invariants']['dual_indices']
 ind=json.loads((ROOT/f'evidence/rank8_frontier_20261021/noncommutative/certified_{case[-3:]}_h6_low0.json').read_text())['indicators']
 ind=[1]+ind
 neg=[j for j in range(8) if ind[j]==-1]
 total=[sum(N[i][d[i]][j] for i in range(8)) for j in range(8)]
 assert all(total[j]==0 for j in neg)
 quartic.append({'id':case,'second_indicators':ind,'negative_indices':neg,'restriction_of_I_unit':total,'negative_constituents_present':False})
receipt={'result':'PASS, no parity obstruction','rank10_selfdual_distinguished_restrictions':dict(low),'rank10_negative_indicator_indices':[2,3,8],'galois_character_ratio_identity_verified':True,'quartic_checks':quartic}
(HERE/'distinguished_parity.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('PASS: new parity test gives no contradiction for R1154, R928, or R941')
