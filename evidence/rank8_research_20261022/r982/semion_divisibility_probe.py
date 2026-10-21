"""A modular semion centralizer has integral formal codegrees."""
from fractions import Fraction as Q
import json
from dnumber_probe import *
def scale(t,v):return tuple(t*x for x in v)
def inv(v):
 p=minpoly(v);acc=ONE
 # Product of the three nonidentity embeddings, including repeated values.
 for a,b in [(-1,1),(1,-1),(-1,-1)]:acc=mul(acc,(v[0],a*v[1],b*v[2],a*b*v[3]))
 norm=mul(v,acc)
 if any(norm[1:])or not norm[0]:raise AssertionError('bad norm')
 return scale(Q(1,norm[0]),acc)
def integral(v):return all(Q(x).denominator==1 for x in minpoly(v))
def run():
 vectors=inputs()
 need(integral(ONE)and not integral((Q(1,2),0,0,0)),'integrality controls')
 D=Z
 for d in DIM:D=add(D,mul(d,d))
 cache={}
 def tests(v):
  d=dim(v)
  if d not in cache:
   ratio=mul(D,inv(d));half_square=scale(Q(1,2),mul(ratio,ratio))
   cache[d]=[integral(ratio),integral(half_square)]
  return cache[d]
 flags=[tests(v)for v in vectors]
 return {'scope':'pseudo_unitary_center_modular_semion_factor_necessary_divisibility','canonical_profile_sha256':PROFILE_SHA,'tensor_sha256':TENSOR_SHA,'global_source_dimension':D,'high_vectors':len(vectors),'distinct_dimensions':len(cache),'center_divisibility_survivors':sum(x[0]for x in flags),'semion_centralizer_codegree_integral_survivors':sum(x[1]for x in flags)}
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--write',action='store_true');args=parser.parse_args()
 out=json.loads(json.dumps(run()));path=HERE/'semion_divisibility_probe.json'
 if args.write:path.write_text(json.dumps(out,indent=2)+'\n')
 else:need(out==json.loads(path.read_text()),'saved semion divisibility receipt changed')
 print('PASS: all 2636 center restrictions satisfy center and semion-centralizer divisibility; no new exclusion.')
