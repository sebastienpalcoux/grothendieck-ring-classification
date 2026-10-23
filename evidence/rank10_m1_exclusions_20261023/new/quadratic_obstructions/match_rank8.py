import json,gzip,itertools,hashlib
from pathlib import Path
import numpy as np
P=Path(__file__).resolve().parent
raw=gzip.open(P/'lower_rank/rank8_tables.txt.gz','rt').read().splitlines();rows=[]
decs={r['tensor_sha256']:r for r in json.loads((P/'lower_rank/decisions.json').read_text())}
for line in raw:
 N=np.array(json.loads(line.replace('{','[').replace('}',']')),dtype=int)
 G=[i for i in range(8) if all(sum(N[i,j])==1 for j in range(8))]
 if len(G)!=2:continue
 # PF vector fromsumleftmatrices
 e,v=np.linalg.eig(np.sum(N,axis=0).T);w=np.abs(v[:,np.argmax(e.real)].real);w/=w[0]
 if not all(min(abs(x-y) for y in [1,1+2**.5,3+2*2**.5])<1e-7 for x in w):continue
 Y=[i for i,x in enumerate(w) if abs(x-(1+2**.5))<1e-7];Z=[i for i,x in enumerate(w) if abs(x-(3+2*2**.5))<1e-7]
 if len(Y)!=4 or len(Z)!=2:continue
 h=hashlib.sha256(json.dumps(N.tolist(),separators=(',',':')).encode()).hexdigest();rows.append((N,G,Y,Z,decs.get(h,{'hash':h})))
print('candidates',len(rows),[a[-1].get('id') for a in rows]);out=[]
for k in [21,114,115,152,153,179]:
 d=json.loads((P/f'R10_1_{k}_dual_tensor.json').read_text());N=np.array(d['fusion_tensor']);u=d['unit'];S={u}
 for i in range(16):S.update(np.flatnonzero(N[i,d['dual'][i]]))
 while True:
  T=set(S)
  for i in T:
   for j in T:S.update(np.flatnonzero(N[i,j]))
  if S==T:break
 order=[u]+sorted(map(int,S-{u}));B=N[np.ix_(order,order,order)];dims=[d['dimensions'][i] for i in order];G=[i for i,x in enumerate(dims) if x==[1,0]];Y=[i for i,x in enumerate(dims) if x==[1,1]];Z=[i for i,x in enumerate(dims) if x==[3,2]];matches=[]
 for C,g,y,z,decision in rows:
  for yp in itertools.permutations(y):
   for zp in itertools.permutations(z):
    p=[None]*8
    for a,b in zip(G,g):p[a]=b
    for a,b in zip(Y,yp):p[a]=b
    for a,b in zip(Z,zp):p[a]=b
    if np.array_equal(B,C[np.ix_(p,p,p)]):matches.append({'decision':decision,'D_ad_basis_in_D':order,'D_ad_to_rank8_basis':p});break
   if matches and matches[-1]['decision']==decision:break
 print(k,'maxmult',int(B.max()),'matches',[(m['decision'].get('id'),m['decision'].get('status'),m['decision'].get('models')) for m in matches]);out.append({'id':f'R10_1_{k}','max_multiplicity':int(B.max()),'matches':matches})
(P/'rank8_matches.json').write_text(json.dumps(out,indent=2)+'\n')
