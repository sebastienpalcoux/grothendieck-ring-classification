"""Bounded exact-ray discovery for every remaining fixed actual-root profile."""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1');os.environ.setdefault('OMP_NUM_THREADS','1')
import argparse,json,time,hashlib
from pathlib import Path
from collections import Counter
import actual48 as Q
import profile_scan as B
import moment48 as W
import prime48 as J
import cone48 as K
from exact import require
from round5_155 import sparse_ray,check_sparse_ray
ap=argparse.ArgumentParser();ap.add_argument('--low',type=int,required=True);ap.add_argument('--lab',type=int,required=True);ap.add_argument('--start',type=int,default=0);ap.add_argument('--stop',type=int);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args();start=time.monotonic();source=Q.P/f'research/round5/m8_1660/low{args.low}_profiles.json';branch=json.loads(source.read_text())['branches'][0];case=branch['cases'][args.lab];V=branch['high_vectors'];profiles=case['profiles'];lab=case['labelling'];front=Path(__file__).with_name('certificate.json');fc=json.loads(front.read_text());frec=next(r for r in fc['branches']if r['low']==args.low and r['labelling']==lab and r['indicators']==[1,1,1,-1,1]);allids=frec['unresolved'];stop=len(allids)if args.stop is None else min(args.stop,len(allids));ids=allids[args.start:stop];R=next(r['N']for r in json.loads((Q.P/'data/census.json').read_text())if r['id']=='R6_8_1660');d=Q.prepare(R);rows,baseb,meta=B.matrix(R,d,args.low,lab,V);nv=meta['variables'];rr,bb,wmd=W.append_rows(d,d['lows'][args.low],meta['high_labels'],nv);rows+=rr;rr,jb,jmd=J.append_rows(R,d,d['lows'][args.low],meta['high_labels'],nv);rows+=rr;bb+=jb;rr,kb,nv,bounds,kmd=K.append_rows(R,d,d['lows'][args.low],meta['high_labels'],nv,V);rows+=rr;bb+=kb;print('ready',args.low,args.lab,len(ids),'total',len(allids),len(rows),nv,kmd,'elapsed',time.monotonic()-start,flush=True);out=dict(id='R6_8_1660',low=args.low,labelling=lab,source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),frontier_sha256=hashlib.sha256(front.read_bytes()).hexdigest(),start=args.start,stop=stop,all_candidates=allids,candidates=ids,moment_metadata=wmd,prime_metadata=jmd,cone_metadata=kmd,complete=False,rays=[],profiles=[]);cache=[];counts=Counter()
for count,j in enumerate(ids):
 rhs=baseb+profiles[j]+bb+bounds(profiles[j]);require(len(rhs)==len(rows),'cone RHS shape');rayix=next((i for i,ray in enumerate(cache)if sum(rhs[k]*a for k,a in ray)<0),None)
 if rayix is None:
  y=sparse_ray(rows,rhs,nv,time_limit=3)
  if y is not None:check_sparse_ray(rows,rhs,nv,y);rayix=len(cache);ray=[[i,int(a)]for i,a in enumerate(y)if a];cache.append(ray);out['rays'].append(ray)
 rec=dict(index=j,outcome='exact_farkas'if rayix is not None else'inconclusive')
 if rayix is not None:rec['ray']=rayix
 out['profiles'].append(rec);counts[rec['outcome']]+=1
 if count%25==0 or count+1==len(ids):args.out.write_text(json.dumps(out,separators=(',',':'))+'\n');print('profile',j,'done',count+1,dict(counts),'rays',len(cache),'elapsed',round(time.monotonic()-start,2),flush=True)
out['complete']=True;out['seconds']=time.monotonic()-start;args.out.write_text(json.dumps(out,separators=(',',':'))+'\n')
