"""Exact bounded Gram vectors, with an independently checkable native backend."""
import math, subprocess, tempfile, os
from pathlib import Path
from functools import lru_cache
import sympy as s
from exact import require
_TEMP=None

@lru_cache(maxsize=256)
def _native(entries):
    global _TEMP
    M=s.Matrix(4,4,entries);adj=M.adjugate();det=int(M.det())
    require(all(M[:j,:j].det()>0 for j in range(1,5)),'positive-definite Gram matrix required')
    vmax=max(math.isqrt(int(M[i,i])) for i in range(4));amax=max(abs(int(x)) for x in adj)
    require(max(abs(int(x)) for x in M)<2**60 and amax<2**60 and 0<det<2**60,'native Gram input range')
    require(16*amax*vmax*vmax<2**120,'native Gram accumulator range')
    if _TEMP is None:
        _TEMP=tempfile.TemporaryDirectory();exe=Path(_TEMP.name)/'gram_vectors'
        subprocess.run(['g++','-O3','-std=c++17',str(Path(__file__).with_suffix('.cpp')),'-o',str(exe)],check=True,capture_output=True)
    values=list(entries)+list(map(int,adj))+[det]
    run=subprocess.run([str(Path(_TEMP.name)/'gram_vectors')],input=' '.join(map(str,values)),text=True,capture_output=True,check=True)
    vectors=[tuple(map(int,line.split())) for line in run.stdout.splitlines()]
    require(vectors==sorted(set(vectors)),'native vector order or duplication')
    for v in vectors:
        require(len(v)==4 and any(v) and min(v)>=0,'native vector shape')
        require(all(v[i]*v[j]<=M[i,j] for i in range(4) for j in range(i,4)),'native Gram entry bound')
        require(sum(v[i]*int(adj[i,j])*v[j] for i in range(4) for j in range(4))<=det,'native rank-one bound')
    return tuple(vectors)

def native(M):return _native(tuple(map(int,M)))
