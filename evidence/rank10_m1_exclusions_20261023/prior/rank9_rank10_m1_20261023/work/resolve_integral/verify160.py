from fuse_mod4_exact import *
import hashlib
OUT=Path(__file__).parent

def require(condition,explanation):
 if not condition:raise ValueError(explanation)

def verify_action(r):
 W=r['omega'];J=r['J'];q=r['q'];els=range(16)
 require(all(W[0][x][y]==W[x][0][y]==W[x][y][0]==0 and J[0][x]==J[x][0]==q[0]==0 for x,y in itertools.product(els,repeat=2)),'normalization')
 require(all((W[y][z][t]-W[x^y][z][t]+W[x][y^z][t]-W[x][y][z^t]+W[x][y][z])%2==0 for x,y,z,t in itertools.product(els,repeat=4)),'pentagon')
 aa=[act((1,0),x) for x in els];bb=[act((0,1),x) for x in els]
 require(all(W[aa[x]][aa[y]][aa[z]]==W[x][y][z] for x,y,z in itertools.product(els,repeat=3)),'C5 invariant associator')
 require(all(J[aa[x]][aa[y]]==J[x][y] for x,y in itertools.product(els,repeat=2)),'C5 invariant tensorator')
 require(all((J[y][z]-J[x^y][z]+J[x][y^z]-J[x][y]-2*(W[x][y][z]-W[bb[x]][bb[y]][bb[z]]))%4==0 for x,y,z in itertools.product(els,repeat=3)),'monoidal involution')
 require(all((J[x][y]+J[bb[x]][bb[y]]-q[x]-q[y]+q[x^y])%4==0 for x,y in itertools.product(els,repeat=2)),'monoidal square identification')
 require(all(q[act(h,x)]==q[x] for h in H for x in els),'action square coherence')
 # Full D10 monoidality and associativity of the compositor.
 for h,k in itertools.product(H,repeat=2):
  require(all((h[1]*J[act(k,x)][act(k,y)]+k[1]*J[x][y]-hm(h,k)[1]*J[x][y]-h[1]*k[1]*(q[x]+q[y]-q[x^y]))%4==0 for x,y in itertools.product(els,repeat=2)),'full compositor monoidality')
 for h,k,l in itertools.product(H,repeat=3):
  require(all((h[1]*k[1]*q[act(l,x)]+hm(h,k)[1]*l[1]*q[x]-k[1]*l[1]*q[x]-h[1]*hm(k,l)[1]*q[x])%4==0 for x in els),'full action pentagon')
 fixed=[x for x in els if bb[x]==x]
 return {'normalized':True,'associator_pentagons':16**4,'monoidal_functor_equations':16**3,'group_action_coherence':True,'fixed_subspace':fixed,'J_symmetric_on_fixed_subspace':all(J[x][y]==J[y][x] for x,y in itertools.product(fixed,repeat=2)),'diagonal_orbit_values':[W[u][u][u] for u in [1,2,4]]}

if __name__=='__main__':
 import sys
 sys.path.insert(0,str(ROOT/'work/models'))
 from match_models import based_iso
 data=json.load(open(OUT/'mod4_model_candidates.json'));T=json.load(open(ROOT/'work/input_audit/tensors.json'));models=[];normalforms=[]
 for mask in[0,16,32,48]:
  r=next(r for r in data if r['omega_basis_mask']==mask);audit=verify_action(r);normalforms.append({'omega_basis_mask':mask,'omega':r['omega'],'J':r['J'],'q':r['q'],'audit':audit})
  print('NORMAL FORM',mask,audit,flush=True)
 for ident,mask in[('R10_1_39',0),('R10_1_138',16)]:
  r=next(r for r in data if r['omega_basis_mask']==mask and any(m['id']==ident for m in r['matches']));N,labs=fuse_action(r['J'],r['q']);p=based_iso(T[ident],N);require(p is not None,'full exact tensor matching')
  require(all(T[ident][i][j][k]==N[p[i]][p[j]][p[k]] for i,j,k in itertools.product(range(10),repeat=3)),'coefficient match')
  models.append({'id':ident,'status':'unitarily_realized','model':'D10-equivariantization of Vec(F16_add)^omega','omega_basis_mask':mask,'omega':r['omega'],'J':r['J'],'q':r['q'],'tensor_sha256':tensor_hash(T[ident]),'input_tensor':T[ident],'model_tensor':N,'basis_map_source_to_model':p,'labels':labs,'coherence_audit':verify_action(r)})
  print('EXACT MODEL',ident,p,flush=True)
 (OUT/'verified_models160.json').write_text(json.dumps(models,indent=2)+'\n');(OUT/'normal_forms160.json').write_text(json.dumps(normalforms,indent=2)+'\n')
