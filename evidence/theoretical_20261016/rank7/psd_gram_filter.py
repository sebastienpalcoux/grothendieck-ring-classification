"""Exact necessary rank-one PSD filter for a nonnegative Gram decomposition."""
import math
import sympy as s

def install(module):
 original=module.gram_columns
 cache={}
 def filtered(Q,dims,target,K,degree):
  key=(Q.rows,tuple(Q));n=Q.rows
  if key not in cache:
   if Q!=Q.T:raise RuntimeError('Nonsymmetric Gram matrix')
   piv=list(Q.rref()[1]);P=Q.extract(piv,piv)
   # A PSD matrix restricts positively to any independent principal block.
   if not piv or any(P[:i,:i].det()<=0 for i in range(1,len(piv)+1)):
    cache[key]=None
   else:
    inv=P.inv();C=Q.extract(range(n),piv)
    if C*inv*C.T!=Q:raise RuntimeError('Principal block does not reconstruct Gram matrix')
    projection=C*inv
    dp=math.lcm(*(int(z.q) for z in projection));di=math.lcm(*(int(z.q) for z in inv))
    pn=[[int(z*dp) for z in row] for row in projection.tolist()]
    an=[[int(z*di) for z in row] for row in inv.tolist()]
    cache[key]=(piv,pn,an,dp,di)
  data=cache[key]
  if data is None:return []
  piv,pn,an,dp,di=data;out=[]
  for v in original(Q,dims,target,K,degree):
   w=[v[i] for i in piv]
   if any(sum(a*b for a,b in zip(row,w))!=dp*v[i] for i,row in enumerate(pn)):continue
   if sum(w[i]*a*b for i,row in enumerate(an) for a,b in zip(row,w))<=di:out.append(v)
  return out
 module.gram_columns=filtered
