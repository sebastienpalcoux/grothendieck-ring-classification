"""Exact height check for equal nonhalf masses s=t>=5/8 in the quartic K24 field."""
from math import gcd, isqrt
import sys
Q=1<<20
D=int(sys.argv[1]) if len(sys.argv)>1 else 50
EPS=(Q+D-1)//D
nodes=leaves=greatest=0
FREQ=((8,(1,1,-1,-1)),(12,(1,-1,1,-1)),(24,(1,-1,-1,1)))
def ceil(a,b): return (a+b-1)//b
def inf(x,row):return sum(a*x[i][a<0] for i,a in enumerate(row))
def cut(x,row,rhs):
    slack=rhs-inf(x,row)
    if slack<0:return False
    for i,a in enumerate(row):
        if a>0:x[i][1]=min(x[i][1],x[i][0]+slack)
        if a<0:x[i][0]=max(x[i][0],x[i][1]-slack)
    return True
def contract(p,q):
    for _ in range(3):
        for x in (p,q):
            if not cut(x,(1,1,1,1),Q) or not cut(x,(-1,-1,-1,-1),-Q):return False
        for c,row in FREQ:
            inv=tuple(-a for a in row)
            pl=max(0,inf(p,row),inf(p,inv));ql=max(0,inf(q,row),inf(q,inv))
            rc=isqrt(c*Q*Q)
            if 25*c*pl*pl+40*rc*ql>128*Q*Q:return False
            pu=isqrt(min(64*gcd(c,2)*Q*Q,128*Q*Q-40*rc*ql)//(25*c))+1
            qu=min(isqrt(64*gcd(c,4)*Q*Q//(25*c))+1,ceil(128*Q*Q-25*c*pl*pl,40*rc))
            for r in (row,inv):
                if not cut(p,r,pu) or not cut(q,r,qu):return False
    return True
def run(x):
    global nodes,leaves,greatest
    nodes+=1;p,q=x[:4],x[4:]
    if not contract(p,q):return
    P=[r[1] for r in p];L=[r[0] for r in q]
    a=min(Q,ceil(Q*P[2],L[2]),ceil(Q*P[3],L[3]))
    b=min(a,ceil(Q*P[2],L[3]),ceil(Q*P[3],L[2]))
    ub=ceil((a+b)*P[1],Q)+ceil(P[2]*P[3],L[2])+ceil(P[2]*P[3],L[3])
    if ub<Q:
        leaves+=1;greatest=max(greatest,ub);return
    i=max((1,2,3,6,7),key=lambda i:x[i][1]-x[i][0])
    lo,hi=x[i]
    if hi-lo<2:raise ValueError(x,ub)
    m=(lo+hi)//2
    y=[r[:] for r in x];x[i][1]=m;y[i][0]=m
    run(x);run(y)
start=[[0,Q] for _ in range(8)]
for i in (0,4,5):start[i]=[0,EPS]
for i in (6,7):start[i][0]=Q//100
run(start)
print('denominator',D,'nodes',nodes,'moment leaves',leaves,'largest upper',greatest,'/',Q)
