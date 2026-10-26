"""Concrete inflated anisotropic cocycle and C4 subgroup algebra."""
from signed_mod4 import *
import numpy as np
sys.path.insert(0,str(BASE));import group_models as gm
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'family_integral'))
from twisted_h4 import solve
from twisted_h4_matrix import construct

def make():
 vals,G=gm.matrix_group(3,True);n=len(G);inv=[next(j for j in range(n)if G[i][j]==0)for i in range(n)]
 i=next(g for g in range(1,n)if gm.order(G,g)==4);H=gm.subgroup(G,[i]);z=G[i][i]
 j=next(g for g in range(1,n)if gm.order(G,g)==4 and g not in H);Q=gm.subgroup(G,[i,j]);a=next(g for g in range(1,n)if gm.order(G,g)==3)
 order3=a;powers=[0,a,G[a][a]];qmap={}
 for x,y,c in itertools.product(range(2),repeat=3):
  v=G[G[i if x else 0][j if y else 0]][z if c else 0];qmap[v]=(x,y)
 common.require(len(qmap)==len(Q)==8,'Q8 normal subgroup')
 els={G[q][p]:(v,e)for q,v in qmap.items()for e,p in enumerate(powers)}
 common.require(len(els)==n,'semidirect quotient coordinates')
 A={v:qmap[G[G[a][q]][inv[a]]]for q,v in qmap.items()}
 def act(v,e):
  for _ in range(e%3):v=A[v]
  return v
 common.require(all(els[G[x][y]]==(tuple(u^v for u,v in zip(els[x][0],act(els[y][0],els[x][1]))),(els[x][1]+els[y][1])%3)for x,y in itertools.product(range(n),repeat=2)),'quotient semidirect law')
 def raw(v,w,u):return(v[0]*w[0]*u[0]+v[1]*w[1]*u[1]+v[0]*w[1]*u[1])%2
 def tri(v,w,u):return sum(raw(act(v,e),act(w,e),act(u,e))for e in range(3))%2
 W=np.zeros((n,n,n),dtype=np.int64)
 for x,y,u in itertools.product(range(n),repeat=3):
  v,e=els[x];w,f=els[y];q,g=els[u];W[x,y,u]=4*tri(v,act(w,e),act(q,e+f))
 GG=np.array(G);cc,dd=np.indices((n,n))
 for a,b in itertools.product(range(n),repeat=2):
  common.require(np.all((W[b,cc,dd]-W[G[a][b],cc,dd]+W[a,GG[b,cc],dd]-W[a,b,GG[cc,dd]]+W[a,b,cc])%8==0),'all actual group cocycle equations')
 vs=[(a,b)for a in H if a for b in H if b];ix={v:i for i,v in enumerate(vs)};AA=[];BB=[]
 for a,b,c in itertools.product(H,repeat=3):
  row=[0]*len(vs)
  for v,sgn in [((b,c),1),((a,G[b][c]),1),((G[a][b],c),-1),((a,b),-1)]:
   if v in ix:row[ix[v]]+=sgn
  AA.append(row);BB.append(-int(W[a,b,c]))
 sol=solve(AA,BB,first=True);common.require(bool(sol),'subgroup cochain exists');v=sol[0];P={(a,b):v[ix[a,b]]if(a,b)in ix else 0 for a,b in itertools.product(H,repeat=2)}
 return G,H,W,P,dict(Q8=Q,order4_generator=i,order3_generator=order3,quotient_coordinates=[[g,list(v),e]for g,(v,e)in els.items()])

if __name__=='__main__':
 start=time.monotonic();G,H,W,P,meta=make();w=lambda a,b,c:int(W[a,b,c]);psi=lambda a,b:P[a,b]
 R,info=construct(G,H,w,psi);print({k:v for k,v in info.items()if k!='objects'},flush=True);models=[]
 if R is not None:
  T=json.loads((BASE/'tensors.json').read_text());common.validate(R)
  for rid,S in T.items():
   if common.coarse(S)!=common.coarse(R):continue
   p=common.based_iso(S,R)
   if p is None:continue
   common.require(all(S[i][j][k]==R[p[i]][p[j]][p[k]]for i,j,k in itertools.product(range(12),repeat=3)),'full tensor match')
   models.append(dict(id=rid,name='C(SL2(3), inflated anisotropic cocycle, C4, psi)',constructor='twisted_group_theoretical_h4',parameters=dict(group_table=G,subgroup=H,cocycle_exponents=W.tolist(),phase_modulus=8,subgroup_cochain=[[a,b,v]for(a,b),v in P.items()],construction=meta),model_tensor=R,basis_map_source_to_model=p,bimodule_witness=info))
 print('matches',[r['id']for r in models],'seconds',time.monotonic()-start,flush=True)
 (Path(__file__).resolve().parent/'sl23_twist_models.json').write_text(json.dumps(dict(candidate_info={k:v for k,v in info.items()if k!='objects'},models=models),indent=2)+'\n')
