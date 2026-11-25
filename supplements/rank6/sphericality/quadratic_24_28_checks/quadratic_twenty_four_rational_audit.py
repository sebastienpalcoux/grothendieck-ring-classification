#!/usr/bin/env python3
"""Exact recurrence and Fourier-margin audit of the K24 rational reduction."""
from fractions import Fraction as Q
from math import gcd


def mul(x,y):return (x[0]*y[0]+6*x[1]*y[1],x[0]*y[1]+x[1]*y[0])


def main():
    U=(5,2);V=(3,1);Vp=(3,-1)
    assert mul(V,Vp)==(3,0) and mul(U,Vp)==V
    # Multiplication by U is unimodular. Thus primitive integral
    # coordinates remain primitive for every positive or negative power.
    assert 5*5-12*2==1 and gcd(*V)==gcd(*Vp)==1
    A=[2,10];B=[2,18]
    for _ in range(4):
        A.append(10*A[-1]-A[-2]);B.append(10*B[-1]-B[-2])
    # Each difference satisfies z[n+1]=10z[n]-z[n-1]. A pair
    # z1>=z0>=0 remains so forever, certifying all four infinite ratios.
    certificates=[([A[k+1]-5*A[k] for k in (0,1)],[0,48]),
                  ([B[k+1]-9*B[k] for k in (0,1)],[0,16]),
                  ([A[k+1]-5*B[k] for k in (0,1)],[0,8]),
                  ([15*B[k]-27*A[k] for k in (1,2)],[0,24])]
    for actual,expected in certificates:
        assert actual==expected and actual[1]>=actual[0]>=0
    assert [x%5 for x in A[:4]]==[2,0,3,0]
    assert [x%5 for x in B[:4]]==[2,3,3,2]
    assert [x%5 for x in A[4:6]]==[x%5 for x in A[:2]]
    assert [x%5 for x in B[4:6]]==[x%5 for x in B[:2]]
    assert Q(A[1]-2,A[1]+2)==Q(2,3)
    assert Q(A[2]-2,A[2]+2)==Q(24,25)
    assert Q(A[3]-2,A[3]+2)==Q(242,243)
    assert Q(A[4]-2,A[4]+2)==Q(2400,2401)
    def harmonic(a,b):return a*b/(a+b)
    assert harmonic(Q(48),Q(24,25))==Q(16,17)
    assert harmonic(Q(12),Q(24,25))==Q(8,9)
    assert Q(3,16)<Q(7,15)**2
    assert harmonic(Q(48),Q(242,243))==Q(5808,5953)
    assert harmonic(Q(48),Q(2400,2401))==Q(800,817)
    assert Q(5808,5953)*Q(5,12)**2==Q(3025,17859)>Q(1,6)
    assert Q(800,817)*Q(5,12)**2==Q(1250,7353)>Q(1,6)
    # The reciprocal cutoff forces g=3 and h<5; larger g already gives<=1/2.
    assert Q(1,4)+Q(1,4)<Q(8,15)
    assert [(g,h) for g in (3,4) for h in range(g,6)
            if Q(1,g)+Q(1,h)>Q(8,15)]==[(3,3),(3,4)]
    print('K24 rational reduction: primitive ratios, complete mod5 cycles, and both exact margins verified.')


if __name__=='__main__':main()
