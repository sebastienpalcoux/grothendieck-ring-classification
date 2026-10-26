"""Exact offline certificate for R12_1_408; no numerical or bounded-search premise."""
from pathlib import Path
import itertools,json,sys
HERE=Path(__file__).resolve().parent
import ring_checks as common
import bimodule

def build():
 E=list(itertools.product(range(8),range(2)))
 def mul(g,h):return((g[0]+3**g[1]*h[0])%8,(g[1]+h[1])%2)
 omega_table=json.loads((HERE/'cocycle_SD16_mod16.json').read_text());index={g:j for j,g in enumerate(E)}
 def omega(g,h,k):return omega_table[index[g]][index[h]][index[k]]
 cocycle_checks=0
 for g,h,k,l in itertools.product(E,repeat=4):
  common.require((omega(h,k,l)-omega(mul(g,h),k,l)+omega(g,mul(h,k),l)-omega(g,h,mul(k,l))+omega(g,h,k))%16==0,'exact normalized SD16 3-cocycle');cocycle_checks+=1
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
  if aa==cc==2 and bb!=2:return(v+8*bb*kk)%16
  if aa!=2 and bb==2 and cc!=2:return(v+8*aa*cc)%16
  common.require(not(aa==bb==cc==2),'no triple-odd F block in subgroup bimodule operations')
  return v
 gen=labs.index((0,(0,1)));M,info=bimodule.construct(R,F,gen,q=16)
 source=json.loads((HERE/'census_R408.json').read_text());p=common.based_iso(source,M)
 common.require(p is not None,'full source-to-model based ring isomorphism')
 checks=0
 for a,b,c in itertools.product(range(12),repeat=3):
  common.require(source[a][b][c]==M[p[a]][p[b]][p[c]],'every structure constant');checks+=1
 return dict(id='R12_1_408',status='modeled',constructor='C2_Morita_dual_of_Ising_SD16_twisted_graded_pullback',parameters=dict(group='SD16',group_order=16,grading='rotation exponent modulo 2',group_cocycle_modulus=16,group_cocycle_table='cocycle_SD16_mod16.json',algebra_generator=[0,[0,1]]),basis_map_source_to_model=p,model_tensor=M,source_tensor=R,source_labels=labs,bimodules=info['objects'],checks=dict(group_cocycle_equations=cocycle_checks,full_tensor_coefficients=checks,associativity='common.validate for source and model',independent_audit='../independent/audit_ising_dual.py'))
if __name__=='__main__':
 result=build();(HERE/'r408_certificate.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(id=result['id'],checks=result['checks'],basis_map=result['basis_map_source_to_model'])))
