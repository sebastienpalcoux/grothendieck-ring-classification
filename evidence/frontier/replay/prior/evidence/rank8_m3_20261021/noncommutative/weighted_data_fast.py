"""Exact weighted row-sum enumeration by meet in the middle.

The ordered output retains all low frames up to exchanging identical
restriction-column sets of equal character multiplicity.
"""
import itertools,math
def low_frames(sets,weights,B):
    n=B.rows;unit=(1,)+(0,)*(n-1);target=tuple(int(B[0,i])-unit[i] for i in range(n))
    if not sets or any(not cs for cs in sets):return []
    count=len(sets);indices=tuple(range(count))
    choices=[(J,tuple(i for i in indices if i not in J)) for k in range(1,count) for J in itertools.combinations(indices,k)]
    if not choices:
        return [(unit,c) for c in sets[0] if tuple(weights[0]*x for x in c)==target]
    left,right=min(choices,key=lambda p:sum(math.prod(len(sets[i]) for i in h) for h in p))
    if math.prod(len(sets[i]) for i in left)>math.prod(len(sets[i]) for i in right):left,right=right,left
    buckets={}
    for columns in itertools.product(*(sets[i] for i in left)):
        key=tuple(sum(weights[i]*c[j] for i,c in zip(left,columns)) for j in range(n))
        if any(x>y for x,y in zip(key,target)):continue
        buckets.setdefault(key,[]).append(columns)
    out=[]
    for columns in itertools.product(*(sets[i] for i in right)):
        key=tuple(target[j]-sum(weights[i]*c[j] for i,c in zip(right,columns)) for j in range(n))
        for other in buckets.get(key,[]):
            full=[None]*count
            for i,c in zip(left,other):full[i]=c
            for i,c in zip(right,columns):full[i]=c
            if any(weights[i]==weights[j] and sets[i]==sets[j] and full[i]>full[j] for i in indices for j in range(i+1,count)):continue
            out.append((unit,)+tuple(full))
    return sorted(out)
