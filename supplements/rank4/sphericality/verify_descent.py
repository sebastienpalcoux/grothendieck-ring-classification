"""The bounded sphericality test. Run verify.py to regenerate its ordinary input."""
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from itertools import product
from pathlib import Path
import json
import math
import sys

import sympy as sp

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'supplementary' / 'census'))
from rank4 import casimir, characteristic_polynomial, tensor

t = sp.Symbol('t')


@lru_cache(maxsize=None)
def factors(coefficients):
    polynomial = sp.Poly.from_list(coefficients, t, domain=sp.ZZ)
    return tuple(f for f, _ in polynomial.factor_list()[1])


def is_d_number(f):
    a = [int(x) for x in f.all_coeffs()]
    return all(c**f.degree() % abs(a[-1])**j == 0
               for j, c in enumerate(a[1:], 1))


def allowed_codegree_field(polynomials):
    # In the quartic case D generates the ordinary algebra. In the
    # quadratic case all codegrees belong to Q(D), and D is irrational.
    if len(polynomials) == 1 and polynomials[0].degree() == 4:
        return True
    if any(f.degree() > 2 for f in polynomials):
        return False
    radicands = set()
    for f in polynomials:
        if f.degree() == 2:
            disc = int(f.discriminant())
            if disc <= 0:
                raise ValueError("nonpositive discriminant for a self-dual ring")
            radicands.add(math.prod(p for p, e in sp.factorint(disc).items() if e % 2))
    return len(radicands) == 1


def linear_solutions(coefficient, rhs, domain):
    if coefficient == 0:
        return domain if rhs == 0 else ()
    x, remainder = divmod(rhs, coefficient)
    return (x,) if remainder == 0 and x in domain else ()


def proper_signed_lifts(n):
    v = [range(-k, k+1, 2) for k in n]
    # The signs of a,b,c can be fixed independently (also when one vanishes).
    first = [range(k % 2, k+1, 2) for k in n[:3]]
    for a, b, c, d, e, f in product(*first, *v[3:6]):
        for h in v[7]:
            gs = linear_solutions(b, b*b + d*d + e*e - 1 - a*d - c*h, v[6])
            if not gs:
                continue
            indices = linear_solutions(c, b*c + e*(d+f-a) - b*h, v[8])
            for g, i in product(gs, indices):
                if b*e - c*d + d*h - e*g + e*i - f*h:
                    continue
                for j in linear_solutions(c, c*c + e*e + f*f - 1 - a*f - b*i, v[9]):
                    if b*f - c*e + d*i - e*h + e*j - f*i:
                        continue
                    if d*f - e*e + g*i - h*h + h*j - i*i + 1:
                        continue
                    q = (a, b, c, d, e, f, g, h, i, j)
                    if any(abs(x) < bound for x, bound in zip(q, n)):
                        yield q


def norm_possible(e, requirements):
    return all(abs(int(e.TC()))**f.degree() % abs(int(f.TC()))**e.degree() == 0
               for f in requirements)


def inverse_square_sum(coefficients):
    # For a polynomial with roots f_i, differentiate or apply Vieta
    # to the reverse polynomial to obtain sum_i 1/f_i^2.
    a = coefficients
    return Fraction(a[-2], a[-1])**2 - 2*Fraction(a[-3], a[-1])


def check():
    counts = Counter()
    remaining = []
    with (ROOT / 'supplementary/census/data/rings.jsonl').open() as source:
        for record in map(json.loads, source):
            if record['tag'] != 'S':
                continue
            counts['self-dual rings'] += 1
            n = tuple(record['parameters'])
            matrices = tensor('S', n)
            if any(matrices[i][i] == [1, 0, 0, 0] for i in (1, 2, 3)):
                continue
            counts['without nontrivial invertibles'] += 1
            if any(matrices[i][i][i] >= 2 and
                   all(matrices[i][i][j] == 0 for j in (1, 2, 3) if j != i)
                   for i in (1, 2, 3)):
                continue
            counts['without a forbidden rank-two subring'] += 1
            ordinary = tuple(characteristic_polynomial(casimir(matrices)))
            F = factors(ordinary)
            if not all(map(is_d_number, F)):
                continue
            counts['ordinary d-numbers'] += 1
            if not allowed_codegree_field(F):
                continue
            counts['ordinary field test'] += 1
            signed_polynomials = set()
            for q in proper_signed_lifts(n):
                counts['proper signed tuples in this gauge'] += 1
                signed_polynomials.add(tuple(characteristic_polynomial(casimir(tensor('S', q)))))
            counts['pairs of ordinary rings and signed polynomials'] += len(signed_polynomials)
            for signed in sorted(signed_polynomials):
                G = factors(signed)
                if any(norm_possible(e, F+G) for e in G):
                    remaining.append((n, ordinary, signed))
    target = (2, 2, 2, 2, 3, 4, 2, 4, 4, 6)
    ordinary = (1, -288, 2880, -9216, 9216)
    first = (1, -96, 1728, -9216, 9216)
    second = (1, -96, 1920, -9216, 9216)
    expected = {(target, ordinary, first), (target, ordinary, second)}
    if len(remaining) != 2 or set(remaining) != expected:
        raise ValueError(f"unexpected norm-test survivors: {remaining}")
    if factors(ordinary)[0].degree() != 4:
        raise ValueError("ordinary quartic is reducible")
    moment_sums = [inverse_square_sum(ordinary) + inverse_square_sum(q) for q in (first, second)]
    if moment_sums != [1, Fraction(23, 24)] or min(moment_sums) <= Fraction(7, 8):
        raise ValueError("quartic moment test failed")
    for stage, number in counts.items():
        print(f"{stage}: {number}")
    print(f"norm-test survivors: {len(remaining)}")
    for n, ordinary, signed in remaining:
        print(f"  {n}: {signed}")
    print("remaining candidates for nonspherical categorifications: 0")


if __name__ == '__main__':
    check()
