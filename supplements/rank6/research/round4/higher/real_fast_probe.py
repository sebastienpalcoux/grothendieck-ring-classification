import sys,json,time,signal,traceback
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'));import round4_higher_real as m
rid='R6_6_1035';R=next(r['N']for r in json.load(open(P/'data/census.json'))if r['id']==rid);st=time.monotonic();out={'id':rid,'branches':[]};p=Path(__file__).with_name(rid+'_projection_real_fast.json')
def stop(*a):raise TimeoutError('840-second budget')
signal.signal(signal.SIGALRM,stop);signal.alarm(840)
try:
 d=m.data_for(R);tab=d['tab'];out['trace_metadata']=d['trace_metadata'];print('data',d['trace_metadata'],time.monotonic()-st,flush=True)
 for ix,cols in enumerate(d['lows']):
  br={'low':ix,'columns':list(map(list,cols))};out['branches'].append(br);why=m.low_failure(cols,d['ch'].C,d['ds'],d['D'],d['K'],d['embedding'],d['ch'].du)
  if why:br['ordinary']=why;continue
  g,x=m.half_e6_subrings(R)[0]
  if not m.half_e6_low_allowed(cols,g,x):br['low_branching_failure']=True;continue
  labs=tab.assignments(cols);br['labellings']=list(map(list,labs));br['cases']=[]
  for lab in labs:
   for ep in m.ambient.indicator_choices(R):
    if ep[g-1]!=1 or ep[x-1]!=1:continue
    A,b,meta=m.system(R,d,cols,ep,lab);print('system',ix,ep,len(A),len(A[0]),time.monotonic()-st,flush=True);y=m.farkas(A,b);print('ray',y is not None,time.monotonic()-st,flush=True)
    br['cases'].append({'labelling':list(lab),'indicators':list(ep),'system':meta,'ray':y});p.write_text(json.dumps(out,separators=(',',':'))+'\n')
    if y is None:raise ValueError('no_exact_obstruction')
 out['outcome']='pseudo_unitary_excluded'
except Exception as e:out.update(outcome='budget_incomplete'if isinstance(e,TimeoutError)else str(e));traceback.print_exc()
finally:signal.alarm(0);out['seconds']=time.monotonic()-st;p.write_text(json.dumps(out,separators=(',',':'))+'\n')
