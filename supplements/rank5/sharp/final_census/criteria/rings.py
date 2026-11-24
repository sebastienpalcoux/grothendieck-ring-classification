"""Exact commutative based-ring arithmetic, with rank supplied by the tensor.

The semisimple character routines require commutativity explicitly.
No rank-four commutativity theorem is assumed in rank five.
"""
import itertools, hashlib, json
import sympy as s
from exact import *

def flat(R): return tuple(v for M in R for row in M for v in row)
def dual(R):
    n=len(R)
    d=[]
    for i in range(n):
        hits=[j for j in range(n) if R[i][j][0]]
        require(len(hits)==1,'duality is not unique')
        d.append(hits[0])
    return d
def matrices(R): return list(map(s.Matrix,R))
def permute(R,p): return [[[R[i][j][k] for k in p] for j in p] for i in p]
def canonical(R):
    return min(flat(permute(R,(0,)+p)) for p in itertools.permutations(range(1,len(R))))
def fingerprint(R): return hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()
def casimir(R):
    N=matrices(R)
    return sum((a*a.T for a in N),s.zeros(len(R)))
def codegree_poly(R): return casimir(R).charpoly(t).as_poly()
def codegree_factors(R): return factors(tuple(pc(codegree_poly(R))))
def validate(R,nonnegative=True):
    n=len(R);I=range(n)
    require(all(len(M)==n and all(len(row)==n for row in M) for M in R),'tensor shape')
    require(all(type(v) is int and (v>=0 or not nonnegative) for v in flat(R)),'coefficient')
    du=dual(R)
    require(all(du[du[i]]==i for i in I),'duality involution')
    for i,j in itertools.product(I,repeat=2):
        require(R[0][i][j]==R[i][0][j]==int(i==j),'unit')
        require(R[i][j][0]==int(du[i]==j),'unit coefficient')
    for i,j,k in itertools.product(I,repeat=3):
        require(R[i][j][k]==R[j][i][k]==R[du[i]][k][j]==R[k][du[j]][i],'commutativity/reciprocity')
    N=matrices(R)
    for i,j in itertools.product(I,repeat=2):
        require(N[i]*N[j]==sum((R[i][j][k]*N[k] for k in I),s.zeros(n)),'associativity')
def dnumber(R):
    for p,m in codegree_factors(R):
        co=list(map(int,p.all_coeffs())); e=p.degree(); q=abs(co[-1])
        for j,a in enumerate(co[1:],1):
            if a**e%q**j: return {'kind':'dnumber','factor':pc(p),'j':j}
    return None
def check_dnumber(R,c):
    p=poly(c['factor']);j=c['j'];co=p.all_coeffs()
    require(any(p==q for q,m in codegree_factors(R)),'unrelated factor')
    require(1<=j<=p.degree(),'coefficient index')
    require(int(co[j])**p.degree()%abs(int(co[-1]))**j!=0,'divisibility holds')

class Characters:
    """A separating element 1+b1+k*b2+...+k^(r-2)*b_(r-1).

    Each pair of distinct characters coincides for at most r-2 values of k.
    Thus (r choose 2)(r-2)+1 positive integers suffice.
    """
    def __init__(self,R,k=None):
        self.R=R; self.N=N=matrices(R); self.n=n=len(R);self.du=dual(R)
        require(all(N[i]*N[j]==N[j]*N[i] for i in range(n) for j in range(i)),'noncommutative algebra')
        self.C=casimir(R)
        for a in ([k] if k is not None else range(1,n*(n-1)*(n-2)//2+2)):
            H=N[0]+sum((a**(i-1)*N[i] for i in range(1,n)),s.zeros(n))
            p=H.charpoly(t).as_poly()
            if s.gcd(p,p.diff()).degree()==0: break
        else: raise VerificationError('no separating element')
        require(s.gcd(p,p.diff()).degree()==0,'nonseparating generator')
        self.k=a;self.H=H;self.p=p;self.components=p.factor_list()[1]
        V=s.Matrix.hstack(*[(H**i)[0,:].T for i in range(n)])
        require(V.det()!=0,'powers do not span')
        self.coeff=[list(V.inv()*N[i][0,:].T) for i in range(n)]
        for i in range(n):
            require(sum((self.coeff[i][j]*H**j for j in range(n)),s.zeros(n))==N[i],'polynomial coordinates')
        self.cf=codegree_factors(R)
    def component(self,f):
        K=field(f)
        ds=[K(s.Poly.from_list(list(reversed(c)),t,domain=s.QQ).rem(f).all_coeffs()) for c in self.coeff]
        delta=sum((ds[i]*ds[self.du[i]] for i in range(self.n)),K.zero)
        matches=[p for p,m in self.cf if not evaluate(p.all_coeffs(),delta,K)]
        require(len(matches)==1,'ambiguous codegree')
        return K,ds,delta,matches[0]
    def fp(self):
        require(all(v>0 for v in self.H),'nonpositive separating matrix')
        f,emb=max(((f,e) for f,m in self.components for e in embeddings(f)),key=lambda fe:fe[1].hi)
        K,ds,D,pD=self.component(f)
        require(all(emb.sign(d)>0 for d in ds),'selected character not positive')
        return f,K,ds,D,pD,emb
