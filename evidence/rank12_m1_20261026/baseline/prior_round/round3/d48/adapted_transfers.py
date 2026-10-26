from extra_groups import *
from transfer48_models import transfer_generators
from twisted48_models import families as cups
from twisted_h4_matrix import construct
import hashlib

def main():
 ps,S,gens,info=transfer_generators();old=json.loads((ROOT/'rank12-m1-round2-20261025/family_integral/order48_models.json').read_text());parity=[sum(p[i]>p[j]for i in range(4)for j in range(i+1,4))%2 for p in ps]
 D=json.loads((BASE/'tensors.json').read_text());ids=[r['id']for r in json.loads((ROOT/'rank12-m1-round2-20261025/unresolved_tensors.json').read_text())if r['exact_dimension_character']['family']=='D48'];out=[];attempt=[];cupdata=list(cups());fingerprints=set()
 for bits in itertools.product(range(2),repeat=len(gens)):
  V=sum((bit*W for bit,W in zip(bits,gens)),np.zeros((24,24,24),dtype=np.int16))%4
  fp=[]
  for g in range(24):
   k=0;v=0
   while True:
    v+=int(V[g,k,g]);k=S[k][g]
    if k==0:break
   fp.append(v%4)
  if tuple(fp) in fingerprints:continue
  fingerprints.add(tuple(fp))
  for row in old:
   G=row['model']['parameters']['group_table'];H=row['model']['parameters']['subgroup'];name=row['model']['name'];fiber='fiber'in name
   q=[(parity[a//2]+2*(a%2))%4 if fiber else 2*parity[a//2]+a%2 for a in range(48)];section={q[h]:h for h in H};sec=[section[q[a]]//2 for a in range(48)]
   W=np.array([[[2*(int(V[a//2,b//2,c//2])-int(V[sec[a],sec[b],sec[c]]))%8 for c in range(48)]for b in range(48)]for a in range(48)],dtype=np.int16)
   common.require(all(W[a,b,c]==0 for a,b,c in itertools.product(H,repeat=3)),'relative restriction')
   if not W.any():continue
   classes=[0,1]if all(G[h][h]==0 for h in H)else[0];h1,h2=H[1:3];labels={0:(0,0),h1:(1,0),h2:(0,1),G[h1][h2]:(1,1)}
   for name2,G2,H2,v,par2 in cupdata:
    if name2!=name:continue
    def omega(a,b,c,W=W,v=v):return(int(W[a,b,c])+v(a,b,c))%8
    for cl in classes:
     psi=lambda a,b,cl=cl:4*cl*labels[a][0]*labels[b][1]
     R,info=construct(G,H,omega,psi=psi);hits=[]
     if R is not None:
      common.validate(R)
      for rid in ids:
       p=common.based_iso(D[rid],R)
       if p is not None:
        hits.append(rid)
        if any(x['id']==rid for x in out):continue
        out.append(dict(id=rid,name=name,group=G,subgroup=H,tensor=R,source_to_model=p,bits=bits,cup_bits=par2['character_coefficients'],subgroup_class=cl,relative_transfer=W.tolist(),cup=par2))
     attempt.append(dict(name=name,bits=bits,cup_bits=par2['character_coefficients'],subgroup_class=cl,info={k:v for k,v in info.items()if k!='objects'},hits=hits));print(name,bits,par2['character_coefficients'],cl,{k:v for k,v in info.items()if k!='objects'},hits,flush=True)
     (OUT/'adapted_transfer_models.json').write_text(json.dumps(out,indent=2)+'\n');(OUT/'adapted_transfer_attempts.json').write_text(json.dumps(attempt,indent=2)+'\n')
 print('DONE',len(attempt),'attempts',len(out),'hits',flush=True)
if __name__=='__main__':main()
