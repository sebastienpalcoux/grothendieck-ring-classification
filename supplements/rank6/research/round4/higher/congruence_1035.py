import sys,json,time,signal,traceback,pickle
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'));import round4_higher_real as m
from sparse_congruence import witness
import modular_moments as MM
rid='R6_6_1035';R=next(r['N']for r in json.load(open(P/'data/census.json'))if r['id']==rid);st=time.monotonic();out={'id':rid,'branches':[]};p=Path(__file__).with_suffix('.json')
def stop(*a):raise TimeoutError('840-second budget')
signal.signal(signal.SIGALRM,stop);signal.alarm(840)
try:
 d=m.data_for(R);tab=d['tab'];cols=d['lows'][1];lab=tab.assignments(cols)[0]
 for ep in[(1,1,1,1,-1),(1,1,1,1,1)]:
  A,b,meta=m.system(R,d,cols,ep,lab);base=len(A[0]);A,b=m.add_verlinde(R,d,cols,lab,A,b,meta['labels']);integ=[int(j<len(meta['labels'])or j>=base)for j in range(len(A[0]))]
  pickle.dump((A,b,integ,meta,lab,ep),open(P.parent/('higher_1035_system_'+str(ep[-1])+'.pkl'),'wb'))
  print('system',ep,len(A),len(A[0]),time.monotonic()-st,flush=True);c=witness(A,b,integ);print('certificate',c,time.monotonic()-st,flush=True)
  if c:MM.check_congruence(A,b,integ,c)
  out['branches'].append({'indicators':ep,'congruence':c});p.write_text(json.dumps(out,indent=2)+'\n')
 out['outcome']='exact_congruences'if all(r['congruence']for r in out['branches'])else'no_congruence'
except Exception as e:out.update(outcome='budget_incomplete'if isinstance(e,TimeoutError)else'error',reason=str(e));traceback.print_exc()
finally:signal.alarm(0);out['seconds']=time.monotonic()-st;p.write_text(json.dumps(out,indent=2)+'\n')
