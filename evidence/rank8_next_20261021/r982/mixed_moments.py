"""Exhaustive mixed vacuum moments of distinguished simples through degree8.

For a modular center, [1](X_1...X_k)=sum_Z d_Z^2/Dim(ZC)
 times the product of the fusion eigenvalues. Every value is a
nonnegative integer. All multisets of seven distinguished nonunit
labels in degrees0..8 are checked on the selected joint witness.
"""
from pathlib import Path
import hashlib,itertools,json,time,sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE));import joint_galois_check as L
K=L.T.K;T=L.T;Elist=[E for E in range(8)if E!=L.meta['FP_character']];cols=[tuple(v)for v in L.P['low_columns']];counts=[1]*8
for label,n in zip(L.labels,L.original):
 if label[0]=='high_orbit'and n:cols.extend(label[2]);counts.extend([n]*len(label[2]))
lam=[];weight=[]
for v,n in zip(cols,counts):
 d=sum((K(x)*a for x,a in zip(v,T.ds)),K.zero);weight.append(K(n)*d*d/(T.D*T.D));lam.append([T.beta[E]*sum((K(x)*a for x,a in zip(v,T.characters[E])),K.zero)/d for E in Elist])
previous={():[K.one]*len(cols)};records=[];start=time.monotonic();failures=[]
for degree in range(9):
 current={};values=[]
 for monomial in itertools.combinations_with_replacement(range(7),degree):
  if degree:entries=[a*row[monomial[-1]]for a,row in zip(previous[monomial[:-1]],lam)]
  else:entries=previous[()]
  z=sum((w*a for w,a in zip(weight,entries)),K.zero);co=z.to_list()
  valid=len(co)<=1 and (not co or co[0].denominator==1 and co[0]>=0)
  if not valid:failures.append({'degree':degree,'monomial':[Elist[j]for j in monomial],'field_coefficients':list(map(str,co))})
  values.append(list(map(str,co)));current[monomial]=entries
 records.append({'degree':degree,'monomials':len(current),'values_sha256':hashlib.sha256(repr(values).encode()).hexdigest(),'failures_to_here':len(failures),'largest_rational_value':str(max((int(v[0])if v else 0)for v in values))if not failures else None})
 previous=current;print('degree',degree,'monomials',len(current),'failures',len(failures),'seconds',time.monotonic()-start,flush=True)
 if failures:break
out={'tensor_sha256':L.source['tensor_sha256'],'integer_joint_witness_sha256':hashlib.sha256((HERE/'joint_integer_result.json').read_bytes()).hexdigest(),'scope':'selected_pattern_all_mixed_vacuum_moments_through_degree8_only','records':records,'failures':failures,'outcome':'exact_mixed_moment_survivor_through_degree8'if not failures else'selected_joint_pattern_fails_mixed_moments'}
(HERE/'mixed_moments.json').write_text(json.dumps(out,indent=2)+'\n');print(out['outcome'],flush=True)
