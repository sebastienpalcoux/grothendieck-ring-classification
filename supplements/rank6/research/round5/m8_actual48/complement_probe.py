"""Probe the three global remaining actual-root branches with prime indicators and the complete modular representation cone."""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1');os.environ.setdefault('OMP_NUM_THREADS','1')
import json,time
from pathlib import Path
import actual48 as Q
from exact import require,evaluate
import prime48 as P
import moment48 as W
import sys
sys.path.insert(0,str(Q.P/'research/round5/m8_modrep'))
import ising_complement as K
from round5_155 import sparse_ray,check_sparse_ray
R=next(r['N']for r in json.loads((Q.P/'data/census.json').read_text())if r['id']=='R6_8_1660');d=Q.prepare(R);require(all(evaluate(z.to_list(),d['C'].unit**47,d['C'])==z for row in d['tab'].rows for z in row),'low center characters are not all real');out=[];start=time.monotonic()
for low in range(2):
 for lab in d['tab'].assignments(d['lows'][low]):
  if low==0 and list(lab)==[0,5,4,1,2,3]:continue
  A,b,md=Q.build(R,d,low,lab,[1,1,1,-1,1]);rows=[{j:int(a)for j,a in enumerate(row)if a}for row in A];nv=md['variables'];rr,bb,pmd=P.append_rows(R,d,d['lows'][low],md['high_labels'],nv);rows+=rr;b+=bb;rr,bb,wmd=W.append_rows(d,d['lows'][low],md['high_labels'],nv);rows+=rr;b+=bb;AA=[[row.get(j,0)for j in range(nv)]for row in rows];AA,b,kmd=K.append_complement(AA,b,md['high_labels'],md['ising_root_exponents'][4]);nv=len(AA[0]);rows=[{j:int(a)for j,a in enumerate(row)if a}for row in AA];print('built',low,lab,len(rows),nv,time.monotonic()-start,flush=True);y=sparse_ray(rows,b,nv,time_limit=30)
  if y is not None:check_sparse_ray(rows,b,nv,y)
  rec=dict(low=low,labelling=list(lab),indicators=[1,1,1,-1,1],prime_metadata=pmd,moment_metadata=wmd,representation_cone_metadata=kmd,outcome='exact_farkas'if y is not None else'inconclusive',ray=None if y is None else[[i,a]for i,a in enumerate(y)if a]);out.append(rec);Path(__file__).with_name('complement_global_probe.json').write_text(json.dumps(dict(complete=False,branches=out),indent=2)+'\n');print('result',rec['outcome'],time.monotonic()-start,flush=True)
Path(__file__).with_name('complement_global_probe.json').write_text(json.dumps(dict(complete=True,branches=out,seconds=time.monotonic()-start),indent=2)+'\n')
