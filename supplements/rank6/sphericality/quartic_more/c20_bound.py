"""Integer half-mass bound for the nine biquadratic fields and cyclic conductor 48."""
from math import gcd,isqrt
from fractions import Fraction as F
from sys import argv
Q=1<<20
G=1<<15
CONDUCTORS=[(8,28,56),(8,44,88),(8,13,104),(8,17,136),(12,5,60),
            (12,28,21),(12,40,120),(12,44,33),(12,13,156),(8,48)]
def ceilpos(a,b):return -(-a//b)

def bound(denominator,s,t,cutoff,correction=None,saturated=False):
    cs=(5,20);slo=shi=s;tlo=thi=t
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
    freq=[(c,isqrt(c*Q**2),isqrt(gcd(c,2)*Q**2//c)+1,
            isqrt(gcd(c,4)*Q**2//c)+1,rows) for c,rows in freq]
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
            for x,lo,hi in ((p,slo,shi),(q,tlo,thi)):
                if not cut(x,[1]*4,ceilpos(hi.numerator*Q,hi.denominator)) or not cut(x,[-1]*4,-(lo.numerator*Q//lo.denominator)):return False
            for c,root,up,uq,rr in freq:
                lp=max([0]+[lower(p,r)//G for r in rr]);lq=max([0]+[lower(q,r)//G for r in rr])
                if lp>up or lq>uq or c*lp**2+root*lq>2*Q**2:return False
                a=min(up,1+isqrt((2*Q**2-root*lq)//c))
                b=min(uq,ceilpos(2*Q**2-c*lp**2,root))
                if c==5 and saturated:a=b=0
                for r in rr:
                    if not cut(p,r,G*a) or not cut(q,r,G*b):return False
        return True
    def objective(p,q):
        P=[u for l,u in p]; L=[l for l,u in q]
        h=[(Q*Q,0,Q*Q),(-Q*Q,Q*Q,0),(-Q*Q,0,0),(0,-Q*Q,0)]
        for i in (1,2,3):
            h.extend([(L[i]*Q,0,P[i]*Q),(0,L[(i+1)%4]*Q,P[i]*Q)])
            if correction is not None:
                err=P[0]*(ceilpos(correction.numerator*Q,correction.denominator)+sum(ceilpos(P[(l+i)%4]**2,p[l][0]) for l in (1,2,3)))
                h.append((L[i]**2,L[(i+1)%4]**2,P[i]**2+err))
        ub=P[3]+P[1]
        for n,(a,b,c) in enumerate(h):
            for x,y,z in h[n+1:]:
                det=a*y-b*x
                if not det:continue
                s=P[3]*y-P[1]*x;t=P[1]*a-P[3]*b
                if det<0:det,s,t=-det,-s,-t
                if s>=0 and t>=0:ub=min(ub,ceilpos(s*c+t*z,det))
        return ub+ceilpos(P[1]*P[2],L[2])+ceilpos(P[2]*P[3],L[3])
    count=[0,0,0]
    def visit(x):
        count[0]+=1
        p,q=x[:4],x[4:]
        if not shrink(p,q):return True
        if (correction is None or all(p[l][0]>0 for l in (1,2,3))) and min(q[l][0] for l in (2,3))>0:
            k=objective(p,q)
            if k<cutoff*Q:
                count[1]+=1;count[2]=max(count[2],k);return True
        j=max((1,2,3,6,7),key=lambda i:(x[i][1]-x[i][0])*(13 if i>=4 else 10))
        lo,hi=x[j]
        if hi-lo<=1:return False
        v=(lo+hi)//2;y=[r[:] for r in x];x[j][1]=v;y[j][0]=v
        return visit(x) and visit(y)
    x=[[0,Q] for i in range(8)]
    for i in (0,4,5):x[i][1]=eps
    result=visit(x)
    print(cs,denominator,slo,shi,tlo,thi,cutoff,correction,result,*count,flush=True)
    return result

if __name__=='__main__':
    den=int(argv[1])
    rows=[(F(11,20),F(11,20),F(11,20),None,False),(F(8,15),F(3,5),F(2,5),None,False),
          (F(3,5),F(3,5),F(3,5),None,False),(F(2,5),F(3,5),F(3,5),None,False),
          (F(1,2),F(1,2),F(1,2),F(1,2),False),(F(1,2),F(1,2),F(1,2),None,True)]
    for i in map(int,argv[2].split(',')):bound(den,*rows[i])
