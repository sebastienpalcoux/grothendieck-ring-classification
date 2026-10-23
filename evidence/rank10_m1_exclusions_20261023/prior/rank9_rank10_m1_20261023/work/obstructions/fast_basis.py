"""Find an exact algebra basis using a modular discovery accelerator.

A full modular rank proves rational independence. Modular failure produces no
mathematical conclusion. Returned coordinates are checked over QQ.
"""
import sympy as s

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
