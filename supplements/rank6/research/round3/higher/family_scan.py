import sys,json,time,signal
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'software'));import stabilizer_rotation_higher as H
D=Path(__file__).parent;C=json.load(open(ROOT/'data/census.json'));template=next(r['N']for r in C if r['id']=='R6_5_638');out=[]
def end(*a):raise TimeoutError('90-second per-input family discovery budget')
signal.signal(signal.SIGALRM,end)
for p in (1,3,5,7):
 R=json.loads(json.dumps(template))
 for i in range(2,6):
  for j in range(2,6):
   for k in range(2,6):R[i][j][k]+=p-4
 ids=[r['id']for r in C if r['N']==R];row={'parameter':p,'matching_ids':ids};t=time.monotonic();signal.alarm(90)
 try:c=H.certificate(R,height=6);H.verify(R,c);row.update(outcome='pseudo_unitary_excluded',certificate=c)
 except H.Ineligible as e:row.update(outcome='ineligible',reason=str(e))
 except H.Survives as e:row.update(outcome='no_exact_obstruction',reason=str(e))
 except Exception as e:row.update(outcome='incomplete',reason=str(e))
 finally:signal.alarm(0)
 row['seconds']=time.monotonic()-t;out.append(row);(D/'family_scan.json').write_text(json.dumps(out)+'\n');print({k:v for k,v in row.items()if k!='certificate'},flush=True)
