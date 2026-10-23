"""Enumerate normalized sign branches and exclude inadmissible dimensions.

Only zero dimensions, unequal dual dimensions, and exact mandatory dimension-
field containment are used. No commutativity is assumed for signed quotients.
"""
import json,sys,itertools,time,collections
from pathlib import Path
import sympy as s
from oriented import *
from exact import t,field,pc,ec,evaluate,vector,norm_failure,field_failure

def signed_tensor(R,a,values):
 T=json.loads(json.dumps(R))
 for ijk,v in a['mapping'].items():
  i,j,k=ijk;T[i][j][k]*=(-1 if values>>v&1 else 1)
 return T

def validate(T,du):
 n=len(T)
 for i,j,k in itertools.product(range(n),repeat=3):
  require(T[0][i][j]==T[i][0][j]==int(i==j),'unit')
  require(T[i][j][0]==int(du[i]==j),'dual unit coefficient')
  require(T[i][j][k]==T[du[i]][k][j]==T[k][du[j]][i]==T[du[j]][du[i]][du[k]],'oriented Frobenius reciprocity')
 N=list(map(s.Matrix,T))
 for i,j in itertools.product(range(n),repeat=2):
  require(N[i]*N[j]==sum((T[j][i][k]*N[k] for k in range(n)),s.zeros(n)),'oriented associativity')
 return True

def char_data(T):
 n=len(T);N=list(map(s.Matrix,T))
 if comm(T):W=s.eye(n)
 else:
  cs=[N[i]*N[j]-N[j]*N[i] for i in range(n) for j in range(i)]
  vs=s.Matrix.vstack(*cs).nullspace()
  if not vs:return None
  W=s.Matrix.hstack(*vs)
 m=W.cols;piv=list(W.T.rref()[1]);J=W.extract(piv,range(m)).inv();A=[J*(a*W).extract(piv,range(m)) for a in N]
 require(all(a*W==W*b for a,b in zip(N,A)),'scalar character space invariant')
 for k in range(1,max(3,n*n*n)):
  H=A[0]+sum((k**(i-1)*A[i] for i in range(1,n)),s.zeros(m));p=H.charpoly(t).as_poly()
  if s.gcd(p,p.diff()).degree()==0:break
 require(s.gcd(p,p.diff()).degree()==0,'scalar character separator')
 V=s.Matrix.hstack(*[s.Matrix(list(H**j)) for j in range(m)])
 coeff=[list(V.gauss_jordan_solve(s.Matrix(list(a)))[0]) for a in A]
 require(all(sum((co[j]*H**j for j in range(m)),s.zeros(m))==a for co,a in zip(coeff,A)),'polynomial character coordinates')
 return dict(W=W,A=A,k=k,p=p,coeff=coeff)

def dimension_test(R,T,du):
 a=char_data(T)
 if a is None:return {'all_dimension_characters_excluded':True,'reason':'no_scalar_characters','branches':[]}
 required=[]
 # For field containment only, regular Casimir eigenvalues dim(E)*f_E
 # and f_E generate exactly the same field. No norm test with these
 # scaled eigenvalues is used.
 for U in (R,T):
  N=list(map(s.Matrix,U));C=sum((N[i]*N[du[i]] for i in range(len(U))),s.zeros(len(U)))
  required+=C.charpoly(t).as_poly().factor_list()[1]
 bs=[]
 for f,e in a['p'].factor_list()[1]:
  require(e==1,'scalar characters separated');K=field(f)
  ds=[K(s.Poly.from_list(list(reversed(co)),t,domain=s.QQ).rem(f).all_coeffs()) for co in a['coeff']]
  delta=sum((ds[i]*ds[du[i]] for i in range(len(T))),K.zero)
  reason=None
  zero=next((i for i,d in enumerate(ds) if not d),None)
  if zero is not None:reason=dict(kind='zero_dimension',object=zero)
  neq=next((i for i,d in enumerate(ds) if d!=ds[du[i]]),None)
  if reason is None and neq is not None:reason=dict(kind='unequal_dual_dimensions',object=neq)
  if reason is None:reason=field_failure(f,required)
  bs.append(dict(factor=pc(f),dimensions=[ec(d) for d in ds],global_dimension=ec(delta),obstruction=reason))
 return dict(all_dimension_characters_excluded=all(b['obstruction'] for b in bs),scalar_character_dimension=a['W'].cols,separating_k=a['k'],separating_polynomial=pc(a['p']),branches=bs)

def analyze(r):
 R=r['tensor'];a=linear_analysis(R);res=serial_analysis(r,a);branches=[]
 for z in range(1<<len(a['free'])):
  zfull=sum(((z>>j)&1)<<i for j,i in enumerate(a['free']));values=sum(parity(m&zfull)<<i for i,m in enumerate(a['reduced_variables']))
  fail=next(({'source':list(source),'difference':sum(c*(-1 if parity(m&values) else 1) for m,c in p.items())} for source,p in a['equations'] if sum(c*(-1 if parity(m&values) else 1) for m,c in p.items())),None)
  branch=dict(free_bits=z,sign_assignment=values,associativity_failure=fail)
  if not fail:
   T=signed_tensor(R,a,values);validate(T,a['du']);branch['signed_tensor_sha256']=hashlib.sha256(json.dumps(T,separators=(',',':')).encode()).hexdigest();branch['commutative']=comm(T)
   if values==0:branch['outcome']='gauge_original'
   else:
    branch['dimension_test']=dimension_test(R,T,a['du']);branch['outcome']='excluded_dimension_characters' if branch['dimension_test']['all_dimension_characters_excluded'] else 'signed_branch_survives'
  else:branch['outcome']='not_associative'
  branches.append(branch)
 res['branches']=branches;res['all_signed_tables_are_gauge_original']=all(b['outcome'] in ['not_associative','gauge_original'] for b in branches)
 res['all_categorical_signed_tables_are_gauge_original']=all(b['outcome']!='signed_branch_survives' for b in branches)
 return res

if __name__=='__main__':
 out=[];start=time.monotonic()
 for r in targets():
  rec=analyze(r);out.append(rec);(P/'ledger.json').write_text(json.dumps(out,indent=2)+'\n')
  print(r['id'],'branches',[b['outcome'] for b in rec['branches']],'seconds',round(time.monotonic()-start,2),flush=True)
 print('DONE',len(out),'gauge trivial',sum(r['all_signed_tables_are_gauge_original'] for r in out),'categorical gauge trivial',sum(r['all_categorical_signed_tables_are_gauge_original'] for r in out),'seconds',time.monotonic()-start,flush=True)
