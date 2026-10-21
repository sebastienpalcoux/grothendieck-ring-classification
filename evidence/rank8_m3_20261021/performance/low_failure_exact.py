"""Exact positive-PSD shortcut for the frozen low-induction obstruction test.

The original checker is retained for non-PSD inputs so its first obstruction
and coordinates are unchanged. Positive inputs execute the identical moment
formula. Python integer arithmetic has no overflow bound.
"""
import functools,sys
import induction
from exact import ec
_FROZEN_LOW_FAILURE=induction.low_failure

@functools.lru_cache(maxsize=32768)
def positive_semidefinite(entries):
    """Decide PSD for a symmetric integral matrix by fraction-free Schur steps.

    A zero diagonal in a PSD matrix forces its entire row to vanish. A positive
    diagonal allows the exact Schur-complement reduction. The denominator in
    Bareiss elimination is the preceding positive pivot; exact divisions are
    checked, so no truncation can produce a false positive.
    """
    n=len(entries)
    if any(len(row)!=n for row in entries):return None
    if any(type(x) is not int for row in entries for x in row):return None
    if any(entries[i][j]!=entries[j][i] for i in range(n) for j in range(i)):return None
    a=[list(row) for row in entries];previous=1
    for k in range(n):
        pivot=a[k][k]
        if pivot<0:return False
        if pivot==0:
            if any(a[k][j]!=0 for j in range(k+1,n)):return False
            continue
        for i in range(k+1,n):
            for j in range(i,n):
                value=pivot*a[i][j]-a[i][k]*a[k][j]
                quotient,remainder=divmod(value,previous)
                if remainder:return None
                a[i][j]=a[j][i]=quotient
        previous=pivot
    return True

def low_failure(cols,B,ds,D,K,emb,du):
    n=len(ds)
    LL=[[sum(c[i]*c[j] for c in cols) for j in range(n)] for i in range(n)]
    Q=[[int(B[i,j])-LL[i][j] for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(i,n):
            if Q[i][j]<0:return {'kind':'gram_entry','coordinates':[i,j]}
    tail=tuple(tuple(Q[i][j] for j in range(1,n)) for i in range(1,n))
    if positive_semidefinite(tail) is not True:
        return _FROZEN_LOW_FAILURE(cols,B,ds,D,K,emb,du)
    for i in range(1,n):
        low=sum((K(LL[i][j])*ds[j] for j in range(n)),K.zero)
        gap=(K(3)*low-D*ds[i]) if du[i]!=i else ((K(3)*ds[i]+K.one)*low-D*ds[i]*(ds[i]+K.one))
        if emb.sign(gap)>0:return {'kind':'moment','object':i,'nonselfdual':du[i]!=i,'gap':ec(gap)}
    return None

def install(extra_module=None):
    old=induction.low_failure
    if extra_module is not None:
        extra=getattr(extra_module,'low_failure',None)
        if extra is _FROZEN_LOW_FAILURE:setattr(extra_module,'low_failure',low_failure)
        elif extra is not low_failure:raise RuntimeError('explicit module has an unfamiliar low_failure; review before installing')
    if old is low_failure:return
    if old is not _FROZEN_LOW_FAILURE:
        raise RuntimeError('low_failure was changed by another adapter; review before installing')
    for module in tuple(sys.modules.values()):
        if module is not None and getattr(module,'low_failure',None) is old:
            setattr(module,'low_failure',low_failure)
    induction.low_failure=low_failure
