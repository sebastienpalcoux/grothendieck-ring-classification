#!/usr/bin/env python3
"""Reopen the rank-seven census and verify four general PSD-Gram exclusions.

All finite domains are rebuilt, all arithmetic is exact, and no optimizer runs.
The vendored support code is bound by SHA-256. Requires SymPy and NumPy only.
"""
import argparse,collections,gzip,hashlib,json,sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
SUPPORT=HERE/'gram_support'

def require(condition,message):
 if not condition:raise RuntimeError(message)

def canonical(T):
 return tuple(tuple(int(x) for row in M for x in row) for M in T)

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--repo',type=Path,default=HERE.parents[2]);p.add_argument('--output',type=Path);a=p.parse_args()
 for entry in json.loads((SUPPORT/'manifest.json').read_text()):
  require(hashlib.sha256((SUPPORT/entry['path']).read_bytes()).hexdigest()==entry['sha256'],'Changed support file '+entry['path'])
 sys.path.insert(0,str(SUPPORT))
 from anti_module import solve
 import module_dual_gram
 from psd_gram_filter import install
 install(module_dual_gram)
 from module_dual_gram import system
 from higher_traces import check_farkas
 from rings import Characters,validate
 cert=json.loads((HERE/'psd_gram_certificate.json').read_text());by={c['id']:c for c in cert['cases']}
 expected={'R7_4_776','R7_4_927','R7_4_2126','R7_3_909'}
 require(hashlib.sha256((HERE/'psd_gram_filter.py').read_bytes()).hexdigest()==cert['psd_filter_sha256'],'Changed PSD filter')
 require(set(by)==expected and len(by)==len(cert['cases']),'Incorrect case domain')
 tensors={};counts=collections.Counter()
 for line in gzip.open(a.repo/'supplements/rank7/data/rank7_tables.txt.gz','rt'):
  N=json.loads(line.replace('{','[').replace('}',']'));m=max(x for M in N for row in M for x in row);counts[m]+=1;rid=f'R7_{m}_{counts[m]}'
  if rid in by:tensors[rid]=N
 require(set(tensors)==expected,'Missing census cases');results=[]
 for rid in sorted(expected):
  N=tensors[rid];c=by[rid];validate(N);digest=hashlib.sha256(json.dumps(N,separators=(',',':')).encode()).hexdigest();require(digest==c['tensor_sha256'],'Source tensor mismatch')
  g=c['involution'];require(N[g][g]==[1,0,0,0,0,0,0],'Not an involution')
  fixed=[i for i in range(7) if N[g][i][i]];require(fixed==c['fixed'] and len(fixed)==3,'Incorrect fixed domain')
  rebuilt=solve(N,g,fixed);actual={canonical(T) for T in rebuilt['representations']};recorded={canonical(b['T']) for b in c['branches']}
  require(len(actual)==c['gauge_orbits']==len(c['branches']) and actual==recorded,'Incomplete anti-module domain')
  arithmetic=Characters(N).fp();negative=[]
  for b in c['branches']:
   T=canonical(b['T']);ab,meta=system(N,g,fixed,T,b['module_simple'],arithmetic)
   if ab is None:require(meta['reason']==b.get('reason'),'Incorrect negative Gram claim');negative.append(None)
   else:
    require(json.loads(json.dumps(meta))==b['meta'],'Incorrect Gram metadata')
    A,B=ab;y=b['y'];check_farkas(A,B,y);negative.append(sum(yi*bi for yi,bi in zip(y,B)))
  results.append({'id':rid,'status':'PASS','scope':'general_complex','tensor_sha256':digest,'anti_module_gauge_orbits':len(actual),'exact_negative_pairings':negative})
 out={'status':'PASS','cases':results,'count':len(results),'optimizer_used':False}
 if a.output:a.output.write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(out,indent=2))

if __name__=='__main__':main()
