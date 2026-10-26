from pathlib import Path
import itertools,json
import ring_checks as common,bimodule,liptrap_certificate as lip
HERE=Path(__file__).resolve().parent

def verify():
 E=list(itertools.product(range(8),range(2)));ei={g:i for i,g in enumerate(E)};SD=json.loads((HERE/'cocycle_SD16_mod16.json').read_text());D=json.loads((HERE/'original_tensors.json').read_text());out=[]
 for row in json.loads((HERE/'models.json').read_text()):
  R=row['source_tensor'];common.validate(R);sourcecheck=lip.check(R,row['liptrap_certificate']);F0,mul,du=lip.reconstruct(R,row['liptrap_certificate']);degree=[tuple(x)for x in row['source_degrees']];u=row['u'];c=row['subgroup_generator'];fix=row['subgroup_correction'];rot=row['rotation_twist'];mix=row['mixed_twist'];q=row['phase_modulus'];um=lambda g,h:((g[0]+u**g[1]*h[0])%8,g[1]^h[1])
  def omega(g,h,k):
   if u==3:return SD[ei[g]][ei[h]][ei[k]]
   a,b=g;cc,d=h;e,f=k;t=cc+(-1)**d*e;return(2*a*(-1)**b*((t-t%8)//8))%16
  def twist(g,h,k):return(fix*g[1]*h[1]*k[1]+rot*omega(g,h,k)+8*mix*(g[0]%2)*h[1]*k[1])%16
  for g,h,k,l in itertools.product(E,repeat=4):common.require((twist(h,k,l)-twist(um(g,h),k,l)+twist(g,um(h,k),l)-twist(g,h,um(k,l))+twist(g,h,k))%16==0,'group cocycle equations')
  for a,b,k in itertools.product(range(len(R)),repeat=3):
   if R[a][b][k]:common.require(um(degree[a],degree[b])==degree[k],'actual universal grading')
  F=lambda a,b,d,k:(q//16)*((F0(a,b,d,k)+twist(degree[a],degree[b],degree[d]))%16)
  M,info=bimodule.construct(R,F,c,q=q);common.require(M==row['model_tensor'],'full reconstructed model tensor');p=row['basis_map'];common.require(sorted(p)==list(range(12))and p[0]==0,'basis bijection')
  for a,b,k in itertools.product(range(12),repeat=3):common.require(D[row['id']][a][b][k]==M[p[a]][p[b]][p[k]],'every original tensor coefficient')
  out.append(dict(id=row['id'],status='pass',source=sourcecheck,cocycle_equations=65536,full_tensor_coefficients=1728,basis_map=p))
 return out
if __name__=='__main__':
 out=verify();(HERE/'verification.json').write_text(json.dumps(dict(status='pass',models=out),indent=2)+'\n');print(json.dumps(out,indent=2))
