#!/usr/bin/env python3
"""Exact bounded column-capacity follow-up, no feasibility/categorification claim."""
from pathlib import Path
from fractions import Fraction
import json,hashlib
import sympy as s

HERE=Path(__file__).resolve().parent
P=HERE.parents[1]/'prior/evidence/rank8_frontier_20261021'
paths=[P/'quartic_integer_center/source.json',P/'quartic_integer_center/gram_cubic.json',P/'review/r941_fusion_traces.json']
r=next(x for x in json.loads(paths[0].read_text())['records'] if x['id']=='R8_3_941')
N=r['tensor']; basis=[[int(i in subset) for i in range(8)] for subset in ([0],[3],[1,2],[4,5],[6,7])]
def need(b,m):
    if not b:raise ValueError(m)
for b in basis:
    need(all(sum(b[k]*N[k][i][j] for k in range(8))==sum(b[k]*N[i][k][j] for k in range(8)) for i in range(8) for j in range(8)),'central basis')
# Compute whole source-ring center directly.
constraints=s.Matrix([[N[k][i][j]-N[i][k][j] for k in range(8)] for i in range(8) for j in range(8)])
need(8-constraints.rank()==5,'center has dimension5')
rad=[1,s.sqrt(2),s.sqrt(3),s.sqrt(6)]
chars=[[sum(s.Rational(a)*b for a,b in zip(c,rad)) for c in row] for row in r['full_characters']]
M=s.Matrix([[sum(ch[i]*b[i] for i in range(8)) for b in basis] for ch in chars])
need(s.simplify(M.det())==3072,'character determinant')
Q=s.Matrix(r['reduced_Gram']);need(all(Q[:k,:k].det()>0 for k in range(1,5)),'positive Gram')
inv=Q.inv();norms=[(s.Matrix(v).T*inv*s.Matrix(v))[0] for v in r['reduced_high_vectors']]
eligible=[i for i,n in enumerate(norms) if 3*n<=1]
need(len(eligible)==22,'22 eligible/43 denied column types')
need([int(1/norms[i]) for i in [9,10,12,17]]==[23,11,8,5],'four present fiber capacities')
patterns=json.loads(paths[1].read_text())['patterns'];f=json.loads(paths[2].read_text());cases={x['allocation_index']:x for x in f['cases']}
rows=[]
for ix in f['paired_surviving_allocations']:
    c=cases[ix];p=patterns[c['pattern_index']]
    capacity=[{'column':i,'multiplicity':n} for i,n in enumerate(p) if n>=3 and i in eligible]
    need(bool(capacity),'every retained allocation has at leastone eligible fiber')
    rows.append({'allocation':ix,'pattern':c['pattern_index'],'eligible_fibers_multiplicity_at_least3':capacity})
need(len(rows)==14,'14 allocations')
out={'status':'PASS','classification':'UNRESOLVED','new_whole_allocation_exclusions':0,
     'character_center_determinant':3072,'Gram_determinant':int(Q.det()),
     'eligible_column_indices':eligible,'exact_Gram_norms':[str(n) for n in norms],
     'retained_allocations':rows,'inputs_sha256':{str(p.relative_to(P)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
     'scope':'Necessary same-restriction Galois orbit capacity only; no full modular feasibility or existence claim.'}
(HERE/'r941_galois_followup.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS: 22 of65 column types can support order-divisible-by9 twists; all14 retained allocations retain eligible fibers; no exclusion')
