def _audit_require(ok, message):
    if not ok: raise AssertionError(message)

#!/usr/bin/env python3
"""Exact rank-six Morita action reconstruction for type III mixed signs."""
import json
from pathlib import Path
import sympy as s

I3=s.eye(3)
g=s.Matrix([[0,1,0],[1,0,0],[0,0,1]])
sig=s.Matrix([[0,0,1],[0,0,1],[1,1,0]])
U=s.Matrix([[1,2],[2,5]])
R=s.Matrix([[0,1],[1,4]])
V=s.diag(1,-1)
P=(U+V)/2;Q=(U-V)/2
I=s.eye(6);G=s.kronecker_product(s.eye(2),g)
S=s.kronecker_product(s.eye(2),sig)
X=s.kronecker_product(P,I3)+s.kronecker_product(Q,g)+s.kronecker_product(R,sig)
N=[I,G,X,G*X,S,S*X]
K=sum((s.kronecker_product(n,n) for n in N),s.zeros(36))
vec=lambda M:s.Matrix(list(M))
mat=lambda v:s.Matrix(6,6,list(v))
Y=mat(K[:,0]-vec(I))
basis=[I,G,Y,G*Y]
H=K-sum((vec(m)*vec(m).T for m in basis),s.zeros(36))
_audit_require(H.rank()==2, 'Exact audit check failed')
anchor=2
_audit_require(H[anchor,anchor]==2, 'Exact audit check failed')
total=H[:,anchor]
difgram=2*H-total*total.T
_audit_require(difgram.rank()==1, 'Exact audit check failed')
j=next(i for i in range(36) if difgram[i,i])
root=s.sqrt(difgram[j,j]);_audit_require(root.is_Integer, 'Exact audit check failed')
diff=difgram[:,j]/root
extras=[mat((total+diff)/2),mat((total-diff)/2)]
_audit_require(all(v.is_Integer and v>=0 for m in extras for v in m), 'Exact audit check failed')
basis+=extras
_audit_require(sum((vec(m)*vec(m).T for m in basis),s.zeros(36))==K, 'Exact audit check failed')
W=s.Matrix.hstack(*(vec(m) for m in basis))
tensor=[]
for a in basis:
    line=[]
    for b in basis:
        coeff,params=W.gauss_jordan_solve(vec(a*b))
        _audit_require(params.rows==0, 'Exact audit check failed')
        _audit_require(all(x.is_Integer and x>=0 for x in coeff), 'Exact audit check failed')
        line.append([int(x) for x in coeff])
    tensor.append(line)
receipt={'status':'Forced dual action basis under full-center rank-six theorem.',
         'basis':['1','g','Y','gY','Z0','Z1'],
         'action_matrices':[[list(map(int,row)) for row in m.tolist()] for m in basis],
         'fusion_tensor':tensor}
Path(__file__).with_name('type_iii_dual_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
for i in range(6):
 print(i, 'square',tensor[i][i])
print('Y square',tensor[2][2])
print('Z0 Y',tensor[4][2])
print('Z1 Y',tensor[5][2])
