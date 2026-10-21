#!/usr/bin/env python3
"""Joint Gram/rotation search after the simple-center prime-power sieve."""
import argparse,hashlib,json,runpy,time
from pathlib import Path
HERE=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--height',type=int,default=6);p.add_argument('--verify',action='store_true');p.add_argument('--write',action='store_true');args=p.parse_args()
if args.verify:
 if args.height!=6:raise SystemExit('The read-only final certificate is at height 6.')
 runpy.run_path(str(HERE/'verify_central_731.py'),run_name='__main__');raise SystemExit(0)
if not args.write:raise SystemExit('Discovery writes evidence; pass --write, or --verify for read-only replay.')
z=runpy.run_path(str(HERE/'central_731_sieve.py'));a=z['a'];R=z['R'];s=z['s'];fr=z['fr'];grams=z['grams'];rs=z['rs'];orig=z['orig'];primepower=z['primepower']
def filtered(data,L):
 Q,hi=orig(data,L);return Q,[(v,d) for v,d in hi if not primepower(int(d[0]))]
grams.high_columns=filtered
saved=json.loads((HERE/'central_731_sieve.json').read_text());out=[];start=time.monotonic();path=HERE/f'central_731_rotation_h{args.height}.json';expected=json.loads(path.read_text()) if args.verify else None
for rec in saved['records']:
 if rec['outcome']!='gram_not_excluded':continue
 ix=rec['low_index'];cols=saved['frames'][ix];L=s.Matrix.hstack(*map(s.Matrix,cols))
 for ep in rs.h.indicator_choices(R):
  A,b,meta=fr.system(R,a,L,ep,args.height);fp=hashlib.sha256(json.dumps([A,b],separators=(',',':')).encode()).hexdigest()
  if args.verify:
   item=expected['records'][len(out)];z['c'].require(item['system_sha256']==fp and item['metadata']==meta and item['low_index']==ix,'system identity');ray=item['ray']
  else:ray=rs.h.farkas(A,b)
  if ray:rs.h.check_farkas(A,b,ray)
  out.append({'low_index':ix,'indicators':ep,'metadata':meta,'system_sha256':fp,'ray':ray,'outcome':'excluded' if ray else 'no_exact_obstruction'})
  print('ROTATION',ix,meta,'exact_ray',bool(ray),flush=True)
  if not args.verify:path.write_text(json.dumps({'id':'R8_3_731','height':args.height,'records':out,'complete':False},indent=2))
if args.verify:z['c'].require(len(expected['records'])==len(out) and expected['complete'],'complete branches')
else:path.write_text(json.dumps({'id':'R8_3_731','height':args.height,'records':out,'complete':True},indent=2))
print('PASS complete jointrotation',len(out),'branches',sum(r['ray'] is not None for r in out),'excluded','seconds',time.monotonic()-start,flush=True)
