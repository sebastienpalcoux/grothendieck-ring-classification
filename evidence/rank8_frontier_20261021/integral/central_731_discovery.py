#!/usr/bin/env python3
import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
import hashlib,itertools,json,math,sys,time
from pathlib import Path
if __name__=='__main__' and '--write' not in sys.argv:
 raise SystemExit('Discovery writes evidence; pass --write. For read-only replay use verify_central_731.py.')
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT/'evidence/rank8_frontier_20261021/noncommutative'))
import central_support as c
import rotation_search as rs
import full_rotation as fr
sys.path.insert(0,str(ROOT/'evidence/rank8_m3_20261021/performance'))
import gram_vectors_rank8 as grams
from low_frames_rank8 import low_matrices
row=next(r for r in json.loads((ROOT/'evidence/rank8_m3_20261021/pipeline/census_m3.json').read_text()) if r['id']=='R8_3_731');R=row['tensor'];a=c.w.spectral(R);B=a['Gram'];dims=[1,5,5,10,10,11,12,12];D=660
print('codegrees',[str(x) for x in a['codegrees']],'Gram',B.tolist(),flush=True)
start=time.monotonic();vs=grams.native(B);print('fullGramvectors',len(vs),time.monotonic()-start,flush=True)
# The checked integral codegrees are copied by exact field arithmetic.
from exact import ec
targets=[int(ec(a['D']/f)[0]) for f in a['codegrees'][1:]]
sets=[sorted(v for v in vs if v[0]==1 and sum(d*x for d,x in zip(dims,v))==target) for target in targets]
print('targets',targets,'columncounts',list(map(len,sets)),flush=True)
frames=low_matrices(sets,B,gram_prune=True);print('frames',len(frames),time.monotonic()-start,flush=True)
(HERE/'central_731_low_frames.json').write_text(json.dumps({'tensor_sha256':row['tensor_sha256'],'codegrees':[int(ec(f)[0]) for f in a['codegrees']],'Gram':B.tolist(),'dimensions':dims,'column_counts':list(map(len,sets)),'frames':frames},default=int))
