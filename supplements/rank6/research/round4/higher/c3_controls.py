import sys,json,time,signal
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'));import round4_higher_c3 as M
D=__import__('frozen_inputs').rows(P);C={r['id']:r['N']for r in json.load(open(P/'data/census.json'))};out=[]
def stop(*a):raise TimeoutError('20-second per-control discovery budget')
signal.signal(signal.SIGALRM,stop)
for rr in D:
 if rr['status']=='excluded':continue
 rid=rr['id'];R=C[rid];st=time.monotonic();r={'id':rid,'inherited_status':rr['status']}
 if not M.cyclic_three_subrings(R):r['outcome']='ineligible_no_C3_subcategory'
 elif rid=='R6_6_49':r['outcome']='covered_by_complete_exact_certificate';r['certificate']='R6_6_49_general.json'
 else:
  signal.alarm(20)
  try:
   c=M.certificate(R);r['outcome']='pseudo_unitary_excluded'if c else'necessary_system_survives'
   if c:r['certificate']=c
  except M.Ineligible as e:r.update(outcome='ineligible',reason=str(e))
  except TimeoutError as e:r.update(outcome='budget_incomplete',reason=str(e))
  except Exception as e:r.update(outcome='error',reason=repr(e))
  finally:signal.alarm(0)
 r['seconds']=time.monotonic()-st;out.append(r);Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(rid,r['outcome'],flush=True)
M.require(len(out)==64,'unexpected inherited control size');M.require(not any(r['outcome']=='pseudo_unitary_excluded'for r in out),'unexpected control exclusion')
