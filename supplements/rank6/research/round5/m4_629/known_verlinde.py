import sys,json,time,itertools
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'));from round5_629 import *
here=Path(__file__).parent;R,d,cols,lab,src=source_data();C=d['C'];out=[];st=time.monotonic()
for branch in json.load(open(here/'modular_closure.json')):
 known=branch['known_class_rows'];rows=[[C([s.Rational(z) for z in vals]) for vals in r['S_image']] for r in known];unit=next(j for j,x in enumerate(known) if x['indices']==[0]);s0=rows[unit];bad=[];count=0;nn={}
 for i,j,k in itertools.combinations_with_replacement(range(len(rows)),3):
  z=sum((a*b*c/dd for a,b,c,dd in zip(rows[i],rows[j],rows[k],s0)),C.zero);count+=1
  co=z.to_list();q=s.Rational(co[0]) if len(co)==1 else s.Integer(0) if not co else None
  if q is None or q.q!=1 or q<0:
   bad.append({'triple':[i,j,k],'objects':[known[t]['indices'] for t in [i,j,k]],'coefficient':list(map(str,co))});print('BAD',branch['rank'],bad[-1],flush=True);break
  nn[i,j,k]=int(q)
 out.append({'rank':branch['rank'],'solution':branch['solution'],'known_objects':[x['indices'] for x in known],'triple_checks':count,'failures':bad,'coefficients':[[list(t),v] for t,v in nn.items()]});(here/'known_verlinde.json').write_text(json.dumps(out));print('rank',branch['rank'],'checks',count,'failures',len(bad),'seconds',time.monotonic()-st,flush=True)
