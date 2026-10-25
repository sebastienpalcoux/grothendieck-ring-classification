"""Complete exact Gram-vector enumeration through rank eight.

Reduce to a nonsingular principal coordinate subspace, then enumerate its
ellipsoid using exact prefix principal-minor tests. Singular coordinates
are reconstructed by the rational range map. Every native arithmetic bound
is checked before invocation. The zero vector is excluded, as in the frozen
rank-independent implementation.
"""
from pathlib import Path
from native_build import ensure_native
import functools,math,os,subprocess,sys
import sympy as s
from fractions import Fraction as F
HERE=Path(__file__).resolve().parent
_FROZEN_HIGH_COLUMNS=None
def require(p,msg):
 if not p:raise ValueError(msg)
def executable():
 source=HERE/'gram_vectors_rank8.cpp';exe=source.with_suffix('')
 ensure_native(source,exe,flags=('-O3', '-std=c++17'))
 return exe
def principal_coordinates(Q):
 """Return a positive definite principal coordinate set, or None if not PSD."""
 n=Q.rows;order=sorted(range(n),key=lambda i:(Q[i,i],i));A=Q.extract(order,order);ix=[];previous=s.Integer(1)
 for p in range(n):
  pivot=A[p,p]
  if pivot<0:return None
  if pivot==0:
   if any(A[p,j]!=0 for j in range(p+1,n)):return None
   continue
  ix.append(order[p])
  for i in range(p+1,n):
   for j in range(i,n):
    z=(pivot*A[i,j]-A[i,p]*A[p,j])/previous
    require(z.q==1,'nonexact fraction-free Gram elimination');A[i,j]=A[j,i]=z
  previous=pivot
 return ix
@functools.lru_cache(maxsize=256)
def _cached(n,entries):
 Q=s.Matrix(n,n,entries);require(1<=n<=8 and Q==Q.T,'Gram shape/symmetry')
 if any(x<0 for x in entries):return ()
 ix=principal_coordinates(Q)
 if not ix:return ()
 r=len(ix);bounds=[math.isqrt(int(Q[i,i]))for i in range(n)];vmax=max(bounds)
 vals=[n,r]+list(entries)+ix+bounds;prefix=[]
 for m in range(1,r+1):
  S=Q.extract(ix[:m],ix[:m]);det=int(S.det());adj=S.adjugate();require(det>0,'nonpositive principal Gram determinant')
  amax=max(map(abs,map(int,adj)))
  require(m*m*amax*vmax*vmax<2**120,'Gram quadratic arithmetic bound exceeded')
  vals.extend([det]+list(map(int,adj)));prefix.append((det,adj))
 det,adj=prefix[-1];M=Q.extract(range(n),ix)*adj
 require(r*max(map(abs,map(int,M)))*vmax<2**120,'Gram range arithmetic bound exceeded')
 vals.extend(map(int,M));require(max(map(abs,vals))<2**60,'Gram input integer range exceeded')
 run=subprocess.run([str(executable())],input=' '.join(map(str,vals)),text=True,capture_output=True,check=True,timeout=300)
 out=sorted(tuple(map(int,line.split()))for line in run.stdout.splitlines())
 require(all(len(v)==n for v in out)and len(out)==len(set(out)),'invalid/duplicate Gram vector')
 return tuple(out)
def native(Q):
 require(Q.rows==Q.cols and all(x==int(x)for x in Q),'nonintegral/square Gram input')
 return _cached(Q.rows,tuple(map(int,Q)))
def high_columns(data,L):
 """Frozen rational/quadratic arithmetic filter after native Gram enumeration."""
 if os.environ.get('RANK6_REFERENCE_GRAM') and _FROZEN_HIGH_COLUMNS is not None:return _FROZEN_HIGH_COLUMNS(data,L)
 n=data['ch'].n;q=data['q'];d=data['dimensions'];D=data['global_dimension'];Q=(data['ch'].C-L*L.T).extract(range(1,n),range(1,n));out=[]
 denominator=math.lcm(*(x.denominator for pair in d for x in pair));dimensions=[[int(x*denominator)for x in pair]for pair in d]
 for v in native(Q):
  z=tuple(F(sum(v[i]*dimensions[i+1][j]for i in range(n-1)),denominator)for j in range(2));norm=z[0]**2-q*z[1]**2
  if not norm:continue
  quotient=((D[0]*z[0]-q*D[1]*z[1])/norm,(D[1]*z[0]-D[0]*z[1])/norm)
  if (2*quotient[0]).denominator!=1 or (quotient[0]**2-q*quotient[1]**2).denominator!=1:continue
  if z[1] and ((2*z[0])**2/norm).denominator!=1:continue
  out.append((v,z))
 return Q,out
def install():
 global _FROZEN_HIGH_COLUMNS
 import gram_vectors_general,higher_traces
 old=gram_vectors_general.native
 if old is not native:
  for module in tuple(sys.modules.values()):
   if module is not None and getattr(module,'native',None) is old:setattr(module,'native',native)
 gram_vectors_general.native=native
 oldhigh=higher_traces.high_columns
 if oldhigh is not high_columns:
  if _FROZEN_HIGH_COLUMNS is None:_FROZEN_HIGH_COLUMNS=oldhigh
  for module in tuple(sys.modules.values()):
   if module is not None and getattr(module,'high_columns',None) is oldhigh:setattr(module,'high_columns',high_columns)
 higher_traces.high_columns=high_columns
