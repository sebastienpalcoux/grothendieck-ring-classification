import sys,json,time
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'))
import round3_verlinde as V
import galois_pseudo_reduction as G
from exact import require
R=next(x['N'] for x in json.load(open(P/'data/census.json')) if x['id']=='R6_4_243');st=time.monotonic();raw=json.load(open(Path(__file__).with_name('probe_243.json')));require(raw['outcome']=='pseudo_unitary_excluded','raw discovery incomplete')
data,tab=V.data_for(R);index={(r['low'],tuple(r['lab']),tuple(r['indicators'])):r for r in raw['branches'] if 'lab' in r};used=set()
c={'kind':'low_verlinde_restriction','version':1,'scope':'pseudo_unitary','height':6,'q':data['q'],'table':tab.metadata(),'column_counts':list(map(len,data['columns'])),'branches':[]}
for ix,cols in enumerate(data['lows']):
 br={'columns':list(map(list,cols))};c['branches'].append(br);why=V.low_failure(cols,data['ch'].C,data['ds'],data['D'],data['K'],data['embedding'],data['ch'].du)
 if why:br['ordinary']=why;continue
 labs=tab.assignments(cols);br['labellings']=list(map(list,labs));br['cases']=[]
 for lab in labs:
  for ep in V.indicator_choices(R):
   key=(ix,tuple(lab),tuple(ep));r=index[key];used.add(key);br['cases'].append({'labelling':list(lab),'indicators':list(ep),'rows':r['rows'],'variables':r['variables'],'ray':r['ray'],'congruence':r['congruence']})
require(set(index)==used,'raw branch not in exhaustive domain')
red=G.certificate(R,timeout=120);require(red is not None,'general reduction absent');meta=G.verify(R,red)
z={'kind':'general_low_verlinde_restriction','version':1,'scope':'general','reduction':red,'pseudo':c}
Path(__file__).with_name('R6_4_243_general.json').write_text(json.dumps({'id':'R6_4_243','certificate':z,'reduction_verification':meta,'seconds':time.monotonic()-st},separators=(',',':'))+'\n');print(meta,'cases',len(used),'seconds',time.monotonic()-st,flush=True)
