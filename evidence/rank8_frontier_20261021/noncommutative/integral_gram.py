"""Complete bounded integral Gram-completion enumeration for small kernels."""
import itertools,math
import character_modular as modular
c=modular.c;full=modular.full

def completions(a,cols,maximum_box=1000000):
    L=c.s.Matrix.hstack(*map(c.s.Matrix,cols));Q,high=full.base.grams.high_columns(a,L)
    pairs=list(itertools.combinations_with_replacement(range(7),2))
    A=c.s.Matrix([[v[i]*v[j] for v,z in high] for i,j in pairs]);b=c.s.Matrix([Q[i,j] for i,j in pairs])
    n=len(high);rr,piv=A.row_join(b).rref();c.require(n not in piv,'Gram system consistent')
    bounds=[min(int(Q[j,j])//(v[j]**2) for j in range(7) if v[j]) for v,z in high]
    free=[j for j in range(n) if j not in piv];box=math.prod(bounds[j]+1 for j in free)
    c.require(box<=maximum_box,'complete integral Gram box exceeds explicit resource limit')
    out=[]
    for vs in itertools.product(*(range(bounds[j]+1) for j in free)):
        v=[c.s.S.Zero]*n
        for j,z in zip(free,vs):v[j]=c.s.Integer(z)
        for row,j in enumerate(piv):v[j]=rr[row,n]-sum(rr[row,k]*v[k] for k in free)
        if all(z.q==1 and 0<=z<=bounds[j] for j,z in enumerate(v)):out.append(tuple(map(int,v)))
    return sorted(out),{'high_columns':n,'equation_rank':A.rank(),'free_coordinates':free,'box_size':box,'complete':True}

def append_multiplicities(A,b,counts,nt):
    A=list(A);b=list(b)
    for j,count in enumerate(counts):
        row=[0]*len(A[0]);row[j*nt:(j+1)*nt]=[1]*nt;A.append(row);b.append(count)
    return A,b
