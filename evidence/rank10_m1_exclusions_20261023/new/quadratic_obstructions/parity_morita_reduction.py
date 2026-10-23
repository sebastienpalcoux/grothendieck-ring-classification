#!/usr/bin/env python3
"""Exact tensor hypotheses for the uniform rank-16 Morita reduction.
No numerical FP calculation is used. Dimensions live in Q(sqrt(2)).
"""
import json, hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
CASES=json.loads((ROOT/'catalogue.json').read_text())['cases']
TARGETS=[114,115,152,153,179]
def mul(x,y): return (x[0]*y[0]+2*x[1]*y[1], x[0]*y[1]+x[1]*y[0])
def add(x,y):return (x[0]+y[0],x[1]+y[1])
def require(x,msg):
 if not x:raise RuntimeError(msg)
def check(k):
 r=next(r for r in CASES if r['id']==f'R10_1_{k}');N=r['fusion_tensor'];n=10
 require(all(len(a)==n and all(len(b)==n for b in a) for a in N),'shape')
 G=[g for g in range(n) if all(sum(N[g][j])==1 for j in range(n))]
 def p(g,x):return N[g][x].index(1)
 H=[h for h in G if h and p(h,h)==0 and sum(N[h][x][x] for x in range(n))==2]
 require(len(H)==1,'unique involution');h=H[0]
 Y=[x for x in range(n) if N[h][x][x]]
 Z=[x for x in range(n) if x not in G+Y]
 dims=[(1,0) if x in G else (2,2) if x in Y else (3,2) for x in range(n)]
 for i in range(n):
  for j in range(n):
   dim=(0,0)
   for t in range(n): dim=add(dim,(N[i][j][t]*dims[t][0],N[i][j][t]*dims[t][1]))
   require(dim==mul(dims[i],dims[j]),'exact FP dimension homomorphism')
 require(all(N[i][j]==N[j][i] for i in range(n) for j in range(n)),'commutativity')
 require(len(G)==4 and len(Y)==2 and len(Z)==4,'orbit sizes')
 require(all(N[i][j][t]==1 for i in Y for j in Y for t in Y),'odd fixed-sector structure constants')
 swappers=[g for g in G if p(g,Y[0])==Y[1]];require(len(swappers)==2,'transitivity on fixed simples')
 orbits=[];seen=set()
 for x in range(n):
  if x in seen:continue
  o=sorted({x,p(h,x)});orbits.append(o);seen.update(o)
 require(sorted(map(len,orbits))==[1,1,2,2,2,2],'right A-module orbit pattern')
 return {'id':r['id'],'tensor_sha256_compact_json':hashlib.sha256(json.dumps(N,separators=(',',':')).encode()).hexdigest(),'invertibles':G,'involution':h,'fixed_Y':Y,'dimension_delta_squared_Z':Z,'swapping_invertibles':swappers,'h_orbits':orbits,'fixed_sector_coefficients':[N[i][j][t] for i in Y for j in Y for t in Y],'right_module_rank':8,'dual_rank':16,'dual_dimension_profile':{'1':4,'1+sqrt(2)':8,'3+2*sqrt(2)':4},'decision':'necessary_Morita_reduction_only'}
if __name__=='__main__':
 out={'schema':1,'claim':'Every complex categorification of a listed ring has the rank-16 Morita dual specified in MORITA_REDUCTION.md. This does not itself prove existence or exclusion.','cases':[check(k) for k in TARGETS]}
 dst=Path(__file__).with_name('parity_morita_certificate.json');dst.write_text(json.dumps(out,indent=2)+'\n');print('PASS exact hypotheses:',len(out['cases']),'rings')
