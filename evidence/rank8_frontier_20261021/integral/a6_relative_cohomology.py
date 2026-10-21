#!/usr/bin/env python3
"""Exact mod-two stable cohomology; primary argument is in the proof notes."""
import argparse, hashlib, importlib.util, itertools, json
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
OLD=ROOT/'evidence/rank8_m3_20261021/models/psl2_11/r360/verify_a6_twist.py'
spec=importlib.util.spec_from_file_location('old_a6',OLD); old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
G=old.G; e=old.UNIT

def require(c,m):
 if not c: raise ValueError(m)
def digest(x):return hashlib.sha256(json.dumps(x,separators=(',',':')).encode()).hexdigest()
def reduce(v,piv):
 while v:
  p=(v&-v).bit_length()-1
  if p not in piv:break
  v^=piv[p]
 return v
def span(vs):
 p={}
 for v in vs:
  v=reduce(v,p)
  if v:p[(v&-v).bit_length()-1]=v
 return p
def nullspace(rows,n):
 p=span(rows);ans=[]
 for f in range(n):
  if f in p:continue
  v=1<<f
  for j in sorted(p,reverse=True):
   if (p[j]&v).bit_count()%2:v^=1<<j
  require(all((r&v).bit_count()%2==0 for r in rows),'nullspace failure')
  ans.append(v)
 return ans

def differential_rows(group,degree):
 """Rows of d:C^degree -> C^(degree+1), normalized, F2."""
 J=[a for a in group if a!=e];tuples=list(itertools.product(J,repeat=degree));ix={a:i for i,a in enumerate(tuples)};rows=[]
 for a in itertools.product(J,repeat=degree+1):
  terms=[a[1:],a[:-1]]+[a[:i]+(old.mul(a[i],a[i+1]),)+a[i+2:] for i in range(degree)]
  v=0
  for t in terms:
   if e not in t:v^=1<<ix[t]
  rows.append(v)
 return tuples,rows

def cohomology(group,degree):
 tuples,rows=differential_rows(group,degree);low,prev=differential_rows(group,degree-1)
 b=[sum(((r>>j)&1)<<i for i,r in enumerate(prev)) for j in range(len(low))]
 z=nullspace(rows,len(tuples));p=span(b);bdim=len(p);reps=[]
 for a in z:
  a=reduce(a,p)
  if a:reps.append(a);p[(a&-a).bit_length()-1]=a
 require(len(reps)==len(z)-bdim,'wrong cohomology dimension')
 return tuples,reps,{'normalized_cochains':len(tuples),'cocycle_dimension':len(z),'coboundary_dimension':bdim,'cohomology_dimension':len(reps),'cocycle_equations_sha256':digest(rows)}

def is_boundary(group,degree,values):
 low,rows=differential_rows(group,degree-1);n=len(low);p={}
 for i,r in enumerate(rows):
  v=r | (values[i]<<n)
  while v&((1<<n)-1):
   k=(v&-v).bit_length()-1
   if k not in p:p[k]=v;break
   v^=p[k]
  else:
   if v>>n:return False
 return True

def embedding_data():
 E=tuple(range(6));r=old.cycles((0,1,2,3),(4,5));s=old.cycles((0,2),(4,5))
 def power(x,k):
  z=E
  for _ in range(k):z=old.permutation_multiply(z,x)
  return z
 emb={a:old.permutation_multiply(power(r,a[0]),power(s,a[1])) for a in G};inv={v:k for k,v in emb.items()}
 A6=[p for p in itertools.permutations(range(6)) if sum(p[i]>p[j] for i in range(6) for j in range(i+1,6))%2==0]
 actions=[]
 for g in A6:
  gi=old.permutation_inverse(g)
  conj={a:old.permutation_multiply(old.permutation_multiply(gi,emb[a]),g) for a in G}
  K=[a for a in G if conj[a] in inv];theta={a:inv[conj[a]] for a in K}
  actions.append((K,theta))
 return actions

def compute():
 acts=embedding_data();result={}
 for degree in [2,3]:
  tuples,basis,meta=cohomology(G,degree);index={a:i for i,a in enumerate(tuples)};records=[]
  for bits in itertools.product(range(2),repeat=len(basis)):
   v=0
   for b,k in zip(basis,bits):
    if k:v^=b
   def w(a):return 0 if e in a else (v>>index[a])&1
   stable=True;failed=None
   for number,(K,theta) in enumerate(acts):
    J=[a for a in K if a!=e]
    vals=[w(t)^w(tuple(theta[a] for a in t)) for t in itertools.product(J,repeat=degree)]
    if not is_boundary(K,degree,vals):stable=False;failed=number;break
   J=[a for a in old.H if a!=e];restriction_zero=is_boundary(old.H,degree,[w(t) for t in itertools.product(J,repeat=degree)])
   records.append({'basis_bits':bits,'stable':stable,'first_failed_conjugation':failed,'restriction_to_point_V4_is_zero':restriction_zero})
  stable=[r for r in records if r['stable']];kernel=[r for r in stable if r['restriction_to_point_V4_is_zero']]
  meta.update(basis_normalized_cochain_bits=[[b>>i&1 for i in range(len(tuples))] for b in basis],all_classes=records,stable_class_count=len(stable),stable_restriction_kernel_count=len(kernel))
  result[str(degree)]=meta
 require(result['2']['stable_class_count']==2,'H2(A6,F2) mismatch')
 require(result['2']['stable_restriction_kernel_count']==1,'H2 restriction is not injective')
 require(result['3']['stable_restriction_kernel_count']==2,'H3 relative kernel is not order two')
 # The old cocycle's nonzero U1 multiplier proves its class is nontrivial.
 w,cert=old.local_relative_cocycle();old.stable_elements(w)
 require(all(w(a,b,c)==0 for a,b,c in itertools.product(old.H,repeat=3)),'old relative cocycle not strict')
 result['known_nonzero_relative_class']={'old_verifier_sha256':hashlib.sha256(OLD.read_bytes()).hexdigest(),'relative_equations_sha256':cert['relative_equations_sha256'],'forced_negative_stabilizer_commutator':True}
 # Integral H4(C3^2,Z)=Sym^2 F3^2. Rotation r(x,y)=(-y,x).
 invariant=[]
 for a,b,c in itertools.product(range(3),repeat=3):
  if (c,-b%3,a)==(a,b,c):invariant.append([a,b,c])
 require(invariant==[[0,0,0],[1,0,1],[2,0,2]],'unexpected C4 invariants')
 require(all(a!=0 for a,b,c in invariant[1:]),'restriction kernel on coordinate C3 nontrivial')
 a=old.cycles((0,1,2));b=old.cycles((3,4,5));r=(3,4,5,0,2,1);ri=old.permutation_inverse(r)
 require(sum(r[i]>r[j] for i in range(6) for j in range(i+1,6))%2==0,'rotation not in A6')
 require(old.permutation_multiply(old.permutation_multiply(r,a),ri)==b,'rotation does not send a to b')
 require(old.permutation_multiply(old.permutation_multiply(r,b),ri)==old.permutation_inverse(a),'rotation does not send b to inverse a')
 result['primary3']={'Sylow_generators':[a,b],'normalizer_permutation':r,'H4_C3_squared_basis':['x^2','xy','y^2'],'normalizer_rotation':[[0,-1],[1,0]],'invariants':invariant,'restriction_coordinate_kernel_size':1}
 return result

def main():
 p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');a=p.parse_args();r=compute();dest=HERE/'a6_relative_cohomology.json'
 if a.write:dest.write_text(json.dumps(r,indent=2)+'\n')
 else:require(json.loads(dest.read_text())==json.loads(json.dumps(r)),'certificate mismatch')
 print('PASS exact stable H2/H3 and primary3 invariant kernel:',[(d,r[d]['stable_class_count'],r[d]['stable_restriction_kernel_count']) for d in ['2','3']])
if __name__=='__main__':main()
