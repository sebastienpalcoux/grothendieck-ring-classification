"""Portable exact complex 2D2 generator certificate, Python standard library only.

Input data are rational pairs a+b*sqrt(5), and sparse polynomials. No floating
point, numerical solver, conjugation equation or source notebook is used.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse,json,hashlib
Z=(F(0),F(0));O=(F(1),F(0));R=(F(0),F(1));NM=8;M0=(0,)*NM

def q(v):return (F(v),F(0))
def add(a,b):return (a[0]+b[0],a[1]+b[1])
def neg(a):return (-a[0],-a[1])
def sub(a,b):return add(a,neg(b))
def mul(a,b):return (a[0]*b[0]+5*a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def inv(a):
 d=a[0]*a[0]-5*a[1]*a[1]
 if not d:raise ValueError('division by zero')
 return (a[0]/d,-a[1]/d)
def div(a,b):return mul(a,inv(b))
def dec(a):return tuple(map(F,a))
def req(ok,msg):
 if not ok:raise ValueError(msg)
def padd(a,b):
 c=dict(a)
 for m,v in b.items():
  w=add(c.get(m,Z),v)
  if w!=Z:c[m]=w
  elif m in c:del c[m]
 return c
def scale(a,c):return {m:mul(v,c) for m,v in a.items() if mul(v,c)!=Z}
def shift(a,m):return {tuple(i+j for i,j in zip(k,m)):v for k,v in a.items()}
def pmul(a,b):
 c={}
 for m,v in a.items():
  for n,w in b.items():
   h=tuple(i+j for i,j in zip(m,n));c[h]=add(c.get(h,Z),mul(v,w))
 return {m:v for m,v in c.items() if v!=Z}
def pd(a):return {tuple(t['m']):dec(t['c']) for t in a if dec(t['c'])!=Z}
def norm(a):return scale(a,inv(a[max(a)])) if a else {}
def key(a):return tuple(sorted(a.items()))
def reduce(a,gg):
 a=dict(a);rem={}
 while a:
  m=max(a);v=a[m]
  for g in gg:
   n=max(g)
   if all(i>=j for i,j in zip(m,n)):
    h=tuple(i-j for i,j in zip(m,n));a=padd(a,scale(shift(g,h),neg(div(v,g[n]))));break
  else:rem[m]=v;del a[m]
 return rem

def ident(n):return [[O if i==j else Z for j in range(n)] for i in range(n)]
def mm(A,B):
 return [[sumq(mul(A[i][k],B[k][j]) for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def sumq(it):
 a=Z
 for b in it:a=add(a,b)
 return a

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--certificate',type=Path,default=Path(__file__).with_name('gpa_certificate.json'));args=ap.parse_args();raw=args.certificate.read_bytes();data=json.loads(raw)
 adj={i:[] for i in range(8)}
 for a,b in data['graph_edges']:adj[a].append(b);adj[b].append(a)
 for v in adj:adj[v].sort()
 ev=[0,2,5,7];req(data['even_vertices']==ev,'even vertices')
 d=add(q(2),R);D=add(q(3),R);phi=div(add(O,R),q(2));w={0:O,1:O,2:d,3:phi,4:phi,5:d,6:O,7:O}
 def loops(n):
  out=[]
  def go(p):
   if len(p)==n:
    if p[0] in adj[p[-1]]:out.append(tuple(p))
   else:
    for v in adj[p[-1]]:go(p+[v])
  for v in ev:go([v])
  return out
 L=loops(6);req(L==[tuple(v) for v in data['loop_basis']],'complete loop basis');idx={v:i for i,v in enumerate(L)};B=[[dec(v) for v in row] for row in data['linear_basis']];req(len(B)==152 and all(len(r)==8 for r in B),'linear basis size')
 piv=data['coordinate_loop_indices'];req(len(piv)==8,'coordinate count');req([B[i] for i in piv]==ident(8),'coordinate normalization')
 constraints=[]
 for l in loops(4):
  for k in [1,2]:
   v=l[k-1];constraints.append({idx[l[:k]+(n,v)+l[k:]]:O for n in adj[v]})
 for l in L:
  c=div(mul(w[l[0]],w[l[5]]),mul(w[l[2]],w[l[1]]));r=l[-2:]+l[:-2];row={idx[r]:O};i=idx[l];row[i]=sub(row.get(i,Z),c);constraints.append({k:v for k,v in row.items() if v!=Z})
 for row in constraints:
  req(all(sumq(mul(c,B[i][j]) for i,c in row.items())==Z for j in range(8)),'caps or rotation')
 echelon={}
 for row in constraints:
  row=dict(row)
  while row:
   j=min(row)
   if j not in echelon:
    z=inv(row[j]);echelon[j]={i:mul(v,z) for i,v in row.items()};break
   c=row[j]
   for i,v in echelon[j].items():
    z=sub(row.get(i,Z),mul(c,v))
    if z!=Z:row[i]=z
    elif i in row:del row[i]
 req(len(echelon)==144,'dimension 8 exhaustiveness')
 X=[tuple(int(i==j) for i in range(NM)) for j in range(NM)];V=[{X[j]:v for j,v in enumerate(row) if v!=Z} for row in B]
 G=[pd(p) for p in data['normal_form']];eq=[pd(p) for p in data['quadratic_equations']]
 actual=set();all_entries=0;blocks=0
 # T(1)=A+sqrt(c) C. c=(5 sqrt(5)-11)/2 is positive.
 k=div(sub(q(3),R),q(2));base=[neg(O),neg(mul(k,k)),Z,Z,neg(mul(div(sub(R,O),q(2)),k)),Z,Z,k];rad=[Z,Z,q(-2),q(-2),Z,O,O,Z]
 winding=lambda l:sum(1 if (a,b)==(3,5) else -1 if (a,b)==(5,3) else 0 for a,b in zip(l,l[1:]+l[:1]))
 winds=[winding(L[i]) for i in piv]
 req(winds==[0,0,1,-1,0,1,-1,0],'free coordinates have primitive opposite gauge weights')
 c=div(sub(mul(q(5),R),q(11)),q(2))
 expected=[{X[0]:O,X[7]:div(add(q(3),R),q(2))},{X[1]:O,X[7]:k},{X[2]:O,X[5]:q(2)},{X[3]:O,X[6]:q(2)},{X[4]:O,X[7]:div(sub(R,O),q(2))},{tuple(a+b for a,b in zip(X[5],X[6])):O,M0:neg(c)},{tuple(2*a for a in X[7]):O,M0:neg(mul(k,k))}]
 req(G==expected,'normal form matches stated two-family equations')
 req(c!=Z and k!=Z,'parameters nonzero')
 # Substitute each sign of x_j=epsilon*(base_j+rad_j*q*lambda^wind_j),
 # in the Laurent ring K[lambda,+/-q]/(q^2-c).
 def lmul(a,b):
  out={}
  for (u,v),av in a.items():
   for (h,j),bv in b.items():
    power=v+j;z=mul(av,bv)
    if power>=2:z=mul(z,c);power-=2
    key=(u+h,power);out[key]=add(out.get(key,Z),z)
  return {key:z for key,z in out.items() if z!=Z}
 for eps in [O,neg(O)]:
  values=[]
  for j in range(8):
   value={}
   if base[j]!=Z:value[(0,0)]=mul(eps,base[j])
   if rad[j]!=Z:value[(winds[j],1)]=mul(eps,rad[j])
   values.append(value)
  for g in G:
   value={}
   for mon,coef in g.items():
    term={(0,0):coef}
    for j,power in enumerate(mon):
     for _ in range(power):term=lmul(term,values[j])
    for monkey,z in term.items():value[monkey]=add(value.get(monkey,Z),z)
   req(all(z==Z for z in value.values()),'both full Laurent parameter families satisfy the ideal')
 for l,row in zip(L,B):req(all(v==Z or winding(l)==winds[j] for j,v in enumerate(row)),'edge-character gauge covariance')
 for st in ev:
  for en in [1,3,4,6]:
   paths=sorted({l[:4] for l in L if l[0]==st and l[3]==en});n=len(paths)
   if not n:continue
   blocks+=1;Es=[]
   for h in [1,2]:
    E=[[Z]*n for _ in range(n)]
    for i,p in enumerate(paths):
     if p[h-1]!=p[h+1]:continue
     for j,t in enumerate(paths):
      if all(p[a]==t[a] for a in range(4) if a!=h):E[i][j]=div(w[p[h]],sumq(w[a] for a in adj[p[h-1]]))
    Es.append(E)
   E,Fm=Es;EF=mm(E,Fm);FE=mm(Fm,E);I=ident(n);factor=div(D,d)
   f=[[add(I[i][j],mul(factor,sub(add(EF[i][j],FE[i][j]),add(E[i][j],Fm[i][j])))) for j in range(n)] for i in range(n)]
   req(mm(E,E)==E and mm(Fm,Fm)==Fm and mm(f,f)==f,'TL/JW idempotents');req(all(v==Z for row in mm(E,f)+mm(Fm,f) for v in row),'JW caps')
   rows=[[idx[p+t[-2:0:-1]] for t in paths] for p in paths];T=[[V[h] for h in row] for row in rows]
   for i in range(n):
    for j in range(n):
     poly={}
     for h in range(n):poly=padd(poly,pmul(T[i][h],T[h][j]))
     if f[i][j]!=Z:poly=padd(poly,{M0:neg(f[i][j])})
     if poly:actual.add(key(norm(poly)))
     req(not reduce(poly,G),'normal form implies original square equations');all_entries+=1
     for vals in [base,rad]:
      tij=sumq(mul(a,b) for a,b in zip(B[rows[i][j]],vals));tji=sumq(mul(a,b) for a,b in zip(B[rows[j][i]],vals));hi=mul(w[paths[i][1]],w[paths[i][2]]);hj=mul(w[paths[j][1]],w[paths[j][2]])
      req(mul(tij,hj)==mul(tji,hi),'base spherical self-adjointness')
 req(actual==set(key(p) for p in eq),'stored equations equal generated equations')
 req(len(G)==len(data['certificates'])==7,'normal form count')
 for g,certificate in zip(G,data['certificates']):
  answer={}
  for term in certificate:
   h=M0 if term['multiplier']==-1 else X[term['multiplier']];answer=padd(answer,scale(shift(eq[term['equation']],h),dec(term['coefficient'])))
  req(answer==g,'ideal consequence certificate')
 print(json.dumps({'status':'PASS','field':'Q(sqrt(5))','loop_coordinates':len(L),'linear_constraint_rank':len(echelon),'dimension':8,'path_matrix_blocks':blocks,'square_entries_checked':all_entries,'distinct_square_equations':len(eq),'normal_form_generators':len(G),'all_complex_ideal_equality':True,'self_adjointness_imposed':False,'self_adjoint_base_verified':True,'complex_edge_gauge_verified':True,'two_full_Laurent_families_verified':True,'primitive_opposite_free_gauge_weights_verified':True,'certificate_sha256':hashlib.sha256(raw).hexdigest(),'scope':'rotation-1 uncappable complex T with T^2=f3; categorical bridge and other rotations are separate'},indent=2))

if __name__=='__main__':main()
