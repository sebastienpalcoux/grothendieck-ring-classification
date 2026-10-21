"""Independent read-only review of quadratic Morita/profile closure.

Does not import any quadratic producer or modify its receipts.  Completeness
of the finite Gram/action-row domains is separately certified by that campaign.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product,permutations
from collections import defaultdict,Counter
import hashlib,json
import sympy as s
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];QDIR=HERE.parent/'quadratic'
def need(ok,msg):
 if not ok:raise ValueError(msg)
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def times(x,y,q):return (x[0]*y[0]+q*x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def ratio(x,y,q):
 z=times(x,(y[0],-y[1]),q);n=y[0]**2-q*y[1]**2
 need(n!=0,'nonzero dimension');return (z[0]/n,z[1]/n)
def value(v,ds):return tuple(sum(F(n)*d[j] for n,d in zip(v,ds)) for j in (0,1))
def canonical(U,dims):
 blocks=[[i for i,d in enumerate(dims) if d==z] for z in sorted(set(dims))]
 return min(tuple(U[k][i,j] for k in range(8) for i in p for j in p) for pp in product(*(permutations(b) for b in blocks)) for p in [[i for b in pp for i in b]])
def main():
 gram=read(QDIR/'integral_gram.json');module=read(QDIR/'module_rows.json');morita=read(QDIR/'morita_closure.json');profiles=read(QDIR/'profile_closure.json');classes=read(QDIR/'action_classes.json')
 census=read(ROOT/'evidence/rank8_m3_20261021/pipeline/census_m3.json');source={x['id']:x for x in census};by={(r['id'],r['candidate_index']):r for r in gram};moduleby={(r['id'],r['candidate_index']):r for r in module}
 result=[]
 for rid,mr in morita.items():
  R=source[rid]['tensor'];q=mr['radicand'];ds=[tuple(map(F,d)) for d in mr['dimension_pairs']];du=[next(j for j in range(8) if R[i][j][0]) for i in range(8)]
  need(sha(ROOT/'evidence/rank8_m3_20261021/pipeline/census_m3.json')==read(QDIR/'source_verification.json')['sources']['evidence/rank8_m3_20261021/pipeline/census_m3.json'],'census source binding')
  need(hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()==source[rid]['tensor_sha256'],'tensor binding')
  for i,j in product(range(8),repeat=2):need(times(ds[i],ds[j],q)==value(R[i][j],ds),'dimension homomorphism')
  roots={};allf={};live=set()
  for (r,a),g in by.items():
   if r!=rid:continue
   av=g['algebra_object'];need([av[j] for j in du]==av,'self-dual connected algebra object');roots[a]=value(av,ds)
   for fi,ns in enumerate(g['all_multiplicities']):
    B=[av]+[v for v,n in zip(g['vectors'],ns) for _ in range(n)]
    prof=tuple(sorted(ratio(times(value(v,ds),value(v,ds),q),roots[a],q) for v in B))
    allf[(a,fi)]=(B,prof)
    if fi in moduleby[(rid,a)]['surviving_factor_indices']:live.add((a,fi))
  stages=[]
  while True:
   available={roots[a] for a,fi in live}
   kept={key for key in live if set(allf[key][1])<=available}
   stages.append([len({a for a,fi in live}),len(live)])
   if kept==live:break
   live=kept
  expected={(r['candidate_index'],fi) for r in mr['survivors'] for fi in r['factor_indices']}
  need(live==expected,'independent dimension closure');need(stages==[[z['starting_algebras'],z['starting_factors']] for z in mr['stages']],'dimension closure stages')
  available=defaultdict(set)
  for a,fi in live:available[allf[(a,fi)][1]].add(roots[a])
  live={key for key in live if set(allf[key][1])<=available[allf[key][1]]}
  actual={(r['candidate_index'],r['factor_index']):r for r in profiles[rid]['surviving_factors']}
  need(live==set(actual),'independent full-profile closure')
  action_keys=set();full=0
  for key,rec in actual.items():
   B,prof=allf[key];need(rec['B']==B and tuple(sorted(tuple(map(F,z)) for z in rec['profile']))==prof,'profile receipt reconstruction')
   MM=s.Matrix(B);r=MM.rows
   if rec['full_rank_action'] is None:need(MM.rank()<r,'missing full-rank action');continue
   full+=1;need(MM.rank()==r,'full-rank claim');U=list(map(s.Matrix,rec['full_rank_action']))
   need(U[0]==s.eye(r),'module unit')
   for i in range(8):
    need(all(z.q==1 and z>=0 for z in U[i]),'nonnegative integral action')
    need(U[i]*MM==MM*s.Matrix(R[i]).T,'intertwining orientation')
    need(U[i][:,0]==MM[:,i],'distinguished column')
    need(U[du[i]]==U[i].T,'module adjoint')
    for j in range(8):need(U[i]*U[j]==sum((R[i][j][k]*U[k] for k in range(8)),s.zeros(r)),'all module fusion products')
   dims=[ratio(times(value(v,ds),value(v,ds),q),roots[key[0]],q) for v in B]
   action_keys.add(canonical(U,dims))
  need(len(action_keys)==classes[rid]['complete_class_count'],'independent class count')
  controls=0
  for i in range(8):
   av=R[i][du[i]];a=next(a for (r,a),g in by.items() if r==rid and g['algebra_object']==av);g=by[(rid,a)]
   B=[[R[j][i][k] for j in range(8)] for k in range(8)];ct=Counter(tuple(v) for k,v in enumerate(B) if k!=i)
   ns=[ct[tuple(v)] for v in g['vectors']];fi=g['all_multiplicities'].index(ns)
   need((a,fi) in live,'canonical internal-end positive control');controls+=1
  result.append({'id':rid,'final_objects':len({a for a,fi in live}),'final_factors':len(live),'full_rank_factors':full,'full_action_classes':len(action_keys),'canonical_controls':controls,'dimension_closure_stages':stages})
 files=[QDIR/n for n in ['README.md','integral_gram.json','module_rows.json','morita_closure.json','profile_closure.json','action_classes.json','trace_closure.json','source_verification.json']]
 print(json.dumps({'kind':'independent_quadratic_Morita_profile_review','records':result,'source_sha256':{str(p.relative_to(ROOT)):sha(p) for p in files},'verifier_sha256':sha(Path(__file__)),'scope':'Independently recomputed dimension/profile closures, full-rank actions, classes and canonical controls. Gram-domain and row-exclusion completeness are reviewed in code and certified separately by the quadratic campaign.'},indent=2))
if __name__=='__main__':main()
