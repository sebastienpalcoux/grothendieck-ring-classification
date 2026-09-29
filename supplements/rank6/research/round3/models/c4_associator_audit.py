#!/usr/bin/env python3
"""Independent exact arithmetic checks for the C4 associator argument.

This checks the finite algebraic statements, not a formalization of the
module-category and indicator theorems explained in the companion note.
"""
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

def require(value, message):
    if not value:
        raise ValueError(message)

def exponent(k, a, b, c):
    """omega_k(a,b,c)=i**exponent, for representatives 0,...,3."""
    return (k * a * ((b + c) // 4)) % 4

def run():
    rows = json.loads((ROOT / 'data/census.json').read_text())
    R = next(r['N'] for r in rows if r['id'] == 'R6_4_6')
    # Reconstruct labels from the tensor, with no dimension approximation.
    g, h, g3, rho, sigma = 1, 5, 2, 3, 4
    e = lambda i: [int(j == i) for j in range(6)]
    require(R[g][g] == e(h) and R[h][g] == e(g3), 'not cyclic order four')
    require(R[g3][g] == e(0), 'wrong generator inverse')
    require(R[g][rho] == e(sigma) and R[h][rho] == e(rho), 'wrong orbit')
    require(R[rho][rho] == [1, 0, 0, 4, 4, 1], 'wrong square')
    require(R[rho][sigma] == [0, 1, 1, 4, 4, 0], 'wrong mixed product')
    # d=(4,3) in Q(sqrt(2)): d^2=2+8d.
    require((4*4+2*3*3, 2*4*3) == (2+8*4, 8*3), 'dimension identity')
    module_branches = []
    for chi in (-1, 1):
        possible = []
        for a in range(9):
            lam = 2*a-8
            if lam*lam == 2+4*(1+chi)*lam:
                possible.append(a)
        require(not possible, 'unexpected regular-algebra module branch')
        module_branches.append({'chi_t': chi, 'a_range': [0, 8],
                                'solutions': possible})
    cocycles = []
    for k in range(4):
        for a,b,c,d in itertools.product(range(4), repeat=4):
            left = exponent(k,b,c,d) + exponent(k,a,(b+c)%4,d) + exponent(k,a,b,c)
            right = exponent(k,(a+b)%4,c,d) + exponent(k,a,b,(c+d)%4)
            require((left-right)%4 == 0, '3-cocycle identity')
        indicators = {str(x): sum(exponent(k,x,(j*x)%4,x)
                                  for j in range(4)) % 4 for x in (1,3)}
        require(exponent(k,2,2,2) == (2*k)%4, 'restriction to C2')
        require(indicators == {'1': k, '3': k}, 'fourth indicator')
        cocycles.append({'class_k': k, 'restriction_C2_class': k%2,
                         'fourth_indicator_exponent_mod4': indicators})
    return {'passed': True, 'scope': 'independent finite arithmetic audit',
            'categorical_proof': 'c4_associator_audit.md',
            'ring_id': 'R6_4_6', 'module_branches': module_branches,
            'cocycle_representatives_checked': cocycles,
            'forced_class': 2, 'forced_fourth_indicator': -1}

if __name__ == '__main__':
    result = run()
    Path(__file__).with_suffix('.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'passed': result['passed'], 'forced_class': 2,
                      'forced_fourth_indicator': -1}))
