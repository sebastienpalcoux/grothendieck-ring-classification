"""Exact rank-eight low-induction frames; additive native acceleration.

The complete meet-in-the-middle output equals frozen induction.low_matrices
with gram_prune=False. With Gram pruning, entrywise nonnegativity and exact
positive semidefiniteness are additionally required. No numerical decision.
"""
from pathlib import Path
import functools,math,os,subprocess,sys
import sympy as s
HERE=Path(__file__).resolve().parent
def require(p,msg):
 if not p:raise ValueError(msg)
def executable():
 source=HERE/'low_frames_rank8.cpp';exe=source.with_suffix('')
 if not exe.exists() or not os.access(exe,os.X_OK) or exe.stat().st_mtime_ns<source.stat().st_mtime_ns:
  tmp=exe.with_name(exe.name+'_'+str(os.getpid()))
  subprocess.run(['g++','-O3','-std=c++17',str(source),'-o',str(tmp)],check=True,capture_output=True);os.replace(tmp,exe)
 return exe
@functools.lru_cache(maxsize=8)
def _cached(sets,n,entries,prune):
 B=s.Matrix(n,n,entries);unit=(1,)+(0,)*(n-1)
 require(B==B.T and 2<=n<=8 and len(sets)==n-1,'low-frame shape/symmetry')
 require(all(x>=0 and x<=10**6 for x in entries),'low-frame integer bound')
 require(B[0,0]==n,'low-frame unit row')
 if prune:
  # Every Bareiss entry is a minor, bounded by m! max(B)^m. Each
  # numerator is a difference of two products; denominators are >=1.
  d=n-1;bound=math.factorial(max(0,d-1))*max(1,max(entries))**max(0,d-1)
  require(2*bound*bound<2**120,'exact low-frame PSD arithmetic bound exceeded')
 if not sets or any(not cs for cs in sets):return ()
 require(all(list(cs)==sorted(set(cs)) for cs in sets),'column sets must be sorted and distinct')
 require(all(len(c)==n and c[0]==1 and all(isinstance(x,int) and 0<=x<=10**6 for x in c) for cs in sets for c in cs),'low-frame column')
 values=[n-1,len(sets),int(prune)]+[int(B[0,i]) for i in range(1,n)]+[int(B[i,j]) for i in range(1,n) for j in range(1,n)]
 for cs in sets:values.extend([len(cs)]+[x for c in cs for x in c[1:]])
 result=subprocess.run([str(executable())],input=' '.join(map(str,values)),capture_output=True,text=True,check=True,timeout=300)
 out=[]
 for line in result.stdout.splitlines():
  ix=list(map(int,line.split()));require(len(ix)==len(sets),'native output shape')
  out.append((unit,)+tuple(sets[i][j] for i,j in enumerate(ix)))
 out.sort();require(len(out)==len(set(out)),'duplicate low frame')
 return tuple(out)
def low_matrices(column_sets,B,gram_prune=False):
 entries=tuple(B);require(all(x==int(x) for x in entries),'nonintegral Gram input')
 require(all(x==int(x) for cs in column_sets for c in cs for x in c),'nonintegral restriction column')
 return list(_cached(tuple(tuple(tuple(map(int,c))for c in cs)for cs in column_sets),B.rows,tuple(map(int,entries)),bool(gram_prune)))
native=low_matrices
def install():
 import induction
 old=induction.low_matrices
 if old is low_matrices:return
 # Modules using "from induction import *" retain their own binding.
 for module in tuple(sys.modules.values()):
  if module is not None and getattr(module,'low_matrices',None) is old:setattr(module,'low_matrices',low_matrices)
 induction.low_matrices=low_matrices
