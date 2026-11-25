#!/usr/bin/env python3
"""Independent exact arithmetic audit of the conductor28 closing argument."""
from fractions import Fraction as Q


def squareclass(n):
    result=1;p=2
    while p*p<=n:
        e=0
        while n%p==0:n//=p;e+=1
        if e%2:result*=p
        p+=1
    return result*n


def main():
    lam=Q(63,64);ratio=Q(127,4)
    def mixed(t,s):return lam*(t*t+(Q(1,3)-t)**2+2*s*s)
    assert mixed(Q(1,7)/ratio,Q(1,7))-Q(1,7)==Q(27339,7225792)
    assert mixed(Q(23,5334),Q(23,168))-Q(1,7)==Q(144481,231225344)
    assert Q(7,18)*Q(15,17)**2>Q(1,14)
    assert Q(7,18)*Q(11,21)**2>Q(1,14)
    assert lam/6==Q(21,128)>Q(1,7)
    # For a=3,b>=7 the mass forces c4,d4or6 and b<42.
    survivors=[]
    for b in range(7,42,2):
        if b%8 not in (3,7):continue
        for d in (4,6):
            mass=Q(1,3)+Q(1,b)+Q(1,4)+Q(1,d)
            if Q(6,7)<mass<1 and squareclass(3*b*4*d)==7:
                survivors.append((3,b,4,d))
    assert survivors==[]
    # With a=b3 and c>=8 the mass forces c8or10; the largest d is14.
    for c in (8,10):
        for d in range(c,16,2):
            mass=Q(2,3)+Q(1,c)+Q(1,d)
            if Q(6,7)<mass<1 and squareclass(9*c*d)==7:
                survivors.append((3,3,c,d))
    assert survivors==[(3,3,8,14)]
    # The c6 branch needs no categorical exclusion: d=42h².
    assert Q(1,6)+Q(1,42)==Q(4,21)
    print('Conductor28: all exact mass gaps and finite squareclass branches verified.')
    print('Only residual tuple before the mixed bound:',survivors[0])


if __name__=='__main__':main()
