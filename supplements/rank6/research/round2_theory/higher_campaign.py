"""Uniform exact-status ledger for the inherited unresolved census inputs.

This research index does not modify the classification ledger. Positive outcomes
refer to full certificates; no separating ray, ineligible input, and interrupted
finite domains remain distinct.
"""
import json,sys,signal,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'software'))
import stabilizer_rotation_higher as H
DIR=Path(__file__).parent
cp=DIR/'higher_campaign_inputs.json'
if not cp.exists():
 rows=json.load(open(ROOT/'data/decisions.json'))
 cp.write_text(json.dumps([{'id':r['id'],'m':r['m']} for r in rows if r['existence']['general']=='unknown'],indent=2)+'\n')
inputs=json.load(open(cp));census={r['id']:r['N'] for r in json.load(open(ROOT/'data/census.json'))}

def budget(*a):raise TimeoutError('explicit 90-second unreported-input budget')
signal.signal(signal.SIGALRM,budget);out=[]
for row in inputs:
 name=row['id'];R=census[name];rec={**row}
 reports=[]
 for suffix,h in [('_higher.json',3),('_higher_h6.json',6),('_higher_h6_resumed.json',6)]:
  p=DIR/(name+suffix)
  if p.exists():
   rr=json.load(open(p));reports.append({'height':h,'path':str(p.relative_to(ROOT)),'outcome':rr['outcome'],'seconds':rr.get('seconds')})
 if reports:
  good=next((r for r in reports if r['outcome']=='pseudo_unitary_excluded'),None)
  if good:rec.update(outcome='pseudo_unitary_excluded',certificate_record=good['path'])
  else:rec['outcome']='no_exact_obstruction' if any(r['outcome'] in ('no_exact_obstruction','survives_necessary_conditions') for r in reports) else reports[-1]['outcome']
  rec['runs']=reports
 elif row['m']==3:
  rec.update(outcome='handled_by_dimension_two_stabilizer_campaign',note='Separate full general certificate; this file indexes higher-dimensional follow-up.')
 else:
  signal.alarm(90);start=time.monotonic()
  try:
   cert=H.certificate(R,height=3);signal.alarm(0);H.verify(R,cert)
   p=DIR/(name+'_higher.json');p.write_text(json.dumps({'id':name,'outcome':'pseudo_unitary_excluded','certificate':cert,'seconds':time.monotonic()-start},separators=(',',':'))+'\n')
   rec.update(outcome='pseudo_unitary_excluded',certificate_record=str(p.relative_to(ROOT)))
  except H.Ineligible as e:rec.update(outcome='ineligible',reason=str(e))
  except H.Survives as e:rec.update(outcome='no_exact_obstruction',reason=str(e))
  except TimeoutError as e:rec.update(outcome='budget_incomplete',reason=str(e))
  finally:signal.alarm(0)
  rec['seconds']=time.monotonic()-start
 out.append(rec);(DIR/'higher_campaign.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(rec),flush=True)
