"""Portable exact support for accepted structural certificate replays."""
from pathlib import Path
import gzip, hashlib, json, os
import sympy as s

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]

def require(ok, message='exact certificate condition failed'):
    if not ok:
        raise ValueError(message)

def sha(R):
    return hashlib.sha256(json.dumps(R, separators=(',', ':')).encode()).hexdigest()

def load():
    source = Path(os.environ.get('RANK11_SOURCE', str(ROOT/'repositories/fusion-ring-census/results/rank11/tables.txt.gz')))
    with gzip.open(source, 'rt') as f:
        lines = f.read().splitlines()
    require(len(lines) == 182, 'expected 182 physical input lines')
    rows = []
    for i,line in enumerate(lines,1):
        R = json.loads(line.replace('{','[').replace('}',']'))
        require(len(R) == 11 and all(len(A) == 11 and all(len(B) == 11 for B in A) for A in R), 'rank eleven shape')
        require(all(type(v) is int and v in (0,1) for A in R for B in A for v in B), 'multiplicity one input')
        rows.append(dict(id=f'R11_1_{i}', tensor=R, tensor_sha256=sha(R)))
    return rows


def generated_basis(R,seed):
 n=len(R);p=1000003;echelon={};words=[];rows=[]
 def add(v,word):
  w=[int(x)%p for x in v]
  for k,row in sorted(echelon.items()):
   if w[k]:
    a=w[k];w=[(x-a*y)%p for x,y in zip(w,row)]
  k=next((k for k,x in enumerate(w)if x),None)
  if k is None:return False
  z=pow(w[k],-1,p);echelon[k]=[(x*z)%p for x in w];words.append(word);rows.append(tuple(v));return True
 add([1]+[0]*(n-1),())
 at=0
 while at<len(rows):
  for j in seed:
   v=tuple(sum(rows[at][a]*R[a][j][b]for a in range(n))for b in range(n))
   add(v,words[at]+(j,))
   if len(rows)==n:
    V=s.Matrix(rows);W=V.inv()
    if V*W!=s.eye(n):raise ValueError('bad exact inverse')
    return words,W
  at+=1
 return None
