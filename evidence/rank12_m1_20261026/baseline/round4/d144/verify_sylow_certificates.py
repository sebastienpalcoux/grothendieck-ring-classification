"""Replay positive and negative Liptrap certificates; no rank12 conclusion."""
from pathlib import Path
import sys,json
HERE=Path(__file__).resolve().parent
BASE=HERE.parents[1]/'prior_round/prior_round/evidence/rank12-m1-offline-20261025'
sys.path.insert(0,str(BASE))
import feudal
def need(v,msg):
    if not v:raise ValueError(msg)
Rp=json.loads((HERE/'sylow_a10.json').read_text())
cp=json.loads((HERE/'sylow_a10_test.json').read_text())['certificate']
vp=feudal.check_positive(Rp,cp)
Rn=json.loads((HERE/'sylow_a01.json').read_text())
cn=json.loads((HERE/'sylow_a01_obstruction_short.json').read_text())
z=feudal.setup(Rn,variable_tau=True)
need(len(z['assignments'])==1,'all nondegenerate bicharacters covered')
comb=cn['contradictions'][0]['row_combination']
coef={}
rhs=0
for row,m in comb:
    for k,c in z['equations'][row].items():coef[k]=coef.get(k,0)+m*c
    rhs+=m*z['B'][row][0]
need(all(c==0 for c in coef.values()),'all complex variables cancel integrally')
need(rhs%2==1,'contradiction 1=-1')
out=dict(scope='two dimension16 local candidate rings only; no rank12 case is excluded or realized by this file',
         positive_a10=vp,negative_a01=dict(equation_count=len(z['equations']),variable_count=len(z['keys']),
         relation_terms=len(comb),maximum_coefficient=max(abs(c)for r,c in comb),rhs_mod2=rhs%2,
         all_variable_coefficients_zero=True,all_bicharacter_assignments_covered=True,
         variable_tau=True,obstruction_over='complex numbers, without a phase-grid assumption'))
(HERE/'sylow_certificate_replay.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
