"""Checkpointed discovery, with exact second-indicator row reuse.

This is a discovery driver only. Full certificate verification uses the public
unmodified engine, after writing the unverified discovery record separately.
No persisted candidate ray is trusted: every reuse gets check_farkas.
"""
import argparse,hashlib,json,math,signal,sys,time
from fractions import Fraction as Q
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'software'))
import stabilizer_rotation_higher as H
from higher_traces import check_farkas
p=argparse.ArgumentParser();p.add_argument('id');p.add_argument('--height',type=int,default=6);p.add_argument('--seconds',type=int,default=900);a=p.parse_args()
R=next(r['N'] for r in json.load(open(ROOT/'data/census.json')) if r['id']==a.id)
DIR=Path(__file__).parent;out=DIR/(a.id+'_higher_h'+str(a.height)+'_resumed.json');cp=DIR/(a.id+'_higher_h'+str(a.height)+'_rays.json')
rays=json.load(open(cp)) if cp.exists() else {};raw=H.trace_system;cache={};calls=0

def fast(R,data,tab,cols,ep,height,lab,sp,objects,targets=None):
 global calls
 key=(tuple(map(tuple,cols)),height,tuple(lab) if lab is not None else None,tuple(objects),tuple(targets) if targets is not None else None)
 if key not in cache:
  A,b,m=raw(R,data,tab,cols,ep,height,lab,sp,objects,targets)
  L=H.I.s.Matrix.hstack(*map(H.I.s.Matrix,cols));BA,bb,bm=H.I.system_rotation(R,data,L,ep,height)
  forbidden=set(map(tuple,sp.forbidden)) if lab is not None else set();labs=bm['labels'];keep=[j for j in range(len(BA[0])) if j>=len(labs) or tuple(labs[j][0]) not in forbidden]
  LL=L*L.T;d=data['dimensions'];n=len(R);low=[tuple(sum(Q(int(LL[i,j]))*d[j][k] for j in range(n)) for k in range(2)) for i in range(1,n)]
  cache[key]=(A,b,m,tuple(ep),BA,keep,low)
 else:A,b,m,old,BA,keep,low=cache[key]
 A0,b0,m,old,BA,keep,low=cache[key];A=list(A0);b=list(b0);n=len(R);start=(n-1)*n//2+2*(n-1);D=data['global_dimension']
 for i in range(n-1):
  if ep[i]==old[i]:continue
  for k in range(2):
   rowid=start+2*i+k;prior=old[i]*D[k]-low[i][k];nextrhs=ep[i]*D[k]-low[i][k]
   if prior==0:
    # Safe uncommon fallback; no speculative scale reconstruction.
    return raw(R,data,tab,cols,ep,height,lab,sp,objects,targets)
   ratio=Q(b0[rowid])/prior;rhs=nextrhs*ratio;den=rhs.denominator
   rr=[x*den for x in BA[rowid]];vv=int(rhs*den);g=math.gcd(vv,*rr) or 1;rr=[x//g for x in rr];vv//=g
   A[rowid]=[rr[j] for j in keep]+[0]*(len(A0[rowid])-len(keep));b[rowid]=vv
 calls+=1
 # Deterministic sample compares the optimization against original assembly.
 if calls in (1,2,3,7,19,53):
  AA,bb,mm=raw(R,data,tab,cols,ep,height,lab,sp,objects,targets)
  if (A,b,m)!=(AA,bb,mm):raise RuntimeError('second-indicator cache comparison failed')
 return A,b,m
H.trace_system=fast
oldf=H.cached_farkas

def ray(A,b):
 key=hashlib.sha256(repr((A,b)).encode()).hexdigest()
 if key in rays:
  y=rays[key];check_farkas(A,b,y);return y
 y=oldf(A,b)
 if y is not None:
  check_farkas(A,b,y);rays[key]=y
  if len(rays)%20==0:cp.write_text(json.dumps(rays,separators=(',',':'))+'\n')
 return y
H.cached_farkas=ray
start=time.monotonic();last=None

def progress(*z):
 global last
 last=z;print(json.dumps({'id':a.id,'progress':z,'rays':len(rays)}),flush=True)
def timeout(*z):raise TimeoutError('explicit resumed discovery budget')
signal.signal(signal.SIGALRM,timeout);signal.alarm(a.seconds)
record={'id':a.id,'height':a.height}
try:
 c=H.certificate(R,a.height,progress);signal.alarm(0)
 record.update(outcome='discovered_unverified',certificate=c)
except H.Survives as e:record.update(outcome='no_exact_obstruction',reason=str(e),certificate=None)
except H.Ineligible as e:record.update(outcome='ineligible',reason=str(e),certificate=None)
except TimeoutError as e:record.update(outcome='budget_incomplete',reason=str(e),certificate=None,last_progress=last)
finally:
 signal.alarm(0);cp.write_text(json.dumps(rays,separators=(',',':'))+'\n')
record['seconds']=time.monotonic()-start;out.write_text(json.dumps(record,separators=(',',':'))+'\n');print(json.dumps({k:v for k,v in record.items() if k!='certificate'}),flush=True)
