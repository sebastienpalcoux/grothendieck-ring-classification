"""Exact quantum-Weyl dimension/twist and simple-current orbit receipt.

This verifies arithmetic for an existing WZW construction; it does not
replace the categorical conformal-embedding and condensation theorems.
Uses only the Python standard library and works under python -O.
"""
from fractions import Fraction as Q
from collections import Counter
from pathlib import Path
import json

ZERO=(Q(0),)*4
ONE=(Q(1),Q(0),Q(0),Q(0))
T=(Q(0),Q(1),Q(0),Q(0))

def require(test, message):
    if not test:
        raise RuntimeError(message)

def add(a,b):
    return tuple(x+y for x,y in zip(a,b))

def scale(a,c):
    return tuple(x*c for x in a)

def mul(a,b):
    c=[Q(0)]*7
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            c[i+j]+=x*y
    for k in range(6,3,-1):
        c[k-2]+=5*c[k]
        c[k-4]-=5*c[k]
    return tuple(c[:4])

QN={0:ZERO,1:ONE}
for n in range(2,10):
    QN[n]=add(mul(T,QN[n-1]),scale(QN[n-2],-1))
INV_DENOM=(Q(3),Q(0),Q(-4,5),Q(0))
require(mul(INV_DENOM,mul(mul(QN[2],QN[2]),QN[3]))==ONE,
        "quantum Weyl denominator inverse")

def dim(w):
    a,b,c=w
    f=INV_DENOM
    for n in (a+1,b+1,c+1,a+b+2,b+c+2,a+b+c+3):
        f=mul(f,QN[n])
    return f

def conformal_weight(w):
    a,b,c=w
    v=[a,b,c]
    r=[a+2,b+2,c+2]
    cartan4=[[3,2,1],[2,4,2],[1,2,3]]
    return Q(sum(v[i]*cartan4[i][j]*r[j]
                 for i in range(3) for j in range(3)),80)%1

def j2(w):
    a,b,c=w
    return (c,6-a-b-c,a)

weights=[(a,b,c) for a in range(7) for b in range(7-a)
         for c in range(7-a-b)]
neutral=[w for w in weights if (w[0]+2*w[1]+3*w[2])%4==0]
even=[w for w in weights if (w[0]+2*w[1]+3*w[2])%2==0]
require(len(weights)==84 and len(neutral)==22 and len(even)==44,
        "weight counts")
require([w for w in neutral if j2(w)==w]==[(1,2,1),(3,0,3)],
        "fixed-point list")
require(conformal_weight((6,0,0))==Q(1,4),"semion twist")
require(conformal_weight((0,6,0))==0,"boson twist")

rows=[]
seen=set()
for w in neutral:
    if w in seen:
        continue
    orbit={w,j2(w)}
    seen |= orbit
    require(all(x in neutral for x in orbit),"neutral orbit closure")
    count=2 if len(orbit)==1 else 1
    dimension=scale(dim(w),Q(1,count))
    for split in range(count):
        rows.append((w,split,dimension,conformal_weight(w)))
require(len(rows)==14,"rank")
D=(Q(-3),Q(0),Q(2),Q(0))  # 2+sqrt(5)=2t^2-3
expected=Counter({
    (ONE,Q(0)):1,
    (add(ONE,D),Q(1,5)):2,
    (add(ONE,D),Q(4,5)):2,
    (add(ONE,scale(D,3)),Q(1,5)):2,
    (add(ONE,scale(D,3)),Q(4,5)):2,
    (scale(D,2),Q(2,5)):1,
    (scale(D,2),Q(3,5)):1,
    (D,Q(0)):1,
    (scale(D,5),Q(1,2)):1,
    (mul(D,D),Q(0)):1,
})
require(Counter((d,h) for _,_,d,h in rows)==expected,
        "rank14 dimension/twist profile")
global_dim=ZERO
for _,_,d,h in rows:
    global_dim=add(global_dim,mul(d,d))
require(global_dim==scale(mul(D,D),100),"global dimension")
require(j2((2,0,2))==(2,2,2),"algebra orbit")
require(dim((2,0,2))==mul(D,D),"algebra U dimension")
receipt={
    "arithmetic_field":"Q[t]/(t^4-5*t^2+5), t=2*cos(pi/10)",
    "weights_total":len(weights),"weights_even_4ality":len(even),
    "weights_zero_4ality":len(neutral),"rank":len(rows),
    "rows":[{"representative":list(w),"fixed_split":split,
             "dimension_polynomial":[str(v) for v in d],
             "twist_exp_2pi_i":str(h)} for w,split,d,h in rows],
    "global_dimension_polynomial":[str(v) for v in global_dim],
    "status":"PASS"
}
Path(__file__).with_name("r189_rank14_wzw_receipt.json").write_text(
    json.dumps(receipt,indent=2)+"\n")
print("PASS: rank14 WZW orbit count, all quantum dimensions/twists, algebra orbit")
