from pathlib import Path
import sys,itertools
import ring_checks as common
need=common.require
def construct(R,F,c,expected_rank=12,q=4):
 n=len(R);serfs=[a for a in range(n)if sum(R[a][common.dual(R)[a]])==1];Ss=set(serfs);mul={(a,b):row.index(1)for a,T in enumerate(R)for b,row in enumerate(T)if a in Ss or b in Ss};cert={'serfs':serfs}
 need(c in cert['serfs']and mul[c,c]==0 and F(c,c,c,c)==0,'actual involutive subgroup algebra')
 objs=[];seen=set()
 for z in range(n):
  if z in seen:continue
  D=sorted({z,mul[c,z],mul[z,c],mul[mul[c,z],c]});seen.update(D);L={};todo=set(D)
  while todo:
   x=min(todo);y=mul[c,x];need(x!=y,'free left action');L[x]=0;L[y]=-F(c,c,x,x)%q;todo-={x,y}
  choices=[]
  for values in itertools.product(range(q),repeat=len(D)-int(len(D)==4)):
   phase=([0]+list(values))if len(D)==4 else list(values);A=dict(zip(D,phase))
   if any((A[x]+A[mul[x,c]]-F(x,c,c,x))%q for x in D):continue
   if any((L[x]+A[mul[c,x]]-A[x]-L[mul[x,c]]-F(c,x,c,mul[mul[c,x],c]))%q for x in D):continue
   choices.append(A)
  need(len(choices)==(1 if len(D)==4 else 2),'complete projective stabilizer characters')
  for A in choices:objs.append(dict(z=z,D=D,L=L,R=A))
 rank=len(objs)
 if rank!=expected_rank:return None,dict(rank=rank)
 N=[[[0]*rank for _ in range(rank)]for _ in range(rank)]
 for i,A in enumerate(objs):
  for j,B in enumerate(objs):
   pairs=[(x,y,k)for x in A['D']for y in B['D']for k,v in enumerate(R[x][y])if v];maps={}
   for P in pairs:
    x,y,k=P;Q=(mul[x,c],mul[c,y],k);delta=(F(mul[x,c],c,y,k)+B['L'][y]-A['R'][mul[x,c]])%q;back=(F(x,c,mul[c,y],k)+B['L'][mul[c,y]]-A['R'][x])%q
    need((delta+back)%q==0,'balanced relation');rep=min(P,Q);maps[P]=(rep,0 if P==rep else delta)
   reps=sorted({p for p,v in maps.values()});left={};right={}
   for P in reps:
    x,y,k=P;Q,a=maps[mul[c,x],y,mul[c,k]];left[P]=(Q,(A['L'][x]-F(c,x,y,mul[c,k])+a)%q)
    Q,a=maps[x,mul[y,c],mul[k,c]];right[P]=(Q,(F(x,y,c,mul[k,c])+B['R'][y]+a)%q)
   for P in pairs:
    x,y,k=P;rep,a=maps[P]
    for target,phase,op in [((mul[c,x],y,mul[c,k]),A['L'][x]-F(c,x,y,mul[c,k]),left),((x,mul[y,c],mul[k,c]),F(x,y,c,mul[k,c])+B['R'][y],right)]:
     Q,b=maps[target];Q0,d=op[rep];need(Q==Q0 and(phase+b-a-d)%q==0,'balanced action descent')
   linv={Q:(P,-v%q)for P,(Q,v)in left.items()};need(len(linv)==len(reps),'invertible balanced left action')
   for k,C in enumerate(objs):
    z=C['z'];basis=[P for P in reps if P[2]==z]
    if len(C['D'])==4:N[i][j][k]=len(basis)
    else:
     phase=(C['R'][z]-C['L'][z])%q;co=[0]*q;co[0]=len(basis)
     for P in basis:
      Q,a=right[P];V,b=linv[Q]
      if V==P:co[(a+b-phase)%q]+=1
     # Exact Phi_10 / Phi_20 reduction of the stabilizer character sum.
     need(q in[4,8,16,32],'recorded exact cyclotomic modulus');phi=[1]+[0]*(q//2-1)+[1];deg=len(phi)-1
     for d in range(q-1,deg-1,-1):
      v=co[d]
      for j0,f in enumerate(phi):co[d-deg+j0]-=v*f
     need(not any(co[1:])and co[0]>=0 and co[0]%2==0,'exact nonnegative stabilizer projection');N[i][j][k]=co[0]//2
 units=[i for i in range(rank)if all(N[i][j][k]==N[j][i][k]==int(j==k)for j,k in itertools.product(range(rank),repeat=2))];need(len(units)==1,'unique tensor unit');order=units+[i for i in range(rank)if i not in units];N=[[[N[i][j][k]for k in order]for j in order]for i in order];objs=[objs[i]for i in order];common.validate(N)
 return N,dict(rank=rank,objects=objs)
