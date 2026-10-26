#!/usr/bin/env python3
"""Exact arithmetic/source replay; categorical proof is saturation_exclusion.md.

No optimization, finite exponent bound, or floating-point arithmetic is used.
"""
from fractions import Fraction as Q
from pathlib import Path
import hashlib
import itertools
import json

P = Path(__file__).resolve().parent

def need(test, message):
    if not test:
        raise ValueError(message)

# Q(sqrt(10)) in the ordered basis 1,sqrt(10).
def aadd(x,y): return (x[0]+y[0], x[1]+y[1])
def amul(x,y): return (x[0]*y[0]+10*x[1]*y[1], x[0]*y[1]+x[1]*y[0])
def ainv(x):
    norm=x[0]*x[0]-10*x[1]*x[1]
    return (x[0]/norm,-x[1]/norm)
def scale(c,x): return (c*x[0],c*x[1])

d=(Q(3),Q(1)); D=(Q(120),Q(36)); Dbar=(D[0],-D[1])
need(amul(d,d)==aadd((Q(1),Q(0)),scale(6,d)), 'dimension polynomial')
need(D==scale(6,aadd((Q(1),Q(0)),amul(d,d))), 'global dimension')
delta=aadd(ainv(D),scale(-1,ainv(Dbar)))
need(amul(delta,delta)==(Q(1,40),Q(0)), 'exact conductor saturation')
need(amul(scale(3,delta),scale(3,delta))==(Q(9,40),Q(0)), 'quotient obstruction')
need(Q(9,40)>Q(1,40), 'quotient strictness')
# The fundamental discriminant of Q(sqrt(10)) is 4*10=40.
need(10%4 in (2,3) and 4*10==40, 'quadratic conductor')

# Q(zeta_3), basis 1,z; z^2=-1-z. S*T^n*S^-1 has no sqrt(3)
# in its vacuum column, so this exact check uses only this quadratic field.
def zadd(x,y): return (x[0]+y[0],x[1]+y[1])
def zmul(x,y): return (x[0]*y[0]-x[1]*y[1], x[0]*y[1]+x[1]*y[0]-x[1]*y[1])
def zscale(c,x): return (c*x[0],c*x[1])
one=(Q(1),Q(0)); zero=(Q(0),Q(0))
zeta=[one,(Q(0),Q(1)),(Q(-1),Q(-1))]
fourier=[]
for r,n in itertools.product((1,2),repeat=2):
    column=[]
    for a in range(3):
        total=zero
        for b in range(3):
            total=zadd(total,zeta[(2*r*a*b+r*n*b*b)%3])
        column.append(zscale(Q(1,3),total))
    z=zeta[(r*n)%3]
    expected=[zscale(Q(1,3),zadd(one,zscale(2,z))),
              zscale(Q(1,3),zadd(one,zscale(-1,z))),
              zscale(Q(1,3),zadd(one,zscale(-1,z)))]
    need(column==expected, 'Fourier lower-unipotent formula')
    need(column[1]!=zero and column[2]!=zero, 'vacuum line moved')
    fourier.append({'metric_parameter':r,'exponent_mod_3':n,
                    'vacuum_column':[[str(t) for t in u] for u in column]})

inputs=json.loads((P/'inputs.json').read_text())
bindings=[]
for rid in ['R12_1_561','R12_1_628']:
    R=inputs[rid]['tensor']; co=inputs[rid]['coordinate_to_input']; t=inputs[rid]['pointed_square_exponent']
    need(t==(0 if rid.endswith('561') else 3),'pointed square binding')
    for i,j in itertools.product(range(12),repeat=2):
        a,u=i%6,i//6; b,v=j%6,j//6; row=[0]*12
        if u+v<2: row[co[(a+b)%6+6*(u+v)]]=1
        else:
            row[co[(a+b+t)%6]]=1
            for k in range(6): row[co[6+k]]=1
        need(R[co[i]][co[j]]==row, 'source tensor presentation')
    h=co[2]
    need(all(R[h][j][j]==0 for j in range(12)), 'free C3 action')
    du=[next(j for j in range(12) if R[i][j][0]) for i in range(12)]
    ad={0}
    for i in range(12): ad.update(k for k in range(12) if R[i][du[i]][k])
    while True:
        nxt=ad|{k for i in ad for j in ad for k in range(12) if R[i][j][k]}
        if nxt==ad: break
        ad=nxt
    need(len(ad)==12,'full adjoint subring')
    bindings.append({'id':rid,'tensor_sha256':hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest(),
                     'checked_products':144,'central_subgroup_coordinates':[0,2,4]})
report={'status':'PASS','new_general_complex_exclusions':['R12_1_561','R12_1_628'],
        'global_dimension':'120+36sqrt(10)','conductor':40,
        'squared_reciprocal_difference':'1/40','quotient_squared_difference':'9/40',
        'source_bindings':bindings,'metric_Fourier_checks':fourier,
        'finite_exponent_bound_assumed':False,'optimizer_used':False,
        'proof':'saturation_exclusion.md',
        'categorical_prerequisite':'Previously proved central C3 lift, replayed in the preceding evidence packet.'}
(P/'saturation_certificate.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
