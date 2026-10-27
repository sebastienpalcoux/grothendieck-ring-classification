"""Exact Gaussian phase of the R1768 diagonal Shintani product.

This verifies a finite arithmetic identity, not a categorification.
No floating point arithmetic or external dependencies.
"""
from fractions import Fraction as F
import json

class Q:
    def __init__(self, a=0, b=0): self.a, self.b = F(a), F(b)
    def __add__(self, o):
        o = o if isinstance(o, Q) else Q(o)
        return Q(self.a + o.a, self.b + o.b)
    __radd__ = __add__
    def __neg__(self): return Q(-self.a, -self.b)
    def __sub__(self, o): return self + -(o if isinstance(o, Q) else Q(o))
    def __rsub__(self, o): return -self + o
    def __mul__(self, o):
        o = o if isinstance(o, Q) else Q(o)
        return Q(self.a*o.a + 37*self.b*o.b, self.a*o.b + self.b*o.a)
    __rmul__ = __mul__
    def __truediv__(self, o):
        o = o if isinstance(o, Q) else Q(o)
        d = o.a*o.a - 37*o.b*o.b
        return self * Q(o.a/d, -o.b/d)
    def __rtruediv__(self, o): return Q(o)/self
    def __eq__(self, o):
        o = o if isinstance(o, Q) else Q(o)
        return self.a == o.a and self.b == o.b
    def pair(self): return [str(self.a), str(self.b)]

def require(ok, message):
    if not ok: raise ValueError(message)

rows = []
for l in range(1, 12):
    w, x, y, phase = Q(7, 1), F(12-l, 12), F(0), Q()
    trajectory = []
    for b in [14] + [2]*11:
        t = x*w + y
        term = (t*t - (w+1)*t + (1+3*w+w*w)/6)/(2*w)
        phase += term
        trajectory.append(dict(w=w.pair(), x=str(x), y=str(y), phase=term.pair()))
        x, y = (b*x+y)%1, (-x)%1
        if x == 0: x = F(1)
        w = 1/(b-w)
    require(phase == 0, f"nonzero phase at {l}")
    require(w == Q(7, 1) and x == F(12-l, 12) and y == 0, "nonclosed orbit")
    rows.append(dict(l=l, phase=phase.pair(), trajectory=trajectory))

print(json.dumps(dict(status="PASS", field="Q(sqrt(37))", rows=rows), indent=2))
