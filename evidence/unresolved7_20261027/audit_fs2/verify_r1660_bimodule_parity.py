"""Independent source-bound exact check; excludes two module realizations only."""
from pathlib import Path
import hashlib,json,runpy
import sympy as s
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[2]
def ck(t,msg):
 if not t:raise ValueError(msg)
source=ROOT/'data/current_remaining_cases.py'; N0=runpy.run_path(str(source))['TENSORS']['R6_8_1660']; digest=hashlib.sha256(json.dumps(N0,separators=(',',':')).encode()).hexdigest()
ck(digest=='697ec27fe203356199bfcf674587be9c71455dbb681f2e086a076f726b03d267','source hash')
receipt_path=ROOT/'supplements/rank6/research/frontier/new_research/r1660_categorical/dual_actions_receipt.json'; archive=json.loads(receipt_path.read_text())
i3=s.eye(3);g=s.Matrix([[0,1,0],[1,0,0],[0,0,1]]);sg=s.Matrix([[0,0,1],[0,0,1],[1,1,0]])
I=s.eye(6);G=s.kronecker_product(s.eye(2),g);S=s.kronecker_product(s.eye(2),sg)
params=[('III_mixed',1,2,0,1,s.diag(1,-1)),('IV_mixed',1,2,1,2,s.diag(1,-1)),('III_same',1,2,0,1,s.eye(2))]
rows=[]
for tag,a,b,c,f,V in params:
 U=s.Matrix([[a,b],[b,6-a]]);R=s.Matrix([[c,f],[f,4-c]]);P=(U+V)/2;Q=(U-V)/2
 X=s.kronecker_product(P,i3)+s.kronecker_product(Q,g)+s.kronecker_product(R,sg);N=[I,G,X,G*X,S,S*X]
 for i in range(6):
  for j in range(6):ck(N[i]*N[j]==sum((N0[i][j][k]*N[k]for k in range(6)),s.zeros(6)),'module source product')
 item=next(z for z in archive if z['type']==tag)
 for solution_index,sol in enumerate(item['solutions']):
  B=[s.Matrix(q)for q in sol['action_matrices']];t=sol['fusion_tensor'];du=sol['dual'];ck(B[0]==I,'dual unit')
  for i in range(len(B)):
   ck(B[i].T==B[du[i]],'dual matrix transpose')
   for j in range(len(B)):
    ck(B[i]*B[j]==sum((t[i][j][k]*B[k]for k in range(len(B))),s.zeros(6)),'dual matrix product')
  restrictions=[[int((ni*bi)[0,0])for ni in N]for bi in B]
  bad=[{'dual_simple':j,'restriction':r}for j,r in enumerate(restrictions)if du[j]==j and r[4]%2 and any(r[i]%2 for i in [0,1,2,3,5])]
  rows.append({'tag':tag+str(solution_index),'duality':du,'restrictions':restrictions,'mixed_odd_sign_selfdual_rows':bad})
bytag={row['tag']:row for row in rows}
ck(bytag['III_mixed0']['mixed_odd_sign_selfdual_rows'][0]=={'dual_simple':4,'restriction':[0,0,0,0,1,1]},'III contradiction')
ck(bytag['IV_mixed1']['mixed_odd_sign_selfdual_rows'][0]=={'dual_simple':2,'restriction':[0,0,1,1,1,1]},'IV contradiction')
ck(not bytag['IV_mixed0']['mixed_odd_sign_selfdual_rows'],'retained IV control')
ck(not bytag['III_same0']['mixed_odd_sign_selfdual_rows'],'retained rank8 control')
ind_path=ROOT/'evidence/unresolved10_20261027/r6_1660/all_indicators_source.json';ind=json.loads(ind_path.read_text())
for case in ind['cases']:
 if case['cyclic_dimension_three_compatible']:
  mom=case['moments_ascending_zeta48_coefficients']['2']
  for label in ['X','T']:
   coeff=list(map(int,mom[label]));ck(coeff[0]==1 and all(v==0 for v in coeff[1:]),'positive source indicator '+label)
ck(s.simplify(s.sqrt(2)*s.cos(6*s.pi/8))==-1,'negative Ising sigma indicator')
result={'status':'PASS','source_tensor_sha256':digest,'archive_sha256':hashlib.sha256(receipt_path.read_bytes()).hexdigest(),'indicator_source_sha256':hashlib.sha256(ind_path.read_bytes()).hexdigest(),'source_FS2':[1,1,1,1,-1,1],'rows':rows,'excluded_module_realizations':['III_mixed0','IV_mixed1'],'whole_ring_excluded':False,'categorical_dependency':'Positive pivotal Frobenius forgetful functor U from A-bimodules; preserves duality transpose signs.'}
(HERE/'r1660_bimodule_parity_receipt.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS: two module realizations rejected; retained controls pass; no whole-ring exclusion')
