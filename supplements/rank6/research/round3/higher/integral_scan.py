"""Apply the new modular Morita test to every current frontier and all models."""
import sys,json,time,signal,collections
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'software'));import round3_integral_morita as IM;import stabilizer_rotation_higher as H
D=Path(__file__).parent;C={r['id']:r['N']for r in json.load(open(ROOT/'data/census.json'))};frontier=[r['id']for r in json.load(open(ROOT/'data/unresolved_tensors.json'))];models=[r['id']for r in json.load(open(ROOT/'data/model_catalog.json'))]
def end(*a):raise TimeoutError('60-second per-input modular Morita budget')
signal.signal(signal.SIGALRM,end);out=[]
for name in frontier+models:
 R=C[name];start=time.monotonic();row={'id':name,'input_group':'frontier'if name in frontier else 'model'};signal.alarm(60)
 try:
  if any(R[i][j]!=R[j][i]for i in range(6)for j in range(6)):raise H.Ineligible('commutative module implementation')
  infos=[(g,H.anti_representations(R,g))for g in H.invs(R)];infos=[z for z in infos if z[1]is not None]
  if not infos:raise H.Ineligible('no eligible forced involution module')
  logs=[];excluded=False
  for g,(fixed,seed,nodes,reps)in infos:
   methods=[]
   for T in reps:
    ab,meta=H.C.morita_system(R,g,fixed,T)
    if ab is None:methods.append('rank');continue
    c=IM.modular_ray(*IM.reduced(*ab),2)
    if c is not None:IM.verify_system(*ab,c);methods.append('modular')
    else:methods.append('survives');break
   logs.append({'g':g,'module_branches':len(reps),'visited':len(methods),'outcomes':methods})
   if len(methods)==len(reps)and 'survives'not in methods:excluded=True;break
  row.update(outcome='excluded'if excluded else 'no_modular_obstruction',module_runs=logs)
  if excluded and name in models:raise RuntimeError('false modular exclusion of model')
 except H.Ineligible as e:row.update(outcome='ineligible',reason=str(e))
 except TimeoutError as e:row.update(outcome='budget_incomplete',reason=str(e))
 finally:signal.alarm(0)
 row['seconds']=time.monotonic()-start;out.append(row);(D/'integral_scan.json').write_text(json.dumps(out)+'\n');print({k:v for k,v in row.items()if k!='module_runs'},flush=True)
