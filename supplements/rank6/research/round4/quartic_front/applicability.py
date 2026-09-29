import sys,json,time,signal,hashlib
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'software'))

def run(arg):
 rid,R,status=arg;st=time.monotonic()
 def stop(*_):raise TimeoutError('120-second applicability budget')
 signal.signal(signal.SIGALRM,stop);signal.alarm(120)
 try:
  from rings import Characters
  from character_induction import Ineligible
  from round3_m4 import data_for
  if any(R[i][j]!=R[j][i] for i in range(len(R)) for j in range(len(R))):raise Ineligible('commutative ring required')
  degree=Characters(R).fp()[0].degree()
  if degree!=4:raise Ineligible('quartic FP field required; degree='+str(degree))
  d=data_for(R,3);out={'outcome':'eligible','ambient_conductor':d['F'],'low_frames':len(d['lows'])}
 except Ineligible as e:out={'outcome':'ineligible','reason':str(e)}
 except TimeoutError as e:out={'outcome':'budget_incomplete','reason':str(e)}
 except Exception as e:out={'outcome':'error','reason':type(e).__name__+': '+str(e)}
 finally:signal.alarm(0)
 return dict(id=rid,status=status,tensor_sha256=hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest(),seconds=time.monotonic()-st,**out)
if __name__=='__main__':
 rings={x['id']:x['N'] for x in json.load(open(ROOT/'data/census.json'))};decs=json.load(open(ROOT/'data/decisions.json'));selected=[(d['id'],rings[d['id']],d['status']) for d in decs if d['status']!='excluded'];require=lambda x:None if x else (_ for _ in ()).throw(ValueError('expected64'));require(len(selected)==64)
 with ProcessPoolExecutor(max_workers=3) as ex:records=list(ex.map(run,selected))
 out=dict(scope='quartic_full_character_profile_implementation_applicability',frontier_count=10,positive_count=54,records=records);Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print([(x['id'],x['outcome']) for x in records if x['outcome']!='ineligible']);print('outcomes',__import__('collections').Counter(x['outcome'] for x in records))
