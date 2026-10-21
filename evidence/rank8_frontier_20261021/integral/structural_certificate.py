#!/usr/bin/env python3
"""Source-bound hypotheses for the integral frontier proofs. No floating point."""
import argparse, hashlib, importlib.util, itertools, json
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('old_a6',ROOT/'evidence/rank8_m3_20261021/models/psl2_11/r360/verify_a6_twist.py');old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
def require(c,m):
 if not c:raise ValueError(m)
def sha(x):return hashlib.sha256(json.dumps(x,separators=(',',':')).encode()).hexdigest()
def closed(R,S):return all(not R[i][j][k] for i in S for j in S for k in range(len(R)) if k not in S)
def proper(R):
 return [list(S) for bits in itertools.product([0,1],repeat=len(R)-1) if len(S:={0}|{i+1 for i,b in enumerate(bits) if b}) not in [1,len(R)] and closed(R,S)]
def adjoint(R,dual):
 S={0}|{k for i in range(len(R)) for k,n in enumerate(R[i][dual[i]]) if n}
 while True:
  T=S|{k for i in S for j in S for k,n in enumerate(R[i][j]) if n}
  if T==S:return sorted(S)
  S=T

def a5_subgroups():
 G=[p for p in itertools.permutations(range(5)) if sum(p[i]>p[j] for i in range(5) for j in range(i+1,5))%2==0];e=tuple(range(5));ix={p:i for i,p in enumerate(G)}
 mul=[[ix[tuple(a[b[k]] for k in range(5))] for b in G] for a in G];u=ix[e]
 def closure(gens):
  S={u};queue=[u]
  for a in queue:
   for b in gens:
    c=mul[a][b]
    if c not in S:S.add(c);queue.append(c)
  return frozenset(S)
 groups={frozenset([u])};todo=list(groups)
 for H in todo:
  for g in range(60):
   if g in H:continue
   K=closure(list(H)+[g])
   if K not in groups:groups.add(K);todo.append(K)
 orders=[]
 for a in range(60):
  k=1;b=a
  while b!=u:b=mul[b][a];k+=1
  orders.append(k)
 relevant=sorted(H for H in groups if len(H)<60 and any(orders[g]==3 for g in H))
 from collections import Counter
 hist=Counter(len(H) for H in relevant)
 require(set(hist)=={3,6,12},'unexpected A5 subgroup projection')
 v4=next(H for H in groups if len(H)==4 and all(orders[g]<=2 for g in H))
 conjugates=[]
 for a in range(60):
  ai=next(b for b in range(60) if mul[a][b]==u)
  K=frozenset(mul[mul[a][h]][ai] for h in v4)
  if K not in conjugates:conjugates.append(K)
 require(len(conjugates)==5,'wrong V4 conjugate count')
 require(all(len(v4&K)==1 for K in conjugates if K!=v4),'distinct V4 intersection nontrivial')
 require(len(closure(set().union(*conjugates)))==60,'V4 normal closure not A5')
 return {'subgroup_count':len(groups),'proper_subgroups_containing_order3_histogram':sorted(hist.items()),'V4_conjugate_count':len(conjugates),'distinct_V4_intersection_order':1,'V4_normal_closure_order':60}

def compute():
 rows=json.loads((ROOT/'evidence/rank8_m3_20261021/pipeline/census_m3.json').read_text());records=[]
 for name,dims in [('R8_3_731',[1,5,5,10,10,11,12,12]),('R8_3_3344',[1,3,3,10,10,10,4,5]),('R8_3_3342',[1,3,3,10,10,10,4,5])]:
  row=next(r for r in rows if r['id']==name);R=row['tensor'];require(sha(R)==row['tensor_sha256'],'source hash mismatch');dual=[next(j for j in range(8) if R[i][j][0]) for i in range(8)]
  require(all(sum(R[i][j][k]*dims[k] for k in range(8))==dims[i]*dims[j] for i,j in itertools.product(range(8),repeat=2)),'dimension character failure')
  inv=[i for i,d in enumerate(dims) if d==1];sub=proper(R);ad=adjoint(R,dual)
  rec={'id':name,'tensor_sha256':sha(R),'dimensions':dims,'global_dimension':sum(d*d for d in dims),'dual':dual,'proper_subrings':sub,'invertibles':inv,'adjoint_basis':ad}
  if name=='R8_3_731':require(sub==[] and inv==[0],'731 not simple nonpointed')
  else:
   S=[0,1,2,6,7];T=[3,4,5];require(sub==[S],'unexpected proper subrings')
   model,_=old.model_tensor();require(all(R[S[i]][S[j]][S[k]]==model[i][j][k] for i,j,k in itertools.product(range(5),repeat=3)),'A5 fulltensor mismatch')
   acts=[[[R[a][i][j] for j in T] for i in T] for a in S];want=[[[int(i==j) for j in range(3)] for i in range(3)],[[1]*3 for _ in range(3)],[[1]*3 for _ in range(3)],[[1+int(i==j) for j in range(3)] for i in range(3)],[[2-int(i==j) for j in range(3)] for i in range(3)]]
   require(acts==want,'nimrep mismatch');require(all(R[i][a][j]==R[a][i][j] for a in S for i,j in itertools.product(T,repeat=2)),'right nimrep differs')
   rec.update(A5_basis=S,complement_basis=T,action_matrices=acts,dimension10_cube_coefficients=[R[i][i][i] for i in T])
   require(inv==[0] and ad==list(range(8)),'center invertibility prerequisites fail')
  records.append(rec)
 # Exhaustive necessary orders under the three possible projection orders.
 possibilities=[]
 for q in range(1,13):
  n=3*q*q
  if any(a*b%n==0 for a,b in itertools.product([3,6,12],repeat=2)):possibilities.append({'q':q,'K_order':n,'dual_complement_rank':3600//n,'dual_simple_dimension':str(__import__('fractions').Fraction(q,2))})
 require([r['K_order'] for r in possibilities]==[3,12,48],'order sieve failed')
 perfect=json.loads((HERE/'perfect_groups.json').read_text());require(perfect['order360_groups']==162 and perfect['perfect360_indices']==[118],'perfect scan mismatch')
 return {'records':records,'A5_subgroups':a5_subgroups(),'bimodule_order_sieve':possibilities,'perfect_group_catalogue':perfect,'scope':'Exact finite hypotheses; the categorical implications are proved in PROOF.md, not formalized by this script.'}
def main():
 p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');args=p.parse_args();r=compute();dest=HERE/'structural_certificate.json'
 if args.write:dest.write_text(json.dumps(r,indent=2)+'\n')
 else:require(json.loads(dest.read_text())==json.loads(json.dumps(r)),'certificate mismatch')
 print('PASS source tensors, exact A5 nimreps, subgroup enumeration, bimodule order sieve and perfect-group receipt')
if __name__=='__main__':main()
