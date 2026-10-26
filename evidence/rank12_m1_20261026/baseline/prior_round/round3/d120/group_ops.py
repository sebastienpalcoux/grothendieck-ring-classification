import itertools
import common
def order(M,a):
    x=a;k=1
    while x:x=M[x][a];k+=1
    return k
def subgroup(M,gens):
    out={0};queue=[0]
    for x in queue:
        for g in gens:
            y=M[x][g]
            if y not in out:out.add(y);queue.append(y)
    return sorted(out)
def group_product(A,B):
    b=len(B)
    return [[A[i//b][j//b]*b+B[i%b][j%b]for j in range(len(A)*b)]for i in range(len(A)*b)]
def matrix_group(p,special=False):
    vals=[a for a in itertools.product(range(p),repeat=4)if ((a[0]*a[3]-a[1]*a[2])%p==1 if special else(a[0]*a[3]-a[1]*a[2])%p!=0)]
    one=(1,0,0,1);vals=[one]+[a for a in vals if a!=one];ix={a:i for i,a in enumerate(vals)}
    def mul(a,b):return((a[0]*b[0]+a[1]*b[2])%p,(a[0]*b[1]+a[1]*b[3])%p,(a[2]*b[0]+a[3]*b[2])%p,(a[2]*b[1]+a[3]*b[3])%p)
    return vals,[[ix[mul(a,b)]for b in vals]for a in vals]
def permutation_group(n):
    vals=list(itertools.permutations(range(n)));ix={a:i for i,a in enumerate(vals)}
    return vals,[[ix[tuple(a[b[i]]for i in range(n))]for b in vals]for a in vals]

