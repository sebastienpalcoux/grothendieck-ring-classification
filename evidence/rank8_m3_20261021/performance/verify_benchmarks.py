#!/usr/bin/env python3
"""Rebuild the real census performance fixtures from exact source tensors."""
from pathlib import Path
import hashlib,json,sys,time
import sympy as s
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT/'supplements/rank6/software'));sys.path.insert(0,str(HERE))
from induction import Characters,restriction_columns,discover_roots,check_roots,codegree_poly
from low_frames_rank8 import low_matrices,require
from gram_vectors_rank8 import native
def digest(x):return hashlib.sha256(json.dumps(x,separators=(',',':')).encode()).hexdigest()
def main():
 census={r['id']:r for r in json.loads((HERE.parent/'pipeline/census_m3.json').read_text())};expected={r['id']:r for r in json.loads((HERE/'native_benchmarks.json').read_text())};fixtures=[]
 for ident in (65,1453,903,731):
  rid='R8_3_'+str(ident);source=census[rid];require(digest(source['tensor'])==source['tensor_sha256'],'census tensor digest');start=time.monotonic();a=Characters(source['tensor'])
  if ident==731:out=native(a.C.extract(range(1,8),range(1,8)))
  else:
   f,K,ds,D,pD,emb=a.fp();p=codegree_poly(source['tensor']);roots=discover_roots(p,K);require(roots is not None,'required splitting field');check_roots(p,K,roots);roots.remove(D)
   columns=[restriction_columns(ds,D/r,K,a.C)for r in roots];out=low_matrices(columns,a.C,gram_prune=True)
   for j in sorted({i*(len(out)-1)//10 for i in range(11)}):fixtures.append(dict(id=rid,columns=out[j]))
  require(len(out)==expected[rid]['count']and digest(out)==expected[rid]['output_sha256'],'real complete kernel output '+rid)
  print('PASS:',rid,len(out),'complete outputs;',round(time.monotonic()-start,3),'seconds',flush=True)
 require(json.loads(json.dumps(fixtures))==json.loads((HERE/'low_failure_real_fixtures.json').read_text()),'low-failure sampled fixture source')
if __name__=='__main__':main()
