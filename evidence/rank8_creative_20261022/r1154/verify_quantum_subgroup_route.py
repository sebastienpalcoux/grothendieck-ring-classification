#!/usr/bin/env python3
"""Exact dimensions and obstruction to a specific index-five construction.

All arithmetic is in Q(sqrt(5)). No numerical approximation or optimizer.
"""
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
import hashlib,json

def need(ok,msg):
    if not ok: raise ValueError(msg)
def add(x,y): return (x[0]+y[0],x[1]+y[1])
def neg(x): return (-x[0],-x[1])
def mul(x,y): return (x[0]*y[0]+5*x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def powq(x,n):
    y=(F(1),F(0))
    for _ in range(n): y=mul(y,x)
    return y
def enc(x): return [str(z) for z in x]

def main():
    one=(F(1),F(0));zero=(F(0),F(0));phi=(F(1,2),F(1,2))
    t2=(F(5,2),F(1,2))
    # [n]=sin(n*pi/10)/sin(pi/10). For even n remove the
    # common factor t=2cos(pi/10); t^2=(5+sqrt(5))/2.
    u={0:zero,1:one,2:one}
    for n in range(2,10):
        u[n+1]=add(mul(t2,u[n]),neg(u[n-1])) if n%2==0 else add(u[n],neg(u[n-1]))
    need(u[10]==zero,'root-of-unity quantum integer [10] vanishes')
    rows=[]
    for a in range(8):
        for b in range(8-a):
            inds=[a+1,b+1,a+b+2]
            evens=sum(i%2==0 for i in inds)
            need(evens in (1,3),'parity reduction of [a+1][b+1][a+b+2]/[2]')
            d=mul(mul(u[inds[0]],u[inds[1]]),u[inds[2]])
            if evens==3:d=mul(d,t2)
            need(d[0]>0 and d[1]>=0,'nonnegative radical coefficient')
            rows.append({'label':[a,b],'dimension':d})
    need(len(rows)==36,'complete SU(3)_7 alcove')
    D=zero
    for row in rows:D=add(D,powq(row['dimension'],2))
    need(D==(F(750),F(330)),'SU(3)_7 global dimension')
    prod=[{'label':row['label']+[f],'dimension':mul(row['dimension'],powq(phi,f))} for row in rows for f in range(2)]
    need(len(prod)==72,'complete product simple domain')
    integral=[r for r in prod if r['dimension'][1]==0]
    need(len(integral)==3 and all(r['dimension']==one for r in integral),'only three simples have rational dimension, all invertible')
    need(all(r['dimension'][1]>0 for r in prod if r not in integral),'strict positive radical coefficient for every noninvertible')
    Dprod=mul(D,add(one,powq(phi,2)))
    DR=(F(540),F(240))
    need(Dprod==mul((F(5),F(0)),DR),'index-five dimension identity')
    hist=Counter(r['dimension'] for r in rows)
    result={'schema':'r1154-targeted-quantum-subgroup/v1','status':'PASS','scope':'Rules out a connected separable algebra of FP dimension 5 in SU(3)_7 tensor Fib, hence the direct index-five connected-etale module-category construction of R1154. Does not exclude R1154 or arbitrary quantum-group constructions.','target_dimension':enc(DR),'su3_7_dimension':enc(D),'product_dimension':enc(Dprod),'dimension_representation':'[a,b] denotes a+b*sqrt(5)','su3_dimension_histogram':[{'dimension':enc(d),'multiplicity':n} for d,n in sorted(hist.items())],'product_simples':[{'label':r['label'],'dimension':enc(r['dimension'])}for r in prod],'rational_dimension_labels':[r['label']for r in integral],'maximum_possible_rational_dimension_connected_separable_algebra':3,'required_algebra_dimension':5,'verifier_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    Path(__file__).with_name('quantum_subgroup_route.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items()if k!='product_simples'},indent=2))
if __name__=='__main__':main()
