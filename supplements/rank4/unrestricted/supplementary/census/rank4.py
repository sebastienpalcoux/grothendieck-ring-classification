"""Small exact rank-four tensor utilities; Python standard library only.
R[i][j][k] is the coefficient of basis k in the product of bases i,j.
"""
import hashlib
import itertools
import json

PERMUTATIONS=tuple((0,)+p for p in itertools.permutations((1,2,3)))

def require(ok,message):
    if not ok: raise ValueError(message)

def tensor(tag,p):
    unit=[[int(j==k) for k in range(4)] for j in range(4)]
    if tag=='S':
        a,b,c,d,e,f,g,h,i,j=p
        return [unit,[[0,1,0,0],[1,a,b,c],[0,b,d,e],[0,c,e,f]],
                [[0,0,1,0],[0,b,d,e],[1,d,g,h],[0,e,h,i]],
                [[0,0,0,1],[0,c,e,f],[0,e,h,i],[1,f,i,j]]]
    require(tag=='N','unknown parameter tag')
    a,b,c,d,e,f=p
    y=[[0,0,1,0],[0,b,c,d],[0,d,e,f],[1,c,e,e]]
    return [unit,[[0,1,0,0],[1,a,b,b],[0,b,c,d],[0,b,d,c]],y,
            [list(row) for row in zip(*y)]]

def canonical(R):
    return min(tuple(R[p[i]][p[j]][p[k]] for i in range(4)
                     for j in range(4) for k in range(4)) for p in PERMUTATIONS)

def fingerprint(R):
    return hashlib.sha256(json.dumps(canonical(R),separators=(',',':')).encode()).hexdigest()

def casimir(R):
    return [[sum(R[i][j][l]*R[i][k][l] for i in range(4) for l in range(4))
             for k in range(4)] for j in range(4)]

def leading_minors(C,D=1000):
    """Return all positive leading minors, ending at the first nonpositive one."""
    A=[[D*(i==j)-C[i][j] for j in range(4)] for i in range(4)]
    out=[];previous=1
    for k in range(4):
        pivot=A[k][k];out.append(pivot)
        if pivot<=0 or k==3:return out
        for i in range(k+1,4):
            for j in range(k+1,4):
                value=A[i][j]*pivot-A[i][k]*A[k][j]
                require(value%previous==0,'inexact Bareiss division')
                A[i][j]=value//previous
        previous=pivot
    return out

def matmul(A,B):
    return [[sum(A[i][k]*B[k][j] for k in range(4)) for j in range(4)]for i in range(4)]

def characteristic_polynomial(C):
    """Descending coefficients, from exact Newton identities."""
    powers=C;traces=[0]
    for k in range(1,5):
        traces.append(sum(powers[i][i]for i in range(4)))
        if k<4:powers=matmul(powers,C)
    coefficients=[1]
    for k in range(1,5):
        value=-sum(coefficients[k-i]*traces[i]for i in range(1,k+1))
        require(value%k==0,'nonintegral characteristic coefficient')
        coefficients.append(value//k)
    return coefficients

def validate(R):
    require(len(R)==4 and all(len(A)==4 and all(len(row)==4 for row in A) for A in R),'tensor shape')
    require(all(type(v)is int and v>=0 for A in R for row in A for v in row),'invalid coefficient')
    dual=[]
    for i in range(4):
        choices=[j for j in range(4)if R[i][j][0]==1]
        require(len(choices)==1,'nonunique dual');dual.append(choices[0])
    for i in range(4):
        require(dual[dual[i]]==i,'duality not involutive')
        for j in range(4):
            require(R[0][i][j]==(i==j)==R[i][0][j],'unit')
            require(R[i][j][0]==(dual[i]==j),'unit coefficient')
            for k in range(4):
                require(R[i][j][k]==R[j][i][k],'commutativity')
                require(R[i][j][k]==R[dual[i]][k][j]==R[k][dual[j]][i],'reciprocity')
                for l in range(4):
                    left=sum(R[i][j][s]*R[s][k][l] for s in range(4))
                    right=sum(R[j][k][s]*R[i][s][l] for s in range(4))
                    require(left==right,'associativity')
    return dual
