"""Exact offline certificate for R12_1_240; no numerical or bounded-search premise."""
from pathlib import Path
import itertools,json,sys
HERE=Path(__file__).resolve().parent
import ring_checks as common
import bimodule

def build():
 E=list(itertools.product(range(8),range(2)))
 def mul(g,h):return((g[0]+(-1)**g[1]*h[0])%8,(g[1]+h[1])%2)
 def omega(g,h,k):
  a,b=g;c,d=h;e,f=k;t=c+(-1)**d*e
  return (a*(-1)**b*((t-t%8)//8))%8
 cocycle_checks=0
 for g,h,k,l in itertools.product(E,repeat=4):
  common.require((omega(h,k,l)-omega(mul(g,h),k,l)+omega(g,mul(h,k),l)-omega(g,h,mul(k,l))+omega(g,h,k))%8==0,'exact normalized D16 3-cocycle');cocycle_checks+=1
 common.require(all(omega(g,h,k)==0 for g,h,k in itertools.product(E,repeat=3)if (0,0)in(g,h,k)),'normalized group cocycle')
 # Ising labels 0=1,1=psi,2=sigma.
 def ising(a,b,c):
  if a<2 and b<2:return int(c==a^b)
  if (a==2)!=(b==2):return int(c==2)
  return int(c<2)
 labs=[(a,g)for a in range(3)for g in E if int(a==2)==g[0]%2]
 R=[[[ising(a,b,c)*int(mul(g,h)==k)for c,k in labs]for b,h in labs]for a,g in labs]
 common.validate(R)
 def F(a,b,c,k):
  aa,bb,cc,kk=[labs[x][0]for x in (a,b,c,k)];v=omega(labs[a][1],labs[b][1],labs[c][1])
  if aa==cc==2 and bb!=2:return(v+4*bb*kk)%8
  if aa!=2 and bb==2 and cc!=2:return(v+4*aa*cc)%8
  common.require(not(aa==bb==cc==2),'no triple-odd F block in subgroup bimodule operations')
  return v
 gen=labs.index((0,(0,1)));M,info=bimodule.construct(R,F,gen,q=8)
 source=json.loads((HERE/'census_R240.json').read_text());p=common.based_iso(source,M)
 common.require(p is not None,'full source-to-model based ring isomorphism')
 checks=0
 for a,b,c in itertools.product(range(12),repeat=3):
  common.require(source[a][b][c]==M[p[a]][p[b]][p[c]],'every structure constant');checks+=1
 return dict(id='R12_1_240',status='modeled',constructor='C2_Morita_dual_of_Ising_D16_twisted_graded_pullback',parameters=dict(group='D16',group_order=16,grading='rotation exponent modulo 2',group_cocycle_modulus=8,group_cocycle_formula='a*(-1)^b*(c+(-1)^d*e-[c+(-1)^d*e]_8)/8 modulo 8',algebra_generator=[0,[0,1]]),basis_map_source_to_model=p,model_tensor=M,source_tensor=R,source_labels=labs,bimodules=info['objects'],checks=dict(group_cocycle_equations=cocycle_checks,full_tensor_coefficients=checks,associativity='common.validate for source and model',independent_audit='../independent/audit_ising_dual.py'))
if __name__=='__main__':
 result=build();(HERE/'r240_certificate.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(id=result['id'],checks=result['checks'],basis_map=result['basis_map_source_to_model'])))
