"""An exact outer list of cyclic quartic field presentations.

For quadratic subfield Q(sqrt(D)), fix D=B^2+C^2. Every real cyclic
quartic extension with this subfield is F(sqrt(m(D+B sqrt(D)))) for a
positive squarefree rational twist m. Hilbert90 proves this because the
quotient of two defining radicands has rational-square norm. Odd primes
outside D occur in m precisely when they occur in the field conductor.
We retain both dyadic twists, without assuming either has the assigned
conductor. This only enlarges the necessary search.
"""
from pathlib import Path
from math import isqrt, prod
from itertools import product
import json
from higher_degree_quartic_bounds import factor

BASE=Path(__file__).parent


def presentations():
    data=json.loads((BASE/'higher_degree_quartic_bounds_certificate.json').read_text())
    rows=[]
    for f in data['fields']['cyclic']:
        a,J,cap=f['quadratic_conductor'],f['conductor'],f['trace_cap']
        if cap is None:continue
        D=a if a%4 else a//4
        choices=[(B,isqrt(D-B*B)) for B in range(1,isqrt(D)+1)
                 if D-B*B>0 and isqrt(D-B*B)**2==D-B*B]
        assert choices
        B,C=max(choices) # Keep C small; any representation suffices.
        inside=list(factor(D))
        external=prod(p for p in factor(J) if p!=2 and D%p)
        twists=set()
        for bits in product((0,1),repeat=len(inside)):
            for dyadic in (1,2):
                m=external*dyadic*prod(p for p,e in zip(inside,bits) if e)
                m=prod(p for p,e in factor(m).items() if e%2)
                other=prod(p for p,e in factor(m*D).items() if e%2)
                twists.add(min(m,other))
        for m in sorted(twists):
            numerator=256*m*m*D**3;denominator=a*J*J
            if numerator%denominator:continue
            I=isqrt(numerator//denominator)
            if I*I*denominator!=numerator:continue
            rows.append([a,J,D,B,C,m,I,cap])
    return rows


if __name__=='__main__':
    rows=presentations()
    (BASE/'higher_degree_quartic_cyclic_fields.txt').write_text(''.join(' '.join(map(str,r))+'\n' for r in rows))
    print('Cyclic outer presentations',len(rows))
