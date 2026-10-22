
if not __debug__:
    raise RuntimeError('Proof verification requires assertions enabled; run without -O.')
from pathlib import Path
import json,sys,time,hashlib
PACKAGE=Path(__file__).resolve().parents[1];ROOT=PACKAGE.parents[1];B=PACKAGE;ST=ROOT/'evidence/rank8_frontier_20261021';sys.path.insert(0,str(ST/'quadratic'))
from joint_atomic_integer import AtomicSpectrum,table_for,filter_support,joint_filter,st
start=time.time();R=json.load(open(ROOT/'site/dist/downloads/fusion-tensors/R8_3_3472.txt'));print('start complete source domain',flush=True);C=AtomicSpectrum(R,4);print('atomic',len(C.low),len(C.orbits),'seconds',time.time()-start,flush=True);T=table_for(R,C.a)
A,individual=filter_support(C,T);print('individual closure',len(A.low),len(A.orbits),'seconds',time.time()-start,flush=True)
D,joint=joint_filter(A,T);print('joint closure',len(D.low),len(D.orbits),'seconds',time.time()-start,flush=True)
highs=sorted((0,)+tuple(D.a['high'][j][0])for orbit in D.orbits for j in orbit)
assert all(len(orbit)==1 for orbit in D.orbits)
expected=sorted(tuple(x[1])for x in json.load(open(PACKAGE/'domain/final_highs_discovery.json')))
assert highs==expected,(len(highs),len(expected))
from collections import Counter
dims=Counter(tuple(map(str,D.a['high'][j][1]))for orbit in D.orbits for j in orbit)
report={'tensor_sha256':st.digest(R),'complete_atomic_low_columns':len(C.low),'complete_atomic_high_vectors':len(C.orbits),'individual_surviving_low':len(A.low),'individual_surviving_high':len(A.orbits),'joint_surviving_low':len(D.low),'joint_surviving_high':len(D.orbits),'dimension_counts':[(list(k),v)for k,v in dims.items()],'all_high_orbits_singletons':True,'exact_agreement_with_final_highs_discovery':True,'individual_report':individual,'joint_report':joint}
assert st.encode(report)==json.loads((PACKAGE/'domain/high_domain_receipt.json').read_text())
print('PASS complete high domain172',dict(dims),'seconds',time.time()-start,flush=True)
