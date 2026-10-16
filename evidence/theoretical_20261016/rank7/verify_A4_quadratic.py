#!/usr/bin/env python3
import itertools,json,hashlib,argparse,gzip
from pathlib import Path
import numpy as np
import sympy as S
HERE=Path(__file__).resolve().parent
ap=argparse.ArgumentParser()
ROOT=next((p for p in HERE.parents if (p/'supplements/rank8/data/rank8_tables.txt.gz').exists()),Path('.'))
ap.add_argument('--repo',type=Path,default=ROOT)
ap.add_argument('--output',type=Path)
args=ap.parse_args()
DEC={x['id']:x for x in json.loads((args.repo/'supplements/rank8/data/decisions.json').read_text())}
BY_DIGEST={x['tensor_sha256']:x['id'] for x in DEC.values()}
SOURCE={}
with gzip.open(args.repo/'supplements/rank8/data/rank8_tables.txt.gz','rt') as f:
 for line in f:
  raw=json.loads(line.replace('{','[').replace('}',']'))
  digest=hashlib.sha256(json.dumps(raw,separators=(',',':')).encode()).hexdigest()
  if digest in BY_DIGEST:SOURCE[BY_DIGEST[digest]]=raw

def check(ok,msg):
 if not ok: raise ValueError(msg)
def mul(p,q):return tuple(p[q[i]] for i in range(4))
def inv(p):return tuple(p.index(i) for i in range(4))
def parity(p):return sum(p[i]>p[j] for i in range(4) for j in range(i+1,4))%2
Id=tuple(range(4)); G=[Id]+[p for p in itertools.permutations(range(4)) if p!=Id and not parity(p)]; gi={g:i for i,g in enumerate(G)}
prod=lambda g,h:gi[mul(G[g],G[h])]
V=[i for i,g in enumerate(G) if mul(g,g)==Id]
tau=(1,0,2,3)
def cycle_type(p):
 rem=set(range(4));lens=[]
 while rem:
  a=min(rem);cyc=[]
  while a not in cyc:cyc.append(a);rem.remove(a);a=p[a]
  lens.append(len(cyc))
 return sorted(lens)
def tensor(sig,n):
 phi=[gi[mul(mul(sig,g),inv(sig))] for g in G];a=gi[mul(sig,sig)]
 R=np.zeros((24,24,24),dtype=np.int64)
 for g,h in itertools.product(range(12),repeat=2):
  R[g,h,prod(g,h)]=1
  R[g,h+12,prod(g,h)+12]=1
  R[g+12,h,prod(g,phi[h])+12]=1
  gh=prod(g,phi[h]);R[g+12,h+12,prod(gh,a)]=1
  for u in range(12):R[g+12,h+12,prod(gh,u)+12]=n[u]
 return R

def validate(R):
 r=len(R);du=[int(np.flatnonzero(R[i,:,0])[0]) for i in range(r)]
 check(all(sum(R[i,:,0])==1 for i in range(r)),'duality')
 check(np.array_equal(R[0],np.eye(r,dtype=int)),'unit')
 for i,j in itertools.product(range(r),repeat=2):
  check(np.array_equal(R[i].T@R[j].T,np.einsum('k,kab->ab',R[i,j],R.transpose(0,2,1))),'associativity')
  for k in range(r):
   check(R[i,j,k]==R[du[i],k,j]==R[k,du[j],i],'reciprocity')
   check(R[i,j,k]==R[du[j],du[i],du[k]],'star')
 return du

def match8(R):
 data=SOURCE;dec=DEC
 for key,raw in data.items():
  T=np.array(raw,dtype=np.int64)
  if T.max()!=R.max():continue
  invert=[i for i in range(8) if T[i].sum()==8]
  if len(invert)!=4 or not all(T[i,i,0] for i in range(8)):continue
  other=[i for i in range(8) if i not in invert]
  for q in itertools.permutations(invert[1:]):
   for t in itertools.permutations(other):
    p=(0,)+q+t
    if np.array_equal(R,T[np.ix_(p,p,p)]):
     digest=hashlib.sha256(json.dumps(raw,separators=(',',':')).encode()).hexdigest()
     check(digest==dec[key]['tensor_sha256'],'matched subring source digest')
     return {'id':key,'source_permutation':list(p),'decision':dec[key]}
 return None

def coefficient_orbits(sig):
 a=mul(sig,sig);si=inv(sig)
 phi=lambda g:mul(mul(sig,g),si)
 transforms=[lambda g,h=h:mul(mul(phi(h),g),inv(h)) for h in G]
 transforms += [phi,lambda g:mul(a,inv(g))]
 unseen=set(G);orbits=[]
 while unseen:
  start=min(unseen);orbit={start};todo=[start]
  while todo:
   g=todo.pop()
   for f in transforms:
    h=f(g)
    if h not in orbit:orbit.add(h);todo.append(h)
  check(orbit<=unseen,'orbit partition');unseen-=orbit;orbits.append(sorted(orbit))
 return orbits

def weighted_coefficients(orbits,total):
 if not orbits:
  if total==0:yield {}
  return
 first,*rest=orbits
 for c in range(total//len(first)+1):
  for tail in weighted_coefficients(rest,total-c*len(first)):
   yield {**tail,**{g:c for g in first}}

raw_counts={k:0 for k in [3,4,6]};normalized={k:set() for k in [3,4,6]}
for sig in itertools.permutations(range(4)):
 target=Id if not parity(sig) else tau
 b=mul(target,inv(sig));check(b in gi,'gauge must be in A4')
 a=mul(sig,sig)
 check(mul(mul(b,mul(mul(sig,b),inv(sig))),a)==Id,'new rho square invertible part')
 for k in [3,4,6]:
  for nmap in weighted_coefficients(coefficient_orbits(sig),k):
   raw_counts[k]+=1;n=[nmap[g] for g in G]
   normalized_n=[0]*12
   for g in G:normalized_n[gi[mul(b,g)]]=nmap[g]
   normalized[k].add((int(parity(sig)),tuple(normalized_n)))
   old=tensor(sig,n);new=tensor(target,normalized_n)
   p=list(range(12))+[gi[mul(g,b)]+12 for g in G]
   check(np.array_equal(new,old[np.ix_(p,p,p)]),'full gauge tensor identity')
check(raw_counts=={3:24,4:24,6:60},'unreduced domain counts')
records=[]
for k in [3,4,6]:
 for b in range(k//3+1):
  n=[0]*12;n[0]=k-3*b
  for v in V[1:]:n[v]=b
  R=tensor(Id,n);du=validate(R)
  idx=V+[v+12 for v in V];sub=R[np.ix_(idx,idx,idx)]
  rec={'kind':'inner','k':k,'n_identity':n[0],'n_involution':b,'rho_self_dual':du[12]==12,'tensor_sha256':hashlib.sha256(json.dumps(R.tolist(),separators=(',',':')).encode()).hexdigest(),'V4_subring':match8(sub),'tensor':R.tolist()}
  records.append(rec)
 for typ in [[1,1,2],[4]]:
  n=[int(cycle_type(mul(tau,g))==typ) for g in G]
  if sum(n)!=k:continue
  R=tensor(tau,n);du=validate(R)
  records.append({'kind':'outer','k':k,'odd_coset_cycle_type':typ,'rho_self_dual':du[12]==12,'tensor_sha256':hashlib.sha256(json.dumps(R.tolist(),separators=(',',':')).encode()).hexdigest(),'tensor':R.tolist()})
expected={k:set() for k in [3,4,6]}
for rec in records:
 R=np.array(rec['tensor'],dtype=np.int64)
 expected[rec['k']].add((int(rec['kind']=='outer'),tuple(map(int,R[12,12,12:]))))
check(expected==normalized,'complete normalized domain')
X=S.Symbol('X')
for rec in records:
 R=np.array(rec['tensor'],dtype=np.int64);du=[int(np.flatnonzero(R[i,:,0])[0]) for i in range(24)]
 C=sum((R[i].T@R[du[i]].T for i in range(24)),np.zeros((24,24),dtype=np.int64))
 k=rec['k']; q=lambda ell:X**2-12*(ell**2+4)*X+144*(ell**2+4)
 ell=rec['n_identity']-rec['n_involution'] if rec['kind']=='inner' else 2
 pred=q(k)**3*q(ell)**9 if rec['kind']=='inner' else q(k)*(X-24)**4*q(2)**9
 actual=S.Matrix(C.tolist()).charpoly(X).as_expr()
 check(S.expand(actual-pred)==0,'formal-codegree Casimir audit')
 rec['Casimir_polynomial']=str(S.factor(actual))
 rec['formal_codegrees']={'dimension_1':'6*(k^2+4 +/- k*sqrt(k^2+4))','dimension_3':f'2*(({ell})^2+4 +/- ({ell})*sqrt(({ell})^2+4))'}
 if rec['kind']=='outer':rec['formal_codegrees']['dimension_2']='12'
 rec['codegree_field_obstruction']=rec['kind']=='outer' or (rec['n_involution']>0 and k in [3,6])
 rec['rank_two_subring_obstruction']=rec['kind']=='inner' and rec['n_involution']==0
out={'status':'PASS','unnormalized_counts':raw_counts,'basis_group_elements':G,'V4_indices':V,'records':records,'counts':{str(k):sum(x['k']==k for x in records) for k in [3,4,6]}}
if args.output:args.output.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':'PASS','counts':out['counts'],'unnormalized_counts':raw_counts,'results':[{k:v for k,v in x.items() if k!='tensor'} for x in records]},indent=2))
