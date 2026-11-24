"""Bounds for the least simple dimension from the vacuum twist inequalities."""
from fractions import Fraction as Q
from math import isqrt

SCALE = 10**12


def upper_sqrt(value):
    root = isqrt(value.numerator*SCALE**2//value.denominator)
    return Q(root+1, SCALE)


def separates(conductor, f, m):
    """Outward rational bound for all least simple dimensions at least m."""
    s = Q(f-1, f)
    p = Q(1, 1+4*m*m)
    # The function (1+2 sqrt(D-1))/D decreases for D>=17.
    m2 = (1+4*m)*p
    capacities = []
    for pair_bound in [upper_sqrt(Q(1,5))]+[upper_sqrt(Q(2,conductor))]*2:
        reciprocal = (s-pair_bound)/2-p
        if reciprocal<=0:
            return False
        capacities.append(1/reciprocal)
    maximum = upper_sqrt(max(capacities)-1)
    total = sum(capacities)
    # |rho|=1 at f=5; at f=4, rho=0 is possible.
    rest = (Q(4,5) if f==5 else Q(1))-Q(1,4)
    if m <= maximum+upper_sqrt(total/rest)/2:
        return False
    m3 = Q(1,4)+(maximum*rest+upper_sqrt(rest*total))/m
    if f == 4:
        upper = (2003 + 3334*p + 2236*m2 + 1098*m3 + 44*upper_sqrt(Q(2,15))
                 + 22*s + 22 + 120*s + 230 - 61)/10000
        lower = Q(5,64)+(s-p)**2/3
    else:
        upper = (20100 + 32214*p + 21426*m2 + 10787*m3
                 + (188+1558+1039+1511-403)*s)/100000
        lower = Q(1,20)+(s-p)**2/3
    return upper < lower


def generator_cap(conductor, f):
    m=1
    while not separates(conductor,f,m):
        m+=1
    return m


if __name__ == '__main__':
    for c, f in ((15,4),(15,5),(20,5)):
        print(c,f,generator_cap(c,f))
