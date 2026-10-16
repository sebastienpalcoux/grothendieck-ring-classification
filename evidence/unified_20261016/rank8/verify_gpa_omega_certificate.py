"""Exact primitive-rotation obstruction; standard-library arithmetic only."""
import importlib.util
base_spec=importlib.util.spec_from_file_location("_gpa_base_for_rotation",__import__("pathlib").Path(__file__).with_name("verify_gpa_certificate.py"))
v=importlib.util.module_from_spec(base_spec)
base_spec.loader.exec_module(v)
from fractions import Fraction as F
import json,hashlib
from pathlib import Path
P=Path(__file__).parent
# Extend K=Q(sqrt5) by omega²+omega+1=0.
a5,m5,n5,i5,q5=v.add,v.mul,v.neg,v.inv,v.q
Z5=v.Z;O5=v.O;R5=v.R
Z=(Z5,Z5);O=(O5,Z5);R=(R5,Z5);OM=(Z5,O5)
def add(a,b):return(a5(a[0],b[0]),a5(a[1],b[1]))
def neg(a):return(n5(a[0]),n5(a[1]))
def sub(a,b):return add(a,neg(b))
def mul(a,b):
 p=m5(a[1],b[1]);return(a5(m5(a[0],b[0]),n5(p)),a5(a5(m5(a[0],b[1]),m5(a[1],b[0])),n5(p)))
def inv(a):
 norm=a5(a5(m5(a[0],a[0]),n5(m5(a[0],a[1]))),m5(a[1],a[1]));ni=i5(norm);return(m5(a5(a[0],n5(a[1])),ni),n5(m5(a[1],ni)))
def q(a):return(q5(a),Z5)
def div(a,b):return mul(a,inv(b))
for name in ['Z','O','R','add','neg','sub','mul','inv','q','div']:setattr(v,name,globals()[name])
adj={0:[1],1:[0,2],2:[1,3,4],3:[2,5],4:[2,5],5:[3,4,6],6:[5,7],7:[6]};d=add(q(2),R);D=add(q(3),R);phi=div(add(O,R),q(2));w={0:O,1:O,2:d,3:phi,4:phi,5:d,6:O,7:O};even=[0,2,5,7]
def loops(n):
 out=[]
 def go(p):
  if len(p)==n:
   if p[0] in adj[p[-1]]:out.append(tuple(p))
  else:
   for x in adj[p[-1]]:go(p+[x])
 for x in even:go([x])
 return out
L=loops(6);idx={l:i for i,l in enumerate(L)};constraints=[]
for l in loops(4):
 for k in [1,2]:
  vv=l[k-1];constraints.append({idx[l[:k]+(n,vv)+l[k:]]:O for n in adj[vv]})
for l in L:
 r=l[-2:]+l[:-2];c=mul(OM,div(mul(w[l[0]],w[l[5]]),mul(w[l[2]],w[l[1]])));row={idx[r]:O};i=idx[l];row[i]=sub(row.get(i,Z),c);constraints.append({k:z for k,z in row.items() if z!=Z})
echelon={}
for row in constraints:
 row=dict(row)
 while row:
  j=min(row)
  if j not in echelon:
   z=inv(row[j]);echelon[j]={i:mul(c,z) for i,c in row.items()};break
  c=row[j]
  for i,z in echelon[j].items():
   t=sub(row.get(i,Z),mul(c,z))
   if t!=Z:row[i]=t
   elif i in row:del row[i]
free=[i for i in range(152) if i not in echelon];B=[[Z]*len(free) for _ in L]
for j,i in enumerate(free):B[i][j]=O
for i in sorted(echelon,reverse=True):
 B[i]=[neg(v.sumq(mul(z,B[k][j]) for k,z in echelon[i].items() if k!=i)) for j in range(len(free))]
X=[tuple(int(i==j) for i in range(8)) for j in range(8)];V=[{X[j]:z for j,z in enumerate(row) if z!=Z} for row in B];eq=[];seen=set()
for st in even:
 for en in [1,3,4,6]:
  paths=sorted({l[:4] for l in L if l[0]==st and l[3]==en});n=len(paths)
  if not n:continue
  Es=[]
  for h in [1,2]:
   E=[[Z]*n for _ in range(n)]
   for i,p in enumerate(paths):
    if p[h-1]!=p[h+1]:continue
    for j,t in enumerate(paths):
     if all(p[a]==t[a] for a in range(4) if a!=h):E[i][j]=div(w[p[h]],v.sumq(w[a] for a in adj[p[h-1]]))
   Es.append(E)
  E,Fm=Es;EF=v.mm(E,Fm);FE=v.mm(Fm,E);I=v.ident(n);factor=div(D,d);f=[[add(I[i][j],mul(factor,sub(add(EF[i][j],FE[i][j]),add(E[i][j],Fm[i][j])))) for j in range(n)] for i in range(n)];T=[[V[idx[p+t[-2:0:-1]]] for t in paths] for p in paths]
  for i in range(n):
   for j in range(n):
    pol={}
    for h in range(n):pol=v.padd(pol,v.pmul(T[i][h],T[h][j]))
    if f[i][j]!=Z:pol=v.padd(pol,{v.M0:neg(f[i][j])})
    if pol:
     pol=v.norm(pol);key=v.key(pol)
     if key not in seen:seen.add(key);eq.append(pol)

# Replay a constant combination of five generated quadratic equations.
raw=(P/'gpa_omega_certificate.json').read_bytes();certificate=json.loads(raw)
v.req(len(echelon)==certificate['expected_rank']==144,'primitive rotation rank')
v.req(free==certificate['free_loop_indices'],'primitive rotation coordinates')
v.req(len(eq)==certificate['equation_count']==90,'primitive rotation equation count')
answer={}
for term in certificate['constant_contradiction']:
 a,b,c,d=map(F,term['coefficient']);coefficient=((a,b),(c,d));answer=v.padd(answer,v.scale(eq[term['equation']],coefficient))
v.req(answer=={v.M0:O},'five-equation constant contradiction')
print(json.dumps({'status':'PASS','field':'Q(sqrt(5),omega), omega^2+omega+1=0','loop_coordinates':152,'linear_constraint_rank':144,'dimension':8,'square_equations':90,'constant_contradiction_terms':len(certificate['constant_contradiction']),'identity':'sum coefficient_i*(T^2-f3 equation_i)=1','both_primitive_cube_roots_excluded':True,'self_adjointness_imposed':False,'certificate_sha256':hashlib.sha256(raw).hexdigest()},indent=2))
