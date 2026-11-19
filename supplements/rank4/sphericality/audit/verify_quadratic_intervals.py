#!/usr/bin/env python3
"""Exact short quadratic character chart and unit-norm second-moment comparisons."""

from fractions import Fraction as Q
from itertools import combinations_with_replacement, product
from math import gcd, isqrt


def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


def quadratic_chart():
    # All equivalences are coordinate permutations, simultaneous signs within
    # coordinates, and conjugation (one common sign for the radical parts).
    def key(s, t):
        return min(tuple(sorted((x, sign*y if x else abs(y))
                                for x, y in zip(s, t))) for sign in (-1, 1))

    # d, t, s, norm, reciprocal trace, squared norm of primitive vector
    printed = [
        (5, (2,-1,-1), (0,1,1), 20, Q(1,2), 1),
        (5, (2,-1,1), (0,1,1), 25, Q(2,5), 6),
        (5, (-3,-1,-1), (1,1,1), 25, Q(3,5), 6),
        (2, (2,-2,-2), (0,2,2), 32, Q(1,2), 1),
        (3, (0,-4,-2), (0,2,2), 36, Q(2,3), 2),
        (5, (-3,-1,1), (1,1,1), 45, Q(1,3), 2),
        (5, (-3,-1,-4), (1,1,2), 45, Q(2,3), 2),
        (13, (2,-3,-3), (0,1,1), 52, Q(1,2), 1),
        (2, (2,-2,2), (0,2,2), 64, Q(1,4), 3),
        (2, (-2,-2,-6), (2,2,4), 64, Q(3,4), 3),
        (2, (-4,-2,0), (2,2,2), 72, Q(1,3), 2),
        (5, (2,-4,-4), (0,2,2), 80, Q(1,2), 1),
        (3, (2,-4,0), (0,2,2), 96, Q(1,4), 3),
        (3, (-4,-4,-6), (2,2,4), 96, Q(3,4), 3),
    ]
    expected = {(d, key(s,t), L, ell, n) for d,t,s,L,ell,n in printed}
    found = set()
    for d in range(2, 50):
        if any(d % (i*i) == 0 for i in range(2, isqrt(d)+1)):
            continue
        for s in combinations_with_replacement(range(isqrt(99//d)+1), 3):
            J = sum(x*x for x in s)
            if d*J >= 100 or sum(x != 0 for x in s) < 2:
                continue
            n = d*J-4
            for t in product(range(-isqrt(n), isqrt(n)+1), repeat=3):
                if sum(x*x for x in t) != n:
                    continue
                if d % 4 == 1:
                    if any((x-y) % 2 for x,y in zip(s,t)):
                        continue
                elif any(x % 2 for x in s+t):
                    continue
                C = sum(x*y for x,y in zip(s,t))
                L, remainder = divmod((d*J)**2-d*C*C, 4)
                if remainder or not d*J < L < 100 or (d*J)**2 % L:
                    continue
                primitive = [J*y-C*x for x,y in zip(s,t)]
                divisor = gcd(*primitive)
                squared = sum((v//divisor)**2 for v in primitive)
                found.add((d,key(s,t),L,Q(d*J,L),squared))
    require(found == expected, ('chart discrepancy', found ^ expected))
    return printed


def F(x):
    return (1-x)**2+x*x


def fixed_input(p, lower_U, kappa=1):
    def H(t):
        return lower_U + F(p*t) - 1 - Q(1,50)
    return p, kappa, H


def verify_subdivision(name, dimension, rows, right_endpoints):
    checks = 0
    for p, kappa, H in rows:
        # isqrt(floor(q)) is floor(sqrt(q)) for nonnegative rational q.
        lower = Q(isqrt(int(10_000*dimension*kappa/p)), 100)
        a = Q(0)
        for endpoint in right_endpoints:
            b = Q(endpoint,1000)
            Z = max(dimension*a, lower)
            remainder = Z*H(b)-3
            require(remainder > 0 and remainder**2 > 3*(Z-1),
                    (name, p, a, b, Z, remainder))
            a = b
            checks += 1
    print(f'{name}: {checks} endpoint pairs passed')
    return checks


def main():
    chart = quadratic_chart()
    print('All 14 short character rows and idempotent norms agree.')
    ordinary = {}
    for _,_,_,M,ell,_ in chart:
        if M == 20 or (M,ell) == (25,Q(2,5)):
            continue
        p = 1-ell
        U = F(p)-Q(2,M)
        ordinary[p] = min(ordinary.get(p, U), U)
    specified = {Q(1,4):Q(19,32), Q(1,3):Q(1,2), Q(2,5):Q(11,25),
                 Q(1,2):Q(7,16), Q(2,3):Q(23,45), Q(3,4):Q(19,32)}
    require(ordinary.keys() == specified.keys() and
            all(ordinary[p] >= v for p,v in specified.items()), 'ordinary chart')
    def rational_row(g,j):
        p = 1-Q(1,g)-Q(1,j)
        return fixed_input(p, p*p+Q(1,g*g)+Q(1,j*j), Q(5,2) if (g,j)==(3,3) else 1)
    pairs = [(g,j) for g in range(3,10) for j in range(g,99//g+1)
             if not ({g,j} & {5,8,16} or (g,j) in {(3,4),(3,12),(9,9),(4,4)}
                     or (g==4 and j%2))]
    require(len(pairs)==52, 'rational character pair count')
    squares = {a*a for a in range(1,10)}
    exceptional = {(g,j) for g,j in pairs if g*j in squares | {5*x for x in squares}}
    require(exceptional == {(3,3),(3,15),(3,27),(4,20),(6,6),(7,7)}, 'exceptional field')
    def large(t):
        return (1-t)**2/(2*(1+t*t))-Q(1,25)
    repeated = [fixed_input(Q(3,5),Q(11,25))]
    cases = [
        ('Large ordinary product', 1000, [(Q(1),1,large)], [60,190,360,382]),
        ('Quadratic rows', 1000, [fixed_input(p,u) for p,u in specified.items()], [90,220,340,382]),
        ('Repeated five, smaller units', 1000, repeated, [60,130,230,268]),
        ('Repeated five, all units', 3000, repeated, [150,340,382]),
        ('Rational pairs, smaller units', 1000, [rational_row(*x) for x in pairs], [46,52,75,140,220,268]),
        ('Rational pairs, exceptional unit', 1000, [rational_row(*x) for x in sorted(exceptional-{(3,3)})],
         [100,240,340,370,382]),
    ]
    total = sum(verify_subdivision(*case) for case in cases)
    print(f'All {total} endpoint pairs passed using exact arithmetic.')


if __name__ == '__main__':
    main()
