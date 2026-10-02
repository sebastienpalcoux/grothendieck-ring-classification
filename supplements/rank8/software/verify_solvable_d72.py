"""Exact premises of the dimension72 LPR24 module obstruction.
The categorical implication is proved in paper/solvable_proofs.tex.
Python standard library only; no assertions disabled by -O.
"""
import itertools,json,hashlib
from pathlib import Path

def require(b,msg='certificate condition failed'):
 if not b:raise ValueError(msg)

def verify_tensor(record, expected_tensor=None):
 N=record['tensor'];require(len(N)==8)
 if expected_tensor is not None:require(N==expected_tensor, 'external census mismatch')
 sha=hashlib.sha256(json.dumps(N,separators=(',',':')).encode()).hexdigest()
 require(sha==record['tensor_sha256'], 'tensor hash mismatch')
 p=record['proof_to_census'];require(sorted(p)==list(range(8)) and p[0]==0)
 T=[[[N[p[i]][p[j]][p[k]]for k in range(8)]for j in range(8)]for i in range(8)]
 require(all(type(v)is int and v>=0 for M in T for row in M for v in row))
 require(all(T[0][i][j]==T[i][0][j]==int(i==j)for i,j in itertools.product(range(8),repeat=2)))
 require(all(T[i][j]==T[j][i]for i,j in itertools.product(range(8),repeat=2)))
 require(all(sum(T[i][j][a]*T[a][k][l]for a in range(8))==sum(T[j][k][a]*T[i][a][l]for a in range(8))
             for i,j,k,l in itertools.product(range(8),repeat=4)), 'associativity')
 dual=[next(j for j in range(8)if T[i][j][0])for i in range(8)]
 require(dual==[0,1,2,4,3,5,6,7])
 inv=[i for i in range(8)if T[i][dual[i]]==[1]+[0]*7]
 require(inv==[0,1], 'invertible group notC2')
 dims=[1,1,2,3,3,4,4,4]
 require(sum(d*d for d in dims)==72)
 require(all(dims[i]*dims[j]==sum(T[i][j][k]*dims[k]for k in range(8))for i,j in itertools.product(range(8),repeat=2)))
 # The adjoint subring is all of T, excluding a final nontrivial extension step.
 ad={0}
 for i in range(8):ad.update(k for k,v in enumerate(T[i][dual[i]])if v)
 change=True
 while change:
  new=ad|{k for i,j in itertools.product(ad,repeat=2)for k,v in enumerate(T[i][j])if v}
  change=new!=ad;ad=new
 require(ad==set(range(8)), 'universal grading may be nontrivial')
 def expect(i,j,terms):
  require(T[i][j]==[terms.count(k)for k in range(8)],f'fusion premise {i},{j}')
 # proof order1,h,E,P,Q,W0,W1,W2
 expect(1,1,[0]);expect(1,2,[2]);expect(1,3,[4]);expect(1,4,[3]);expect(2,2,[0,1,2])
 expect(2,3,[3,4]);expect(2,4,[3,4]);expect(3,3,[1,2,3,4]);expect(4,4,[1,2,3,4]);expect(3,4,[0,2,3,4])
 for w in range(5,8):
  expect(1,w,[w]);expect(2,w,[v for v in range(5,8)if v!=w])
  expect(3,w,[5,6,7]);expect(4,w,[5,6,7])
 return dict(id=record['id'],status='PASS',scope='general noncategorification, subject to accompanying categorical proof',
             tensor_sha256=sha,proof_to_census=p,FPdim=72,adjoint_rank=8,
             invertible_group='C2',subring='LPR24',complement_module_rank=3)

def action_and_cohomology_checks():
 # V4=F2². J is a normalized C3-invariant nontrivial2cocycle.
 v=list(itertools.product(range(2),repeat=2));zero=(0,0)
 plus=lambda a,b:(a[0]^b[0],a[1]^b[1])
 J=lambda a,b:(a[0]*b[0]+a[0]*b[1]+a[1]*b[1])%2
 lam=lambda a:int(a!=zero)
 rot=lambda a:(a[1],a[0]^a[1])
 tau=lambda a:(a[1],a[0])
 require(all((J(a,b)+J(plus(a,b),c)-J(b,c)-J(a,plus(b,c)))%2==0 for a,b,c in itertools.product(v,repeat=3)))
 require(all(J(rot(a),rot(b))==J(a,b)for a,b in itertools.product(v,repeat=2)))
 require(all((J(a,b)+J(tau(a),tau(b)))%2==(lam(a)+lam(b)-lam(plus(a,b)))%2 for a,b in itertools.product(v,repeat=2)))
 require(all(lam(tau(a))==lam(a)for a in v))
 fixed=[a for a in v if a!=zero and tau(a)==a];require(len(fixed)==1)
 a=fixed[0];require(J(a,a)==lam(a)==1)
 # Both outeraction lifts have +1 on the fixed unit channel in X_±².
 # Twisted: equivariant scalar squared eta_a=-1; tensorator J(a,a)=-1.
 require((-1)**(J(a,a)+lam(a))==1)
 # Check the entire six-element action, not only its C2 restriction.
 ix={a:i for i,a in enumerate(v)}
 idperm=tuple(range(4));R=tuple(ix[rot(a)]for a in v);S=tuple(ix[tau(a)]for a in v)
 compose=lambda p,q:tuple(p[q[i]]for i in range(4))
 group={idperm};queue=[idperm]
 for g in queue:
  for t in(R,S):
   h=compose(g,t)
   if h not in group:group.add(h);queue.append(h)
 require(len(group)==6)
 parity=lambda g:sum(g[i]>g[j]for i in range(1,4)for j in range(i+1,4))%2
 tensorator=lambda g,a,b:parity(g)*J(a,b)
 comparison=lambda g,h,a:parity(g)*parity(h)*lam(a)
 for g,h in itertools.product(group,repeat=2):
  gh=compose(g,h)
  for a,b in itertools.product(v,repeat=2):
   left=tensorator(h,a,b)+tensorator(g,v[h[ix[a]]],v[h[ix[b]]])-tensorator(gh,a,b)
   right=comparison(g,h,a)+comparison(g,h,b)-comparison(g,h,plus(a,b))
   require((left-right)%2==0,'S3 comparison not monoidal')
 for g,h,k in itertools.product(group,repeat=3):
  for a in v:
   require((comparison(g,h,v[k[ix[a]]])+comparison(compose(g,h),k,a)-comparison(h,k,a)-comparison(g,compose(h,k),a))%2==0,
           'S3 action coherence')
 # EveryH3(V4,C*)class is represented by one of these8normalizedcocycles.
 # Kunneth gives group order8; distinct restriction triples certify them all.
 restrictions=[]
 for p,q,r in itertools.product(range(2),repeat=3):
  omega=lambda a,b,c:(p*a[0]*b[0]*c[0]+q*a[1]*b[1]*c[1]+r*a[1]*b[0]*c[0])%2
  require(all((omega(b,c,d)-omega(plus(a,b),c,d)+omega(a,plus(b,c),d)-omega(a,b,plus(c,d))+omega(a,b,c))%2==0
              for a,b,c,d in itertools.product(v,repeat=4)))
  restrictions.append(tuple(omega(a,a,a)for a in v if a!=zero))
 require(len(set(restrictions))==8)
 require([x for x in restrictions if len(set(x))==1]==[(0,0,0),(1,1,1)])
 # Six2D objects divide into twoC3orbits. Possible X-actionconstant blocks.
 # FPdimension forcesblockrow sums1; selfduality enforces symmetry.
 possible=[]
 for a,b,d in itertools.product(range(2),repeat=3):
  if a+b!=1 or b+d!=1:continue
  B=[[a,b],[b,d]]
  if all(3*sum(B[i][k]*B[k][j]for k in range(2))==int(i==j)+2*B[i][j]
         for i,j in itertools.product(range(2),repeat=2)):possible.append(B)
 require(possible==[[[1,0],[0,1]]])
 # Independently enumerate A4 subgroups and their K\A4/H double cosets.
 perms=list(itertools.permutations(range(4)))
 A4=[p for p in perms if sum(p[i]>p[j]for i in range(4)for j in range(i+1,4))%2==0]
 identity=tuple(range(4))
 inv=lambda g:tuple(g.index(i)for i in range(4))
 cyclic=lambda g:frozenset((identity,g,compose(g,g)))
 K=cyclic((1,2,0,3));require(len(K)==3)
 subgroups=[]
 for mask in range(1<<12):
  H=frozenset(A4[i]for i in range(12)if mask>>i&1)
  if identity not in H:continue
  if all(compose(g,h)in H for g,h in itertools.product(H,repeat=2)):subgroups.append(H)
 admissible=[]
 for H in subgroups:
  if len(H)%2==0:
   require(any(g!=identity and compose(g,g)==identity for g in H))
   continue # Omega restricts nontrivially to every order2 subgroup.
  require(len(H)in(1,3))
  left=set(A4);intersections=[]
  while left:
   g=min(left)
   dc={compose(compose(k,g),h)for k,h in itertools.product(K,H)}
   left-=dc
   intersection=K&{compose(compose(g,h),inv(g))for h in H}
   require(len(intersection)in(1,3))
   intersections.append(len(intersection))
  require(sum(intersections)==4)
  admissible.append(dict(subgroup_order=len(H),intersection_orders=sorted(intersections),module_rank=4))
 require(len(admissible)==5 and sum(x['subgroup_order']==1 for x in admissible)==1)
 return dict(status='PASS',action_unit_channel_sign=1,S3_monoidality_checks=576,S3_coherence_checks=864,cohomology_restrictions=restrictions,A4_admissible_module_ranks=admissible,rank_divisibility_contradiction='4 does not divide 10',
             permitted_X_blocks=possible,scope='finite algebraic premises, not a replacement for cited categorical structure theorems')

if __name__=='__main__':
 records=json.loads((Path(__file__).resolve().parents[1]/'data/solvable_d72_certificates.json').read_text())
 require([r['id']for r in records]==['R8_1_45','R8_1_47'])
 print(json.dumps(dict(cases=[verify_tensor(r)for r in records],auxiliary=action_and_cohomology_checks()),indent=2))
