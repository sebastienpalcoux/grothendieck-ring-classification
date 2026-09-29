import sys,json,time,signal,contextlib
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'))
import round3_m4 as m
from collections import Counter
rows={r['id']:r for r in json.load(open(P/'data/census.json'))};models=json.load(open(P/'data/model_catalog.json'));unresolved=json.load(open(P/'data/unresolved_tensors.json'))
ids=[(r['id'],'positive_model') for r in models]+[(r['id'],'frontier') for r in unresolved]
report={'criterion':'ambient full-character cyclotomic rotation/moments','engine_version':2,'height':3,'per_input_seconds':30,'records':[]};out=Path(__file__).with_suffix('.json')
def stop(*_):raise TimeoutError('per-input discovery budget')
signal.signal(signal.SIGALRM,stop)
for rid,kind in ids:
 st=time.monotonic();signal.alarm(30)
 rec={'id':rid,'input_kind':kind}
 try:
  with open(Path(__file__).with_name('scan_detail.log'),'a') as log,contextlib.redirect_stdout(log):z=m.run(rows[rid]['N'],3)
  rec.update(outcome=z['outcome'],metadata=z['metadata'],branches_checked=len(z['branches']))
  if z['outcome']=='pseudo_unitary_excluded':
   Path(__file__).with_name(rid+'_scan_candidate.json').write_text(json.dumps(z,separators=(',',':'))+'\n')
   if kind=='positive_model':raise RuntimeError('positive control rejected')
 except m.Ineligible as e:rec.update(outcome='ineligible',reason=str(e))
 except TimeoutError as e:rec.update(outcome='budget_incomplete',reason=str(e))
 except Exception as e:rec.update(outcome='error',reason=type(e).__name__+': '+str(e))
 finally:signal.alarm(0)
 rec['seconds']=time.monotonic()-st;report['records'].append(rec);report['counts']=dict(Counter(r['outcome'] for r in report['records']));out.write_text(json.dumps(report,indent=2)+'\n');print(rec,flush=True)
