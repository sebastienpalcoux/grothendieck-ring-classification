"""Exact cyclic field of conductor 16 lower bounds for normalized nonidentity coordinates."""
from math import gcd,isqrt
from itertools import product
Q=1<<20
G=65
CIRC=sorted({(a*x,b*y,-a*x,-b*y) for a,b in product((-1,1),repeat=2) for x,y in ((0,65),(16,63),(25,60),(33,56),(39,52),(52,39),(56,33),(60,25),(63,16),(65,0))})
FREQ=((8,[(a,-a,a,-a) for a in (-G,G)]),(16,CIRC))
def ceil(a,b):return -(-a//b)
def inf(x,row):return sum(a*x[i][a<0] for i,a in enumerate(row))
def cut(x,row,rhs):
    slack=rhs-inf(x,row)
    if slack<0:return False
    for i,a in enumerate(row):
        if a>0:x[i][1]=min(x[i][1],x[i][0]+ceil(slack,a))
        if a<0:x[i][0]=max(x[i][0],x[i][1]-ceil(slack,-a))
    return True

def contract(p,q):
    for _ in range(3):
        for x in (p,q):
            if not cut(x,(1,1,1,1),Q) or not cut(x,(-1,-1,-1,-1),-Q):return False
        for c,dirs in FREQ:
            pl=max(0,max(inf(p,d) for d in dirs)//G);ql=max(0,max(inf(q,d) for d in dirs)//G);rc=isqrt(c*Q**2)
            if 25*c*pl**2+40*rc*ql>128*Q**2:return False
            pu=1+isqrt(min(64*gcd(c,2)*Q**2,128*Q**2-40*rc*ql)//(25*c))
            qu=min(1+isqrt(64*gcd(c,4)*Q**2//(25*c)),ceil(128*Q**2-25*c*pl**2,40*rc))
            for d in dirs:
                if not cut(p,d,G*pu) or not cut(q,d,G*qu):return False
    return True

def check(j,den):
    cnt=[0,0,0];z=[i for i in (1,2,3) if i!=j]
    def visit(x):
        cnt[0]+=1;p,q=x[:4],x[4:]
        if not contract(p,q):return
        P=[h for l,h in p];L=[l for l,h in q]
        a=min([Q]+[ceil(Q*P[i],L[i]) for i in z]);b=min([a]+[ceil(Q*P[(i-j)%4],L[i]) for i in z])
        ub=ceil(a*P[-j]+b*P[j],Q)+sum(ceil(P[i]*P[(i-j)%4],L[i]) for i in z)
        if ub<Q:cnt[1]+=1;cnt[2]=max(cnt[2],ub);return
        i=max([1,2,3]+[4+i for i in z],key=lambda i:x[i][1]-x[i][0]);l,h=x[i]
        assert h-l>1,(x,ub)
        m=(l+h)//2;y=[a[:] for a in x];x[i][1]=m;y[i][0]=m
        visit(x);visit(y)
    x=[[0,Q] for _ in range(8)]
    for i in (0,4,4+j):x[i][1]=ceil(Q,den)
    for i in z:x[4+i][0]=Q//20
    visit(x)
    print('cyclic shift',j,'denominator',den,'boxes',cnt,flush=True)
if __name__=='__main__':
    import sys
    for j in (1,2):check(j,int(sys.argv[1]) if len(sys.argv)>1 else 100)
