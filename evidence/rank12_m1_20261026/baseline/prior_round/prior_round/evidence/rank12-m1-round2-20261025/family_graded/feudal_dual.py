"""Actual C2-bimodule tensor products inside a Liptrap feudal category.
Only scalar recouplings (at most two lords) enter balanced products.
"""
from pathlib import Path
import json,sys,itertools,collections
BASE=Path(__file__).resolve().parents[2]/'rank12-m1-offline-20261025';OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE));import feudal
from group_models import common
need=common.require

def reconstruct(R,cert):
 q=cert['modulus'];S=cert['serfs'];M=cert['lords'];Ss=set(S);du=common.dual(R);mul={(a,b):row.index(1)for a,T in enumerate(R)for b,row in enumerate(T)if a in Ss or b in Ss};p={tuple(v[:-1]):v[-1]for v in cert['phase_values']}
 def x(a,b,m):return p.get(('chi',a,b,m),0)
 def u(a,b,m):return p.get(('upsilon',a,b,m),0)
 def tau(m):return p.get(('tau',m),0)
 def alpha(a,b,c):
  vals={(u(a,b,m)+u(mul[a,b],c,m)-u(a,mul[b,c],m)-u(b,c,mul[du[a],m]))%q for m in M};need(len(vals)==1,'scalar pointed associator independent of lord');return vals.pop()
 from functools import lru_cache
 alpha=lru_cache(None)(alpha)
 @lru_cache(None)
 def F(a,b,c,k):
  if a in Ss and b in Ss and c in Ss:return alpha(a,b,c)
  if a in Ss and b in Ss:return u(a,b,k)
  if a in Ss and c in Ss:return x(a,c,k)
  if b in Ss and c in Ss:return -u(b,c,du[a])%q
  if a in Ss:return(alpha(du[k],a,mul[du[a],k])-u(du[k],a,mul[mul[du[k],a],b]))%q
  if b in Ss:return(u(k,du[k],a)-u(k,du[k],mul[a,b])+x(k,b,mul[a,b]))%q
  if c in Ss:return(u(c,du[k],du[b])+tau(mul[b,c])-tau(b)-alpha(c,du[k],k)-alpha(mul[c,du[k]],mul[k,du[c]],c))%q
  raise ValueError('Three-lord Fourier block is not used in these bimodule operations')
 return F,mul,du

def construct(R,cert,c,expected_rank=12,twist=None):
 F0,mul,du=reconstruct(R,cert);n=len(R)
 if twist is None:q=10;F=lambda a,b,d,k:2*F0(a,b,d,k)%q
 else:
  degree=twist['grading'];omega=twist['cocycle'];q=20 if all(v%2==0 for A in omega for row in A for v in row)else 40
  F=lambda a,b,d,k:((q//5)*F0(a,b,d,k)+(q//4)*omega[degree[a]][degree[b]][degree[d]])%q
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
     need(q in[10,20,40],'recorded exact cyclotomic modulus');phi=([1,-1,1,-1,1]if q==10 else[1,0,-1,0,1,0,-1,0,1]if q==20 else[1,0,0,0,-1,0,0,0,1,0,0,0,-1,0,0,0,1]);deg=len(phi)-1
     for d in range(q-1,deg-1,-1):
      v=co[d]
      for j0,f in enumerate(phi):co[d-deg+j0]-=v*f
     need(not any(co[1:])and co[0]>=0 and co[0]%2==0,'exact nonnegative stabilizer projection');N[i][j][k]=co[0]//2
 units=[i for i in range(rank)if all(N[i][j][k]==N[j][i][k]==int(j==k)for j,k in itertools.product(range(rank),repeat=2))];need(len(units)==1,'unique tensor unit');order=units+[i for i in range(rank)if i not in units];N=[[[N[i][j][k]for k in order]for j in order]for i in order];objs=[objs[i]for i in order];common.validate(N)
 return N,dict(rank=rank,objects=objs)

def main():
 D=json.loads((BASE/'tensors.json').read_text());targets={r['id']for r in json.loads((BASE/'unresolved_families.json').read_text())['records']if r['family']=='D40'};out={};attempts=[]
 for row in json.loads((OUT/'feudal40_models_sparse.json').read_text()):
  if not row['certificate']:continue
  R=row['tensor'];cert=row['certificate'];F,mul,du=reconstruct(R,cert)
  # c is a noncentral involution; conjugate choices give equivalent duals.
  cs=[a for a in cert['serfs']if a and mul[a,a]==0 and any(mul[a,b]!=mul[b,a]for b in cert['serfs'])]
  if not cs:continue
  c=cs[0];N,info=construct(R,cert,c);hits=[]
  if N is not None:
   for rid in targets:
    p=common.based_iso(D[rid],N)
    if p is not None:
     hits.append(rid);out.setdefault(rid,[]).append(dict(name='C2 Morita dual of Liptrap feudal category '+str(row['parameters']),constructor='feudal_c2_morita_dual',parameters=dict(feudal_parameters=row['parameters'],feudal_tensor=R,feudal_certificate=cert,subgroup_generator=c),model_tensor=N,basis_map_source_to_model=p))
  attempts.append(dict(feudal_parameters=row['parameters'],subgroup_generator=c,rank=info['rank'],matches=hits));print(row['parameters'],info['rank'],hits,flush=True)
 (OUT/'feudal_dual_results.json').write_text(json.dumps([dict(id=rid,family='D40',models=ms)for rid,ms in out.items()],indent=2)+'\n');(OUT/'feudal_dual_attempts.json').write_text(json.dumps(attempts,indent=2)+'\n')
if __name__=='__main__':main()
