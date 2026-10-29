#!/usr/bin/env python3
"""Exact exponent replay of the proved six-dimensional STS block lemma."""
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
N=1728
rows=[]
for pattern,outside in [(186,[288,1512,720]),(40,[288,1512,936,720])]:
    checks=[]
    for alpha in [162,378]:
        for lam in outside:
            residue=(4*alpha+lam-432)%N
            checks.append({'H_initial_exponent':alpha,'outside_pair_twist':lam,'STS_residue':residue})
    surviving=[r for r in checks if r['STS_residue']==0]
    if surviving!=[{'H_initial_exponent':162,'outside_pair_twist':1512,'STS_residue':0}]:
        raise ValueError('Unexpected STS block outcome')
    rows.append({'pattern':pattern,'checks':checks,'surviving':surviving})
output={'status':'PASS','modulus':N,'categorical_lemma':'REPORT.md section6',
        'claim':'a^4 lambda=xi^2=i; each remaining pattern has one T multiset and matching',
        'scope':'necessary data only; R928 remains unresolved','patterns':rows}
(HERE/'six_dimensional_block_verification.json').write_text(json.dumps(output,indent=2)+'\n')
print('PASS: patterns40,186 each retain one phase multiset and matching.')
