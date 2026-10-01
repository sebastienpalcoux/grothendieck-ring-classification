"""Rank-independent exact Gram vectors, reducing first to the rational range."""
import itertools,math,subprocess,os
from functools import lru_cache
from pathlib import Path
import sympy as s
from exact import require
BUILD_DIRECTORY = None

@lru_cache(maxsize=256)
def _native(n,entries):
    Q=s.Matrix(n,n,entries);r=Q.rank()
    if r==0:return ()
    ix=next(I for I in itertools.combinations(range(n),r) if Q.extract(I,I).det()!=0);S=Q.extract(ix,ix);adj=S.adjugate();det=int(S.det());M=Q.extract(range(n),ix)*adj
    require(det>0,'Gram principal minor is not positive')
    vals=list(entries)+list(ix)+list(map(int,adj))+[det]+list(map(int,M))
    vmax=max(math.isqrt(int(Q[i,i])) for i in range(n));amax=max(abs(int(x)) for x in adj);mmax=max(abs(int(x)) for x in M)
    require(max(abs(v) for v in vals)<2**60 and r*r*amax*vmax*vmax<2**120 and r*mmax*vmax<2**120,'Gram native exact integer range exceeded')
    src=Path(__file__).with_suffix('.cpp')
    require(BUILD_DIRECTORY is not None, 'native temporary build directory not configured')
    BUILD_DIRECTORY.mkdir(parents=True, exist_ok=True)
    exe=BUILD_DIRECTORY/'gram_vectors_general'
    if not exe.exists() or not os.access(exe, os.X_OK):
        tmp=exe.with_name(exe.name+'_'+str(os.getpid()));subprocess.run(['g++','-O3','-std=c++17',str(src),'-o',str(tmp)],check=True,capture_output=True);os.replace(tmp,exe)
    run=subprocess.run([str(exe)],input=' '.join(map(str,[n,r]+vals)),text=True,capture_output=True,check=True,timeout=60)
    out=sorted(tuple(map(int,line.split())) for line in run.stdout.splitlines());require(len(out)==len(set(out)),'duplicate Gram vector')
    return tuple(out)
def native(Q):return _native(Q.rows,tuple(map(int,Q)))
