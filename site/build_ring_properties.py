#!/usr/bin/env python3
"""Exact, source-bound ring properties for every individual atlas record.

No numeric tolerance is used. The largest real root of each integral fusion
matrix polynomial is its Perron root. The largest root of the central Casimir
polynomial is the global FP dimension. Integrality is decided by rational
root isolation, not rounded displayed dimensions.
"""
from pathlib import Path
from functools import lru_cache
import hashlib,json
import sympy as sp
ROOT=Path(__file__).resolve().parents[1];DIST=ROOT/'site/dist';T=sp.Symbol('t')
SOURCES=('realized_rings.json','unresolved_cases.json','resolved_cases.json','rank9_rank10_m1.json','rank11_m1.json','rank9_m2.json')
def sha(raw):return hashlib.sha256(raw).hexdigest()
@lru_cache(maxsize=None)
def perron_integrality(coefficients):
 p=sp.Poly.from_list(list(coefficients),T)
 intervals=p.intervals(eps=sp.Rational(1,8))
 if not intervals:raise ValueError('A nonnegative matrix must have a real Perron root')
 (a,b),_=intervals[-1]
 return {'integer':bool(a==b and a.q==1),'isolating_interval':[str(a),str(b)]}
def derive(tensor):
 n=len(tensor);dual=[]
 for i in range(n):
  hits=[j for j in range(n) if tensor[i][j][0]]
  if len(hits)!=1 or tensor[i][hits[0]][0]!=1:raise ValueError('Invalid duality')
  dual.append(hits[0])
 support=[[{k for k,v in enumerate(row) if v}for row in mat]for mat in tensor]
 def closure(seed):
  found={0,*seed};changed=True
  while changed:
   old=set(found);found.update(dual[i]for i in old)
   for i in old:
    for j in old:found.update(support[i][j])
   changed=found!=old
  return found
 inv=[i for i in range(n) if tensor[i][dual[i]]==[1]+[0]*(n-1)]
 matrices=[sp.Matrix(m)for m in tensor]
 polys=[tuple(int(c)for c in m.charpoly(T).all_coeffs())for m in matrices]
 dims=[perron_integrality(p)for p in polys]
 omega=sum((matrices[i]*matrices[dual[i]]for i in range(n)),sp.zeros(n))
 global_poly=tuple(int(c)for c in omega.charpoly(T).all_coeffs())
 global_test=perron_integrality(global_poly)
 properties={
  'integral':all(d['integer']for d in dims),'weakly_integral':global_test['integer'],
  'pointed':len(inv)==n,'perfect':inv==[0],
  'simple':all(len(closure({i,dual[i]}))==n for i in range(1,n)),
  'commutative':all(tensor[i][j]==tensor[j][i]for i in range(n)for j in range(n)),
  'self_dual':dual==list(range(n)),
  'multiplicity_free':max(v for m in tensor for row in m for v in row)==1,
 }
 if properties['integral'] and not properties['weakly_integral']:raise ValueError('Integral implies weakly integral')
 return {'properties':properties,'certificate':{'dimension_characteristic_polynomials':[list(p)for p in polys],
  'dimension_root_isolation':dims,'casimir_polynomial':list(global_poly),'global_root_isolation':global_test,
  'invertible_indices':inv,'dual_indices':dual,
  'single_generator_closure_ranks':[len(closure({i,dual[i]}))for i in range(1,n)]}}
def build():
 path=DIST/'data/ring_properties.json';cache=json.loads(path.read_text()).get('records',{})if path.exists()else{}
 records={};bindings={}
 for name in SOURCES:
  raw=(DIST/'data'/name).read_bytes();payload=json.loads(raw);bindings[name]=sha(raw)
  for r in payload.get('records',payload.get('cases',[])):
   tensor=r.get('fusion_tensor',r.get('tensor'))
   if tensor is None:raise ValueError('Missing tensor: '+r['id'])
   h=sha(json.dumps(tensor,separators=(',',':')).encode())
   if r.get('tensor_sha256')and r['tensor_sha256']!=h:raise ValueError('Tensor digest: '+r['id'])
   old=cache.get(r['id'],{})
   result={k:v for k,v in old.items()if k not in ('tensor_sha256',)}if old.get('tensor_sha256')==h else derive(tensor)
   records[r['id']]={'tensor_sha256':h,**result}
  print('Indexed',name,flush=True)
 result={'schema':'ring-atlas/exact-properties/v1','scope':'Exact structural properties of individual catalogued fusion rings; independent of categorifiability. Aggregate census count tables are not structurally filtered.',
  'method':'Integral Perron-root isolation over QQ, full invertible products, exhaustive generated based-subring closure, and exact coefficient tests. Simple means no proper nontrivial dual-closed based subring. Perfect means the unit is the only invertible basis element.',
  'source_sha256':bindings,'records':dict(sorted(records.items()))}
 path.write_text(json.dumps(result,ensure_ascii=False,separators=(',',':'))+'\n')
 flags={**result,'records':{rid:{'tensor_sha256':r['tensor_sha256'],'properties':r['properties']}for rid,r in result['records'].items()}}
 (DIST/'data/ring_property_flags.json').write_text(json.dumps(flags,ensure_ascii=False,separators=(',',':'))+'\n')
 print('Exact property records:',len(records),flush=True)
if __name__=='__main__':build()
