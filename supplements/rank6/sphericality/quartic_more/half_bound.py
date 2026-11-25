"""Rational interval bounds for quartic dimension ratios at equal half mass.

With trace_threshold set, a box may close either by trace or by the
positive shifted moment. The default check uses the shifted moment alone."""
from math import gcd,isqrt
from sys import argv
Q=1<<20
G=1<<15
CONDUCTORS=[(8,28,56),(8,44,88),(8,13,104),(8,17,136),(12,5,60),
            (12,28,21),(12,40,120),(12,44,33),(12,13,156),(8,48)]
def ceilpos(a,b):return -(-a//b)

def bound(cs,denominator,correction=0, *, trace_threshold=None):
    eps=ceilpos(Q,denominator)
    cyclic=len(cs)==2
    if cyclic:
        add=lambda i,j:(i+j)%4
        k=isqrt(3*G**2//4)
        cos=[G,k,G//2,0,-G//2,-k-1,-G,-k-1,-G//2,0,G//2,k]
        freq=[(cs[0],[[s*G*(-1)**i for i in range(4)] for s in (-1,1)]),
              (cs[1],[[cos[(3*i-j)%12] for i in range(4)] for j in range(12)])]
    else:
        add=lambda i,j:i^j
        freq=[(c,[[s*G*x for x in row] for s in (-1,1)]) for c,row in
              zip(cs,((1,-1,1,-1),(1,1,-1,-1),(1,-1,-1,1)))]
    freq=[(c,isqrt(c*Q**2),isqrt(4*gcd(c,2)*Q**2//c)+1,
            isqrt(4*gcd(c,4)*Q**2//c)+1,rows) for c,rows in freq]
    def lower(x,row):return sum(e*x[i][e<0] for i,e in enumerate(row))
    def cut(x,row,rhs):
        gap=rhs-lower(x,row)
        if gap<0:return False
        for i,e in enumerate(row):
            lo,hi=x[i]
            if e>0:x[i][1]=min(hi,lo+ceilpos(gap,e))
            if e<0:x[i][0]=max(lo,hi-ceilpos(gap,-e))
        return True
    def shrink(p,q):
        for z in range(3):
            for x in (p,q):
                if not cut(x,[1]*4,Q) or not cut(x,[-1]*4,-Q):return False
            for c,root,up,uq,rr in freq:
                lp=max([0]+[lower(p,r)//G for r in rr]);lq=max([0]+[lower(q,r)//G for r in rr])
                if lp>up or lq>uq or c*lp**2+2*root*lq>8*Q**2:return False
                a=min(up,1+isqrt((8*Q**2-2*root*lq)//c))
                b=min(uq,ceilpos(8*Q**2-c*lp**2,2*root))
                for r in rr:
                    if not cut(p,r,G*a) or not cut(q,r,G*b):return False
        return True
    def objective(p,q):
        P=[u for l,u in p]; L=[l for l,u in q]
        h=[(Q*Q,0,Q*Q),(-Q*Q,Q*Q,0),(-Q*Q,0,0),(0,-Q*Q,0)]
        for i in (1,3):
            # correction is twice the excess ordinary complementary norm.
            err=P[0]*(correction*Q+sum(ceilpos(P[add(l,i)]**2,p[l][0]) for l in (1,2,3)))
            h.extend([(L[i]*Q,0,P[i]*Q),(0,L[add(i,2)]*Q,P[i]*Q),
                      (L[i]**2,L[add(i,2)]**2,P[i]**2+err)])
        ub=2*P[2]
        for n,(a,b,c) in enumerate(h):
            for x,y,z in h[n+1:]:
                det=a*y-b*x
                if not det:continue
                s=P[2]*(y-x);t=P[2]*(a-b)
                if det<0:det,s,t=-det,-s,-t
                if s>=0 and t>=0:ub=min(ub,ceilpos(s*c+t*z,det))
        return ub+ceilpos(P[1]*P[3],L[1])+ceilpos(P[1]*P[3],L[3])
    count=[0,0,0]
    def visit(x):
        count[0]+=1
        p,q=x[:4],x[4:]
        if not shrink(p,q):return True
        if trace_threshold is not None:
            # The distinguished ratio is at most 1. With positive lower
            # endpoints, test the other three ratios by cross multiplication.
            l1, l2, l3 = (q[i][0] for i in (1, 2, 3))
            if min(l1, l2, l3) > 0:
                upper_num = p[1][1]*l2*l3 + p[2][1]*l1*l3 + p[3][1]*l1*l2
                if upper_num < (trace_threshold-1)*l1*l2*l3:
                    return True
        if all(p[l][0]>0 for l in (1,2,3)) and min(q[l][0] for l in (1,3))>0:
            k=objective(p,q)
            if k<Q:
                count[1]+=1;count[2]=max(count[2],k);return True
        j=max((1,2,3,5,7),key=lambda i:(x[i][1]-x[i][0])*(13 if i>=4 else 10))
        lo,hi=x[j]
        if hi-lo<=1:return False
        v=(lo+hi)//2;y=[r[:] for r in x];x[j][1]=v;y[j][0]=v
        return visit(x) and visit(y)
    x=[[0,Q] for i in range(8)]
    for i in (0,4,6):x[i][1]=eps
    result=visit(x)
    print(cs,denominator,correction,result,*count,flush=True)
    return result

if __name__=='__main__':
    d=int(argv[1]) if len(argv)>1 else 64
    for i,cs in enumerate(CONDUCTORS):
        if len(argv)>2 and i not in list(map(int,argv[2].split(','))):continue
        bound(cs,d,int(argv[3]) if len(argv)>3 else 0)
