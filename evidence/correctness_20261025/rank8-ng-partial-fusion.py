import pathlib,importlib.util,json,itertools,os
from pathlib import Path
R=Path(os.environ.get('FUSION_CLASSIFICATION_REPO',Path(__file__).resolve().parents[2])).resolve()
P=R/'evidence/unified_20261016/rank8/verify_neargroup_centralizer.py';A=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('candidate_exact_field',P);f=importlib.util.module_from_spec(spec);spec.loader.exec_module(f)
def require(condition,message):
 if not condition:raise ValueError(message)
records=[]
for which in (820,869):
 M=f.matrix(which)
 # Discard the candidate D-D block: none of it is used below.
 for i in range(4,8):
  for j in range(4,8):M[i][j]=None
 dims=M[0];D=f.D;b=f.b;c=f.c
 inverses=[f.ONE,f.inv_b,f.inv_c,f.inv_c]
 nb=[[0]*8 for _ in range(8)];nc=[[[0]*8 for _ in range(8)] for _ in range(2)]
 def integer(z):
  require(all(v==0 for v in z[1:]) and z[0].denominator==1 and z[0]>=0,'nonnegative exact integer coefficient')
  return int(z[0])
 for j,k in itertools.product(range(8),repeat=2):
  # N_B = -I + ((b+1)d*d^T +(1+1/b) S_B*S_B^T +2 S_C*S_C^T)/D
  term=f.total([f.mul(f.add(b,f.ONE),f.mul(dims[j],dims[k])),f.mul(f.add(f.ONE,f.inv_b),f.mul(M[j][1],M[k][1]))]+[f.scale(f.mul(M[j][l],M[k][l]),2) for l in (2,3)])
  nb[j][k]=integer(f.sub(f.mul(f.invD,term),f.ONE if j==k else f.ZERO))
  for ii,i in enumerate((2,3)):
   term=f.total(f.mul(f.mul(f.mul(M[i][l],M[j][l]),M[k][l]),inverses[l]) for l in range(4))
   nc[ii][j][k]=integer(f.mul(f.invD,term))
 model=f.model(which)
 require([nb,*nc]==model[1:4],'partial matrix correspondence')
 tc=f.scale(f.add(f.scalar(-1),f.Q if which==820 else f.neg(f.Q)),f.F(1,2))
 td=f.scalar(-2 if which==820 else 1)
 gauss=f.total([f.ONE,f.mul(b,b),f.mul(f.mul(c,c),tc),f.mul(f.mul(f.a,f.a),td)])
 require(gauss==f.scale(f.a,3 if which==820 else -3),'squared-dimension Gauss normalization')
 records.append({'pairing_parameter':1 if which==820 else 2,'known_fusion_matrices':[nb,*nc],'result':'PASS','unknown_D_D_S_block_used':False})
require(records[0]['known_fusion_matrices']==records[1]['known_fusion_matrices'],'both seeds have same partial matrices')
result={'scope':'Exact partial fusion derived solely from actual non-D-D tube blocks and unitarity; no candidate D-D block used','records':records}
(A/'rank8-ng-partial-fusion.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS both actual partial-block types; common matrices B,C1,C2')
