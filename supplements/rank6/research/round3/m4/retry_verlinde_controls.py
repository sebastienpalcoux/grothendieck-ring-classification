import sys,json,time,signal
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'))
import round3_verlinde as v
rows={r['id']:r for r in json.load(open(P/'data/census.json'))};src=json.load(open(Path(__file__).with_name('verlinde_controls.json')))
ids=[r['id'] for r in src['records'] if r['input_kind']=='positive_model' and r['outcome']=='budget_incomplete'];original=v.indicator_choices;v.indicator_choices=lambda R:list(reversed(original(R)))
rec={'scope':'pseudo_unitary_positive_controls','criterion':'low-Verlinde/restriction-product','height':6,'per_input_seconds':75,'indicator_search_order':'reverse (only existence of a surviving branch is recorded)','records':[]};out=Path(__file__).with_suffix('.json')
def stop(*_):raise TimeoutError('budget')
signal.signal(signal.SIGALRM,stop)
for rid in ids:
 st=time.monotonic();signal.alarm(75);r={'id':rid}
 try:
  x=v.certificate(rows[rid]['N'],6)
  if x is not None:raise RuntimeError('positive control rejected')
  r.update(outcome='no_exact_obstruction')
 except TimeoutError:r.update(outcome='budget_incomplete')
 finally:signal.alarm(0)
 r['seconds']=time.monotonic()-st;rec['records'].append(r);out.write_text(json.dumps(rec,indent=2)+'\n');print(r,flush=True)
