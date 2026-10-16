#!/usr/bin/env python3
"""Check scalar algebra in the proposed shorter proofs (requires SymPy).
This is not a categorical theorem prover or a classification verifier.
"""


def _require(condition, message):
    if not condition:
        raise RuntimeError(message)

import sympy as s

f, g, E, u, v, S = s.symbols('f g E u v S', positive=True)
H = lambda r: s.Rational(1,2) - 1/r + s.Rational(3,2)/r**2
J = lambda r: 1 - 2/r + 2/r**2
lower = s.Rational(3,2)*(2*H(f)+J(g)-J(f))+(f-2)/f**2+(g-2)/g**2
_require(s.simplify(lower-(s.Rational(3,2)+1/f-1/(2*f**2)-2/g+1/g**2)) == 0, 'audit/check_shortcut_algebra.py exact check failed at source line 11')
_require(s.simplify(lower.subs(g,2*f)-(s.Rational(3,2)-1/(4*f**2))) == 0, 'audit/check_shortcut_algebra.py exact check failed at source line 12')
same = s.simplify(3*H(f)+2*(f-2)/f**2)
_require(s.simplify(same-(s.Rational(3,2)-1/f+1/(2*f**2))) == 0, 'audit/check_shortcut_algebra.py exact check failed at source line 14')
_require(same.subs(f,3) == s.Rational(11,9), 'audit/check_shortcut_algebra.py exact check failed at source line 15')
_require(same.subs(f,4) == s.Rational(41,32), 'audit/check_shortcut_algebra.py exact check failed at source line 16')
_require(same.subs(f,5) > s.Rational(9,7), 'audit/check_shortcut_algebra.py exact check failed at source line 17')
large_norm = s.Rational(3,2)*(s.Rational(5,4)*H(f)+s.Rational(3,4)*J(f))+2*(f-2)/f**2
_require(s.simplify(large_norm-(s.Rational(33,16)-s.Rational(17,8)/f+s.Rational(17,16)/f**2)) == 0, 'audit/check_shortcut_algebra.py exact check failed at source line 19')
_require(large_norm.subs(f,3) == s.Rational(53,36), 'audit/check_shortcut_algebra.py exact check failed at source line 20')
_require(s.Rational(53,36) > s.Rational(9,7), 'audit/check_shortcut_algebra.py exact check failed at source line 21')

phi = (1+s.sqrt(5))/2
_require(s.simplify(phi**2-phi**-2-(-1+2*phi)) == 0, 'audit/check_shortcut_algebra.py exact check failed at source line 24')
_require(s.simplify((1-phi)**2+4-(6-phi)) == 0, 'audit/check_shortcut_algebra.py exact check failed at source line 25')
_require(s.simplify((6-phi)*(5+phi)) == 29, 'audit/check_shortcut_algebra.py exact check failed at source line 26')

mass = E**2*(u+v)
C = E**2*(u-v)
gap = (4*E**2-2*mass)*(2*E*S+2*E**2-2*mass)-(2*E-mass-C)**2
_require(s.simplify(gap/(4*E**4)-((2-u-v)*(1-u-v+S/E)-(u-1/E)**2)) == 0, 'audit/check_shortcut_algebra.py exact check failed at source line 31')

a,b,c,d,e,ff = s.symbols('a b c d e ff')
N = s.Matrix([[0,1,0,0],[1,a,b,c],[0,b,d,e],[0,c,e,ff]])
_require(s.expand(N.det()-(e**2-d*ff)) == 0, 'audit/check_shortcut_algebra.py exact check failed at source line 35')
print('PASS: scalar identities for the cubic, Fibonacci, signed-moment, and determinant shortcuts.')
print('Scope: algebraic checks only; all categorical and completeness hypotheses remain separate.')

p,c=s.symbols('p c', real=True)
F=lambda x: x*x+(1-x)**2
_require(s.simplify(F(p)+F(c*p)-1-2*(1+c*c)*(p-(1+c)/(2*(1+c*c)))**2-(1-c)**2/(2*(1+c*c)))==0, 'audit/check_shortcut_algebra.py exact check failed at source line 41')
_require(s.simplify(p*p+(1-p)**2/2+F(c*p)-1-(3+4*c*c)*(p-(1+2*c)/(3+4*c*c))**2/2-(1-2*c)/(3+4*c*c))==0, 'audit/check_shortcut_algebra.py exact check failed at source line 42')
print('PASS: both shared quadratic completion-of-squares identities.')
