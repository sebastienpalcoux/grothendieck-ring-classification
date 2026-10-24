"""Exact arithmetic checks for TY_SPECTRUM.md; not a categorification proof."""
import itertools,json
from functools import reduce
from operator import xor
from pathlib import Path
import sympy as s

HERE=Path(__file__).resolve().parent
def require(x,msg):
    if not x:raise ValueError(msg)
indicators={}
for epsilon in [1,-1]:
    values=[]
    for k in range(1,5):
        total=sum((-1)**sum((a&b).bit_count() for i,a in enumerate(z) for b in z[i+1:])
                  for z in itertools.product(range(4),repeat=k) if reduce(xor,z,0)==0)
        v=s.Rational(epsilon**k*total,2**(k-1));values.extend([0,int(v)])
    require(values==[0,epsilon,0,0,0,epsilon,0,2],'TY indicator sum')
    indicators[str(epsilon)]=values
    zeta=(1+s.I)/s.sqrt(2)
    moment=[2]+values[:7]
    for j in range(8):
        weight=s.simplify(sum(moment[n]*zeta**(-j*n) for n in range(8))/8)
        expected=s.simplify((2+2*epsilon*s.cos(s.pi*j/2))/8)
        require(s.simplify(weight-expected)==0,'finite Fourier transform')
source=[]
for rid,Y in [('R9_2_137',8),('R9_2_1607',3),('R9_2_1976',5)]:
    R=json.loads((HERE.parent/'inputs'/f'{rid}.json').read_text())['fusion_tensor']
    du=[next(j for j in range(9) if R[i][j][0]) for i in range(9)]
    G=[i for i in range(9) if R[i][du[i]]==[1]+[0]*8]
    v=[sum(R[i][Y][j]*R[j][du[i]][k] for i in range(9) for j in range(9)) for k in range(9)]
    require(all(v[g]==0 for g in G),'invertible support')
    require(v[Y]==16 and all(v[k]==16 for k in range(9) if k not in G+[Y]),'TY induction column')
    source.append({'id':rid,'Y':Y,'forget_induce_Y':v})
d=4+3*s.sqrt(2);D=16+32*d
divisibility=[]
for b in range(9):
    z=s.radsimp(D**2/(2+b*d)**2).expand()
    a=z.coeff(s.sqrt(2),0);c=z.coeff(s.sqrt(2),1)
    integral=bool(a.is_Integer and c.is_Integer)
    require(integral==(b in [0,1,4,7,8]),'modular codegree integrality')
    divisibility.append({'b':b,'formal_codegree':str(z),'algebraic_integer':integral})
out={'status':'PASS','classification_changes':[], 'TY_indicators':indicators,
     'source_induction':source,'primitive_eighth_root_pairs_after_integral_center_theorem':[[1,7],[4,4]],
     'codegree_checks':divisibility}
(HERE/'ty_spectrum_receipt.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS: TY indicators, Fourier weights, source inductions, and exact packet dimensions')
