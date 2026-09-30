"""Integral fixed spaces of complete cyclic rotations when the twist exponent is48."""
import math,itertools
import actual48 as Q
from exact import require,evaluate
from modular_character_induction import rational_rows

def append_rows(R,d,cols,labels,nv,orders=(8,12,16,24,48),root_powers=(0,)):
 C=d['C'];D=d['DD'];F=d['F'];require(F==48 and all(F%n==0 for n in orders),'rotation orders must divide proved48');units=[u for u in range(F)if math.gcd(u,F)==1];allcols=sorted(set(tuple(c)for c in cols)|{(0,)+tuple(v)for v,a in labels});dim={v:sum((C(v[i])*d['dims'][i]for i in range(len(R))),C.zero)/D for v in allcols};sig={(v,u):evaluate(z.to_list(),C.unit**u,C)for v,z in dim.items()for u in units};root=[C.unit**a for a in range(F)];ms=sorted({m for n in orders for m in range(2,n+1)if n%m==0});lifts={m:[next(u for u in units if u%m==a)for a in range(1,m)if math.gcd(a,m)==1]for m in ms};high={((0,)+tuple(v),a)for v,a in labels};support=sorted(high|{(tuple(v),0)for v in cols});alpha={}
 for m in ms:
  for e in sorted({e%m for n in orders if n%m==0 for e in root_powers if e<n}):
   for v,a in support:alpha[m,e,v,a]=sum((sig[v,u]*root[(u*(a*m-(F//m)*e))%F]for u in lifts[m]),C.zero)
 powers={}
 for obj in range(1,len(R)):
  pp=[[1]+[0]*(len(R)-1)]
  for k in range(max(orders)):pp.append([sum(pp[-1][i]*R[i][obj][j]for i in range(len(R)))for j in range(len(R))])
  powers[obj]=pp
 rows=[];rhs=[];blocks=[];nnew=sum(1 for obj in powers for n in orders for e in root_powers if e<n);newnv=nv+nnew;aux=nv
 for obj,pp in powers.items():
  for n in orders:
   for e in root_powers:
    if e>=n:continue
    divisors=[m for m in ms if n%m==0];coef=[]
    for v,a in labels:
     full=(0,)+tuple(v);value=sum((C(sum(pp[n//m][i]*full[i]for i in range(len(R))))*alpha[m,e%m,full,a]for m in divisors),C.zero)/C(n);coef.append(value)
    constant=C(pp[n][0])/C(n)+sum((C(sum(pp[n//m][i]*v[i]for i in range(len(R))))*alpha[m,e%m,tuple(v),0]for m in divisors for v in cols),C.zero)/C(n);row=coef+[C.zero]*(newnv-len(labels));row[aux]=-C.one
    for rr,bb in rational_rows(row,-constant,C):
     if any(rr)or bb:rows.append({j:int(a)for j,a in enumerate(rr)if a});rhs.append(int(bb))
    blocks.append(dict(object=obj,order=n,root_power=e,variable=aux));aux+=1
 return rows,rhs,newnv,dict(kind='complete_cyclic_rotation_root_multiplicity',proved_exponent=48,orders=list(orders),root_powers=list(root_powers),blocks=blocks,equations=len(rows))
