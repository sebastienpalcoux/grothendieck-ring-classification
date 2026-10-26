"""Exact full triality-gauging tensors and their bosonic C2 zests.

S matrix source: Cui--Galindo--Plavnik--Wang arXiv:1510.03475v3,
Section 6.2; m=0 variant: Teo--Hughes--Fradkin arXiv:1503.06812,
Eq. (6.53), already used in the lower-rank project.
Arithmetic is Q[y,s]/(y^3-3y-1,s^2-2), y=2cos(pi/9), s=sqrt(2).
"""
from fractions import Fraction as Q
import itertools

def require(ok, text):
    if not ok:
        raise ValueError(text)

def e(c=0, y=0, s=0):
    z=[Q(0)]*6;z[y+3*s]=Q(c);return tuple(z)

def add(a,b):return tuple(x+y for x,y in zip(a,b))
def scale(a,b):return tuple(x*b for x in a)
def mul(a,b):
    z=[Q(0)]*5;w=[Q(0)]*5
    for i,x in enumerate(a):
        if not x:continue
        for j,y in enumerate(b):
            if not y:continue
            k=(i%3)+(j%3);r=i//3+j//3
            (w if r%2 else z)[k]+=x*y*(2 if r==2 else 1)
    for v in [z,w]:
        for k in (4,3):v[k-2]+=3*v[k];v[k-3]+=v[k]
    return tuple(z[:3]+w[:3])
def total(seq):
    z=e()
    for v in seq:z=add(z,v)
    return z

def source_tensor(m):
    require(m in [0,1], 'retained gauging parameter')
    a,b,c=(e(4),e(-8),e(4)) if m==0 else (add(e(8),e(-4,2)),add(add(e(-8),e(-4,1)),e(4,2)),e(4,1))
    top=[[e(v)for v in row]for row in [
        [1,1,2,4,4,4,3,3],[1,1,2,4,4,4,3,3],
        [2,2,4,-4,-4,-4,6,6],[4,4,-4,0,0,0,0,0],
        [4,4,-4,0,0,0,0,0],[4,4,-4,0,0,0,0,0],
        [3,3,6,0,0,0,-3,-3],[3,3,6,0,0,0,-3,-3]]]
    for i,row in enumerate([[b,c,a],[c,a,b],[a,b,c]]):
        for j,v in enumerate(row):top[3+i][3+j]=v
    u=[[3]*4,[-3]*4,[0]*4,[0]*4,[0]*4,[0]*4,[-3,-3,3,3],[3,3,-3,-3]]
    bottom=[[0,0,6,-6],[0,0,-6,6],[6,-6,0,0],[-6,6,0,0]]
    S=[[e()for _ in range(12)]for _ in range(12)]
    for i,j in itertools.product(range(8),repeat=2):S[i][j]=top[i][j]
    for i in range(8):
        for j in range(4):S[i][8+j]=S[8+j][i]=e(u[i][j],s=1)
    for i,j in itertools.product(range(4),repeat=2):S[8+i][8+j]=e(bottom[i][j])
    require(all(S[i][j]==S[j][i]for i,j in itertools.product(range(12),repeat=2)),'S symmetry')
    require(all(total(mul(S[i][k],S[k][j])for k in range(12))==e(144*(i==j))for i,j in itertools.product(range(12),repeat=2)),'exact S orthogonality')
    inverse_dimensions=[e(Q(1,d))for d in [1,1,2,4,4,4,3,3]]+[e(Q(1,6),s=1)]*4
    R=[[[0]*12 for _ in range(12)]for _ in range(12)]
    for i,j,k in itertools.product(range(12),repeat=3):
        v=scale(total(mul(mul(mul(S[i][a],S[j][a]),S[k][a]),inverse_dimensions[a])for a in range(12)),Q(1,144))
        require(all(x==0 for x in v[1:])and v[0].denominator==1 and v[0]>=0,'exact Verlinde integrality')
        R[i][j][k]=int(v[0])
    return R

def zest(R):
    """Odd objects 8..11; h=1 is the canonical Rep(C2) boson."""
    n=len(R);g=[0]*8+[1]*4;h=1
    hp=[row.index(1)for row in R[h]]
    return [[[R[i][j][hp[k]if g[i]and g[j]else k]for k in range(n)]for j in range(n)]for i in range(n)]
