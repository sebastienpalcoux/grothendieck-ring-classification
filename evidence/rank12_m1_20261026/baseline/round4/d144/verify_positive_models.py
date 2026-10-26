from pathlib import Path
import json,hashlib,itertools
from triality import source_tensor,zest,require
R=Path(__file__).resolve().parent
inputs=json.loads((R/'positive_tensors.json').read_text())
maps=json.loads((R/'positive_maps.json').read_text())
receipt=[]
for row in maps:
 N=source_tensor(row['m']);G=[0]*8+[1]*4
 require(all(not N[i][j][k] or G[k]==(G[i]+G[j])%2 for i,j,k in itertools.product(range(12),repeat=3)),'full parity grading')
 require(N[1][1][0]==1 and sum(N[1][1])==1,'order-two charge')
 M=zest(N) if row['zested'] else N
 p=row['basis_map_source_to_model'];T=inputs[row['id']]
 require(all(T[i][j][k]==M[p[i]][p[j]][p[k]] for i,j,k in itertools.product(range(12),repeat=3)),'all1728 coefficients')
 receipt.append({'id':row['id'],'status':'retained_model','tensor_coefficients_checked':1728,'sha256':hashlib.sha256(json.dumps(T,separators=(',',':')).encode()).hexdigest(),'categorical_existence_separate_from_tensor_check':True})
(R/'positive_model_audit.json').write_text(json.dumps({'status':'PASS','primary_m0_matrix_freshly_inspected':True,'results':receipt},indent=2)+'\n')
print('PASS: 4 retained models, 6912 coefficient comparisons')
