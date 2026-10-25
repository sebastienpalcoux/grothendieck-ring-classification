#!/usr/bin/env python3
"""Exact seed-rotation and center-induction calculation, independent of candidate S."""
from pathlib import Path
import hashlib
import json
import sympy as sp

x = sp.Symbol('x')
phi = sp.Poly(sp.cyclotomic_poly(15, x), x, domain=sp.QQ)

class K:
    def __init__(self, value=0):
        self.p = (value.p if isinstance(value, K) else sp.Poly(value, x, domain=sp.QQ)).rem(phi)
    def __add__(self, other): return K(self.p + K(other).p)
    __radd__ = __add__
    def __neg__(self): return K(-self.p)
    def __sub__(self, other): return self + -K(other)
    def __rsub__(self, other): return K(other) - self
    def __mul__(self, other): return K(self.p * K(other).p)
    __rmul__ = __mul__
    def __truediv__(self, other): return self * K(sp.invert(K(other).p, phi))
    def __rtruediv__(self, other): return K(other) / self
    def __pow__(self, n):
        if n < 0: return (K(1) / self) ** (-n)
        out, a = K(1), self
        while n:
            if n & 1: out = out * a
            a, n = a * a, n // 2
        return out
    def __eq__(self, other): return self.p == K(other).p
    def bar(self):
        return sum((K(coef) * root ** (-mon[0]) for mon, coef in self.p.terms()), K(0))
    def record(self): return str(self.p.as_expr())

def require(condition, message):
    if not condition: raise RuntimeError(message)

root = K(x)
z5, z3 = root**3, root**5
sqrt5 = 1 + 2*(z5 + z5**-1)
require(sqrt5**2 == 5, 'sqrt5 expression')
a = (5 + 3*sqrt5) / 2
b, c = a + 1, a + 2
require(a*a == 5 + 5*a, 'near-group dimension equation')
records = []
for m, seed_c, expected_nu, expected_sum in [(1, K(-1), K(-1), K(4)), (2, z3, -z3, 1+3*z3.bar())]:
    # Both j1 and j2 are anti-linear. The bars in j2 were checked on the
    # rendered primary PDF p70, not inferred from lossy pdftotext output.
    a_fn = [z5 ** (2*m*h*h) for h in range(5)]
    J1 = [[a_fn[h] if k == -h % 5 else K(0) for h in range(5)] for k in range(5)]
    J2 = [[seed_c.bar()/sqrt5 * z5**(-m*h*k) for h in range(5)] for k in range(5)]
    rotation = [[sum((J1[i][k] * J2[k][j].bar() for k in range(5)), K(0)) for j in range(5)] for i in range(5)]
    rotation2 = [[sum((rotation[i][k]*rotation[k][j] for k in range(5)), K(0)) for j in range(5)] for i in range(5)]
    rotation3 = [[sum((rotation2[i][k]*rotation[k][j] for k in range(5)), K(0)) for j in range(5)] for i in range(5)]
    require(all(rotation3[i][j] == int(i == j) for i in range(5) for j in range(5)), 'rotation cube identity')
    nu = sum((rotation[i][i] for i in range(5)), K(0))
    require(nu == expected_nu, 'actual seed third indicator')
    G3 = sum((z5**(3*m*g*g) for g in range(5)), K(0))
    known_c_sum = sum((z5**(3*m*k*l) for k in range(5) for l in range(k+1, 5)), K(0))
    factor_c_sum = z5**(-3*m) + z5**(-12*m)
    require(known_c_sum == G3*factor_c_sum, 'unordered c-label orbit sum')
    D3 = (5*c*nu - b*G3 - c*known_c_sum)/(a*G3)
    require(D3 == expected_sum, 'sum of four actual D twists cubed')
    require((b*G3 + c*known_c_sum + a*G3*D3)/(5*c) == nu, 'induction indicator reconstruction')
    records.append({'m':m,'seed_c':seed_c.record(),'nu3_rho':nu.record(),'D_twist_cube_sum':D3.record(), 'expected_description':'4' if m == 1 else '1 + 3*zeta3^2','rotation_cube_checks':25,'candidate_S_used':False})

out = {'status':'PASS','field':'Q[x]/Phi_15(x)','root_embedding':'x=exp(2*pi*i/15); sqrt5=1+2*(x^3+x^-3)>0','source_formula':'Izumi1512.04288v2 Remark3.11 pp22–23 and §9 p70; NG tube inventory EG1208.1500 §4.3 pp44–45; Ng–Schauenburg math/0601012v3 Theorem4.1 p10','cases':records,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'scope':'Exact rotation trace and induction sum only. Categorical statements use the cited actual-category/tube inventory theorems. No unknown tube S block, candidate modular matrix, or guessed T eigenvalues used.'}
path=Path(__file__).with_suffix('.json')
path.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
