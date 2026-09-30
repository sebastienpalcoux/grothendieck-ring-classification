"""Reusable exact integer-lattice constraints for the complete representation cone."""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1');os.environ.setdefault('OMP_NUM_THREADS','1')
import argparse,json,time,hashlib
from pathlib import Path
import actual48 as Q
import profile_scan as B
import moment48 as W
import prime48 as J
import cone48 as K
from modular_scan import conditions
from exact import require
from round5_155 import check_sparse_modular
ap=argparse.ArgumentParser();ap.add_argument('--low',type=int,required=True);ap.add_argument('--lab',type=int,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args();start=time.monotonic();source=Q.P/f'research/round5/m8_1660/low{args.low}_profiles.json';branch=json.loads(source.read_text())['branches'][0];case=branch['cases'][args.lab];V=branch['high_vectors'];profiles=case['profiles'];lab=case['labelling'];front=Path(__file__).with_name('certificate.json');fc=json.loads(front.read_text());frec=next(r for r in fc['branches']if r['low']==args.low and r['labelling']==lab and r['indicators']==[1,1,1,-1,1]);ids=frec['unresolved'];R=next(r['N']for r in json.loads((Q.P/'data/census.json').read_text())if r['id']=='R6_8_1660');d=Q.prepare(R);rows,baseb,meta=B.matrix(R,d,args.low,lab,V);nv=meta['variables'];rr,bb,wmd=W.append_rows(d,d['lows'][args.low],meta['high_labels'],nv);rows+=rr;rr,jb,jmd=J.append_rows(R,d,d['lows'][args.low],meta['high_labels'],nv);rows+=rr;bb+=jb;rr,kb,nv,bounds,kmd=K.append_rows(R,d,d['lows'][args.low],meta['high_labels'],nv,V);rows+=rr;bb+=kb;print('built',len(rows),nv,time.monotonic()-start,flush=True);cc=conditions(rows,nv,2,6)+conditions(rows,nv,3,3);print('conditions',len(cc),time.monotonic()-start,flush=True);used=[];pos={};excluded=[];kept=[]
for j in ids:
 rhs=baseb+profiles[j]+bb+bounds(profiles[j]);record=None
 for k,c in enumerate(cc):
  value=sum(rhs[i]*a for i,a in c['rows'])%c['modulus']
  if value:
   check_sparse_modular(rows,rhs,nv,dict(c,value=value))
   if k not in pos:pos[k]=len(used);used.append(c)
   record=dict(index=j,condition=pos[k],value=value);break
 if record is None:kept.append(j)
 else:excluded.append(record)
out=dict(complete=True,id='R6_8_1660',low=args.low,labelling=lab,source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),frontier_sha256=hashlib.sha256(front.read_bytes()).hexdigest(),candidates=ids,moment_metadata=wmd,prime_metadata=jmd,cone_metadata=kmd,conditions=used,excluded=excluded,survivors=kept,total=len(ids),seconds=time.monotonic()-start);args.out.write_text(json.dumps(out,separators=(',',':'))+'\n');print('done',len(excluded),len(kept),out['seconds'],flush=True)
