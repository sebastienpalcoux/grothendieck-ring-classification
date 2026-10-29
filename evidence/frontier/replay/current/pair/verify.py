#!/usr/bin/env python3
"""Small exact checks for pair REPORT.md; no categorical premise is inferred."""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import importlib.util
import json

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('tensors',ROOT/'current_remaining_cases.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

# Basis index bits: r=sqrt(2), s=sqrt(3), c=sqrt(2+r).
def e(i=0,a=1):
    x=[F(0)]*8;x[i]=F(a);return tuple(x)
def add(x,y):return tuple(a+b for a,b in zip(x,y))
def scale(x,a):return tuple(F(a)*b for b in x)
def mul(x,y):
    z=[F(0)]*8
    for i,a in enumerate(x):
      for j,b in enumerate(y):
        if not a or not b:continue
        factor=a*b*(2 if i&j&1 else 1)*(3 if i&j&2 else 1)
        k=i^j
        if i&j&4:
            z[k]+=2*factor
            z[k^1]+=factor*(2 if k&1 else 1)
        else:z[k]+=factor
    return tuple(z)
def sq(x):return mul(x,x)
def summ(xs):
    z=e(0,0)
    for x in xs:z=add(z,x)
    return z
def nonnegative(x):return all(a>=0 for a in x)
one,r,s,rs,c=[e(i) for i in (0,1,2,3,4)]
d=summ([scale(one,3),scale(r,2),scale(s,2),rs])
a=summ([scale(one,2),r,s,rs]);b=add(a,r)
D=scale(add(one,sq(d)),4)
assert D==(144,96,80,56,0,0,0,0)
checks={}

for key, dims in [
 ('R6_8_1660',[one,one,d,d,r,mul(r,d)]),
 ('R8_3_941',[one,b,b,one,a,a,d,d])]:
    N=m.TENSORS[key]
    sha=hashlib.sha256(json.dumps(N,separators=(',',':')).encode()).hexdigest()
    assert sha==m.METADATA[key]['tensor_sha256'],(key,sha)
    for i in range(len(N)):
      for j in range(len(N)):
        assert mul(dims[i],dims[j])==summ(scale(dims[k],N[i][j][k]) for k in range(len(N)))
    assert summ(sq(x) for x in dims)==D
    checks[key]={'tensor_sha256':sha,'FP_dimension_character':True,'global_dimension':[str(x) for x in D[:4]]}

N=m.TENSORS['R6_8_1660']
assert N[2][2][2]==3 and N[5][5][5]==8
# Inherited indicators: (1,0,2+omega,2+omega,0,2), omega=(-1+i sqrt3)/2.
real=summ([one,scale(d,3),scale(mul(r,d),2)])
imag=mul(s,d)
assert real==(18,12,10,7,0,0,0,0)
assert imag==(6,3,3,2,0,0,0,0)
assert nonnegative(imag) and imag!=e(0,0)
checks['W3']={'real_coefficients':[str(x) for x in real[:4]],'imaginary_coefficients_plus_branch':[str(x) for x in imag[:4]],'conjugate_branch_changes_imaginary_sign':True,'inherited_indicator_hypothesis_explicit':True}

for i in range(8):
  for j in range(8):assert nonnegative(mul(e(i),e(j)))

q6=[one,c,add(one,r),mul(r,c),add(one,r),c,one]
q10=[one,scale(add(r,rs),F(1,2)),add(one,s),scale(add(scale(r,3),rs),F(1,2)),add(scale(one,2),s),add(r,rs)]
q10+=q10[-2::-1]
for qs in (q6,q10):
    for j in range(1,len(qs)-1):
        assert add(mul(qs[1],qs[j]),scale(qs[j-1],-1))==qs[j+1]
    assert mul(qs[1],qs[-1])==qs[-2]
    assert all(nonnegative(x) for x in qs)
W6=summ(sq(x) for x in q6);W10=summ(sq(x) for x in q10)
assert W6==(16,8,0,0,0,0,0,0)
assert W10==(48,0,24,0,0,0,0,0)
W=mul(W6,W10);A=add(scale(one,24),scale(rs,-8))
assert mul(D,A)==W
assert all(nonnegative(mul(x,y)) for x in q6 for y in q10)
assert not nonnegative(A)
checks['level_6_10']={'basis_cone_products':64,'source_simple_dimensions':77,'required_algebra_dimension':[str(x) for x in A[:4]],'negative_sqrt6_coefficient':str(A[3]),'dimension_identity':True,'square_source_local_dimension_identity':mul(sq(D),sq(A))==sq(W)}
checks['status']={'new_ring_exclusions':0,'new_models':0,'both_unresolved':True}
out=Path(__file__).with_name('verification.json')
out.write_text(json.dumps(checks,indent=2)+'\n')
print(json.dumps(checks,indent=2))
