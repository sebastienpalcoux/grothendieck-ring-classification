"""Complete independent bounded N1-row feasibility for the small high0 objects."""
import sys,json,math,itertools,time
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
UP=Path(__file__).resolve().with_name('joint_triple_after_a2.py');exec(compile(UP.read_text().split('def main():')[0],str(UP),'exec'))
BOUNDS=HERE/'low_action_bounds.json';bounds=json.load(open(BOUNDS));byix={r['index']:r for r in bounds['results']};need(bounds['verifier_sha256']==digest(HERE/'low_action_bounds.py'),'action bounds binding')
def row_test(ix,pairhist,targetx,sig):
 b=byix[ix];group=b['group'];inds,C,alpha,hh,mom=augmented(sig);rrow,rbasis,q,vals=row_data(group,0,targetx,sig);base=[rrow[i]for i in inds];zs=[sum(x*C[k][j]for k,x in enumerate(base))for j in range(20)]
 lowrows=[]
 for j in range(5):lowrows.append([int(j==k)for k in range(5)]+[mom[tuple(sorted(pair+(j,)))]if j else int(pair[0]==pair[1])for pair in pairs]+list(cols[j]))
 nlow=[0]+[int(rrow[5+pairs.index((1,j))])for j in range(1,5)]
 old0=next(i for i,l in enumerate(b['labels'])if l.get('type')==0)
 variables=[]
 for typ,hist in enumerate(pairhist):
  for x,n in hist:
   if not n:continue
   if typ==0:
    # The chosen row has a fixed zero diagonal. Other copies of the same
    # restriction type use off-diagonal bounds, which differ from that zero.
    n-=int(x==targetx)
    if not n:continue
    oldj=next(i for i,l in enumerate(b['labels'])if l.get('type')==0 and i!=old0)
   else:oldj=next(i for i,l in enumerate(b['labels'])if l.get('type')==typ)
   lo=b['lower'][old0][oldj];hi=b['upper'][old0][oldj]
   row,bs,qq,vv=row_data(group,typ,x,sig)
   options=range(n*lo,n*hi+1,n if typ==10 else 1)
   if hi==0:continue
   variables.append((typ,x,n,row,tuple(int(row[k])for k in inds[5:]),tuple(options),lo,hi))
 variables.sort(key=lambda z:(len(z[5]),sum(v!=0 for v in z[4])))
 N=len(variables);lows=[[0]*4 for _ in range(N+1)];highs=[[0]*4 for _ in range(N+1)]
 for k in range(N-1,-1,-1):
  typ,x,n,row,co,os,lo,hi=variables[k]
  for j in range(4):lows[k][j]=lows[k+1][j]+min(os)*co[j];highs[k][j]=highs[k+1][j]+max(os)*co[j]
 @lru_cache(None)
 def search(k,target):
  if any(not lows[k][j]<=target[j]<=highs[k][j]for j in range(4)):return None
  if k==N:return ()if all(v==0 for v in target)else None
  typ,x,n,row,co,os,lo,hi=variables[k]
  for v in os:
   tail=search(k+1,tuple(target[j]-v*co[j]for j in range(4)))
   if tail is not None:return (v,)+tail
  return None
 actualrest=(0,)+tuple(domain['high_columns'][0]);targetM=[sum(cols[1][i]*actualrest[j]*R[i][j][k]for i in range(8)for j in range(8))for k in range(8)]
 successes=[];failures=[]
 for z in vals:
  triple=[v+(F(z)-q)*h for v,h in zip(zs,hh)];fulltarget=[0]+[int(rrow[5+pairs.index((1,j))])for j in range(1,5)]+[triple[triples.index(tuple(sorted((1,)+pair)))]for pair in pairs]+targetM
  need(all(F(v).denominator==1 for v in fulltarget),'integer required row action')
  residual=[F(v)-sum(n*rr[j]for n,rr in zip(nlow,lowrows))for j,v in enumerate(fulltarget)]
  target=tuple(int(residual[j])for j in inds[5:]);answer=search(0,target)
  if answer is None:failures.append(z);continue
  direct=[sum(v*rr[j]for v,(_,_,_,rr,_,_,_,_)in zip(answer,variables))for j in range(23)];need(direct==residual,'all23 row action equations')
  successes.append({'triple133':z,'aggregate_entries':[{'type':typ,'pair11':x,'copies':n,'row_sum':v,'individual_lower':lo,'individual_upper':hi}for v,(typ,x,n,rr,co,os,lo,hi)in zip(answer,variables)]})
 return {'type':0,'pair11':targetx,'initial_triple133_domain':list(vals),'excluded_triple133':failures,'surviving_triple133':[v['triple133']for v in successes],'witnesses':successes,'states':search.cache_info().currsize}
out=[];start=time.monotonic()
for row in fibers['results']:
 if row['index']not in byix:continue
 ix=row['index'];ns=[1]+domain['completions'][ix];sig=tuple(sum(n*v[1]for n,v in zip(ns,co))//den for co,den in moment_coefficients.values())
 for number,pairhist in enumerate(row['pair11_histogram_solutions_by_high_type']):
  checks=[row_test(ix,pairhist,x,sig)for x,n in pairhist[0]if n];out.append({'index':ix,'pair_histogram':number,'rows':checks,'excluded_if_any_domain_empty':any(not r['surviving_triple133']for r in checks)})
  print(json.dumps({'index':ix,'pair_histogram':number,'rows':[(r['pair11'],r['surviving_triple133'])for r in checks],'seconds':round(time.monotonic()-start,2)}),file=sys.stderr,flush=True)
print(json.dumps({'schema':'r1154-bounded-high0-rows/v1','scope':'Complete necessary row feasibility, with rowwise symmetry relaxation; no full action or categorification asserted','results':out,'source_sha256':{p.relative_to(ROOT).as_posix():digest(p)for p in [UP,BOUNDS,fiberpath]},'verifier_sha256':digest(Path(__file__))},indent=2))
