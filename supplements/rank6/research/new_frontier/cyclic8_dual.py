import itertools,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'software'))
import sympy as s
from full_morita_gram import full_gram
n=4;rank=8
N=[[[0]*rank for j in range(rank)] for i in range(rank)]
for i,j in itertools.product(range(rank),repeat=2):
 a,ia=i%4,i//4;b,jb=j%4,j//4
 if not ia and not jb:N[i][j][(a+b)%4]=1
 elif not ia and jb:N[i][j][4+(a+b)%4]=1
 elif ia and not jb:N[i][j][4+(a-b)%4]=1
 else:
  N[i][j][(a-b)%4]=1
  for k in range(4,8):N[i][j][k]=2
B=s.zeros(8,6)
for g in range(4):B[g,g]=1;B[4+g,g]=1
for g in range(4):B[4+g,4]=1;B[4+g,5]=1
# action alpha on module, determined by Nalpha B=B Malpha
A=s.zeros(6)
for g in range(4):A[g,(g+1)%4]=1
A[4,5]=A[5,4]=1
# row convention standard N_i[j,k]=coeff k in i*j. N_i B = B M_i
print('A valid',s.Matrix(N[1])*B==B*A)
# obtain rho by solving and then add parameters
xs=s.symbols('x:36');X=s.Matrix(6,6,xs)
eq=list(s.Matrix(N[4])*B-B*X)+list(X-X.T)
sol=s.linsolve(eq,xs);print(sol)
