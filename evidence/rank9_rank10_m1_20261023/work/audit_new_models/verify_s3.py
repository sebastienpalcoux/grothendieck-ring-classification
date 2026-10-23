"""Independent reconstruction of coherent pointed S3 equivariantizations.

Does not import action_search.py or its Gaussian elimination / fusion routine.
Checks monoidal diagrams directly, constructs the equivariant simple objects
as honest projective matrix actions, and computes their tensor characters.
"""
import itertools,json,gzip,hashlib
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent

def require(c,m):
 if not c:raise ValueError(m)

perms=list(itertools.permutations(range(3)))
P=[[sum(((a>>p[i])&1)<<i for i in range(3)) for a in range(8)] for p in perms]
G=[[P.index([P[g][P[h][a]] for a in range(8)]) for h in range(6)] for g in range(6)]
inverse=[next(h for h in range(6) if G[g][h]==G[h][g]==0) for g in range(6)]
parity=[sum(p[i]>p[j] for i in range(3) for j in range(i+1,3))%2 for p in perms]
std=[]
for g in range(6):
 Q=np.zeros((3,3),dtype=np.int64)
 for i in range(3):Q[(P[g][1<<i]).bit_length()-1,i]=1
 B=np.array([[1,0],[0,1],[-1,-1]],dtype=np.int64)
 M=(Q@B)[:2,:]
 require(np.array_equal(Q@B,B@M),'standard representation restriction')
 std.append(M)
for g,h in itertools.product(range(6),repeat=2):
 require(np.array_equal(std[g]@std[h],std[G[g][h]]),'ordinary S3 representation')

def cocycle(bits):
 def w(a,b,c):
  aa=[a>>i&1 for i in range(3)];bb=[b>>i&1 for i in range(3)];cc=[c>>i&1 for i in range(3)]
  vals=[aa[i]*bb[i]*cc[i] for i in range(3)]
  vals += [aa[j]*bb[i]*cc[i] for i in range(3) for j in range(i+1,3)]
  vals += [aa[0]*bb[1]*cc[2]]
  return 4*sum(v*t for v,t in zip(vals,bits))%8
 return w

def phase_matrix_equal(e,M,f,N):
 z=(e-f)%48
 return (z==0 and np.array_equal(M,N)) or (z==24 and np.array_equal(M,-N))

def scalar_splitting(H,c,mu):
 generators=[];closure={0}
 for h in H:
  if h in closure:continue
  generators.append(h)
  while True:
   more=closure|{G[g][k] for g in closure for k in generators}
   if more==closure:break
   closure=more
 for chosen in itertools.product(range(48),repeat=len(generators)):
  lam={0:0};queue=[0];ok=True
  for g in queue:
   for h,x in zip(generators,chosen):
    gh=G[g][h];v=(lam[g]+x-6*mu[g][h][c])%48
    if gh in lam:
     if lam[gh]!=v:ok=False;break
    else:lam[gh]=v;queue.append(gh)
   if not ok:break
  if ok and all((lam[g]+lam[h]-lam[G[g][h]]-6*mu[g][h][c])%48==0 for g,h in itertools.product(H,repeat=2)):
   return lam
 raise ValueError('projective stabilizer not split by supplied phases')

def build_objects(mu):
 objects=[]
 for weight in range(4):
  orbit=[a for a in range(8) if a.bit_count()==weight];c=orbit[0]
  H=[g for g in range(6) if P[g][c]==c]
  lam=scalar_splitting(H,c,mu)
  t={a:next(g for g in range(6) if P[g][c]==a) for a in orbit}
  reps=['triv','sign','std'] if len(H)==6 else ['triv','sign']
  require(sum((2 if r=='std' else 1)**2 for r in reps)==len(H),'complete stabilizer irreducibles')
  for rep in reps:
   maps={};dim=2 if rep=='std' else 1
   for g,a in itertools.product(range(6),orbit):
    b=P[g][a];h=G[inverse[t[b]]][G[g][t[a]]]
    require(h in H,'transport stabilizer')
    exponent=(6*(mu[g][t[a]][c]-mu[t[b]][h][c])+lam[h])%48
    matrix=std[h] if rep=='std' else np.array([[(-1)**parity[h] if rep=='sign' else 1]],dtype=np.int64)
    maps[g,a]=(exponent,matrix)
   for g,h,a in itertools.product(range(6),range(6),orbit):
    e,U=maps[g,P[h][a]];f,V=maps[h,a];q,W=maps[G[g][h],a]
    require(phase_matrix_equal(e+f,U@V,q+6*mu[g][h][a],W),'equivariant-object matrix coherence')
   objects.append({'label':[weight,rep],'orbit':orbit,'representative':c,'stabilizer':H,'maps':maps,'dimension':len(orbit)*dim})
 require(sum(o['dimension']**2 for o in objects)==48,'global dimension')
 return objects

def residue(coeff):
 co=coeff[:]
 for d in range(47,15,-1):
  co[d-8]+=co[d];co[d-16]-=co[d];co[d]=0
 require(not any(co[1:]),'multiplicity is not rational')
 return co[0]

def tensor_from_objects(objects,J):
 n=len(objects);N=[[[0]*n for _ in range(n)] for _ in range(n)]
 for i,X in enumerate(objects):
  for j,Y in enumerate(objects):
   for k,Z in enumerate(objects):
    c=Z['representative'];H=Z['stabilizer'];co=[0]*48
    for g in H:
     ek,Mk=Z['maps'][g,c];tk=int(np.trace(Mk))
     for a in X['orbit']:
      b=a^c
      if b not in Y['orbit'] or P[g][a]!=a or P[g][b]!=b:continue
      ea,Ma=X['maps'][g,a];eb,Mb=Y['maps'][g,b]
      co[(ea+eb-6*J[g][a][b]-ek)%48]+=int(np.trace(Ma))*int(np.trace(Mb))*tk
    z=residue(co);require(z>=0 and z%len(H)==0,'nonnegative integral multiplicity')
    N[i][j][k]=z//len(H)
 return N

def verify_record(record,targets):
 model=record['models'][0];pars=model['parameters'];J=pars['J'];mu=pars['mu'];w=cocycle(pars['omega_bits'])
 require(pars['modulus']==8,'phase modulus')
 require(all(w(a,b,c)==0 for a,b,c in itertools.product(range(8),repeat=3) if 0 in [a,b,c]),'normalized associator')
 require(all(J[g][a][b]==0 for g,a,b in itertools.product(range(6),range(8),range(8)) if g==0 or a==0 or b==0),'normalized tensorators')
 require(all(mu[g][h][a]==0 for g,h,a in itertools.product(range(6),range(6),range(8)) if g==0 or h==0 or a==0),'normalized compositors')
 for a,b,c,d in itertools.product(range(8),repeat=4):
  require((w(b,c,d)-w(a^b,c,d)+w(a,b^c,d)-w(a,b,c^d)+w(a,b,c))%8==0,'pointed pentagon')
 for g,a,b,c in itertools.product(range(6),range(8),range(8),range(8)):
  # J : F(a) tensor F(b) -> F(a tensor b).
  lhs=J[g][a][b]+J[g][a^b][c]+w(a,b,c)
  rhs=w(P[g][a],P[g][b],P[g][c])+J[g][b][c]+J[g][a][b^c]
  require((lhs-rhs)%8==0,'monoidal functor pentagon')
 for g,h,a,b in itertools.product(range(6),range(6),range(8),range(8)):
  lhs=mu[g][h][a^b]+J[g][P[h][a]][P[h][b]]+J[h][a][b]
  rhs=J[G[g][h]][a][b]+mu[g][h][a]+mu[g][h][b]
  require((lhs-rhs)%8==0,'compositor monoidality')
 for g,h,k,a in itertools.product(range(6),range(6),range(6),range(8)):
  require((mu[g][h][P[k][a]]+mu[G[g][h]][k][a]-mu[h][k][a]-mu[g][G[h][k]][a])%8==0,'categorical action associativity')
 objects=build_objects(mu);N=tensor_from_objects(objects,J)
 require([o['label'] for o in objects]==model['labels'],'simple labels')
 require(N==model['model_tensor'],'stored tensor differs from independent reconstruction')
 p=model['basis_map_source_to_model'];R=targets[record['id']]
 require(sorted(p)==list(range(10)) and p[0]==0,'based map permutation')
 require(all(R[i][j][k]==N[p[i]][p[j]][p[k]] for i,j,k in itertools.product(range(10),repeat=3)),'based tensor map')
 return {'id':record['id'],'verdict':'PASS','coherence':'all normalized diagrams checked modulo 8',
         'simple_objects':'all projective matrix-action identities checked modulo roots of unity of order 48',
         'fusion':'all 1000 coefficients independently reconstructed by stabilizer character inner products',
         'categorical_conclusion':'unitary equivariantization exists'}

if __name__=='__main__':
 records=json.load(open(ROOT/'work/resolve_small_models/coherent_s3_models.json'))
 targets={f'R10_1_{i}':json.loads(line.replace('{','[').replace('}',']')) for i,line in enumerate(gzip.open(ROOT/'inputs/rank10_M1_verified/FusionRingMultiplicationTables.txt.gz','rt'),1)}
 results=[]
 for r in records:
  results.append(verify_record(r,targets));print(r['id'],'PASS',flush=True)
 (OUT/'s3_audit.json').write_text(json.dumps(results,indent=2)+'\n')
