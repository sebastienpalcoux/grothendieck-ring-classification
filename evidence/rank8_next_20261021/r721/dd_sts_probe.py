exec(open(__file__.replace('dd_sts_probe.py','s_matrix_probe.py')).read().split('for sign in[1,-1]:')[0].replace("__file__.replace('s_matrix_probe.py','twist_sums_probe.py')","__file__.replace('dd_sts_probe.py','twist_sums_probe.py')"))
x=s.Symbol('x');L=s.QQ.alg_field_from_poly(s.Poly(s.cyclotomic_poly(17,x),x));zeta=L.unit
qr={k*k%17 for k in range(1,17)};rad=L.one+2*sum((zeta**k for k in qr),L.zero)
assert rad**2==L(17)
convert=lambda t:sum((L(co)*(21+5*rad)**i for i,co in enumerate(reversed(t.to_list()))),L.zero)
D=convert(a['D']);ss=[[convert(S0[i][j])/D for j in range(22)]for i in range(22)]
tw=[zeta**(3*l*l%17)for l in range(1,9)]
# row0 STS, C quartet sumzero
const=sum((ss[0][k]*ss[k][14]*(L(-1)if 5<=k<=8 else L.one)for k in range(10)),L.zero)
# also lowsA2,A3 alreadyinside0..4; C10..13zero
leg=lambda k:1 if k%17 in qr else -1
def sigma(v,k):return sum((L(co)*zeta**((i*k)%17)for i,co in enumerate(reversed(v.to_list()))),L.zero)
basis=[L.one]+[zeta**j+zeta**(17-j)for j in range(1,8)]
equations=[]
for j in range(1,9):
 co=[ss[0][14]*sum((tw[l-1]*L(leg(l*j))*sigma(v,l*j)for l in range(1,9)),L.zero)for v in basis]
 target=ss[0][14]/tw[j-1]-const
 vectors=[([s.Rational(str(t))for t in v.to_list()][::-1]+[s.Rational(0)]*16)[:16]for v in co+[target]]
 equations.extend([[vec[k]for vec in vectors]for k in range(16)])
A=s.Matrix(equations);red,pivs=A.rref();print('RANK',len(pivs),'PIVOTS',pivs)
if pivs==tuple(range(8)):
 coeff=list(red[:8,-1]);b=sum((L(co)*v for co,v in zip(coeff,basis)),L.zero);print('b coeff',coeff,'b',b)
 B=[[L(leg(l*j))*sigma(b,l*j)for j in range(1,9)]for l in range(1,9)]
 assert all(B[i][j]==B[j][i]for i in range(8)for j in range(8))
 print('Weil candidates',[(sign,k)for sign in[1,-1]for k in range(1,9)if b==L(sign)*(zeta**k+zeta**(17-k))/rad])
 # normalized14x14 data for bothCtwists and sign=+1, exactfieldno i neededSreal
 for ctype in[0,1]:
  qc=[]
  for u,v in w['C_matching']:
   q=s.zeros(22,1);q[rc['C_labels'][u]]=1;q[rc['C_labels'][v]]=-1;qc.append(q)
  CC=(-qc[0]*qc[0].T+qc[1]*qc[1].T)/2 if ctype==0 else -(qc[0]*qc[1].T+qc[1]*qc[0].T)/2
  add=-QA+va*vc.T+vc*va.T+CC
  S=[[ss[i][j]+L(add[i,j])for j in range(22)]for i in range(22)]
  for i in range(8):
   for j in range(8):S[14+i][14+j]=B[i][j]
  ortho=all(sum((S[i][k]*S[k][j]for k in range(22)),L.zero)==L(int(i==j))for i in range(22)for j in range(22))
  print('CTYPE',ctype,'SORTHOGONAL',ortho)
  bad=[];maxcoef=0
  for i,j,k in itertools.combinations_with_replacement(range(22),3):
   n=sum((S[i][l]*S[j][l]*S[k][l]/S[0][l]for l in range(22)),L.zero);nr=n.to_list()
   if len(nr)>1 or(nr and(nr[0].denominator!=1 or nr[0]<0)):bad.append((i,j,k,str(n)))
   elif nr:maxcoef=max(maxcoef,int(nr[0]))
  print('CTYPE',ctype,'BADFUSION',len(bad),bad[:3],'MAX',maxcoef)
