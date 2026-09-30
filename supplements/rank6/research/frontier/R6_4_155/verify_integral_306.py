"""Optimizer-blocked exact replay of the R155 profile306 integer obstruction."""
import scipy.optimize

def forbidden(*args,**kwargs):raise RuntimeError('Optimizer forbidden during verification')
scipy.optimize.linprog=forbidden
scipy.optimize.milp=forbidden
from integer_trace_system import System,Path,json

def require(condition,message):
 if not condition:raise ValueError(message)

def check(A,b,bounds,ray):
 m=len(A);n=len(A[0]);k=len(bounds)
 rows={i:v for i,v in ray}
 require(len(rows)==len(ray),'Duplicate ray index')
 require(all(type(i) is int and 0<=i<m+k and type(v) is int and v for i,v in ray),'Malformed ray')
 rhs=sum(b[i]*v for i,v in ray if i<m)
 pairing=[sum(A[i][j]*v for i,v in ray if i<m) for j in range(n)]
 for t,(j,op,v) in enumerate(bounds):
  y=rows.get(m+t,0);sgn=1 if op=='upper' else -1
  require(y>=0,'Negative slack column')
  pairing[j]+=sgn*y;rhs+=sgn*v*y
 require(rhs<0 and min(pairing)>=0,'Invalid Farkas inequality')

def verify(S,q):
 require(q['height']==S.height==6,'Height mismatch')
 require(q['profile']==306,'Wrong profile')
 A,b,labs=S.profile(q['profile']);bounds=[]
 require(all(type(v) is int for row in A for v in row) and all(type(v) is int for v in b),'Nonintegral system')
 for c in q['cuts']:
  j,op,v=c['bound']
  require(type(j)is int and 0<=j<len(labs) and op in ('upper','lower') and type(v)is int,'Invalid bound')
  require(tuple(c['label'])==labs[j],'Wrong variable label')
  opposite=(j,'lower',v+1) if op=='upper' else (j,'upper',v-1)
  check(A,b,bounds+[opposite],c['ray']);bounds.append(c['bound'])
 check(A,b,bounds,q['final_ray'])
 return len(q['cuts'])

if __name__=='__main__':
 import time
 t=time.time();S=System(6);q=json.loads(Path(__file__).with_name('exact_integral_306.json').read_text())
 cuts=verify(S,q)
 import hashlib,sys
 from integer_trace_system import P
 sources={Path(__file__).resolve(),Path(__file__).with_name('exact_integral_306.json'),P/'data/census.json',P/'research/round5/m4_155/frontier_certificate.json',P/'research/round5/m4_155/packet_frontier.json'}
 for module in list(sys.modules.values()):
  name=getattr(module,'__file__',None)
  if name:
   path=Path(name).resolve()
   if path.is_relative_to(P) and path.suffix=='.py':sources.add(path)
 result={'passed':True,'profile':q['profile'],'integer_bounds':cuts,'remaining_profiles':[275,277,279,296,298],'remaining_center_ranks':[46,48,52,54,60],'optimizer_used':False,'optimized_python':not __debug__,'seconds':time.time()-t,'source_sha256':{str(path.relative_to(P)):hashlib.sha256(path.read_bytes()).hexdigest() for path in sorted(sources)}}
 (P/'verification/current/R6_4_155_integral_306.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result))
