from pathlib import Path
import itertools,json,sys
HERE=Path(__file__).resolve().parent;BASE=HERE.parents[1]/'prior_round/prior_round/evidence/rank12-m1-offline-20261025';sys.path.insert(0,str(BASE/'sources/work/rank11'));import common
records=json.loads((BASE/'models.json').read_text());DATA=json.loads((BASE/'tensors.json').read_text());out=[]
for row in records:
 if row['id']not in ['R12_1_28','R12_1_183','R12_1_405','R12_1_522']:continue
 m=row['models'][0];p=m['parameters'];orders=p['orders'];E=list(itertools.product(*(range(n)for n in orders)));idx={x:i for i,x in enumerate(E)};G=[[idx[tuple((x+y)%n for x,y,n in zip(a,b,orders))]for b in E]for a in E];h=len(E);N=[[[0]*(h+1)for _ in range(h+1)]for _ in range(h+1)]
 for a,b in itertools.product(range(h),repeat=2):N[a][b][G[a][b]]=1
 for a in range(h):N[a][h][h]=N[h][a][h]=N[h][h][a]=1
 sigma=p['automorphism'];C=p['bicharacter_exponents'];q=p['bicharacter_modulus'];parity=p['parity']
 common.require(sorted(sigma)==list(range(h+1))and all(sigma[sigma[i]]==i for i in range(h+1)),'actual involution')
 common.require(len(set(map(tuple,C)))==h,'nondegeneracy')
 for a,b,c in itertools.product(range(h),repeat=3):
  common.require(C[a][b]==C[b][a],'symmetry');common.require((C[G[a][b]][c]-C[a][c]-C[b][c])%q==0,'bicharacter');common.require(sigma[G[a][b]]==G[sigma[a]][sigma[b]],'group automorphism')
 def F(a,b,c,d,e,f):
  if a==b==c==h:return('Fourier',-C[e][f]%q)
  if a<h and b==h and c<h:return('scalar',C[a][c]%q)
  if a==h and b<h and c==h:return('scalar',C[b][d]%q)
  return('scalar',0)
 count=0
 for a,b,c,d in itertools.product(range(h+1),repeat=4):
  for e in range(h+1):
   if not N[a][b][e]*N[e][c][d]:continue
   for f in range(h+1):
    if not N[b][c][f]*N[a][f][d]:continue
    common.require(F(a,b,c,d,e,f)==F(*(sigma[x]for x in(a,b,c,d,e,f))),'every TY scalar and Fourier entry invariant');count+=1
 common.require(parity[:-1]==[0]*h and parity[-1]in(0,1),'parity natural isomorphism')
 for a,b,c in itertools.product(range(h+1),repeat=3):
  if N[a][b][c]:common.require((parity[a]+parity[b]-parity[c])%2==0,'eta monoidal')
 common.require(all(parity[sigma[a]]==parity[a]for a in range(h+1)),'eta action coherence')
 labs=[];seen=set()
 for a in range(h+1):
  if a in seen:continue
  orb=sorted({a,sigma[a]});seen.update(orb)
  for bit in range(2 if len(orb)==1 else 1):labs.append((orb,bit))
 R=[]
 for A,aa in labs:
  rr=[]
  for B,bb in labs:
   vv=[]
   for Cc,cc in labs:
    c=Cc[0];dim=sum(N[a][b][c]for a in A for b in B)
    if len(Cc)==2:vv.append(dim);continue
    tr=0
    for a in A:
     for b in B:
      if sigma[a]!=a or sigma[b]!=b or not N[a][b][c]:continue
      exponent=(parity[a]+parity[b]-parity[c]+2*(aa+bb-cc))%4
      common.require(exponent in(0,2),'involutive Hom action');tr+=1 if exponent==0 else -1
    common.require((dim+tr)%2==0 and dim+tr>=0,'equivariant Hom dimension');vv.append((dim+tr)//2)
   rr.append(vv)
  R.append(rr)
 common.validate(R);perm=common.based_iso(DATA[row['id']],R);common.require(perm is not None,'full original tensor match')
 out.append(dict(id=row['id'],categorical_premise='actual TY category with strict orthogonal involution and coherent parity square',full_F_entries_checked=count,full_tensor_coefficients=1728,basis_map=perm,parameters=p))
(HERE/'ty_control_audit.json').write_text(json.dumps(dict(status='pass',records=out),indent=2)+'\n');print([(r['id'],r['full_F_entries_checked'])for r in out])
