import sys,json,itertools
from pathlib import Path
import sympy as s
G=Path('/workspace/scratch/90f37cc83103/online_revision/grothendieck-ring-classification')
sys.dont_write_bytecode=True
sys.path.insert(0,str(G/'evidence/rank8_creative_20261022/r1154'))
import verify_semionic_packet as p
l=p.l
b=p.build_at(6971,1);labels=b['labels'];n=len(labels)
M=s.Matrix([l.cols[q['low']]if 'low'in q else (0,)+tuple(l.domain['high_columns'][q['type']])for q in labels]).T
Ng=s.Matrix(8,8,lambda k,j:l.R[3][j][k]);J=M.T*Ng*M
r=json.loads((G/'evidence/rank8_creative_20261022/r1154/semionic_packet.json').read_text())['results'][0]
N=s.Matrix(r['packet_fusion_matrices'][0]);K=4*N-J
print('G action', [list(Ng[:,i]).index(1)for i in range(8)])
print('K support',[(i,j)for i in range(n)for j in range(n)if K[i,j]])
ds=s.Matrix([l.K.to_sympy(sum((l.K(int(M[j,i]))*l.a['ds'][j]for j in range(8)),l.K.zero))for i in range(n)])
tw=s.ones(n,1)
for i in r['packet_indices']:tw[i]=-1
v=ds.multiply_elementwise(tw);D=l.K.to_sympy(l.a['D'])
extra=s.simplify((v.T*K*v)[0]/D**2)
print('extra',extra)
for a in itertools.product((-1,1),repeat=4):
 nu=s.Matrix([1,0,0,-1,*a]);answer=s.simplify(((nu.T*Ng*nu)[0]+extra)/4)
 print(a,'packetnu2=',answer)
