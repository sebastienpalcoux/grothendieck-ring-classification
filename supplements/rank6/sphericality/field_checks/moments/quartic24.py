"""Exact local obstruction for the four quartic conductor-24 trace moments."""
from itertools import product
from math import gcd

# Coordinates in the seed table are (4a,b,2c,d), and z=a+b*sqrt(2)/2+c*sqrt(3)+d*sqrt(6)/2.
SEEDS = ((4,0,0,0,1), (8,-2,0,0,4), (8,-1,0,-1,1), (12,-3,-2,1,9),
         (12,0,-2,0,36), (12,0,0,-2,9), (12,2,-2,-2,4), (24,-6,4,-4,36))
BASE=(6,6,8)

def orbit(z,axis,modulus):
    line=[]
    while not line or z!=line[0]:
        line.append(z)
        a,b,c,d=z
        if axis==0:z=(3*a+2*b,3*b+4*a,3*c+2*d,3*d+4*c)
        if axis==1:z=(2*a+3*c,2*b+3*d,2*c+a,2*d+b)
        if axis==2:z=(5*a+6*d,5*b+12*c,5*c+2*b,5*d+4*a)
        z=tuple(v%modulus for v in z)
    return line

def q_equation(z,norm):
    a,b,c,d=z
    L=a*b-3*c*d
    R=2*a*a+b*b-6*c*c-3*d*d
    return (8*a**3+12*a*b*b)*R-(48*a*a*b+8*b**3)*L-32*norm*a

def multiply(s,t,p):
    a,b,c,d=s; A,B,C,D=t
    return ((a*A+2*b*B+3*c*C+6*d*D)%p,(a*B+b*A+3*c*D+3*d*C)%p,
            (a*C+c*A+2*b*D+2*d*B)%p,(a*D+d*A+b*C+c*B)%p)

def has_x(z,p):
    a,b,c,d=z
    q=(a,b*pow(2,-1,p)%p,c,d*pow(2,-1,p)%p)
    a,b,c,d=q
    for A,B in product(range(p),repeat=2):
        if (a*A+2*b*B-2*a)%p:continue
        for C,D in product(range(p),repeat=2):
            if (3*c*C+6*d*D+a)%p:continue
            x=(A,B,C,D); jx=(A,B,-C,-D)
            qjx=multiply(q,jx,p)
            if multiply(qjx,x,p)[0]==a and multiply(qjx,jx,p)[0]==11*a%p:return True
    return False

def survivors(seed):
    A,b,v,d,N=seed
    possible=set(product(*(range(i) for i in BASE)))
    counts=[]
    for m in (64,5,7,11):
        z=tuple(x%m for x in (A//4,b,v//2,d))
        period=[len(orbit(z,i,m)) for i in range(3)]
        reduced=[gcd(i,j) for i,j in zip(BASE,period)]
        mask=set(); xcache={}
        for i,z1 in enumerate(orbit(z,0,m)):
            for j,z2 in enumerate(orbit(z1,1,m)):
                for k,t in enumerate(orbit(z2,2,m)):
                    if q_equation(t,N)%m:continue
                    if m==11:
                        if t not in xcache:xcache[t]=has_x(t,m)
                        if not xcache[t]:continue
                    mask.add(tuple(v%d for v,d in zip((i,j,k),reduced)))
        possible={r for r in possible if tuple(v%d for v,d in zip(r,reduced)) in mask}
        counts.append(len(possible))
    return counts

if __name__=='__main__':
    for seed in SEEDS:
        counts=survivors(seed)
        print(seed[:4], *counts)
        assert counts[-1]==0
