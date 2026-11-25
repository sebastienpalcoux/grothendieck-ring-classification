"""Exact unit-lattice enumeration for the quartic field of conductor 16."""
from math import gcd,lcm
from pathlib import Path
from collections import defaultdict
from tempfile import TemporaryDirectory
import sys, subprocess
from sympy import divisors
HERE=Path(__file__).resolve().parent

def mul(z,t):
    a,b,c,d=z;e,f,g,h=t
    return (a*e+2*(b*f+c*g+d*h),a*f+b*e+c*g-d*h+c*h+d*g,
            a*g+c*e+b*(g+h)+f*(c+d),a*h+d*e+b*(g-h)+f*(c-d))

def g(z):a,b,c,d=z;return(a,-b,-d,c)
def conj(z):
    yield z
    for i in range(3):z=g(z);yield z

def norm(z):
    a,b,c,d=z;I=a*a+2*b*b-2*(c*c+d*d);J=2*a*b-c*c+d*d-2*c*d
    return I*I-2*J*J

def coeff(z):
    a,b,c,d=z;h=c*c+d*d;k=c*c-d*d+2*c*d
    return 4*a,6*a*a-4*b*b-4*h,4*a**3-8*a*b*b-8*a*h+8*b*k,norm(z)

units=((3,2,0,0),(3,1,2,0),(3,-1,0,2));invs=((3,-2,0,0),(5,-3,-2,4),(5,3,-4,-2))
def line(z,j,bound):
    yield z
    for u in (units[j],invs[j]):
        v=z
        for k in range(bound):v=mul(v,u);yield v

def orbit(z,C):
    # The orbit seed has trace at most 320. The bit length is an upper bound for log(C).
    h=C.bit_length()+9
    for v in line(z,1,h):
        for w in line(v,2,h):
            for r in line(w,0,2*h):
                if 4*r[0]<=C:yield r

def seeds():
    with TemporaryDirectory() as td:
        p=Path(td)/'check';subprocess.run(['c++','-O3','-std=c++17',str(HERE/'seeds16.cpp'),'-o',str(p)],check=True)
        data=set(tuple(map(int,l.split())) for l in subprocess.check_output([str(p)],text=True).splitlines())
    out=[]
    while data:
        z=min(data,key=lambda t:(norm(t),t));out.append(z);data.difference_update(orbit(z,320))
    assert [norm(v) for v in out]==[1,2,4,8]
    return out

def ratio_rows(zlist,cap):
    for z in zlist:
        if norm(z)!=1:continue
        for row in orbit(z,cap):
            if row!=min(conj(row)) or not any(row[2:]):continue
            a,b,c,n=coeff(row)
            for k in range(1,cap//a+1,2):
                A,B,C,N=k*a,k*k*b,k**3*c,k**4*n
                if min(B-3*A+6,C-2*B+3*A-4,N-C+B-A+1)>0:break
                if A%2 or B%2 or C%2 or not N%2:continue
                yield tuple(k*v for v in row)

def denom(x):
    a,b,c,d=x
    h=4*gcd(b,c*c-d*d+2*c*d,c*c-d*d-2*c*d)
    return lcm(4,8*h,16*(c*c+d*d))

def run(cap):
    ss=seeds();data=list(ratio_rows(ss,cap));den={r:denom(r) for r in data};print('seeds',ss,'ratios',len(den),'max denominator',max(den.values()),flush=True)
    ds={m:[int(t) for t in divisors(m) if t%4==0] for m in set(den.values())};pt={t for s in ds.values() for t in s}
    pool=defaultdict(list)
    for s in ss:
        for z in orbit(s,max(den.values())):
            if 4*z[0] in pt:pool[4*z[0]].append(z)
    ntest=nsum=nshift=0;out=[]
    for x,M in den.items():
        for T in ds[M]:
            for z in pool.get(T,[]):
                ntest+=1;t=z[0]
                if mul(z,x)[0]!=t:continue
                nsum+=1
                if any(mul(z,y)[0]%(2*t)!=t for y in conj(x)):continue
                nshift+=1;out.append((x,z))
    print('tested sum shift',ntest,nsum,nshift,flush=True)
    return out
