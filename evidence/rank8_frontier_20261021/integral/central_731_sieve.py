#!/usr/bin/env python3
import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
import collections,hashlib,itertools,json,sys,time
from fractions import Fraction as F
from pathlib import Path
if __name__=='__main__' and '--write' not in sys.argv:
 raise SystemExit('Discovery writes evidence; pass --write. For read-only replay use verify_central_731.py.')
from types import SimpleNamespace
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT/'evidence/rank8_frontier_20261021/noncommutative'))
import central_support as c
import rotation_search as rs
import full_rotation as fr
sys.path.insert(0,str(ROOT/'evidence/rank8_m3_20261021/performance'))
import gram_vectors_rank8 as grams
import low_failure_exact as lf
from low_frames_rank8 import low_matrices
from exact import ec
s=c.s
row=next(r for r in json.loads((ROOT/'evidence/rank8_m3_20261021/pipeline/census_m3.json').read_text()) if r['id']=='R8_3_731');R=row['tensor'];a=c.w.spectral(R);B=a['Gram'];dims=[1,5,5,10,10,11,12,12];D=660
vs=grams.native(B);targets=[int(ec(a['D']/f)[0]) for f in a['codegrees'][1:]];sets=[sorted(v for v in vs if v[0]==1 and sum(d*x for d,x in zip(dims,v))==target) for target in targets];frames=low_matrices(sets,B,gram_prune=True)
a.update(ch=SimpleNamespace(n=8,C=B,du=a['du']),q=1,conductor=1,dimensions=[(F(d),F(0)) for d in dims],global_dimension=(F(D),F(0)),primes=[2,3,5,11])
def primepower(n):return n>1 and len(s.factorint(n))==1
orig=grams.high_columns
records=[];start=time.monotonic()
for ix,cols in enumerate(frames):
 rec={'low_index':ix};records.append(rec)
 fail=lf.low_failure(cols,B,a['ds'],a['D'],a['K'],a['embedding'],a['du'])
 if fail:rec.update(outcome='ordinary_obstruction',certificate=fail);continue
 if collections.Counter(cols)!=collections.Counter(tuple(v[j] for j in a['du']) for v in cols):rec.update(outcome='duality_failure');continue
 L=s.Matrix.hstack(*map(s.Matrix,cols));Q,allhi=orig(a,L);hi=[(v,z) for v,z in allhi if not primepower(int(z[0]))]
 pairs=list(itertools.combinations_with_replacement(range(7),2));A=[[v[i]*v[j] for v,z in hi] for i,j in pairs];b=[int(Q[i,j]) for i,j in pairs]
 ray=rs.h.farkas(A,b)
 rec.update(outcome='gram_obstruction' if ray else 'gram_not_excluded',high_columns_before=len(allhi),high_columns_after=len(hi),ray=ray)
 if ray:rs.h.check_farkas(A,b,ray)
 print(ix,rec['outcome'],len(allhi),len(hi),flush=True)
 result={'id':row['id'],'tensor_sha256':row['tensor_sha256'],'scope':'general_complex_after_integrality_and_simple_center_reduction','column_counts':list(map(len,sets)),'frame_count':len(frames),'frames':frames,'records':records,'complete':len(records)==len(frames)}
 (HERE/'central_731_sieve.json').write_text(json.dumps(result,default=int))
result={'id':row['id'],'tensor_sha256':row['tensor_sha256'],'scope':'general_complex_after_integrality_and_simple_center_reduction','column_counts':list(map(len,sets)),'frame_count':len(frames),'frames':frames,'records':records,'complete':True}
(HERE/'central_731_sieve.json').write_text(json.dumps(result,default=int))
print('DONE',collections.Counter(x['outcome'] for x in records),'seconds',time.monotonic()-start,flush=True)
