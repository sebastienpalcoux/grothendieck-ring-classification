from graph_twist import *
import scalar_base

def second_cocycle(G,H):
 Q=np.array([[G[2*a][2*b]//2 for b in range(60)]for a in range(60)],dtype=int);inv=[next(j for j in range(60)if Q[i,j]==0)for i in range(60)]
 invol=[a for a in range(1,60)if Q[a,a]==0];a=invol[0];b=next(b for b in invol if b!=a and Q[a,b]==Q[b,a]);P=[0,a,b,int(Q[a,b])];coord={x:(i%2,i//2)for i,x in enumerate(P)}
 reps=[];cos={}
 for r in range(60):
  if r in cos:continue
  j=len(reps);reps.append(r)
  for h in P:cos[int(Q[h,r])]=j
 monomial.require(len(reps)==15,'index15 SylowV4')
 nxt=np.array([[cos[int(Q[r,g])]for g in range(60)]for r in reps],dtype=int)
 hh=np.array([[coord[int(Q[Q[r,g],inv[reps[nxt[i,g]]]])]for g in range(60)]for i,r in enumerate(reps)],dtype=int)
 W=np.zeros((60,60,60),dtype=np.int64)
 for i in range(15):
  for g in range(60):
   x=hh[i,g];j=nxt[i,g]
   for h in range(60):
    y=hh[j,h];k=nxt[j,h];z=hh[k]
    W[g,h]+=(x[0]*y[0]*z[:,0]+x[1]*y[1]*z[:,1]+x[0]*y[1]*z[:,1])
 W%=2
 for a in range(60):
  # coboundary at(a,b,c,d), withaxes b,c,d
  b=np.arange(60)[:,None,None];c=np.arange(60)[None,:,None];d=np.arange(60)[None,None,:]
  v=W[b,c,d]-W[Q[a,b],c,d]+W[a,Q[b,c],d]-W[a,b,Q[c,d]]+W[a,b,c]
  monomial.require(not np.any(v%2),'all12960000 transferred3cocycle equations')
 D=[h//2 for h in H];sgn={h//2:h%2 for h in H};variables=[(a,b)for a,b in itertools.product(D,repeat=2)if a and b];ix={v:i for i,v in enumerate(variables)};mat=[];rhs=[]
 for a,b,c in itertools.product(D,repeat=3):
  row=[0]*len(variables)
  for v in [(b,c),(int(Q[a,b]),c),(a,int(Q[b,c])),(a,b)]:
   if 0 not in v:row[ix[v]]^=1
  mat.append(row);rhs.append(int(W[a,b,c])^sgn[a]*sgn[b]*sgn[c])
 sol=scalar_base.solve(mat,rhs,mod=2,first=True);monomial.require(len(sol)==1,'relative gauge exists')
 beta=np.zeros((60,60),dtype=int)
 for v,t in zip(variables,sol[0]):beta[v]=t
 for a,b,c in itertools.product(range(60),repeat=3):W[a,b,c]=(W[a,b,c]+beta[b,c]+beta[Q[a,b],c]+beta[a,Q[b,c]]+beta[a,b])%2
 for a,b,c in itertools.product(D,repeat=3):monomial.require(W[a,b,c]==sgn[a]*sgn[b]*sgn[c],'adapted3cocycle onD10')
 return W,dict(sylow=P,coset_representatives=reps,gauge=beta.tolist(),base_cocycle='x0*y0*z0+x1*y1*z1+x0*y1*z1 mod2')

def main():
 start=time.monotonic();G,H,lam=candidate();W,cert=second_cocycle(G,H);data=json.load(open(BASE/'source_tensors.json'));out=[]
 for a,b in [(0,0),(0,1),(1,0),(1,1)]:
  w=lambda x,y,z:10*((a*(int(W[x//2,y//2,z//2])+(x%2)*(y%2)*(z%2))+b*(lam[x//2][y//2]+(x%2)*(y%2))*(z%2))%2)
  R,info=monomial.construct(G,H,w);hits=[]
  if R is not None:
   gt.common.validate(R)
   for rid,S in data.items():
    if gt.common.coarse(S)!=gt.common.coarse(R):continue
    p=gt.common.based_iso(S,R)
    if p is not None:
     monomial.require(all(S[i][j][k]==R[p[i]][p[j]][p[k]]for i,j,k in itertools.product(range(12),repeat=3)),'1728exact tensor identification')
     hits.append(dict(id=rid,basis_map_source_to_model=p,tensor_sha256=gt.common.sha(S)))
  result=dict(parameters=[a,b],group_table=G,subgroup=H,schur_cocycle=lam,transfer_cocycle=W.tolist(),transfer_certificate=cert,model_tensor=R,info=info,matches=hits,seconds=time.monotonic()-start)
  out.append(result);(ROOT/'all_graph_twists.json').write_text(json.dumps(out,separators=(',',':'))+'\n');print('PAR',a,b,'matches',hits,'info',{k:v for k,v in info.items()if k!='objects'},'seconds',time.monotonic()-start,flush=True)
if __name__=='__main__':main()
