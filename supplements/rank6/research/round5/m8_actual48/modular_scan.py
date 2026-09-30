"""Exact necessary integral conditions by reusable local Smith row elimination."""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1');os.environ.setdefault('OMP_NUM_THREADS','1')
import argparse,json,time,hashlib
from pathlib import Path
import actual48 as Q
import profile_scan as B
import moment48 as W
from exact import require
from round5_155 import check_sparse_modular

def conditions(rows,nv,prime=2,power=6):
 modulus=prime**power;rr=[{int(j):a%modulus for j,a in row.items()if a%modulus}for row in rows];ww=[{i:1}for i in range(len(rows))];active=set(range(len(rows)));bycol=[set()for _ in range(nv)];out=[]
 for i,row in enumerate(rr):
  for j in row:bycol[j].add(i)
 def val(a):
  v=0
  while a%prime==0:v+=1;a//=prime
  return v
 def add(i,m):
  if m>1:out.append(dict(modulus=m,rows=sorted([j,x%m]for j,x in ww[i].items()if x%m)))
 while active:
  empty=[i for i in active if not rr[i]]
  for i in empty:add(i,modulus);active.remove(i)
  if not active:break
  choice=None
  for i in sorted(active):
   for j,a in rr[i].items():
    v=val(a)
    if choice is None or v<choice[0]:choice=(v,i,j)
    if v==0:break
   if choice[0]==0:break
  v,i,j=choice;divisor=prime**v;factor=pow(rr[i][j]//divisor,-1,modulus);rr[i]={k:a*factor%modulus for k,a in rr[i].items()};ww[i]={k:a*factor%modulus for k,a in ww[i].items()};require(rr[i][j]==divisor,'Smith pivot mismatch');add(i,divisor);active.remove(i)
  for k in rr[i]:bycol[k].discard(i)
  for target in list(bycol[j]):
   require(target in active and rr[target][j]%divisor==0,'Smith pivot divisibility');q=rr[target][j]//divisor
   for k,a in rr[i].items():
    z=(rr[target].get(k,0)-q*a)%modulus
    if z:rr[target][k]=z;bycol[k].add(target)
    elif k in rr[target]:del rr[target][k];bycol[k].discard(target)
   for k,a in ww[i].items():
    z=(ww[target].get(k,0)-q*a)%modulus
    if z:ww[target][k]=z
    elif k in ww[target]:del ww[target][k]
 return out

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--low',type=int,required=True);ap.add_argument('--lab',type=int,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--prime',type=int,default=2);ap.add_argument('--power',type=int,default=6);args=ap.parse_args();start=time.monotonic();source=Q.P/f'research/round5/m8_1660/low{args.low}_profiles.json';branch=json.loads(source.read_text())['branches'][0];case=branch['cases'][args.lab];V=branch['high_vectors'];profiles=case['profiles'];indices=case.get('gram_filter',{}).get('survivor_indices',range(len(profiles)));lab=case['labelling'];R=next(r['N']for r in json.loads((Q.P/'data/census.json').read_text())if r['id']=='R6_8_1660');d=Q.prepare(R);rows,baseb,meta=B.matrix(R,d,args.low,lab,V);nv=meta['variables'];rr,bb,md=W.append_rows(d,d['lows'][args.low],meta['high_labels'],nv);rows+=rr;print('built',len(rows),nv,time.monotonic()-start,flush=True);cc=conditions(rows,nv,args.prime,args.power);print('conditions',len(cc),time.monotonic()-start,flush=True);kept=[];used=[];positions={};excluded=[]
 for j in indices:
  rhs=baseb+profiles[j]+bb;record=None
  for k,c in enumerate(cc):
   value=sum(rhs[i]*a for i,a in c['rows'])%c['modulus']
   if value:
    witness=dict(c,value=value);check_sparse_modular(rows,rhs,nv,witness)
    if k not in positions:positions[k]=len(used);used.append(c)
    record=dict(index=j,condition=positions[k],value=value);break
  if record is None:kept.append(j)
  else:excluded.append(record)
 out=dict(id='R6_8_1660',low=args.low,labelling=lab,source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),prime=args.prime,power=args.power,moment_metadata=md,conditions=used,excluded=excluded,survivors=kept,total=len(indices),complete=True,seconds=time.monotonic()-start);args.out.write_text(json.dumps(out,separators=(',',':'))+'\n');print('finished',len(excluded),len(kept),out['seconds'],flush=True)
if __name__=='__main__':main()
