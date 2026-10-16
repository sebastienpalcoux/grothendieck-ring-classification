"""Exact arithmetic in the twist-one support theorem (not a categorification test)."""
import itertools
import sympy as s
r = s.sqrt(2)
t = s.sqrt(3)
d = 3 + 2 * r + 2 * t + r * t
D = s.expand(4 * (1 + d * d))
inv = (6 - 2 * t - r * t) / 48
if not s.expand(D * inv) == 1:
    raise ValueError('Exact twist-one arithmetic failed')
conj = lambda a, b: (6 - 2 * b * t - a * b * r * t) / 48
coeff = {}
for i, j in itertools.product(range(2), repeat=2):
    coeff[i, j] = s.expand(sum((a ** i * b ** j * conj(a, b) for a, b in itertools.product((-1, 1), repeat=2))))
if not coeff[0, 0] == s.Rational(1, 2):
    raise ValueError('Exact twist-one arithmetic failed')
if not coeff[1, 0] == 0:
    raise ValueError('Exact twist-one arithmetic failed')
if not coeff[0, 1] == -t / 6:
    raise ValueError('Exact twist-one arithmetic failed')
if not coeff[1, 1] == -r * t / 12:
    raise ValueError('Exact twist-one arithmetic failed')
if not s.expand(coeff[0, 1] ** 2) == s.Rational(1, 12):
    raise ValueError('Exact twist-one arithmetic failed')
if not s.expand(coeff[1, 1] ** 2) == s.Rational(1, 24):
    raise ValueError('Exact twist-one arithmetic failed')
u, v, w, z = s.symbols('u v w z')
expr = s.expand((u + v * r + (w + z * r) * d) * inv)
expected = u / 8 + v * r / 8 + t * (-u - v + w - z) / 24 + r * t * (-u - 2 * v - w + 2 * z) / 48
if not s.expand(expr - expected) == 0:
    raise ValueError('Exact twist-one arithmetic failed')
if not s.solve([-u - v + w - z, -u - 2 * v - w + 2 * z], (w, z)) == {w: 3 * u + 4 * v, z: 2 * u + 3 * v}:
    raise ValueError('Exact twist-one arithmetic failed')
import json
print(json.dumps({'status':'PASS','checks':['reciprocal dimension','two saturated conductor bounds','exact twist-one column equations'],'categorification_decision':None}))
