"""Exact twisted group-theoretical tensor construction, rank-eleven candidates.
All cyclotomic coefficients are integer polynomials modulo Phi_16=x^8+1.
"""
from pathlib import Path
import sys,itertools,json,numpy as np
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'work/rank11'))
from common import read,based_iso,sha,validate,require,dump
OUT=Path(__file__).parent
MOD=16

def scalar(G,H,alpha):
 gens=[];cl={0}
 for a in H:
  if a in cl:continue
  gens.append(a)
  while True:
   nc=cl|{G[b][a]for b in cl for a in gens}
   if nc==cl:break
   cl=nc
 for vs in itertools.product(range(MOD),repeat=len(gens)):
  d={0:0};queue=[0];ok=True
  for a in queue:
   for g,v in zip(gens,vs):
    b=G[a][g];e=(d[a]+v-alpha[a,g])%MOD
    if b in d:
     if d[b]!=e:ok=False;break
    else:d[b]=e;queue.append(b)
   if not ok:break
  if ok and all((d[a]+d[b]-d[G[a][b]]-alpha[a,b])%MOD==0 for a,b in itertools.product(H,repeat=2)):return d
 raise ValueError('nontrivial projective class')

def linear_chars(G,H):
 return [d for d in _linear(G,H)]
def _linear(G,H):
 gens=[];cl={0}
 for a in H:
  if a in cl:continue
  gens.append(a)
  while True:
   nc=cl|{G[b][a]for b in cl for a in gens}
   if nc==cl:break
   cl=nc
 for vs in itertools.product(range(MOD),repeat=len(gens)):
  d={0:0};queue=[0];ok=True
  for a in queue:
   for g,v in zip(gens,vs):
    b=G[a][g];e=(d[a]+v)%MOD
    if b in d:
     if d[b]!=e:ok=False;break
    else:d[b]=e;queue.append(b)
   if not ok:break
  if ok:yield d

def representations(G,K,alpha):
 try:
  lam=scalar(G,K,alpha)
  chars=[{a:{e:1}for a,e in d.items()}for d in linear_chars(G,K)]
  if len(chars)<len(K):
   require(len(K)==8 and len(chars)==4,'unsupported ordinary character group')
   z=next(a for a in K if a!=0 and all(G[a][b]==G[b][a]for b in K))
   chars.append({a:{0:2}if a==0 else{MOD//2:2}if a==z else{}for a in K})
  return [(lam,c)for c in chars]
 except ValueError:pass
 if len(K)==4 and all(G[a][b]==G[b][a] for a,b in itertools.product(K,repeat=2)):
  require(any((alpha[a,b]-alpha[b,a])%MOD for a,b in itertools.product(K,repeat=2)), 'abelian projective class requires higher roots')
  return [({a:0 for a in K},{a:{0:2} if a==0 else {} for a in K})]
 require(len(K)==8,'unsupported projective stabilizer')
 r=next(a for a in K if G[a][a]!=0);rr=[0,r,G[r][r],G[G[r][r]][r]];s=next(a for a in K if a not in rr and G[a][a]==0)
 co={rr[i]:(i,0)for i in range(4)};co.update({G[rr[i]][s]:(i,1)for i in range(4)})
 st={}
 for a,b in itertools.product(K,repeat=2):
  i,e=co[a];j,f=co[b];v=i+(-1)**e*j
  require(co[G[a][b]]==(v%4,(e+f)%2),'D8 coordinates')
  st[a,b]=(MOD//2)*(v//4)%MOD
 lam=scalar(G,K,{ab:(alpha[ab]-st[ab])%MOD for ab in st})
 cs=[]
 for k in[1,3]:
  chi={}
  for a,(i,e)in co.items():
   p={}
   if e==0:
    for exp in[(MOD//8)*k*i%MOD,-(MOD//8)*k*i%MOD]:p[exp]=p.get(exp,0)+1
   chi[a]=p
  cs.append((lam,chi))
 return cs

def fusion(G,H,W,psi):
 n=len(G);inv=[r.index(0)for r in G];H=sorted(H);hs=set(H);GT=np.array(G);nn=np.arange(n)
 for a in range(n):require(not np.any((W-W[GT[a],:,:]+W[a,GT[:,:,None],nn[None,None,:]]-W[a,nn[:,None,None],GT[None,:,:]]+W[a,:,:,None])%MOD),'3-cocycle')
 w=lambda a,b,c:int(W[a,b,c])
 require(all((psi[a,b]+psi[G[a][b],c]-w(a,b,c)-psi[b,c]-psi[a,G[b][c]])%MOD==0 for a,b,c in itertools.product(H,repeat=3)),'algebra cochain')
 def kappa(a,b,c,d,x):
  xd=G[x][inv[d]];xdb=G[xd][inv[b]]
  return(w(c,xd,inv[b])-w(a,c,xdb)+w(x,inv[d],inv[b])+psi[a,c]+psi[inv[d],inv[b]])%MOD
 objs=[];seen=set()
 for z in range(n):
  if z in seen:continue
  orb={G[G[u][z]][inv[v]]:(u,v)for u,v in itertools.product(H,repeat=2)};seen|=set(orb)
  K=[a for a in H if G[G[inv[z]][a]][z]in hs];conj={a:G[G[inv[z]][a]][z]for a in K}
  al={(a,b):kappa(a,conj[a],b,conj[b],z)for a,b in itertools.product(K,repeat=2)}
  for lam,chi in representations(G,K,al):objs.append((z,K,conj,lam,chi,orb))
 cos=[];seen=set()
 for x in range(n):
  if x in seen:continue
  cos.append(x);seen|={G[x][h]for h in H}
 cache={}
 def val(i,x,a,b):
  key=i,x,a,b
  if key in cache:return cache[key]
  z,K,conj,lam,chi,orb=objs[i]
  if x not in orb or G[a][x]!=G[x][b]:return(0,{})
  u,v=orb[x];k=G[G[inv[u]][a]][u];l=G[G[inv[v]][b]][v]
  require(l==conj[k],'stabilizer conjugation')
  e=(kappa(a,b,u,v,z)-kappa(u,v,k,l,z)+lam[k])%MOD
  cache[key]=(e,chi[k]);return cache[key]
 r=len(objs);T=[[[0]*r for _ in range(r)]for _ in range(r)]
 for k,(z,K,conj,lam,chi,orb)in enumerate(objs):
  for i,j in itertools.product(range(r),repeat=2):
   coeff=[0]*MOD
   for a in K:
    if not chi[a]:continue
    b=conj[a]
    for x in cos:
     h=G[G[inv[x]][a]][x]
     if h not in hs:continue
     y=G[inv[x]][z];yb=G[y][inv[b]];hy=G[inv[h]][y]
     require(yb==hy,'balanced pair')
     extra=w(x,y,inv[b])-w(a,x,yb)+w(x,h,hy)-w(x,h,inv[h])-psi[h,inv[h]]+w(a,x,inv[h])
     ea,va=val(i,x,a,h);eb,vb=val(j,y,h,b)
     for ec,vc in chi[a].items():
      for eaa,caa in va.items():
       for ebb,cbb in vb.items():coeff[(ea+eb-lam[a]+extra-ec+eaa+ebb)%MOD]+=vc*caa*cbb
   for d in range(MOD-1,MOD//2-1,-1):coeff[d-MOD//2]-=coeff[d];coeff[d]=0
   require(not any(coeff[1:]),'noninteger convolution')
   require(coeff[0]>=0 and coeff[0]%len(K)==0,'nonpositive or nonintegral coefficient')
   T[i][j][k]=coeff[0]//len(K)
 unit=next(u for u in range(r)if all(T[u][i][j]==T[i][u][j]==int(i==j)for i,j in itertools.product(range(r),repeat=2)))
 if unit:
  perm=[unit]+[i for i in range(r)if i!=unit];T=[[[T[i][j][k]for k in perm]for j in perm]for i in perm];objs=[objs[i]for i in perm]
 validate(T)
 return T,[{'z':z,'stabilizer':K,'scalar_projective':lam,'character_polynomial':chi}for z,K,c,lam,chi,o in objs]

def source(k=2,extra=0,psi_bit=0):
 els=list(itertools.product(range(8),range(2),range(2)));ix={a:i for i,a in enumerate(els)}
 G=[[ix[((a+(-1)**e*b)%8,(e+f)%2,(z+w)%2)]for b,f,w in els]for a,e,z in els]
 H=[ix[(2*u,e,u%2)]for u in range(4)for e in range(2)];H.sort()
 W=np.zeros((32,32,32),dtype=np.int64)
 for i,(a,e,z)in enumerate(els):
  for j,(b,f,w)in enumerate(els):
   for l,(c,h,v)in enumerate(els):
    carry=(b+(-1)**f*c)//8
    add=((extra&1)*((a%2)*(b%2)*(c%2)) + ((extra>>1)&1)*((a%2)*f*h) + ((extra>>2)&1)*((a%2)*w*v) + ((extra>>3)&1)*((a%2)*f*v))
    W[i,j,l]=2*((k*a*(-1)**e+4*z)*carry+4*add)%MOD
 psi={}
 for i,j in itertools.product(H,repeat=2):
  a,e,z=els[i];b,f,w=els[j];psi[i,j]=psi_bit*8*((a//2+(-1)**e*(b//2))//4)%MOD
 return G,H,W,psi

if __name__=='__main__':
 rr=read();records=[];seen=set()
 for k in[2,6]:
  for extra in range(16):
   for eps in[0,1]:
    print('TRY',k,extra,eps,flush=True)
    G,H,W,psi=source(k,extra,eps)
    try:T,labs=fusion(G,H,W,psi)
    except Exception as ex:print('ERROR',type(ex).__name__,str(ex),flush=True);continue
    print('RANK',len(T),'DUAL',[next(j for j in range(len(T))if T[i][j][0])for i in range(len(T))],flush=True)
    for rid,R in rr.items():
     if rid in seen:continue
     bm=based_iso(R,T)
     if bm is None:continue
     seen.add(rid);print('MATCH',rid,flush=True)
     records.append({'id':rid,'tensor_sha256':sha(R),'status':'candidate_pending_independent_audit','model':'C(D16 x C2, omega, graph(D8 -> C2), psi)','parameters':{'k':k,'extra':extra,'psi_bit':eps},'group_table':G,'subgroup':H,'omega_exponents':W.tolist(),'psi_matrix':[[psi[a,b]for b in H]for a in H],'modulus':MOD,'labels':labs,'model_tensor':T,'basis_map_source_to_model':bm})
     dump(OUT/'gt32_models.json',records)
 print('MATCHED',sorted(seen))
