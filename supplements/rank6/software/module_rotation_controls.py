"""Exact regression controls for the low-multiplicity continuation."""
import os
for name in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[name]='1'
from pathlib import Path
import json,time,copy,itertools
from exact import require
P=Path(__file__).resolve().parents[1]
(P/'verification/current').mkdir(parents=True,exist_ok=True)
def main():
 st=time.monotonic();report={};rows=json.load(open(P/'data/census.json'));by={r['id']:r['N'] for r in rows}
 import involution_module as im,field_automorphisms as fa,rotation_frontier as rf
 from additional_models import examples
 from positive_models import examples as old
 # Every applicable known-positive model must survive the necessary module test.
 number=0
 for name,R,ref in itertools.chain(old(),examples()):
  require(im.certificate(R) is None,'module obstruction rejects a constructed positive: '+name);number+=1
 report['constructed_positive_module_controls']=number
 for fn,check in [('continuation_module.json',im.verify),('continuation_fields.json',fa.verify)]:
  records=json.load(open(P/'certificates'/fn))
  for r in records:check(by[r['id']],r['certificate'])
  report[fn]=len(records)
 o=json.load(open(P/'data/frontier_rotation_feasible.json'));require(o['N']==by[o['id']],'frontier tensor mismatch');report['rotation_frontier']=rf.verify(o['N'],o['certificate'])
 # Root traces for a cyclic permutation of binary words: the trace of the
 # rth power is exactly 2^gcd(n,r), and for r|n it is 2^r.
 import math
 ncases=0
 for n in range(2,10):
  words=list(itertools.product(range(2),repeat=n))
  for r in range(1,n+1):
   fixed=sum(word==word[r%n:]+word[:r%n] for word in words)
   require(fixed==2**math.gcd(n,r),'cyclic permutation trace identity')
   if n%r==0:require(fixed==2**r,'block rotation trace identity')
   ncases+=1
 report['ordinary_rotation_controls']=ncases
 # Every mutation below must be rejected by the actual exact verifier.
 mutated=0
 for fn,check,change in [
  ('continuation_module.json',im.verify,lambda c:c.update(involution=0)),
  ('continuation_fields.json',fa.verify,lambda c:c['automorphisms'].__setitem__(0,['1','0']))]:
  rec=json.load(open(P/'certificates'/fn))[0];bad=copy.deepcopy(rec['certificate']);change(bad);rejected=False
  try:check(by[rec['id']],bad)
  except Exception:rejected=True
  require(rejected,'corrupted continuation certificate accepted');mutated+=1
 bad=copy.deepcopy(o['certificate']);bad['primal'][0][1]+=1;rejected=False
 try:rf.verify(o['N'],bad)
 except Exception:rejected=True
 require(rejected,'corrupted rotation primal accepted');mutated+=1
 from proofs import positive_sign_embedding
 from rings import Characters
 signcount=0
 for rid in ['R6_2_37','R6_2_57','R6_3_204']:
  R=by[rid];ch=Characters(R)
  for f,m in ch.components:
   K,ds,D,pD=ch.component(f)
   if any(not x for x in ds):continue
   c=positive_sign_embedding(R,f,ds)
   if c:
    require(all(c['signs'][i]*c['signs'][j]==c['signs'][k] for i in range(6) for j in range(6) for k in range(6) if R[i][j][k]),'invalid tensor-sign support');signcount+=1
 report['tensor_sign_components_checked']=signcount;report['rejected_mutations']=mutated
 report.update(passed=True,optimized_python=not __debug__,seconds=time.monotonic()-st)
 (P/'verification/current'/('module_rotation_controls_optimized.json' if not __debug__ else 'module_rotation_controls_normal.json')).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2));return 0
if __name__=='__main__':raise SystemExit(main())
