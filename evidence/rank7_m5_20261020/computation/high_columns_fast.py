"""Same exact high-vector condition; native rational-range enumeration.
Discovery acceleration only; accepted certificates replay the inherited engine.
"""
from higher_traces import s,itertools,math,Q,integer_pair
from gram_vectors_fast import native

def high_columns(data,L):
    n=data['ch'].n;q=data['q'];d=data['dimensions'];D=data['global_dimension']
    B=data['ch'].C;Qm=(B-L*L.T).extract(range(1,n),range(1,n));rank=Qm.rank()
    if not rank:return Qm,[]
    ix=next(ii for ii in itertools.combinations(range(n-1),rank) if Qm.extract(ii,ii).det()!=0)
    sub=Qm.extract(ix,ix);adj=[[int(x) for x in row] for row in sub.adjugate().tolist()];det=int(sub.det());null=Qm.nullspace();cols=[]
    null=[[int(x*math.lcm(*(int(y.q) for y in z))) for x in z] for z in null]
    entries=[[int(x) for x in row] for row in Qm.tolist()]
    denominator=math.lcm(*(x.denominator for pair in d for x in pair))
    dimensions=[[int(x*denominator) for x in pair] for pair in d]
    candidates=native(Qm)
    for v in candidates:
        if not any(v):continue
        if any(v[i]*v[j]>entries[i][j] for i in range(n-1) for j in range(i,n-1)):continue
        if any(sum(v[i]*z[i] for i in range(n-1)) for z in null):continue
        vv=[v[i] for i in ix]
        if sum(vv[i]*adj[i][j]*vv[j] for i in range(rank) for j in range(rank))>det:continue
        z=tuple(Q(sum(v[i]*dimensions[i+1][j] for i in range(n-1)),denominator) for j in range(2));norm=z[0]**2-q*z[1]**2
        if not norm:continue
        quotient=( (D[0]*z[0]-q*D[1]*z[1])/norm, (D[1]*z[0]-D[0]*z[1])/norm )
        if not integer_pair(quotient,q):continue
        if z[1] and ((2*z[0])**2/norm).denominator!=1:continue
        cols.append((v,z))
    return Qm,cols
