"""Exact finite-domain propagation for integer equalities and box bounds.

Every tightening is a consequence of one original equality and the current
integer interval bounds. Default replay recomputes all steps exactly.
"""
from collections import deque
from dataclasses import replace
import hashlib,json,math
from features import require,st

def propagate(system):
    m=len(system.rhs);n=len(system.columns)
    rows=[[]for _ in range(m)];cols=[]
    for j,col in enumerate(system.columns):
        nz=[]
        for i,a in enumerate(col):
            if a:rows[i].append((j,a));nz.append((i,a))
        cols.append(nz)
    lo=[0]*n;hi=list(system.bounds)
    mn=[sum(min(0,a*hi[j])for j,a in row)for row in rows]
    mx=[sum(max(0,a*hi[j])for j,a in row)for row in rows]
    queue=deque(range(m));queued=set(range(m));steps=[]
    def receipt(outcome,contradiction=None):
        out={'outcome':outcome,'lower_bounds':lo,'upper_bounds':hi,'tightenings':len(steps),
             'step_sha256':st.digest(steps),'fixed_variables':sum(a==b for a,b in zip(lo,hi)),
             'fixed_nonzero_variables':sum(a==b and a!=0 for a,b in zip(lo,hi))}
        if contradiction is not None:out['contradiction']=contradiction
        return out
    while queue:
        i=queue.popleft();queued.remove(i);b=system.rhs[i]
        if not mn[i]<=b<=mx[i]:
            return receipt('integer_box_obstruction',{'row':i,'rhs':b,'minimum':mn[i],'maximum':mx[i]})
        # GCD is an additional necessary integer condition after fixed
        # variables are moved to the RHS.
        g=0;fixed=0
        for j,a in rows[i]:
            if lo[j]==hi[j]:fixed+=a*lo[j]
            else:g=math.gcd(g,abs(a))
        if g and (b-fixed)%g:
            return receipt('integer_box_obstruction',{'row':i,'rhs':b,'fixed_contribution':fixed,'free_gcd':g})
        for j,a in rows[i]:
            if lo[j]==hi[j]:continue
            l,h=lo[j],hi[j];oldmin=min(a*l,a*h);oldmax=max(a*l,a*h)
            othermin=mn[i]-oldmin;othermax=mx[i]-oldmax
            ceil=lambda x,d:-((-x)//d)
            if a>0:newlo=max(l,ceil(b-othermax,a));newhi=min(h,(b-othermin)//a)
            else:newlo=max(l,ceil(b-othermin,a));newhi=min(h,(b-othermax)//a)
            if newlo>newhi:
                return receipt('integer_box_obstruction',{'row':i,'variable':j,'derived_lower':newlo,'derived_upper':newhi})
            if newlo==l and newhi==h:continue
            steps.append((i,j,newlo,newhi));lo[j]=newlo;hi[j]=newhi
            for k,c in cols[j]:
                mn[k]+=min(c*newlo,c*newhi)-min(c*l,c*h)
                mx[k]+=max(c*newlo,c*newhi)-max(c*l,c*h)
                if k not in queued:queue.append(k);queued.add(k)
    return receipt('integer_box_consistent')


def reduced(system,result):
    require(result['outcome']=='integer_box_consistent','cannot reduce inconsistent bounds')
    lo=result['lower_bounds'];hi=result['upper_bounds'];keep=[j for j in range(len(lo))if lo[j]!=hi[j]]
    b=tuple(value-sum(lo[j]*col[i]for j,col in enumerate(system.columns)if lo[j])for i,value in enumerate(system.rhs))
    cols=tuple(system.columns[j]for j in keep);bounds=tuple(hi[j]-lo[j]for j in keep)
    # All free variables have been shifted by their propagated lower bound.
    meta={'kind':'integer_box_reduced_system','source_metadata':system.metadata,'bounds_result_sha256':st.digest(result),'retained_indices':keep}
    return replace(system,columns=cols,rhs=b,bounds=bounds,column_labels=tuple(system.column_labels[j]for j in keep),metadata=meta)


def lift(system,result,values):
    keep=[j for j,(l,h)in enumerate(zip(result['lower_bounds'],result['upper_bounds']))if l!=h]
    require(len(values)==len(keep),'reduced integer vector length mismatch')
    out=list(result['lower_bounds'])
    for j,v in zip(keep,values):out[j]+=v
    return out


def verify(system,result):
    require(propagate(system)==result,'integer bound-propagation receipt differs')
    return True
