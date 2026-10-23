"""Independent phase-diagram checks and exact character reconstruction for C2 actions."""
import itertools,json,gzip,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def need(v,m):
 if not v:raise ValueError(m)
def check(r,targets):
 m=r['models'][0];p=m['parameters'];G=p['group_table'];f=p['automorphism'];w=p['omega'];J=p['J'];mu=p['mu'];n=len(G);I=range(n)
 need(p['modulus']==8,'modulus')
 need(all(G[0][a]==G[a][0]==a and f[f[a]]==a for a in I),'identity and involution')
 need(all(G[G[a][b]][c]==G[a][G[b][c]] for a,b,c in itertools.product(I,repeat=3)),'group associativity')
 need(all(any(G[a][b]==G[b][a]==0 for b in I) for a in I),'inverses')
 need(all(f[G[a][b]]==G[f[a]][f[b]] for a,b in itertools.product(I,repeat=2)),'automorphism')
 need(all(w[a][b][c]%8==0 for a,b,c in itertools.product(I,repeat=3) if 0 in [a,b,c]),'normalized omega')
 need(all(J[0][a]==J[a][0]==0 for a in I) and mu[0]==0,'normalized action')
 for a,b,c,d in itertools.product(I,repeat=4):
  need((w[b][c][d]-w[G[a][b]][c][d]+w[a][G[b][c]][d]-w[a][b][G[c][d]]+w[a][b][c])%8==0,'pointed pentagon')
 for a,b,c in itertools.product(I,repeat=3):
  need((J[a][b]+J[G[a][b]][c]+w[a][b][c]-w[f[a]][f[b]][f[c]]-J[b][c]-J[a][G[b][c]])%8==0,'tensorator pentagon')
 for a,b in itertools.product(I,repeat=2):
  need((mu[G[a][b]]+J[f[a]][f[b]]+J[a][b]-mu[a]-mu[b])%8==0,'compositor monoidality')
 need(all(mu[a]==mu[f[a]] for a in I),'action pentagon')
 # Each orbit has stabilizer 1 or C2. Construct every equivariant simple;
 # its nonidentity fiber map is a sixteenth root of unity.
 objects=[];seen=set()
 for a in I:
  if a in seen:continue
  O=sorted({a,f[a]});seen.update(O)
  for sign in ([0,1] if len(O)==1 else [0]):
   U={a:(mu[a]+8*sign)%16} if len(O)==1 else {O[0]:0,O[1]:2*mu[O[0]]%16}
   need(all((U[x]+U[f[x]]-2*mu[x])%16==0 for x in O),'simple equivariance')
   objects.append((O,sign,U))
 need(sum(len(O)**2 for O,_,_ in objects)==2*n,'complete simple-object count')
 rank=len(objects);T=[[[0]*rank for _ in range(rank)]for _ in range(rank)]
 for i,(A,_,U) in enumerate(objects):
  for j,(B,_,V) in enumerate(objects):
   for k,(C,_,W) in enumerate(objects):
    c=C[0];pairs=[(a,b) for a in A for b in B if G[a][b]==c]
    if len(C)==2:T[i][j][k]=len(pairs);continue
    # The quotient multiplicity is the +1 eigenspace of the C2 Hom action.
    trace=[0]*16
    for a,b in pairs:
     if a==f[a] and b==f[b]:trace[(U[a]+V[b]-2*J[a][b]-W[c])%16]+=1
    coeff=[trace[z]-trace[z+8] for z in range(8)]
    need(not any(coeff[1:]),'rational exact trace')
    value=len(pairs)+coeff[0];need(value>=0 and value%2==0,'integral multiplicity');T[i][j][k]=value//2
 need(T==m['model_tensor'],'independent fusion reconstruction')
 q=m['basis_map_source_to_model'];R=targets[r['id']]
 need(sorted(q)==list(range(rank)) and q[0]==0,'basis map')
 need(all(R[i][j][k]==T[q[i]][q[j]][q[k]] for i,j,k in itertools.product(range(rank),repeat=3)),'source fusion coefficients')
 need(hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()==r['tensor_sha256'],'source hash')
 return {'id':r['id'],'verdict':'PASS','checks':['all pointed pentagons','all monoidal C2 action diagrams','complete equivariant simples','all fusion coefficients by exact Hom-action traces','source basis map and hash']}
if __name__=='__main__':
 targets={f'R9_1_{i}':json.loads(line.replace('{','[').replace('}',']')) for i,line in enumerate(gzip.open(ROOT/'inputs/rank9_M1_verified/FusionRingMultiplicationTables.txt.gz','rt'),1)}
 result=[check(r,targets) for r in json.load(open(ROOT/'work/resolve_small_models/coherent_c2_models.json'))]
 (Path(__file__).parent/'c2_audit.json').write_text(json.dumps(result,indent=2)+'\n')
 print(result)
