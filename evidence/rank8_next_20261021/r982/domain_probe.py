"""Exact finite-domain propagation using equivalent rational row equations.

All deletions are backed by an equality, interval/gcd tests, or complete
finite convolution of the remaining variable domains. No solver status is
accepted as a mathematical conclusion.
"""
from collections import deque
from pathlib import Path
from functools import reduce
import hashlib,itertools,json,math,time,sys
HERE=Path(__file__).resolve().parent

def rows_for(name):
 d=json.loads((HERE/(name+'_system.json')).read_text());rows=[list(x)+[b]for x,b in zip(zip(*d['columns']),d['rhs'])]
 from flint import fmpq_mat,fmpz_mat
 M,rank=fmpq_mat(rows).rref();rr=[];table=M.table()
 for i in range(rank):
  l=math.lcm(*(int(x.denominator) for x in table[i]));rr.append([int(x*l) for x in table[i]])
 ll=fmpz_mat(rr).lll().tolist()
 joined=rows+rr+ll
 # A canonical independent row-space replay makes each derived equality exact.
 if fmpq_mat(joined).rref()[1]!=rank:raise AssertionError('derived rows change the rational row space')
 return d,joined,rank

def propagate(rows,domains,dp_limit=30000,seedvars=None,record_steps=False):
 n=len(domains);domains=[set(d) for d in domains]
 nz=[[(j,a)for j,a in enumerate(row[:-1])if a]for row in rows]
 uses=[[]for _ in range(n)]
 for i,row in enumerate(nz):
  for j,a in row:uses[j].append(i)
 initial=range(len(rows)) if seedvars is None else sorted({i for j in seedvars for i in uses[j]})
 queue=deque(initial);queued=set(queue);changes=0;steps=[]
 def finish(outcome,contradiction=None):
  d={'outcome':outcome,'domains':[sorted(d)for d in domains],'deletions':changes,'step_sha256':hashlib.sha256(repr(steps).encode()).hexdigest()}
  if record_steps:d['steps']=steps
  if contradiction is not None:d['contradiction']=contradiction
  return d
 while queue:
  at=queue.popleft();queued.remove(at);row=nz[at];b=rows[at][-1]
  vals=[sorted(a*x for x in domains[j]) for j,a in row]
  minimum=sum(v[0] for v in vals);maximum=sum(v[-1]for v in vals)
  if not minimum<=b<=maximum:return finish('exact_domain_obstruction',{'row':at,'minimum':minimum,'maximum':maximum,'rhs':b})
  free=[k for k,v in enumerate(vals)if len(v)>1]
  if not free:continue
  # DP is complete over the actual current domains, including holes.
  span=maximum-minimum
  use_dp=span<=dp_limit and len(free)<=30
  for pos in free:
   j,a=row[pos];others=[vals[k] for k in free if k!=pos]
   omin=minimum-vals[pos][0];omax=maximum-vals[pos][-1]
   residue=omin;g=0
   for v in others:
    for x in v[1:]:g=math.gcd(g,x-v[0])
   keep={x for x in domains[j] if omin<=b-a*x<=omax and (not g or (b-a*x-residue)%g==0)}
   if use_dp and keep:
    bits=1
    for v in others:
     shifted=0
     for x in v:shifted |= bits<<(x-v[0])
     bits=shifted
    keep={x for x in keep if (bits>>(b-a*x-omin))&1}
   if not keep:return finish('exact_domain_obstruction',{'row':at,'variable':j,'domain':sorted(domains[j]),'method':'complete_finite_convolution'if use_dp else'interval_gcd'})
   if keep!=domains[j]:
    removed=sorted(domains[j]-keep);changes+=len(removed);steps.append((at,j,removed));domains[j]=keep
    for k in uses[j]:
     if k not in queued:queue.append(k);queued.add(k)
    # Current row caches need refresh after any change.
    break
 return finish('exact_domains_consistent')

if __name__=='__main__':
 name=sys.argv[1] if len(sys.argv)>1 else'frame0'
 start=time.monotonic();d,rows,rank=rows_for(name);print('rowspace',len(rows),rank,flush=True)
 result=propagate(rows,[set(range(b+1))for b in d['bounds']],record_steps=True);result.update(matrix_sha256=hashlib.sha256(repr(rows).encode()).hexdigest(),source=name,rank=rank)
 (HERE/(name+'_domains.json')).write_text(json.dumps(result,separators=(',',':'))+'\n')
 print(result['outcome'],'removed',result['deletions'],'fixed',sum(len(x)==1 for x in result['domains']),'seconds',time.monotonic()-start,flush=True)
 if'contradiction'in result:print(result['contradiction'],flush=True)
