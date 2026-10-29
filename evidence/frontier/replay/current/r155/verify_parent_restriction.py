"""Finite algebraic checks for the conditional order-32 parent restriction.

No associator search, optimization, or claim of parent-category existence.
"""
from itertools import product
from pathlib import Path
import hashlib, importlib.util, json

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('six_tensors', ROOT/'current_remaining_cases.py')
data = importlib.util.module_from_spec(spec)
spec.loader.exec_module(data)
N = data.TENSORS['R6_4_155']
digest = hashlib.sha256(json.dumps(N,separators=(',',':')).encode()).hexdigest()
if digest != data.METADATA['R6_4_155']['tensor_sha256']:
    raise ValueError('tensor digest mismatch')
# Original tensor labels: 1=X, 2=Y, 3=h, 4=g, 5=hg.
expected = [1,4,4,1,0,0]
if N[1][2] != expected or N[1][1] != [0,4,4,0,1,1]:
    raise ValueError('wrong Rprime(4) convention')

def bilinear(x,y,M):
    return sum(x[i]*M[i][j]*y[j] for i in range(len(x)) for j in range(len(x)))%4

def radical(elements,M):
    return [x for x in elements if all(bilinear(x,y,M)==0 for y in elements)]

# For C4^2 x C2, any possible H must be all of G[2].
G=list(product(range(4),range(4),range(2)))
H=[x for x in G if x[0]%2==x[1]%2==0]
nondegenerate = 0
bosonic_H = 0
for p,q,s,r,t,u in product(range(4),range(4),range(2),range(4),range(2),range(2)):
    M=((p,r,2*t),(r,q,2*u),(2*t,2*u,2*s))
    if len(radical(G,M))!=1:
        continue
    nondegenerate+=1
    if all(bilinear(h,h,M)==0 for h in H):
        bosonic_H+=1
if bosonic_H:
    raise ValueError('C4^2 x C2 survived unexpectedly')

# Surviving metric data on C4 x C2^3. Values are powers of i.
G=list(product(range(4),range(2),range(2),range(2)))
M=((1,0,0,0),(0,2,0,0),(0,0,2,0),(0,0,0,2))
H=[x for x in G if x[0]%2==0 and sum(x[1:])%2==0]
if len(H)!=8 or len(radical(G,M))!=1:
    raise ValueError('bad explicit metric data')
if any(bilinear(h,h,M) for h in H):
    raise ValueError('H not twist-free')
if any(2*bilinear(g,h,M)%4 for g in G for h in H):
    raise ValueError('H not in monodromy radical')
restricted_radical=[h for h in H if all(bilinear(h,k,M)==0 for k in H)]
if len(restricted_radical)!=2:
    raise ValueError('wrong restriction radical')
reps=[(0,0,0,0),(0,1,0,0),(1,0,0,0),(1,1,0,0)]
q=[(-bilinear(x,x,M))%4 for x in reps]
# q=(1,-1,-i,i), the conjugate-normalized form of the R155 pointed center.
if q!=[0,2,3,1]:
    raise ValueError('wrong quotient twists')
receipt={
 'result':'PASS',
 'scope':'conditional pointed-center restriction; no categorification or exclusion',
 'tensor_sha256':digest,
 'C4_squared_times_C2':{'nondegenerate_symmetric_bicharacters':nondegenerate,
                      'with_twist_free_G2':bosonic_H},
 'surviving_parent_group':'C4 x C2^3',
 'example_H_order':len(H),
 'example_restricted_radical_order':len(restricted_radical),
 'quotient_twist_exponents_mod4':q,
 'parent_existence':'not established',
 'R6_4_155_status':'unresolved'}
out=Path(__file__).with_name('parent_restriction_receipt.json')
out.write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
