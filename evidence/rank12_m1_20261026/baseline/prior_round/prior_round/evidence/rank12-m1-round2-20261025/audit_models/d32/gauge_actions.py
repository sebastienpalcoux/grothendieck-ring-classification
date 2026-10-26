"""Exact linear categorical-action equations on explicit Liptrap categories.

No search for associators: all starting associators are reconstructed by
Liptrap Lemma5.4. Only scalar tensorators and coherent involutive squares
are solved over finite roots of unity. Failed solves make no exclusion.
"""
from pathlib import Path
import collections,itertools,json,sys,time
import numpy as np
HERE=Path(__file__).resolve().parent;BASE=HERE.parents[2]/'rank12-m1-offline-20261025'
sys.path.insert(0,str(BASE));sys.path.insert(0,str(BASE/'sources/work/rank11'))
import common
from feudal import prime_power_solve
from ising_equivariants import maps,chars

def reconstructed(R,c,q):
 S=set(c['serfs']);M=c['lords'];du=common.dual(R);X={tuple(v[:-1]):v[-1]*(q//c['modulus'])for v in c['phase_values']}
 mul=lambda a,b:R[a][b].index(1)
 def v(f,a,b,m):return X.get((f,a,b,m),0)
 def tau(m):return X.get(('tau',m),0)
 def alpha(a,b,d):
  m=M[0]
  return(-v('upsilon',b,d,mul(du[a],m))+v('upsilon',mul(a,b),d,m)-v('upsilon',a,mul(b,d),m)+v('upsilon',a,b,m))%q
 def alpha1(a,b,m):return-v('upsilon',a,b,du[mul(m,du[mul(a,b)])])%q
 def beta1(a,b,m):return(alpha(du[b],a,mul(du[a],b))-v('upsilon',du[b],a,mul(mul(du[b],a),m)))%q
 def beta2(a,b,m):return(v('upsilon',b,du[b],m)-v('upsilon',b,du[b],mul(m,a))+v('chi',b,a,mul(m,a)))%q
 def beta3(a,b,m):return(v('upsilon',a,du[b],du[m])+tau(mul(m,a))-alpha(a,du[b],b)-alpha(mul(a,du[b]),mul(b,du[a]),a)-tau(m))%q
 def gamma(a,b,m):
  u=mul(du[b],m)
  return(tau(u)+v('upsilon',du[a],a,du[u])-v('upsilon',du[b],b,mul(u,du[a]))-v('chi',b,a,m))%q
 supp={(i,j):[k for k in range(len(R))if R[i][j][k]]for i,j in itertools.product(range(len(R)),repeat=2)};out={}
 for i,j,k in itertools.product(range(len(R)),repeat=3):
  for e in supp[i,j]:
   for l in supp[e,k]:
    for f in supp[j,k]:
     if not R[i][f][l]:continue
     typ=(int(i not in S),int(j not in S),int(k not in S))
     if typ==(0,0,0):phase=alpha(i,j,k)
     elif typ==(0,0,1):phase=v('upsilon',i,j,l)
     elif typ==(0,1,0):phase=v('chi',i,k,l)
     elif typ==(1,0,0):phase=alpha1(j,k,l)
     elif typ==(0,1,1):phase=beta1(i,l,j)
     elif typ==(1,0,1):phase=beta2(j,l,i)
     elif typ==(1,1,0):phase=beta3(k,l,j)
     else:phase=gamma(f,e,l)
     out[i,j,k,l,e,f]=phase%q
 return out

def equations(R,F,p,q):
 n=len(R);vertices=[(i,j,k)for i,j,k in itertools.product(range(n),repeat=3)if i and j and R[i][j][k]];keys=[('J',*v)for v in vertices]+[('eta',i)for i in range(1,n)];ix={k:i for i,k in enumerate(keys)};rows=[];rhs=[]
 def add(terms,value):
  z=collections.Counter()
  for a,key in terms:
   if key in ix:z[ix[key]]+=a
  z={k:v for k,v in z.items()if v}
  if z or value%q:rows.append(z);rhs.append(value%q)
 for key,phase in F.items():
  i,j,k,l,e,f=key
  add([(1,('J',i,j,e)),(1,('J',e,k,l)),(-1,('J',j,k,f)),(-1,('J',i,f,l))],F[tuple(p[a]for a in key)]-phase)
 for i,j,k in vertices:
  add([(1,('eta',i)),(1,('eta',j)),(-1,('eta',k)),(-1,('J',i,j,k)),(-1,('J',p[i],p[j],p[k]))],0)
 for i in range(1,n):add([(1,('eta',p[i])),(-1,('eta',i))],0)
 A=np.zeros((len(rows),len(keys)),dtype=np.int64)
 for i,row in enumerate(rows):
  for j,v in row.items():A[i,j]=v
 return A,np.array(rhs,dtype=np.int64).reshape(-1,1),keys

def verify_action(R,F,p,J,eta,q):
 def j(a,b,c):return J.get((a,b,c),0)
 common.require(sorted(p)==list(range(len(R)))and all(p[p[i]]==i for i in range(len(R))),'involutive permutation')
 for (a,b,c,d,e,f),phase in F.items():
  common.require((j(a,b,e)+j(e,c,d)-j(b,c,f)-j(a,f,d)-F[p[a],p[b],p[c],p[d],p[e],p[f]]+phase)%q==0,'every tensor-functor equation')
 for a,b,c in itertools.product(range(len(R)),repeat=3):
  if R[a][b][c]:common.require((eta[a]+eta[b]-eta[c]-j(a,b,c)-j(p[a],p[b],p[c]))%q==0,'monoidal square coherence')
 common.require(all(eta[p[a]]==eta[a]for a in range(len(R))),'action pentagon')

def equiv(R,p,J,eta,q):
 n=len(R);labs=[];seen=set()
 for a in range(n):
  if a in seen:continue
  O=sorted({a,p[a]});seen.update(O)
  for k in range(2 if len(O)==1 else 1):labs.append([O,k])
 r=len(labs);T=[[[0]*r for _ in range(r)]for _ in range(r)]
 for i,(A,a0)in enumerate(labs):
  for j,(B,b0)in enumerate(labs):
   for k,(C,c0)in enumerate(labs):
    c=C[0];dim=sum(R[a][b][c]for a in A for b in B)
    if len(C)==2:T[i][j][k]=dim;continue
    tr=0
    for a,b in itertools.product(A,B):
     if p[a]!=a or p[b]!=b or not R[a][b][c]:continue
     e=(eta[a]+eta[b]-eta[c]-2*J.get((a,b,c),0)+q*(a0+b0-c0))%(2*q)
     common.require(e in(0,q),'genuine stabilizer involution')
     tr+=(1 if e==0 else-1)*R[a][b][c]
    common.require(dim+tr>=0 and(dim+tr)%2==0,'integer Fourier projection');T[i][j][k]=(dim+tr)//2
 return T,labs

def main():
 start=time.monotonic();D=json.loads((BASE/'tensors.json').read_text());families=json.loads((BASE/'unresolved_families.json').read_text())['records'];targets={r['id']:D[r['id']]for r in families if r['family']=='D32'};buckets=collections.defaultdict(list)
 for rid,R in targets.items():buckets[common.coarse(R)].append((rid,R))
 receipts=[];hits=collections.defaultdict(list);seen=set();q=128
 for row in json.loads((BASE/'feudal.json').read_text())['records']:
  c=row['model']
  if not c or len(c['serfs'])!=8 or len(c['lords'])!=4:continue
  R=D[row['id']];F=reconstructed(R,c,q);characters=list(chars(R,c));count=0
  for p in maps(R,c):
   A,B,keys=equations(R,F,p,q);sols=prime_power_solve(A,B,2,7)
   if 0 not in sols:
    receipts.append(dict(base_id=row['id'],automorphism=p,status='no_solution_in_modulus128',not_an_exclusion=True));continue
   sol=sols[0];common.require(np.all((A@sol-B[:,0])%q==0),'all original linear equations');count+=1
   J={key[1:]:int(sol[i])for i,key in enumerate(keys)if key[0]=='J'};eta0=[0]+[int(sol[keys.index(('eta',i))])for i in range(1,len(R))]
   for char in characters:
    if any(char[p[a]]!=char[a]for a in range(len(R))):continue
    eta=[(a+(q//8)*b)%q for a,b in zip(eta0,char)];verify_action(R,F,p,J,eta,q)
    T,labs=equiv(R,p,J,eta,q);key=common.sha(T)
    if key in seen:continue
    seen.add(key);common.validate(T);matched=[]
    for rid,S in buckets[common.coarse(T)]:
     bm=common.based_iso(S,T)
     if bm is None:continue
     common.require(all(S[i][j][k]==T[bm[i]][bm[j]][bm[k]]for i,j,k in itertools.product(range(12),repeat=3)),'complete model match')
     matched.append(rid);hits[rid].append(dict(name='Coherent C2 equivariantization of '+row['id'],constructor='liptrap_C2_equivariant',parameters=dict(base_id=row['id'],base_tensor=R,base_liptrap_model=c,automorphism=p,phase_modulus=q,tensorator_phases=[[*k,v]for k,v in J.items()],square_coherence_phases=eta,labels=labs),model_tensor=T,basis_map_source_to_model=bm))
     print('HIT',rid,'base',row['id'],'p',p,flush=True)
    receipts.append(dict(base_id=row['id'],automorphism=p,status='verified_unitary_action',eta=eta,matches=matched,tensor_sha256=key))
  print('base',row['id'],'verified actions',count,'seconds',time.monotonic()-start,flush=True)
 rows=[dict(id=rid,tensor_sha256=common.sha(D[rid]),models=ms)for rid,ms in hits.items()]
 (HERE/'gauge_equivariant_models.json').write_text(json.dumps(rows,indent=2)+'\n');(HERE/'gauge_equivariant_attempts.json').write_text(json.dumps(dict(records=receipts,seconds=time.monotonic()-start),indent=2)+'\n')
 print('TOTAL',len(hits),'models',sum(map(len,hits.values())),'distinct candidates',len(seen),'seconds',time.monotonic()-start,flush=True)
if __name__=='__main__':main()
