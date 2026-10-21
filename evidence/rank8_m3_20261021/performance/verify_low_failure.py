#!/usr/bin/env python3
"""Fresh exact comparisons of the additive PSD shortcut with frozen induction."""
from pathlib import Path
import argparse,hashlib,itertools,json,random,sys,time
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT/'supplements/rank8/experimental_signed'));sys.path.insert(0,str(HERE))
import sympy as s
import induction,higher_traces
import low_failure_exact as fast
from exact import field,Embedding,t

def require(test,message):
 if not test:raise ValueError(message)
def principal_minor_reference(Q):
 n=len(Q)
 for size in range(1,n+1):
  for ix in itertools.combinations(range(n),size):
   if s.Matrix([[Q[i][j] for j in ix] for i in ix]).det()<0:return False
 return True

def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--real-fixtures',type=Path,default=HERE/'low_failure_real_fixtures.json');parser.add_argument('--write',action='store_true',help='Explicitly replace the validation receipt; default is read-only');args=parser.parse_args();started=time.monotonic();rng=random.Random(20261021);matrices=[]
 for n in range(1,8):
  matrices.extend([[[0]*n for _ in range(n)],[[int(i==j) for j in range(n)] for i in range(n)]])
  for sample in range(6):
   C=s.Matrix(n,max(1,n//2),[rng.randrange(-3,4) for _ in range(n*max(1,n//2))]);Q=C*C.T
   matrices.append([[int(Q[i,j]) for j in range(n)] for i in range(n)])
  for sample in range(4):
   Q=[[0]*n for _ in range(n)]
   for i in range(n):
    for j in range(i,n):Q[i][j]=Q[j][i]=rng.randrange(-2,7)
   matrices.append(Q)
 # Degenerate diagonal, nonzero row, and arithmetic far beyond fixed-width bounds.
 matrices.extend([[[0,1],[1,10]],[[0,0,0],[0,4,2],[0,2,1]],[[10**80,10**70],[10**70,10**60]],[[10**80,10**70+1],[10**70+1,10**60]]])
 for i,Q in enumerate(matrices):require(fast.positive_semidefinite(tuple(map(tuple,Q)))==principal_minor_reference(Q),f'PSD fixture {i}')
 K=field(s.Poly(t-1,t));emb=Embedding(s.Poly(t-1,t),(1,1));full=0;outcomes={}
 for tail in matrices:
  n=len(tail)+1;cols=[tuple([1]+[rng.randrange(0,3) for _ in range(n-1)]) for _ in range(n)];LL=s.Matrix.hstack(*(s.Matrix(c) for c in cols));LL=LL*LL.T;Q=s.zeros(n)
  for i in range(n-1):
   for j in range(n-1):Q[i+1,j+1]=tail[i][j]
  if full%5==0:Q[0,n-1]=Q[n-1,0]=-1
  B=LL+Q;ds=[K.one]*n;D=K(1000 if full%2 else 1);du=list(range(n))
  if n>2 and full%3:du[1],du[2]=2,1
  expected=fast._FROZEN_LOW_FAILURE(cols,B,ds,D,K,emb,du);got=fast.low_failure(cols,B,ds,D,K,emb,du);require(got==expected,f'full synthetic fixture {full}')
  name='none' if got is None else got['kind'];outcomes[name]=outcomes.get(name,0)+1;full+=1
 real=[]
 if args.real_fixtures:
  fixtures=json.loads(args.real_fixtures.read_text())
  if fixtures and 'columns' in fixtures[0]:
   grouped={}
   for fixture in fixtures:grouped.setdefault(fixture['id'],[]).append(fixture['columns'])
   fixtures=[{'id':rid,'frames':frames} for rid,frames in grouped.items()]
  census={x['id']:x['tensor'] for x in json.loads((HERE.parent/'pipeline/census_m3.json').read_text())}
  for fixture in fixtures:
   rid=fixture['id'];R=census[rid];a=induction.Characters(R);f,K,ds,D,pD,e=a.fp();oldtime=newtime=0;results=[]
   for columns in fixture['frames']:
    st=time.monotonic();expected=fast._FROZEN_LOW_FAILURE(columns,a.C,ds,D,K,e,a.du);oldtime+=time.monotonic()-st
    st=time.monotonic();got=fast.low_failure(columns,a.C,ds,D,K,e,a.du);newtime+=time.monotonic()-st
    require(got==expected,'actual frame obstruction mismatch '+rid);results.append(got)
   real.append({'id':rid,'frames_compared':len(results),'exact_obstruction_objects_equal':True,'frozen_seconds':oldtime,'accelerated_seconds':newtime,'outcomes':results})
 # Imported aliases are patched, and repeated installation is idempotent.
 require(induction.low_failure is fast._FROZEN_LOW_FAILURE and higher_traces.low_failure is fast._FROZEN_LOW_FAILURE,'initial frozen alias')
 from types import SimpleNamespace
 extra=SimpleNamespace(low_failure=fast._FROZEN_LOW_FAILURE)
 fast.install();fast.install(extra);fast.install(extra);require(induction.low_failure is fast.low_failure and higher_traces.low_failure is fast.low_failure and extra.low_failure is fast.low_failure,'alias installation')
 sources={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [HERE/'low_failure_exact.py',Path(induction.__file__),Path(__file__)]}
 result={'status':'PASS','recovery':'Fresh execution after workspace loss; no old receipt recreated.','synthetic_psd_comparisons':len(matrices),'synthetic_full_obstruction_comparisons':full,'synthetic_outcomes':outcomes,'real_frames':real,'alias_installation':'PASS','sources_sha256':sources,'elapsed_seconds':time.monotonic()-started}
 if args.real_fixtures:result['real_fixture_sha256']=hashlib.sha256(args.real_fixtures.read_bytes()).hexdigest()
 def stable(value):
  if isinstance(value,dict):return {k:stable(v) for k,v in value.items() if not k.endswith('_seconds')}
  if isinstance(value,list):return [stable(v) for v in value]
  return value
 receipt=HERE/'low_failure_validation.json'
 if args.write:receipt.write_text(json.dumps(result,indent=2)+'\n')
 else:require(stable(result)==stable(json.loads(receipt.read_text())),'deterministic validation receipt mismatch')
 print(json.dumps({k:v for k,v in result.items() if k not in ['real_frames','sources_sha256']},indent=2))
if __name__=='__main__':main()
