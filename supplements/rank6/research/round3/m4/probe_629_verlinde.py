import sys,json,time,signal
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path[:0]=[str(P/'software'),str(P/'research/round3/quartic')]
import round3_m4 as m
from verlinde_probe import verlinde
from exact import require
from spectral_induction import Spectrum
from higher_traces import farkas,check_farkas
R=next(x['N'] for x in json.load(open(P/'data/census.json')) if x['id']=='R6_4_629');st=time.monotonic();out=Path(__file__).with_suffix('.json');rec={'id':'R6_4_629','scope':'pseudo_unitary_necessary','height':3,'branches':[]}
def stop(*_):raise TimeoutError('budget')
signal.signal(signal.SIGALRM,stop);signal.alarm(840)
try:
 data=m.data_for(R,3,15);tab=data['tab'];rec['metadata']=m.metadata(data)
 for ix,cols in enumerate(data['lows']):
  why=m.low_failure(cols,data['ch'].C,data['ds'],data['D'],data['K'],data['embedding'],data['ch'].du)
  if why:rec['branches'].append({'low':ix,'ordinary':why});continue
  labs=tab.assignments(cols)
  for lab in labs:
   for ep in m.indicator_choices(R):
    A,b,meta=m.system(R,data,cols,ep,lab)
    if A is None:rec['branches'].append({'low':ix,'lab':lab,'ep':ep,'spectrum':meta});continue
    G,vs=m.high_vectors(data,cols);sp=Spectrum(tab,cols,[(v,None) for v in vs]);bad=set(map(tuple,sp.forbidden));labels=[(v,ti) for v in vs if v not in bad for ti in range(len(data['phases']))]
    A,b,labels,base=verlinde(R,data,tab,cols,lab,A,b,labels)
    y=farkas(A,b)
    if y:check_farkas(A,b,y)
    z={'low':ix,'lab':lab,'ep':ep,'rows':len(A),'variables':len(A[0]),'ray':y};rec['branches'].append(z);out.write_text(json.dumps(rec,separators=(',',':'))+'\n');print(ix,lab,ep,len(A),len(A[0]),'excluded',y is not None,flush=True)
    if y is None:raise ValueError('necessary system survives')
 rec['outcome']='pseudo_unitary_excluded'
except TimeoutError:rec['outcome']='budget_incomplete'
except ValueError as e:rec['outcome']='no_exact_obstruction';rec['reason']=str(e)
finally:signal.alarm(0)
rec['seconds']=time.monotonic()-st;out.write_text(json.dumps(rec,separators=(',',':'))+'\n');print(rec['outcome'],rec['seconds'],flush=True)
