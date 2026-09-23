"""Independent exact checks for the finite rank-three arithmetic reduction.

Run ``python audit_rank3.py``. This supplement verifies the finite table,
the polynomial identities in the center bound, and the uniform moment sign.
The manuscript contains the mathematical proofs of the unbounded claims.
"""

from fractions import Fraction

import sympy as sp


def swap(row):
    k, l, m, n = row
    return l, k, n, m


def coefficients(row):
    k, l, m, n = row
    b = 7 + 3 * k * k + 3 * l * l + m * m + n * n
    c = 4 * b - 9 + (k * l - m * n) ** 2 + (2 * (k * k - l * m) - 1) ** 2
    return b, c


def finite_rows():
    out = set()
    # b < 50 forces k,l < 4 and m,n < 7; l and k strictly positive.
    for k in range(1, 4):
        for l in range(1, 4):
            for m in range(7):
                for n in range(7):
                    row = (k, l, m, n)
                    if k * k + l * l != k * n + l * m + 1:
                        continue
                    if coefficients(row)[0] >= 50:
                        continue
                    out.add(min(row, swap(row)))
    return out


rows = finite_rows()
expected = {
    min(x, swap(x))
    for x in ((1, 1, 1, 0), (2, 1, 0, 2), (2, 1, 2, 1),
              (2, 1, 4, 0), (3, 1, 0, 3))
}
assert rows == expected, (rows, expected)

t, b, c = sp.symbols("t b c")
p = t**3 - b * t**2 + c * t - c
k, l, m, n = sp.symbols("k l m n", integer=True)
mx = sp.Matrix([[0, 1, 0], [1, m, k], [0, k, l]])
my = sp.Matrix([[0, 0, 1], [0, k, l], [1, l, n]])
omega = sp.eye(3) + mx**2 + my**2
assoc = k*k + l*l - k*n - l*m - 1
b_formula = 7 + 3*k*k + 3*l*l + m*m + n*n
c_formula = 4*b_formula - 9 + (k*l - m*n)**2 + (2*(k*k-l*m)-1)**2
poly_actual = omega.charpoly(t).as_expr()
for difference in (sp.trace(omega)-b_formula,
                   poly_actual-(t**3-b_formula*t**2+c_formula*t-c_formula)):
    assert sp.rem(sp.expand(difference), assoc, k) == 0
assert sp.simplify(p.subs(t, b - 5) -
                   ((b - 5) * (c - sp.Rational(9, 2) * b +
                               (50 - b) / 2) - c)) == 0

for row in sorted(rows):
    bi, ci = coefficients(row)
    factors = sp.factor_list(p.subs({b: bi, c: ci}))[1]
    if sorted(row) == sorted((2, 1, 2, 1)):
        assert sp.expand(p.subs({b: bi, c: ci})) == sp.expand(
            (t - 3) * (t**2 - 24 * t + 36)
        )
    else:
        assert len(factors) == 1 and sp.degree(factors[0][0]) == 3
    print(row, (bi, ci), factors)

u, v, eta = sp.symbols("u v eta", real=True)
R = sp.sqrt(u**2 + 2)
M = u**2 + 4 + 2 * v
S1 = -2 * v - u * R
S2 = 2 * v - u**2 - (2 * u - 2 * eta) * R
assert sp.simplify(3 * M + 4 * S1 + 2 * S2 -
                   (u**2 + 12 + 2 * v - (8 * u - 4 * eta) * R)) == 0
assert sp.simplify(sp.Rational(3, 2) * u**2 + 12 - (8 * u - 4) * u -
                   (12 + 4 * u - sp.Rational(13, 2) * u**2)) == 0
assert sp.solve(12 + 4 * u - sp.Rational(13, 2) * u**2, u)[1] < 2

# For the Pell family p(t)=t^3-b(t-2)^2, every positive integer root
# r != 2 satisfies r - 2 | 8; all possibilities with b > 1 are below 50.
candidates = [1, 3, 4, 6, 10]
root_to_b = {
    r: Fraction(r**3, (r - 2) ** 2)
    for r in candidates
}
assert all(val < 50 for val in root_to_b.values())
print("Pell integer root constraints:", root_to_b)
print("All exact checks passed.")
