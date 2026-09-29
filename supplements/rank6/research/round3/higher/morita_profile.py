import sys,json,time,signal
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'software'));import stabilizer_rotation_higher as H
D=Path(__file__).parent;C={r['id']:r['N']for r in json.load(open(ROOT/'data/census.json'))};out=[]
def end(*a):raise TimeoutError('180-second module profile budget')
signal.signal(signal.SIGALRM,end)
for name in ['R6_5_638','R6_7_1225']:
 R=C[name];t=time.monotonic();row={'id':name,'involutions':[]};signal.alarm(180)
 try:
  for g in H.invs(R):
   fixed,seed,nodes,reps=H.anti_representations(R,g);records=[]
   for T in reps:
    ab,meta=H.C.morita_system(R,g,fixed,T);record={'T':list(map(list,T)),'objects':H.objects_for(R,g,fixed,T),'meta':meta}
    if ab is None:record['method']='morita_rank'
    else:
     ray=H.C.zero_column_ray(*ab)
     if ray is None:record['method']='survives'
     else:H.check_farkas(*ab,ray);record.update(method='morita_gram',y=ray)
    records.append(record)
   row['involutions'].append({'g':g,'branches':records})
  row['complete']=True
 except Exception as e:row.update(complete=False,reason=str(e))
 finally:signal.alarm(0)
 row['seconds']=time.monotonic()-t;out.append(row);(D/'morita_profiles.json').write_text(json.dumps(out)+'\n');print(name,row['complete'],[[(b['objects'],b['method'])for b in v['branches']]for v in row['involutions']],flush=True)
