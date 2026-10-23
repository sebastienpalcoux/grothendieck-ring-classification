"""Exact anti-invariant module obstruction; no pivotality assumption."""
import itertools,json,math,time
from fractions import Fraction as Q
from pathlib import Path
import sympy as s
from exact import require

def invs(R):
 n=len(R)
 return [g for g in range(1,n) if R[g][g]==[1]+[0]*(n-1) and all(sum(x)==1 for x in R[g])]
def prod(A,B,f):return tuple(sum(A[i*f+k]*B[k*f+j] for k in range(f)) for i in range(f) for j in range(f))
def transpose(A,f):return tuple(A[j*f+i] for i in range(f) for j in range(f))
def generated_basis(R,seed):
 n=len(R);unit=tuple(int(i==0) for i in range(n));words=[()];rows=[unit];V=s.Matrix([unit]);at=0
 while at<len(words):
  for j in seed:
   word=words[at]+(j,);v=tuple(sum(rows[at][a]*R[a][j][b] for a in range(n)) for b in range(n));W=V.col_join(s.Matrix([v]))
   if W.rank()>V.rank():words.append(word);rows.append(v);V=W
   if len(rows)==n:return words,V.inv()
  at+=1
 return None

def solve(R,g):
 n=len(R);du=[next(j for j in range(n) if R[i][j][0]) for i in range(n)]
 require(all(R[i][j]==R[j][i] for i in range(n) for j in range(n)),'commutative module test only')
 fixed=[x for x in range(n) if R[g][x][x]];f=len(fixed)
 if not 0<f<=2:return None
 eye=tuple(int(i==j) for i in range(f) for j in range(f));sets=[]
 for i in range(n):
  bounds=[R[i][x][y] for x in fixed for y in fixed]
  cand=list(itertools.product(*(range(-a,a+1,2) for a in bounds)))
  if du[i]==i:cand=[a for a in cand if transpose(a,f)==a]
  sets.append(cand)
 sets[0]=[eye];choices=[]
 for count in range(1,n):
  for seed in itertools.combinations(range(1,n),count):
   info=generated_basis(R,seed)
   if info:choices.append((math.prod(len(sets[i]) for i in seed),seed,info))
  if choices:break
 if not choices:return None
 _,seed,(words,inv)=min(choices,key=lambda v:(v[0],v[1]));coef=[[Q(inv[j,i]) for i in range(n)] for j in range(n)];allowed=list(map(set,sets));nodes=0;witness=None
 for vals in itertools.product(*(sets[i] for i in seed)):
  nodes+=1;given=dict(zip(seed,vals))
  if any(prod(given[i],given[j],f)!=prod(given[j],given[i],f) for i in seed for j in seed):continue
  images=[]
  for word in words:
   z=eye
   for i in word:z=prod(z,given[i],f)
   images.append(z)
  mats=[]
  for k in range(n):
   v=tuple(sum(coef[k][i]*images[i][a] for i in range(n)) for a in range(f*f))
   if v not in allowed[k]:break
   mats.append(tuple(int(x) for x in v))
  if len(mats)!=n:continue
  if any(transpose(mats[i],f)!=mats[du[i]] for i in range(n)):continue
  if any(prod(mats[i],mats[j],f)!=tuple(sum(R[i][j][k]*mats[k][a] for k in range(n)) for a in range(f*f)) for i in range(n) for j in range(n)):continue
  witness=mats;break
 return {'fixed':fixed,'generators':list(seed),'candidate_counts':[len(x) for x in sets],'nodes':nodes,'feasible':witness is not None,'witness':witness}
def certificate(R):
 n=len(R)
 if not all(R[i][j]==R[j][i] for i in range(n) for j in range(n)):return None
 for g in invs(R):
  z=solve(R,g)
  if z is not None and not z['feasible']:return {'kind':'involution_module','involution':g,**z}
 return None
def verify(R,c):
 require(c['kind']=='involution_module','wrong module certificate kind');g=c['involution'];require(g in invs(R),'not an invertible involution');z=solve(R,g)
 require(z is not None and not z['feasible'],'module representation exists or test inapplicable')
 for k in z:require(c[k]==z[k], 'incorrect module search record '+k)
if __name__=='__main__':
 import argparse
 P=Path(__file__).resolve().parents[1]
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument('--discover',action='store_true',help='search census tensors instead of verifying frozen certificates')
 ap.add_argument('--bound',type=int,default=3,help='maximum exact multiplicity for discovery')
 ap.add_argument('--out',type=Path,help='new output path for discovery; may not overwrite an existing file')
 args=ap.parse_args();rows=json.load(open(P/'data/census.json'));by={r['id']:r['N'] for r in rows}
 if not args.discover:
  records=json.load(open(P/'certificates/continuation_module.json'))
  for rec in records:verify(by[rec['id']],rec['certificate'])
  print('EXACT FROZEN CERTIFICATES VERIFIED',len(records))
 else:
  if args.out is None:ap.error('--discover requires --out with a new file path')
  if args.out.exists():ap.error('refusing to overwrite an existing output')
  out=[]
  for r in rows:
   if r['m']>args.bound:continue
   c=certificate(r['N'])
   if c:
    verify(r['N'],c);out.append({'id':r['id'],'status':'excluded','certificate':c});print(r['id'],flush=True)
  args.out.parent.mkdir(parents=True,exist_ok=True)
  with args.out.open('x') as f:json.dump(out,f,indent=2);f.write('\n')
  print('NEW CERTIFICATES',len(out))

# Modular discovery selects a full QQ basis; all returned matrices are checked.
from fast_basis import generated_basis
