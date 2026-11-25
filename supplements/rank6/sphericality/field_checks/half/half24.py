"""Exact half-mass dimension denominator bound in conductor 24."""
from pathlib import Path
import sys
from math import gcd,lcm
from itertools import permutations,product
from collections import defaultdict
for parent in Path(__file__).resolve().parents:
    if (parent/'quartic24_fast.py').is_file():
        sys.path.insert(0,str(parent)); break
from quartic24_fast import seeds,exponent_bound,orbit_line,coefficients,DISCS,CROSS

def orbit_inventory(seedlist,cap):
    bs=[exponent_bound(cap,t) for t in (6,4,10)]
    for initial in seedlist:
        for x in orbit_line(initial,0,bs[0]):
            for y in orbit_line(x,1,bs[1]):
                for z in orbit_line(y,2,bs[2]):
                    if z[0]<=cap:yield z

def ratio_rows(seedlist,cap):
    for z in orbit_inventory(seedlist,cap):
        a,u,v,w=z
        if u<0 or v<0 or ((not u or not v) and w<0):continue
        if sum(k!=0 for k in (u,v,w))<2:continue
        _,b,c,n=coefficients(z)
        for h in range(1,cap//a+1):
            A,B,C,N=h*a,h*h*b,h**3*c,h**4*n
            if min(B-3*A+6,C-2*B+3*A-4,N-C+B-A+1)>0:break
            if A%2 or B%2 or C%2 or N%2==0:continue
            yield A,h*u,h*v,h*w

def denominator(z):
    c=z[1:];g=[gcd(c[i],CROSS[i]*c[(i+1)%3]*c[(i+2)%3]) for i in range(3)]
    return 4*lcm(*(d*k for d,k in zip(DISCS,g)))

def run(cap):
    seedlist=seeds();data=sorted(set(ratio_rows(seedlist,cap)))
    denoms={x:denominator(x) for x in data};print('ratios',len(data),'max denominator',max(denoms.values()),flush=True)
    from sympy import divisors
    ds={M:[int(t) for t in divisors(M) if t%4==0] for M in set(denoms.values())}
    possible={t for v in ds.values() for t in v};print('distinct trace divisors',len(possible),flush=True)
    pool=defaultdict(list)
    for z in orbit_inventory(seedlist,max(denoms.values())):
        if z[0] in possible:pool[z[0]].append(z)
    ntest=nsum=nshift=0; survivors=[]
    for x,M in denoms.items():
        A,u,v,w=x
        for t in ds[M]:
            for z in pool.get(t,[]):
                ntest+=1
                zz=(8*z[1]*u,12*z[2]*v,24*z[3]*w)
                if sum(zz)!=(4-A)*t:continue
                nsum+=1
                if any((t*A+i*zz[0]+j*zz[1]+i*j*zz[2])%(8*t)!=4*t for i,j in ((-1,1),(1,-1),(-1,-1))):continue
                nshift+=1
                survivors.append((x,z))
    print('tests/sum/shift',ntest,nsum,nshift,flush=True)
    return survivors
