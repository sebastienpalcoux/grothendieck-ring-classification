"""Exploratory exact C4 tensor action on a pointed eight-object category."""
from standard import *

def bits(a):return[(a>>i)&1 for i in range(3)]
def p(a):
 x,y,z=bits(a);return (x^y)+2*(y^z)+4*z
P=[list(range(8))]
for _ in range(3):P.append([p(a)for a in P[-1]])

def omega(a,b,c):
 x,y,z=map(bits,(a,b,c));return x[0]*(y[0]*z[0]+y[1]*z[1]+y[2]*z[2]+y[1]*z[2])%2

def gf2(A,b,n):
 bas={};eq=[]
 for row,rhs in zip(A,b):
  orig=row
  while row:
   j=row.bit_length()-1
   if j in bas:row^=bas[j][0];rhs^=bas[j][1]
   else:bas[j]=row,rhs;break
  if not row and rhs:return None
 v=0
 for j,(r,s)in sorted(bas.items()):
  if((r&v).bit_count()%2)^s:v^=1<<j
 kern=[]
 for j in sorted(set(range(n))-set(bas)):
  z=1<<j
  for i,(r,s)in sorted(bas.items()):
   if(r&z).bit_count()%2:z^=1<<i
  kern.append(z)
 return v,kern

def solveJ():
 keys=[(a,b)for a,b in itertools.product(range(1,8),repeat=2)];ix={k:i for i,k in enumerate(keys)};forms=[];rows=[];rhs=[]
 for a,b,c in itertools.product(range(8),repeat=3):
  form=[(1,(b,c)),(-1,(a^b,c)),(1,(a,b^c)),(-1,(a,b))]
  form=[(s,ix[k])for s,k in form if k in ix];forms.append(form)
  row=0
  for s,i in form:row^=1<<i
  rows.append(row);rhs.append(2*(omega(a,b,c)-omega(p(a),p(b),p(c))))
 zero,kern=gf2(rows,[0]*len(rows),len(keys));print('mod2ker',len(kern),flush=True)
 for mask in range(1<<len(kern)):
  x0=0
  for i,z in enumerate(kern):
   if mask>>i&1:x0^=z
  rr=[]
  for form,r in zip(forms,rhs):
   v=sum(s*((x0>>i)&1)for s,i in form);assert(r-v)%2==0;rr.append(((r-v)//2)%2)
  sol=gf2(rows,rr,len(keys))
  if sol is None:continue
  x1,_=sol;J=[[0]*8 for _ in range(8)]
  for(a,b),i in ix.items():J[a][b]=((x0>>i)&1)+2*((x1>>i)&1)
  if not all((J[b][c]-J[a^b][c]+J[a][b^c]-J[a][b]-2*omega(a,b,c)+2*omega(p(a),p(b),p(c)))%4==0 for a,b,c in itertools.product(range(8),repeat=3)):raise ValueError('tensorator')
  print('FOUNDJ mask',mask,flush=True);return J
 raise ValueError('J obstruction')

def main():
 J0=solveJ();out=[]
 for mask in range(8):
  pairs=[(0,1),(0,2),(1,2)];J=[[ (J0[a][b]+2*sum(((mask>>j)&1)*bits(a)[r]*bits(b)[s]for j,(r,s)in enumerate(pairs)))%4 for b in range(8)]for a in range(8)]
  N=[[sum(J[P[e][a]][P[e][b]]for e in range(4))%4 for b in range(8)]for a in range(8)]
  mus=[]
  for vv in itertools.product(range(2),repeat=7):
   mu=[0]+[(N[a][a]+4*vv[a-1])%8 for a in range(1,8)]
   if not all((mu[a]+mu[b]-mu[a^b]-2*N[a][b])%8==0 for a,b in itertools.product(range(8),repeat=2)):continue
   if not all(mu[p(a)]==mu[a]for a in range(8)):continue
   mus.append(mu)
  print('Jclass',mask,'mus',mus,flush=True)
  for mu in mus:
   out.append({'J_mod4':J,'mu_mod8':mu,'mask':mask})
 (HERE/'jordan_action.json').write_text(json.dumps({'status':'exploratory','actions':out,'omega_mod2':[[[omega(a,b,c)for c in range(8)]for b in range(8)]for a in range(8)],'permutation':P[1]},indent=2)+'\n')
if __name__=='__main__':main()
