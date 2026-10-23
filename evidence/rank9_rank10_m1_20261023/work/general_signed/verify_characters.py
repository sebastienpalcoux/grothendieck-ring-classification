"""Independent exact check of complete scalar-character inventories.

Does not call the character-discovery or character-restriction routines.
Checks homomorphisms directly, completeness by the commutator-kernel dimension,
and each scalar/Casimir/norm/field/sign identity from supplied exact coordinates.
"""
import collections,json,itertools
import sympy as s
from oriented import P,read,require,parity
from branches import signed_tensor
from exact import t,poly,field,pc,vector,check_norm,check_field,embeddings

def commutator_kernel_dimension(N):
 n=len(N)
 C=[N[i]*N[j]-N[j]*N[i] for i in range(n) for j in range(i)]
 return n-s.Matrix.vstack(*C).rank()

def character_inventory(T,record):
 n=len(T);N=list(map(s.Matrix,T));du=[next(j for j in range(n) if T[i][j][0]) for i in range(n)];m=commutator_kernel_dimension(N)
 require(m==record['scalar_character_dimension'],'scalar character dimension')
 polys=[];data=[]
 for b in record['branches']:
  f=poly(b['factor']);require(f.is_irreducible and f.LC()==1,'irreducible scalar field');require(pc(f) not in polys,'distinct scalar components');polys.append(pc(f));K=field(f)
  ds=[K([s.Rational(x) for x in co]) for co in b['dimensions']];require(len(ds)==n and ds[0]==K.one,'normalized dimensions')
  for i,j in itertools.product(range(n),repeat=2):
   require(ds[i]*ds[j]==sum((T[i][j][k]*ds[k] for k in range(n)),K.zero),'exact dimension homomorphism')
  u=K(s.Poly(t,t).rem(f).all_coeffs());h=K.one+sum((record['separating_k']**(i-1)*ds[i] for i in range(1,n)),K.zero)
  require(h==u,'separating generator equals field generator')
  D=sum((ds[i]*ds[du[i]] for i in range(n)),K.zero);require(D==K([s.Rational(x) for x in b['global_dimension']]),'global dimension')
  pD=s.Matrix.hstack(*(vector(D*u**i,f.degree()) for i in range(f.degree()))).charpoly(t).as_poly().sqf_part().monic()
  if 'global_dimension_polynomial' in b:require(pc(pD)==b['global_dimension_polynomial'],'minimal dimension polynomial')
  data.append((b,f,K,ds,D,pD))
 require(sum(poly(c).degree() for c in polys)==m,'all scalar characters exhausted')
 sep=s.prod(poly(c).as_expr() for c in polys);require(pc(s.Poly(sep,t))==record['separating_polynomial'],'separating polynomial')
 return N,du,data

def verify_original(R,record):
 N,du,data=character_inventory(R,record);n=len(R);C=sum((N[i]*N[du[i]] for i in range(n)),s.zeros(n));cp=C.charpoly(t).as_poly();qlin=s.Poly(1,t)
 for b,f,K,ds,D,pD in data:
  require(f.degree()%pD.degree()==0,'dimension extension degree');qlin*=pD**(f.degree()//pD.degree())
 require(pc(cp)==record['regular_Casimir_polynomial'] and pc(qlin)==record['scalar_Casimir_polynomial'],'Casimir receipt')
 required=qlin.factor_list()[1];quotient,rem=cp.div(qlin);require(rem.is_zero,'scalar Casimir divides');deficit=n-record['scalar_character_dimension']
 if deficit:
  require(deficit in [4,8,9],'exhaustive Wedderburn partition');d=3 if deficit==9 else 2
  for q,e in quotient.factor_list()[1]:
   require(e%(d*d)==0,'matrix block multiplicity');v=s.Poly(q.as_expr().subs(t,d*t)/d**q.degree(),t,domain=s.QQ);required.append((v,e//(d*d)))
 require([{'polynomial':pc(f),'multiplicity':e} for f,e in required]==record['formal_codegree_factors'],'actual formal codegrees')
 for b,f,K,ds,D,pD in data:
  why=b['obstruction']
  if why:
   kind=why['kind']
   if kind=='zero_dimension':require(not ds[why['object']],'zero dimension')
   elif kind=='unequal_dual_dimensions':require(ds[why['object']]!=ds[du[why['object']]],'dual dimension mismatch')
   elif kind=='norm':check_norm(pD,required,why)
   elif kind.startswith('field_'):check_field(f,required,why)
   else:raise ValueError(kind)
  if b['positive_Galois_tensor_signs']:
   w=b['positive_Galois_tensor_signs'];e=embeddings(f)[w['embedding']];signs=[e.sign(d) for d in ds]
   require(signs==w['signs'] and all(signs) and signs[0]==1,'exact embedding signs')
   require(all(signs[i]*signs[j]==signs[k] for i,j,k in itertools.product(range(n),repeat=3) if R[i][j][k]),'tensor sign character')
 require(record['all_spherical_characters_reduce_to_pseudo_unitary']==all(b['obstruction'] or b['positive_Galois_tensor_signs'] for b in record['branches']),'reduction outcome')
 return True

def verify_signed(R,T,record):
 if record.get('reason')=='no_scalar_characters':
  require(commutator_kernel_dimension(list(map(s.Matrix,T)))==0,'no scalar characters');return True
 N,du,data=character_inventory(T,record);required=[]
 for U in (R,T):
  M=list(map(s.Matrix,U));required+=sum((M[i]*M[du[i]] for i in range(len(U))),s.zeros(len(U))).charpoly(t).as_poly().factor_list()[1]
 required=[(q.set_domain(s.QQ),m) for q,m in required]
 for b,f,K,ds,D,pD in data:
  why=b['obstruction'];require(why is not None,'signed character excluded');kind=why['kind']
  if kind=='zero_dimension':require(not ds[why['object']],'zero signed dimension')
  elif kind=='unequal_dual_dimensions':require(ds[why['object']]!=ds[du[why['object']]],'signed dual dimensions')
  elif kind.startswith('field_'):check_field(f,required,why)
  else:raise ValueError(kind)
 return True

if __name__=='__main__':
 rows={r['id']:r for r in read()};records=json.loads((P/'original_characters.json').read_text())
 for i,r in enumerate(records,1):
  require(rows[r['id']]['tensor_sha256']==r['tensor_sha256'],'source identity');verify_original(rows[r['id']]['tensor'],r)
  if i%10==0:print('PASS original',i,flush=True)
 count=0
 for rec in json.loads((P/'ledger.json').read_text()):
  R=rows[rec['id']]['tensor'];du=[next(j for j in range(len(R)) if R[i][j][0]) for i in range(len(R))];mapping={}
  for j,orb in enumerate(rec['oriented_orbits']):
   for i,k,l in orb:mapping[i,k,du[l]]=j
  for b in rec['branches']:
   if b['outcome']=='excluded_dimension_characters':
    T=signed_tensor(R,{'mapping':mapping},b['sign_assignment']);print('VERIFY signed',rec['id'],b['free_bits'],flush=True);verify_signed(R,T,b['dimension_test']);count+=1
 print('PASS independent original character records',len(records),'and alternate signed quotient records',count,flush=True)
