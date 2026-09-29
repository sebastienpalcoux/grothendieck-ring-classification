"""Rule out three dimension-matched modular Morita model families exactly.

These model-scope obstructions do not prove noncategorifiability.
"""
import json
import sys
from pathlib import Path
import sympy as s
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'software'))
from exact import field,require,ec,evaluate
from rings import Characters
from model_dimension_scan import polynomial
t=s.Symbol('t')
records=json.loads((ROOT/'verification/round4/campaign_manifest.json').read_text())['tensors']

def qinteger(q,n,K):
    return sum((q**(n-1-2*j)for j in range(n)),K.zero)

def check(rid,K,D,center_dims,codegree,description):
    R=next(r['N']for r in records if r['id']==rid)
    ch=Characters(R)
    require(ch.C.charpoly().as_poly().eval(codegree)==0,'missing formal codegree')
    p=ch.fp()[4]
    require(not evaluate(p.all_coeffs(),D,K),'model global dimension is not a target conjugate')
    target=D/K(codegree)
    differences=[z-target for z in center_dims]
    require(all(differences),'required low central dimension actually occurs')
    return dict(id=rid,model=description,codegree=codegree,
                candidate_global_dimension_polynomial=polynomial(K,D),
                required_central_dimension=ec(target),
                field_polynomial=list(map(str,K.mod.to_list())),
                center_rank=len(center_dims),
                differences=[ec(v)for v in differences],
                exact_dimension_obstruction=True,
                scope='excludes this entire Morita class only')

out=[]
# Ad(D16), the modularization of the even part of SU(2)_28.
K=field(s.Poly(s.cyclotomic_poly(60,t),t));q=K.unit
d=[qinteger(q,2*j+1,K)for j in range(7)]
d += [qinteger(q,15,K)/K(2)]*2
D=sum((z*z for z in d),K.zero)
out.append(check('R6_4_629',K,D,[a*b for a in d for b in d],5,
                 'Ad(D16) and all categories Morita equivalent to it'))
# The rank-nine modular category C(sl3,9)^0_Rep(C3).
K=field(s.Poly(t*t-3,t));r=K.unit
d=[K.one,K(7)+4*r,K(8)+4*r]+[K(3)+2*r]*6
D=sum((z*z for z in d),K.zero)
out.append(check('R6_5_1204',K,D,[a*b for a in d for b in d],8,
                 'C(sl3,9)^0_Rep(C3) and all categories Morita equivalent to it'))
# Center of PSU(2)_14: diagonal-fermion quotient of the same-parity pairs.
K=field(s.Poly(s.cyclotomic_poly(32,t),t));q=K.unit
d=[qinteger(q,j+1,K)for j in range(15)]
D=sum((d[j]*d[j]for j in range(0,15,2)),K.zero)
pairs={(i,j)for i in range(15)for j in range(15)if (i-j)%2==0}
center_dims=[]
while pairs:
    i,j=min(pairs);mate=(14-i,14-j);pairs.remove((i,j))
    if mate==(i,j):center_dims.extend([d[i]*d[j]/K(2)]*2)
    else:pairs.remove(mate);center_dims.append(d[i]*d[j])
require(len(center_dims)==58,'wrong PSU(2)_14 center rank')
out.append(check('R6_4_91',K,D,center_dims,4,
                 'PSU(2)_14 and all categories Morita equivalent to it'))
result=dict(scope='specific known Morita models, never a general exclusion',cases=out,passed=True)
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print([(r['id'],r['center_rank'],r['exact_dimension_obstruction'])for r in out])
