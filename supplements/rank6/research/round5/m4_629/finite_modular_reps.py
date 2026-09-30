"""Derive small modular-representation spectra from finite group class algebras."""
import sys,json,itertools,math,time
from pathlib import Path
import sympy as s
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'));from exact import require
here=Path(__file__).parent;st=time.monotonic()
def mul(g,h,p):a,b,c,d=g;e,f,u,v=h;return ((a*e+b*u)%p,(a*f+b*v)%p,(c*e+d*u)%p,(c*f+d*v)%p)
def inv(g,p):a,b,c,d=g;return (d,-b%p,-c%p,a)
def records(p):
 G=[g for g in itertools.product(range(p),repeat=4) if (g[0]*g[3]-g[1]*g[2])%p==1];unit=(1,0,0,1);center=((-1)%p,0,0,(-1)%p);T=(1,1,0,1);todo=set(G);classes=[]
 while todo:
  g=unit if unit in todo else min(todo);cl={mul(mul(h,g,p),inv(h,p),p) for h in G};classes.append(sorted(cl));todo-=cl
 classes.sort(key=lambda c:(c!=[unit],len(c),c));ix={g:i for i,cl in enumerate(classes) for g in cl};n=len(classes);N=[[[0]*n for _ in range(n)] for _ in range(n)]
 for i,Ci in enumerate(classes):
  for j,Cj in enumerate(classes):
   for x in Ci:
    for y in Cj:N[i][j][ix[mul(x,y,p)]]+=1
   for k in range(n):require(N[i][j][k]%len(classes[k])==0,'nonintegral class algebra');N[i][j][k]//=len(classes[k])
 M=[s.Matrix(n,n,lambda k,j:N[i][j][k]) for i in range(n)];generic=sum(((i+1)**2*M[i] for i in range(n)),s.zeros(n));ev=generic.eigenvects();require(len(ev)==n and all(m==1 for _,m,_ in ev),'primitive class element collision')
 rec=[];z=s.exp(2*s.pi*s.I/p);powers=[unit]
 for _ in range(1,p):powers.append(mul(powers[-1],T,p))
 for eigenvalue,multiplicity,vecs in ev:
  v=vecs[0];q=next(i for i,x in enumerate(v) if x);lam=[s.simplify((mm*v)[q]/v[q]) for mm in M]
  dim=s.simplify(s.sqrt(len(G)/sum((x*s.conjugate(x)/len(cl) for x,cl in zip(lam,classes)),s.S.Zero)));require(dim.is_Integer and dim>0,'nonintegral irrep degree');chars=[s.simplify(dim*x/len(cl)) for x,cl in zip(lam,classes)]
  spec=[]
  for a in range(p):
   value=s.simplify(s.expand_complex(sum((chars[ix[g]]*z**(-a*r) for r,g in enumerate(powers)),s.S.Zero)/p));value=s.simplify(value.rewrite(s.sqrt));require(value.is_Integer and value>=0,'bad exact T eigen multiplicity');spec.append(int(value))
  sign=s.simplify(chars[ix[center]]/dim);require(sign in (1,-1),'bad central character')
  rec.append({'degree':int(dim),'T_multiplicities':spec,'central_sign':int(sign),'characters':list(map(str,chars))})
 rec.sort(key=lambda x:(x['degree'],x['T_multiplicities'],x['central_sign']));return {'p':p,'order':len(G),'classes':classes,'class_algebra':N,'irreps':rec}
data=[records(p) for p in (3,5)];irreps=[]
for i,a in enumerate(data[0]['irreps']):
 for j,b in enumerate(data[1]['irreps']):
  if a['degree']*b['degree']>5:continue
  spec=[0]*15
  for x,m in enumerate(a['T_multiplicities']):
   for y,n in enumerate(b['T_multiplicities']):spec[(5*x+3*y)%15]+=m*n
  irreps.append({'factors':[i,j],'degree':a['degree']*b['degree'],'spectrum':spec,'central_sign':a['central_sign']*b['central_sign']})
target=[int(i in (2,3,8,10,12)) for i in range(15)];allowed=[r for r in irreps if all(a<=b for a,b in zip(r['spectrum'],target))];solutions=[]
def dfs(k,remaining,cs):
 if k==len(allowed):
  if not any(remaining):solutions.append(cs)
  return
 spec=allowed[k]['spectrum'];bound=min((b//a for a,b in zip(spec,remaining) if a),default=0)
 for m in range(bound+1):dfs(k+1,[b-m*a for a,b in zip(spec,remaining)],cs+[m])
dfs(0,target,[]);out={'finite_groups':data,'target_spectrum':target,'allowed_tensor_irreps':allowed,'decompositions':solutions,'seconds':time.monotonic()-st};(here/'finite_modular_reps.json').write_text(json.dumps(out,indent=2));print('allowed',allowed,'decompositions',solutions,'seconds',out['seconds'],flush=True)
