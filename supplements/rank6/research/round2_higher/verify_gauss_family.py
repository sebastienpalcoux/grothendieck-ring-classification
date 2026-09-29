"""Replay Gauss-family PU exclusion; audit controls, relabellings and tampering."""
import copy,json,sys,time
from pathlib import Path
P=Path(__file__).resolve().parents[2];sys.path.insert(0,str(P/'software'))
from exact import require,VerificationError
from new_gauss_family import certificate,verify,identify
from rings import permute
by={r['id']:r['N'] for r in json.load(open(P/'data/census.json'))}
R=by['R6_8_6520'];c=json.load(open(Path(__file__).with_name('R6_8_6520_pseudo.json')))['certificate']
t=time.monotonic();verify(R,c)
controls=[r for r in json.load(open(P/'data/decisions.json')) if r['status'] in ('unitarily_realized','spherically_realized_nonpseudounitary')]
require(len(controls)==54,'positive controls changed')
require(all(certificate(by[r['id']]) is None for r in controls),'positive control excluded')
p=[0,5,3,1,4,2];S=permute(R,p);d=certificate(S);require(d is not None,'relabelling lost criterion');verify(S,d)
tests=[]
for label,mutator in [
 ('root_count',lambda x:x.__setitem__('uniform_root_count',x['uniform_root_count']+1)),
 ('missing_high_column',lambda x:x['high_columns'][1].pop()),
 ('missing_low_branch',lambda x:x['low_enumeration']['branches'].pop()),
 ('false_conductor',lambda x:x['Gauss'].__setitem__('fundamental_conductor',1231)),
 ('false_coefficient_bound',lambda x:x['Gauss'].__setitem__('single_root_coefficient_bound','1/1227')),
 ('wrong_parameter',lambda x:x.__setitem__('parameter',6))]:
 d=copy.deepcopy(c);mutator(d)
 try:verify(R,d)
 except VerificationError:tests.append(label)
 else:raise RuntimeError('accepted tampering '+label)
S=copy.deepcopy(R);S[1][1][1]+=1
try:verify(S,c)
except VerificationError:tests.append('tensor')
else:raise RuntimeError('accepted tampered tensor')
ids=json.load(open(Path(__file__).with_name('input_ids.json')))
if isinstance(ids,dict):ids=ids['input_ids']
rows=[]
for rid in ids:
 a=identify(by[rid]);d=certificate(by[rid]) if a is not None else None
 rows.append({'id':rid,'family_parameter':a[0] if a else None,'PU_excluded':d is not None})
report={'optimized_python':not __debug__,'verified':'R6_8_6520','positive_controls_preserved':[r['id'] for r in controls],
 'permutation':p,'rejected_tampering':tests,'frozen_application':rows,'seconds':round(time.monotonic()-t,3)}
Path(__file__).with_name('gauss_verification_optimized.json' if not __debug__ else 'gauss_verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ('positive_controls_preserved','frozen_application')}))
print('Frozen family cases', [r for r in rows if r['family_parameter'] is not None])
