"""Dimension-order obstruction for spherical characters.

The proof input is dim(I(1)_chi)=delta/f_chi.  Forgetting to the category
places this dimension in the Z-span of the simple categorical dimensions.
No positivity, tensor label or floating-point arithmetic is used.
"""
import math
import sympy as s
from sympy.matrices.normalforms import hermite_normal_form
from exact import require,poly,vector,evaluate,discover_roots,pc

def lattice(ds,K):
 degree=K.mod.degree();V=s.Matrix.hstack(*(vector(d,degree) for d in ds))
 den=math.lcm(*(int(x.q) for x in V))
 H=hermite_normal_form(s.Matrix(V.rows,V.cols,lambda i,j:int(V[i,j]*den)))
 require(H.shape==(degree,degree),'simple dimensions do not span the character field')
 return den,H

def certificate(a,f):
 K,ds,D,pD=a.component(f); den,H=lattice(ds,K); inverse=H.inv()*den
 for p,m in a.cf:
  roots=discover_roots(p,K)
  if roots is None:continue
  for root in roots:
   if not root:continue
   coords=inverse*vector(D/root,f.degree())
   for j,x in enumerate(coords):
    if x.q!=1:
     return {'kind':'dimension_order','polynomial':pc(p),'root':[str(x) for x in root.to_list()],
       'coordinate':j,'functional':[str(x) for x in inverse[j,:]],'value':str(x),
       'lattice_denominator':den,'hermite_basis':[[str(x) for x in row] for row in H.tolist()]}
 return None

def verify(a,f,c):
 require(c['kind']=='dimension_order','wrong dimension-order certificate kind')
 K,ds,D,pD=a.component(f);p=poly(c['polynomial'])
 require(any(p==g for g,m in a.cf),'polynomial is not a formal-codegree factor')
 root=K([s.Rational(x) for x in c['root']]);require(root and evaluate(p.all_coeffs(),root,K)==K.zero,'not a nonzero codegree root')
 den,H=lattice(ds,K);j=c['coordinate'];require(type(j) is int and 0<=j<f.degree(),'invalid lattice coordinate')
 functional=H.inv()[j,:]*den
 require(c['lattice_denominator']==den and c['hermite_basis']==[[str(x) for x in row] for row in H.tolist()],'wrong dimension lattice')
 require(c['functional']==[str(x) for x in functional],'incorrect separating functional')
 require(all((functional*vector(d,f.degree()))[0].q==1 for d in ds),'functional not integral on the dimension order')
 value=(functional*vector(D/root,f.degree()))[0]
 require(str(value)==c['value'] and value.q!=1,'dimension quotient lies in the order or witness is incorrect')
