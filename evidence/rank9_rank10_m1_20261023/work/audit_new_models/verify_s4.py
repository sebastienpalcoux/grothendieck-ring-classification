"""Audit explicit C2 subgroup bimodules using monomial maps on balanced products.

The discovery routine is not imported. All phases are exponents modulo 8.
"""
import itertools,json,gzip,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def need(v,m):
 if not v:raise ValueError(m)
def check(record,targets):
 model=record['models'][0];p=model['parameters'];G=p['group_table'];s=p['s'];w=p['omega_exponents'];n=len(G);I=range(n)
 need(p['modulus']==8 and s!=0 and G[s][s]==0,'subgroup')
 need(all(G[0][a]==G[a][0]==a and any(G[a][b]==G[b][a]==0 for b in I) for a in I),'group identities')
 need(all(G[G[a][b]][c]==G[a][G[b][c]] for a,b,c in itertools.product(I,repeat=3)),'group associativity')
 need(all(w[a][b][c]%8==0 for a,b,c in itertools.product(I,repeat=3) if 0 in [a,b,c]),'normalization')
 need(all(w[a][b][c]%8==0 for a,b,c in itertools.product([0,s],repeat=3)),'subgroup algebra associativity')
 for a,b,c,d in itertools.product(I,repeat=4):
  need((w[b][c][d]-w[G[a][b]][c][d]+w[a][G[b][c]][d]-w[a][b][G[c][d]]+w[a][b][c])%8==0,'pointed pentagon')
 objs=[];bycoset={}
 for raw in model['homogeneous_bimodules']:
  o=dict(raw);o['L']={int(k):v for k,v in o['L'].items()};o['R']={int(k):v for k,v in o['R'].items()};D=o['D'];z=o['z'];L=o['L'];R=o['R']
  need(D==sorted({z,G[s][z],G[z][s],G[G[s][z]][s]}),'double coset support')
  for x in D:
   need((L[x]+L[G[s][x]]+w[s][s][x])%8==0,'left module diagram')
   need((R[x]+R[G[x][s]]-w[x][s][s])%8==0,'right module diagram')
   need((L[x]+R[G[s][x]]-R[x]-L[G[x][s]]-w[s][x][s])%8==0,'bimodule diagram')
  need(o['e']==(R[z]-L[z])%8,'eigenphase')
  bycoset.setdefault(tuple(D),[]).append(o);objs.append(o)
 need(set().union(*(set(D)for D in bycoset))==set(I),'all double cosets')
 for D,oo in bycoset.items():
  need(len(oo)==(2 if len(D)==2 else 1),'complete irreducibles')
  if len(oo)==2:need((oo[0]['e']-oo[1]['e'])%8==4,'inequivalent stabilizer characters')
 need(sum((len(o['D'])//2)**2 for o in objs)==n,'global dimension')
 rank=len(objs);T=[[[0]*rank for _ in range(rank)]for _ in range(rank)]
 for i,A in enumerate(objs):
  for j,B in enumerate(objs):
   pairs=list(itertools.product(A['D'],B['D']))
   # Each balance orbit has size two. Return [x,y]=zeta^phase [representative].
   def normal(pair):
    x,y=pair;other=(G[x][s],G[s][y]);rep=min(pair,other)
    return (rep,0) if pair==rep else (rep,(w[G[x][s]][s][y]+B['L'][y]-A['R'][G[x][s]])%8)
   basis=sorted({normal(pair)[0]for pair in pairs})
   def act(pair,left):
    x,y=pair
    if left:target=(G[s][x],y);phase=A['L'][x]-w[s][x][y]
    else:target=(x,G[y][s]);phase=w[x][y][s]+B['R'][y]
    q,e=normal(target);return q,(phase+e)%8
   for pair in pairs:
    x,y=pair;other=(G[x][s],G[s][y]);phase=(w[G[x][s]][s][y]+B['L'][y]-A['R'][G[x][s]])%8
    for left in [False,True]:
     q,e=act(pair,left);r,f=act(other,left);need(q==r and (e-f-phase)%8==0,'balanced action well-defined')
   left={b:act(b,True)for b in basis};right={b:act(b,False)for b in basis}
   for b in basis:
    degree=G[b[0]][b[1]];l,e=left[b];ll,f=left[l];r,g=right[b];rr,h=right[r]
    need(ll==b and (e+f+w[s][s][degree])%8==0,'tensor left module')
    need(rr==b and (g+h-w[degree][s][s])%8==0,'tensor right module')
    lr,u=right[l];rl,v=left[r]
    need(lr==rl and (e+u-g-v-w[s][degree][s])%8==0,'tensor bimodule')
   invleft={q:(b,(-e)%8)for b,(q,e)in left.items()}
   for k,C in enumerate(objs):
    z=C['z'];fiber=[b for b in basis if G[b[0]][b[1]]==z]
    if len(C['D'])==4:T[i][j][k]=len(fiber);continue
    trace=[0]*8
    for b in fiber:
     q,e=right[b];r,f=invleft[q]
     if r==b:trace[(e+f-C['e'])%8]+=1
    coeff=[trace[a]-trace[a+4]for a in range(4)];need(not any(coeff[1:]),'rational trace in Q(zeta8)')
    value=len(fiber)+coeff[0];need(value>=0 and value%2==0,'integral multiplicity');T[i][j][k]=value//2
 need(T==model['model_tensor'],'independent monomial tensor reconstruction')
 R=targets[record['id']];q=model['basis_map_source_to_model']
 need(sorted(q)==list(range(rank)) and q[0]==0,'based permutation')
 need(all(R[i][j][k]==T[q[i]][q[j]][q[k]]for i,j,k in itertools.product(range(rank),repeat=3)),'source tensor')
 need(hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()==record['tensor_sha256'],'source hash')
 return {'id':record['id'],'verdict':'PASS','checks':['all pointed pentagons','all simple bimodule diagrams and completeness','balanced tensor product maps well-defined','all tensor bimodule diagrams','all fusion coefficients by exact eigencharacters','source tensor and hash']}
if __name__=='__main__':
 targets={f'R9_1_{i}':json.loads(line.replace('{','[').replace('}',']')) for i,line in enumerate(gzip.open(ROOT/'inputs/rank9_M1_verified/FusionRingMultiplicationTables.txt.gz','rt'),1)}
 result=[check(r,targets)for r in json.load(open(ROOT/'work/resolve_small_models/s4_twisted_models.json'))]
 (Path(__file__).parent/'s4_audit.json').write_text(json.dumps(result,indent=2)+'\n');print(result)
