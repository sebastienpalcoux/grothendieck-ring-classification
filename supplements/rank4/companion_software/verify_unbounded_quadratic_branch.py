#!/usr/bin/env python3
"""Exact algebra behind the unrestricted Q x Q x quadratic reduction."""
from pathlib import Path
import json
import sympy as s
from signed_tables_bounded import matrices
D,w,z,S=s.symbols('D w z S')
h=D**2*w
E=D*(1-3*w)+(1-w)*S+4*w-2/D
assert s.expand((D**2-h)*(D**2+D*S-2*h)-2*(D-h)**2-D**3*E)==0
assert s.expand(-z*z/s.Integer(8)+s.Rational(49,6)+s.Rational(7,6)*z+(z-14)*(3*z+14)/24)==0
assert s.expand(E.subs(w,s.Rational(3,8)-2/D)-(-D/8+s.Rational(15,2)+(s.Rational(5,8)+2/D)*S-10/D))==0
v=s.symbols('v')
assert s.expand(s.Rational(1,4)+v*v+(s.Rational(1,2)-v)**2-(s.Rational(3,8)+2*(v-s.Rational(1,4))**2))==0
# The two codegree-three characters give a one-parameter linear family.
a,b,c,d,e,f,g,h,i,j=s.symbols('a b c d e f g h i j')
p=(a,b,c,d,e,f,g,h,i,j);M=matrices(p)
chi=((1,0,1,-1),(1,1,-1,0));eq=[]
for row in chi:
 for u in range(1,4):
  for v in range(u,4):eq.append(sum(M[u][v,k]*row[k] for k in range(4))-row[u]*row[v])
assert s.linsolve(eq,p)==s.FiniteSet((j-2,j-2,j-1,j-1,j-1,j-1,j-1,j-1,j,j))
# Primitive elements certify exactly which positive self-dual rings have type(1,1,2).
root=Path(__file__).resolve().parent
with (root.parent/'data/models.json').open() as source:
 models=json.load(source)
assert len({model['model'] for model in models})==len(models)
q=s.symbols('q')
found=set()
quadratic_products=set()
expected={
 'Rep_D10':(q-13)*(q+1)*(q*q+4*q-1),
 'PSU2_6':(q-1)*(q+3)*(q*q-14*q-23),
 'even_part_2D2':(q-1)*(q+3)*(q*q-26*q-11),
 'Haagerup_H1':(q+1)*(q+2)*(q*q-27*q+23),
}
for model in models:
 identity=model['model']
 M=[s.Matrix(a) for a in model['matrices']]
 if not all(M[k][k,0]==1 for k in range(4)):continue
 A=M[1]+2*M[2]+4*M[3];P=A.charpoly(q).as_expr()
 assert s.discriminant(P,q)!=0
 degrees=sorted(s.degree(f,q) for f,m in s.factor_list(P)[1] for _ in range(m))
 if degrees==[2,2]: quadratic_products.add(identity)
 if degrees==[1,1,2]:
  found.add(identity)
  assert s.expand(P-expected[identity])==0
assert found==set(expected)
assert quadratic_products=={'Fib_times_Vec_C2','Fib_times_Fib'}
print('PASS: exact moment algebra, D=196 cutoff factorization, R_n character reduction, and four positive algebra types.')
