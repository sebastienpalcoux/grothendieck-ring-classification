"""Exact rank-five vacuum-moment bounds; all certificate coefficients are integers."""

if not __debug__:
    raise RuntimeError("Run this verifier with Python assertions enabled")

from functools import lru_cache
from fractions import Fraction as Q
from math import gcd, lcm, isqrt

SCALE=10**10
KERNEL={15:(1,14),16:(1,15),20:(1,19),35:(1,11,16,19,24,34),40:(1,11,29,39)}

@lru_cache(None)
def cosine(n,t):
    """Rational midpoint for cos(2*pi*t/n), with error less than 2/SCALE."""
    t=min(t%n,(-t)%n)
    pi=Q(3141592653589793,10**15)
    x=2*pi*t/n
    term=value=Q(1)
    for k in range(1,14):
        term*=-x*x/Q((2*k-1)*(2*k))
        value+=term
    return Q(value.numerator*SCALE//value.denominator,SCALE)

def kronecker(d,u):
    """(d/u) on positive odd and even units, by quadratic reciprocity."""
    if u==0:
        return int(d==1)
    sign=1
    while u%2==0:
        u//=2
        if d%8 in (3,5):sign=-sign
    a=d%u
    while a:
        while a%2==0:
            a//=2
            if u%8 in (3,5):sign=-sign
        if a%4==u%4==3:sign=-sign
        a,u=u%a,a
    return sign if u==1 else 0

def groups(F):
    c=lcm(*F) if len(F)>1 else F[0]
    units=[u for u in range(1,c) if gcd(u,c)==1]
    if len(F)>1:
        classes=[[u for u in units if kronecker(F[0],u)+3*kronecker(F[1],u)==t] for t in (4,2,-2,-4)]
    else:
        ker=KERNEL[c]
        gen=next(u for u in units if u*u%c not in ker)
        classes=[[pow(gen,t,c)*v%c for v in ker] for t in range(4)]
    return c,classes

@lru_cache(None)
def ram(n):
    res=1
    d=2
    while d*d<=n:
        if n%d==0:
            n//=d
            if n%d==0:return Q(0)
            res*=1-d
        d+=1
    return Q(1,res*(1-n if n>1 else 1))

def invsqrt(n):
    """A rational upper bound for the reciprocal square root."""
    return Q(isqrt(SCALE*SCALE//n)+1,SCALE)

def dot(a,b):
    assert len(a)==len(b)
    return sum(x*y for x,y in zip(a,b))

def validate(data):
    F=tuple(map(int,data['F'].split('-')))
    f,J=data['f'],data['J']
    a=[Q(x,10**8) for x in data['ea']]
    b=[Q(x,10**8) for x in data['eb']]
    t=[Q(x,10000) for x in data['t']]
    assert all(x>=0 for x in b)
    # Small deliberate cushion for rounding the numerical dual certificate.
    a[0]+=Q(1,10**5)
    assert a[0]>0
    c,classes=groups(F)
    dchars=F if len(F)>1 else ((8 if c==16 else 5),)
    assert all(all(j%d for d in dchars) for j in J)
    assert f==4 or (f==5 and all(j%5 for j in J))
    jmax=lcm(*J)
    nmax=jmax*lcm(c,*(prime for prime in (2,3,5) if jmax%prime==0))
    assert max(J)<=6
    extrema=[Q(1),-Q(1,next(p for p in (3,5,7,11,13,17,19,23,29,31) if nmax%p)-1)]

    @lru_cache(None)
    def local_orbits(n,t0):
        while t0>=n: t0%=n
        m=n
        while (g:=gcd(m,c))>1:m//=g
        q=n//m
        if c%q or not ram(m):return (0,)*4
        u=t0*pow(m,-1,q)%q if q>1 else 0
        return tuple(ram(m)*sum(cosine(q,u*v%q) for v in orbit)/len(orbit) for orbit in classes)

    # Group columns by their actual vector of cosine averages.
    seen=set()
    for n in range(1,nmax+1):
        if nmax%n:continue
        for num in range(1,n+1):
            if gcd(n,num)!=1:continue
            hlist=[]
            for j in (1,2):
                g=gcd(n,j)
                hlist.append(local_orbits(n//g,num*(j//g)%(n//g)))
            aa=hlist[0]
            zsum=tuple(4*ram(n//gcd(n,j)) for j in J)
            key=(aa,hlist[1][0],zsum,n==1,n==2)
            if key in seen:continue
            seen.add(key)
            if len(F)>1:
                h=[dot(signs,aa) for signs in ((1,-1,1,-1),(1,1,-1,-1),(1,-1,-1,1))]
                fourier=h+[-v for v in h]
            else:
                h=dot((1,-1,1,-1),aa)
                fourier=[h,-h]+[cosine(8,k)*(aa[0]-aa[2])+cosine(8,k-2)*(aa[1]-aa[3]) for k in range(8)]
            for mult in extrema:
                plus=int(n==1 and mult==1)
                minus=int(n==2 and mult==1)
                eq=[1]+[mult*v for v in zsum]
                ub=[mult*v for v in (aa[0],hlist[1][0],-hlist[1][0],*fourier)]
                if f==4:ub.append(-minus)
                err=dot(a,eq)+dot(b,ub)+2*mult*dot(t,aa)-plus
                # Each approximated coordinate has error at most 32/SCALE.
                allowance=Q(32,SCALE)*(sum(map(abs,b))+2*sum(map(abs,t))+1)
                assert err>allowance,(F,n,num,err,allowance)
    threshold=certificate_bound(data)
    print(f"Codegree {f}, field {F}: D < {threshold}.")
    return threshold


def certificate_bound(data):
    """Smallest positive integral upper endpoint certified by this fixed majorant."""
    F=tuple(map(int,data['F'].split('-')))
    f,J=data['f'],data['J']
    a=[Q(x,10**8) for x in data['ea']]
    a[0]+=Q(1,10**5)
    b=[Q(x,10**8) for x in data['eb']]
    t=[Q(x,10000) for x in data['t']]
    sf=1-Q(1,f)
    e=[1]+[(sf if f==5 or j%2 else 1) for j in J]
    if len(F)>1: fourier=2*[invsqrt(d) for d in F]
    else: fourier=[invsqrt(8 if F[0]==16 else 5)]*2+[invsqrt(F[0])]*8
    if f==4: fourier.append(-Q(1,32))
    extra=Q(1,64) if f==4 else 0
    lower=Q(1,f*f)+extra-dot(t,t)
    margin=lower-dot(a,e)-dot(b[3:],fourier)
    A=sum(b[:3]); B=2*sum(b[1:3])
    assert margin>0 and A>=0 and B>=0
    def separates(h):
        remainder=margin*h-A
        return remainder>0 and remainder**2>B*B*h
    hi=1
    while not separates(hi): hi*=2
    lo=0
    while hi-lo>1:
        mid=(hi+lo)//2
        if separates(mid): hi=mid
        else: lo=mid
    return hi

DATA=[{'F': '16',
  'f': 4,
  'J': [1, 2, 3, 4, 5, 6],
  't': [0, 2696, 2291, 2513],
  'ea': [14285715, -43471738, -1187115, 1190476, 2678571, 1428571, 3571429],
  'eb': [63410764, 15462746, 0, 0, 0, 0, 0, 0, 0, 7984, 0, 0, 0, 0]},
 {'F': '20',
  'f': 4,
  'J': [1, 2, 3, 4, 6],
  't': [0, 2835, 2236, 2429],
  'ea': [20000000, -47382521, -4330382, 1649610, 1257834, 4989555],
  'eb': [82911809, 22351809, 0, 0, 0, 0, 0, 0, 0, 1898443, 0, 0, 0, 39670]},
 {'F': '35',
  'f': 4,
  'J': [1, 2, 3, 4, 6],
  't': [0, 3130, 1690, 2680],
  'ea': [20000000, -51190170, -2673503, 0, 1250000, 3333333],
  'eb': [104760680, 22360680, 0, 0, 0, 0, 0, 0, 435, 17352131, 0, 0, 0, 0]},
 {'F': '40',
  'f': 4,
  'J': [1, 2, 3, 4, 6],
  't': [0, 3216, 1581, 2703],
  'ea': [20000000, -53113503, -5590170, 833333, 5000000, 2500000],
  'eb': [109120680, 22360680, 0, 0, 0, 0, 0, 0, 10510, 16980400, 0, 0, 0, 0]},
 {'F': '5-8-40',
  'f': 4,
  'J': [1, 2, 3, 4, 6],
  't': [0, 2511, 2030, 2959],
  'ea': [27207592, -47790170, -7903935, 0, -551898, 4534598],
  'eb': [91160680, 38477346, 0, 0, 0, 0, 0, 332, 2672578, 0]},
 {'F': '5-12-60',
  'f': 4,
  'J': [1, 2, 3, 4, 6],
  't': [0, 2518, 1878, 3105],
  'ea': [20000000, -53486837, 1493163, 4166667, 1250000, -833333],
  'eb': [97260680, 22360680, 0, 0, 0, 0, 0, 1886540, 10759700, 0]},
 {'F': '5-13-65',
  'f': 4,
  'J': [1, 2, 3, 4, 6],
  't': [0, 2363, 1669, 3468],
  'ea': [20000000, -51400170, -2673503, 0, 1250000, 3333333],
  'eb': [105600680, 22360680, 0, 0, 0, 0, 0, 92583, 4965, 0]},
 {'F': '5-17-85',
  'f': 4,
  'J': [1, 2, 3, 4, 6],
  't': [0, 2537, 1543, 3420],
  'ea': [20000000, -52660170, -2673503, 0, 1250000, 3333333],
  'eb': [110640680, 22360680, 0, 0, 0, 0, 0, 6568202, 3336, 0]},
 {'F': '5-21-105',
  'f': 4,
  'J': [1, 2, 3, 4, 6],
  't': [0, 2659, 1579, 3262],
  'ea': [20000000, -59800170, -5590170, 7500000, 5000000, 2500000],
  'eb': [109200680, 22360680, 0, 0, 0, 0, 0, 6705088, 5444139, 0]},
 {'F': '8-12-24',
  'f': 4,
  'J': [1, 2, 3, 4, 5, 6],
  't': [0, 2580, 2191, 2729],
  'ea': [14285715, -47450152, 1957347, 4166667, 2678571, 1428571, 595238],
  'eb': [67419654, 14789660, 0, 0, 0, 0, 2223, 0, 3125670, 0]}]

if __name__=="__main__":
    for row in DATA:validate(row)
