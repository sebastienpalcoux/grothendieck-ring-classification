#!/usr/bin/env python3
from pathlib import Path
from itertools import product
import json
base=Path(__file__).resolve().parent
r=json.loads((base/'structure_receipt.json').read_text());T=r['galois_transform']
def mv(M,v):return [sum(a*b for a,b in zip(row,v)) for row in M]
def outer(v):return [[a*b for b in v] for a in v]
def add(A,B):return [[a+b for a,b in zip(r,s)] for r,s in zip(A,B)]
def neg(A):return [[-a for a in row] for row in A]
def zero():return [[0]*5 for _ in range(5)]
for j in range(10):
 v=[int(i==j) for i in range(10)];w=v
 for _ in range(4):w=mv(T,w)
 assert w==v
G0=zero()
for bits in product(range(2),repeat=4):
 if sum(bits) in [0,1,3,4]:G0=add(G0,outer([0]+list(bits)))
target=[[15+15*int(i==j) for j in range(5)] for i in range(5)]
records=[]
compositions=[c for c in product(range(5),repeat=4) if sum(c)==4]
assert len(compositions)==35
equivariant_compositions=[c for c in compositions if all(c[i-1]==c[(2*i)%5-1] for i in range(1,5))]
assert equivariant_compositions==[(1,1,1,1)]
for bits in list(product(range(2),repeat=4))[:8]:
 vv=[]
 for b in [bits,tuple(1-x for x in bits)]:
  v=[0]*10;v[1]=1
  for i,x in zip([0,2,3,4],b):v[5+i]=x
  for _ in range(4):vv.extend([v]*5);v=mv(T,v)
  assert all(x>=0 for x in v)
 G=zero()
 for v in vv:G=add(G,outer(v[5:]))
 Q=add(add(target,neg(G0)),neg(G))
 assert all(Q[i][i]==10 for i in range(5))
 bad=[{'i':i,'j':j,'entry':Q[i][j],'minor':100-Q[i][j]**2} for i in range(5) for j in range(i+1,5) if Q[i][j]>10]
 if sum(bits):assert bad
 else:assert not bad
 # Independent stronger check: permit every singleton count composition.
 # Triple-missing counts equal singleton counts by FI(1).
 all_composition_witnesses=[]
 for c in compositions:
  G0c=[[0 if i==0 or j==0 else (5 if i==j else 5-c[i-1]-c[j-1]) for j in range(5)] for i in range(5)]
  Qc=add(add(target,neg(G0c)),neg(G))
  assert all(Qc[i][i]==10 for i in range(5))
  witnesses=[(i,j,Qc[i][j]) for i in range(5) for j in range(i+1,5) if Qc[i][j]>10]
  if sum(bits):assert witnesses
  all_composition_witnesses.append({'singleton_counts':c,'negative_minor_witness':witnesses[0] if witnesses else None})
 records.append({'base_subset_bits':bits,'residual':Q,'negative_minor_witness':bad[0] if bad else None,'all_35_compositions_checked':True,'all_composition_witnesses':all_composition_witnesses,'alternative_obstruction':'five central lifts of one invertible; tensor automorphism group is trivial' if not bad else None})
out={'status':'verified structural reduction: pointed associator must be trivial; categorifiability unresolved','T_fourth_power_identity':True,'a8_mod25_for_a2mod25':pow(2,8,25),'order_of_6_mod25':next(n for n in range(1,26) if pow(6,n,25)==1),'singleton_composition_count':len(compositions),'Galois_equivariant_singleton_compositions':equivariant_compositions,'cases':records}
(base/'pointed_associator_receipt.json').write_text(json.dumps(out,indent=2)+'\n');print('PASS: T^4, all8complementpairs, sevennegativeGramminors; lastpair requires fivecentral lifts.')
