"""Verify the period-basis identities for the conductor-fifteen trace obstruction."""
from sympy import Matrix, Poly, Symbol, cyclotomic_poly

T = Symbol("T")
phi = Poly(cyclotomic_poly(15,T),T)

def period(j):
    return Poly(T**(j % 15) + T**((-j) % 15),T).rem(phi)

def real_trace(v):
    return sum((v.compose(Poly(T**j,T)).rem(phi) for j in (1,2,4,8)),
               Poly(0,T)).rem(phi).as_expr()

periods = [period(j) for j in (1,2,4,8)]
gram = Matrix([[real_trace(a*b) for b in periods] for a in periods])
assert gram == Matrix([[9,-1,-6,-1],[-1,9,-1,-6],[-6,-1,9,-1],[-1,-6,-1,9]])
assert gram.det() == 5*15**2
x = Poly(2,T) - periods[0]
P = Poly(T**4-7*T**3+14*T**2-8*T+1,T)
assert P.compose(x).rem(phi).is_zero
tau_x = Poly(2,T) - periods[2]
w = (tau_x-x)*P.diff().compose(x)
inverse = Poly(T**3-7*T**2+13*T-4,T).compose(x)
assert (w*inverse).rem(phi) == Poly(15,T)
assert sum(periods,Poly(0,T)).rem(phi) == Poly(1,T)
print("Conductor 15: integral normal basis, Fourier lengths, and trace-dual denominator verified.")
