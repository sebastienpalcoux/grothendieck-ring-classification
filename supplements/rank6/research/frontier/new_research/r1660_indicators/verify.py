#!/usr/bin/env python3
"""Exact all-object FRS audit for the remaining R6_8_1660 relative ring."""
import json
from itertools import product
from pathlib import Path

P = Path(__file__).resolve().parent
B = list(product(range(3), repeat=2))  # 0=1, 1=g, 2=sigma
labels = [(a,b,k) for k in (0,1) for a,b in B]
index = {v:i for i,v in enumerate(labels)}

def imul(a,b):
    if a == 0: return {b:1}
    if b == 0: return {a:1}
    if a == b == 1: return {0:1}
    if a == b == 2: return {0:1,1:1}
    return {2:1}

def bmul(x,y):
    return {(a,b):m*n for a,m in imul(x[0],y[0]).items()
                     for b,n in imul(x[1],y[1]).items()}

A = {(2,0):2,(2,1):2,(2,2):3}
def atom(x,y):
    out = [0]*18
    for b,n in bmul(x[:2],y[:2]).items():
        if x[2]+y[2] < 2:
            out[index[(*b,x[2]+y[2])]] += n
        else:
            for c,m in bmul(b,(1,1)).items():
                out[index[(*c,0)]] += n*m
            for aa,z in A.items():
                for c,m in bmul(b,aa).items():
                    out[index[(*c,1)]] += n*z*m
    return out

N = [[atom(a,b) for b in labels] for a in labels]
def vmul(a,b):
    out = [0]*18
    for i,x in enumerate(a):
        if x:
            for j,y in enumerate(b):
                if y:
                    for k,z in enumerate(N[i][j]): out[k] += x*y*z
    return out

unit = [int(i == 0) for i in range(18)]
dual = []
for i,x in enumerate(labels):
    candidates = [j for j in range(18) if N[i][j][0]]
    if len(candidates) != 1 or N[i][candidates[0]][0] != 1:
        raise ValueError("Invalid based-ring duality")
    dual.append(candidates[0])
for i,j,k in product(range(18),repeat=3):
    ei = [int(s==i) for s in range(18)]
    ek = [int(s==k) for s in range(18)]
    if vmul(N[i][j],ek) != vmul(ei,N[j][k]):
        raise ValueError("Associativity failed")

# B signs multiply; only S=(sigma,sigma)t is self-dual outside B,
# and its multiplicity-one forgetful image X+gX forces sign +1.
fs = []
for i,(a,b,k) in enumerate(labels):
    fs.append(((-1)**((a==2)+(b==2))) if not k else (1 if dual[i]==i else 0))
negative = [i for i in range(18) if fs[i] == -1]
diag = [[N[dual[i]][i][y] for y in negative] for i in range(18)]
if any(any(row) for row in diag): raise ValueError("Unexpected negative target")
for y in negative:
    for i,j in product(range(18),repeat=2):
        if N[dual[i]][j][y] != N[dual[j]][i][y]:
            raise ValueError("Cross-term pairing failed")

# Existing third-degree constraints: Clifford multiplicities total four,
# rotation multiplicities (4-a,4-b,4-c), all even.
third=[]
for a in range(5):
    for b in range(5-a):
        c=4-a-b
        if all((4-v)%2==0 for v in (a,b,c)):
            # -(a+b*w+c*w^2) = (c-a)+(c-b)*w.
            third.append({'clifford_multiplicities':[a,b,c],
                          'rotation_multiplicities':[4-a,4-b,4-c],
                          'nu3_in_Z_omega':[c-a,c-b]})
if len(third)!=6: raise ValueError("Third-degree domain mismatch")
receipt = {
  'ring':'R6_8_1660 relative center, surviving labelled orientation',
  'rank':18, 'associativity_triples_checked':18**3,
  'labels':labels, 'dual_indices':dual, 'second_indicators':fs,
  'negative_second_indicator_labels':[labels[i] for i in negative],
  'negative_target_diagonal_multiplicities':diag,
  'all_object_FRS_parity':'passes, by symmetric cross-term pairing',
  'third_degree_domain':third,
  'new_profile_exclusions':0,
  'status':'Necessary-condition audit, not a categorification or exclusion.'
}
(P/'certificate.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({k:receipt[k] for k in ('rank','associativity_triples_checked',
 'all_object_FRS_parity','new_profile_exclusions','status')},indent=2))
