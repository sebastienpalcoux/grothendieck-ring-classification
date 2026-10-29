#!/usr/bin/env python3
import itertools,json,math
from pathlib import Path

def need(ok,why):
    if not ok:raise ValueError(why)
rows=[]
for m in [6,12]:
    for r in range(1,m):
        if math.gcd(r,m)!=1:continue
        f=lambda a,b,c:r*a*((b+c)//m)%m
        for a,b,c,d in itertools.product(range(m),repeat=4):
            need((f(b,c,d)-f((a+b)%m,c,d)+f(a,(b+c)%m,d)-f(a,b,(c+d)%m)+f(a,b,c))%m==0,'carry cocycle identity')
        restrictions=[]
        for d in range(2,m+1):
            if m%d:continue
            h=m//d;t=sum(f(h,j*h%m,h)for j in range(d))%m
            need(t==r*h%m,'exact cyclic restriction invariant')
            need(m//math.gcd(t,m)==d,'full-order restriction class')
            restrictions.append({'subgroup_order':d,'root_exponent_mod_m':t,'class_order':d})
        if m==12:need(f(6,6,6)==6,'nontrivial C2 associator')
        rows.append({'quotient_order':m,'bicharacter_parameter':r,'restrictions':restrictions})
result={'status':'PASS','scope':'Conditional cyclic crossed-product pointed associator; no near-group existence assertion',
        'results':rows,'R1768_consequence':'The proposed second C2 quotient after cyclic144/maximal-isotropic12 is obstructed.'}
Path(__file__).with_name('cyclic_anomaly_verified.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS: exact carry cocycles and subgroup invariants; C12 quotient restricts nontrivially to C2.')
