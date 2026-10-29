#!/usr/bin/env python3
"""Short exact radical-cone check for three specified construction routes."""
from fractions import Fraction as Q
from pathlib import Path
import json

def need(ok,msg):
    if not ok:raise ValueError(msg)

ZERO=(Q(0),)*8
def basis(i):return tuple(Q(j==i) for j in range(8))
ONE=basis(0);R=basis(1);S=basis(2);C=basis(4)
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def scale(k,a):return tuple(k*x for x in a)
def mul(a,b):
    out=[Q(0)]*8
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            if not x or not y:continue
            fi,fj=i%4,j%4
            scalar=x*y*(2 if fi&fj&1 else 1)*(3 if fi&fj&2 else 1)
            k=fi^fj
            if i<4 or j<4:
                out[k+(4 if (i>=4)^(j>=4) else 0)]+=scalar
            else:
                # c²=2+(sqrt2+sqrt6)/2.
                out[k]+=2*scalar
                for extra in (1,3):
                    out[k^extra]+=scalar*Q(1,2)*(2 if k&extra&1 else 1)*(3 if k&extra&2 else 1)
    return tuple(out)

def quantum_dims(fundamental,level):
    vals=[ONE,fundamental]
    for j in range(1,level+1):
        vals.append(add(mul(fundamental,vals[-1]),scale(-1,vals[-2])))
    need(vals[-1]==ZERO,'level boundary')
    return vals[:-1]

q22=quantum_dims(C,22)
q10=quantum_dims(scale(Q(1,2),add(R,mul(R,S))),10)
adE6=[ONE,ONE,add(ONE,S)]
for family in (q22,q10,adE6):
    need(all(all(a>=0 for a in d) for d in family),'nonnegative radical cone')

def integral(v):return not any(v[1:])
products1=[(i,j,mul(a,b)) for i,a in enumerate(q22) for j,b in enumerate(adE6)]
products2=[(i,j,k,mul(mul(a,b),c)) for i,a in enumerate(q22) for j,b in enumerate(q22) for k,c in enumerate(q10)]
ints1=[(i,j) for i,j,d in products1 if integral(d)]
ints2=[(i,j,k) for i,j,k,d in products2 if integral(d)]
need(ints1==[(i,j) for i in(0,22) for j in(0,1)],'only four pointed simples in first product')
need(ints2==[(i,j,k) for i in(0,22) for j in(0,22) for k in(0,10)],'only eight pointed simples in second product')
W22=sumvec=ZERO
for d in q22:W22=add(W22,mul(d,d))
W10=ZERO
for d in q10:W10=add(W10,mul(d,d))
E6=ZERO
for d in adE6:E6=add(E6,mul(d,d))
D=tuple(map(Q,(144,96,80,56,0,0,0,0)))
need(W22==mul(add(scale(3,ONE),scale(-1,S)),D),'W22 ratio')
need(mul(W22,E6)==scale(12,D),'full-module algebra dimension12')
need(mul(mul(W22,W22),W10)==scale(144,mul(D,D)),'local-module algebra dimension12')
need(q22[10]==tuple(map(Q,(2,1,1,1,0,0,0,0))),'R941 a dimension is level22 label10')

out={'status':'PASS','full_module_source':'SU(2)_22 tensor Ad(E6)',
     'full_module_source_simple_count':len(products1),'integral_simple_labels':ints1,
     'local_center_source':'SU(2)_22 tensor SU(2)_22 tensor SU(2)_10',
     'local_center_source_simple_count':len(products2),'local_source_integral_simple_labels':ints2,
     'required_algebra_dimension_both':12,'pointed_algebra_upper_bounds':[4,8],
     'categorification_decision':'none; excludes only the specified direct constructions',
     'coefficient_basis':['1','sqrt2','sqrt3','sqrt6','c','c sqrt2','c sqrt3','c sqrt6'],
     'c':'2 cos(pi/24); c²=2+(sqrt2+sqrt6)/2',
     'SU2_22_FP_dimensions':[[str(x) for x in d] for d in q22],
     'SU2_10_FP_dimensions':[[str(x) for x in d] for d in q10]}
Path(__file__).with_name('quantum_routes.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS: positive radical cone; only4/8 integral simples; both required dimension12 algebras impossible')
