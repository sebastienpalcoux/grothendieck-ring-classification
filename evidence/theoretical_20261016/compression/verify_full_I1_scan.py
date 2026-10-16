"""Quadratic-field compression tests, summed over the full regular Casimir spectrum."""
import json
from pathlib import Path
from collections import defaultdict
import sympy as s

import hashlib
HERE=Path(__file__).resolve().parent
inputs=json.loads((HERE/'source_tensors.json').read_text())
J={}
for key, entry in inputs.items():
    tensor=entry['tensor']
    digest=hashlib.sha256(json.dumps(tensor,separators=(',',':')).encode()).hexdigest()
    if digest!=entry['tensor_sha256']:raise ValueError(key+': tensor hash mismatch')
    J[key]=tensor
if len(J)!=85:raise ValueError('expected the 85 original residual source tensors')
x=s.Symbol('x');out=[]
for key,R in J.items():
    n=len(R);N=[s.Matrix(M) for M in R]
    C=sum((M*M.T for M in N),s.zeros(n))
    facs=s.factor_list(C.charpoly(x).as_expr())[1]
    groups=defaultdict(lambda:s.S(0));items=defaultdict(list)
    for pol,m in facs:
        p=s.Poly(pol,x)
        if p.degree()!=2:continue
        a,b,c=p.all_coeffs();b/=a;c/=a
        disc=s.factor(b*b-4*c)
        sf=s.prod(q for q,e in s.factorint(disc).items() if e%2)
        groups[sf]+=m*disc/c**2
        items[sf].append([str(pol),m])
    for sf,total in groups.items():
        cond=sf if sf%4==1 else 4*sf
        ratio=s.factor(cond*total)
        row={'id':key,'field_squarefree':int(sf),'conductor':int(cond),'ratio':str(ratio),'factors':items[sf],'violates':bool(ratio>1)}
        out.append(row)
        # Every violation remains in the exact receipt below.
Path(__file__).with_name('full_I1_quadratic_scan.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':'PASS','tensors':len(J),'quadratic_checks':len(out),'violations':sum(r['violates'] for r in out)}))
