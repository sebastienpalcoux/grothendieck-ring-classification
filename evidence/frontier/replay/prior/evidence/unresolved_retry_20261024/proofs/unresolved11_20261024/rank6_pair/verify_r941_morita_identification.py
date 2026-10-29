#!/usr/bin/env python3
"""Verify one necessary Morita alternative; this does not construct a module."""
import hashlib,json,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[2]
BASE=ROOT/'online_revision/grothendieck-ring-classification'
p=BASE/'supplements/rank6/research/frontier/new_research/r1660_categorical/dual_actions_receipt.json'
q=ROOT/'unresolved11_20261024/inputs/R8_3_941.json'
records=json.loads(p.read_text());target=json.loads(q.read_text())
row=next(x for x in records if x['type']=='III_same')
source=row['solutions'][0]
M=source['fusion_tensor'];N=target['fusion_tensor'];perm=[0,3,6,7,4,5,2,1]
assert sorted(perm)==list(range(8))
for i in range(8):
 for j in range(8):
  for k in range(8):
   assert M[i][j][k]==N[perm[i]][perm[j]][perm[k]],(i,j,k)
ans={'status':'PASS','source_file_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
 'target_file_sha256':hashlib.sha256(q.read_bytes()).hexdigest(),
 'source_type':'III_same','source_solution_index':0,'target_id':target['id'],
 'basis_permutation':perm,'coefficients_checked':512,
 'scope':'Identifies a necessary Morita-dual based ring. No existence of the nonpointed algebra or corresponding module category is established.'}
output=pathlib.Path(__file__).with_name('r941_morita_identification_certificate.json')
output.write_text(json.dumps(ans,indent=2)+'\n');print(json.dumps(ans,indent=2))
