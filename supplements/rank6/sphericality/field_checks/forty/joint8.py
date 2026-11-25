"""Exact local square obstruction at joint ramified valuation eight. Run with Python 3."""
from itertools import product
from functools import lru_cache
def quadratic(a,b,c,d):
    return a*c+b*d, a*d+b*c+b*d  # phi^2 = 1+phi

def mul4(u,v):
    a,b,c,d=u
    x,y,z,w=v
    e,f=quadratic(a,b,x,y)
    g,h=quadratic(c,d,z,w)
    i,j=quadratic(a,b,z,w)
    k,l=quadratic(c,d,x,y)
    return e+2*g,f+2*h,i+k,j+l

def multiply(x,y,kind):
    u,v=x[4:]; a,b=y[4:]
    return mul4(x[:4],y[:4])+((u*a,v*b) if kind=="R" else quadratic(u,v,a,b))

def conjugate(v,j,l):
    a,b,c,d=v
    if j: a,b,c,d=a+b,-b,c+d,-d
    if l: c,d=-c,-d
    return a,b,c,d

N=32
one4=(1,0,0,0)
def sc(x,k,m=N):return tuple(v*k%m for v in x)
def cm(x,y):return sc(mul4(x,y),1)
def pw(x):
 vals=[one4]
 while 1:
  t=cm(vals[-1],x)
  if t==one4:return vals
  vals.append(t)
xi=pw((1,0,1,0));ph=pw((0,1,0,0));th=pw((3,0,-1,2));S5=(-1,2,0,0)

# normalized weight 8 tau mod32 for inner products modulo4.
def candidates(kind):
 C=set()
 for i,j,l in product(range(1,len(xi),2),range(0,len(ph),6),range(1,len(th),2)):
  F=cm(cm(xi[i],ph[j]),cm(th[l],S5))
  Finv=sc(cm(cm(xi[-i],ph[-j]),cm(th[-l],S5)),pow(5,-1,N))
  assert cm(F,Finv)==one4
  W=tuple(cm(F,conjugate(Finv,J,L)) for J,L in ((1,0),(0,1),(1,1)))
  for h in range(1,N,2):
   V=sc(Finv,h);H=sc(F,pow(h,-1,N));A=sc(H,4)
   a,b,c,d=V
   wk=(2*a+b,a+3*b,4*c+2*d,2*c+6*d)
   if kind=='R':
    for cn in (1,9,17,25):
     v=tuple(t%N for t in wk+(2,2*pow(cn,-1,N)))
     if (v[0]+v[4]+v[5])%N!=8:continue
     C.add((v,(A+(0,0),*(t+(1,1) for t in W))))
   else:
    for J in range(3,len(ph),6):
     f=cm(ph[J],S5); fi=sc(cm(ph[-J],S5),pow(5,-1,N))
     w=cm(f,conjugate(fi,1,0))[:2]
     for k in range(1,N,2):
      a,b= sc(fi,k)[:2]
      v=tuple(t%N for t in wk+(2*(2*a+b),2*(a+3*b)))
      if (v[0]+v[4])%N!=8:continue
      C.add((v,(A+(0,0),W[0]+w,W[1]+(1,0),W[2]+w)))
 return C

# coordinates of O/I after quotient by <1>. 
rad=(8,4,4,4,4)
X=list(product(*(range(r) for r in rad)))
index={v:i for i,v in enumerate(X)}
localidx=[index[x] for x in X if not any(x[i]%2 for i in (0,3,4))]
def add(u,v):return index[tuple((c+d)%r for c,d,r in zip(X[u],X[v],rad))]

def eval_orders(mode,wx):
 w=tuple(t%8 for t in wx)
 def tau(a):return sum(x*y for x,y in zip(w,a))%8
 def lift(i):return (0,)+X[i]
 def canon(v):
  a,b,c,d,e,f=v;return index[(b%8,c%4,d%4,(e-a)%4,(f-a*int(mode=='R'))%4)]
 def mul(i,j):return multiply(lift(i),lift(j),mode)
 @lru_cache(None)
 def transit(i,j):return canon(mul(i,j))
 cand=[i for i in localidx if not tau(lift(i)) and not tau(mul(i,i))]
 ortho={i:{j for j in cand if not tau(mul(i,j))} for i in cand}
 def close(H,g):
  ss=set(H); q=list(H);q.append(g)
  while q:
   x=q.pop()
   if x in ss:continue
   if x not in ortho or not ss<=ortho[x]:return None
   for y in ss:
    q.append(add(x,y));q.append(transit(x,y))
   q.extend([add(x,x),transit(x,x)])
   ss.add(x)
   if len(ss)>16:return None
  return frozenset(ss)
 current=[frozenset((0,))]; seen=set(current);final=[]
 while current:
  h=current.pop()
  if len(h)==16:
   final.append(h);continue
  for x in set(cand)-h:
   enlarged=close(h,x)
   if enlarged is None or enlarged in seen:continue
   seen.add(enlarged);current.append(enlarged)
 return final,canon

def census(mode):
    weights={}
    for w, M in candidates(mode):
        weights.setdefault(tuple(x%8 for x in w),set()).add(M)
    signatures=set()
    cases=0
    for w, marks in weights.items():
        orders,canon=eval_orders(mode,w)
        for H in orders:
            one=(1,0,0,0,1,int(mode=='R'))
            def scaled(v,m):
                return all(x%m==0 for x in v) and canon(tuple(x//m for x in v)) in H
            generators=[one]+[(0,)+X[i] for i in H]
            generators += [tuple(v*int(i==j) for i,v in enumerate((8,8,4,4,4,4))) for j in range(6)]
            reps=[(0,)*6]
            for g in generators:
                if not any(scaled(tuple(x-y for x,y in zip(g,h)),2) for h in reps):
                    reps += [tuple(x+y for x,y in zip(g,r)) for r in reps]
            assert len(reps)==64
            squares=[multiply(r,r,mode) for r in reps]
            short={m[0] for m in marks if all(canon(a) in H for a in m)}
            for A in short:
                rhs=tuple(x+y for x,y in zip(one,A))
                signatures.add(sum(scaled(tuple(x-y for x,y in zip(r,rhs)),4) for r in squares))
            cases+=1
    print(mode,len(weights),cases,sorted(signatures))
    return signatures

if __name__=='__main__':
    assert census('R')=={0}
    assert census('T')=={2}
