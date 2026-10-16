import sys,json,itertools,math,time
from pathlib import Path
import numpy as np
import sympy as s

from involution_module import invs
from rings import dual

def candidates(R,g,fix):
 n=len(R);f=len(fix);du=dual(R);eye=np.eye(f,dtype=object);sets={}
 for i in range(n):
  if i in sets:continue
  if i==0:sets[i]=eye[None];continue
  ix=[(a,b) for a in range(f) for b in range(f) if du[i]!=i or a<=b]
  vals=[range(-R[i][fix[a]][fix[b]],R[i][fix[a]][fix[b]]+1,2) for a,b in ix]
  count=math.prod(len(v) for v in vals)
  if count>2000000:raise RuntimeError(('large',i,count))
  arr=np.zeros((count,f,f),dtype=object)
  for z,vec in enumerate(itertools.product(*vals)):
   for (a,b),c in zip(ix,vec):
    arr[z,a,b]=c
    if du[i]==i:arr[z,b,a]=c
  if du[i]!=i:arr=arr[np.all(arr@arr.transpose(0,2,1)==arr.transpose(0,2,1)@arr,axis=(1,2))]
  coeff=[int(c) for c in s.Poly(s.Matrix(R[i]).charpoly().as_expr()).sqf_part().all_coeffs()]
  ev=np.zeros_like(arr)
  for c in coeff:ev=ev@arr+c*eye
  arr=arr[np.all(ev==0,axis=(1,2))]
  sets[i]=arr
  if du[i]!=i:sets[du[i]]=arr.transpose(0,2,1)
 return sets

def solve(R,g,fix,cap=100000):
 n=len(R);f=len(fix);du=dual(R);sets=candidates(R,g,fix)

 # Cache every pair multiplication table feasibility as early constraints.
 reps=[];nodes=0
 def rec(given):
  nonlocal nodes
  nodes+=1
  # Exact relations whose RHS now available, and commutativity.
  for i in given:
   for j in given:
    if j<i:continue
    if not np.array_equal(given[i]@given[j],given[j]@given[i]):return
    support=[k for k in range(n) if R[i][j][k]]
    if all(k in given for k in support):
     rhs=sum((R[i][j][k]*given[k] for k in support),np.zeros((f,f),dtype=object))
     if not np.array_equal(given[i]@given[j],rhs):return
  if len(given)==n:
   reps.append([given[i].tolist() for i in range(n)]);return
  # Propagate one unknown multiplication RHS, and direct duality.
  for i in given:
   for j in given:
    if j<i:continue
    missing=[k for k in range(n) if R[i][j][k] and k not in given]
    if len(missing)==1:
     k=missing[0];v=given[i]@given[j]-sum((R[i][j][a]*given[a] for a in given),np.zeros((f,f),dtype=object));q=R[i][j][k]
     if np.any(v%q):return
     v=v//q
     if not any(np.array_equal(v,z) for z in sets[k]):return
     nxt=dict(given);nxt[k]=v
     if du[k] in given and not np.array_equal(v.T,given[du[k]]):return
     nxt[du[k]]=v.T
     rec(nxt);return
  remaining=[i for i in range(n) if i not in given]
  options=[]
  for i in remaining:
   allowed=[v for v in sets[i] if all(np.array_equal(v@z,z@v) for z in given.values())]
   options.append((len(allowed),i,allowed))
  _,i,allowed=min(options,key=lambda z:(z[0],z[1]))
  for v in allowed:
   nxt=dict(given);nxt[i]=v;nxt[du[i]]=v.T;rec(nxt)
 rec({0:np.eye(f,dtype=object)})
 # Gauge by diagonal signs.
 out={}
 for rr in reps:
  keys=[]
  for signs in itertools.product((-1,1),repeat=f):
   S=np.diag(signs);keys.append(tuple(tuple((S@np.array(M)@S).ravel()) for M in rr))
  key=min(keys);out[key]=[[list(key[i][a*f:(a+1)*f]) for a in range(f)] for i in range(n)]
 return dict(fixed=fix,involution=g,domains={i:len(v) for i,v in sets.items()},nodes=nodes,representations=list(out.values()))

