"""Exact reconstruction of all sixteen involution-module action branches."""
import json,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'software'))
import sympy as s
from full_morita_gram import *
from rings import permute
R=next(r['N'] for r in json.load(open(ROOT/'data/census.json')) if r['id']=='R6_3_215')
fixed,seed,nodes,reps=anti_representations(R,1);records=[]
for ti,T in enumerate(reps):
 ab,meta=system(R,1,fixed,T);rec={'branch':ti,'T':T,'meta':meta}
 if ab is None:rec['outcome']='exact_rank_obstruction'
 else:
  A,b=ab
  if len(A[0]):y=farkas(A,b)
  elif any(b):
   y=[0]*len(b);j=next(j for j,z in enumerate(b) if z);y[j]=-1 if b[j]>0 else 1
  else:y=None
  if y is not None:
   check_farkas(A,b,y);rec['outcome']='exact_farkas_obstruction';rec['y']=y
  else:
   rec['outcome']='no_exact_obstruction'
   p=ROOT/f'research/new_frontier/full_gram_{ti}.json'
   if p.exists():
    z=json.load(open(p));M=[s.Matrix(6,6,c) for m,c in z for _ in range(m)];V=s.Matrix.hstack(*[m.reshape(36,1) for m in M])
    labels,L=module_matrices(R,1,fixed,T);G=full_gram(L)
    require(V*V.T==G,'invalid frozen full Gram frame')
    require(V.rank()==len(M),'nonfaithful right action')
    unit=next(k for k,m in enumerate(M) if m==s.eye(6));order=[unit]+[k for k in range(len(M)) if k!=unit];M=[M[k] for k in order];V=s.Matrix.hstack(*[m.reshape(36,1) for m in M])
    N=[]
    for a in M:
     row=[]
     for bmat in M:
      n,p=V.gauss_jordan_solve((a*bmat).reshape(36,1));require(not p.rows and all(x.is_Integer and x>=0 for x in n),'invalid right action product');row.append(list(map(int,n)))
     N.append(row)
    perms=[(0,)+p for p in itertools.permutations(range(1,6)) if permute(N,(0,)+p)==R];require(perms,'right action ring mismatch')
    rec.update(outcome='exact_full_based_bimodule_witness',right_actions=[m.tolist() for m in M],dual_N=N,census_permutation=list(perms[0]))
 records.append(rec)
 print(ti,rec['outcome'],flush=True)
out={'id':'R6_3_215','kind':'full_morita_action_gram_frontier','scope':'Necessary conditions and based bimodule completions only, not associators or a categorification','branches':records}
(ROOT/'research/new_frontier/frontier_full_morita.json').write_text(json.dumps(out,indent=2,default=int)+'\n')
