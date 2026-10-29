from itertools import product
G=list(product(range(2),repeat=3));e=(0,0,0)
def swap(a):return a[1],a[0]
def mul(a,b,side=0):
 x,y,n=a;u,v,m=b
 if side==0:
  if n:u,v=v,u
 else:
  if m:x,y=y,x
 return x^u,y^v,n^m
def omega(a,b,c,mode=0):
 x,y,n=a;u,v,m=b;_,_,l=c
 if not l:return 0
 res=3*m*((x+y)%2)
 if mode==0 and m:x,y=y,x
 elif mode==1:x,y=y,x
 t={((1,0),(1,0)):1,((0,1),(0,1)):1,((1,0),(1,1)):1,((1,1),(0,1)):1,((0,1),(1,0)):2,((1,1),(1,0)):3,((0,1),(1,1)):3}
 return (res+t.get(((x,y),(u,v)),0))%4
for s,mode in product(range(2),range(2)):
 bad=sum((omega(b,c,d,mode)-omega(mul(a,b,s),c,d,mode)+omega(a,mul(b,c,s),d,mode)-omega(a,b,mul(c,d,s),mode)+omega(a,b,c,mode))%4!=0 for a,b,c,d in product(G,repeat=4))
 print('side mode',s,mode,'bad',bad)
if __name__=='__main__':
 import z3,json,time
 L=list(product(G,range(2)));I={a:i for i,a in enumerate(L)};N=len(L)
 def lm(a,b):return mul(a[0],b[0],1),a[1]^b[1]
 def p2(a):g,k=a;return (g[0]^k,g[1]^k,g[2])
 W=[[[ (omega(a[0],b[0],c[0],0)-omega(p2(a),p2(b),p2(c),0))%4 for c in L]for b in L]for a in L]
 for mod in (4,8,16,64):
  S=z3.Solver();S.set(timeout=30000)
  B={(i,j):z3.Int(f'b{i}_{j}')for i in range(1,N)for j in range(1,N)}
  def bv(i,j):return B.get((i,j),0)
  for v in B.values():S.add(v>=0,v<mod)
  for i,j,k in product(range(1,N),repeat=3):
   a,b,c=L[i],L[j],L[k];ab=I[lm(a,b)];bc=I[lm(b,c)]
   S.add((bv(j,k)-bv(ab,k)+bv(i,bc)-bv(i,j)-W[i][j][k]*(mod//4))%mod==0)
  t=time.time();ans=S.check();print('cochain modulus',mod,'answer',ans,'seconds',time.time()-t,flush=True)
  if ans==z3.sat:
   m=S.model();vals=[[m.eval(bv(i,j)).as_long() if (i,j)in B else 0 for j in range(N)]for i in range(N)]
   out={'modulus':mod,'group':L,'cochain':vals,'w':W};open('unresolved11_20261024/rank9_noncommutative/full_stabilizer_cochain.json','w').write(json.dumps(out))
   break
