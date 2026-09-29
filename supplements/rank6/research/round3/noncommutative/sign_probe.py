import sys,json,subprocess,tempfile,re
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[3]/'software'))
from oriented_signed import problem,validate_general
from signed import from_values,gauge_original
root=Path(__file__).resolve().parents[3]
R=next(r['N'] for r in json.load(open(root/'data/unresolved_tensors.json')) if r['id']=='R6_6_170')
p=problem(R,normalized=False);source=p['source']
for i,dom in enumerate(p['domains']):
 bound=max(map(abs,dom));d=[v for v in dom if abs(v)==bound]
 source,count=re.subn(r'for\(int x:vector<int>\{[^}]+\}\)\{v\['+str(i)+r'\]=x;', 'for(int x:vector<int>{'+','.join(map(str,d))+'}){v['+str(i)+']=x;',source)
 assert count==1
with tempfile.TemporaryDirectory() as td:
 cpp=Path(td)/'enum.cpp';exe=Path(td)/'enum';cpp.write_text(source)
 subprocess.run(['g++','-std=c++17','-O3',str(cpp),'-o',str(exe)],check=True)
 run=subprocess.run([str(exe)],capture_output=True,text=True,check=True,timeout=120)
print(run.stderr,flush=True)
vals=sorted(tuple(map(int,x.split())) for x in run.stdout.splitlines());out=[]
for v in vals:
 T=from_values(R,p,v);validate_general(T);g=gauge_original(T,R);out.append({'values':list(v),'gauge':g})
print('values',len(vals),'ungauged',sum(x['gauge'] is None for x in out),flush=True)
(root/'research/round3/noncommutative/sign_probe.json').write_text(json.dumps({'statistics':run.stderr,'tables':out},indent=2)+'\n')
