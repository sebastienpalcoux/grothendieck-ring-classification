from setup import *
from transfer48_models import transfer_generators
from twisted48_models import schur_cover
from twisted_h8 import solve,objects
from twisted_h8_matrix import construct

def s4_cocycles():
 ps,S,gens,info=transfer_generators();seen=set();rows=[]
 for bits in itertools.product(range(2),repeat=len(gens)):
  V=sum((b*w for b,w in zip(bits,gens)),np.zeros((24,24,24),dtype=np.int16))%4;fp=[]
  for a in range(24):
   x=0;v=0
   while True:
    v+=int(V[a,x,a]);x=S[x][a]
    if x==0:break
   fp.append(v%4)
  if tuple(fp)in seen:continue
  seen.add(tuple(fp));rows.append((bits,V))
 return ps,S,rows

def trivializer(G,H,W):
 var=[(a,b)for a,b in itertools.product(H,repeat=2)if a and b];ix={v:i for i,v in enumerate(var)};eq=[];rhs=[]
 for a,b,c in itertools.product(H,repeat=3):
  r=[0]*len(var)
  for x,y,z in[(b,c,1),(a,G[b][c],1),(G[a][b],c,-1),(a,b,-1)]:
   if x and y:r[ix[x,y]]+=z
  eq.append(r);rhs.append(-int(W[a,b,c])%8)
 sol=solve(eq,rhs,first=True)
 if not sol:return None
 p={v:x for v,x in zip(var,sol[0])};p.update({(a,b):0 for a,b in itertools.product(H,repeat=2)if not a or not b});return p

def main():
 ps,S,vs=s4_cocycles();ps0,S0,beta=schur_cover();common.require(ps==ps0 and S==S0,'same S4coordinates');par=[sum(p[i]>p[j]for i in range(4)for j in range(i+1,4))%2 for p in ps];pindex={p:i for i,p in enumerate(ps)};pairs=json.loads((OUT/'h8_pairs.json').read_text());attempt=[];models=[];seenmodels=set();start=time.monotonic()
 for gi in [28,29,30,48]:
  fam=[r for r in pairs if r['smallgroup'][1]==gi];G=fam[0]['table'];proj=[pindex[tuple(x-1 for x in p)]for p in fam[0]['projection_permutations']];q=fam[0]['quotient_character'];A=np.array(G);pr=np.array(proj);B=np.array(beta)[pr[:,None],pr[None,:]];sg=np.array(par)[pr];q=np.array(q)
  common.require(all(proj[G[a][b]]==S[proj[a]][proj[b]]for a,b in itertools.product(range(48),repeat=2)),'S4quotient homomorphism')
  if len(q):common.require(all(q[G[a][b]]==(q[a]+q[b])%(4 if gi==30 else 2)for a,b in itertools.product(range(48),repeat=2)),'extra quotientcharacter homomorphism')
  extra=list(itertools.product(range(2),repeat=3))if gi==48 else [(k,)for k in range(4)]if gi==30 else [()]
  for bits,V in vs:
   base=2*V[pr[:,None,None],pr[None,:,None],pr[None,None,:]]
   for ex in extra:
    W=base.copy()
    if gi==48:
     W+=4*(ex[0]*q[:,None,None]*q[None,:,None]*q[None,None,:]+ex[1]*sg[:,None,None]*q[None,:,None]*q[None,None,:]+ex[2]*q[:,None,None]*B[None,:,:])
    elif gi==30:W+=2*ex[0]*q[:,None,None]*((q[None,:,None]+q[None,None,:])//4)
    W%=8
    for hi,row in enumerate(fam):
     H=row['subgroup'];p0=trivializer(G,H,W)
     if p0 is None:continue
     for cl,P in enumerate(row['schur_cocycles']):
      p={ (a,b):(p0[a,b]+4*P[i][j])%8 for i,a in enumerate(H)for j,b in enumerate(H)};w=lambda a,b,c:int(W[a,b,c]);psi=lambda a,b:p[a,b]
      objs,info=objects(G,H,w,psi,allow_matrix=True);dims=[] if objs is None else sorted(len(o['D'])*o.get('dimension',1)//8 for o in objs);hits=[]
      if dims==[1]*8+[2]*2+[4]*2:
       M,inf=construct(G,H,w,psi=psi)
       info={k:v for k,v in inf.items()if k!='objects'}
       if M is not None:
        common.validate(M)
        for rid in IDS:
         pmap=common.based_iso(DATA[rid],M)
         if pmap is not None:
          hits.append(rid)
          if rid not in seenmodels:
           seenmodels.add(rid);models.append(dict(id=rid,smallgroup=[48,gi],group_table=G,subgroup=H,modulus=8,omega=W.tolist(),psi=[[p[a,b]for b in H]for a in H],objects=inf['objects'],model_tensor=M,source_tensor=DATA[rid],source_to_model=pmap,source_tensor_sha256=digest(DATA[rid]),model_tensor_sha256=digest(M),omega_sha256=digest(W.tolist()),transfer_bits=bits,extra_bits=ex,subgroup_index=hi,schur_class=cl))
      attempt.append(dict(smallgroup=gi,subgroup_index=hi,transfer_bits=bits,extra=ex,schur_class=cl,dimensions=dims,info=info,matches=hits));print(gi,hi,bits,ex,cl,dims,info,hits,flush=True)
      (OUT/'h8_attempts.json').write_text(json.dumps(attempt,indent=2)+'\n');(OUT/'h8_positive_witnesses.json').write_text(json.dumps(models,separators=(',',':'))+'\n')
 print('DONE',len(attempt),sorted(seenmodels),'seconds',time.monotonic()-start,flush=True)
if __name__=='__main__':main()
