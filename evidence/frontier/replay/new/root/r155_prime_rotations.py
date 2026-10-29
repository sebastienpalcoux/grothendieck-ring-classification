"""Generalized prime-order spectra for forced rank26 datum; exact integer arithmetic."""
from pathlib import Path
import runpy,json,time,hashlib
import sympy as sp
import numpy as np
P=Path(__file__).parent; ns=runpy.run_path(str(P/'r155_cubic.py'))
N,t,r,trace,J=map(ns.get,('N','t','r','trace','J'))
def cycloroots(L):
 x=sp.Symbol('x'); pol=sp.Poly(sp.cyclotomic_poly(L,x),x);deg=pol.degree();cc=[int(pol.nth(i)) for i in range(deg)];out=[]
 for e in range(L):
  a=[0]*(max(e,deg)+1);a[e]=1
  for k in range(len(a)-1,deg-1,-1):
   v=a[k]
   if v:
    for i,c in enumerate(cc):a[k-deg+i]-=c*v
    a[k]=0
  out.append(a[:deg])
 return np.array(out,dtype=np.int64)
rows=[];fail=[];start=time.time()
for p in (5,7):
 L=24*p;roots=cycloroots(L);degree=roots.shape[1];basis=sp.Matrix(np.array([roots[24*s] for s in range(p-1)]).T.tolist());pivots=list(basis.T.rref()[1]);inv=sp.Matrix([list(basis.row(i)) for i in pivots]).inv();assert all(v.q==1 for v in inv);inv=np.array(inv.tolist(),dtype=np.int64)
 G=trace(p)
 for k in range(r):
  power=np.zeros(r,dtype=np.int64);power[k]=1
  for _ in range(p-1):power=power@N[:,k,:]
  H=np.einsum('ijx,x->ij',N,power)
  for i in range(r):
   for j in range(r):
    v=sum((G[k,i,j,q]*roots[(p*q+int(t[i])-int(t[j]))%L] for q in range(8)),np.zeros(degree,dtype=np.int64))
    c=inv@v[pivots];ok=np.array_equal(np.array(basis.tolist(),dtype=np.int64)@c,v)
    h=int(H[i,j]);base=576*h-int(sum(c));nums=[base+p*int(a) for a in c]+[base]
    ok=ok and all(a>=0 and a%(576*p)==0 for a in nums)
    if ok:rows.append([p,k,i,j,h]+[a//(576*p) for a in nums])
    else:fail.append({'p':p,'base':k,'target':[i,j],'hom_dim':h,'trace':v.tolist(),'nums':nums})
 out={'scope':'necessary prime rotation spectra, not realizability','orders':[5,7],'blocks':len(rows)+len(fail),'failures':fail,'elapsed_seconds':time.time()-start,'rows':rows}
(P/'r155_prime_rotations_receipt.json').write_text(json.dumps(out,separators=(',',':'))+'\n');print(json.dumps({k:v for k,v in out.items() if k!='rows'},indent=2))
