"""Integer boxes for the short irrational signed pair at cyclic conductor 16."""
from math import isqrt,gcd
from nonhalf_height import Q,G,FREQ,ceil,inf,cut

def contract(p,q):
    for _ in range(3):
        for x in (p,q):
            if not cut(x,(1,1,1,1),Q) or not cut(x,(-1,-1,-1,-1),-Q):return False
        for c,dirs in FREQ:
            pl=max(0,max(inf(p,d) for d in dirs)//G);ql=max(0,max(inf(q,d) for d in dirs)//G);rc=isqrt(c*Q**2)
            if c*pl**2+2*rc*ql>8*Q**2:return False
            pu=isqrt(min(4*gcd(c,2)*Q**2,8*Q**2-2*rc*ql)//c)+1
            qu=min(isqrt(4*gcd(c,4)*Q**2//c)+1,ceil(8*Q**2-c*pl**2,2*rc))
            if c==8:
                if 2*pl**2+ql**2>Q**2:return False
                pu=min(pu,1+isqrt((Q**2-ql**2)//2));qu=min(qu,1+isqrt(Q**2-2*pl**2),1+isqrt(8*Q**2//9))
            for d in dirs:
                if not cut(p,d,G*pu) or not cut(q,d,G*qu):return False
    return True

def check(den):
    cnt=[0,0,0]
    def visit(x):
        cnt[0]+=1;p,q=x[:4],x[4:]
        if not contract(p,q):return
        P=[h for l,h in p];L=[l for l,h in q]; M=[l for l,h in p]
        constraints=[(1,0,Q),(-1,1,0),(-1,0,0),(0,-1,0)] # Variables Q*a, Q*b.
        for i in (1,2,3):
            constraints.extend([(L[i],0,Q*P[i]),(0,L[(i+1)%4],Q*P[i])]);
            if all(M[k]>0 for k in (1,2,3)):
                err=P[0]*sum(ceil(P[(k+i)%4]**2,M[k]) for k in (1,2,3))
                constraints.append((L[i]**2,L[(i+1)%4]**2,Q*(P[i]**2+err)))
        # h= (q0/q1) p1 + q1 p2/q2 + q2 p3/q3 + q3 (p0/q0) is a positive integer.
        hbase=q[1][0]*M[2]//q[2][1]+q[2][0]*M[3]//q[3][1]
        htop=ceil(q[1][1]*P[2],L[2])+ceil(q[2][1]*P[3],L[3])+q[3][1]
        levels=[n*Q for n in range(1,3+(htop+P[1])//Q,2) if hbase<=n*Q<=htop+P[1]]
        if not levels:return
        constraints.append((min(levels)-htop,-P[1],0))
        constraints.append((hbase-max(levels),M[1],0))
        bound=(P[1]+P[3])*Q
        for idx,(u,v,c) in enumerate(constraints):
            for U,V,C in constraints[idx+1:]:
                det=u*V-U*v
                if det==0:continue
                l=P[3]*V-P[1]*U;m=u*P[1]-v*P[3]
                if det<0:det,l,m=-det,-l,-m
                if l>=0 and m>=0:bound=min(bound,ceil(l*c+m*C,det))
        ub=ceil(bound,Q)+ceil(P[2]*P[1],L[2])+ceil(P[3]*P[2],L[3])
        if ub<Q:cnt[1]+=1;cnt[2]=max(cnt[2],ub);return
        i=max((1,2,3,6,7),key=lambda i:x[i][1]-x[i][0]);l,h=x[i]
        assert h-l>1,(x,ub)
        m=(l+h)//2;y=[a[:] for a in x];x[i][1]=m;y[i][0]=m
        visit(x);visit(y)
    x=[[0,Q] for _ in range(8)]
    for i in (0,4,5):x[i][1]=ceil(Q,den)
    for i in (6,7):x[i][0]=Q//40
    visit(x);print('adjacent short, denominator',den,'boxes',cnt,flush=True)
if __name__=='__main__':
    import sys
    check(int(sys.argv[1]) if len(sys.argv)>1 else 1000)
