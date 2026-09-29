import itertools,sympy as s
q=8
norm=lambda a:min(a,tuple((-z)%q for z in a))
def mul(a,b):return norm(((a[0]*b[0]+a[1]*b[2])%q,(a[0]*b[1]+a[1]*b[3])%q,(a[2]*b[0]+a[3]*b[2])%q,(a[2]*b[1]+a[3]*b[3])%q))
G=sorted({norm((a,b,c,d)) for a,b,c,d in itertools.product(range(q),repeat=4) if (a*d-b*c)%q==1})
I=norm((1,0,0,1));T=norm((1,1,0,1));S=norm((0,7,1,0));H=[I]
while mul(H[-1],T)!=I:H.append(mul(H[-1],T))
seen=set();cosets=[];lookup={};ks={}
for g in G:
 if g in seen:continue
 C=[mul(h,g) for h in H];idx=len(cosets);cosets.append(C);seen.update(C)
 for k,x in enumerate(C):lookup[x]=idx;ks[x]=k
A=s.zeros(24);K=s.zeros(24);Ki=s.zeros(24)
for j,C in enumerate(cosets):
 for x in C:
  z=mul(S,x);A[lookup[z],j]+=s.Rational(1,8);K[lookup[z],j]+=s.Rational((-1)**ks[z],8);Ki[lookup[z],j]+=s.I**(-ks[z])/8
L=K.T*K;Li=s.conjugate(Ki.T)*Ki
print('A,L commute?',A*L==L*A,'A,Li?',A*Li==Li*A)
for v in [0,1,-s.Rational(1,2)]:
 B=s.Matrix.hstack(*(A-v*s.eye(24)).nullspace()); gram=B.T*B; rep=gram.inv()*B.T*L*B; ri=gram.inv()*B.T*Li*B
 print('lambda',v,'dim',B.cols,'L cp',s.factor(rep.charpoly().as_expr()),'Li cp',s.factor(ri.charpoly().as_expr()),flush=True)
 if v==0:
  print('L zero eigen vectors overlap Li', s.Matrix.vstack(K*B,Ki*B).rank(),flush=True)
