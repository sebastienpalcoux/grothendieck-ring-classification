"""Explicit homogeneous bimodules for an inflated C4 three-cocycle.

All scalars are fourth roots of unity, stored as exponents modulo four.
The bimodule actions and balanced quotient are derived directly from Vec_G^omega.
"""
from pathlib import Path
from itertools import product
import json,gzip,sys,hashlib

G=list(product(range(5),range(4)))
e=(0,0);s=(0,2);H=[e,s]
def mul(x,y):return ((x[0]+pow(2,x[1],5)*y[0])%5,(x[1]+y[1])%4)
def w(x,y,z):return (2*x[1]*((y[1]+z[1])//4))%4
def require(x):
    if not x:raise ValueError('exact condition failed')

def construct():
    require(all((w(b,c,d)+w(a,mul(b,c),d)+w(a,b,c)-w(mul(a,b),c,d)-w(a,b,mul(c,d)))%4==0
                for a,b,c,d in product(G,repeat=4)))
    require(all(w(a,b,c)==0 for a,b,c in product(H,repeat=3)))
    seen=set();objs=[]
    for g in G:
        if g in seen:continue
        tags={mul(mul(h,g),k):(h,k) for h,k in product(H,repeat=2)}
        D=set(tags);seen|=D;p=g[1]%2
        for sign in ([0,2] if len(D)==2 else [0]):
            L={x:(mul(s,x),0) for x in D}
            R={x:(mul(x,s),(p+sign)%4 if len(D)==2 else (2*p if tags[x][1]==s else 0)) for x in D}
            require(all(R[R[x][0]][0]==x and (R[x][1]+R[R[x][0]][1]-w(x,s,s))%4==0 for x in D))
            require(all(R[L[x][0]][0]==L[R[x][0]][0] and (R[L[x][0]][1]-R[x][1])%4==0 for x in D))
            objs.append({'g':g,'D':D,'L':L,'R':R,'sign':sign,'p':p})
    n=len(objs);N=[[[0]*n for _ in range(n)]for _ in range(n)]
    for i,A in enumerate(objs):
        for j,B in enumerate(objs):
            pairs=list(product(sorted(A['D']),sorted(B['D'])))
            # e_(x,y)=i^phase e_representative in the balanced quotient.
            maps={}
            for x,y in pairs:
                Q=(mul(x,s),mul(s,y));P=(x,y)
                require(mul(*P)==mul(*Q))
                phase=(w(mul(x,s),s,y)-A['R'][mul(x,s)][1])%4
                back=(w(x,s,mul(s,y))-A['R'][x][1])%4
                require((phase+back)%4==0)
                rep=min(P,Q)
                maps[P]=(rep,0 if P==rep else phase)
            reps=sorted({p for p,a in maps.values()})
            for k,C in enumerate(objs):
                z=C['g'];basis=[P for P in reps if mul(*P)==z]
                if len(C['D'])==4:
                    N[i][j][k]=len(basis);continue
                # L_s^{-1}R_s on grade z; its eigenvalues for C are i^(p+sign).
                trace=[0,0,0,0]
                for P in basis:
                    x,y=P
                    # right action followed by inverse left action (left phases 1).
                    target=(mul(s,x),mul(y,s))
                    ph=(w(x,y,s)+B['R'][y][1])%4
                    rep,q=maps[target]
                    require(mul(*rep)==z)
                    if rep==P:trace[(ph+q)%4]+=1
                # trace divided by i^p must be an integer; split +/- eigenspaces.
                tr=[trace[(t+C['p'])%4] for t in range(4)]
                require(tr[1]==tr[3])
                t=tr[0]-tr[2]
                multiplicity=(len(basis)+(1 if C['sign']==0 else -1)*t)
                require(multiplicity%2==0 and multiplicity>=0)
                N[i][j][k]=multiplicity//2
    require(all(N[0][i][j]==N[i][0][j]==int(i==j) for i,j in product(range(n),repeat=2)))
    require(all(sum(N[i][j][p]*N[p][k][l] for p in range(n))==sum(N[j][k][p]*N[i][p][l]for p in range(n))
                for i,j,k,l in product(range(n),repeat=4)))
    dims=[len(x['D'])//2 for x in objs]
    require(all(sum(N[i][j][k]*dims[k] for k in range(n))==dims[i]*dims[j] for i,j in product(range(n),repeat=2)))
    return N,[{'g':a['g'],'support':sorted(a['D']),'sign':a['sign'],'p':a['p']}for a in objs]

if __name__=='__main__':
    R, labels=construct()
    print(json.dumps({'rank':len(R),'simple_bimodules':labels,'tensor':R},indent=2))
