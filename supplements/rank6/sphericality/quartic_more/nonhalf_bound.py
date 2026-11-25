"""Integer half-mass bound for the nine biquadratic fields and cyclic conductor 48."""
from math import gcd,isqrt
from fractions import Fraction as F
from sys import argv
Q=1<<20
G=1<<15
CONDUCTORS=[(8,28,56),(8,44,88),(8,13,104),(8,17,136),(12,5,60),
            (12,28,21),(12,40,120),(12,44,33),(12,13,156),(8,48)]
def ceilpos(a,b):return -(-a//b)

def bound(cs,denominator,slo,shi,tlo,thi,cutoff,correction=0,restrict_shift=True,shift_min=None,chi_bounds=None):
    if shift_min is None:shift_min=slo
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
                if chi_bounds and c in chi_bounds:
                    a=min(a,ceilpos(chi_bounds[c][0].numerator*Q,chi_bounds[c][0].denominator))
                    b=min(b,ceilpos(chi_bounds[c][1].numerator*Q,chi_bounds[c][1].denominator))
                for r in rr:
                    if not cut(p,r,G*a) or not cut(q,r,G*b):return False
        return True
    def objective(p,q):
        P=[u for l,u in p]; L=[l for l,u in q]
        h=[(Q*Q,0,Q*Q),(-Q*Q,Q*Q,0),(-Q*Q,0,0),(0,-Q*Q,0)]
        for i in (1,3):
            # correction is twice the excess ordinary complementary norm.
            h.extend([(L[i]*Q,0,P[i]*Q),(0,L[add(i,2)]*Q,P[i]*Q)])
            if correction is not None:
                err=P[0]*(ceilpos(correction.numerator*Q,correction.denominator)+sum(ceilpos(P[add(l,i)]**2,p[l][0]) for l in (1,2,3)))
                h.append((L[i]**2,L[add(i,2)]**2,P[i]**2+err))
        if restrict_shift:
            # h = (q0/qj) pj + (p0/q0) qj + qm pk/qk + qk pm/qm lies in s+Z.
            hbase=sum(q[i][0]*p[i^2][0]//q[i^2][1] for i in (1,3))
            H=sum(ceilpos(q[i][1]*p[i^2][1],q[i^2][0]) for i in (1,3))+P[2]+q[2][1]
            if not any((shift_min+k)*Q>=hbase and (shift_min+k)*Q<=H for k in range(0,1+H//Q)):
                return 0
            # Feasible t=q0/qj=b/a must put the shifted trace above s+k.
            # For the smallest admissible shift, this bounds b/a from below.
            kk=min(k for k in range(0,1+H//Q) if (shift_min+k)*Q>=hbase and (shift_min+k)*Q<=H)
            maximum_base=sum(ceilpos(q[i][1]*p[i^2][1],q[i^2][0]) for i in (1,3))
            tmin=max(0,((shift_min+kk)*Q).__floor__()-q[2][1]-maximum_base)
            if tmin>P[2]:return 0
            h.append((tmin*Q,-P[2]*Q,0))
            # Largest admissible shift bounds b/a above.
            kk=max(k for k in range(0,1+H//Q) if (shift_min+k)*Q>=hbase and (shift_min+k)*Q<=H)
            tmax=((shift_min+kk)*Q).__ceil__()-hbase
            if p[2][0]>0:h.append((-tmax*Q,p[2][0]*Q,0))
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
        if (correction is None or all(p[l][0]>0 for l in (1,2,3))) and min(q[l][0] for l in (1,3))>0:
            k=objective(p,q)
            if k<cutoff*Q:
                count[1]+=1;count[2]=max(count[2],k);return True
        j=max((1,2,3,5,7),key=lambda i:(x[i][1]-x[i][0])*(13 if i>=4 else 10))
        lo,hi=x[j]
        if hi-lo<=1:return False
        v=(lo+hi)//2;y=[r[:] for r in x];x[j][1]=v;y[j][0]=v
        return visit(x) and visit(y)
    x=[[0,Q] for i in range(8)]
    for i in (0,4,6):x[i][1]=eps
    result=visit(x)
    print(cs,denominator,slo,shi,tlo,thi,cutoff,correction,result,*count,flush=True)
    return result

if __name__=='__main__':
    d=int(argv[1]);cases=[(8,28,56),(8,44,88),(8,48),(8,13,104),(8,17,136),
        (8,60,120),(8,76,152),(8,21,168),(8,92,184),(8,29,232),
        (8,33,264),(8,37,296),(8,41,328),(8,80),(8,112)]
    ss=F(1,2);tt=F(5,8)
    for i in map(int,argv[2].split(',')):
        for typ in argv[3].split(','):
            if typ=='a':bound(cases[i],d,ss,ss,tt,tt,F(1,4),F(1,8))
            if typ=='b':bound(cases[i],d,ss,ss,tt,F(11,16),F(1,2),F(1,4))
            if typ=='c':bound(cases[i],d,tt,tt,tt,tt,F(5,8),F(0))
