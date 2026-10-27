"""Exact reconstruction of the necessary third-rotation systems. No optimizer.
Frozen old center domains and the new categorical doubling law are inputs.
"""
from pathlib import Path
from fractions import Fraction as Q
import sys, json, time, math, itertools

def build(objects):
 HERE=Path(__file__).resolve().parent
 ROOT=HERE.parents[2]
 OLD=ROOT/'evidence/rank8_frontier_20261021'
 sys.path.insert(0,str(OLD/'noncommutative'))
 sys.path.insert(0,str(HERE/'replay_dependencies'))
 import character_modular as md
 md.full.base.install()
 c=md.c
 domain=json.loads((OLD/'central_integrality/integer_gram_1154.json').read_text())
 source=json.loads((ROOT/'evidence/unresolved_retry_20261024/proofs/unresolved11_20261024/inputs/R8_3_1154.json').read_text())
 R=source['fusion_tensor']; a=c.w.data(R); K=a['K']
 L=c.s.Matrix.hstack(*map(c.s.Matrix,domain['low_columns']))
 def frozen_high(data,frame):
  if frame!=L: raise ValueError('Different low frame')
  ds=data['dimensions']
  high=[(tuple(v),tuple(sum((Q(v[i])*ds[i+1][k] for i in range(7)),Q(0)) for k in range(2))) for v in domain['high_columns']]
  return c.s.Matrix(domain['gram_remainder']),high
 md.full.base.grams.high_columns=frozen_high
 start=time.monotonic()
 height=3
 A,b,meta=md.full.system(R,a,L,(0,0,-1,1,1,1,1),height)
 A,b,meta=md.append_sts(R,a,domain['low_columns'],(0,1,2,3,4),A,b,meta,height)
 types,bound=md.full.h.trace_types(a['q'],a['primes'],height)
 high=md.full.base.grams.high_columns(a,L)[1]
 nv=len(A[0]); nt=len(types)
 LL=L*L.T; dims=a['dimensions']; D=a['global_dimension']
 low=[tuple(sum((Q(int(LL[i,j]))*dims[j][k] for j in range(8)),Q(0)) for k in range(2)) for i in range(8)]
 mul=lambda x,y:md.full.h.mul(x,y,a['q'])
 
 # Fix all high restriction multiplicities in each of the three frozen patterns.
 countrows=[]
 for h in range(len(high)):
  row=[0]*nv
  for t in range(nt): row[h*nt+t]=1
  countrows.append(row)
 
 # The four I(g) packet twists are two i and two -i, hence normalized
 # Q(sqrt(5))-traces (0,-1,0,1). Other trace types on this support are removed.
 packettrace=((Q(0),Q(0)),(Q(-1),Q(0)),(Q(0),Q(0)),(Q(1),Q(0)))
 keep=[j for j in range(nv) if j>=len(high)*nt or j//nt!=10 or tuple(types[j%nt])==packettrace[:height]]
 A=[[row[j] for j in keep] for row in A]
 countrows=[[row[j] for j in keep] for row in countrows]
 
 rotationrows=[]; constants=[]
 for i in objects:
  for k in range(2):
   row=[]
   for j in range(nv):
    if j<len(high)*nt:
     h,t=divmod(j,nt); v,z=high[h]
     row.append(v[i-1]*mul(z,types[t][2])[k])
    else: row.append(Q(0))
   row=[row[j] for j in keep]
   den=math.lcm(*(v.denominator for v in row),low[i][k].denominator,D[k].denominator)
   rotationrows.append([int(v*den) for v in row]); constants.append((den*D[k],den*low[i][k]))
 
 AA=A+countrows+rotationrows
 return AA,b,constants,domain,dict(height=height,variables=len(keep),rows=len(AA),objects=list(objects),source_tensor=R,types=types,keep=keep)
