"""Based rings and character fields. No catalogue-index exclusion rules."""
import itertools,hashlib,json,math
import sympy as s
from exact import *

PERMS=tuple((0,)+p for p in itertools.permutations((1,2,3)))
def flat(R):return tuple(v for M in R for row in M for v in row)
def permute(R,p):return [[[R[p[i]][p[j]][p[k]] for k in range(4)] for j in range(4)] for i in range(4)]
def canonical(R):return min(flat(permute(R,p)) for p in PERMS)
def fingerprint(R):return hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()
def dual(R):return [next(j for j in range(4) if R[i][j][0]) for i in range(4)]
def multiplicity(R):return max(flat(R))
def matrices(R):return list(map(s.Matrix,R))
def casimir(R):
    N=matrices(R);d=dual(R);return sum((N[i]*N[d[i]] for i in range(4)),s.zeros(4))
def casimir_determinant(R):
    """Exact fraction-free determinant of sum_i N_i N_i^T, over Python integers."""
    C=[[sum(R[i][j][l]*R[i][k][l] for i in range(4) for l in range(4))
        for k in range(4)] for j in range(4)]
    # N_0 is the identity, so this Gram sum is positive definite and every
    # Bareiss pivot is nonzero. The exact divisions are checked explicitly.
    previous=1
    for k in range(3):
        pivot=C[k][k];require(pivot>0,'nonpositive Casimir pivot')
        for i in range(k+1,4):
            for j in range(k+1,4):
                q=C[i][j]*pivot-C[i][k]*C[k][j]
                require(q%previous==0,'nonintegral Bareiss division')
                C[i][j]=q//previous
        previous=pivot
    return C[3][3]

def codegree_poly(R):return casimir(R).charpoly(t).as_poly()
def codegree_factors(R):return factors(tuple(pc(codegree_poly(R))))

def validate(R,nonnegative=True):
    require(len(R)==4 and all(len(M)==4 and all(len(row)==4 for row in M) for M in R),'not rank four')
    require(all(type(v) is int and (v>=0 or not nonnegative) for v in flat(R)),'invalid coefficient')
    d=dual(R);require(all(d[d[i]]==i for i in range(4)),'invalid involution')
    for i,j in itertools.product(range(4),repeat=2):
        require(R[0][i][j]==(i==j) and R[i][0][j]==(i==j),'unit failure')
        require(R[i][j][0]==(d[i]==j),'unit coefficient failure')
    for i,j,k in itertools.product(range(4),repeat=3):
        require(R[i][j][k]==R[j][i][k]==R[d[i]][k][j]==R[k][d[j]][i],'reciprocity failure')
    for i,j,k,l in itertools.product(range(4),repeat=4):
        require(sum(R[i][j][a]*R[a][k][l] for a in range(4))==sum(R[j][k][a]*R[i][a][l] for a in range(4)),'associativity failure')

def dnumber(R):
    for p,m in codegree_factors(R):
        co=list(map(int,p.all_coeffs()));d=p.degree();n=abs(co[-1])
        for j,a in enumerate(co[1:],1):
            if a**d%n**j:return {'kind':'dnumber','factor':pc(p),'j':j}
    return None

def check_dnumber(R,c):
    p=poly(c['factor']);j=c['j'];require(any(p==q for q,m in codegree_factors(R)),'unrelated d-number factor')
    require(1<=j<=p.degree(),'coefficient index');co=p.all_coeffs()
    require(int(co[j])**p.degree()%abs(int(co[-1]))**j!=0,'d-number divisibility holds')

def sd_tuple(R):
    return (R[1][1][1],R[1][1][2],R[1][1][3],R[1][2][2],R[1][2][3],R[1][3][3],R[2][2][2],R[2][2][3],R[2][3][3],R[3][3][3])
def sd_tensor(p):
    a,b,c,d,e,f,g,h,i,j=p
    return [[[int(v==w) for w in range(4)] for v in range(4)],[[0,1,0,0],[1,a,b,c],[0,b,d,e],[0,c,e,f]],[[0,0,1,0],[0,b,d,e],[1,d,g,h],[0,e,h,i]],[[0,0,0,1],[0,c,e,f],[0,e,h,i],[1,f,i,j]]]
SD_MASKS=(1,2,4,1,7,1,2,4,2,4)
SD_PERM_MAPS=tuple(sd_tuple(permute(sd_tensor(tuple(range(10))),p)) for p in PERMS)

def canonical_sd_tuple(p):
    return min(tuple(p[k] for k in mapping) for mapping in SD_PERM_MAPS)

def ns_tensor(p):
    a,b,c,d,e,f=p
    x=[[0,1,0,0],[1,a,b,b],[0,b,c,d],[0,b,d,c]]
    y=[[0,0,1,0],[0,b,c,d],[0,d,e,f],[1,c,e,e]]
    return [[[int(v==w) for w in range(4)] for v in range(4)],x,y,list(map(list,zip(*y)))]
def ns_tuple(R):return (R[1][1][1],R[1][1][2],R[1][2][2],R[1][2][3],R[2][2][2],R[2][2][3])

def root_family(R):
    if dual(R)!=[0,1,2,3]:return None
    for p in PERMS:
        A=permute(R,p);n=A[1][1][3]
        if n>=2 and A==sd_tensor((n-1,n-1,n,n,n,n,n,n,n+1,n+1)):
            return {'kind':'root_length','basis':list(p),'n':n}
    return None

class Characters:
    """Q[R] presented by a separating element 1+b1+k*b2+k^2*b3."""
    def __init__(self,R,k=None):
        self.R=R;self.N=matrices(R);self.du=dual(R);self.C=casimir(R)
        for a in ([k] if k is not None else range(1,14)):
            H=self.N[0]+self.N[1]+a*self.N[2]+a*a*self.N[3]
            p=H.charpoly(t).as_poly()
            if s.gcd(p,p.diff()).degree()==0:break
        else:raise VerificationError('no separating element')
        require(s.gcd(p,p.diff()).degree()==0,'nonseparating proposed element')
        self.k=a;self.H=H;self.p=p;self.components=p.factor_list()[1]
        V=s.Matrix.hstack(*[(H**i)[0,:].T for i in range(4)])
        require(V.det()!=0,'powers do not span the algebra')
        self.coeff=[list(V.inv()*self.N[i][0,:].T) for i in range(4)]
        for i in range(4):
            require(sum((self.coeff[i][j]*H**j for j in range(4)),s.zeros(4))==self.N[i],'wrong polynomial coordinates')
        self.cf=codegree_factors(R)
    def component(self,f):
        K=field(f)
        ds=[K(s.Poly.from_list(list(reversed(c)),t,domain=s.QQ).rem(f).all_coeffs()) for c in self.coeff]
        delta=sum((ds[i]*ds[self.du[i]] for i in range(4)),K.zero)
        match=[p for p,m in self.cf if not evaluate(p.all_coeffs(),delta,K)]
        require(len(match)==1,'ambiguous codegree factor')
        return K,ds,delta,match[0]
    def fp(self):
        # The separating element is strictly positive in the regular basis.
        require(all(v>0 for v in self.H),'FP selection requires a positive matrix')
        f,emb=max(((f,e) for f,m in self.components for e in embeddings(f)),key=lambda fe:fe[1].hi)
        K,ds,D,pD=self.component(f)
        require(all(emb.sign(d)>0 for d in ds),'selected character not positive')
        return f,K,ds,D,pD,emb
