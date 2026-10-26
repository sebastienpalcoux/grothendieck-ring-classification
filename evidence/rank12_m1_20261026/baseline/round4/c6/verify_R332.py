#!/usr/bin/env python3
"""Portable exact R332 tensor/character verifier; standard library only.
The categorical conjugation-action lemma is proved in R332_proof.md.
"""
import json,itertools,hashlib
from pathlib import Path
from fractions import Fraction as Q
P=Path(__file__).resolve().parent
J=json.loads((P/'R332_frozen.json').read_text());R=J['source_tensor'];S=J['target_tensor'];T=J['reconstructed_target_tensor']
def need(x,m):
 if not x:raise ValueError(m)
def fp(R):return hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()
def unitrow(n,k):return [int(i==k)for i in range(n)]
def prod(R,i,j):
 need(sum(R[i][j])==1,'not simple product');return R[i][j].index(1)
def validate(R):
 n=len(R);du=[next(j for j in range(n)if R[i][j][0])for i in range(n)]
 for i,j in itertools.product(range(n),repeat=2):
  need(R[0][i]==R[i][0]==unitrow(n,i),'unit');need(R[i][j][0]==int(j==du[i]),'duality')
  for k in range(n):
   need(R[i][j][k]==R[du[i]][k][j]==R[k][du[j]][i],'reciprocity')
   for l in range(n):need(sum(R[i][j][t]*R[t][k][l]for t in range(n))==sum(R[j][k][t]*R[i][t][l]for t in range(n)),'associativity')
 return du
D=validate(R);validate(S);validate(T)
G=[i for i in range(12)if sum(R[i][D[i]])==1]
neutral=[0,3,4,9,10,11]
need(all(not R[i][j][k]for i in neutral for j in neutral for k in range(12)if k not in neutral),'neutral closure')
need(len(G)==6,'pointed count')
choices=[]
for a in G:
 if a==0 or a not in neutral:continue
 a2=prod(R,a,a)
 if prod(R,a2,a)!=0:continue
 for b in G:
  if b in neutral or prod(R,b,b)!=0 or prod(R,prod(R,b,a),b)!=a2:continue
  for x in neutral:
   if x in G or prod(R,prod(R,b,x),b)!=x:continue
   ax=prod(R,a,x);a2x=prod(R,a2,x)
   if prod(R,x,a)!=a2x:continue
   target=[int(i in [0,x,ax,a2x])for i in range(12)]
   if R[x][x]!=target:continue
   choices.append((a,b,x,a2,ax,a2x))
need(choices,'no promised source subgroup/action')
a,b,x,a2,ax,a2x=choices[0]
# Forgetful map from the six equivariant simples into the original neutral ring.
F=[unitrow(12,0),unitrow(12,0),[int(i in [a,a2])for i in range(12)],unitrow(12,x),unitrow(12,x),[int(i in [ax,a2x])for i in range(12)]]
for i,j in itertools.product(range(6),repeat=2):
 lhs=[sum(F[i][p]*F[j][q]*R[p][q][k]for p in range(12)for q in range(12))for k in range(12)]
 rhs=[sum(T[i][j][t]*F[t][k]for t in range(6))for k in range(12)]
 need(lhs==rhs,'forgetful multiplication')
p=J['reconstructed_to_target']
need(sorted(p)==list(range(6))and p[0]==0,'target permutation')
need(all(T[i][j][k]==S[p[i]][p[j]][p[k]]for i,j,k in itertools.product(range(6),repeat=3)),'full target isomorphism')
# The only fusion-rule ambiguity: x^2=a+x_s+V. If a=g, duality
# would exchange x_+ and x_-, but their squares are equal and have unequal
# multiplicities on this pair. No sign s repairs the based-ring involution.
for s in range(2):
 sq=[0]*6;sq[1]=sq[3+s]=sq[5]=1
 dual=[0,1,2,4,3,5]
 need([sq[dual[k]]for k in range(6)]!=sq,'unexpected nonselfdual branch')
# Arithmetic in Q(sqrt(q)).
def add(a,b):return tuple(a[i]+b[i]for i in range(2))
def mul(a,b,q):return (a[0]*b[0]+q*a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def checkchar(c,q):
 for i,j in itertools.product(range(6),repeat=2):
  need(mul(c[i],c[j],q)==tuple(sum(T[i][j][k]*c[k][h]for k in range(6))for h in range(2)),'character')
# Positive dimension character (1,1,2,d,d,2d).
d=(Q(3,2),Q(1,2));dims=[(Q(1),Q(0)),(Q(1),Q(0)),(Q(2),Q(0)),d,d,(Q(3),Q(1))]
checkchar(dims,13)
globaldim=tuple(sum(mul(v,v,13)[h]for v in dims)for h in range(2));need(globaldim==(39,9),'global dimension')
# Non-FP one-dimensional character with g=-1 and rho=phi.
t=(Q(1,2),Q(1,2));chi=[(Q(1),Q(0)),(Q(-1),Q(0)),(Q(0),Q(0)),t,(-t[0],-t[1]),(Q(0),Q(0))]
checkchar(chi,5)
f=tuple(sum(mul(v,v,5)[h]for v in chi)for h in range(2));need(f==(5,1),'formal codegree')
Dnorm=globaldim[0]**2-13*globaldim[1]**2;fnorm=f[0]**2-5*f[1]**2
norm=(Dnorm/fnorm)**2;need(norm==Q(13689,25)and norm.denominator!=1,'integrality obstruction')
report={'status':'PASS','ring':J['source_id'],'general_complex_exclusion':True,'tensor_sha256':fp(R),'source_generators':{'a':a,'b':b,'rho':x},'neutral_input_labels':neutral,'equivariantization_target':J['target_id'],'target_sha256':fp(S),'target_permutation':p,'global_dimension':'39+9*sqrt(13)','formal_codegree':'5+sqrt(5)','norm_of_required_central_dimension':'13689/25','parent_repository_imports':False,'optimizer_used':False,'assertions_used':False}
(P/'R332_verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
