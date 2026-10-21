"""Bind the new finite enumerations to immutable tensors and old candidate domains."""
import hashlib,json,itertools
import sympy as s
from gram_discovery import HERE,REPO,OLD,TARGETS,rows,require
from integral_gram import bounded_solutions
from morita_closure import DATA,dim,mul,enc
from module_rows import FLOORS

def verify():
 paths=[REPO/'evidence/rank8_m3_20261021/pipeline/census_m3.json',OLD/'quadratic/connected_algebra_candidates_results.json',OLD/'structural_models/algebra_candidates.json']
 bindings={str(p.relative_to(REPO)):hashlib.sha256(p.read_bytes()).hexdigest()for p in paths}
 src={x['id']:x for x in json.loads(paths[0].read_text())}
 old=json.loads(paths[1].read_text())['records']+json.loads(paths[2].read_text())['records']
 domain={(x['id'],i):a for x in old if x['id']in TARGETS for i,a in enumerate(x['necessary_survivor_vectors'])}
 recs=json.loads((HERE/'integral_gram.json').read_text());require(len(recs)==len(domain)==302,'complete candidate coverage')
 require({(x['id'],x['candidate_index'])for x in recs}==set(domain),'exact keys')
 positive_controls=[]
 for rid,(q,ds)in DATA.items():
  R=src[rid]['tensor']
  require([int(s.floor(s.Rational(d[0])+s.Rational(d[1])*s.sqrt(q)))for d in ds]==FLOORS[rid],'exact FP entry floors')
  for i,j in itertools.product(range(8),repeat=2):require(mul(ds[i],ds[j],q)==dim(R[i][j],ds),'exact FP homomorphism')
  for i in range(8):
   dual=next(j for j in range(8)if R[i][j][0]);a=R[i][dual]
   ai=next(k[1]for k,v in domain.items()if k[0]==rid and v==a)
   # Induction from the regular C-module category based at X_i.
   B=[[R[j][i][k]for j in range(8)]for k in range(8)]
   require(B[i]==a,'canonical distinguished row')
   positive_controls.append({'id':rid,'simple':i,'candidate_index':ai,'induction_rows':B})
 for x in recs:
  rid=x['id'];ai=x['candidate_index'];a=domain[(rid,ai)];R=src[rid]['tensor'];require(a==x['algebra_object'],'object source')
  G=s.Matrix(8,8,lambda i,j:sum(a[k]*R[i][k][j]for k in range(8))-a[i]*a[j]);require(G.tolist()==x['gram'],'Gram source')
  V,meta=rows(G);require(V==[tuple(v)for v in x['vectors']]and meta==x['enumeration'],'complete ellipsoid rows')
  P=list(G.rref()[1]);H=G.extract(P,P)
  require(all(H[:k,:k].det()>0 for k in range(1,len(P)+1)),'positive principal block')
  require(not P or G==G[:,P]*H.inv()*G[P,:],'PSD rank decomposition')
  bounds=[min(int(G[i,i])//v[i]**2 for i in range(8)if v[i])for v in V];require(bounds==x['bounds'],'complete multiplicity bounds')
  pairs=list(itertools.combinations_with_replacement(range(8),2));A=s.Matrix([[v[i]*v[j]for v in V]for i,j in pairs]);b=[G[i,j]for i,j in pairs]
  sol,meta=bounded_solutions(A,b,bounds);require(sol==x['all_multiplicities'],'complete integer factors')
 report={'sources':bindings,'candidate_count':len(recs),'tensor_sha256':{r:src[r]['tensor_sha256']for r in sorted(TARGETS)},'exact_FP_homomorphism_verified':True,'complete_Gram_enumeration_verified':True,'canonical_internal_end_positive_controls':positive_controls}
 (HERE/'source_verification.json').write_text(json.dumps(report,default=int,separators=(',',':'))+'\n');print('Verified source binding and complete exact Gram enumeration for',len(recs),'objects; canonical controls',len(positive_controls))
 return report
if __name__=='__main__':verify()
