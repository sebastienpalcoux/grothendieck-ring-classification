"""Single-support induction cannot have zero categorical twist trace.

For X != 1, Tr(theta_{I(X)})=Dim(C)*nu_1(X)=0. If I(X)=m Z
for one central simple Z, its trace is m theta_Z dim(Z), which is nonzero.
This necessary obstruction uses no guessed twist order or numerical solver.
"""
import json,hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
def need(ok,msg):
    if not ok:raise ValueError(msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
A=HERE/'a2_action_probe.json';D=ROOT/'evidence/rank8_frontier_20261021/central_integrality/integer_gram_1154.json'
a=json.load(open(A));d=json.load(open(D))
need(a['verifier_sha256']==sha(HERE/'a2_action_probe.py'),'A2 verifier binding')
need(a['tensor_sha256']==d['tensor_sha256'],'tensor binding')
need(a['complete'],'complete A2 domain')
for p,h in a['source_sha256'].items():need(sha(ROOT/p)==h,'A2 source binding '+p)
out=[]
for ix in a['surviving_pattern_indices']:
    counts=d['completions'][ix];obstructions=[]
    for obj in range(1,8):
        support=[{'kind':'low','type':j,'induction_multiplicity':v[obj]}for j,v in enumerate(d['low_columns'])if v[obj]]
        for typ,(n,v)in enumerate(zip(counts,d['high_columns'])):
            if n and v[obj-1]:support.extend([{'kind':'high','type':typ,'copy':j,'induction_multiplicity':v[obj-1]}for j in range(n)])
        if len(support)==1:obstructions.append({'source_simple':obj,'single_central_simple':support[0],'required_twist_trace':0,'actual_twist_trace':'nonzero integer multiplicity times nonzero twist times positive FP dimension'})
    out.append({'index':ix,'status':'excluded_single_induction_support'if obstructions else 'passes_single_induction_support','obstructions':obstructions})
survivors=[r['index']for r in out if r['status']=='passes_single_induction_support'];hist=[r for r in a['results']if r['status']=='passes_fixed_action'and r['index']in survivors]
result={'schema':'r1154-single-induction-trace/v1','id':a['id'],'tensor_sha256':a['tensor_sha256'],'scope':'Necessary induction twist trace obstruction in the pseudo-unitary center; no remaining pattern is asserted categorifiable','incoming_patterns':len(out),'remaining_patterns':len(survivors),'surviving_pattern_indices':survivors,'remaining_pair_histograms':len(hist),'results':out,'source_sha256':{p.relative_to(ROOT).as_posix():sha(p)for p in [A,D]},'verifier_sha256':sha(Path(__file__))}
print(json.dumps(result,indent=2))
