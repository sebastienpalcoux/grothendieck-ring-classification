"""Eligibility and explicit positive controls for the higher stabilizer sieve."""
import json,sys,signal,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'software'))
import stabilizer_rotation_higher as H
C={x['id']:x['N'] for x in json.load(open(ROOT/'data/census.json'))}
models=json.load(open(ROOT/'data/model_catalog.json'));out=[]
def limit(*args):raise TimeoutError('positive control reached 120-second per-input budget')
signal.signal(signal.SIGALRM,limit)
for model in models:
 name=model['id'];R=C[name];start=time.monotonic();row={'id':name,'model':model['latex_model']}
 potential=[]
 if all(R[i][j]==R[j][i] for i in range(len(R)) for j in range(len(R))):
  for g in H.invs(R):
   info=H.anti_representations(R,g)
   if info is not None:
    fixed,seed,nodes,reps=info
    if any(H.objects_for(R,g,fixed,T) for T in reps):potential.append(g)
 if not potential:row.update(outcome='ineligible_for_new_local_rotation',involutions=[])
 else:
  row['involutions']=potential;signal.alarm(120)
  try:
   cert=H.certificate(R,height=6)
   H.verify(R,cert)
   row.update(outcome='FALSE_EXCLUSION',certificate=cert)
  except H.Ineligible as e:row.update(outcome='ineligible_trace_domain',reason=str(e))
  except H.Survives as e:row.update(outcome='no_exact_obstruction',reason=str(e))
  except TimeoutError as e:row.update(outcome='budget_incomplete',reason=str(e))
  finally:signal.alarm(0)
 row['seconds']=time.monotonic()-start;out.append(row)
 Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({k:v for k,v in row.items() if k!='certificate'}),flush=True)
 if row['outcome']=='FALSE_EXCLUSION':raise RuntimeError('higher rotation falsely excludes known model')
