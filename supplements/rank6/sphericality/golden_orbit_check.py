"""Exact bounds for three quadratic codegree orbits, with one orbit 5 +/- sqrt(5)."""
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


def parameter_tuples():
    for e in (0, 1):
        for f in (0, 1):
            for r in range(-1, 7):
                ratio = mul(power_u(r), {-1: inv_v, 0: one, 1: v}[f-e])
                for a in range(1, 10):
                    if not greater(ratio, (a, 0)):
                        continue
                    if f > e and a % 5:
                        continue
                    w = trace_seq(e, 0)*trace_seq(f, r+1) - trace_seq(e, 1)*trace_seq(f, r)
                    assert 0 < abs(w) <= 720
                    for h in divisors(2*a*abs(w)):
                        for b in range(-11, 3):
                            if 2*r+f >= 2*b+e:
                                yield e, f, r, a, h, b


def small_allowed(tuple_, k):
    e, f, r, a, h, b = tuple_
    j, l = k+b, k+r
    if j < 1 or l < 0 or 2*l+f < 2:
        return False
    B, G, C = trace_seq(e, k), trace_seq(e, j), trace_seq(f, l)
    m = 2*(B + h*G)
    if m % h or m % a or (a*C-B) % h:
        return False
    n, M = m//h, m//a
    if (e == 0 and (m % 5 or n % 5)) or (f == 0 and M % 5):
        return False
    # The squared gap at a codegree z P_i equals (T_i^2 - 4/N(P_i))/z^2.
    return (20*((5**e*B*B-4) + h*h*(5**e*G*G-4)) <= 3*5**e*m*m
            and 20*(5**f*C*C-4) <= 3*5**f*M*M)


@cache
def large_mass_square(h, b):
    x = scale(power_u(b), h)
    one_plus_x = add(one, x)
    return x, scale(mul(one_plus_x, one_plus_x), 3)


def large_allowed(tuple_):
    e, f, r, a, h, b = tuple_
    x, right = large_mass_square(h, b)
    # (1-epsilon)/(1+epsilon), epsilon = 10^-9
    eta_sq = F(10**9-1, 10**9+1)**2
    if greater(scale(add(one, mul(x, x)), 5*eta_sq), right):
        return False
    # c1 = v/5 and 1/c1 = 3-phi
    factor = {-1: (3, -1), 0: one, 1: scale(v, F(1,5))}[f-e]
    y = scale(mul(factor, power_u(r)), a)
    return not greater(scale(mul(y, y), 5*eta_sq), right)


if __name__ == "__main__":
    tuples = list(parameter_tuples())
    large = [t for t in tuples if large_allowed(t)]
    small = [(t,k) for t in tuples for k in range(24) if small_allowed(t, k)]
    expected = [(0,0,1,1,1,1), (1,1,1,1,1,1)]
    assert sorted(large) == expected
    assert sorted(small) == sorted((t,k) for t in expected for k in range(24))
    assert greater(power_u(26), (10**9, 0))
    print(len(tuples), "parameter tuples;", len(small), "small cases;", len(large), "unbounded cases")
    print("In every case D = G.")
