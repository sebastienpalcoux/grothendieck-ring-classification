"""Independent exact audit from Teo--Hughes--Fradkin Eq.(6.53), m=0.
Uses Q(sqrt(2)) arithmetic, not the proposed fusion constructor.
"""
from fractions import Fraction as F
from pathlib import Path
import itertools,json,hashlib

def require(b,msg='audit condition failed'):
 if not b:raise ValueError(msg)
def q(a,b=0):return F(a),F(b)
def add(x,y):return x[0]+y[0],x[1]+y[1]
def mul(x,y):return x[0]*y[0]+2*x[1]*y[1],x[0]*y[1]+x[1]*y[0]
def div(x,y):
 n=y[0]**2-2*y[1]**2;require(n!=0)
 return mul(x,(y[0]/n,-y[1]/n))
def total(xs):
 ans=q(0)
 for x in xs:ans=add(ans,x)
 return ans

def source():
 # Unnormalized S from THF Eq.(6.53), source order Table IX.
 # The three cosine values for m=0 are -8,4,4.
 top=[[1,1,2,4,4,4,3,3],[1,1,2,4,4,4,3,3],
      [2,2,4,-4,-4,-4,6,6],[4,4,-4,-8,4,4,0,0],
      [4,4,-4,4,4,-8,0,0],[4,4,-4,4,-8,4,0,0],
      [3,3,6,0,0,0,-3,-3],[3,3,6,0,0,0,-3,-3]]
 u=[[3]*4,[-3]*4,[0]*4,[0]*4,[0]*4,[0]*4,[-3,-3,3,3],[3,3,-3,-3]]
 bottom=[[0,0,6,-6],[0,0,-6,6],[6,-6,0,0],[-6,6,0,0]]
 S=[[q(0)for j in range(12)]for i in range(12)]
 for i,j in itertools.product(range(8),repeat=2):S[i][j]=q(top[i][j])
 for i in range(8):
  for j in range(4):S[i][8+j]=S[8+j][i]=q(0,u[i][j])
 for i,j in itertools.product(range(4),repeat=2):S[8+i][8+j]=q(bottom[i][j])
 require(all(S[i][j]==S[j][i] for i,j in itertools.product(range(12),repeat=2)))
 require(all(total(mul(S[i][k],S[k][j])for k in range(12))==q(144*(i==j))
             for i,j in itertools.product(range(12),repeat=2)), 'S orthogonality')
 R=[[[0]*12 for j in range(12)]for i in range(12)]
 for i,j,k in itertools.product(range(12),repeat=3):
  v=div(total(div(mul(mul(S[i][a],S[j][a]),S[k][a]),S[0][a])for a in range(12)),q(144))
  require(v[1]==0 and v[0].denominator==1 and v[0]>=0,'Verlinde integrality')
  R[i][j][k]=int(v[0])
 require(all(R[i][j][k]==0 for i,j in itertools.product(range(8),repeat=2)for k in range(8,12)), 'not fusion closed')
 T=[[row[:8]for row in mat[:8]]for mat in R[:8]]
 require(all(sum(T[i][j][a]*T[a][k][l]for a in range(8))==sum(T[j][k][a]*T[i][a][l]for a in range(8))
             for i,j,k,l in itertools.product(range(8),repeat=4)), 'associativity')
 return T

def audit(record):
 T=source();N=record['tensor']
 p=[0,1,7,4,5,6,2,3]
 # The target model uses [1,z,E,P,Q,W0,W1,W2]; S uses [1,z,E,W0,W1,W2,P,Q].
 source_to_proposed=[0,1,2,5,6,7,3,4]
 require(all(T[i][j][k]==record['model_tensor'][source_to_proposed[i]][source_to_proposed[j]][source_to_proposed[k]]
             for i,j,k in itertools.product(range(8),repeat=3)), 'independent/proposed tensor mismatch')
 p=[record['model_to_census'][i]for i in source_to_proposed]
 require(all(T[i][j][k]==N[p[i]][p[j]][p[k]]for i,j,k in itertools.product(range(8),repeat=3)), 'census mismatch')
 sha=hashlib.sha256(json.dumps(N,separators=(',',':')).encode()).hexdigest()
 require(sha==record['tensor_sha256'])
 return dict(id=record['id'],status='PASS',scope='unitary model',tensor_sha256=sha,
             independent_source='Teo--Hughes--Fradkin arXiv:1503.06812 Eq.(6.53), m=0',
             source_to_census=p,verified_full_modular_Verlinde_coefficients=1728,
             verified_subcategory_coefficients=512,verified_subcategory_associativity=4096)

def verify():
 record=json.loads((Path(__file__).resolve().parents[1]/'data/triality_integral_m0.json').read_text())
 return audit(record)

if __name__=='__main__':
 print(json.dumps(verify(),indent=2))
