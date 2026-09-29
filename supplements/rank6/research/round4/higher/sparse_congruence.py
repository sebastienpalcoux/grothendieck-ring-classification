def witness(A,b,integer,primes=(2,3,5,7)):
 cont=[j for j,v in enumerate(integer)if not v];ii=[i for i,row in enumerate(A)if not any(row[j]for j in cont)]
 for p in primes:
  basis={}
  for i in ii:
   v={j:a%p for j,a in enumerate(A[i])if a%p};v[len(A[i])]=b[i]%p;w={i:1}
   while True:
    pivot=min((j for j,x in v.items()if x and j<len(A[i])),default=None)
    if pivot is None:
     if v.get(len(A[i]),0):return {'prime':p,'rows':sorted([j,x]for j,x in w.items()if x),'value':v[len(A[i])]}
     break
    if pivot not in basis:
     q=pow(v[pivot],-1,p);v={j:x*q%p for j,x in v.items()if x};w={j:x*q%p for j,x in w.items()if x};basis[pivot]=(v,w);break
    u,z=basis[pivot];a=v[pivot]
    for j,x in u.items():
     v[j]=(v.get(j,0)-a*x)%p
     if not v[j]:v.pop(j)
    for j,x in z.items():
     w[j]=(w.get(j,0)-a*x)%p
     if not w[j]:w.pop(j)
  print('prime done',p,'rank',len(basis),flush=True)
 return None
