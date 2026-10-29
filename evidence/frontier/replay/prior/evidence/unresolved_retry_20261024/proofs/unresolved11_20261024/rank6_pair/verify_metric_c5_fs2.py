#!/usr/bin/env python3
"""Exact second FS indicator test; passing is necessary, not categorification."""
from pathlib import Path
import hashlib,json
SOURCE=Path(__file__).resolve().parents[1]/'rank10_case189/metric_modular_completion.py'
raw=SOURCE.read_text();scope={'__file__':str(SOURCE)}
exec(compile(raw.split('\nresults=[]',1)[0],str(SOURCE),'exec'),scope)
cv,mul,add,total,conj,enc=[scope[n] for n in ['cv','mul','add','total','conj','enc']]
S,T,dual,dims=scope['build'](1,2,1)
Q=scope['Q'];d,dp=scope['d'],scope['dp']
inv_d=[cv(1),mul(dp,dp)]+[mul(Q(1,4),add(1,dp))]*4+[mul(Q(1,4),add(1,mul(3,dp)))]*4+[scope['neg'](dp),mul(Q(-1,2),dp),mul(Q(-1,2),dp),mul(Q(-1,5),dp)]
assert all(mul(x,y)==cv(1) for x,y in zip(dims,inv_d))
D=total(mul(x,x) for x in dims);Dinv=mul(S[0][0],S[0][0]);assert mul(D,Dinv)==cv(1)
invS0=[mul(mul(10,d),x) for x in inv_d];assert all(mul(S[0][j],invS0[j])==cv(1) for j in range(14))
T2=[mul(x,x) for x in T];iT2=[conj(x) for x in T2]
A=[total(mul(mul(S[i][l],dims[i]),T2[i]) for i in range(14)) for l in range(14)]
B=[total(mul(mul(S[i][l],dims[i]),iT2[i]) for i in range(14)) for l in range(14)]
nu=[mul(Dinv,total(mul(mul(mul(conj(S[k][l]),invS0[l]),A[l]),B[l]) for l in range(14))) for k in range(14)]
viol=[k for k,v in enumerate(nu) if (v not in [cv(-1),cv(1)] if dual[k]==k else v!=cv(0))]
# If the independently exported full tensor is available, also evaluate the
# original double-sum formula directly, without factorization through S.
candidate=SOURCE.with_name('metric_candidate_q1_c2.json');direct=False
if candidate.exists():
 N=json.loads(candidate.read_text())['fusion_tensor']
 nu_direct=[mul(Dinv,total(mul(mul(mul(mul(N[i][j][k],dims[i]),dims[j]),T2[i]),iT2[j]) for i in range(14) for j in range(14))) for k in range(14)]
 assert nu_direct==nu;direct=True
receipt={'status':'PASS' if not viol else 'FAIL','source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'parameters':[1,2,1],'field':'Q(zeta5), basis1,zeta5,zeta5^2,zeta5^3','global_dimension':enc(D),'dual':dual,'second_indicators':[enc(x) for x in nu],'violating_labels':viol,'direct_tensor_double_sum_checked':direct,'scope':'Necessary modular-indicator test only; no category existence proved.'}
out=Path(__file__).with_name('metric_c5_fs2_certificate.json');out.write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
