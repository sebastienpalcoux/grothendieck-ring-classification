"""Frozen-input, optimized-safe controls for the trace-ideal criterion."""
import copy,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'software'))
from exact import require,VerificationError
import new_trace_ideal as t
rows={r['id']:r for r in json.load(open(ROOT/'data/census.json'))}
inputs=json.load(open(ROOT/'verification/round2/campaign_manifest.json'))['inputs']
positive=[r['id'] for r in json.load(open(ROOT/'data/decisions.json')) if r['existence']['general']=='yes']
require(len(positive)==54,'positive control set changed')
for id in positive:require(t.certificate(rows[id]['N']) is None,'positive excluded')
found=[]
for row in inputs:
 c=t.certificate(row['N'])
 if c:t.verify(row['N'],c);found.append(row['id'])
id='R6_8_6997';R=rows[id]['N'];c=t.certificate(R);t.verify(R,c)
p=[0,3,2,5,1,4];P=[[[R[p[i]][p[j]][p[k]] for k in range(6)] for j in range(6)] for i in range(6)]
t.verify(P,c)
mut=[]
for field in ['dimension_trace_multiple','original_Casimir_trace','deficit_budget']:
 z=copy.deepcopy(c);z['arithmetic'][field]+=1
 try:t.verify(R,z)
 except VerificationError:mut.append(field)
 else:raise RuntimeError('tampered certificate accepted')
red=json.load(open(ROOT/'research/round2_external/R6_8_6520_trace_ideal.json'))['reduction'];t.verify_reduction(rows['R6_8_6520']['N'],red)
z=copy.deepcopy(red);z['signed_tables']=[]
try:t.verify_reduction(rows['R6_8_6520']['N'],z)
except VerificationError:mut.append('omitted_signed_table')
else:raise RuntimeError('omitted signed table accepted')
report={'frozen_residual_count':len(inputs),'direct_exclusions':found,'positive_controls':positive,'positive_controls_passed':len(positive),'basis_permutation':{'id':id,'permutation':p,'verified':True},'tampering_rejected':mut,'R6_8_6520_reduction_verified':True,'R6_8_6520_reduction_is_not_an_exclusion':True}
(ROOT/'research/round2_external/trace_ideal_audit.json').write_text(json.dumps(report,indent=2)+'\n')
(ROOT/'research/round2_external/R6_8_6997_general.json').write_text(json.dumps({'id':id,'certificate':c},indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='positive_controls'},indent=2))
