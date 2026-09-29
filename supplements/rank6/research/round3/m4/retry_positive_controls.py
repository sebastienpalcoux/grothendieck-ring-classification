import sys,json,time,signal,contextlib
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'))
import round3_m4 as m
rows={r['id']:r for r in json.load(open(P/'data/census.json'))};src=json.load(open(Path(__file__).with_name('scan_controls.json')))
ids=[r['id'] for r in src['records'] if r['input_kind']=='positive_model' and r['outcome']=='budget_incomplete'];original=m.indicator_choices;m.indicator_choices=lambda R:list(reversed(original(R)))
rec={'scope':'pseudo_unitary_positive_controls','criterion':'ambient full-character moments','height':3,'per_input_seconds':120,'indicator_search_order':'reverse (only existence of a surviving branch is recorded)','records':[]};out=Path(__file__).with_suffix('.json')
def stop(*_):raise TimeoutError('budget')
signal.signal(signal.SIGALRM,stop)
for rid in ids:
 st=time.monotonic();signal.alarm(120);r={'id':rid}
 try:
  with open(Path(__file__).with_suffix('.detail.log'),'a') as log,contextlib.redirect_stdout(log):x=m.run(rows[rid]['N'],3)
  if x['outcome']!='no_exact_obstruction':raise RuntimeError('positive control did not survive')
  r.update(outcome=x['outcome'],metadata=x['metadata'])
 except TimeoutError:r.update(outcome='budget_incomplete')
 finally:signal.alarm(0)
 r['seconds']=time.monotonic()-st;rec['records'].append(r);out.write_text(json.dumps(rec,indent=2)+'\n');print(r,flush=True)
