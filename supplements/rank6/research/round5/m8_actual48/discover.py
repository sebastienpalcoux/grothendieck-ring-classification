"""Bounded discovery; only exactly checked rational Farkas rays certify exclusions."""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1');os.environ.setdefault('OMP_NUM_THREADS','1')
import argparse,json,time,hashlib,sys,traceback
from pathlib import Path
import actual48 as Q
from exact import require
from round5_155 import sparse_ray,check_sparse_ray

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--low',type=int);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--verify',action='store_true');args=ap.parse_args();start=time.monotonic()
 R=next(r['N']for r in json.loads((Q.P/'data/census.json').read_text())if r['id']=='R6_8_1660');d=Q.prepare(R);print('prepared',round(time.monotonic()-start,2),flush=True)
 branches=[(low,list(lab),list(ep))for low,cols in enumerate(d['lows'])if args.low is None or low==args.low for lab in d['tab'].assignments(cols)for ep in Q.M.indicator_choices(R)]
 if args.verify:
  import scipy.optimize as opt
  def forbidden(*a,**k):raise RuntimeError('optimizer forbidden during exact replay')
  opt.linprog=forbidden;opt.milp=forbidden
  cert=json.loads(args.out.read_text());require(cert['complete']and len(branches)==len(cert['branches']),'incomplete actual48 branch domain');nr=0
 else:cert=dict(id='R6_8_1660',scope='pseudo_unitary_necessary',actual_twist_exponent_divides=48,complete=False,branches=[])
 for ix,(low,lab,ep)in enumerate(branches):
  t=time.monotonic();A,b,meta=Q.build(R,d,low,lab,ep);rows=[{j:int(a)for j,a in enumerate(row)if a}for row in A];nv=meta['variables'];print('built',ix,low,lab,ep,len(A),nv,round(time.monotonic()-t,2),flush=True)
  system_hash=hashlib.sha256(json.dumps([A,b],separators=(',',':')).encode()).hexdigest()
  if args.verify:
   rec=cert['branches'][ix];require(rec['meta']==json.loads(json.dumps(meta))and rec['system_sha256']==system_hash,'actual48 system mismatch')
   if rec['outcome']=='exact_farkas':check_sparse_ray(rows,b,nv,rec['ray']);nr+=1
  else:
   ray=sparse_ray(rows,b,nv,time_limit=30);rec=dict(meta=meta,system_sha256=system_hash,outcome='exact_farkas'if ray is not None else'inconclusive')
   if ray is not None:rec['ray']=ray
   rec['elapsed_seconds']=round(time.monotonic()-t,4);cert['branches'].append(rec);args.out.write_text(json.dumps(cert,indent=2)+'\n');print('result',ix,rec['outcome'],rec['elapsed_seconds'],flush=True)
 if args.verify:
  receipt=dict(passed=True,optimizer_used=False,branches=len(branches),exact_farkas=nr,inconclusive=len(branches)-nr,elapsed_seconds=round(time.monotonic()-start,4));args.out.with_name(args.out.stem+'_replay_O.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt),flush=True)
 else:
  cert['complete']=True;cert['all_branches_excluded']=all(b['outcome']=='exact_farkas'for b in cert['branches']);cert['elapsed_seconds']=round(time.monotonic()-start,4);args.out.write_text(json.dumps(cert,indent=2)+'\n')
if __name__=='__main__':main()
