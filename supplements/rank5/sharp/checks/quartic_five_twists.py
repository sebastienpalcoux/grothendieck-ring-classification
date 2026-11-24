"""Verify the cyclotomic inequality for either quartic field at codegree five."""

if not __debug__:
    raise RuntimeError("Run this verifier with Python assertions enabled")

from fractions import Fraction as Q
from functools import lru_cache
from itertools import product
from math import factorial, gcd, prod

MOMENTS = (1, 2, 3, 4, 6)
CONDITIONAL = (32214, 21426, 10787)
UNCONDITIONAL = (188, 1558, 1039, 1511, -403)


@lru_cache(None)
def primes(n):
    return tuple(p for p in (2, 3, 5, 7) if n % p == 0)


def mobius(n):
    ps = primes(n)
    return 0 if any(n % (p*p) == 0 for p in ps) else (-1)**len(ps)


def phi(n):
    for p in primes(n):
        n = n//p*(p-1)
    return n


@lru_cache(None)
def cos_scaled(c, a):
    """Integer within 15 units of 10^8*cos(2*pi*a/c), rounded down at the midpoint approximation."""
    a %= c
    a = min(a, c-a)
    # 3.14159265 < pi < 3.14159266. Taylor's remainder on [0, pi] is < 10^-11.
    t = Q(2*a*314159265, c*10**8)
    value = sum((-1)**i*t**(2*i)/factorial(2*i) for i in range(13))
    return (value*10**8).__floor__()


@lru_cache(None)
def restriction(c, n, j):
    ps = [p for p in primes(n) if c % p]
    s = prod((Q(p-1, p) for p in ps), start=Q(1))
    terms = []
    for e in product((0, 1), repeat=len(ps)):
        d = prod(p for p, used in zip(ps, e) if used)
        if j*d*c % n == 0:
            a = j*d*c//n * pow(d, -1, c)
            terms.append((Q((-1)**sum(e), d)/s, a % c))
    return terms


def conditional_lower(c, n, j, a):
    # Inclusion-exclusion over the residue classes divisible by p and u=1 mod c.
    return sum(v * (cos_scaled(c, a*t) - (15 if v>0 else -15))
               for v, t in restriction(c, n, j)) / Q(10**8)


def verify():
    minimum = None
    for c in [15, 20]:
        for h, k, l, m in product(range(5), range(3), range(3), (1,7)):
            n = 2**h * 3**k * 5**l * m
            base = Q(20100)
            for j, v in zip(MOMENTS, UNCONDITIONAL):
                d = n//gcd(n,j)
                base += 4*v*Q(mobius(d),phi(d))
            base -= 100000*(n==1) + 20000*(n==25)
            for a in range(1,n+1):
                if gcd(a,n)>1:
                    continue
                b = base+sum(v*conditional_lower(c,n,j,a)
                             for j,v in enumerate(CONDITIONAL,1))
                minimum = b if minimum is None else min(minimum,b)
    assert minimum>90, minimum
    print('The codegree-five twist inequality holds for both conductors, with positive slack.')


if __name__=='__main__':
    verify()
