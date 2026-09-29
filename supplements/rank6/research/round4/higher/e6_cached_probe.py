import sys,json,time,signal,traceback
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'))
import round4_higher_e6 as m
rid=sys.argv[1]if len(sys.argv)>1 else 'R6_6_1035';R=next(r['N']for r in json.load(open(P/'data/census.json'))if r['id']==rid);st=time.monotonic();out={'id':rid,'scope':'pseudo_unitary','branches':[]};path=Path(__file__).with_name(rid+'_half_e6_cached.json')
def stop(*a):raise TimeoutError('840-second external budget')
signal.signal(signal.SIGALRM,stop);signal.alarm(840)
try:
 data=m.data_for(R,3,60);tab=data['tab'];g,x=m.half_e6_subrings(R)[0];out['metadata']=m.metadata(data);out['subring']=[0,g,x]
 print('data',out['metadata'],time.monotonic()-st,flush=True)
 for ix,cols in enumerate(data['lows']):
  why=m.low_failure(cols,data['ch'].C,data['ds'],data['D'],data['K'],data['embedding'],data['ch'].du);br={'low':ix,'columns':list(map(list,cols))};out['branches'].append(br)
  if why:br['ordinary']=why;continue
  if not m.half_e6_low_allowed(cols,g,x):br['center_branching_rejected']=True;continue
  labs=tab.assignments(cols);br['labellings']=list(map(list,labs));br['cases']=[]
  for lab in labs:
   for conj in [False]:
    for ep in m.indicator_choices(R):
     if ep[g-1]!=1 or ep[x-1]!=1:continue
     print('build',ix,conj,ep,time.monotonic()-st,flush=True)
     A,b,meta=m.system(R,data,cols,ep,lab,g,x,conj);print('farkas',len(A),len(A[0]),time.monotonic()-st,flush=True)
     ray=m.cached_farkas(A,b);rec={'labelling':list(lab),'conjugate':conj,'indicators':list(ep),'system':meta,'ray':ray,'excluded':ray is not None};br['cases'].append(rec);print('result',ray is not None,time.monotonic()-st,flush=True)
     path.write_text(json.dumps(out,separators=(',',':'))+'\n')
     if ray is None:raise RuntimeError('no_exact_obstruction')
 out['outcome']='pseudo_unitary_excluded'
except Exception as e:out.update(outcome='budget_incomplete'if isinstance(e,TimeoutError)else str(e));traceback.print_exc()
finally:signal.alarm(0);out['seconds']=time.monotonic()-st;path.write_text(json.dumps(out,separators=(',',':'))+'\n')
