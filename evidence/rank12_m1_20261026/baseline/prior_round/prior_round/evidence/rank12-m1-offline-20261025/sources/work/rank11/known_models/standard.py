"""Known unitary model construction and exact rank-eleven tensor matches.

All identities checked over integers. The fusion ring equality does not replace
categorical existence proofs; references and admissibility are in THEORY.md.
"""
from pathlib import Path
import sys,json,gzip,itertools,collections,hashlib
ROOT=Path(__file__).resolve().parents[3];HERE=Path(__file__).parent
sys.path.insert(0,str(ROOT/'work/models'));sys.path.insert(0,str(ROOT/'work/root_models'))
from match_models import based_iso,tensor_hash,coarse,group,ty,su2,rep_dihedral
from extra_models import metaplectic,auts,abelian_table,dihedral_table,dicyclic_table,pointed_equivariant
from zest_models import gradings,zest
from construct import half_even_metaplectic
def cyclic_equivariant(R,sigma,m,parity=None):
 # Exact cyclotomic Fourier projection, with no symbolic exponential heuristics.
 import sympy as sp
 n=len(R);parity=parity or [0]*n;seen=set();labs=[]
 for a in range(n):
  if a in seen:continue
  O=[];b=a
  while b not in O:O.append(b);b=sigma[b]
  if b!=a or m%len(O):raise ValueError('cyclic action')
  seen.update(O)
  for j in range(m//len(O)):labs.append((O,j))
 powers=[list(range(n))]
 for _ in range(1,m):powers.append([sigma[powers[-1][a]]for a in range(n)])
 x=sp.Symbol('x');phi=[int(v)for v in reversed(sp.Poly(sp.cyclotomic_poly(2*m,x),x).all_coeffs())];deg=len(phi)-1
 r=len(labs);T=[[[0]*r for _ in range(r)]for _ in range(r)]
 for i,(A,ja)in enumerate(labs):
  for j,(B,jb)in enumerate(labs):
   for k,(C,jc)in enumerate(labs):
    c=C[0];lc=len(C);co=[0]*(2*m)
    for h in range(0,m,lc):
     tr=sum(R[a][b][c]for a in A for b in B if powers[h][a]==a and powers[h][b]==b)
     co[((2*(ja+jb-jc)+parity[A[0]]+parity[B[0]]-parity[C[0]])*h)%(2*m)]+=tr
    for d in range(2*m-1,deg-1,-1):
     q=co[d]
     for t,v in enumerate(phi):co[d-deg+t]-=q*v
    divisor=m//lc
    if any(co[1:])or co[0]<0 or co[0]%divisor:raise ValueError('nonintegral Fourier projection')
    T[i][j][k]=co[0]//divisor
 return T,labs

def so8_level2():
 # Section3.3 of GRR, N=8: invertibles1,h,g,hg; X0;
 # and three pairs V1,V2;W1,W2;Y0,Y1, stabilizersh,g,hg.
 n=11;T=[[[0]*n for _ in range(n)]for _ in range(n)]
 for a,b in itertools.product(range(4),repeat=2):T[a][b][a^b]=1
 for a in range(4):T[a][4][4]=T[4][a][4]=T[4][4][a]=1
 for q,s in enumerate([1,2,3]):
  labs=[5+2*q,6+2*q]
  for a in range(4):
   for e in range(2):T[a][labs[e]][labs[e^int(a not in(0,s))]]=T[labs[e]][a][labs[e^int(a not in(0,s))]]=1
  for e,f in itertools.product(range(2),repeat=2):
   T[4][labs[e]][labs[f]]=T[labs[e]][4][labs[f]]=1
   T[labs[e]][labs[f]][4]=1
   for a in range(4):
    if int(a not in(0,s))==(e^f):T[labs[e]][labs[f]][a]=1
 for q,r in itertools.combinations(range(3),2):
  t=3-q-r
  for e,f,h in itertools.product(range(2),repeat=3):T[5+2*q+e][5+2*r+f][5+2*t+h]=T[5+2*r+f][5+2*q+e][5+2*t+h]=1
 return T

def ty_abelian_equivariants():
 # Additional orthogonal involutions of noncyclic metric groups.
 for orders,mod,forms in [
   ((3,3),3,[(a,b,c)for a,b,c in itertools.product(range(3),repeat=3)if(a*c-b*b)%3]),
   ((3,2,2),6,[(a,b,c)for a,b,c in itertools.product(range(2),repeat=3)if(a*c-b*b)%2])]:
  G=abelian_table(orders);els=list(itertools.product(*(range(a)for a in orders)));m=len(G);R=ty(orders)
  for sigma0 in auts(G):
   if not all(sigma0[sigma0[i]]==i for i in range(m)):continue
   sigma=sigma0+[m];f=sum(sigma[a]==a for a in range(m+1))
   if(m+1+3*f)//2!=11:continue
   chi=None
   for a,b,c in forms:
    if orders==(3,3):C=[[(a*x[0]*y[0]+b*(x[0]*y[1]+x[1]*y[0])+c*x[1]*y[1])%3 for y in els]for x in els]
    else:C=[[(2*x[0]*y[0]+3*(a*x[1]*y[1]+b*(x[1]*y[2]+x[2]*y[1])+c*x[2]*y[2]))%6 for y in els]for x in els]
    if all(C[sigma0[i]][sigma0[j]]==C[i][j]for i,j in itertools.product(range(m),repeat=2)):chi=C;break
   if chi is None:continue
   for parity in [0,1]:
    pp=[0]*m+[parity];T,labs=cyclic_equivariant(R,sigma,2,pp)
    yield 'TY('+str(orders)+f')^C2[sigma={sigma0}, eta_m={(-1)**parity}]',T,'ty_cyclic_equivariant',{'orders':orders,'automorphism':sigma,'group_order':2,'parity':pp,'labels':labs,'bicharacter_modulus':mod,'bicharacter_exponents':chi},'Orthogonal automorphism of the explicit nondegenerate symmetric TY bicharacter; either natural parity coherence is unitary',False

def targets():
 return {f'R11_1_{i}':json.loads(s.replace('{','[').replace('}',']')) for i,s in enumerate(gzip.open(ROOT/'repositories/fusion-ring-census/results/rank11/tables.txt.gz','rt'),1)if s.strip()}

def standard():
 yield 'Vec(C11)',group((11,)),'pointed',{'orders':[11]},'EGNO, Tensor Categories, pointed fusion categories',False
 yield 'TY(C10)',ty((10,)),'ty',{'orders':[10]},'Tambara--Yamagami, J. Algebra 209 (1998), Theorem 1; bicharacter exp(2pi i ab/10), positive tau',False
 for k,even in [(10,False),(20,True),(21,True)]:
  yield ('PSU'if even else 'SU')+f'(2)_{k}',su2(k,even),'su2',{'level':k,'even':even},'Standard unitary SU(2) level k category and even fusion subcategory',True
 for m,dic in [(16,False),(16,True),(19,False)]:
  yield f'Rep({"Dic"+str(m//2)if dic else "D"+str(2*m)})',rep_dihedral(m,dic),'rep_dihedral',{'m':m,'dicyclic':dic},'Ordinary unitary complex representations of the displayed finite group',True
 yield 'SO(15)_2',metaplectic(15),'odd_metaplectic',{'N':15},'Standard unitary SO(15) level 2 category; Ardonne--Cheng--Rowell--Wang, Classification of metaplectic modular categories',True
 yield 'SO(8)_2',so8_level2(),'even_metaplectic',{'N':8},'Gustafson--Rowell--Ruan, Metaplectic Categories, Gauging and Property F, Section 3.3, arXiv:1808.00698',True
 T,L=half_even_metaplectic(24)
 yield 'Half SO(24)_2',T,'half_even_metaplectic',{'N':24,'labels':L},'Gustafson--Rowell--Ruan, Metaplectic Categories, Gauging and Property F, Section 3.3, arXiv:1808.00698',True
 # Strict C2 actions on pointed categories. Every parameter is explicit.
 gs=[('C16',abelian_table((16,))),('C8xC2',abelian_table((8,2))),('C4xC4',abelian_table((4,4))),('C4xC2xC2',abelian_table((4,2,2))),('C2^4',abelian_table((2,2,2,2))),('D16',dihedral_table(8)),('Q16',dicyclic_table(4)),('C19',abelian_table((19,)))]
 for name,G in gs:
  seen=set()
  for sigma in auts(G):
   if not all(sigma[sigma[i]]==i for i in range(len(G))):continue
   f=sum(sigma[i]==i for i in range(len(G)))
   if(len(G)+3*f)//2!=11:continue
   T=pointed_equivariant(G,sigma);h=tensor_hash(T)
   if h in seen:continue
   seen.add(h)
   yield f'Vec({name})^C2[{sigma}]',T,'pointed_equivariant',{'group_name':name,'group_table':G,'automorphism':sigma},'Strict group-automorphism action on Vec(G), followed by unitary equivariantization',all(G[a][b]==G[b][a]for a,b in itertools.product(range(len(G)),repeat=2))
 # TY(C12) orthogonal involutions, including either parity coherence.
 for m in [12,15]:
  R=ty((m,))
  for u in range(1,m):
   if(u*u-1)%m:continue
   sigma=[u*a%m for a in range(m)]+[m];f=sum(sigma[a]==a for a in range(m+1))
   if (m+1+3*f)//2!=11:continue
   for parity in [0,1]:
    pp=[0]*m+[parity];T,labs=cyclic_equivariant(R,sigma,2,pp)
    yield f'TY(C{m})^C2[u={u}, eta_m={(-1)**parity}]',T,'ty_cyclic_equivariant',{'orders':[m],'automorphism':sigma,'group_order':2,'parity':pp,'labels':labs},'Canonical orthogonal automorphism of the standard TY skeleton; either natural parity coherence is unitary',False
 yield from ty_abelian_equivariants()
 # The cyclic coordinate permutation preserves chi(x,y)=(-1)^(x dot y)
 # and the braided TY quadratic refinement q(x)=i^weight(x).
 els=list(itertools.product(range(2),repeat=3));sigma=[els.index((b,c,a))for a,b,c in els]+[8]
 T,labs=cyclic_equivariant(ty((2,2,2)),sigma,3)
 yield 'TY(C2^3)^C3, coordinate cycle',T,'ty_cyclic_equivariant',{'orders':[2,2,2],'automorphism':sigma,'group_order':3,'parity':[0]*9,'labels':labs,'bicharacter_modulus':2,'bicharacter_exponents':[[sum(a*b for a,b in zip(x,y))%2 for y in els]for x in els],'braided_quadratic_exponents_mod4':[sum(x)%4 for x in els]},'Braided TY category with chi(x,y)=(-1)^(x dot y), q(x)=i^weight(x); strict C3 action by coordinate cycle preserves the associator and braiding',True

def validate(T):
 n=len(T)
 if n!=11:return False
 if max(x for a in T for b in a for x in b)>1:return False
 for i,j,k,l in itertools.product(range(n),repeat=4):
  if sum(T[i][j][x]*T[x][k][l]for x in range(n))!=sum(T[j][k][x]*T[i][x][l]for x in range(n)):raise ValueError('nonassociative model')
 if not all(T[0][i][j]==T[i][0][j]==int(i==j)for i,j in itertools.product(range(n),repeat=2)):raise ValueError('unit')
 return True

def main():
 data=targets();buckets=collections.defaultdict(list)
 for rid,R in data.items():buckets[coarse(R)].append((rid,R))
 out=collections.defaultdict(list);attempt=[];seen=set()
 for name,T,kind,par,ref,braided in standard():
  variants=[(name,T,kind,par,ref)]
  if braided:
   for g in gradings(T):
    for h in range(1,len(T)):
     if g[h] or T[h][h][0]!=1 or sum(T[h][h])!=1:continue
     if not all(T[h][i]==T[i][h]and sum(T[h][i])==1 for i in range(len(T))):continue
     U=zest(T,g,h)
     variants.append((f'C2-zest({name};h={h},grading={g})',U,'associative_C2_zest',{'base_name':name,'base_constructor':kind,'base_parameters':par,'base_tensor':T,'grading':g,'central_invertible':h},ref+'; Delaney--Galindo--Plavnik--Rowell--Zhang, braided zesting, associative construction'))
  for name,T,kind,par,ref in variants:
   h=tensor_hash(T)
   if h in seen:continue
   seen.add(h)
   if not validate(T):continue
   matches=[]
   for rid,R in buckets[coarse(T)]:
    p=based_iso(R,T)
    if p is None:continue
    out[rid].append({'name':name,'constructor':kind,'parameters':par,'reference':ref,'model_tensor':T,'basis_map_source_to_model':p})
    matches.append(rid)
   attempt.append({'name':name,'constructor':kind,'matches':matches,'model_tensor_sha256':h})
   print(name, matches,flush=True)
 rows=[{'id':rid,'tensor_sha256':tensor_hash(data[rid]),'status':'unitarily_realized','models':models}for rid,models in sorted(out.items(),key=lambda kv:int(kv[0].split('_')[-1]))]
 (HERE/'standard_models.json').write_text(json.dumps(rows,indent=2)+'\n');(HERE/'standard_attempts.json').write_text(json.dumps(attempt,indent=2)+'\n')
 print('TOTAL',len(rows),[x['id']for x in rows],flush=True)
if __name__=='__main__':main()
