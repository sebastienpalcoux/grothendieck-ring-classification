#!/usr/bin/env python3
"""Read-only, exact replay of the complete R731 simple-center obstruction.

No LP solver or numerical inference is used. Exact enumeration plus saved
integer Farkas rays are replayed against the authoritative tensor.
"""
import os
for key in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[key]='1'
import collections,hashlib,itertools,json,sys
from fractions import Fraction as F
from pathlib import Path
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
s=c.s;require=c.require

def digest(x):return hashlib.sha256(json.dumps(x,separators=(',',':')).encode()).hexdigest()
def primepower(n):return n>1 and len(s.factorint(n))==1

def main():
 saved=json.loads((HERE/'central_731_sieve.json').read_text());rotation=json.loads((HERE/'central_731_rotation_h6.json').read_text())
 row=next(r for r in json.loads((ROOT/'evidence/rank8_m3_20261021/pipeline/census_m3.json').read_text()) if r['id']=='R8_3_731');R=row['tensor'];require(digest(R)==row['tensor_sha256']==saved['tensor_sha256'],'tensor hash')
 a=c.w.spectral(R);B=a['Gram'];dims=[1,5,5,10,10,11,12,12];D=660
 require([int(ec(d)[0]) for d in a['ds']]==dims and int(ec(a['D'])[0])==D,'integral dimension gate')
 # Source-bound non-group-like gate: previous exhaustive scan is a separate input.
 scan=json.loads((ROOT/'evidence/rank8_m3_20261021/performance/group_scan/per_id_attempts.json').read_text());sc=next(r for r in scan if r['id']==row['id'])
 require(sc['tensor_sha256']==row['tensor_sha256'] and sc['outcome']=='no_ordinary_group_model' and sc['matches']==[] and sc['groups_checked']==40 and sc['order']==660 and sc['exact_full_tensor_isomorphism_test_for_every_degree_match'],'ordinary group gate')
 from structural_certificate import proper
 require(proper(R)==[],'simple fusion ring gate')
 vs=grams.native(B);targets=[int(ec(a['D']/f)[0]) for f in a['codegrees'][1:]]
 sets=[sorted(v for v in vs if v[0]==1 and sum(d*x for d,x in zip(dims,v))==target) for target in targets]
 frames=low_matrices(sets,B,gram_prune=True)
 require(saved['scope']=='general_complex_after_integrality_and_simple_center_reduction','scope')
 require(saved['complete'] and saved['frame_count']==len(frames)==450,'frame completion')
 require(saved['column_counts']==list(map(len,sets)),'restriction counts')
 require(saved['frames']==json.loads(json.dumps(frames)),'complete low frame identity')
 require(len(saved['records'])==len(frames),'frame records complete')
 a.update(ch=SimpleNamespace(n=8,C=B,du=a['du']),q=1,conductor=1,dimensions=[(F(d),F(0)) for d in dims],global_dimension=(F(D),F(0)),primes=[2,3,5,11])
 original_high=grams.high_columns
 def filtered(data,L):
  Q,hi=original_high(data,L)
  return Q,[(v,d) for v,d in hi if not primepower(int(d[0]))]
 remaining=[];counts=collections.Counter();eps=rs.h.indicator_choices(R)
 require(eps==[(0,0,0,0,1,1,1)],'indicator branches')
 for ix,(cols,rec) in enumerate(zip(frames,saved['records'])):
  require(rec['low_index']==ix,'low index')
  fail=lf.low_failure(cols,B,a['ds'],a['D'],a['K'],a['embedding'],a['du'])
  if fail:
   require(rec['outcome']=='ordinary_obstruction' and rec['certificate']==fail,'ordinary obstruction');counts['ordinary']+=1;continue
  dual_failure=collections.Counter(cols)!=collections.Counter(tuple(v[j] for j in a['du']) for v in cols)
  if dual_failure:require(rec['outcome']=='duality_failure','duality obstruction');counts['duality']+=1;continue
  L=s.Matrix.hstack(*map(s.Matrix,cols));Q,allhi=original_high(a,L);hi=[(v,d) for v,d in allhi if not primepower(int(d[0]))]
  require(rec['high_columns_before']==len(allhi) and rec['high_columns_after']==len(hi),'high column completeness')
  pairs=list(itertools.combinations_with_replacement(range(7),2));A=[[v[i]*v[j] for v,d in hi] for i,j in pairs];b=[int(Q[i,j]) for i,j in pairs]
  if rec['ray'] is not None:
   require(rec['outcome']=='gram_obstruction','Gram outcome');rs.h.check_farkas(A,b,rec['ray']);counts['gram']+=1
  else:require(rec['outcome']=='gram_not_excluded','remaining outcome');remaining.append(ix)
 require(remaining==[293,301,303],'rotation branch completeness')
 require(rotation['complete'] and rotation['id']==row['id'] and rotation['height']==6,'rotation metadata')
 require([r['low_index'] for r in rotation['records']]==remaining,'all rotation branches')
 grams.high_columns=filtered
 for rec in rotation['records']:
  ix=rec['low_index'];L=s.Matrix.hstack(*map(s.Matrix,frames[ix]));require(rec['indicators']==list(eps[0]),'rotation indicators')
  A,b,meta=fr.system(R,a,L,eps[0],6)
  require(rec['metadata']==meta and rec['system_sha256']==digest([A,b]),'exact joint rotation system')
  require(rec['ray'] is not None and rec['outcome']=='excluded','rotation conclusion');rs.h.check_farkas(A,b,rec['ray']);counts['rotation']+=1
 grams.high_columns=original_high
 require(sum(counts.values())==450,'all branches excluded')
 print('PASS general-complex R8_3_731 exclusion:',dict(counts),'; complete exact Gram and joint rotation replay')
if __name__=='__main__':main()
