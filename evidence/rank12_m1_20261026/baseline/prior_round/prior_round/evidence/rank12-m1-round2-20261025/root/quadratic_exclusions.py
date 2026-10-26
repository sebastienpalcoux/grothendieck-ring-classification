"""Short accepted proof certificates for the four quadratic-C2 cases."""
from characters import characters,exact,t,s
from signed_enumerate import enumerate_kernel
from signed_mod4 import BASE,common
from pathlib import Path
from sympy.matrices.normalforms import hermite_normal_form
import json,math

def certificate(R):
 signed=enumerate_kernel(R,True)
 common.require(signed['all_gauge_original'],'spherical descent not established')
 cc=characters(R);C=sum((s.Matrix(A)*s.Matrix(A).T for A in R),s.zeros(len(R)));p=C.charpoly(t).as_poly();q=s.Poly(t*t-720*t+2592,t)
 common.require(p.rem(q).is_zero and q.is_irreducible,'quadratic Casimir factor')
 g=s.Poly(t-36,t)
 common.require(p.rem(g).is_zero and not p.rem(g*g).is_zero,'unique codegree36')
 branches=[]
 for row in cc['characters']:
  f=exact.poly(row['field_polynomial']);K=exact.field(f);ds=[K(list(map(s.Rational,v)))for v in row['dimensions']];D=K(list(map(s.Rational,row['global_dimension'])))
  if row['zero_objects']:why=dict(kind='zero_dimension',object=row['zero_objects'][0])
  elif row['unequal_duals']:why=dict(kind='unequal_dual_dimensions',object=row['unequal_duals'][0])
  elif f.degree()%2:why=dict(kind='codegree_field_degree',required_casimir_factor=exact.pc(q),character_field_degree=f.degree())
  else:
   degree=f.degree();V=s.Matrix.hstack(*(exact.vector(d,degree)for d in ds));den=math.lcm(*(int(x.q)for x in V));H=hermite_normal_form((V*den).applyfunc(int));common.require(H.shape==(degree,degree),'full dimension order')
   value=H.inv()*exact.vector(D/K(36),degree)*den
   common.require(any(x.q!=1 for x in value),'central dimension lies in order')
   why=dict(kind='central_dimension_order',codegree=36,regular_multiplicity=1,dimension=exact.ec(D/K(36)),lattice_denominator=den,hermite_basis=[[str(v)for v in r]for r in H.tolist()],order_coordinates=list(map(str,value)))
  branches.append(dict(character=row,obstruction=why))
 return dict(tensor_sha256=common.sha(R),signed_descent=signed,one_dimensional_character_count=cc['one_dimensional_count'],character_generator=cc['separating_k'],spherical_character_branches=branches,scope='arbitrary_complex_fusion_category')

if __name__=='__main__':
 T=json.loads((BASE/'tensors.json').read_text());out=[]
 for i in (63,64,215,365):
  rid=f'R12_1_{i}';z=certificate(T[rid]);z.update(id=rid,status='excluded',criterion='mod4_signed_descent_and_dimension_order');out.append(z);print(rid,'PASS',z['signed_descent']['associative_count'],'signed tables',len(z['spherical_character_branches']),'character orbits')
 (Path(__file__).resolve().parent/'quadratic_exclusions.json').write_text(json.dumps(out,indent=2)+'\n')
