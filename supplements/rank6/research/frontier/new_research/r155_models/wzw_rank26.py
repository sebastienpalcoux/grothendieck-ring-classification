def _audit_require(ok, message):
    if not ok: raise AssertionError(message)

"""Exact integrable-weight counts for full untwisted WZW categories of rank 26.
This excludes no subquotient, coset, orbifold, or extension of such categories.
"""
from pathlib import Path
import json

def counts(marks, cap=60):
 c=[1]+[0]*cap
 for a in marks:
  for k in range(a,cap+1): c[k]+=c[k-a]
 return [sum(c[:k+1])for k in range(cap+1)]

families={}
for r in range(1,27): families['A'+str(r)]=[1]*r
for r in range(2,27):
 families['B'+str(r)]=[1]+[2]*(r-2)+[1]
 families['C'+str(r)]=[1]*r
for r in range(4,27):families['D'+str(r)]=[1]+[2]*(r-3)+[1,1]
families.update(E6=[1,2,3,2,1,2],E7=[2,2,3,4,3,2,1],E8=[2,3,4,6,5,4,3,2],F4=[2,3,2,1],G2=[1,2])
found=[]
for name,marks in families.items():
 c=counts(marks)
 _audit_require(c[-1]>26, 'Exact audit check failed')
 for level,n in enumerate(c[1:],1):
  if n==26:found.append([name,level])
_audit_require(found==[['A1',25],['A25',1],['B22',2],['C25',1],['D19',2]], found)
out={'rank':26,'full_untwisted_WZW_matches':found,'marks':families,'scope':'integrable highest-weight counts; not a classification of quantum-group-derived categories','rank_bound_explanation':'Beyond Lie rank 26, A,C level1 ranks exceed26; B,D level1 ranks3,4, and level2 ranksr+4,r+7 exceed26. Counts are nondecreasing in level.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(found)
