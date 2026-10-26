"""Portable exact replay of the Liptrap unitary reconstruction hypotheses."""
from functools import lru_cache
import itertools,collections
import ring_checks as common

def check(R,cert):
 q=cert['modulus'];S=cert['serfs'];M=cert['lords'];H=cert['stabilizer'];du=common.dual(R);Ss=set(S);mul={(a,b):row.index(1)for a,T in enumerate(R)for b,row in enumerate(T)if a in Ss or b in Ss};X={tuple(v[:-1]):v[-1]for v in cert['phase_values']}
 common.require(q==16 and len(H)==2,'recorded source precision and stabilizer');common.require(len(X)==len(cert['phase_values']),'unique phase keys')
 keys={(f,a,b,m)for f in['chi','upsilon']for a in S if a for b in S if b for m in M}|{('tau',m)for m in M};common.require(set(X)==keys,'complete phase key set')
 common.require(all([a for a in S if mul[a,m]==m]==H==[a for a in S if mul[m,a]==m]for m in M),'common stabilizer')
 def v(f,a,b,m):return X.get((f,a,b,m),0)
 def tau(m):return X['tau',m]
 count=0
 for a,b,m in itertools.product(S,S,M):
  common.require((v('chi',b,a,du[m])-v('chi',a,b,mul[mul[a,m],b])-tau(mul[mul[a,m],b])-tau(m)+tau(mul[a,m])+tau(mul[m,b]))%q==0,'Liptrap quasisymmetry');count+=1
 for a,b,c,m in itertools.product(S,S,S,M):
  common.require((v('upsilon',a,b,m)-v('upsilon',a,b,mul[m,du[c]])+v('chi',mul[a,b],c,m)-v('chi',a,c,m)-v('chi',b,c,mul[du[a],m]))%q==0,'Liptrap biderivation');count+=1
 for m in M:
  common.require((tau(m)+tau(du[m]))%q==0,'tau times tau dual');common.require(v('chi',H[1],H[1],m)%q==q//2,'nondegenerate stabilizer bicharacter')
 def gamma(a,b,m):
  u=mul[du[b],m];return(tau(u)+v('upsilon',du[a],a,du[u])-v('upsilon',du[b],b,mul[u,du[a]])-v('chi',b,a,m))%q
 def zero(co):
  for k in range(q-1,q//2-1,-1):co[k-q//2]-=co[k];co[k]=0
  return not any(co)
 cosets=sorted({tuple(sorted(mul[a,h]for h in H))for a in S});blocks=0
 for I,J,m in itertools.product(cosets,cosets,M):
  for a,b in itertools.product(I,repeat=2):
   co=[0]*q
   for j in J:co[(gamma(a,j,m)-gamma(b,j,m))%q]+=1
   if a==b:co[0]-=len(H)
   common.require(zero(co),'exact unitary Fourier block')
  blocks+=1
 return dict(defining_identities=count,exact_unitary_fourier_blocks=blocks)

def reconstruct(R,cert):
 q=cert['modulus'];S=cert['serfs'];M=cert['lords'];Ss=set(S);du=common.dual(R);mul={(a,b):row.index(1)for a,T in enumerate(R)for b,row in enumerate(T)if a in Ss or b in Ss};p={tuple(v[:-1]):v[-1]for v in cert['phase_values']}
 def x(a,b,m):return p.get(('chi',a,b,m),0)
 def u(a,b,m):return p.get(('upsilon',a,b,m),0)
 def tau(m):return p.get(('tau',m),0)
 @lru_cache(None)
 def alpha(a,b,c):
  vals={(u(a,b,m)+u(mul[a,b],c,m)-u(a,mul[b,c],m)-u(b,c,mul[du[a],m]))%q for m in M};common.require(len(vals)==1,'pointed associator independent of lord');return vals.pop()
 @lru_cache(None)
 def F(a,b,c,k):
  if a in Ss and b in Ss and c in Ss:return alpha(a,b,c)
  if a in Ss and b in Ss:return u(a,b,k)
  if a in Ss and c in Ss:return x(a,c,k)
  if b in Ss and c in Ss:return-u(b,c,du[a])%q
  if a in Ss:return(alpha(du[k],a,mul[du[a],k])-u(du[k],a,mul[mul[du[k],a],b]))%q
  if b in Ss:return(u(k,du[k],a)-u(k,du[k],mul[a,b])+x(k,b,mul[a,b]))%q
  if c in Ss:return(u(c,du[k],du[b])+tau(mul[b,c])-tau(b)-alpha(c,du[k],k)-alpha(mul[c,du[k]],mul[k,du[c]],c))%q
  raise ValueError('Three-lord Fourier block is not used in subgroup bimodule operations')
 return F,mul,du
