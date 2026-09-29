"""Detect the necessary scalar-third condition in frozen residual/positive domains.

Scope: pseudo-unitary. If Hom(1,X^3) is one-dimensional and 3 is absent
from the global-dimension norm, nu3(X)=1. This is not an exclusion test.
"""
import sys,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];BASE=Path(__file__).parent;sys.path.insert(0,str(ROOT/'software'))
from rings import Characters,dual
rows={r['id']:r for r in json.load(open(ROOT/'data/census.json'))};inputs=json.load(open(BASE/'campaign_inputs.json'));out=[]
for rid in inputs['residual_ids']+inputs['positive_ids']:
 R=rows[rid]['N'];du=dual(R);obj=[i for i in range(1,len(R)) if R[i][i][du[i]]==1]
 if not obj:out.append(dict(id=rid,outcome='ineligible_no_scalar_cubic_space'));continue
 try:pD=Characters(R).fp()[4]
 except Exception as e:out.append(dict(id=rid,outcome='arithmetic_unavailable',reason=type(e).__name__+': '+str(e)));continue
 norm=abs(int(pD.TC()))
 if norm%3==0:out.append(dict(id=rid,outcome='ineligible_exponent_support_contains_3',objects=obj));continue
 out.append(dict(id=rid,outcome='necessary_indicator_values',scope='pseudo_unitary',objects=obj,nu3=[1]*len(obj),global_dimension_norm=norm))
report={'scope':'necessary condition only; no exclusion or model claim','frozen_residual_inputs':len(inputs['residual_ids']),'frozen_positive_inputs':len(inputs['positive_ids']),'records':out}
(BASE/'scalar_third_scan.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps([x for x in out if x['id'] in inputs['residual_ids'] and x['outcome']=='necessary_indicator_values'],indent=2))
