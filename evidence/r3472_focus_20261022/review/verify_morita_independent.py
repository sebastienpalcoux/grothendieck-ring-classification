#!/usr/bin/env python3
"""Independent arithmetic checks supporting the separate mathematical review.

No code is imported from the Morita proof's verifier. This does not mechanically
verify the categorical arguments, which are reviewed in ALL_MORITA_AUDIT.md.
"""
from pathlib import Path
import argparse
import ast
import hashlib
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def need(ok, why):
    if not ok:
        raise ValueError(why)


def polynomial_multiply(a, b):
    out = [0]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i+j] += x*y
    return out


def receipt():
    path = ROOT/'site/dist/downloads/fusion-tensors/R8_3_3472.txt'
    tensor = ast.literal_eval(path.read_text())
    need([tensor[i][i][i] for i in range(1, 8)] == [2]*7,
         'Diagonal occurrence certificate changed')
    dual = [next(j for j in range(8) if tensor[i][j][0]) for i in range(8)]
    need([i for i in range(8) if sum(tensor[i][dual[i]]) == 1] == [0],
         'Source invertible inventory changed')

    # Work before division by five: each permissible type has multiplicity
    # step 1 when its square/5 is integral, and step 5 otherwise. This checks
    # fixed and free orbits together, separately from the proof's 7-type list.
    types = []
    for a in range(19):
        for b in range(1, 14):
            step = 1 if (a*a+2*b*b)%5 == 0 and 2*a*b%5 == 0 else 5
            if step*a*a <= 345 and step*b*b <= 175 and step*(7*b-5*a)**2 <= 50:
                types.append((a, b, step))
    need(types == [(1,1,5),(2,1,5),(3,2,5),(4,3,5),
                   (5,4,5),(6,4,5),(7,5,5),(15,10,1)],
         'Independent all-type C5 domain changed')
    found = []

    def visit(i, A, B, C, chosen):
        if min(A, B, C) < 0 or C*C > A*B:
            return
        if i == len(types):
            if A == B == C == 0:
                found.append(chosen)
            return
        a, b, step = types[i]
        for n in range(min(A//(step*a*a), B//(step*b*b), C//(step*a*b))+1):
            visit(i+1, A-n*step*a*a, B-n*step*b*b, C-n*step*a*b,
                  chosen + ([[a,b,n*step]] if n else []))

    visit(0,345,175,245,[])
    found.sort()
    need(found == sorted([
        [[2,1,5],[4,3,5],[7,5,5]],
        [[1,1,5],[4,3,10],[6,4,5]],
        [[1,1,5],[3,2,20],[4,3,10]],
        [[1,1,10],[3,2,10],[7,5,5]],
    ]), 'Independent C5 profile count differs')

    # Independently expand elimination: A=-y^2+5y-5, B=y-1 and
    # A^2+A*B-B^2=0 from t=A/B, t^2+t-1=0, y=1+x^2=f/5.
    A, B = [-5,5,-1], [-1,1]
    aa, ab, bb = polynomial_multiply(A,A), polynomial_multiply(A,B), polynomial_multiply(B,B)
    coefficients = [aa[i] + (ab[i] if i < len(ab) else 0)
                    - (bb[i] if i < len(bb) else 0) for i in range(5)]
    need(coefficients == [29,-58,40,-11,1], 'Quartic elimination changed')
    scaled = [x*5**(4-i) for i,x in enumerate(coefficients)]
    need(scaled == [18125,-7250,1000,-55,1], 'Formal-codegree polynomial changed')
    need(55**4 % 18125 == 15625, 'Formal-codegree d-number obstruction changed')
    need(18125%29 == 0 and 55%29 != 0, 'Prime-29 divisibility witness changed')

    # The formal-codegree polynomial mod 2 is x^4+x^3+1.
    # Its values at 0 and 1 are one. Mod x^2+x+1, x^3=1 and x^4=x,
    # so its remainder is x, proving irreducibility of the quartic over F2.
    def rem(p,q):
        while p.bit_length() >= q.bit_length():
            p ^= q << (p.bit_length()-q.bit_length())
        return p
    need(rem(0b11001,0b111) == 0b10, 'Quartic quadratic-factor test changed')
    need(sum((0b11001 >> i)&1 for i in range(5))%2 == 1,
         'Quartic F2 evaluation changed')
    files = [path, ROOT/'evidence/r3472_focus_20261022/morita/manuscript.tex',
             ROOT/'evidence/r3472_focus_20261022/morita/verify.py']
    return {
        'schema': 'r3472-independent-morita-arithmetic-review/v1', 'status': 'PASS',
        'code_imports_from_morita_verifier': False,
        'source_nonunit_diagonal_coefficients': [2]*7,
        'source_invertible_ids': [0],
        'C5_complete_type_domain_with_multiplicity_steps': [list(x) for x in types],
        'C5_complete_profiles_including_fixed_orbit_check': found,
        'formal_codegree_minimal_polynomial_descending': list(reversed(scaled)),
        'formal_codegree_prime_obstruction': 29,
        'formal_codegree_divisibility_remainder': 15625,
        'categorical_argument_review': 'evidence/r3472_focus_20261022/review/ALL_MORITA_AUDIT.md',
        'general_categorification_status': 'unresolved',
        'inputs': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files},
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    result = receipt()
    path = HERE/'independent_morita_verification.json'
    if args.write:
        path.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    else:
        need(json.loads(path.read_text()) == result, 'Saved independent audit differs')
    print(json.dumps(result, indent=2, sort_keys=True))
