"""Finite arithmetic in the proof of the quartic dimension bound (Python 3)."""
from collections import Counter
from fractions import Fraction as F
from itertools import product
from math import comb, isqrt


def require(test, message):
    if not test:
        raise ValueError(message)


def square(n):
    return n >= 0 and isqrt(n) ** 2 == n


def factor_over_integers(t, s, r, h):
    """The polynomial is monic and all its roots are positive."""
    for b in range(1, h + 1):
        if h % b:
            continue
        if ((((b-t)*b+s)*b-r)*b+h) == 0:
            return True
        d = h // b
        for a in range(1, t):
            c = t - a
            if a*c+b+d == s and a*d+b*c == r:
                return True
    return False


def outside_fields():
    quartics = set()
    for h in (1, 4):
        for t in range(4, 41):
            for z in range(2*isqrt(h), t*t//4-2*isqrt(h)+1):
                B = z*z - 4*h
                for s in range(z+1, 3*t*t//8+1):
                    A = t*t - 4*s + 4*z
                    if A < 0 or not square(A*B):
                        continue
                    for sign in (-1, 1):
                        twice_r = t*z + sign*isqrt(A*B)
                        r = twice_r//2
                        if twice_r % 2 or not 1 <= r <= t**3//16:
                            continue
                        if h == 4 and (t%2 or s%2 or r%4):
                            continue
                        S = t*t - 2*s - 2*z
                        J = s*s + 2*s*z - 3*z*z - 4*t*r + 16*h
                        if min(S,J) <= 0 or factor_over_integers(t,s,r,h):
                            continue
                        delta = A or B
                        if square(delta) or not (square(J) or square(J*delta)):
                            continue
                        quartics.add((1,-t,s,-r,h))
    quadratics = {(1,-t,h) for h in (1,2) for t in range(3,21)
                  if not square(t*t-4*h) and (h==1 or t%2==0)}
    return quartics | quadratics


def fixed_field():
    """Integral-basis coordinates at trace <=16 in Q(sqrt(2),sqrt(5))."""
    polynomials = set()
    for t in range(2,17,2):
        for b,c,e in product(range(-11,12), range(-7,8), range(-5,6)):
            if (t-c)%4 or (b-e)%4 or c%2 or e%2:
                continue
            if max(2*b*b,5*c*c,10*e*e) >= t*t or b==c==e==0:
                continue
            a = 5*c*c - 2*b*b - 10*e*e
            B,C,J = 2*a-20*c*c, -80*b*c*e, a*a-80*b*b*e*e
            s,r,h = (6*t*t+B)//16,(4*t**3+2*t*B-C)//64,(t**4+B*t*t-C*t+J)//256
            if min(s,r,h) <= 0 or not square(h):
                continue
            polynomial = (1,-t,s,-r,h)
            if any(coef**4 % h**i for i,coef in enumerate(polynomial)):
                continue
            # Every real root is positive by the alternating signs.
            if roots_to_right(polynomial, 1, 1)==4:
                continue
            if sum(x!=0 for x in (b,c,e))==1:
                require(square(h) and t%2==0, 'quadratic multiplicity')
                polynomial = (1,-t//2,isqrt(h))
            polynomials.add(polynomial)
    return polynomials


def roots_to_right(coeffs, n, den):
    """Count real roots strictly greater than n/den, with multiplicity.
    Descartes' sign rule is exact for a real-rooted polynomial. Evaluate
    the translated coefficients with homogeneous integer arithmetic.
    """
    ascending = coeffs[::-1]
    signs = []
    for j in range(len(coeffs)):
        v = sum(ascending[k]*comb(k,j)*n**(k-j)*den**(len(coeffs)-1-k)
                for k in range(j,len(coeffs)))
        if v:
            signs.append(v>0)
    return sum(p!=q for p,q in zip(signs,signs[1:]))


def intervals(coeffs):
    scale = 65536
    degree = len(coeffs)-1
    roots = []
    for i in range(degree):
        low, high = 0, -coeffs[1]*scale
        while high-low>1:
            middle = (low+high)//2
            if roots_to_right(coeffs,middle,scale) >= degree-i:
                low = middle
            else:
                high = middle
        roots.extend([(F(low,scale), F(high,scale))]*(4//degree))
    return roots


def check(polynomials,A,B,l,m,bound):
    worst = F(0)
    worst_polynomial = ()
    counts = Counter()
    for f in sorted(polynomials):
        counts[len(f)-1] += 1
        roots = intervals(f)
        upper = sum((l*hi+m)**2/(A*lo*lo+B) for lo,hi in roots[1:])
        require(upper<bound, ('square bound',f,upper,bound))
        if upper>worst:
            worst,worst_polynomial = upper,f
    # An outward-rounded numerator with denominator 1000, for the printed proof.
    ceiling = -((-1000*worst.numerator)//worst.denominator)
    print(f'quadratic {counts[2]}, quartic {counts[4]}, '
          f'upper {ceiling}/1000, extremal polynomial {worst_polynomial}')
    return counts,ceiling


def main():
    d,r=F(1,950),F(1,150)
    c = F(4,5)-d*d-(1-d)**2/3
    S,W=1-4*r,c-2*r+4*r*r
    lower=r*S*(S*S-2*W)/9+r*r*(S*S-W)/2+r**3*S+r**4
    require(lower>d*(1-d)**3/27,'translated product')
    require((1-r-F(1,40))**2>2*c,'smallest remaining coordinate')
    require(F(5,3)-2*d/3-r-F(17,20)>F(4,5),'ordinary moment contradiction')
    require(8-2*d-F(6,80)-F(41,10)>F(15,4),'exceptional moment contradiction')
    phi=lambda x:x**3*(1-3*x)
    require(phi(F(1,90))>d*d and phi(F(1,27))>d/27,'product endpoints')
    q=F(1,90)
    require((F(15,4)-4*(q*q+(1-q)**2/3))/5<F(49,100),'ordinary square sum')
    require(F(1,200)-d/2>d,'pair comparison')
    S=F(3,40)
    margin=F(21,5)-32*S/5+88*S*S/15-2*d*(2*S+3)/3-F(15,4)
    require(margin==F(3,3800),'two smallest signed weights')
    psi=lambda x:x*(S-x)**2*(1-2*S+x)
    require(12*F(1,27)**2+F(21,5*27)-F(39,160)<0,'product concavity')
    require(psi(F(1,27))>psi(F(1,80))>d/27,'concave product endpoints')
    general=check(outside_fields(),1,1,F(1,3),F(1,2),F(17,20))
    fixed=check(fixed_field(),5,4,F(1),F(3),F(41,10))
    require(general==(Counter({2:27,4:291}),841),'generic summary')
    require(fixed==(Counter({2:5,4:3}),4068),'exceptional summary')


if __name__=='__main__':
    main()
