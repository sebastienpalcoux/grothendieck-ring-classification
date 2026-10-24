"""Weighted center relaxation for the previously uncovered noncommutative1975.
The regular algebra is C^5+M2(C); center restriction columns lie in range(B).
"""
from pathlib import Path
import json,sys,itertools,time,math,collections,types,hashlib
from fractions import Fraction as Q
import sympy as s
import flint
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'work'),str(ROOT/'sources'),str(ROOT/'phase2/quadratic_theory')]
import quadratic_center as qc
from scalar_characters import chars
from exact import ec,t
from induction import discover_roots
from higher_traces import mul,integer_pair

def base(R):
 n=9;a=chars(R);f,K,ds,D,pD,emb=a.fp();d=ds[1]
 assert ds==[K.one]+[d]*4+[K.one]*3+[K(2)] and d*d==8*d+2
 B=s.Matrix(n,n,lambda j,i:sum(R[b][j][k]*R[k][a.du[b]][i]for b,k in itertools.product(range(n),repeat=2)))
 indices=[0,1,2,5,6,8];G=B.extract(indices,indices);inv=G.inv();den=int(s.ilcm(*[c.q for c in inv]));J=inv*den
 assert B.rank()==6 and all(B.row(i)==B.row(j)for i,j in[(1,3),(2,4),(6,7)])
 dims=[(Q(1),Q(0))]+[(Q(4),Q(3))]*4+[(Q(1),Q(0))]*3+[(Q(2),Q(0))]
 DD=(Q(144),Q(96));q=2
 scalar_roots=discover_roots(a.scalar_codegree_polynomial,K);remaining=a.C.charpoly(t).as_poly().exquo(a.scalar_codegree_polynomial)
 assert remaining==(t-8)**4
 spectral=[(r,1)for r in scalar_roots]+[(K(4),2)]
 def pair(x):
  z=list(map(Q,ec(x)));z=[Q(0)]*(2-len(z))+z
  # separating generator = 369+15d = 429+45sqrt2
  return(z[1]+429*z[0],45*z[0])
 assert pair(d)==(4,3) and pair(D)==DD
 lowtypes=collections.Counter((e,pair(D/r))for r,e in spectral);counts=collections.Counter()
 for(e,z),c in lowtypes.items():counts[z]+=c
 bounds=[math.isqrt(int(G[i,i]))for i in range(6)];bounds[0]=2
 raw=[];cols=[]
 for w in itertools.product(*(range(b+1)for b in bounds)):
  if not any(w):continue
  if any(w[i]*w[j]>G[i,j]for i in range(6)for j in range(i+1)):continue
  if sum(w[i]*J[i,j]*w[j]for i in range(6)for j in range(6))>den:continue
  v=(w[0],w[1],w[2],w[1],w[2],w[3],w[4],w[4],w[5]);raw.append(v)
  z=tuple(sum(v[i]*dims[i][c]for i in range(n))for c in range(2))
  if v[0]:
   if (v[0],z)not in lowtypes:continue
  else:
   norm=z[0]**2-q*z[1]**2
   if norm==0 or not integer_pair(qc.div(DD,z,q),q):continue
   if z[1]and((2*z[0])**2/norm).denominator!=1:continue
  cols.append((v,z))
 premod=len(cols)
 W=s.Matrix.hstack(*s.Matrix.vstack(*(a.N[i]*a.N[j]-a.N[j]*a.N[i]for i in range(n)for j in range(i))).nullspace())
 assert W.cols==5
 P=W*(W.T*W).inv()*W.T;E=2*s.eye(n)-P
 op=E*a.C.inv();denop=int(s.ilcm(*[x.q for x in op]));ops=[list(map(int,op*N*denop))for N in a.N]
 keep=[]
 for v,z in cols:
  Nv=sum((v[i]*a.N[i]for i in range(n)),s.zeros(n));assert all(Nv*N==N*Nv for N in a.N)
  M=flint.fmpq_mat(n,n,[flint.fmpq(sum(v[i]*ops[i][j]for i in range(n)),denop)for j in range(n*n)])
  coeff=list(M.charpoly());ratio=qc.div(DD,z,q);power=(Q(1),Q(0));ok=True
  for j in range(1,n+1):
   power=mul(power,ratio,q)
   if not integer_pair(qc.scale(power,Q(str(coeff[n-j]))),q):ok=False;break
  if ok:keep.append((v,z))
 cols=keep;ratio=qc.div(DD,(DD[0],-DD[1]),q)
 def conj(z):
  x=mul(ratio,(z[0],-z[1]),q);return x if qc.sign(x,q)>0 else qc.scale(x,-1)
 available={z for v,z in cols};keep={z for z in available if conj(z)in available};cols=[(v,z)for v,z in cols if z in keep]
 pairs=sorted({tuple(sorted((z,conj(z))))for z in keep if z!=conj(z)})
 print('columns',len(raw),premod,len(cols),'low',sum(bool(v[0])for v,z in cols),flush=True)
 return {'ch':types.SimpleNamespace(C=B,n=n,du=a.du),'q':q,'dims':dims,'D':DD,'counts':counts,'cols':cols,'galois_pairs':pairs,'primes':[2,3],'raw_columns':len(raw),'pre_modular_columns':premod,'pre_galois_dimensions':len(available),'post_galois_dimensions':len(keep),'lowtypes':lowtypes}

def system(R,height=3):
 data=base(R);prev=qc.base;qc.base=lambda _:data
 try:A,b,meta=qc.system(R,height)
 finally:qc.base=prev
 meta['weighted_lowtypes']=[{'degree':e,'dimension':list(map(str,z)),'count':v}for(e,z),v in data['lowtypes'].items()]
 meta['noncommutative_modular_operator']='(D/z) (2I-P_scalar) C_regular^-1 N_v'
 return A,b,meta

def main():
 height=int(sys.argv[1])if len(sys.argv)>1 else 3;R=qc.inputs('R9_2_1975');start=time.monotonic();A,b,meta=system(R,height)
 print('system',len(A),len(A[0]),flush=True);ray,why=qc.exact_separator(A,b,timeout=90)
 if ray:qc.verify_ray(A,b,ray)
 out={'id':'R9_2_1975','outcome':'candidate_exclusion_pending_independent_audit'if ray else'no_conclusion','metadata':meta,'ray':ray,'solver_report':why,'seconds':time.monotonic()-start,'tensor_sha256':hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()}
 Path(__file__).with_name('result_h'+str(height)+'.json').write_text(json.dumps(out,indent=2)+'\n');print(out['outcome'],out['solver_report'],out['seconds'],flush=True)
if __name__=='__main__':main()
