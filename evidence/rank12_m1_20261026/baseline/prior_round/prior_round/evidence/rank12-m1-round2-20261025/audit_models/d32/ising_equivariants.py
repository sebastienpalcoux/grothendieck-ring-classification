"""Actual Liptrap-data-preserving actions on generalized-Ising categories.

The involution preserves the explicit normal reconstruction, so its
tensorator is identity. Its square coherence is any invariant tensor
automorphism of Id; all characters of the order-eight universal grading
are enumerated using eighth-root phases.
"""
from pathlib import Path
import collections,itertools,json,sys,time
HERE=Path(__file__).resolve().parent;BASE=HERE.parents[2]/'rank12-m1-offline-20261025'
sys.path.insert(0,str(BASE));sys.path.insert(0,str(BASE/'sources/work/models'));sys.path.insert(0,str(BASE/'sources/work/rank11'))
import common
from extra_models import auts

def maps(R,c):
 S=c['serfs'];M=c['lords'];idx={g:i for i,g in enumerate(S)};G=[[idx[R[a][b].index(1)]for b in S]for a in S];m0=M[0]
 for a in auts(G):
  p=[None]*len(R)
  for i,g in enumerate(S):p[g]=S[a[i]]
  if sum(p[g]==g for g in S)!=4 or any(p[p[g]]!=g for g in S):continue
  for target in M:
   q=p.copy();good=True
   for g in S:
    x=R[g][m0].index(1);y=R[q[g]][target].index(1)
    if q[x]is not None and q[x]!=y:good=False;break
    q[x]=y
   if not good or any(q[q[x]]!=x or q[x]==x for x in M):continue
   if not all(R[i][j][k]==R[q[i]][q[j]][q[k]]for i,j,k in itertools.product(range(len(R)),repeat=3)):continue
   yield q

def chars(R,c):
 S=c['serfs'];M=c['lords'];n=len(R);gens=[];closure={0}
 for g in S:
  if g in closure:continue
  gens.append(g)
  while True:
   nxt=closure|{R[a][b].index(1)for a in closure for b in gens}
   if nxt==closure:break
   closure=nxt
 for images in itertools.product(range(8),repeat=len(gens)):
  f={0:0};todo=[0];good=True
  for a in todo:
   for g,t in zip(gens,images):
    b=R[a][g].index(1);v=(f[a]+t)%8
    if b in f:
     if f[b]!=v:good=False;break
    else:f[b]=v;todo.append(b)
   if not good:break
  if not good:continue
  for t0 in range(8):
   ff=f.copy();ff[M[0]]=t0
   for a in S:
    b=R[a][M[0]].index(1);v=(f[a]+t0)%8
    if b in ff and ff[b]!=v:break
    ff[b]=v
   else:
    if len(ff)!=n:continue
    v=[ff[i]for i in range(n)]
    if all((v[i]+v[j]-v[k])%8==0 for i,j,k in itertools.product(range(n),repeat=3)if R[i][j][k]):yield v

def equiv(R,p,eta):
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
     e=(eta[a]+eta[b]-eta[c]+8*(a0+b0-c0))%16
     common.require(e in(0,8),'genuine stabilizer involution')
     tr+=(1 if e==0 else-1)*R[a][b][c]
    common.require(dim+tr>=0 and(dim+tr)%2==0,'integer Fourier projection');T[i][j][k]=(dim+tr)//2
 return T,labs

def main():
 start=time.monotonic();D=json.loads((BASE/'tensors.json').read_text());families=json.loads((BASE/'unresolved_families.json').read_text())['records'];targets={r['id']:D[r['id']]for r in families if r['family']=='D32'};buckets=collections.defaultdict(list)
 for rid,R in targets.items():buckets[common.coarse(R)].append((rid,R))
 receipts=[];hits=collections.defaultdict(list);seen=set()
 for row in json.loads((BASE/'feudal.json').read_text())['records']:
  c=row['model']
  if not c or len(c['serfs'])!=8 or len(c['lords'])!=4:continue
  R=D[row['id']];q=c['modulus'];X={tuple(v[:-1]):v[-1]for v in c['phase_values']};characters=list(chars(R,c));candidate=valid=0
  for p in maps(R,c):
   candidate+=1
   def invariant(k):
    return (k[0],*[p[a]for a in k[1:]])
   if any(X.get(invariant(k),0)%q!=v%q for k,v in X.items()):continue
   # Zero phase keys also need preservation, since zero entries are retained.
   valid+=1
   for eta in characters:
    if any(eta[p[a]]!=eta[a]for a in range(len(R))):continue
    T,labs=equiv(R,p,eta);key=common.sha(T)
    if key in seen:continue
    seen.add(key);common.validate(T);matched=[]
    for rid,S in buckets[common.coarse(T)]:
     bm=common.based_iso(S,T)
     if bm is None:continue
     common.require(all(S[i][j][k]==T[bm[i]][bm[j]][bm[k]]for i,j,k in itertools.product(range(12),repeat=3)),'complete model match')
     matched.append(rid);hits[rid].append(dict(name='C2 equivariantization of '+row['id'],constructor='liptrap_strict_C2_equivariant',parameters=dict(base_id=row['id'],base_tensor=R,base_liptrap_model=c,automorphism=p,square_coherence_exponents_mod8=eta,labels=labs),model_tensor=T,basis_map_source_to_model=bm))
     print('HIT',rid,'base',row['id'],'p',p,'eta',eta,flush=True)
    receipts.append(dict(base_id=row['id'],automorphism=p,eta=eta,matches=matched,tensor_sha256=key))
  print('base',row['id'],'characters',len(characters),'ring actions',candidate,'strict actions',valid,flush=True)
 rows=[dict(id=rid,tensor_sha256=common.sha(D[rid]),models=ms)for rid,ms in hits.items()]
 (HERE/'ising_equivariant_models.json').write_text(json.dumps(rows,indent=2)+'\n');(HERE/'ising_equivariant_attempts.json').write_text(json.dumps(dict(records=receipts,seconds=time.monotonic()-start),indent=2)+'\n')
 print('TOTAL',len(hits),'models',sum(map(len,hits.values())),'distinct candidates',len(receipts),'seconds',time.monotonic()-start,flush=True)
if __name__=='__main__':main()
