exec(open(__file__.replace('s_matrix_probe.py','twist_sums_probe.py')).read().split('for case in cases:')[0])
s=c.s
rc=json.loads((repo/'evidence/rank8_center_followup_20261021/r721_center_extension_receipt.json').read_text())['case_results'][7];w=next(w for w in rc['witnesses']if w['matching_size']==2)
Ns=[s.eye(22)]+[s.Matrix(v)for v in w['matrices']];types=[i for i,n in enumerate(rc['counts'])for _ in range(n)];vs=list(cols)+[(0,)+tuple(high[t][0])for t in types];ds=[md.value(chs[0],v,K)for v in vs];groups=[[j]for j in range(5)]+[[5+j for j,t in enumerate(types)if t==k]for k in sorted(set(types))]
U=s.zeros(22,9)
for j,g in enumerate(groups):
 for k in g:U[k,j]=1
Ui=(U.T*U).inv()*U.T;small=[Ui*N*U for N in Ns[1:]];perm=rc['permutation'];inv=[perm.index(i)for i in range(5)]
# algebraic field exact scalar lists; 9x9 sympy solve only where rational eigenvalues forhigh
S0=[[K.zero for j in range(22)]for i in range(22)]
for group in groups:
 j=group[0]; lam=[md.value(chs[inv[i]],vs[j],K)*a['D']/a['codegrees'][inv[i]]/K(a['multiplicities'][inv[i]])/ds[j]for i in range(1,5)]
 # solve eigenvector in K using Gaussian elimination with vacuumcoordinate=dj
 A=[]
 for M,li in zip(small,lam):
  for r in range(9):A.append([K(M[r,t])-(li if r==t else K.zero)for t in range(9)]+[K.zero])
 A.append([K(int(t==0))for t in range(9)]+[ds[j]])
 for k in range(9):
  h=next(t for t in range(k,len(A))if A[t][k]!=K.zero);A[k],A[h]=A[h],A[k];v=A[k][k];A[k]=[x/v for x in A[k]]
  for t in range(len(A)):
   if t!=k:
    v=A[t][k];A[t]=[x-v*y for x,y in zip(A[t],A[k])]
 vec=[A[k][-1]for k in range(9)]
 assert all(all(x==K.zero for x in row)for row in A[9:])
 for col in group:
  for k,gg in enumerate(groups):
   for row in gg:S0[row][col]=vec[k]
assert all(S0[i][j]==S0[j][i]for i in range(22)for j in range(22))
QA=s.zeros(22)
for u,v in w['A_matching']:
 e=s.zeros(22,1);e[rc['A_labels'][u]]=1;e[rc['A_labels'][v]]=-1;QA+=e*e.T/2
va=s.zeros(22,1);vc=s.zeros(22,1)
for pos in range(4):va[rc['A_labels'][pos]]=s.Rational(1,2)*(1 if pos<2 else -1);vc[rc['C_labels'][pos]]=s.Rational(1,2)*(1 if pos<2 else -1)
for sign in[1,-1]:
 M= -QA+sign*(va*vc.T+vc*va.T);S=[[S0[i][j]+a['D']*K(M[i,j])for j in range(22)]for i in range(22)]
 bad=[];trip=[]
 for i,j,k in itertools.combinations_with_replacement(rc['A_labels'],3):
  value=sum((S[i][l]*S[j][l]*S[k][l]/ds[l]for l in range(22)),K.zero)/a['D']**2
  x=value.to_list();trip.append((i,j,k,c.ec(value)))
  if len(x)>1 or(x and(x[0].denominator!=1 or x[0]<0)):bad.append(trip[-1])
 print('SIGN',sign,'BAD',bad,'TRIPLES',trip)
