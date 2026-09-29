import json,sys,time,signal,math
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'))
from rings import Characters
from round4_629_orbits import ambient,orbit_domain,Ineligible
from exact import require
import sympy as s
census={x['id']:x for x in json.load(open(P/'data/census.json'))};ledger=json.load(open(P/'data/decisions.json'));frontier=set(json.load(open(P/'verification/round4/campaign_manifest.json'))['ids']);controls={r['id'] for r in json.load(open(P/'data/model_catalog.json'))};chosen=[dict(r,status='unresolved' if r['id'] in frontier else r['status']) for r in ledger if r['id'] in frontier|controls];require(len(chosen)==64,'frozen campaign/control coverage changed');out=[]
def stop(*a):raise TimeoutError('per-ring 20-second scope budget')
signal.signal(signal.SIGALRM,stop)
for r in chosen:
 st=time.monotonic();rec={'id':r['id'],'ledger_status':r['status'],'scope':'pseudo_unitary_necessary'};signal.alarm(20)
 try:
  R=census[r['id']]['N'];n=len(R)
  if any(R[i][j]!=R[j][i] for i in range(n) for j in range(n)):raise Ineligible('commutative input required')
  ch=Characters(R);f,K,ds,D,pD,ee=ch.fp();ps=set(map(int,s.factorint(abs(int(pD.TC())))))
  if 2 in ps:raise Ineligible('even dimension prime support')
  if pD.degree()!=f.degree() or f.degree()>4:raise Ineligible('global dimension does not generate a supported FP field')
  candidates=[F for F in [1,3,5,15] if set(map(int,s.factorint(F)))==ps]
  if not candidates:raise Ineligible('no supported odd conductor contains the exact prime support')
  for F in candidates:
   try:d=ambient.data_for(R,3,F);break
   except Ineligible:continue
  else:raise Ineligible('no full-character embedding in supported odd conductor')
  dom=orbit_domain(d,10);rec.update(outcome='eligible_domain_constructed',conductor=d['F'],prime_support=d['primes'],low_frames=len(d['lows']),domain_bound=10,trace_types=len(dom))
 except Ineligible as e:rec.update(outcome='ineligible',reason=str(e))
 except TimeoutError as e:rec.update(outcome='budget_incomplete',reason=str(e))
 except Exception as e:rec.update(outcome='error',reason=repr(e))
 finally:signal.alarm(0)
 rec['seconds']=time.monotonic()-st;out.append(rec);print(rec,flush=True);Path(__file__).with_suffix('.json').write_text(json.dumps(out))
