import sys,json,time,hashlib
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'));base=Path(__file__).parent
import scipy.optimize

def disabled(*a,**kw):raise RuntimeError('numerical optimizers disabled')
scipy.optimize.linprog=disabled;scipy.optimize.milp=disabled
import round4_155 as V,round3_m4 as M
from exact import require
from fractions import Fraction
R=next(x['N'] for x in json.load(open(P/'data/census.json')) if x['id']=='R6_4_155');raw=json.load(open(base/'quartic_fixed_probe.json'));c=next(x for x in raw['cases'] if x.get('outcome')=='exact_primal' and x.get('source_pointed_subgroup')==[0,3]);d=M.data_for(R,3,8)
z={k:c[k] for k in ['low','labelling','indicators','rows','variables','values','center_rank']};z.update({'kind':'complex_center_primal','version':1,'height':3,'F':8,'low_columns':list(map(list,d['lows'][c['low']])),'quartic':True,'quartic_cutoff':8,'pointed_subgroup':[0,3]})
st=time.monotonic();A,b,meta=V.primal_system(R,z);z['rows']=len(A);z['variables']=len(A[0]);x=list(map(Fraction,z['values']));require(len(x)==len(A[0]) and all(v>=0 and v.denominator==1 for v in x),'nonintegral or negative witness');x=list(map(int,x));require(all(sum(a*v for a,v in zip(row,x) if a and v)==rhs for row,rhs in zip(A,b)),'quartic/pointed equality failed');report={'passed':True,'optimized_python':not __debug__,'optimizer_used':False,'equations':len(A),'variables':len(x),'center_rank':int(z['center_rank']),'all_coordinates_integral':True,'seconds':time.monotonic()-st,'scope':'necessary_system_survival_only'}
(base/'quartic_exact_primal.json').write_text(json.dumps({'id':'R6_4_155','tensor_sha256':hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest(),'certificate':z},separators=(',',':'))+'\n');(base/('quartic_exact_replay_optimized.json' if not __debug__ else 'quartic_exact_replay.json')).write_text(json.dumps(report,indent=2)+'\n');print(report,flush=True)
