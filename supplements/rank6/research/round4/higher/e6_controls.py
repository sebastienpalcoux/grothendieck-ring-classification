"""Bounded application of the final full half-E6 projection engine to all64 inputs."""
import sys,json,time,signal
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'));import round4_higher_e6 as M
D=[{'id':r['id'],'inherited_status':r['status']}for r in __import__('frozen_inputs').rows(P)];C={r['id']:r['N']for r in json.load(open(P/'data/census.json'))};out=[]
def stop(*a):raise TimeoutError('20-second per-control discovery budget')
signal.signal(signal.SIGALRM,stop)
def probe(R):
 sub=M.half_e6_subrings(R)
 if not sub:raise M.Ineligible('no half-E6 based subcategory')
 g,x=sub[0];d=M.data_for(R,3,60);tab=d['tab'];tested=0
 for cols in d['lows']:
  if M.low_failure(cols,d['ch'].C,d['ds'],d['D'],d['K'],d['embedding'],d['ch'].du):continue
  if not M.half_e6_low_allowed(cols,g,x):continue
  for lab in tab.assignments(cols):
   for ep in M.indicator_choices(R):
    if ep[g-1]!=1 or ep[x-1]!=1:continue
    A,b,meta=M.system(R,d,cols,ep,lab,g,x,False);tested+=1
    if A is not None and M.cached_farkas(A,b)is None:return {'outcome':'necessary_system_survives','systems_tested':tested}
 return {'outcome':'pseudo_unitary_excluded','systems_tested':tested}
for rr in D:
 rid=rr['id'];R=C[rid];st=time.monotonic();r={'id':rid,'inherited_status':rr['inherited_status']}
 if rid=='R6_6_1035':r.update(outcome='covered_by_complete_exact_certificate',certificate='R6_6_1035_general.json')
 else:
  signal.alarm(20)
  try:r.update(probe(R))
  except M.Ineligible as e:r.update(outcome='ineligible',reason=str(e))
  except TimeoutError as e:r.update(outcome='budget_incomplete',reason=str(e))
  except Exception as e:r.update(outcome='error',reason=repr(e))
  finally:signal.alarm(0)
 r['seconds']=time.monotonic()-st;out.append(r);Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(rid,r['outcome'],flush=True)
M.require(len(out)==64,'unexpected inherited scope');M.require(not any(r['outcome']=='pseudo_unitary_excluded'for r in out),'unexpected control exclusion')
