"""Exact small-field acceleration for full-character center spectra.

Values are pulled back from an ambient cyclotomic field to the FP field only
when the complete reconstruction equality succeeds. The integrality test
is unchanged: its multiplication characteristic polynomial is integral.
"""
import sympy as s
from spectral_induction import Spectrum
from cyclotomic_stabilizer_trace import integral_charpoly
from exact import vector,require

class SmallFieldSpectrum(Spectrum):
 def __init__(self,table,cols,high,data):
  self._small_data=data;C=table.K;e=C.mod.degree();r=data['K'].mod.degree();DD=data['DD'];D=data['D'];B=s.Matrix.hstack(*(vector(DD**j,e) for j in range(r)))
  _,pivots=B.T.rref();self._pull_rows=pivots;self._pull_inv=B.extract(pivots,range(r)).inv();self._pull_basis=B
  self._small_powers=[D**j for j in range(r)];self._ambient_e=e
  super().__init__(table,cols,high)
 def integral(self,x):
  if x in self._integer:return self._integer[x]
  v=vector(x,self._ambient_e);co=self._pull_inv*v.extract(self._pull_rows,[0])
  if self._pull_basis*co==v:
   K=self._small_data['K'];z=sum((K(co[j])*y for j,y in enumerate(self._small_powers)),K.zero)
   yes=integral_charpoly(z,K) is not None
  else:yes=super().integral(x)
  self._integer[x]=yes;return yes

def half_e6_subrings(R):
 n=len(R);out=[]
 for g in range(1,n):
  if R[g][g]!=[int(k==0)for k in range(n)]:continue
  for x in range(1,n):
   if x==g:continue
   if R[g][x]!=[int(k==x)for k in range(n)] or R[x][g]!=R[g][x]:continue
   if R[x][x]==[int(k==0)+int(k==g)+2*int(k==x)for k in range(n)]:out.append((g,x))
 return out

def half_e6_high_allowed(data,v,ti,g,x,conjugate):
 C=data['C'];F=data['F'];ph=data['phases'][ti];a=v[g-1];b=v[x-1]
 if not a and not b:return True
 if a:return a>=b and all(ph[k-1]==C((-1)**k)for k in range(1,len(ph)+1))
 exps=[-3,5,2,-4]
 if conjugate:exps=[-e for e in exps]
 return ph in {tuple(C.unit**((F//12)*e*k%F)for k in range(1,len(ph)+1))for e in exps}

def half_e6_low_allowed(cols,g,x):
 # Twist-one columns 1, U=1+x, W=1+g+x.
 return all(0<=c[g]<=c[x]<=c[0] for c in cols)

def cyclic_three_subrings(R):
 n=len(R);out=[]
 for g in range(1,n):
  row=R[g][g]
  if sum(row)!=1:continue
  h=row.index(1)
  if h in [0,g]or g>h:continue
  if R[g][h]==R[h][g]==[int(i==0)for i in range(n)] and R[h][h]==[int(i==g)for i in range(n)]:out.append((g,h))
 return out

def cyclic_three_allowed(data,v,ti,g,h,s):
 if not v[g-1]and not v[h-1]:return True
 C=data['C'];F=data['F'];ph=data['phases'][ti];height=len(ph)
 if s==0:
  return ph in {tuple(C.unit**((F//3)*a*k%F)for k in range(1,height+1))for a in range(3)}
 from round3_m4 import relative_root
 return ph==tuple(relative_root(C,F,9,s*k)for k in range(1,height+1))

def coupled_balance_cached(data,spec,cols,labels,nv):
 """Identical equations/order to round3_m4.coupled_balance; cached automorphisms."""
 from collections import Counter,defaultdict
 from exact import evaluate
 import math
 C=data['C'];F=data['F'];types=data['phases'];idx=dict(zip(spec.vectors,spec.types));type_index={t:i for i,t in enumerate(types)}
 one=type_index[tuple(C.one for _ in types[0])];low=Counter((idx[tuple(c)],one)for c in cols);positions=defaultdict(list)
 for j,(v,ti)in enumerate(labels):positions[idx[(0,)+v],ti].append(j)
 allpairs=set(positions)|set(low);seen=set();rows=[];rhs=[];ordered=sorted(allpairs,key=str);joint_types={t for t,ti in allpairs}
 for a in range(F):
  if math.gcd(a,F)>1:continue
  z=C.unit**a;zz=C.unit**(a*a%F);pm={j:type_index[tuple(evaluate(v.to_list(),zz,C)for v in ty)]for j,ty in enumerate(types)}
  images={t:tuple(evaluate(v.to_list(),z,C)for v in t)for t in joint_types}
  for typ,ti in ordered:
   tt=images[typ];tj=pm[ti]
   if(typ,ti)==(tt,tj):continue
   pair=tuple(sorted(((str(typ),ti),(str(tt),tj))))
   if pair in seen:continue
   seen.add(pair);row=[0]*nv
   for j in positions[typ,ti]:row[j]+=1
   for j in positions[tt,tj]:row[j]-=1
   b=low[tt,tj]-low[typ,ti]
   if any(row)or b:rows.append(row);rhs.append(b)
 return rows,rhs
