"""Exhaustive applicability plus bounded exact subcategory checks on all64 inputs."""
import json,sys,time,signal
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'));import round4_higher_mass as M
from round4_higher_fast import half_e6_subrings,cyclic_three_subrings
import round3_m4 as A
from exact import require
C={r['id']:r['N']for r in json.load(open(P/'data/census.json'))};selected=__import__('frozen_inputs').rows(P);out={'inputs':len(selected),'records':[]}
def stop(*a):raise TimeoutError('30-second per-input discovery budget')
signal.signal(signal.SIGALRM,stop)
for rr in selected:
 rid=rr['id'];R=C[rid];r={'id':rid,'inherited_status':rr['status'],'half_e6_subrings':half_e6_subrings(R),'cyclic_three_subrings':cyclic_three_subrings(R)};st=time.monotonic()
 if not r['half_e6_subrings']:r['mass_outcome']='ineligible_no_subcategory'
 else:
  signal.alarm(30)
  try:
   cert,partial=M.certificate(R);r['mass_outcome']='pseudo_unitary_excluded'if cert else'necessary_system_survives';r['low_frames_seen']=len(partial['branches'])
   if cert:r['certificate']=cert
  except M.Ineligible as e:r.update(mass_outcome='ineligible',reason=str(e))
  except TimeoutError as e:r.update(mass_outcome='budget_incomplete',reason=str(e))
  except Exception as e:r.update(mass_outcome='error',reason=repr(e))
  finally:signal.alarm(0)
 r['seconds']=time.monotonic()-st;out['records'].append(r);Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(rid,r['mass_outcome'],flush=True)
require(len(selected)==64,'unexpected fourth-round inherited frontier/control size')
require(all(not r['mass_outcome'].endswith('excluded')for r in out['records']if r['inherited_status']!='unresolved'),'false-positive model exclusion')
# Exact source checks for all3cyclic pointed associators.
K=A.field(A.s.Poly(A.s.cyclotomic_poly(24,A.s.Symbol('t')),A.s.Symbol('t')));tests=[]
for omega in range(3):
 for a in[1,2]:
  seqs=[tuple(A.relative_root(K,24,9,(omega*a*a+3*a*b)*k)for k in[1,2,3])for b in range(3)]
  want=[tuple(K.unit**((24//3)*b*k%24)for k in[1,2,3])for b in range(3)]if omega==0 else[tuple(A.relative_root(K,24,9,omega*k)for k in[1,2,3])]*3
  require(sorted(seqs,key=str)==sorted(want,key=str),'cyclic-three source twist domain mismatch');tests.append({'omega':omega,'flux':a,'passed':True})
out['cyclic_pointed_source_checks']=tests;out['false_positive_exclusions']=0;Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
