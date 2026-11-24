"""Cubic polar profile: derive the dimension bound, then enumerate integral lattice points."""
from fractions import Fraction as Q
from math import comb, isqrt


def dimension_cap():
    # Gap between the lower twist-one atom and the limiting upper moment bound.
    gap = 1296*Q(473,1536)-340-98*Q(137,242)
    q = [Q(0)]+[98*comb(4,j)*Q(7,8)**(4-j)*Q(5,2)**j for j in range(1,5)]
    q[1] += 616+98*7
    q[2] += 550+308+1296*Q(11,16)

    def possible(n):
        # gap <= q(1/sqrt(n)). Keep the two odd powers together.
        even_gap = gap-q[2]/n-q[4]/(n*n)
        odd = q[1]+q[3]/n
        return even_gap<=0 or n*even_gap*even_gap<=odd*odd

    lo,hi=1,2
    while possible(hi):
        lo,hi=hi,2*hi
    while hi-lo>1:
        mid=(lo+hi)//2
        if possible(mid):
            lo=mid
        else:
            hi=mid
    return hi


def verify():
    h=dimension_cap()
    scale=10**6
    square_scale=scale**2
    solutions=[]
    for c in range((h+24)//5+1):
        # |b-c*(1+alpha_0)| < 2.22.
        lower_b=2246979*c-2220000
        upper_b=2246980*c+2220000
        for b in range(lower_b//scale+1,-(-upper_b//scale)):
            # 2 < a+b*alpha_1+c*alpha_1**2 < 5.
            lower_a=(2*square_scale+scale*min(445041*b,445042*b)
                     -445042**2*c)
            upper_a=(5*square_scale+scale*max(445041*b,445042*b)
                     -445041**2*c)
            c2=-b+5*c
            c1=-2*b*b-b*c+6*c*c
            c0=b**3-b*b*c-2*b*c*c+c**3
            for a in range(lower_a//square_scale+1,-(-upper_a//square_scale)):
                n=((a+c2)*a+c1)*a+c0
                e2=(3*a+2*c2)*a+c1
                if n>0 and 16*e2==11*n and isqrt(n)**2==n:
                    solutions.append((a,b,c,n))
    if solutions:
        raise ArithmeticError(solutions)
    print(f"Polar profile has D < {h}; no dimensions in its cubic embedding lattice.")


if __name__=="__main__":
    verify()
