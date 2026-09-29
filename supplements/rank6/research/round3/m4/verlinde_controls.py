import sys,json,time,signal,contextlib
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'))
import round3_verlinde as v
from collections import Counter
rows={r['id']:r for r in json.load(open(P/'data/census.json'))};models=json.load(open(P/'data/model_catalog.json'));frontier=json.load(open(P/'data/unresolved_tensors.json'))
ids=[(r['id'],'positive_model') for r in models]+[(r['id'],'frontier') for r in frontier]
report={'criterion':'low-Verlinde/restriction-product/congruence','height':6,'per_input_seconds':25,'records':[]};out=Path(__file__).with_suffix('.json')
def stop(*_):raise TimeoutError('per-input discovery budget')
signal.signal(signal.SIGALRM,stop)
for rid,kind in ids:
 st=time.monotonic();signal.alarm(25);rec={'id':rid,'input_kind':kind}
 try:
  c=v.certificate(rows[rid]['N'],6)
  rec.update(outcome='pseudo_unitary_excluded' if c else 'no_exact_obstruction')
  if c:
   Path(__file__).with_name(rid+'_verlinde_scan_candidate.json').write_text(json.dumps(c,separators=(',',':'))+'\n')
   if kind=='positive_model':raise RuntimeError('positive control rejected')
 except v.Ineligible as e:rec.update(outcome='ineligible',reason=str(e))
 except TimeoutError as e:rec.update(outcome='budget_incomplete',reason=str(e))
 except Exception as e:rec.update(outcome='error',reason=type(e).__name__+': '+str(e))
 finally:signal.alarm(0)
 rec['seconds']=time.monotonic()-st;report['records'].append(rec);report['counts']=dict(Counter(r['outcome'] for r in report['records']));out.write_text(json.dumps(report,indent=2)+'\n');print(rec,flush=True)
