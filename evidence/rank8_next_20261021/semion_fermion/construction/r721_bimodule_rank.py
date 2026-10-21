"""Complete free-bimodule Gram and canonical-center rank constraints.

The known algebra A=1+rho is in the C2 de-equivariantization of GH(C8).
Actual algebra existence and the conjugation argument are proved separately.
No modular-data permutation is promoted to a braided autoequivalence.
"""
from pathlib import Path
from itertools import product,combinations_with_replacement
from fractions import Fraction as F
import hashlib,json,math
import sympy as s
HERE=Path(__file__).resolve().parent;NEXT=HERE.parents[1];ROOT=NEXT.parents[1]
def need(ok,msg):
 if not ok:raise ValueError(msg)
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 R=[[[0]*8 for _ in range(8)]for _ in range(8)]
 for i,j in product(range(8),repeat=2):
  if i<4 and j<4:R[i][j][(i+j)%4]=1
  elif i<4:R[i][j][4+(i+j-4)%4]=1
  elif j<4:R[i][j][4+(i-4-j)%4]=1
  else:
   R[i][j][(i-j)%4]=1
   for k in range(4,8):R[i][j][k]=2
 for i,j,k,l in product(range(8),repeat=4):need(sum(R[i][j][t]*R[t][k][l] for t in range(8))==sum(R[j][k][t]*R[i][t][l] for t in range(8)),'source associativity')
 a=[1,0,0,0,1,0,0,0]
 K=s.Matrix(8,8,lambda i,j:sum(R[p][j][t]*R[t][q][i] for p in (0,4) for q in (0,4) for t in range(8)))
 G=K-s.Matrix(a)*s.Matrix([a]);piv=list(G.rref()[1]);H=G.extract(piv,piv);Hi=H.inv();L=Hi*G[piv,:]
 need(G==G[:,piv]*Hi*G[piv,:] and all(H[:i,:i].det()>0 for i in range(1,len(piv)+1)),'positive residual Gram')
 rows=[];box=[math.isqrt(int(G[i,i])) for i in piv]
 for ns in product(*(range(b+1) for b in box)):
  v=s.Matrix(1,len(piv),ns)
  if not any(ns) or (v*Hi*v.T)[0]>1:continue
  row=v*L
  if all(z.q==1 and z>=0 and z*z<=G[i,i] for i,z in enumerate(row)):rows.append(tuple(int(z) for z in row))
 rows.sort();need(len(rows)==7,'complete seven row types')
 bounds=[min(int(G[i,i])//v[i]**2 for i in range(8) if v[i]) for v in rows]
 pairs=list(combinations_with_replacement(range(8),2));eq=[[v[i]*v[j] for v in rows] for i,j in pairs];rhs=[int(G[i,j]) for i,j in pairs]
 factors=[];tested=0
 for ns in product(*(range(b+1) for b in bounds)):
  tested+=1
  if all(sum(n*c for n,c in zip(ns,row))==b for row,b in zip(eq,rhs)):factors.append(list(ns))
 need(len(factors)==4,'complete four factors')
 delta=4+s.sqrt(17);rowdims=[s.radsimp((sum(v[:4])+delta*sum(v[4:]))/(1+delta)) for v in rows]
 records=[]
 for ns in factors:
  B=[a]+[list(v) for v,n in zip(rows,ns) for _ in range(n)];dims=[s.Integer(1)]+[d for d,n in zip(rowdims,ns) for _ in range(n)]
  need(s.simplify(sum(d*d for d in dims)-(4+4*delta**2))==0,'Morita dimension')
  records.append({'rank':len(B),'multiplicities':ns,'forgetful_rows':B,'simple_dimensions':[str(d) for d in dims],'invertibles':sum(d==1 for d in dims)})
 # Known-center comparison binds the GI label set to all exact S/T entries.
 identpath=NEXT/'models/r721_gi_identification.json';sourcepath=NEXT/'r721/modular_completions.json'
 ident=read(identpath);need(ident['all_match'] and ident['source_sha256']==sha(sourcepath),'known-center comparison binding')
 center=read(sourcepath)[0];mapping=ident['candidate_to_GI_permutation'];inv={j:i for i,j in enumerate(mapping)}
 allowed=[0,1,6,7,10,12];need(sorted(mapping[i] for i,t in enumerate(center['T_exponents_mod_136']) if t==0)==allowed,'complete twist-one support')
 # Rows gamma, unit and k22 give p=1, x+y+2z+2w=6,
 # and3(x+y)-2(z+w)=2. Hence x+y=z+w=2.
 variables=s.symbols('p x y z w');p,x,y,z,w=variables
 affine=s.linsolve([p-1,x+y+2*z+2*w-6,3*x+3*y-2*z-2*w-2],variables)
 need(affine==s.FiniteSet((1,2-y,y,2-w,w)),'complete affine fixed-vector system')
 lagrangians=[]
 S=[[[F(t) for t in c]+[F(0)]*(16-len(c)) for c in row] for row in center['S_coefficients_ascending']]
 for xx,zz in product(range(3),repeat=2):
  gi={0:1,1:1,6:xx,7:2-xx,10:zz,12:2-zz};v=[gi.get(mapping[i],0) for i in range(22)]
  for i,row in enumerate(S):
   got=[sum(v[j]*row[j][k] for j in range(22)) for k in range(16)]
   need(got==[F(v[i])]+[F(0)]*15,'full exact S-fixed Lagrangian vector')
  lagrangians.append({'GI_coefficients':[gi[j] for j in allowed],'rank':sum(n*n for n in v)})
 ranks=sorted({v['rank'] for v in lagrangians});need(ranks==[6,8,10],'known-center rank set')
 for r in records:r['passes_known_center_rank']=r['rank'] in ranks
 files=[identpath,sourcepath]
 result={'kind':'actual_Qsystem_dual_rank_constraints','source_fusion_tensor':R,'source_basis':['g0','g1','g2','g3','rho0','rho1','rho2','rho3'],'algebra_object':a,'free_bimodule_Gram':K.tolist(),'residual_Gram':G.tolist(),'row_pivots':piv,'pivot_box_count':math.prod(n+1 for n in box),'complete_row_types':[list(v) for v in rows],'row_dimensions':[str(d) for d in rowdims],'multiplicity_bounds':bounds,'complete_multiplicity_box_count':tested,'factors':records,'GI_twist_one_support':[ident['GI_labels'][i] for i in allowed],'complete_Lagrangian_fixed_vectors':lagrangians,'known_center_possible_ranks':ranks,'remaining_dual_ranks':[r['rank'] for r in records if r['passes_known_center_rank']],'source_sha256':{str(p.relative_to(ROOT)):sha(p) for p in files},'verifier_sha256':sha(Path(__file__)),'scope':'Exact necessary rank constraints for the actual known A-bimodule category. Excluding rank6 additionally uses the explicit Q-system vertex argument in PROOF.md; identifying the full rank8 fusion tensor is separate.'}
 print(json.dumps(result,indent=2,default=int))
if __name__=='__main__':main()
