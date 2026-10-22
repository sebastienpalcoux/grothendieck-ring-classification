
if not __debug__:
    raise RuntimeError('Proof verification requires assertions enabled; run without -O.')
from pathlib import Path
import json,sys
import sympy as s
PACKAGE=Path(__file__).resolve().parents[1];ROOT=PACKAGE.parents[1];OUT=PACKAGE/'frames';sys.path.insert(0,str(ROOT/'evidence/rank8_frontier_20261021/quadratic'))
from sextic_character_table import SexticTable,simple_data
R=json.load(open(ROOT/'site/dist/downloads/fusion-tensors/R8_3_3472.txt'));T=SexticTable(R,simple_data(3472));K=T.K
f=json.load(open(PACKAGE/'domain/low_beta_assignments.json'));ids=f['psd_solutions'][42];low=[[1]+[0]*7]+[f['vectors'][i]for i in ids]+[[1]+[2]*7]
p=json.load(open(OUT/'frame42_gram.json'));vs=[v['restriction']for v in p['beta_columns']]+[[0]+[1]*7];pairs=[(i,j)for i in range(1,8)for j in range(i,8)];A=s.Matrix([[v[i]*v[j]for v in vs]for i,j in pairs]);rank=A.rank();pr=A.T.rref()[1];assert rank==10
B=A[list(pr),:].inv();rhs=[sum((K(low[E][i])*T.characters[E][j]-K(low[E][i]*low[E][j])for E in range(8)),K.zero)for i,j in pairs]
c=[sum((K(B[i,j])*rhs[pr[j]]for j in range(10)),K.zero)for i in range(10)]
assert all(sum((K(A[i,j])*c[j]for j in range(10)),K.zero)==rhs[i]for i in range(28))
rad=(T.ds[1]-K(6))/K(5);th=K([1,0])-rad;names={tuple(T.coordinates(K(2))):'2',tuple(T.coordinates(th)):'2cos(2pi/7)',tuple(T.coordinates(th*th-K(2))):'2cos(4pi/7)',tuple(T.coordinates(th**3-K(3)*th)):'2cos(6pi/7)',tuple(T.coordinates(-K(2)-K(10)*rad)):'-2-10sqrt2'}
for v,z in zip(vs,c):print(v,names.get(tuple(T.coordinates(z)),str(T.coordinates(z))))
actual={'vectors':vs,'coefficient_coordinates':[list(map(str,T.coordinates(z)))for z in c],'coefficient_names':[names.get(tuple(T.coordinates(z)),'unknown')for z in c]}
assert actual==json.loads((OUT/'frame42_sts_coeffs.json').read_text())
print('PASS exact frame42 twist coefficients')
