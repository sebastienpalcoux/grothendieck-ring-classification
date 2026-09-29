"""Discovery of exact branch/Farkas certificates for integer-count systems."""
import numpy as np
from scipy.optimize import linprog
from fractions import Fraction
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'software'))
from higher_traces import farkas,check_farkas
from exact import require

def cut(A,b,j,k,left):
 return [row+[0] for row in A]+[[int(i==j) for i in range(len(A[0]))]+[1 if left else -1]],b+[k]

def discover(A,b,integer,node_limit=80):
 nodes=0
 def visit(A,b,depth):
  nonlocal nodes
  nodes+=1;require(nodes<=node_limit,'branch budget exhausted')
  aa=np.array(A,dtype=float);bb=np.array(b,dtype=float);scale=np.maximum(1,np.maximum(abs(aa).max(axis=1),abs(bb)));sol=linprog(np.zeros(len(A[0])),A_eq=aa/scale[:,None],b_eq=bb/scale,bounds=(0,None),options={'time_limit':30},method='highs')
  print('node',nodes,'depth',depth,'LP',sol.status,flush=True)
  if sol.status==2:
   y=farkas(A,b);require(y is not None,'exact dual reconstruction failed');check_farkas(A,b,y);return {'ray':y}
  require(sol.status==0,'LP incomplete');frac=[(abs(sol.x[j]-round(sol.x[j])),j) for j in integer];gap,j=max(frac)
  require(gap>1e-6,'apparently integral primal; not excluded');k=int(np.floor(sol.x[j]));print('split',j,k,'value',sol.x[j],flush=True)
  return {'split':j,'floor':k,'left':visit(*cut(A,b,j,k,True),depth+1),'right':visit(*cut(A,b,j,k+1,False),depth+1)}
 tree=visit(A,b,0);return dict(nodes=nodes,tree=tree)

def verify(A,b,integer,record):
 nodes=0
 def visit(A,b,c):
  nonlocal nodes
  nodes+=1
  if 'ray' in c:check_farkas(A,b,c['ray']);return
  j=c['split'];k=c['floor'];require(type(j) is int and j in integer and type(k) is int,'invalid integer split');visit(*cut(A,b,j,k,True),c['left']);visit(*cut(A,b,j,k+1,False),c['right'])
 visit(A,b,record['tree']);require(nodes==record['nodes'],'wrong tree node count');return nodes
