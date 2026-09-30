"""Exact coprime indicator values from large-prime congruences, in actual mu48."""
import json,hashlib
import actual48 as Q
from exact import require
from prime_indicator_congruence import large_prime_targets
from modular_character_induction import rational_rows
SOURCE=Q.P/'research/round5/unification/prime_indicator_congruences.json'

def append_rows(R,d,cols,labels,nv):
 require(d['F']==48,'actual48 field required');record=next(x for x in json.loads(SOURCE.read_text())['cases']if x['id']=='R6_8_1660');expected=large_prime_targets(R,48,record['samples_per_residue']);require(record==dict(id='R6_8_1660',**expected)and expected['passed'],'prime indicator source does not replay');C=d['C'];D=d['DD'];dims=d['dims'];dv={tuple(v):sum((C(v[i])*dims[i+1]for i in range(len(v))),C.zero)for v,a in labels};lowmass=[sum((C(sum(v[i]*v[j]for v in cols))*dims[j]for j in range(len(R))),C.zero)for i in range(len(R))];rows=[];rhs=[]
 for target in record['targets']:
  n=target['residue']
  for obj in range(1,len(R)):
   coeff=[C(v[obj-1])*dv[tuple(v)]*C.unit**(a*n)for v,a in labels]+[C.zero]*(nv-len(labels));value=D*C(target['values'][obj])-lowmass[obj]
   for row,val in rational_rows(coeff,value,C):
    if any(row)or val:rows.append({j:int(a)for j,a in enumerate(row)if a});rhs.append(int(val))
 return rows,rhs,dict(source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),exponent=48,residues=[x['residue']for x in record['targets']],target_vectors=[x['values']for x in record['targets']],rational_equations=len(rows))
