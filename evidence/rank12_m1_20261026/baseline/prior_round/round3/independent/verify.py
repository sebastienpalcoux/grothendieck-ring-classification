"""Independent exact replay of the mandatory first Morita premises."""
from pathlib import Path
import json,hashlib,itertools
ROOT=Path(__file__).resolve().parent;BASE=ROOT.parents[1]
def require(c,m):
 if not c:raise ValueError(m)
def sha(R):return hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()
rows=json.loads((ROOT/'frozen/d120_unresolved_tensors.json').read_text())
records=[]
for row in rows:
 if row['exact_dimension_character']['family']!='D120':continue
 R=row['tensor'];n=len(R);ds=[int(v[0])for v in row['exact_dimension_character']['dimensions_in_field']]
 require(sha(R)==row['tensor_sha256'],'input hash')
 require(sorted(ds)==[1]*4+[2]*4+[5]*4,'dimension pattern')
 for i,j in itertools.product(range(n),repeat=2):require(sum(R[i][j][k]*ds[k]for k in range(n))==ds[i]*ds[j],'positive exact dimension character')
 G=[i for i,d in enumerate(ds)if d==1];X=[i for i,d in enumerate(ds)if d==2];Y=[i for i,d in enumerate(ds)if d==5];E=G+X
 require(sum(ds[i]**2 for i in E)==20,'neutral dimension')
 require(all(not R[i][j][k]for i,j in itertools.product(E,repeat=2)for k in Y),'subring closure')
 ls=[{g for g in G if R[g][i][i]}for i in X];rs=[{g for g in G if R[i][g][i]}for i in X]
 require(all(H==ls[0]for H in ls+rs)and len(ls[0])==2,'full common cyclic stabilizer')
 H=sorted(ls[0]);h=next(i for i in H if i!=0);require(R[h][h][0]==1,'order two')
 L=[next(k for k,c in enumerate(R[h][i])if c)for i in Y];P=[next(k for k,c in enumerate(R[i][h])if c)for i in Y]
 require(L==P and all(i!=j for i,j in zip(Y,L)),'equal free action')
 orbits=[];unused=set(Y)
 while unused:
  a=min(unused);O=set();fix=0
  for g,k in itertools.product(H,repeat=2):
   b=next(j for j,c in enumerate(R[g][a])if c);c=next(j for j,c in enumerate(R[b][k])if c);O.add(c);fix+=int(c==a)
  require(len(O)==2 and fix==2,'double orbit and cyclic stabilizer')
  orbits.append(sorted(O));unused-=O
 require(len(orbits)==2,'four new dual simple objects')
 records.append(dict(id=row['id'],tensor_sha256=sha(R),subring=sorted(E),regular_algebra=H,noninvertible_double_orbits=orbits,dual_type={'invertibles':20,'dimension5':4},consequence='Every complex categorification is group-theoretical and unitarizable'))
require(len(records)==15,'all fifteen inputs')
receipt=dict(status='PASS',count=len(records),records=records,scope='Necessary implication only; no existence claim')
(ROOT/'forced_gt_verification.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'status':'PASS','count':len(records),'new_exclusions':0,'new_models':0,'new_forced_group_theoretical':15}))
