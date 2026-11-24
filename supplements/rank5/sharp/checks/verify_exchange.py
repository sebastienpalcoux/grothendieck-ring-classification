"""Exact checks for an invertible transposing two simples in rank five.

Checks the separating linear forms for the remaining two conductor-five parameters.
There is no input file or external dependency.
"""
from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import product
from math import gcd


def radical_sign(a, b, radicand):
    """Sign of a+b sqrt(radicand) for positive nonsquare radicand."""
    if a < 0:
        return -radical_sign(-a, -b, radicand)
    if b >= 0:
        return int(bool(a or b))
    return (a*a > radicand*b*b) - (a*a < radicand*b*b)


@dataclass(frozen=True)
class Quadratic:
    """Coordinates in 1,sqrt(5)."""
    a: Q = Q(0)
    b: Q = Q(0)

    def __add__(self, other):
        return Quadratic(self.a+other.a, self.b+other.b)

    def __mul__(self, other):
        if isinstance(other, Quadratic):
            return Quadratic(self.a*other.a + 5*self.b*other.b,
                             self.b*other.a + self.a*other.b)
        return Quadratic(self.a*other, self.b*other)

    __rmul__ = __mul__

    def conjugate(self):
        return Quadratic(self.a, -self.b)

    def sign(self):
        return radical_sign(self.a, self.b, 5)


K = Quadratic
ONE = K(1)
ZERO = K()
FIRST_FORMS = [(2,1,0,1,-2,-2,0), (5,4,1,4,-4,-10,0)]
SECOND_FORMS = [(2,0,-1,1,-2,1,1,-2,0), (3,1,0,2,-2,0,-1,-2,-2),
                (2,1,-1,2,0,1,-1,-3,-3), (2,1,-1,2,0,1,-1,-4,-4),
                (2,0,-1,0,-1,0,2,-2,0), (3,4,-1,2,0,2,0,-10,0)]


def averaged_power(order, exponent, moment):
    common = gcd(order, moment)
    reduced = order//common
    h = reduced//5 if reduced % 5 == 0 else reduced
    phi = sum(gcd(j, h) == 1 for j in range(h))
    mobius = 0 if h % 4 == 0 or h % 9 == 0 else (-1)**((h % 2 == 0)+(h % 3 == 0))
    avg = Q(mobius, phi)
    if reduced % 5:
        return K(avg)
    k = exponent*(moment//common)*pow(h, -1, 5) % 5
    return K(-avg/4, avg/4 if k in (1, 4) else -avg/4)


def root_columns(f):
    period, moments = (20, 2) if f == 20 else (180, 3)
    columns = {(ONE,) + (ZERO,)*(2*moments+2)}
    for order in range(1, period+1):
        if period % order:
            continue
        for exponent in range(order):
            if gcd(exponent, order) != 1:
                continue
            row = [ONE]
            for j in range(1, moments+1):
                a = averaged_power(order, exponent, j)
                row.extend((a, a.conjugate()))
            row.extend((K(order == 1), K(order == 2)))
            columns.add(tuple(row))
    return columns


def required_moments(f):
    if f == 20:
        x, z, p = K(9, 4), K(4, 2), K(Q(9,40), -Q(1,10))
        extra_plus, minus = Q(1,400)+Q(1,8), Q(0)
        third_indicators = [(0, 0)]
    else:
        x, z, p = K(6, 3), K(14, 6), K(Q(3,20), -Q(1,15))
        extra_plus, minus = Q(1,25)+Q(1,8)+Q(9,100)-Q(2,70), Q(1,8)
        # For a cubic rotation on an H-dimensional space, the real part
        # of its trace is (3*r-H)/2, where r is the multiplicity of 1.
        # The indicators themselves need not be real.  Here H=4 for the
        # combined X,Y rotation spaces and H=19 for the Z rotation space.
        third_indicators = list(product(
            (Q(3*r-4, 2) for r in range(5)),
            (Q(3*r-19, 2) for r in range(20))))
    plus = p*p + p.conjugate()*p.conjugate() + K(extra_plus)
    for sx, sz in product((-2,0,2), (-1,1)):
        m2 = p*(K(2)+sx*x+sz*z)
        for ax, az in third_indicators:
            row = [ONE, p, p.conjugate(), m2, m2.conjugate()]
            if f == 5:
                m3 = p*(ONE+ax*x+az*z)
                row.extend((m3, m3.conjugate()))
            yield row+[plus, K(minus)]


def scalar_product(form, column):
    if len(form) != len(column):
        raise ValueError("Incompatible coordinates")
    return sum((a*b for a, b in zip(form, column)), ZERO)


def high_endpoints():
    for f, forms in ((20, FIRST_FORMS), (5, SECOND_FORMS)):
        columns = root_columns(f)
        targets = list(required_moments(f))
        if len(targets) != (6 if f == 20 else 600):
            raise ValueError("Incomplete second/third indicator assignments")
        for form in forms:
            if max(form[-2:]) > 0 or any(scalar_product(form, c).sign() < 0 for c in columns):
                raise ValueError(f"Invalid separating form at f={f}")
        if any(all(scalar_product(form, target).sign() >= 0 for form in forms)
               for target in targets):
            raise ValueError(f"Unexcluded indicators at f={f}")
        print(f"f={f}: {len(columns)} root columns and {len(targets)} target moment tuples checked.")


if __name__ == "__main__":
    high_endpoints()
