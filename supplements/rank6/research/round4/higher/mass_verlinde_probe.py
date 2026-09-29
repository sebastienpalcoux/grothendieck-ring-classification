import sys,json,time,signal,traceback
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'));import round4_higher_mass as m
rid='R6_6_1035';R=next(r['N']for r in json.load(open(P/'data/census.json'))if r['id']==rid);st=time.monotonic();out={'id':rid,'branches':[]};p=Path(__file__).with_suffix('.json')
def stop(*a):raise TimeoutError('840-second budget')
signal.signal(signal.SIGALRM,stop);signal.alarm(840)
try:
 d=m.data_for(R);tab=d['tab'];g,x=m.half_e6_subrings(R)[0]
 for ix in[1,3]:
  cols=d['lows'][ix]
  for lab in tab.assignments(cols):
   A,b,meta=m.system(R,d,cols,g,x);A,b=m.add_verlinde(R,d,cols,lab,A,b,meta['labels']);print('system',ix,len(A),len(A[0]),time.monotonic()-st,flush=True);y=m.farkas(A,b);print('ray',y is not None,time.monotonic()-st,flush=True);out['branches'].append({'low':ix,'labelling':list(lab),'system':meta,'rows':len(A),'variables':len(A[0]),'ray':y});p.write_text(json.dumps(out,separators=(',',':'))+'\n')
 out['outcome']='pseudo_unitary_excluded'if all(r['ray']is not None for r in out['branches'])else'no_exact_obstruction'
except Exception as e:out.update(outcome='budget_incomplete'if isinstance(e,TimeoutError)else'error',reason=str(e));traceback.print_exc()
finally:signal.alarm(0);out['seconds']=time.monotonic()-st;p.write_text(json.dumps(out,separators=(',',':'))+'\n')
