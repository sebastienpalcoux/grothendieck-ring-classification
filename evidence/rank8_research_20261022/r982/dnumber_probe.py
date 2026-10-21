"""Exact d-number filter on previously enumerated central restrictions."""
from pathlib import Path
import argparse,json,hashlib
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
OLD=ROOT/'evidence/rank8_next_20261021/r982'
P=ROOT/'evidence/rank8_frontier_20261021/commutative_integer/R8_3_982_profile.json'
DIM=[(1,0,0,0),(2,2,1,1),(2,2,1,1),(3,2,2,1),(3,2,2,1),(2,1,1,1),(1,0,0,0),(2,1,1,1)]
PROFILE_SHA='0c39c6201219fcd43bb7b490bfa3ce9aac5949a9378fe5506ed2f62743753bfc'
TENSOR_SHA='f4a9fb77b3a78e9dcd8370ca9fa822ea331f1b71e3fad7990efdd386445fcd1c'
Z=(0,0,0,0);ONE=(1,0,0,0)
def need(c,m):
 if not c:raise ValueError(m)
def add(x,y):return tuple(a+b for a,b in zip(x,y))
def neg(x):return tuple(-a for a in x)
def mul(x,y):
 z=[0]*4
 for i,a in enumerate(x):
  for j,b in enumerate(y):
   z[i^j]+=a*b*(2 if i&j&1 else 1)*(3 if i&j&2 else 1)
 return tuple(z)
def dim(v):return tuple(sum(n*d[k]for n,d in zip(v,DIM))for k in range(4))
def minpoly(v):
 conj={(v[0],s*v[1],t*v[2],s*t*v[3])for s in(-1,1)for t in(-1,1)}
 p=[ONE]
 for root in sorted(conj):
  out=[Z]*(len(p)+1)
  for i,a in enumerate(p):out[i]=add(out[i],mul(a,neg(root)));out[i+1]=add(out[i+1],a)
  p=out
 if any(any(a[1:])for a in p):raise AssertionError('not rational')
 return [a[0]for a in reversed(p)]
def dn(v):
 p=minpoly(v);n=len(p)-1
 return all(pow(p[i],n)%pow(p[-1],i)==0 for i in range(1,n+1))
def inputs():
 need(hashlib.sha256(P.read_bytes()).hexdigest()==PROFILE_SHA,'complete center domain binding')
 row=next(r for r in json.loads((ROOT/'evidence/rank8_m3_20261021/pipeline/census_m3.json').read_text())if r['id']=='R8_3_982')
 R=row['tensor'];need(hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()==TENSOR_SHA,'canonical tensor')
 need(all(mul(DIM[i],DIM[j])==dim(R[i][j])for i in range(8)for j in range(8)),'exact FP dimension homomorphism')
 need(all(all(x>=0 for x in v)and any(v)for v in DIM),'positive radical FP embedding')
 profile=json.loads(P.read_text())['records'][2]
 return [(0,)+tuple(row['vector'])for row in profile['high_vectors']]
def run():
 vectors=inputs()
 need(dn(ONE)and not dn((3,1,0,0)),'positive and negative d-number controls')
 keep=[dn(dim(v))for v in vectors]
 return {'scope':'pseudo_unitary_center_necessary_dnumber_filter','canonical_profile_sha256':PROFILE_SHA,'tensor_sha256':TENSOR_SHA,'high_vectors':len(vectors),'high_vectors_dnumber':sum(keep),'high_vectors_rejected':len(vectors)-sum(keep),'controls':'unit passes; 3+sqrt(2) fails'}
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--write',action='store_true');args=parser.parse_args()
 out=run();path=HERE/'dnumber_probe.json'
 if args.write:path.write_text(json.dumps(out,indent=2)+'\n')
 else:need(out==json.loads(path.read_text()),'saved d-number receipt changed')
 print('PASS: all 2636 center restrictions satisfy the exact d-number criterion; no new exclusion.')
