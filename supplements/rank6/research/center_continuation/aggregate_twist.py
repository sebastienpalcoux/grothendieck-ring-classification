import json,sys,itertools
from pathlib import Path
import sympy as s
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'software'))
import modular_character_induction as I
from augmented_spectrum import AugmentedSpectrum
R=next(r for r in json.loads((ROOT/'data/census.json').read_text()) if r['id']=='R6_3_215')['N'];w=json.loads((ROOT/'systems/integral_frontier_215.json').read_text());gr=json.loads((ROOT/'research/m8_frontier/low_product_gram_certificate.json').read_text())
data,t=I.reciprocity_data(R);low=list(map(tuple,w['columns']));_,hi=I.high_columns(data,s.Matrix.hstack(*map(s.Matrix,low)));spec=AugmentedSpectrum(t,low,hi);typ=dict(zip(spec.vectors,spec.types));K=t.K;high=list(map(tuple,gr['high_restriction_types']));vecs=low+high;counts=[1]*6+gr['high_multiplicities'];D=K.to_sympy(t.D)
S=s.Matrix([[K.to_sympy(typ[v][w['labelling'][a]]*t.dims[v]/t.D) for v in vecs] for a in range(6)])
B=s.Matrix(gr['per_simple_high_coefficients']);lowprod=s.Matrix(gr['low_products']);rhs=s.Matrix([[s.expand(S[a,j]*S[b,j]/S[0,j]-sum(lowprod[p,k]*S[k,j] for k in range(6))) for j in range(9)] for p,(a,b) in enumerate(gr['pairs'])]);rhs=rhs.applyfunc(s.simplify)
H=B.inv_quick() if False else (B.T*B).inv()*B.T*rhs
H=H.applyfunc(s.simplify);assert B*H==rhs
print('high summed S rows',H)
# Multiplicity factors here multiply only low columns. theta high group already summed.
u=s.symbols('a b c'); th=[1]*6+list(u);eq=[]
for a in range(6):
 for b in range(a,6):eq.append(s.expand(sum(S[a,k]*S[b,k]*th[k] for k in range(9))-S[a,b]))
sol=s.solve(eq,u);print('group twist sums',sol)
# High C group has twist sum -multiplicity; all twists necessarily -1.
idx=2; m=counts[6+idx];assert sol[u[idx]]==-m
# The full quadratic form on the sum H_C is computed exactly using constant entries by type.
lhs=s.simplify(sum(H[idx,k]**2*(1 if k<6 else sol[u[k-6]]) for k in range(9)))
rhs=s.simplify(m*H[idx,6+idx]);print('STS aggregate',lhs,'required',rhs,'difference',s.simplify(lhs-rhs))
for p,(a,b) in enumerate(gr['pairs']):
 lhs=s.simplify(sum(lowprod[p,k]*D*S[0,k] for k in range(6))+sum(B[p,k]*D*S[0,6+k]*sol[u[k]] for k in range(3)))
 assert s.simplify(lhs-D*S[a,b])==0,(a,b,lhs,D*S[a,b])
print('all low-low balancing passed')
# n2 indicators are all1 on six input basis objects.
VV=s.Matrix.hstack(*map(s.Matrix,vecs));dd=[s.expand(D*S[0,k]) for k in range(9)]
z=s.symbols('za zb zc');eq2=[s.expand(sum(VV[i,k]*dd[k] for k in range(6))+sum(VV[i,6+k]*dd[6+k]*z[k] for k in range(3))-D) for i in range(6)]
print('n2 sums',s.solve(eq2,z))
y=s.symbols('y');for4=[4*y,sol[u[1]],4];nu4=[s.simplify((sum(VV[i,k]*dd[k] for k in range(6))+sum(VV[i,6+k]*dd[6+k]*for4[k] for k in range(3)))/D) for i in range(6)];print('nu4 if theta17 fixed',nu4)
print('lowblock eigs',S[:,:6].eigenvals())
