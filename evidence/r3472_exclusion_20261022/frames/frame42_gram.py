"""Exact integer Gram decomposition for surviving low frame42.

Input high dimension theorem: eta=50+35sqrt2, beta=2eta, and
c*gamma for c=1,2,5. This proof does not use the finite high restriction list.
"""

if not __debug__:
    raise RuntimeError('Proof verification requires assertions enabled; run without -O.')
from pathlib import Path
import json,hashlib
import sympy as s
PACKAGE=Path(__file__).resolve().parents[1];ROOT=PACKAGE.parents[1];OUT=PACKAGE/'frames'
R=json.load(open(ROOT/'site/dist/downloads/fusion-tensors/R8_3_3472.txt'));N=list(map(s.Matrix,R));B=sum((x*x.T for x in N),s.zeros(8))
f=json.load(open(PACKAGE/'domain/low_beta_assignments.json'));ids=f['psd_solutions'][42];low=[[1]+[0]*7,[1]+[2]*7]+[f['vectors'][i]for i in ids];L=s.Matrix(low);Q=(B-L.T*L)[1:,1:]
V=s.ones(7,1);null=V.copy();null[2]-=7
assert Q*null==s.zeros(7,1)
# PSD implies every high column annihilates null, so total multiplicity=7v3.
# An eta column has v3=1 and A+C=6,C-A=1, impossible in integers.
# Every beta column has v3=2,A=5,C=7. Counts:18 beta and sum c^2=98.
# Therefore z=v-2V has z3=0 and sums -1,+1 on the A,C coordinate triples.
# Integral squares dominate absolute sums, so ||z||^2 >=2.
# The following exact total36 forces equality for every one of18 columns.
assert s.trace(Q)==1226
count=18;gamma_square=98
sumv=(Q[:,2]-gamma_square*V)/2
assert sum(sumv)==14*count
square_total=s.trace(Q)-7*gamma_square-4*sum(sumv)+28*count
assert square_total==2*count==36
A=[0,1,3];C=[4,5,6];vectors=[]
for a in A:
 for c in C:
  v=2*V;v[a]-=1;v[c]+=1;vectors.append(v)
zz=Q-gamma_square*(V*V.T)-2*(V*sumv.T+sumv*V.T)+4*count*(V*V.T)
assert all(zz[a,c]==-2 for a in A for c in C)
assert Q==2*sum((v*v.T for v in vectors),s.zeros(7))+gamma_square*(V*V.T)
profiles=[(98-4*b-25*c,b,c)for c in range(4)for b in range(25)if 98-4*b-25*c>=0]
assert len(profiles)==63
out={'frame':42,'low_indices':ids,'low_columns':low,'tensor_sha256':hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest(),'residual_gram':Q.tolist(),'residual_nullvector':list(null),'eta_impossible':'A+C=6,C-A=1 requires nonintegral A','beta_columns':[{'restriction':[0]+list(v),'multiplicity':2}for v in vectors],'gamma_square_total':98,'gamma_profiles':profiles,'sum_deviation_norm_squared':int(square_total),'status':'complete_integer_Gram_decompositions_given_high_dimension_domain'}
# Convert SymPy integers to builtin before encoding.
out=json.loads(json.dumps(out,default=int));assert out==json.loads((OUT/'frame42_gram.json').read_text())
print('PASS: nine beta restrictions, multiplicity2 each;63 gamma profiles',flush=True)
