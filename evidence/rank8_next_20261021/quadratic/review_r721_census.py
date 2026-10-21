"""Independent exhaustive R721 dimension crosswalk review.
Uses modular determinant necessary tests and rational doubled-field equations,
not the producer's characteristic-polynomial screen or quadratic Gaussian code.
"""
from pathlib import Path
from fractions import Fraction as F
import json,gzip,hashlib,itertools,collections
import sympy as s
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
def need(b,msg):
 if not b:raise ValueError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def fingerprint(R):return sha(json.dumps(R,separators=(',',':')).encode())
def determinant_mod(A,p):
 A=[[v%p for v in row]for row in A];det=1
 for j in range(len(A)):
  k=next((i for i in range(j,len(A))if A[i][j]),None)
  if k is None:return 0
  if k!=j:A[k],A[j]=A[j],A[k];det=-det
  pivot=A[j][j];det=det*pivot%p;iv=pow(pivot,-1,p)
  for i in range(j+1,len(A)):
   c=A[i][j]*iv%p
   for k in range(j+1,len(A)):A[i][k]=(A[i][k]-c*A[j][k])%p
 return det%p
def mul(a,b):return(a[0]*b[0]+17*a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def run():
 paths=[ROOT/'supplements/rank8/data/rank8_m3_tables.txt.gz',ROOT/'supplements/rank8/data/rank8_tables.txt.gz',ROOT/'evidence/rank8_m3_20261021/pipeline/census_m3.json',ROOT/'supplements/rank8/data/decisions.json',ROOT/'evidence/rank8_m3_20261021/pipeline/source_manifest.json',HERE.parent/'r721/census_dimension_crosswalk.json',HERE.parent/'r721/census_dimension_crosswalk.py']
 raw=gzip.decompress(paths[0].read_bytes());oldraw=gzip.decompress(paths[1].read_bytes());parse=lambda b:[json.loads(line.replace('{','[').replace('}',']'))for line in b.decode().splitlines()if line.strip()];Rings=parse(raw);old=parse(oldraw);m=json.loads(paths[4].read_text());need(sha(raw)==m['source_raw_sha256']and sha(paths[0].read_bytes())==m['source_gzip_sha256'],'cumulative immutable source digest')
 hashes=list(map(fingerprint,Rings));oldhash=list(map(fingerprint,old));records=json.loads(paths[2].read_text())+json.loads(paths[3].read_text());need(len(Rings)==len(set(hashes))==len(records)==4500 and len(old)==973,'all4500 unique cumulative tensors and historical records');need(len({r['id']for r in records})==4500,'unique historical IDs');lookup={r['tensor_sha256']:r for r in records};need(set(lookup)==set(hashes),'complete exact ID/tensor bijection');need([h for h in hashes if h in set(oldhash)]==oldhash,'all973 older tensors retained in order')
 primes=[]
 for p in (1009,1013,1019,1021,1031,1033,1039):
  if not s.isprime(p):continue
  root=next((r for r in range(p)if r*r%p==17),None)
  if root is not None:primes.append((p,root))
  if len(primes)==2:break
 need(len(primes)==2,'two prime reductions of sqrt17')
 target=[(F(1),F(0)),(F(3,2),F(1,2)),(F(3,2),F(1,2)),(F(5,2),F(1,2)),(F(5,2),F(1,2)),(F(4),F(1)),(F(3),F(1)),(F(5),F(1))];need(tuple(map(sum,zip(*target)))==(21,5),'necessary dimension sum');hist=collections.Counter();duhist=collections.Counter();mods=[];spectral=[];matches=[];audit=hashlib.sha256();x=s.Symbol('x')
 for line,(R,h)in enumerate(zip(Rings,hashes),1):
  need(len(R)==8 and all(len(M)==8 and all(len(row)==8 for row in M)for M in R),'tensor shape');flat=[z for M in R for row in M for z in row];need(all(type(z)is int and 0<=z<=3 for z in flat),'integer multiplicity bound');hist[max(flat)]+=1
  dual=[next(j for j in range(8)if R[i][j][0])for i in range(8)];duhist[sum(i!=j for i,j in enumerate(dual))//2]+=1
  M=[[sum(R[i][j][k]for i in range(8))for k in range(8)]for j in range(8)];need(all(z>0 for row in M for z in row),'strictlypositive regularsum')
  remainders=[determinant_mod([[M[i][j]-(21+5*r if i==j else 0)for j in range(8)]for i in range(8)],p)for p,r in primes];audit.update((h+':'+','.join(map(str,remainders))+'\n').encode())
  if any(remainders):continue
  mods.append(lookup[h]['id']);P=s.Matrix(M).charpoly(x).as_poly();q=s.Poly(x*x-42*x+16,x)
  if not P.rem(q).is_zero:continue
  spectral.append(lookup[h]['id'])
  # d=u+v sqrt17, (M-21I)u-85v=0, (M-21I)v-5u=0.
  C=s.Matrix(M)-21*s.eye(8);L=C.row_join(-85*s.eye(8)).col_join((-5*s.eye(8)).row_join(C));E=L.row_join(s.zeros(16,1));E=E.col_join(s.Matrix([[int(j==0)for j in range(16)]+[1],[int(j==8)for j in range(16)]+[0]]));rr,piv=E.rref();need(piv==tuple(range(16))and not any(rr[16:,:]),'unique normalized rational doubled-field eigenvector');dims=[(F(str(rr[i,16])),F(str(rr[i+8,16])))for i in range(8)]
  if collections.Counter(dims)!=collections.Counter(target):continue
  for i,j in itertools.product(range(8),repeat=2):need(mul(dims[i],dims[j])==tuple(sum(R[i][j][k]*dims[k][q]for k in range(8))for q in(0,1)),'all64 exact FP equations')
  need(tuple(sum(mul(d,d)[q]for d in dims)for q in(0,1))==(136,32),'exact global dimension');matches.append({'id':lookup[h]['id'],'source_line':line,'tensor_sha256':h,'dimensions':[[str(a),str(b)]for a,b in dims]})
 need(hist=={1:96,2:877,3:3527}and duhist=={0:2621,1:1278,2:516,3:85},'all multiplicity/duality shards covered');need([r['id']for r in matches]==['R8_3_721'],'exactlyone dimension match');producer=json.loads(paths[5].read_text());need(spectral==[r['id']for r in producer['spectral_filter_survivors']]and [r['tensor_sha256']for r in matches]==[r['tensor_sha256']for r in producer['matches']],'independent complete result agrees')
 out={'kind':'independent_complete_R721_census_dimension_review','imports_producer_modules':False,'cumulative_tensors':4500,'previous_tensors':973,'complete_bijective_ID_coverage':True,'multiplicity_shards':dict(hist),'duality_shards':dict(duhist),'modular_primes_and_sqrt17_roots':primes,'modular_screen_sha256':audit.hexdigest(),'modular_filter_survivors':mods,'exact_spectral_survivors':spectral,'matches':matches,'scope':'Complete accepted4500-ring multiplicity-at-most3 census crosswalk; classification source completeness is the existing census theorem/input. Modular tests are exact necessary filters, never floating-point exclusions.','source_sha256':{str(p.relative_to(ROOT)):sha(p.read_bytes())for p in paths},'verifier_sha256':sha(Path(__file__).read_bytes())}
 (HERE/'r721_census_review.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));return out
if __name__=='__main__':run()
