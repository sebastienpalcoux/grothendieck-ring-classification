import sys,json,time,signal
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'))
import modular_moments as m
from spectral_induction import reciprocity_data,low_failure,indicator_choices
from higher_traces import farkas,check_farkas
rid='R6_4_243';R=next(x['N'] for x in json.load(open(P/'data/census.json')) if x['id']==rid)
out=Path(__file__).with_suffix('.json');rec={'id':rid,'scope':'pseudo_unitary_necessary','branches':[]};st=time.monotonic()
def stop(*_):raise TimeoutError('budget')
signal.signal(signal.SIGALRM,stop);signal.alarm(840)
try:
 data,tab=reciprocity_data(R)
 for ix,cols in enumerate(data['lows']):
  why=low_failure(cols,data['ch'].C,data['ds'],data['D'],data['K'],data['embedding'],data['ch'].du)
  if why:rec['branches'].append({'low':ix,'ordinary':why});continue
  for lab in tab.assignments(cols):
   for ep in indicator_choices(R):
    A,b,meta=m.system(R,data,tab,cols,ep,6,lab,cubic=True,restriction_products=True,rational_rotations=True)
    y=farkas(A,b);cong=None
    if y is not None:check_farkas(A,b,y)
    else:
     cong=m.congruence_witness(A,b,meta['integrality'])
     if cong:m.check_congruence(A,b,meta['integrality'],cong)
    r={'low':ix,'lab':lab,'indicators':ep,'rows':len(A),'variables':len(A[0]),'ray':y,'congruence':cong};rec['branches'].append(r)
    print(ix,lab,ep,'excluded',bool(y or cong),flush=True)
    out.write_text(json.dumps(rec,separators=(',',':'))+'\n')
    if y is None and cong is None:raise ValueError('necessary system survives')
 rec['outcome']='pseudo_unitary_excluded'
except TimeoutError as e:rec['outcome']='budget_incomplete';rec['reason']=str(e)
except ValueError as e:rec['outcome']='no_exact_obstruction';rec['reason']=str(e)
rec['seconds']=time.monotonic()-st;out.write_text(json.dumps(rec,separators=(',',':'))+'\n');print(rec['outcome'],rec['seconds'],flush=True)
