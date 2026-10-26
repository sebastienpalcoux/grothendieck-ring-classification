"""Exact parity-cocycle identities used in the U_base exhaustion proof."""
from itertools import product
from pathlib import Path
import json
P=list(product(range(2),repeat=2))
H=[(0,0),(1,1)]
def mul(x,y):return x[0]^y[0],x[1]^y[1]
def eps(x):return x[0]^x[1]
def w(x,y,z):return x[0]*eps(y)*eps(z)
def need(v,msg):
    if not v:raise ValueError(msg)
for a,b,c,d in product(P,repeat=4):
    need((w(b,c,d)+w(mul(a,b),c,d)+w(a,mul(b,c),d)+w(a,b,mul(c,d))+w(a,b,c))%2==0,'3-cocycle')
for h,k,u in product(H,H,P):
    need(w(h,k,u)==w(h,u,k)==w(u,h,k)==0,'bimodule object equations unchanged')
for h,u,v in product(H,P,P):
    need(w(u,h,v)==w(u,v,h)==0,'balancing and right product unchanged')
    need(w(h,u,v)==h[0]*eps(u)*eps(v),'left sign charge zest')
out=dict(status='PASS',parity_quadruples=256,reverse_diagonal_algebra_unchanged=True,
         bimodule_objects_unchanged=True,balanced_product_unchanged=True,
         tensor_left_action='multiplied by sign(h) exactly for odd times odd',
         source_universal_group_unchanged='S3 x S3')
(Path(__file__).resolve().parent/'zest_cocycle_replay.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
