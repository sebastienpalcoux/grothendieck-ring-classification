"""Complete the single eligible realized control whose short pass timed out."""
import sys,json,time,signal,traceback
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'));import round4_higher_e6 as M
source=Path(__file__).with_name('e6_controls.py').read_text();exec(source[source.index('def probe(R):'):source.index('\nfor rr in D:')])
R=next(r['N']for r in json.load(open(P/'data/census.json'))if r['id']=='R6_2_127');st=time.monotonic();out={'id':'R6_2_127','inherited_status':'unitarily_realized','budget_seconds':180}
def stop(*a):raise TimeoutError('180-second eligible-positive retry budget')
signal.signal(signal.SIGALRM,stop);signal.alarm(180)
try:out.update(probe(R));M.require(out['outcome']=='necessary_system_survives','realized positive control excluded')
except Exception as e:out.update(outcome='budget_incomplete'if isinstance(e,TimeoutError)else'error',reason=str(e));traceback.print_exc()
finally:signal.alarm(0);out['seconds']=time.monotonic()-st;Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(out,flush=True)
