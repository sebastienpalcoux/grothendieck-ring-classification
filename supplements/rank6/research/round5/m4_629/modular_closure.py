import sys,json,math,time
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'));from round5_629 import *
here=Path(__file__).parent;R,d,cols,lab,src=source_data();C=d['C'];D=d['DD'];tab=d['tab'];st=time.monotonic();out=[]
def sigma(z,a):return ambient.evaluate(z.to_list(),C.unit**a,C)
def dot(v,w):return sum((x*y for x,y in zip(v,w)),C.zero)
for case in json.load(open(here/'decoded_twists.json')):
 if case['solution']!=0:continue
 rank=case['rank'];vs=list(map(tuple,cols));theta=[C.one]*6
 for o in case['orbits']:
  require(o['orbit_degree']==1,'nontrivial twist orbit')
  vs.extend([(0,)+tuple(o['column'])]*o['copies']);theta.extend([C.unit**(15//o['root_order']*o['root_power'])]*o['copies'])
 require(len(vs)==rank,'rank mismatch');sp=Spectrum(tab,cols,[(v[1:],None) for v in set(vs[6:])]);tt=dict(zip(sp.vectors,sp.types));lowS=[[tt[v][lab[a]]*tab.dims[v]/D for v in vs] for a in range(6)]
 perm={}
 for a in range(15):
  if math.gcd(a,15)>1:continue
  pp=[]
  for i in range(6):
   matches=[(j,sg) for j in range(6) for sg in (1,-1) if all(sigma(lowS[k][i],a)==C(sg)*lowS[k][j] for k in range(6))]
   require(len(matches)==1,'ambiguous low Galois permutation');pp.append(matches[0])
  perm[a]=pp
 basis=[];orig=[];failure=None
 def add(v,w,label):
  global failure
  orig.append((list(v),list(w),label))
  for p,bv,bw in basis:
   q=v[p]
   if q:v=[x-q*y for x,y in zip(v,bv)];w=[x-q*y for x,y in zip(w,bw)]
  nz=next((i for i,x in enumerate(v) if x),None)
  if nz is None:
   if any(w):failure={'relation':label,'nonzero_image':[[i,list(map(str,x.to_list()))] for i,x in enumerate(w) if x]};return False
   return True
  q=v[nz];basis.append((nz,[x/q for x in v],[x/q for x in w]));return True
 for i in range(6):add([C.one if j==i else C.zero for j in range(rank)],list(lowS[i]),['basis',i])
 for n in [0]+[a for a in range(15) if math.gcd(a,15)==1]:
  for i in range(6):
   if n==0:w=[C.one if j==i else C.zero for j in range(rank)]
   else:
    b=pow(n,-1,15);j,sg=perm[b][i];w=[C(sg)*theta[k]**(-b)*lowS[j][k] for k in range(rank)]
   if not add([theta[k]**n*lowS[i][k] for k in range(rank)],w,['STnS',n,i]):break
  if failure:break
 def dependencies(columns):
  cb=[];ans=[];nn=len(columns)
  for j,v0 in enumerate(columns):
   v=list(v0);a=[C.one if j==k else C.zero for k in range(nn)]
   for p,bv,ba in cb:
    q=v[p]
    if q:v=[x-q*y for x,y in zip(v,bv)];a=[x-q*y for x,y in zip(a,ba)]
   p=next((k for k,x in enumerate(v) if x),None)
   if p is None:ans.append(a)
   else:
    q=v[p];cb.append((p,[x/q for x in v],[x/q for x in a]))
  return ans
 closure=[]
 while failure is None:
  oldbasis=list(basis);m=len(oldbasis);vv=[x[1] for x in oldbasis];ww=[x[2] for x in oldbasis]
  deps=dependencies(vv+[[theta[k]*v[k] for k in range(rank)] for v in vv])
  for di,co in enumerate(deps):
   aa=co[:m];bb=[-x for x in co[m:]]
   v=[theta[k]*sum((a*w[k] for a,w in zip(aa,ww)),C.zero) for k in range(rank)]
   w=[theta[k]**(-1)*sum((b*z[k] for b,z in zip(bb,ww)),C.zero) for k in range(rank)]
   if not add(v,w,['closure',len(closure),di]):break
   if not add(w,v,['closure_reverse',len(closure),di]):break
  closure.append({'before':m,'after':len(basis),'intersection_dimension':len(deps)});print('closure',rank,closure[-1],flush=True)
  if len(basis)==m:break
 checks={}
 if failure is None:
  checks['symmetric']=all(dot(v,ww)==dot(w,vv) for _,v,w in basis for _,vv,ww in basis)
  checks['isometric']=all(dot(v,[sigma(x,14) for x in vv])==dot(w,[sigma(x,14) for x in ww]) for _,v,w in basis for _,vv,ww in basis)
 known=[]
 if failure is None:
  from collections import defaultdict
  groups=defaultdict(list)
  for j,(v,t) in enumerate(zip(vs,theta)):groups[(v,str(t))].append(j)
  for indices in groups.values():
   v=[C.one if j in indices else C.zero for j in range(rank)];w=[C.zero]*rank
   for p,bv,bw in basis:
    q=v[p]
    if q:v=[x-q*y for x,y in zip(v,bv)];w=[x+q*y for x,y in zip(w,bw)]
   if not any(v):known.append({'indices':indices,'S_image':[list(map(str,z.to_list())) for z in w]})
 rec={'rank':rank,'solution':case['solution'],'known_span_rank':len(basis),'linear_failure':failure,'checks':checks,'closure':closure,'known_class_rows':known,'low_galois_permutations':perm,'basis':[{'pivot':p,'vector':[list(map(str,z.to_list())) for z in v],'image':[list(map(str,z.to_list())) for z in w]} for p,v,w in basis]};out.append(rec)
 print({k:v for k,v in rec.items() if k not in ('low_galois_permutations','known_class_rows','basis')},'seconds',time.monotonic()-st,flush=True)
 (here/'modular_closure.json').write_text(json.dumps(out,indent=2))
