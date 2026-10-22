"""Solver-free exact checker: Python 3 standard library only.
Run: python verify.py [certificate.json]
The conclusion is infeasibility of the supplied integer linear system.
The mathematical derivation of that system is audited separately.
"""

if not __debug__:
    raise RuntimeError('Proof verification requires assertions enabled; run without -O.')
from pathlib import Path
from fractions import Fraction as Q
import json,sys
p=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('certificate.json')
d=json.loads(p.read_text());A=d['matrix_rows'];b=d['rhs'];bounds=d['initial_integer_bounds']
assert len(A)==len(b)

def combination(covector):
    c=[Q(0) for _ in bounds];v=Q(0)
    for i,z in covector:
        z=Q(z);v+=z*b[i]
        for j,a in A[i]:c[j]+=z*a
    return c,v

for t,cut in enumerate(d['cuts']):
    j=cut['variable'];s=cut['sign'];assert s in (1,-1)
    c,v=combination(cut['covector'])
    residual=[-x for x in c];residual[j]+=s
    lower=v+sum(z*bounds[k][0 if z>=0 else 1] for k,z in enumerate(residual))
    if s==1:
        new=-((-lower.numerator)//lower.denominator)
        assert new>=bounds[j][0]
        bounds[j][0]=new
    else:
        new=(-lower.numerator)//lower.denominator
        assert new<=bounds[j][1]
        bounds[j][1]=new
    assert new==cut['new_bound'],('cut',t)
    assert bounds[j][0]<=bounds[j][1]

c,v=combination(d['separator'])
maximum=sum(z*bounds[k][1 if z>=0 else 0] for k,z in enumerate(c))
gap=v-maximum
assert gap==Q(d['expected_gap']) and gap>0
print('PASS: no integer solution.')
print(f'{len(A)} equations, {len(bounds)} integer variables, {len(d["cuts"])} exact rounding cuts.')
print('Exact positive separating gap:',gap)
