#!/usr/bin/env python3
"""Check the finite trace and norm constraints on proper-subfield ratios in degree six."""

from fractions import Fraction as Q
from math import gcd, isqrt, lcm


def quadratic_candidates():
    before_square = []
    retained = []
    # Positivity and the q-Fourier bound force a in {5,8,12}, B<=2,
    # and A<=2+sqrt(gcd(a,4))*B<=6.
    for a in (5, 8, 12):
        for B in (1, 2):
            for A in range(1, 7):
                discriminant = a*B*B
                n4 = A*A-discriminant
                if n4 <= 0 or n4 % 4:
                    continue
                N = n4//4
                if (A-2)**2 > gcd(a, 4)*B*B:
                    continue
                before_square.append((a, A, B, N))
                # N_K(alpha)=N^3 is a square, so N is a square.
                if isqrt(N)**2 != N:
                    continue
                if a*(2*(2*N-A)**2+(A-2)**2) > 4*discriminant:
                    continue
                retained.append((a, A, B, N))
    assert before_square == [(5, 3, 1, 1), (8, 4, 1, 2),
                             (8, 6, 2, 1), (12, 4, 1, 1)]
    assert retained == [(5, 3, 1, 1)]
    return retained


def positive_irreducible_cubics(A):
    # For positive roots, 3B<=A^2 and 27C<=A^3.
    for B in range(1, A*A//3+1):
        for C in range(1, A**3//27+1):
            discriminant = (A*A*B*B-4*B**3-4*A**3*C-27*C*C
                            +18*A*B*C)
            if discriminant <= 0:
                continue
            # Positive discriminant gives three distinct real roots.  The
            # polynomial at -x is strictly negative for x>=0, so all are positive.
            # Any rational root is an integer, between 1 and their sum A.
            if any(r**3-A*r*r+B*r-C == 0 for r in range(1, A+1)):
                continue
            yield B, C, discriminant


def cubic_candidates():
    # This verifies the elementary trace lower bound A>=5.
    assert not [p for A in range(1, 5) for p in positive_irreducible_cubics(A)]
    retained = []
    for b in (7, 9, 13, 19):
        for A in range(5, 13):
            # Necessary convolution bound; in particular A<=12,8,6,5 respectively.
            if b*(A-3)**2 >= 4*A*A:
                continue
            for B, C, discriminant in positive_irreducible_cubics(A):
                root = isqrt(discriminant)
                if root*root != discriminant or root % b:
                    continue
                # Exact d-number criterion for X^3-A*X^2+B*X-C.
                if A**3 % C or B**3 % (C*C):
                    continue
                for h1 in range(1, A-1):
                    h2 = A-1-h1
                    h_fourier_square = A*A-3*(A-1+h1*h2)
                    if b*h_fourier_square > A*A-3*B:
                        continue
                    retained.append((b, A, B, C, h1, h2))
    assert retained == [(7, 5, 6, 1, 2, 2),
                        (7, 6, 5, 1, 2, 3),
                        (7, 6, 5, 1, 3, 2)]
    assert all(b*(A*A-3*(A-1+h1*h2)) == A*A-3*B
               for b, A, B, C, h1, h2 in retained)
    return retained


def cubic_minimum_restriction():
    # Write u_j=2*cos(2*pi*j/7), u_1>u_2>u_3, and alpha=-sum c_j*u_j.
    # These exact interval signs isolate all three roots and give
    # u_1>31/25, u_2<-11/25, u_3<-7/4.
    polynomial = lambda x: x**3+x*x-2*x-1
    intervals = [(Q(31, 25), Q(5, 4)), (Q(-9, 20), Q(-11, 25)),
                 (Q(-2), Q(-7, 4))]
    assert all(polynomial(a)*polynomial(b) < 0 for a, b in intervals)
    assert all(intervals[i][0] > intervals[i+1][1] for i in range(2))
    assert (Q(31, 25)+Q(7, 4))/7 > Q(5, 12)
    assert (Q(31, 25)+Q(11, 25))/7 == Q(6, 25)

    # Check the unique solutions of 7*C*v=h+2*A for the three trace cases.
    cases = [
        (5, [[2, 2, 1], [2, 1, 2], [1, 2, 2]], [1, 2, 2],
         [Q(2, 7), Q(2, 7), Q(3, 7)]),
        (6, [[3, 1, 2], [1, 2, 3], [2, 3, 1]], [1, 2, 3],
         [Q(2, 7), Q(3, 7), Q(2, 7)]),
        (6, [[3, 1, 2], [1, 2, 3], [2, 3, 1]], [1, 3, 2],
         [Q(5, 21), Q(8, 21), Q(8, 21)])]
    for A, C, h, v in cases:
        assert sum(v) == 1
        assert [7*sum(x*y for x, y in zip(row, v)) for row in C] == [x+2*A for x in h]
    # For the third case P=alpha*Q=(3+2*alpha)/21, and its cubic moment fails.
    bad_moment = Q(3*9+12*6+4*(6*6-2*5), 21**2)
    assert bad_moment == Q(203, 441) and bad_moment > Q(3, 7)
    # In the trace-five case 3*(Q_0-min Q)>5/4, whereas its allowed
    # pair-splitting bound is always <5/4.  The comparisons below certify
    # (1+2/sqrt(7))/sqrt(2)<5/4 and 3/sqrt(7)<5/4.
    assert 4*25**2 < 19**2*7  # 2/sqrt(7)<19/25
    assert 176**2 < 125**2*2  # (44/25)/sqrt(2)<5/4
    assert 12**2 < 5**2*7

    # The trace-six survivor has Q_0-min Q=(u_1-u_2)/7>6/25.
    # Thus sqrt(h/a)+2*sqrt(h/lcm(a,7))>18/25.  Since h<=4,
    # this implies a<70.  Sieve that proved finite range with upward roots.
    assert 36*625 < 324*70
    squarefree = lambda n: all(n % (p*p) for p in range(2, isqrt(n)+1))
    fundamental = lambda a: ((a % 4 == 1 and squarefree(a)) or
                             (a % 4 == 0 and a//4 % 4 in (2, 3)
                              and squarefree(a//4)))
    scale = 10**12
    upper = lambda n, d: Q(isqrt(n*d*scale*scale)+1, d*scale)
    retained = []
    for a in range(5, 70):
        if not fundamental(a):
            continue
        h = gcd(a, 4)
        bound = upper(h, a)+2*upper(h, lcm(a, 7))
        if bound > Q(18, 25):
            retained.append(a)
    assert retained == [5, 8, 12, 28, 56]
    # The full-sextic trace-form norm identity also gives a rational
    # norm-minus-one element in the quadratic subfield. The candidates
    # 12,28,56 have an odd ramified prime 3 or 7 congruent to 3 modulo 4,
    # which obstructs that rational norm equation.
    retained = [a for a in retained if a % 3 and a % 7]
    assert retained == [5, 8]
    return retained


if __name__ == "__main__":
    quadratic = quadratic_candidates()
    cubic = cubic_candidates()
    print("Proper quadratic ratio: a=5, alpha=(3-sqrt(5))/2; the minimum-coset argument gives b=7 or9.")
    print("Proper cubic ratios:")
    for b, A, B, C, h1, h2 in cubic:
        print(f"  conductor {b}; polynomial X^3-{A}*X^2+{B}*X-{C}; h=(1,{h1},{h2}).")
    print("All cubic survivors saturate their conductor-seven Fourier bound.")
    conductors = cubic_minimum_restriction()
    print("After the p-moment, q-minimum and rational-norm constraints: only X^3-6*X^2+5*X-1 remains,")
    print("with quadratic conductor in", conductors)
