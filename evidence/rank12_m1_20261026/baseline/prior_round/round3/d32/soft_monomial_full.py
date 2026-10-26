from pathlib import Path
import itertools,json,math,cmath,sys
import sympy as s
import cls_soft as C
HERE=Path(__file__).resolve().parent;BASE=HERE.parents[1]/'rank12-m1-offline-20261025';sys.path.insert(0,str(BASE/'sources/work/rank11'));import common
DATA=json.loads((BASE/'tensors.json').read_text());N=C.N
blocks=[(a,b,c)for a,b,c in itertools.product(range(1,6),range(1,6),range(6))if N[a][b][c]]
large=[k for k in blocks if N[k[0]][k[1]][k[2]]==2]
roots=[s.expand_complex(s.exp(s.pi*s.I*k/4))for k in range(8)]
def phase(x):
 z=complex(x.evalf());k=round(cmath.phase(z)*4/math.pi)%8
 common.require(s.simplify(x-roots[k])==0,'exact root phase');return k

def solve2(rows,n):
 piv={}
 for mask,b in rows:
  while mask:
   k=(mask&-mask).bit_length()-1
   if k not in piv:piv[k]=(mask,b);break
   a,c=piv[k];mask^=a;b^=c
  if not mask and b:return None
 free=[k for k in range(n)if k not in piv]
 def back(x):
  for k,(a,b)in sorted(piv.items(),reverse=True):
   if ((a&x).bit_count()&1)^b:x^=1<<k
  return x
 x=back(0);return x,[back(1<<k)^x for k in free]
out=[];attempts=[]
for variant in [1,-1]:
 Fdict={}
 for a,b,c,d in itertools.product(range(6),repeat=4):
  for l in C.left(a,b,c,d):
   for r in C.right(a,b,c,d):Fdict[a,b,c,d,l,r]=C.ff(a,b,c,d,l,r,variant,1,1)
 for swaps in itertools.product(range(2),repeat=3):
  ps=dict(zip(large,swaps));svars={};zvars={}
  for k in blocks:
   if ps.get(k,0):zvars[k]=len(zvars)
   else:
    for a in range(N[k[0]][k[1]][k[2]]):svars[k,a]=len(svars)
  def pm(k,a):return a^ps.get(k,0)
  def term(k,a):
   if k in zvars:return 0,{zvars[k]:(1 if a==0 else -1)}
   if(k,a)in svars:return 1<<svars[k,a],{}
   return 0,{}
  def summ(ts):
   mask=0;zs={}
   for sign,k,a in ts:
    m,z=term(k,a);mask^=m
    for j,v in z.items():zs[j]=zs.get(j,0)+sign*v
   return mask,tuple(zs.get(j,0)for j in range(len(zvars)))
  eq=set();bad=False
  for (a,b,c,d,l,r),val in Fdict.items():
   e,mu,nu=l;f,rho,sig=r
   kl1=(a,b,e);kl2=(e,c,d);kr1=(b,c,f);kr2=(a,f,d)
   lp=(e,pm(kl1,mu),pm(kl2,nu));rp=(f,pm(kr1,rho),pm(kr2,sig))
   x=Fdict[a,b,c,d,lp,r];y=Fdict[a,b,c,d,l,rp]
   if bool(x)!=bool(y):bad=True;break
   if not x:continue
   mask,zs=summ([(1,kl1,mu),(1,kl2,nu),(-1,kr1,rp[1]),(-1,kr2,rp[2])]);eq.add((mask,zs,phase(y/x)))
  if bad:continue
  sigs=set();sols=[]
  for z in itertools.product(range(8),repeat=len(zvars)):
   rows=[];bad=False
   for mask,zs,b in eq:
    rhs=(b-sum(a*v for a,v in zip(zs,z)))%8
    if rhs%4:bad=True;break
    rows.append((mask,rhs//4))
   if bad:continue
   sol=solve2(rows,len(svars))
   if sol is None:continue
   x,ker=sol
   common.require(len(ker)<15,'bounded gauge kernel')
   for bs in itertools.product(range(2),repeat=len(ker)):
    v=x
    for bit,k in zip(bs,ker):
     if bit:v^=k
    traces={k:0 if k in zvars else sum((-1)**((v>>svars[k,a])&1)for a in range(N[k[0]][k[1]][k[2]]))for k in blocks}
    signature=tuple(traces[k]for k in blocks)
    if signature in sigs:continue
    sigs.add(signature)
    for parity in [0,1]:
     labs=list(itertools.product(range(6),[1,-1]));M=[]
     for a,sa in labs:
      row=[]
      for b,sb in labs:
       outrow=[]
       for c,sc in labs:
        trace=traces.get((a,b,c),N[a][b][c]);num=N[a][b][c]+((-1)**(parity*int(a==b==5)))*sa*sb*sc*trace
        common.require(num%2==0 and num>=0,'equivariant dimensions');outrow.append(num//2)
       row.append(outrow)
      M.append(row)
     common.validate(M)
     for rid,T in DATA.items():
      if common.coarse(T)!=common.coarse(M):continue
      p=common.based_iso(T,M)
      if p is not None and rid not in [r['id']for r in out]:
       entry=dict(id=rid,variant=variant,swaps=swaps,z=z,sign_bits=v,scalar_variables=[list(k)+[a]for k,a in svars],parity=parity,model_tensor=M,basis_map=p);out.append(entry);print('HIT',rid,variant,swaps,z,v,parity,flush=True)
    sols.append(dict(z=z,sign_bits=v))
  attempts.append(dict(variant=variant,swaps=swaps,sign_variables=len(svars),z_variables=len(zvars),equations=len(eq),trace_signatures=len(sigs)))
  print('DONE',attempts[-1],flush=True)
  (HERE/'soft_monomial_full_results.json').write_text(json.dumps(dict(models=out,attempts=attempts),indent=2))
