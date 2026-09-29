import sys,json,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'software'))
import round3_m4 as m
from induction import low_failure
R=next(r['N'] for r in json.load(open(ROOT/'data/census.json')) if r['id']=='R6_6_1035');data=m.data_for(R,3,60);out=[]
for ix,cols in enumerate(data['lows']):
 why=low_failure(cols,data['ch'].C,data['ds'],data['D'],data['K'],data['embedding'],data['ch'].du)
 labs=[] if why else data['tab'].assignments(cols)
 rec=dict(low=ix,columns=cols,ordinary=why,labellings=labs);out.append(rec);print(rec,flush=True)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2))
