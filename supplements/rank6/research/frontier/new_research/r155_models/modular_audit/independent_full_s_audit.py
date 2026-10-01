def _audit_require(ok, message):
    if not ok: raise AssertionError(message)

from pathlib import Path
import json,time,argparse
import sympy as s
import numpy as np
parser=argparse.ArgumentParser(description='Independent exact audit of the rank-26 modular-data candidate.')
parser.add_argument('--reconstruction',type=Path,default=Path(__file__).resolve().parents[2]/'r155_modular/reconstruction.json')
args=parser.parse_args()
t=time.monotonic()
r=json.loads(args.reconstruction.read_text())
x=s.Symbol('x');K=s.QQ.alg_field_from_poly(s.Poly(s.cyclotomic_poly(24,x),x),alias='audit_z')
z=K.unit;one=K.one;zero=K.zero
S=[[K([s.Rational(c)for c in a])for a in row]for row in r['normalized_S']]
N=np.array(r['fusion_rules'],dtype=np.int64);u=r['unit'];dual=r['duality'];n=len(S)
_audit_require(u==1 and n==26, 'Exact audit check failed')
_audit_require(N.min()>=0, 'Exact audit check failed')
_audit_require(np.array_equal(N,N.swapaxes(0,1)), 'Exact audit check failed')
_audit_require(np.array_equal(N[u],np.eye(n,dtype=np.int64)), 'Exact audit check failed')
_audit_require(np.array_equal(N[:,:,u],np.eye(n,dtype=np.int64)[dual]), 'Exact audit check failed')
# Integer associativity for every i,j,k,l, independent of diagonalization.
for i in range(n):
 for j in range(n):
  _audit_require(np.array_equal(N[i]@N[j],sum((int(N[i,j,k])*N[k]for k in range(n)),start=np.zeros((n,n),dtype=np.int64))), 'Exact audit check failed')
# The defining fusion eigenvector relation is checked in the independently made field.
for i in range(n):
 for j in range(n):
  for l in range(n):
   _audit_require(sum((int(N[i,j,k])*S[k][l]for k in range(n)if N[i,j,k]),zero)==S[i][l]*S[j][l]/S[u][l], 'Exact audit check failed')
# Direct Verlinde, with conjugation replaced by verified duality; all entries of
# four fusion matrices are tested rather than reusing the eigenvector relation.
for i in [2,8,12,23]:
 for j in range(n):
  for k in range(n):
   _audit_require(sum((S[i][l]*S[j][l]*S[dual[k]][l]/S[u][l]for l in range(n)),zero)==K(int(N[i,j,k])), 'Exact audit check failed')
# Direct dimension and anomaly normalization.
sqrt2=z**3+z**21;d=4+3*sqrt2;DD=72+48*sqrt2
_audit_require((12*d)**2==DD**2/2, 'Exact audit check failed')
_audit_require(S[u][u]==one/(12*d), 'Exact audit check failed')
exps=[12,0,0,12,21,0,12,21,4,16,8,20,5,5,13,13,6,6,18,18,9,9,12,0,18,0]
dims=[q/S[u][u]for q in S[u]]
_audit_require(sum((q*q*z**e for q,e in zip(dims,exps)),zero)/(12*d)==z**21, 'Exact audit check failed')
# Independent 2-space scalar arithmetic.
sqrt3=z**2+z**22;ii=z**6;w=z**8
a=one/(ii*(ii*w)*(ii-ii*w))
_audit_require(a==one/sqrt3 and (one-a*a)/3==K(2)/9, 'Exact audit check failed')
out={'passed':True,'all_integer_associativity':True,'all_exact_fusion_eigenvector_identities':True,'direct_Verlinde_matrices':[2,8,12,23],'nonnegative_integral_fusion_coefficients':True,'max_fusion_coefficient':int(N.max()),'positive_dimension_normalization':True,'anomaly_normalization':True,'selfdual_branch_rational_square':'2/9','seconds':time.monotonic()-t,'scope':'independent exact audit of modular-data candidate, not category existence'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(out)
