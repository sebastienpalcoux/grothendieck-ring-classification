"""Exact finite arithmetic for the remaining quadratic signed character profiles."""

if not __debug__:
    raise RuntimeError("Run this verifier with Python assertions enabled")

from fractions import Fraction
from math import gcd, isqrt


def fundamental(c):
    radicand = c if c % 4 == 1 else c // 4
    valid_even = c % 4 == 0 and radicand % 4 in (2, 3)
    return (c % 4 == 1 or valid_even) and all(
        radicand % (p * p) for p in range(2, isqrt(radicand) + 1)
    )


def divisors(n):
    return sorted({d for j in range(1, isqrt(n) + 1) if n % j == 0
                   for d in (j, n // j)})


def positive(c, a, b):
    """The sign of a+b sqrt(c), working only with integers."""
    if b == 0:
        return a > 0
    if b > 0:
        return a >= 0 or b*b*c > a*a
    return a > 0 and a*a > b*b*c


def codegree(c, h, b):
    """Norm of (h+b sqrt(c))/2, or zero if a necessary test fails."""
    if (h-b*c) % 2 or not positive(c, h-2, -b):
        return 0
    n = (h*h-c*b*b)//4
    return n if h % c == 0 and h*h % n == 0 else 0


def radical(c, h, n):
    discriminant = h*h-4*n
    if discriminant <= 0 or discriminant % c:
        return 0
    b = isqrt(discriminant//c)
    return b if c*b*b == discriminant else 0


def sieve():
    totals = [0, 0, 0, 0, 0]
    survivors = []
    for c in range(5, 241):
        if not fundamental(c):
            continue
        bound = Fraction(gcd(c, 4), c)
        for he in range(c, 241, c):
            for be in range(1 + isqrt(he*he // c)):
                ne = codegree(c, he, be)
                if not ne or positive(c, he-240, be):
                    continue
                totals[0] += 1
                qe = Fraction(c*be*be, ne*ne)
                norms = divisors(ne)
                for g in range(3, isqrt(ne) + 1):
                    if he % g or ne % (g*g):
                        continue
                    w = 1-Fraction(1, g)-Fraction(he, ne)
                    if w <= 0:
                        continue
                    for ng in norms:
                        hg = w*ng
                        if hg.denominator != 1:
                            continue
                        hg = int(hg)
                        bg = radical(c, hg, ng)
                        if not bg or codegree(c, hg, bg) != ng:
                            continue
                        if any((he*hg + i*c*be*bg) % (2*ng) for i in (-1, 1)):
                            continue
                        if isqrt(g*ne*ng)**2 != g*ne*ng:
                            continue
                        totals[1] += 1
                        qg = Fraction(c*bg*bg, ng*ng)
                        if qe + qg > bound:
                            continue
                        totals[2] += 1
                        for nd in norms:
                            # Both conjugates exceed one, so Tr(D) < Norm(D)+1.
                            for hd in range(c, nd+1, c):
                                bd = radical(c, hd, nd)
                                if not bd or codegree(c, hd, bd) != nd:
                                    continue
                                if not positive(c, hd-he, bd-be):
                                    continue
                                if (he*hd-c*be*bd) % (2*nd):
                                    continue
                                totals[3] += 1
                                pd = Fraction(c*bd*bd, nd*nd)
                                if pd > bound or 2*pd + qe + qg > Fraction(4, c):
                                    continue
                                totals[4] += 1
                                survivors.append((c, (he, be), (hg, bg), g, (hd, bd)))
    return totals, survivors


if __name__ == '__main__':
    counts, profiles = sieve()
    print(counts, profiles)
    assert counts == [331, 50, 13, 22, 1]
    assert profiles == [(5, (20, 4), (10, 2), 4, (40, 16))]
