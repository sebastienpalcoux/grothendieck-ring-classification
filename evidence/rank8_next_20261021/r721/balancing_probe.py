exec(open(__file__.replace('balancing_probe.py','twist_sums_probe.py')).read().split('for case in cases:')[0])
s=c.s
receipt=json.loads((repo/'evidence/rank8_center_followup_20261021/r721_center_extension_receipt.json').read_text())
case=receipt['case_results'][7];types=[i for i,n in enumerate(case['counts'])for _ in range(n)];vs=list(cols)+[(0,)+tuple(high[t][0])for t in types];ds=[md.value(chs[0],v,K)for v in vs]
perm=case['permutation'];inverse=[perm.index(i)for i in range(5)]
S=[[a['D']/a['codegrees'][inverse[i]]/K(a['multiplicities'][inverse[i]])*md.value(chs[inverse[i]],v,K)for v in vs]for i in range(5)]
def reduce(A):
 piv=[];rr=0
 for k in range(len(A[0])-1):
  j=next((i for i in range(rr,len(A))if A[i][k]!=K.zero),None)
  if j is None:continue
  A[rr],A[j]=A[j],A[rr];v=A[rr][k];A[rr]=[x/v for x in A[rr]]
  for j in range(len(A)):
   if j!=rr:
    v=A[j][k];A[j]=[x-v*y for x,y in zip(A[j],A[rr])]
  piv.append(k);rr+=1
 return A,piv
for size in range(3):
 w=next(w for w in case['witnesses']if w['matching_size']==size);N=w['matrices'];eq=[]
 for i in range(1,5):
  for j in range(22):
   row=[K(N[i-1][k][j])*ds[k]-(S[i][j]if k==j else K.zero)for k in range(22)]
   eq.append(row+[K.zero])
 for j in range(22):
  if j<5 or types[j-5]in(0,3):
   val=-1 if j>=5 and types[j-5]==0 else 1
   eq.append([K(int(k==j))for k in range(22)]+[K(val)])
 A,piv=reduce(eq);bad=any(all(x==K.zero for x in r[:-1])and r[-1]!=K.zero for r in A)
 print('MATCHING',size,'rank',len(piv),'BAD',bad,'types',types)
 if not bad:
  for j,r in zip(piv,A):print(j,[(k,c.ec(x))for k,x in enumerate(r)if x!=K.zero])
