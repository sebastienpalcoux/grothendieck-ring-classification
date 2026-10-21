"""Read-only exact replay of every M3 baseline tensor and exclusion.

The optimized entrypoint re-executes without -O because historical imported
certificate routines contain assertions. New checks use explicit exceptions.
"""
import os,sys
if sys.flags.optimize:
 os.environ['M3_BASELINE_REQUESTED_OPTIMIZATION']='-O';os.execv(sys.executable,[sys.executable,__file__]+sys.argv[1:])
for _key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS'):os.environ[_key]='1'
import argparse,collections,concurrent.futures,gzip,hashlib,json,time
from pathlib import Path
from m3_campaign import REPO,P,OUT,RAW_SHA,GZ_SHA,OLD_SHA,require,sha,verify_certificate
from analyze import fp,commutes,mult
from prepare import flatten
import numpy as np
def check_tensor(R):
 require(len(R)==8 and all(len(M)==8 and all(len(row)==8 for row in M) for M in R),'rank-eight shape')
 require(all(type(v) is int and 0<=v<=3 for v in flatten(R)),'bounded nonnegative integer coefficients')
 A=np.asarray(R,dtype=np.int64);I=np.eye(8,dtype=np.int64)
 require(np.array_equal(A[0],I) and np.array_equal(A[:,0,:],I),'unit')
 require(all(sum(R[i][j][0] for j in range(8))==1 for i in range(8)),'unique dual')
 du=[next(j for j in range(8) if R[i][j][0]) for i in range(8)]
 require(all(du[du[i]]==i for i in range(8)),'dual involution')
 for i in range(8):
  for j in range(8):
   for k in range(8):require(R[i][j][k]==R[du[i]][k][j]==R[k][du[j]][i],'Frobenius reciprocity')
 # At most eight terms, each product <=9: int64 cannot overflow.
 for i in range(8):
  for j in range(8):require(np.array_equal(A[i]@A[j],np.einsum('k,kab->ab',A[j,i],A)),'associativity')
def check_row(pair):
 row,decision=pair;R=row['tensor'];check_tensor(R);require(row['id']==decision['id'],'decision identity');require(row['tensor_sha256']==decision['tensor_sha256']==fp(R),'tensor digest');require(row['commutative']==decision['commutative']==commutes(R),'commutativity')
 require(decision['status'] in ('excluded','unresolved'),'baseline status')
 if decision['status']=='excluded':verify_certificate(R,decision['certificate'])
 else:require('certificate' not in decision,'unresolved baseline has certificate')
 return decision['status']
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--jobs','--workers',type=int,default=8);ap.add_argument('--report',type=Path);args=ap.parse_args();start=time.monotonic()
 rows=json.loads((OUT/'census_m3.json').read_text());decisions=json.loads((OUT/'decisions_m3.json').read_text());require(len(rows)==len(decisions)==3527,'baseline length')
 p=P/'data/rank8_m3_tables.txt.gz';require(sha(p)==GZ_SHA,'source gzip digest');raw=gzip.decompress(p.read_bytes());require(hashlib.sha256(raw).hexdigest()==RAW_SHA,'source raw digest')
 source=[json.loads(s.replace('{','[').replace('}',']')) for s in raw.decode().splitlines() if s.strip()]
 new=sorted([R for R in source if mult(R)==3],key=flatten);require([r['tensor'] for r in rows]==new,'ID ordering and full tensor source binding')
 require([r['id'] for r in rows]==[f'R8_3_{i}' for i in range(1,3528)],'IDs')
 oldraw=gzip.decompress((P/'data/rank8_tables.txt.gz').read_bytes());old=[json.loads(s.replace('{','[').replace('}',']')) for s in oldraw.decode().splitlines() if s.strip()]
 require([R for R in source if mult(R)<=2]==old,'old source ordered subsequence');require(sha(P/'data/decisions.json')==OLD_SHA,'historical decisions digest')
 with concurrent.futures.ProcessPoolExecutor(max_workers=args.jobs) as pool:counts=collections.Counter(pool.map(check_row,zip(rows,decisions)))
 require(counts=={'excluded':3250,'unresolved':277},'unexpected recovered baseline counts')
 report={'result':'PASS','records':3527,'counts':dict(counts),'all_fusion_axioms_checked':True,'all_exclusions_exactly_replayed':True,'source_gzip_sha256':GZ_SHA,'source_raw_sha256':RAW_SHA,'old_decisions_sha256':OLD_SHA,'census_sha256':sha(OUT/'census_m3.json'),'decisions_sha256':sha(OUT/'decisions_m3.json'),'requested_optimization':os.environ.get('M3_BASELINE_REQUESTED_OPTIMIZATION','normal'),'assertions_enabled':__debug__,'seconds':time.monotonic()-start}
 if args.report:args.report.parent.mkdir(parents=True,exist_ok=True);args.report.write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(report,sort_keys=True))
if __name__=='__main__':main()
