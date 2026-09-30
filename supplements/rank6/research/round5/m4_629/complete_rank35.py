import sys,json,itertools,time,math
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'));from round5_629 import *
here=Path(__file__).parent;R,d,cols,lab,src=source_data();C=d['C'];rank=35;st=time.monotonic();conj=lambda z:ambient.evaluate(z.to_list(),C.unit**14,C);dot=lambda a,b:sum((x*y for x,y in zip(a,b)),C.zero)
load=lambda v:[C([s.Rational(z) for z in vals]) for vals in v]
b=next(x for x in json.load(open(here/'modular_closure.json')) if x['rank']==35);basis=[(x['pivot'],load(x['vector']),load(x['image'])) for x in b['basis']]
case=next(x for x in json.load(open(here/'decoded_twists.json')) if x['rank']==35 and x['solution']==0);theta=[0]*6;vs=list(cols)
for o in case['orbits']:theta.extend([15//o['root_order']*o['root_power']%15]*o['copies']);vs.extend([(0,)+tuple(o['column'])]*o['copies'])
U={};norm={}
for t in sorted(set(theta)):
 inds=[i for i,x in enumerate(theta) if x==t];rows=[[v[i] for i in inds] for _,v,_ in basis];bs=[]
 for v in rows:
  for p,w in bs:
   if v[p]:q=v[p];v=[x-q*y for x,y in zip(v,w)]
  p=next((i for i,x in enumerate(v) if x),None)
  if p is not None:q=v[p];bs.append((p,[x/q for x in v]))
 piv=[p for p,v in bs];free=[i for i in range(len(inds)) if i not in piv]
 if not free:continue
 require(len(free)==1,'complement T eigenspace not one-dimensional');v=[C.zero]*len(inds);v[free[0]]=C.one
 for p,w in reversed(bs):v[p]=-sum((w[j]*v[j] for j in range(p+1,len(inds))),C.zero)
 u=[C.zero]*rank
 for i,z in zip(inds,v):u[i]=z
 require(all(z==conj(z) for z in u),'nonreal complement vector');require(all(not dot(u,v) for _,v,_ in basis),'nonorthogonal complement')
 U[t]=u;norm[t]=dot(u,u)
require(set(U)=={2,3,8,10,12},'wrong complement spectrum');K=[]
finite=json.load(open(here/'finite_modular_reps.json'));allowed=finite['allowed_tensor_irreps'];decompositions=[]
for counts in finite['decompositions']:
 degrees=sorted(r['degree'] for r,m in zip(allowed,counts) for _ in range(m));negative=sum(r['degree']*m for r,m in zip(allowed,counts) if r['central_sign']==-1)
 decompositions.append((degrees,negative))
require(sorted(decompositions)==[([1,2,2],4),([1,4],0)],'finite representation alternatives changed')
for j in range(rank):
 v=[C.one if i==j else C.zero for i in range(rank)]
 for t,u in U.items():v=[x-u[j]/norm[t]*y for x,y in zip(v,u)]
 w=[C.zero]*rank
 for p,bv,bw in basis:
  q=v[p]
  if q:v=[x-q*y for x,y in zip(v,bv)];w=[x+q*y for x,y in zip(w,bw)]
 require(not any(v),'known projection outside known modular span');K.append(w)
K=[list(row) for row in zip(*K)];require(all(K[i][j]==K[j][i] for i in range(rank) for j in range(rank)),'asymmetric known action')
z3=C.unit**5;z5=C.unit**3;g3=sum((z3**(x*x) for x in range(3)),C.zero);g5=sum((z5**(x*x) for x in range(5)),C.zero)
S3=[[C(1)/g3,C(2)/g3],[C(1)/g3,-C(1)/g3]]
S5=[[(z5**((-2*x*y)%5)-z5**((2*x*y)%5))/g5 for y in (1,2)] for x in (1,2)]
def verify_finite_model(p,SS,TT):
 from collections import deque
 def gm(g,h):return ((g[0]*h[0]+g[1]*h[2])%p,(g[0]*h[1]+g[1]*h[3])%p,(g[2]*h[0]+g[3]*h[2])%p,(g[2]*h[1]+g[3]*h[3])%p)
 def mm(A,B):return [[sum((A[i][k]*B[k][j] for k in range(2)),C.zero) for j in range(2)] for i in range(2)]
 I=(1,0,0,1);seen={I:[[C.one,C.zero],[C.zero,C.one]]};todo=deque([I]);gens=[((0,p-1,1,0),SS),((1,1,0,1),TT)]
 while todo:
  g=todo.popleft()
  for h,B in gens:
   gh=gm(g,h);M=mm(seen[g],B)
   if gh in seen:require(M==seen[gh],'Weil formula not a representation of finite SL2')
   else:seen[gh]=M;todo.append(gh)
 require(len(seen)==p*(p*p-1),'finite representation omitted group elements')
verify_finite_model(3,S3,[[C.one,C.zero],[C.zero,z3]])
verify_finite_model(5,S5,[[z5,C.zero],[C.zero,z5**4]])
require(S3[0][1] and S3[1][0] and S5[0][1] and S5[1][0],'Weil factors not irreducible')
model=[[S3[a][c]*S5[bb][dd] for c in range(2) for dd in range(2)] for a in range(2) for bb in range(2)];order=[3,12,8,2];h=[1,1,2,2];roots=[C.one]
for i in range(1,4):
 ratio=C(h[i])*norm[order[0]]/norm[order[i]];t=s.Symbol('t');poly=s.Poly.from_list([C.one,C.zero,-ratio],t,domain=C);fac=poly.factor_list()[1];linear=[f for f,m in fac if f.degree()==1];require(len(linear)==2,'isometric scaling not in cyclotomic field');fc=linear[0].rep.to_list();root=-fc[1]/fc[0];require(root**2==ratio,'wrong scaling root');roots.append(root)
print('complement and exact Weil blocks built','seconds',time.monotonic()-st,flush=True)
out=[]
for signs in itertools.product((1,-1),repeat=3):
 q=[roots[0]]+[C(sg)*r for sg,r in zip(signs,roots[1:])];S=[[K[i][j]+U[10][i]*U[10][j]/norm[10]+sum((q[a]/q[bb]*model[a][bb]*U[order[a]][i]*U[order[bb]][j]/norm[order[bb]] for a in range(4) for bb in range(4)),C.zero) for j in range(rank)] for i in range(rank)]
 require(all(S[i][j]==S[j][i] for i in range(rank) for j in range(rank)),'asymmetric completion')
 # Exact defining modular relations, no categorification inferred.
 require(all(sum((S[i][k]*S[k][j] for k in range(rank)),C.zero)==C(int(i==j)) for i in range(rank) for j in range(rank)),'S square not identity')
 require(all(sum((S[i][k]*C.unit**theta[k]*S[k][j] for k in range(rank)),C.zero)==C.unit**(-theta[i]-theta[j])*S[i][j] for i in range(rank) for j in range(rank)),'STS failure')
 bad=None;count=0
 for i,j,k in itertools.combinations_with_replacement(range(1,rank),3):
  z=sum((S[i][l]*S[j][l]*S[k][l]/S[0][l] for l in range(rank)),C.zero);co=z.to_list();qq=s.Rational(co[0]) if len(co)==1 else s.Integer(0) if not co else None;count+=1
  if qq is None or qq.q!=1 or qq<0:bad={'triple':[i,j,k],'value':list(map(str,co))};break
 print('signs',signs,'bad',bad,'checks',count,'seconds',time.monotonic()-st,flush=True);rec={'signs':list(signs),'triple_checks':count,'obstruction':bad,'S':[[list(map(str,z.to_list())) for z in row] for row in S]};out.append(rec);(here/'rank35_modular_completions.json').write_text(json.dumps({'rank':35,'branches':out,'complement_norms':{t:list(map(str,g.to_list())) for t,g in norm.items()},'seconds':time.monotonic()-st}))
