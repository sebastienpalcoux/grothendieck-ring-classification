"""Independent exact polynomial-coefficient audit of the 640 phase Gram filter.
Local patterns are built by coefficient convolution with exact Gram positivity.
Global allocations use meet-in-the-middle products and exact complements.
No floating-point optimizer and no import of the discovery programs.
"""
from pathlib import Path
from collections import Counter
from functools import lru_cache
import hashlib,itertools,json,time
import argparse
from all_indicators import default_repo
ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path);ap.add_argument('--output',type=Path);args=ap.parse_args()
ROOT=(args.repo or default_repo()).resolve();OUT=Path(__file__).parent
PRIOR=ROOT/'supplements/rank7/verification-repository/evidence/residual_20261002/rank6/packet_gram_probe_receipt.json'
DISC=OUT/'phase_full_gram_filter.json'
phases=[12,30,42,44,14,26,36,8,32,20]
triples=[(4,4,4)]+[(8,8,8)]*3+[(16,16,16)]*2+[(36,20,12)]+[(40,24,16)]*2+[(72,40,24)]
targets=[(q//2,q//2,a//2,a//2,s) for q,a,s in triples]
def need(c,m):
 if not c:raise RuntimeError(m)
@lru_cache(None)
def local(types,target):
 # Explicit multiplication of finite geometric sums in five moment variables.
 states={((0,)*5,())}
 for b,c,a in types:
  v=(b*(b+c),c*(b+c),b*a,c*a,a*a)
  cap=min(t//x for t,x in zip(target,v) if x)
  new=set()
  for weight,powers in states:
   for n in range(cap+1):
    w=tuple(t+n*x for t,x in zip(weight,v))
    if all(x<=y for x,y in zip(w,target)):
     rem=tuple(y-x for x,y in zip(w,target))
     if (rem[0]+rem[1])*rem[4]>=(rem[2]+rem[3])**2:new.add((w,powers+(n,)))
  states=new
 return tuple(sorted(p for w,p in states if w==target))
def product(options,limit):
 zero=(0,)*len(limit);states={zero}
 for opts in options:
  nxt=set()
  for a in states:
   for b in opts:
    v=tuple(x+y for x,y in zip(a,b))
    if all(x<=y for x,y in zip(v,limit)):nxt.add(v)
  states=nxt
  if not states:break
 return states
@lru_cache(None)
def solve(types,counts):
 opts=[tuple(p for p in local(types,t) if all(x<=y for x,y in zip(p,counts)))for t in targets]
 if any(not x for x in opts):return False
 opts.sort(key=len,reverse=True)
 left=product(opts[::2],counts);right=product(opts[1::2],counts)
 return any(tuple(x-y for x,y in zip(counts,l))in right for l in left)
# Independently bind each moment target to the Fourier masses and exhaust the
# two exceptional real phases before allocating the ten remaining phases.
from fractions import Fraction as F
massdata=json.loads((OUT/'phase_masses.json').read_text())['cases'][0]['masses']
mass={row['phase']:row for row in massdata}
for k,(Q,H,A) in zip(phases,triples):
 m=[[F(c) for c in v]for v in mass[k]['masses_over_d_K']]
 need(m[0]==m[1]==m[4]==[0]*4,'nonspin phase has no unit, g or sigma mass')
 need(m[2]==m[3]==[F(Q,2),F(H,2),0,0] and m[5]==[H,A,0,0],'phase targets from Fourier coefficients')
dimensions=[(1,0,0,0),(1,0,0,0),(3,2,2,1),(3,2,2,1),(0,1,0,0),(4,3,2,2)]
def restriction_masses(columns):
 out=[[0]*4 for _ in range(6)]
 for v in columns:
  dim=[sum(v[i]*dimensions[i][j]for i in range(6))for j in range(4)]
  for i in range(6):
   for j in range(4):out[i][j]+=v[i]*dim[j]
 return out
start=time.monotonic();receipt=json.loads(PRIOR.read_text());disc=json.loads(DISC.read_text());out=[]
for name,digest in disc['source_sha256'].items():
 need(hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,'phase profile source hash: '+name)
need(len(receipt['branches'])==len(disc['branches'])==3,'three labelled branches')
for branch,db in zip(receipt['branches'],disc['branches']):
 need(branch['low']==db['low'] and branch['labelling']==db['labelling'],'branch correspondence')
 source=ROOT/f'supplements/rank6/research/round5/m8_1660/low{branch["low"]}_profiles.json'
 raw=json.loads(source.read_text())['branches'][0]
 low=raw['columns'];case=next(c for c in raw['cases'] if c['labelling']==branch['labelling'])
 partners=[(v[1],v[0],v[3],v[2],v[4],v[5])for v in low[:4]]
 need(restriction_masses(low)==[[F(c)for c in v]for v in mass[0]['masses_K']],'six low columns exhaust phase zero')
 need(restriction_masses(partners)==[[F(c)for c in v]for v in mass[24]['masses_K']],'four fermion partners exhaust phase 24')
 forced=Counter((v[0],v[3],v[2],v[4],v[5]) for v in low[:4]);survivors=[]
 for idx in branch['survivors']:
  # Source high order omits unit: (g,X,gX,sigma,T).
  remaining=Counter({tuple(v):n for v,n in zip(raw['high_vectors'],case['profiles'][idx]) if n})
  remaining.subtract(forced);need(min(remaining.values())>=0,'forced fermion partners')
  spin={v:n for v,n in remaining.items()if v[3] and n}
  if spin!={(0,2,2,1,3):8}:continue
  remaining={v:n for v,n in remaining.items()if n and not v[3]}
  need(all(v[0]==0 for v in remaining),'phase domain has nonzero g')
  types=tuple(sorted((v[1],v[2],v[4]) for v in remaining))
  counts=tuple(remaining[(0,b,c,0,a)] for b,c,a in types)
  if solve(types,counts):
   survivors.append(idx)
   witness=next(w for w in db['witnesses']if w['profile']==idx)
   need(tuple(map(tuple,witness['types']))==types,'witness type list')
   allocation=witness['phase_counts'];need(len(allocation)==10,'witness phase count')
   for pat,target in zip(allocation,targets):
    need(len(pat)==len(types) and all(isinstance(n,int)and n>=0 for n in pat),'witness nonnegative integers')
    actual=tuple(sum(n*v[j]for n,(b,c,a)in zip(pat,types)for v in [(b*(b+c),c*(b+c),b*a,c*a,a*a)])for j in range(5))
    need(actual==target,'witness exact phase moments')
   need(tuple(sum(p[i]for p in allocation)for i in range(len(types)))==counts,'witness inventory')
 need(survivors==db['survivors'],('survivor mismatch',branch['low'],branch['labelling']))
 out.append({'low':branch['low'],'labelling':branch['labelling'],'input':len(branch['survivors']),'survivors':survivors,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest()})
 print(branch['low'],branch['labelling'],'PASS',len(survivors),flush=True)
result={'status':'PASS','method':'exact coefficient convolution and meet-in-the-middle support intersection','elapsed_seconds':time.monotonic()-start,'input_sha256':hashlib.sha256(PRIOR.read_bytes()).hexdigest(),'discovery_sha256':hashlib.sha256(DISC.read_bytes()).hexdigest(),'total_survivors':sum(len(b['survivors'])for b in out),'branches':out}
need(result['total_survivors']==640,'full phase domain count')
if args.output:args.output.write_text(json.dumps(result,indent=2)+'\n')
print('PASS',result['total_survivors'],result['elapsed_seconds'])
