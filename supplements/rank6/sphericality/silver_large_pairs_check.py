"""Exact Wronskian and periodic residue check in the large-mass silver profiles."""
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from math import gcd, isqrt, lcm

PAIRS = [(4,8), (4,18), (4,25), (4,32), (4,36), (4,49), (4,50), (7,7)]
TRACE = [[(2,0),(2,1)]]
for _ in range(65):
    TRACE.append([(3*x+4*y,2*x+3*y) for x,y in TRACE[-1]])
# Inward/outward rational bounds on u=3+2√2 and v=2+√2.
SCALE = 10**9
SQ = isqrt(2*SCALE*SCALE)
U = F(3)+2*F(SQ,SCALE), F(3)+2*F(SQ+1,SCALE)
V = F(2)+F(SQ,SCALE), F(2)+F(SQ+1,SCALE)
C = V[0]/2,V[1]/2
ETA = F(999999,10**6)

@lru_cache(None)
def power(interval,exponent):
    bounds = tuple(x**exponent for x in interval)
    return min(bounds),max(bounds)

@lru_cache(None)
def divisors(n):
    small=[];large=[]
    for i in range(1,isqrt(n)+1):
        if n%i==0:
            small.append(i)
            if i*i<n:large.append(n//i)
    return small+large[::-1]

def prime_powers(n):
    p=2
    while p*p<=n:
        if n%p==0:
            m=1
            while n%p==0:n//=p;m*=p
            yield m
        p+=1
    if n>1:yield n

def periodic_pair(M,mod1,mod2,e,ee,f,r,b,h):
    k=max(0,-b)
    def state(j):
        return ((TRACE[j][e][0]+h*TRACE[j+b][ee][0])%M,
                TRACE[j+r][f][0]%M)
    (x,y),(z,w)=state(k),state(k+1)
    base=x,z,y,w; found=[];length=0
    while True:
        if x%gcd(M,mod1)==0 and y%gcd(M,mod2)==0:found.append(k+length)
        x,z,y,w=z,(6*z-x)%M,w,(6*w-y)%M
        length+=1
        if (x,z,y,w)==base:return length,found

def compatible_moduli(P,Q,Q0,mc,e,ee,f,r,b,a,h):
    mod1=P*(mc//gcd(mc,Q))
    mod2=h//gcd(h,Q0*a)
    old_n=1; old={0}
    for modulus in prime_powers(lcm(mod1,mod2)):
        n,res=periodic_pair(modulus,mod1,mod2,e,ee,f,r,b,h)
        if not res:return False
        common=gcd(n,old_n);new_n=lcm(n,old_n);new=set()
        inv=pow(old_n//common,-1,n//common) if n>common else 0
        for s in old:
            for t in res:
                if (t-s)%common==0:
                    new.add((s+old_n*(((t-s)//common)*inv))%new_n)
        old_n,old=new_n,new
        if not old:return False
    return True

def check(g1,g2):
    L=1-F(1,g1)-F(1,g2)
    P,Q=L.as_integer_ratio()
    Q0=lcm(g1,g2)
    lower=F(1,100) if (g1,g2) in ((4,8),(4,18)) else L-F(17,24)
    ratio=F(9,16)/lower
    stats=Counter()
    for e,f in product((0,1),repeat=2):
        ee=e^int(isqrt(g1*g2)**2!=g1*g2)
        if (g1,g2)==(4,18) and e:continue
        # At five both v-family branches have W-residue unequal to 1.
        if (g1,g2)==(4,25) and e==ee==1:continue
        for r in range(6):
            W=abs(TRACE[0][e][0]*TRACE[r+1][f][0]-TRACE[1][e][0]*TRACE[r][f][0])
            if W==0:continue
            for a in range(1,2*isqrt(int(ratio))+3):
                if f>e and a%2:continue
                if a>=power(V,f-e)[1]*power(U,r)[1]:continue
                if a*power(U,r)[0]>4*ratio:continue
                y=a*power(C,f-e)[0]*power(U,r)[0]
                for h in divisors(Q0*a*W):
                    if ee>e and h%2:continue
                    for b in range(-16,7):
                        if 2*r+f<=2*b+ee:continue
                        ul,uh=power(U,b)
                        if h*uh<F(1,2) or h*ul>4/lower:continue
                        xl=h*ul*power(C,ee-e)[0]
                        xh=h*uh*power(C,ee-e)[1]
                        mc=lcm(g1,g2,4//(1+e),a*(4//(1+f)),h*(4//(1+ee)))
                        stats['tuples']+=1
                        tail_gap=ETA**2*L**2*(1+xl**2+2*y*y)/(1+xh)**2
                        tmax=L/(ETA*(1+xl))
                        ymax=a*power(C,f-e)[1]*power(U,r)[1]
                        smax=tmax*ymax
                        if (g1,g2)==(4,8) and tmax<F(1,8) and smax<F(1,4):
                            tail_gap+=(F(1,2)-smax)**2
                        if tmax>=lower and 2*tail_gap<=1:
                            stats['tail gap tests']+=1
                            assert not compatible_moduli(P,Q,Q0,mc,e,ee,f,r,b,a,h)
                        for k in range(32):
                            if (g1,g2)==(4,18) and k%2:continue
                            j=k+b;z=k+r
                            if j<0 or 2*j+ee<2:continue
                            B,d0=TRACE[k][e];A,d1=TRACE[z][f];G,d2=TRACE[j][ee]
                            num=(B+h*G)*Q
                            if num%(P*mc):continue
                            m=num//P
                            if (Q0*a*A)%h:continue
                            if B<lower*m:continue
                            mixed=4*d0*d0+4*h*h*d2*d2+8*a*a*d1*d1
                            if (g1,g2)==(4,8) and 8*B<m and 4*a*A<m:
                                mixed+=F((m-2*a*A)**2,2)
                            assert mixed>m*m
    return stats['tuples'],stats['tail gap tests']

if __name__=='__main__':
    for p in PAIRS:
        print(*p,*check(*p),flush=True)
