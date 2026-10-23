"""Homogeneous bimodules over 1+s in Vec(G,omega), exact root-of-unity phases."""
import itertools,json,sys
from pathlib import Path
BASE=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(BASE/'work/models'))
from match_models import read,based_iso,tensor_hash

def fusion(G,s,w,mod=8):
 nG=len(G);I=range(nG)
 assert s!=0 and G[s][s]==0
 assert all(w(a,b,c)%mod==0 for a,b,c in itertools.product([0,s],repeat=3))
 assert all((w(b,c,d)-w(G[a][b],c,d)+w(a,G[b][c],d)-w(a,b,G[c][d])+w(a,b,c))%mod==0 for a,b,c,d in itertools.product(I,repeat=4))
 seen=set();objs=[]
 for z in I:
  if z in seen:continue
  D=sorted({z,G[s][z],G[z][s],G[G[s][z]][s]});seen.update(D)
  L={}
  for x in D:
   if x in L:continue
   L[x]=0;L[G[s][x]]=-w(s,s,x)%mod
  sols=[]
  for q in range(mod):
   R={z:q};changed=True;ok=True
   while changed and ok:
    changed=False
    for x,v in list(R.items()):
     for y,u in [(G[x][s],w(x,s,s)-v),(G[s][x],w(s,x,s)+v+L[G[x][s]]-L[x])]:
      u%=mod
      if y in R and R[y]!=u:ok=False;break
      if y not in R:R[y]=u;changed=True
   if ok:
    assert len(R)==len(D)
    sols.append(R)
    if len(D)==4:break
  assert len(sols)==(2 if len(D)==2 else 1)
  for R in sols:
   assert all((L[x]+L[G[s][x]]+w(s,s,x))%mod==0 and (R[x]+R[G[x][s]]-w(x,s,s))%mod==0 and (L[x]+R[G[s][x]]-R[x]-L[G[x][s]]-w(s,x,s))%mod==0 for x in D)
   objs.append(dict(z=z,D=D,L=L,R=R,e=(R[z]-L[z])%mod))
 nr=len(objs);N=[[[0]*nr for _ in range(nr)]for _ in range(nr)]
 import sympy as sy
 t=sy.Symbol('t');cp=sy.Poly(sy.cyclotomic_poly(mod,t),t)
 for i,A in enumerate(objs):
  for j,B in enumerate(objs):
   maps={}
   for x,y in itertools.product(A['D'],B['D']):
    P=(x,y);Q=(G[x][s],G[s][y]);rep=min(P,Q)
    ph=(w(G[x][s],s,y)+B['L'][y]-A['R'][G[x][s]])%mod
    back=(w(x,s,G[s][y])+B['L'][G[s][y]]-A['R'][x])%mod
    assert (ph+back)%mod==0
    maps[P]=(rep,0 if P==rep else ph)
   reps=sorted({r for r,p in maps.values()})
   for k,C in enumerate(objs):
    z=C['z'];basis=[P for P in reps if G[P[0]][P[1]]==z]
    if len(C['D'])==4:N[i][j][k]=len(basis);continue
    trace=[0]*mod
    for P in basis:
     x,y=P;target=(G[s][x],G[y][s]);rep,ph=maps[target]
     a=(w(x,y,s)+B['R'][y]-A['L'][G[s][x]]+w(s,G[s][x],G[y][s])+ph-C['e'])%mod
     if rep==P:trace[a]+=1
    r=sy.Poly.from_list(list(reversed(trace)),t).rem(cp)
    assert r.degree()<=0,(i,j,k,trace)
    value=len(basis)+int(r.as_expr())
    assert value>=0 and value%2==0
    N[i][j][k]=value//2
 assert all(N[0][i][j]==N[i][0][j]==int(i==j) for i in range(nr) for j in range(nr))
 # Full independent associativity, no numeric tolerance.
 assert all(sum(N[i][j][p]*N[p][k][l] for p in range(nr))==sum(N[j][k][p]*N[i][p][l] for p in range(nr)) for i,j,k,l in itertools.product(range(nr),repeat=4))
 return N,objs

def pgl2f3():
 def mm(a,b):return ((a[0]*b[0]+a[1]*b[2])%3,(a[0]*b[1]+a[1]*b[3])%3,(a[2]*b[0]+a[3]*b[2])%3,(a[2]*b[1]+a[3]*b[3])%3)
 def norm(a):
  c=next(x for x in a if x);return tuple(c*x%3 for x in a),int(c==2)
 els=sorted({norm(a)[0]for a in itertools.product(range(3),repeat=4)if (a[0]*a[3]-a[1]*a[2])%3});ident=(1,0,0,1);els.remove(ident);els.insert(0,ident);ix={a:i for i,a in enumerate(els)}
 G=[[ix[norm(mm(a,b))[0]]for b in els]for a in els];beta=[[norm(mm(a,b))[1]for b in els]for a in els];alpha=[int((a[0]*a[3]-a[1]*a[2])%3==2)for a in els]
 return G,beta,alpha

def main():
 G,b,a=pgl2f3();s=next(i for i in range(1,24)if G[i][i]==0 and a[i]);out=[]
 for eps in [0,1]:
  corr=eps*b[s][s]
  w=lambda i,j,k:4*(eps*a[i]*b[j][k]+corr*a[i]*a[j]*a[k])%8
  R,labels=fusion(G,s,w);print('CASE',eps,'rank',len(R),flush=True)
  for idx,T in enumerate(read(9),1):
   p=based_iso(T,R)
   if p is not None:
    rid=f'R9_1_{idx}';print('MATCH',rid,flush=True)
    out.append({'id':rid,'tensor_sha256':tensor_hash(T),'status':'unitarily_realized','models':[{'model':f'C(S4,omega_{eps},C2,1)','constructor':'twisted_c2_bimodules','parameters':{'eps':eps,'correction':corr,'s':s},'reference':'Explicit unitary subgroup-algebra bimodules in Vec(S4,omega); phase associativity and all fusion coefficients checked exactly.','basis_map_source_to_model':p,'model_tensor':R,'homogeneous_bimodules':labels}]})
 (Path(__file__).parent/'twisted_c2_models.json').write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
