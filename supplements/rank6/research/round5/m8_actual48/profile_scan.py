"""Common exact actual-root matrix, specialized by complete induction profiles."""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1');os.environ.setdefault('OMP_NUM_THREADS','1')
import argparse,json,time,hashlib
from pathlib import Path
from collections import Counter
import actual48 as Q
from exact import require
from round5_155 import sparse_ray,check_sparse_ray

def matrix(R,d,low,lab,V):
 A,b,meta=Q.build(R,d,low,lab,[1,1,1,-1,1]);rows=[{j:int(a)for j,a in enumerate(row)if a}for row in A];nh=len(meta['high_labels']);nv=meta['variables']
 for v in V:rows.append({j:1 for j,(w,a)in enumerate(meta['high_labels'])if tuple(w)==tuple(v)})
 return rows,b,meta

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--low',type=int,required=True);ap.add_argument('--lab',type=int,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--verify',action='store_true');ap.add_argument('--start',type=int,default=0);ap.add_argument('--stop',type=int);args=ap.parse_args();start=time.monotonic()
 source=Q.P/f'research/round5/m8_1660/low{args.low}_profiles.json';inputc=json.loads(source.read_text());branch=inputc['branches'][0];case=branch['cases'][args.lab];V=branch['high_vectors'];profiles=case['profiles'];stop=len(profiles)if args.stop is None else min(args.stop,len(profiles));lab=case['labelling'];R=next(r['N']for r in json.loads((Q.P/'data/census.json').read_text())if r['id']=='R6_8_1660');d=Q.prepare(R);require(lab in list(map(list,d['tab'].assignments(d['lows'][args.low]))),'labelling mismatch');rows,baseb,meta=matrix(R,d,args.low,lab,V);nv=meta['variables'];print('ready',args.low,args.lab,len(profiles),len(rows),nv,round(time.monotonic()-start,3),flush=True)
 if args.verify:
  import scipy.optimize as opt
  def forbidden(*a,**k):raise RuntimeError('optimizer forbidden in exact replay')
  opt.linprog=forbidden;opt.milp=forbidden
  cert=json.loads(args.out.read_text());require(cert['complete']and cert['source_sha256']==hashlib.sha256(source.read_bytes()).hexdigest(),'profile source mismatch');require(cert['start']==args.start and cert['stop']==stop and len(cert['profiles'])==stop-args.start,'incomplete shard');require(cert['meta']==json.loads(json.dumps(meta)),'actual-root metadata mismatch');rays=cert['rays'];valid=[]
  for ray in rays:
   y=[0]*len(rows)
   for i,a in ray:y[i]=a
   z=[0]*nv
   for row,a in zip(rows,y):
    if a:
     for j,k in row.items():z[j]+=a*k
   require(min(z)>=0,'invalid cached coefficient inequality');valid.append(y)
  for j,rec in enumerate(cert['profiles'],args.start):
   require(rec['index']==j,'wrong profile ordering')
   if rec['outcome']=='exact_farkas':require(sum(a*b for a,b in zip(valid[rec['ray']],baseb+profiles[j]))<0,'profile exact Farkas rhs fails')
  receipt=dict(passed=True,optimizer_used=False,profiles=len(cert['profiles']),exact_rays=len(rays),excluded=sum(r['outcome']=='exact_farkas'for r in cert['profiles']),survivors=[r['index']for r in cert['profiles']if r['outcome']!='exact_farkas'],elapsed_seconds=round(time.monotonic()-start,4));args.out.with_name(args.out.stem+'_replay_O.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt),flush=True);return
 cert=dict(id='R6_8_1660',low=args.low,labelling=lab,indicators=[1,1,1,-1,1],source=str(source.relative_to(Q.P)),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),meta=meta,start=args.start,stop=stop,total_profiles=len(profiles),complete=False,rays=[],profiles=[]);cache=[];counts=Counter()
 for j in range(args.start,stop):
  rhs=baseb+profiles[j];rayix=next((i for i,ray in enumerate(cache)if sum(rhs[k]*a for k,a in ray)<0),None)
  if rayix is None:
   y=sparse_ray(rows,rhs,nv,time_limit=5)
   if y is not None:
    check_sparse_ray(rows,rhs,nv,y);rayix=len(cache);ray=[[i,int(a)]for i,a in enumerate(y)if a];cache.append(ray);cert['rays'].append(ray)
  rec=dict(index=j,outcome='exact_farkas'if rayix is not None else'inconclusive')
  if rayix is not None:rec['ray']=rayix
  cert['profiles'].append(rec);counts[rec['outcome']]+=1
  if(j-args.start)%25==0 or j+1==stop:args.out.write_text(json.dumps(cert,separators=(',',':'))+'\n');print('profile',j,dict(counts),'rays',len(cache),'elapsed',round(time.monotonic()-start,2),flush=True)
 cert['complete']=True;cert['elapsed_seconds']=round(time.monotonic()-start,4);args.out.write_text(json.dumps(cert,separators=(',',':'))+'\n')
if __name__=='__main__':main()
