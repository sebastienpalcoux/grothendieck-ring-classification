"""Exhaust the commutative sector of the unrestricted oriented signed box."""
import json,sys,time,itertools,re,tempfile,subprocess,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'software'))
from oriented_signed import problem,validate_general
from signed import from_values
from exact import require

def make_problem(R):
 p=problem(R,normalized=False);mapping=p['mapping'];nvar=len(p['domains']);parent=list(range(nvar));zero=set()
 def find(i):
  if parent[i]!=i:parent[i]=find(parent[i])
  return parent[i]
 def union(a,b):parent[find(a)]=find(b)
 for i,j,k in itertools.product(range(1,len(R)),repeat=3):
  a=mapping.get((i,j,k));b=mapping.get((j,i,k))
  if a is None and b is None:continue
  if a is None:zero.add(b)
  elif b is None:zero.add(a)
  else:union(a,b)
 groups={}
 for i in range(nvar):groups.setdefault(find(i),[]).append(i)
 pos={v:j for j,v in enumerate(p['order'])};source=p['source'];records=[]
 for group in groups.values():
  rep=min(group,key=pos.get);domain=set(p['domains'][group[0]])
  for i in group[1:]:domain &= set(p['domains'][i])
  if any(i in zero for i in group):domain &= {0}
  domain=sorted(domain);records.append({'variables':group,'representative':rep,'domain':domain})
  for i in group:
   allowed=','.join(map(str,domain)) if i==rep else 'v['+str(rep)+']'
   source,count=re.subn(r'for\(int x:vector<int>\{[^}]*\}\)\{v\['+str(i)+r'\]=x;', 'for(int x:vector<int>{'+allowed+'}){v['+str(i)+']=x;',source)
   require(count==1,'native loop matching')
 return p,source,records

def run(R,rid,seconds):
 start=time.monotonic();p,source,groups=make_problem(R);out=Path(__file__).parent;src=out/(rid+'_comm.cpp');src.write_text(source);values=out/(rid+'_comm_values.txt');meta=dict(id=rid,indicator_normalization=False,original_variables=len(p['domains']),commutative_variables=len(groups),groups=groups,source_sha256=hashlib.sha256(source.encode()).hexdigest(),complete=False)
 (out/(rid+'_comm.json')).write_text(json.dumps(meta,indent=2)+'\n');print(rid,'variables',len(p['domains']),len(groups),'rectbox',__import__('math').prod(len(g['domain']) for g in groups),flush=True)
 with tempfile.TemporaryDirectory() as td:
  exe=Path(td)/'enum';subprocess.run(['g++','-std=c++17','-O3',str(src),'-o',str(exe)],check=True,capture_output=True)
  try:
   with values.open('w') as f:proc=subprocess.run([str(exe)],stdout=f,stderr=subprocess.PIPE,text=True,timeout=seconds)
   meta['returncode']=proc.returncode;meta['stderr']=proc.stderr.strip();m=re.fullmatch(r'nodes (\d+) solutions (\d+)\s*',proc.stderr);meta['complete']=proc.returncode==0 and m is not None
   if m:meta['nodes']=int(m[1]);meta['solutions']=int(m[2])
  except subprocess.TimeoutExpired:meta['timeout']=seconds
 meta['seconds']=time.monotonic()-start;meta['values_sha256']=hashlib.sha256(values.read_bytes()).hexdigest();(out/(rid+'_comm.json')).write_text(json.dumps(meta,indent=2)+'\n');print({k:v for k,v in meta.items() if k!='groups'},flush=True)
 return meta
if __name__=='__main__':
 rings={r['id']:r['N'] for r in json.load(open(ROOT/'data/census.json'))}
 for rid in sys.argv[1:] or ['R6_7_200','R6_8_491']:run(rings[rid],rid,300)
