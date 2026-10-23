"""Complete normalized Z/8 cochain solve via a two-generator Cayley tree.

Exploratory until a resulting cocycle and all fusion coefficients are checked.
Each vector is stored in bit planes, with the augmented constant in bit n.
"""
from jordan_action import *
import time

K=3;MOD=1<<K
def add(a,b):
 c=[];carry=0
 for x,y in zip(a,b):
  c.append(x^y^carry);carry=(x&y)|((x^y)&carry)
 return tuple(c)
def neg(a):
 out=[];carry=0
 for x in a:out.append(x^carry);carry|=x
 return tuple(out)
def sub(a,b):return add(a,neg(b))
def scale(a,c):
 out=(0,)*len(a)
 while c:
  if c&1:out=add(out,a)
  a=(0,)+a[:-1];c>>=1
 return out

def build(ext):
 E=list(itertools.product(range(8),range(4)));ix={e:i for i,e in enumerate(E)}
 G=[[ix[(a^P[e][b]^(ext if e+f>=4 else 0),(e+f)%4)]for b,f in E]for a,e in E]
 gens=[ix[0,1],ix[4,0]];tree={0:None};queue=[0]
 for h in queue:
  for g in gens:
   a=G[g][h]
   if a not in tree:tree[a]=(g,h);queue.append(a)
 if len(queue)!=32:raise ValueError('generation')
 keys=[(g,b,c)for g in gens for b in range(1,32)for c in range(1,32)]
 n=len(keys);vix={k:i for i,k in enumerate(keys)}
 W=[(0,0,0)]*(32**3)
 idx=lambda a,b,c:(a*32+b)*32+c
 def atom(g,b,c):return(1<<vix[g,b,c],0,0)if b and c else(0,0,0)
 for a in queue[1:]:
  g,h=tree[a]
  for b,c in itertools.product(range(32),repeat=2):
   W[idx(a,b,c)]=add(sub(add(W[idx(h,b,c)],atom(g,G[h][b],c)),atom(g,h,G[b][c])),atom(g,h,b))
 return E,G,gens,keys,W,idx

def eliminate(rows,n,k,label):
 start=time.time();basis={};pm=0;cm=1<<n;vm=cm-1;res=[]
 for count,row in enumerate(rows):
  row=tuple(row)
  while True:
   active=0
   for x in row:active|=x
   active&=pm
   if not active:break
   p=active.bit_length()-1;c=sum(((x>>p)&1)<<j for j,x in enumerate(row))
   row=add(row,basis[p][1][c])
  odd=row[0]&vm
  if odd:
   p=odd.bit_length()-1;c=sum(((x>>p)&1)<<j for j,x in enumerate(row))
   row=scale(row,pow(c,-1,1<<k));multiples=[scale(neg(row),j)for j in range(1<<k)]
   basis[p]=(row,multiples);pm|=1<<p
  else:
   if row[0]&cm:raise ValueError(f'no Z/{1<<k} solution at {label}:{count}')
   if any(row):res.append(row[1:])
  if count%1000==0:print(label,count,'rank',len(basis),'residual',len(res),'seconds',round(time.time()-start,2),flush=True)
 print('STAGE',label,'rank',len(basis),'residual',len(res),'seconds',time.time()-start,flush=True)
 if res and k==1:raise ValueError('nonzero mod2 remainder')
 x=[0]*n if not res else eliminate(res,n,k-1,label+'/2')
 for p,(row,_)in reversed(list(basis.items())):
  rhs=sum(((z>>n)&1)<<j for j,z in enumerate(row));total=0
  for j,z in enumerate(row):
   z&=vm^(1<<p)
   while z:
    q=(z&-z).bit_length()-1;total+=(1<<j)*x[q];z&=z-1
  x[p]=(rhs-total)%(1<<k)
 return x

def main(ext=1):
 E,G,gens,keys,W,idx=build(ext);n=len(keys);cm=1<<n
 def rows():
  # Restriction is the specified exact pointed associator on A; H is then trivial.
  for a,b,c in itertools.product(range(8),repeat=3):
   row=W[idx(4*a,4*b,4*c)];rhs=4*omega(a,b,c)
   yield tuple(v|((1<<n)if rhs>>j&1 else 0)for j,v in enumerate(row))
  # Generator equations imply every delta-W equation by delta^2=0.
  for a in gens:
   for b,c,d in itertools.product(range(1,32),repeat=3):
    yield add(sub(add(sub(W[idx(b,c,d)],W[idx(G[a][b],c,d)]),W[idx(a,G[b][c],d)]),W[idx(a,b,G[c][d])]),W[idx(a,b,c)])
 x=eliminate(rows(),n,3,'Z8')
 def ev(row):
  s=0
  for j,z in enumerate(row):
   while z:
    q=(z&-z).bit_length()-1;s+=(1<<j)*x[q];z&=z-1
  return s%8
 vals=[ev(row)for row in W]
 out={'status':'candidate_cocycle_pending_full_verification','extension':ext,'modulus':8,'group_table':G,'omega':[[vals[idx(a,b,0):idx(a,b,0)+32]for b in range(32)]for a in range(32)],'generator_variables':x}
 (HERE/f'jordan_full_cochain_{ext}.json').write_text(json.dumps(out)+'\n')
 print('FOUND cocycle',ext,flush=True)
if __name__=='__main__':main(int(sys.argv[1])if len(sys.argv)>1 else 1)
