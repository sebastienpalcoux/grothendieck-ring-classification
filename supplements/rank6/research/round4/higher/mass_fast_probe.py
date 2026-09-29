import sys,json,time,signal,traceback
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'));import round4_higher_mass as m
rid=sys.argv[1]if len(sys.argv)>1 else 'R6_6_1035';R=next(r['N']for r in json.load(open(P/'data/census.json'))if r['id']==rid);st=time.monotonic();out={'id':rid};p=Path(__file__).with_name(rid+'_projection_mass.json')
def stop(*a):raise TimeoutError('840-second budget')
def progress(ix,meta,y):print(ix,meta['variables'],meta['rows'],y is not None,time.monotonic()-st,flush=True)
signal.signal(signal.SIGALRM,stop);signal.alarm(840)
try:
 c,partial=m.certificate(R,progress);out.update(outcome='pseudo_unitary_excluded'if c else'no_exact_obstruction',certificate=c,partial=partial)
except Exception as e:out.update(outcome='budget_incomplete'if isinstance(e,TimeoutError)else'error',reason=str(e));traceback.print_exc()
finally:signal.alarm(0);out['seconds']=time.monotonic()-st;p.write_text(json.dumps(out,separators=(',',':'))+'\n')
