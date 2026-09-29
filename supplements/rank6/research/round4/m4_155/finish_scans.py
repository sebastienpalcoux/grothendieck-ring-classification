"""Resume only missing control inputs, with a hard subprocess wall limit."""
import sys,json,time,subprocess,concurrent.futures,os
from pathlib import Path
P=Path(__file__).resolve().parents[3];base=Path(__file__).parent
kind=sys.argv[1] if len(sys.argv)>1 else 'scan_quartic_controls';path=base/(kind+'.json');old=json.loads(path.read_text());done={r['id'] for r in old['records']};R={r['id']:r['N'] for r in json.load(open(P/'data/census.json'))};sys.path.insert(0,str(P/'software'));import round4_155 as V;tasks=[t for t in V.frozen_control_tasks(P) if t[0] not in done]
script="import sys,json;sys.path[:0]=["+repr(str(base))+"];from "+kind+" import one;print(json.dumps(one(json.loads(sys.stdin.read()))))"
def run(arg):
 st=time.monotonic()
 try:
  p=subprocess.run([sys.executable,'-c',script],input=json.dumps(arg),text=True,capture_output=True,timeout=32,cwd=P,env={**os.environ,'OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1'})
  if p.returncode:return {'id':arg[0],'status':arg[2],'outcome':'subprocess_error','reason':p.stderr[-1000:],'seconds':time.monotonic()-st}
  return json.loads(p.stdout)
 except subprocess.TimeoutExpired:return {'id':arg[0],'status':arg[2],'criterion':kind,'outcome':'wall_clock_budget_incomplete','reason':'The fresh subprocess was terminated after its 32-second wall-clock budget. No feasibility or infeasibility claim.','seconds':time.monotonic()-st,'hard_wall_limit_seconds':32}
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
 for r in ex.map(run,tasks):
  old['records'].append(r);old['records'].sort(key=lambda x:x['id']);old['complete']=len(old['records'])==old['input_count'];path.write_text(json.dumps(old,indent=2)+'\n');print(r['id'],r['outcome'],flush=True)
