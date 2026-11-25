"""Check the small indices remaining in the three-orbit conductor-five proof."""
from fractions import Fraction as F
from functools import cache
from math import isqrt


# Arithmetic in Q(phi), represented in its usual integral basis.
def add(x, y):
    return x[0] + y[0], x[1] + y[1]


def scale(x, a):
    return a*x[0], a*x[1]


def mul(x, y):
    a, b = x
    c, d = y
    return a*c + b*d, a*d + b*c + b*d


def sign(x):
    a, b = x
    p = 2*a + b  # 2*x = p + b*sqrt(5)
    if p*b >= 0:
        t = p or b
    else:
        t = (p*p - 5*b*b)*p
    return (t > 0) - (t < 0)


def greater(x, y):
    return sign(add(x, scale(y, -1))) > 0


one = (1, 0)
u, inv_u = (1, 1), (2, -1)
v, inv_v = (2, 1), (F(3,5), F(-1,5))


@cache
def power_u(i):
    if i == 0:
        return one
    return mul(u, power_u(i-1)) if i > 0 else mul(inv_u, power_u(i+1))


@cache
def trace_seq(e, i):
    x, y = ((2, 3), (1, 2))[e]
    for step in range(max(i, 0)):
        x, y = y, 3*y-x
    for step in range(max(-i, 0)):
        x, y = 3*x-y, x
    return x


def divisors(n):
    small = [i for i in range(1, isqrt(n)+1) if n % i == 0]
    return sorted(set(small + [n//i for i in small]))


def gap_squared(family, index, scalar):
    mass = F(trace_seq(family, index), scalar)
    return mass**2 - F(4, 5**family * scalar**2)


def small_signed(family, index):
    first_trace = trace_seq(family, index)
    for h in divisors(2*first_trace):
        for j in range(1, 4):
            m = 2*(first_trace + h*trace_seq(family, j))
            if m >= 16*first_trace or m % h:
                continue
            n = m//h
            if family == 0 and (m % 5 or n % 5):
                continue
            if gap_squared(family, index, m) + gap_squared(family, j, n) <= F(3, 20):
                yield j, h, m


def small_ordinary(family, index, j, h, m):
    first_trace = trace_seq(family, index)
    for d in (0, 1):
        for ell in range(4):
            if 2*ell + d < 2*j + family:
                continue
            leading_ratio = mul(power_u(ell-index), {-1: inv_v, 0: one, 1: v}[d-family])
            ordinary_trace = trace_seq(d, ell)
            for a in divisors(m):
                scalar = m//a
                if (d > family and a % 5) or (d == 0 and scalar % 5):
                    continue
                if not greater(leading_ratio, (a, 0)) or (a*ordinary_trace-first_trace) % h:
                    continue
                if gap_squared(d, ell, scalar) <= F(3, 20):
                    yield d, ell, a


if __name__ == "__main__":
    claimed = {
        (0, 0): [(1, 1)],
        (0, 1): [(2, 1)],
        (1, 0): [(1, 1), (1, 2)],
        (1, 1): [(1, 1), (2, 1), (1, 2), (1, 4)],
    }
    for (e, k), candidates in claimed.items():
        signed = list(small_signed(e, k))
        assert [(j, h) for j, h, m in signed] == candidates
        survivors = [(j, h, d, ell, a) for j, h, m in signed
                     for d, ell, a in small_ordinary(e, k, j, h, m)]
        assert survivors == [(k+1, 1, e, k+1, 1)]
        print((e, k), "signed choices", candidates, "survivor", survivors[0])
