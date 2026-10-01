def _audit_require(ok, message):
    if not ok: raise AssertionError(message)

from itertools import product
from fractions import Fraction
from json import dumps
from pathlib import Path

# Every symmetric bicharacter of C_n x C_m, n|m, is uniquely specified
# by diagonal coefficients a/n,b/m and cross coefficient c/n.
# Work modulo m, so there are no floating point operations.
results=[]
for n,m in [(1,32),(2,16),(4,8)]:
    elements=list(product(range(n),range(m)))
    records=[]
    for a,b,c in product(range(n),range(m),range(n)):
        def B(x,y):
            return (a*(m//n)*x[0]*y[0]+b*x[1]*y[1]+c*(m//n)*(x[0]*y[1]+x[1]*y[0]))%m
        radical=[x for x in elements if all(B(x,y)==0 for y in elements)]
        if len(radical)!=1: continue
        bosons=[x for x in elements if B(x,x)==0]
        expected=([(0,y) for y in range(0,32,8)] if n==1 else [(0,y) for y in range(0,16,4)] if n==2 else [(x,y) for x in range(0,4,2) for y in range(0,8,4)])
        _audit_require(sorted(bosons)==expected, (n,m,a,b,c,bosons))
        _audit_require(len(bosons)==4, 'Exact audit check failed')
        records.append({'a':a,'b':b,'c':c,'bosons':bosons})
    results.append({'group':[n,m],'nondegenerate_bicharacters':len(records),'boson_count':4,'forms':records})
output=Path(__file__).with_name('bicharacter_order32_certificate.json')
output.write_text(dumps(results,indent=2)+'\n')
print(dumps([{k:v for k,v in row.items() if k!='forms'} for row in results],indent=2))
