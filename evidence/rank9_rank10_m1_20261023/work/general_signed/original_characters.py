"""Exact spherical dimension-character reduction on original rings.

Computes all scalar characters, including for noncommutative rings. Uses
actual formal codegrees rather than dimension-weighted Casimir eigenvalues.
Remaining dimension characters are checked for a positive tensor-sign Galois
embedding, which yields a pseudo-unitary spherical structure after twisting.
"""
import json,itertools,time,collections
import sympy as s
from branches import char_data
from oriented import *
from exact import t,field,pc,ec,vector,norm_failure,field_failure,embeddings

def formal_codegrees(R,a,du):
 n=len(R);N=list(map(s.Matrix,R));C=sum((N[i]*N[du[i]] for i in range(n)),s.zeros(n));cp=C.charpoly(t).as_poly()
 A=a['A'];qlin=sum((A[i]*A[du[i]] for i in range(n)),s.zeros(A[0].rows)).charpoly(t).as_poly()
 quotient,rem=cp.div(qlin);require(rem.is_zero,'linear Casimir factor divides full')
 factors=qlin.factor_list()[1];deficit=n-A[0].rows
 if deficit:
  require(deficit in [4,8,9],'Wedderburn type supported');d=3 if deficit==9 else 2
  for q,e in quotient.factor_list()[1]:
   require(e%(d*d)==0,'matrix block multiplicity')
   f=s.Poly(q.as_expr().subs(t,d*t)/d**q.degree(),t,domain=s.QQ)
   require(all(v.q==1 for v in f.all_coeffs()),'formal codegrees algebraic integral')
   factors.append((f,e//(d*d)))
 return factors,pc(cp),pc(qlin)

def analyze(r):
 R=r['tensor'];n=len(R);du=[next(j for j in range(n) if R[i][j][0]) for i in range(n)]
 a=char_data(R);require(a is not None,'FP character exists');required,cp,clp=formal_codegrees(R,a,du);bs=[]
 for f,e in a['p'].factor_list()[1]:
  require(e==1,'separating scalar characters');K=field(f)
  ds=[K(s.Poly.from_list(list(reversed(co)),t,domain=s.QQ).rem(f).all_coeffs()) for co in a['coeff']]
  delta=sum((ds[i]*ds[du[i]] for i in range(n)),K.zero);u=K(s.Poly(t,t).rem(f).all_coeffs())
  pD=s.Matrix.hstack(*(vector(delta*u**i,f.degree()) for i in range(f.degree()))).charpoly(t).as_poly().sqf_part().monic()
  require(all(v.q==1 for v in pD.all_coeffs()),'global-dimension polynomial integral')
  reason=None;positive=None
  zero=next((i for i,d in enumerate(ds) if not d),None)
  neq=next((i for i,d in enumerate(ds) if d!=ds[du[i]]),None)
  if zero is not None:reason=dict(kind='zero_dimension',object=zero)
  elif neq is not None:reason=dict(kind='unequal_dual_dimensions',object=neq)
  else:
   reason=norm_failure(pD,required)
   if reason is None:reason=field_failure(f,required)
  if reason is None:
   for number,emb in enumerate(embeddings(f)):
    signs=[emb.sign(d) for d in ds]
    if not all(signs) or signs[0]!=1:continue
    if all(signs[i]*signs[j]==signs[k] for i,j,k in itertools.product(range(n),repeat=3) if R[i][j][k]):
     positive=dict(kind='galois_positive_tensor_signs',embedding=number,signs=signs);break
  bs.append(dict(factor=pc(f),dimensions=[ec(d) for d in ds],global_dimension=ec(delta),global_dimension_polynomial=pc(pD),obstruction=reason,positive_Galois_tensor_signs=positive))
 return dict(id=r['id'],tensor_sha256=r['tensor_sha256'],rank=n,commutative=comm(R),scalar_character_dimension=a['W'].cols,separating_k=a['k'],separating_polynomial=pc(a['p']),regular_Casimir_polynomial=cp,scalar_Casimir_polynomial=clp,formal_codegree_factors=[{'polynomial':pc(f),'multiplicity':e} for f,e in required],branches=bs,all_spherical_characters_reduce_to_pseudo_unitary=all(b['obstruction'] or b['positive_Galois_tensor_signs'] for b in bs))

if __name__=='__main__':
 ledger=json.loads((P/'ledger.json').read_text());ids={r['id'] for r in ledger}|{'R9_1_2','R9_1_12','R9_1_15','R9_1_17','R9_1_41','R10_1_20','R10_1_21','R10_1_39'}
 out=[];start=time.monotonic()
 for r in read():
  if r['id'] not in ids:continue
  v=analyze(r);out.append(v);(P/'original_characters.json').write_text(json.dumps(out,indent=2)+'\n')
  statuses=[b['obstruction']['kind'] if b['obstruction'] else 'Galois_FP_signs' if b['positive_Galois_tensor_signs'] else 'SURVIVES' for b in v['branches']]
  print(r['id'],statuses,'seconds',round(time.monotonic()-start,2),flush=True)
 print('DONE',len(out),'reduced',sum(r['all_spherical_characters_reduce_to_pseudo_unitary'] for r in out),'seconds',time.monotonic()-start,flush=True)
