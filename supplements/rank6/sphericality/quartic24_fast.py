"""Certified enumeration of primitive totally positive d-numbers in Q(sqrt2,sqrt3)."""
import argparse
from itertools import product
from math import isqrt

DISCS=(8,12,24)
UNIT_TRACES=(6,4,10)
CROSS=(6,4,2)
NORMS={1,2,4,8,9,18,36,72}

def coefficients(z):
    a,u,v,w=z
    x,y,z2=8*u*u,12*v*v,24*w*w
    s=x+y+z2;t=48*u*v*w
    b8=3*a*a-s
    c16=a**3-a*s+2*t
    n256=a**4-2*s*a*a+8*a*t+s*s-4*(x*y+x*z2+y*z2)
    assert b8%8==0 and c16%16==0 and n256%256==0
    return a,b8//8,c16//16,n256//256

def seeds():
    out=[]
    for a in range(4,173,4):
        for u in range(-isqrt((a*a-1)//8),isqrt((a*a-1)//8)+1):
            for v in range(-2*isqrt((a*a-1)//48),2*isqrt((a*a-1)//48)+1,2):
                bound=isqrt((a*a-1)//24)
                for w in range(-bound+(u+bound)%2,bound+1,2):
                    row=(a,u,v,w)
                    _,b,c,n=coefficients(row)
                    if n not in NORMS or b<=0 or c<=0:continue
                    if a**4%n or b**4%(n*n) or c**4%(n**3):continue
                    vs=(u,v,w);s2=[d*k*k for k,d in zip(vs,DISCS)]
                    good=True
                    for i in range(3):
                        j=(i+1)%3;k=(i+2)%3
                        f=a*a+s2[i]-s2[j]-s2[k]
                        excess=f*f-64*UNIT_TRACES[i]**2*n
                        if excess>0 or (excess==0 and a*vs[i]>CROSS[i]*vs[j]*vs[k]):
                            good=False;break
                    if good:out.append(row)
    return out

def shift(row,axis,sign=1):
    a,u,v,w=row
    if axis==0:
        return (3*a+8*sign*u,3*u+sign*a,3*v+4*sign*w,3*w+2*sign*v)
    if axis==1:
        return (2*a+6*sign*v,2*u+3*sign*w,2*v+sign*(a//2),2*w+sign*u)
    return (5*a+24*sign*w,5*u+6*sign*v,5*v+4*sign*u,5*w+sign*a)

def orbit_line(row,axis,bound):
    yield row
    for sign in (-1,1):
        z=row
        for i in range(bound):
            z=shift(z,axis,sign)
            yield z

def exponent_bound(cap,tr):
    # Tr(U^k)=U^k+U^-k. The first term >2*cap bounds log_U(cap)+1/2.
    # Specifically if U^k>cap then log_U(cap)+1/2<k+1.
    a,b,k=2,tr,1
    while b<=2*cap:
        a,b=b,tr*b-a;k+=1
    return k

def inventory(cap):
    base=seeds()
    bounds=[exponent_bound(cap,t) for t in UNIT_TRACES]
    for initial in base:
        for x in orbit_line(initial,0,bounds[0]):
            for y in orbit_line(x,1,bounds[1]):
                for a,u,v,w in orbit_line(y,2,bounds[2]):
                    if a>cap or u<0 or v<0:continue
                    if (not u or not v) and w<0:continue
                    if sum(t!=0 for t in (u,v,w))<2:continue
                    a,b,c,n=coefficients((a,u,v,w))
                    for h in range(1,cap//a+1):
                        A,B,C,N=h*a,h*h*b,h**3*c,h**4*n
                        if A>4 and B-3*A+6>0 and C-2*B+3*A-4>0 and N-C+B-A+1>0:break
                        yield 8,12,24,A,h*u,h*v,h*w,B,C,N

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('cap',type=int)
    parser.add_argument('output',nargs='?')
    args=parser.parse_args()
    out=open(args.output,'w') if args.output else None
    count=0
    try:
        for row in inventory(args.cap):
            if out: print(*row,file=out)
            count+=1
    finally:
        if out:out.close()
    print('trace cap',args.cap,'primitive conjugacy classes',count)
