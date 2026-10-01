def _audit_require(ok, message):
    if not ok: raise AssertionError(message)

"""Independent Gram replay: subtract only I,G, never the type-III forced Y."""
from pathlib import Path
import json,itertools,math,time
import sympy as s
HERE=Path(__file__).parent;st=time.time()
I3=s.eye(3);g=s.Matrix([[0,1,0],[1,0,0],[0,0,1]]);h=s.Matrix([[0,0,1],[0,0,1],[1,1,0]])
I=s.eye(6);G=s.kronecker_product(s.eye(2),g);Sig=s.kronecker_product(s.eye(2),h)
vec=lambda M:s.Matrix(list(M));mat=lambda v:s.Matrix(6,6,list(v))
ref={r['type']:r for r in json.load(open(HERE/'dual_actions_receipt.json'))};receipts=[]
def canonical_basis(basis):return tuple(sorted(tuple(map(int,list(x)))for x in basis))
for tag,a,b,c,f,V in [('II',2,3,2,2,s.Matrix([[0,1],[1,0]])),('III_mixed',1,2,0,1,s.diag(1,-1)),('III_same',1,2,0,1,s.eye(2)),('IV_mixed',1,2,1,2,s.diag(1,-1)),('IV_same',1,2,1,2,s.eye(2))]:
 U=s.Matrix([[a,b],[b,6-a]]);R=s.Matrix([[c,f],[f,4-c]])
 X=s.kronecker_product((U+V)/2,I3)+s.kronecker_product((U-V)/2,g)+s.kronecker_product(R,h)
 actions=[I,G,X,G*X,Sig,Sig*X]
 # Explicit index formula avoids relying on Kronecker flatten convention.
 K=s.Matrix(36,36,lambda p,q:sum(n[p//6,q//6]*n[p%6,q%6]for n in actions))
 H=K-vec(I)*vec(I).T-vec(G)*vec(G).T;r=H.rank()
 # Independent principal pivots, using reverse index as a tie-break.
 J=[]
 for j in sorted(range(36),key=lambda j:(H[j,j],-j)):
  if H.extract(J+[j],J+[j]).det():J.append(j)
  if len(J)==r:break
 B=H.extract(J,J);Bi=B.inv();den=s.ilcm(*(v.q for v in Bi));E=[[int(v*den)for v in row]for row in Bi.tolist()];lift=H[:,J]*Bi
 bounds=[math.isqrt(int(B[i,i]))for i in range(r)];cands=[]
 for v in itertools.product(*(range(z+1)for z in bounds)):
  if sum(v[i]*E[i][j]*v[j]for i in range(r)for j in range(r))!=den:continue
  q=lift*s.Matrix(v)
  if all(z.is_Integer and z>=0 for z in q):cands.append((v,q))
 def orth(u,v):return sum(u[i]*E[i][j]*v[j]for i in range(r)for j in range(r))==0
 # Independent combinations enumeration: candidate sets are tiny.
 bases=[];accepted=[];forced_Y=True;maxclique=0
 for k in range(1,r+1):
  found=False
  for cc in itertools.combinations(range(len(cands)),k):
   if not all(orth(cands[i][0],cands[j][0])for i,j in itertools.combinations(cc,2)):continue
   found=True
   if k!=r:continue
   basis=[I,G]+[mat(cands[i][1])for i in cc]
   _audit_require(sum((vec(q)*vec(q).T for q in basis),s.zeros(36))==K, 'Exact audit check failed')
   if tag.startswith('III'):
    Y=mat(K[:,0]-vec(I));_audit_require(Y!=G*Y and Y not in [I,G] and G*Y not in [I,G], 'Exact audit check failed')
    forced_Y&=Y in basis and G*Y in basis
   bases.append(basis);W=s.Matrix.hstack(*(vec(q)for q in basis));good=True;N=[]
   for A in basis:
    row=[]
    for B0 in basis:
     try:x,params=W.gauss_jordan_solve(vec(A*B0))
     except ValueError:good=False;break
     if params.rows or not all(z.is_Integer and z>=0 for z in x):good=False;break
     row.append(list(map(int,x)))
    if not good:break
    N.append(row)
   if not good:continue
   dual=[]
   for A in basis:
    choices=[j for j,B0 in enumerate(basis)if B0==A.T]
    if len(choices)!=1:good=False;break
    dual.append(choices[0])
   if not good or any(N[i][j][0]!=int(j==dual[i])for i in range(len(basis))for j in range(len(basis))):continue
   # Check all associativity independently on multiplication structure constants.
   for ai,aj,ak,al in itertools.product(range(len(basis)),repeat=4):
    _audit_require(sum(N[ai][aj][t]*N[t][ak][al]for t in range(len(basis)))==sum(N[aj][ak][t]*N[ai][t][al]for t in range(len(basis))), 'Exact audit check failed')
   accepted.append(basis)
  if found:maxclique=k
 expected={canonical_basis([s.Matrix(q)for q in z['action_matrices']])for z in ref[tag]['solutions']}
 print('compare',tag,'bases',len(bases),'accepted',len(accepted),'expected',len(expected),flush=True)
 _audit_require(set(map(canonical_basis,accepted))==expected, 'Exact audit check failed')
 _audit_require(forced_Y, 'Exact audit check failed')
 rec=dict(type=tag,subtract_only=['I','G'],residual_rank=r,pivots=J,bounds=bounds,candidates=len(cands),complete_Gram_bases=len(bases),largest_orthogonal_set=maxclique,accepted=len(accepted),same_as_original_exact=True,type_III_forced_columns_appear_automatically=forced_Y)
 if tag=='IV_same':
  rec['pivot_inverse_denominator']=int(den);rec['scaled_inverse_pivot']=E;rec['candidate_pivot_vectors']=[list(v)for v,q in cands];rec['orthogonality_edges']=[[i,j]for i,j in itertools.combinations(range(len(cands)),2)if orth(cands[i][0],cands[j][0])]
 receipts.append(rec);print({k:v for k,v in rec.items()if k not in ['scaled_inverse_pivot','candidate_pivot_vectors','orthogonality_edges']},flush=True)
# Independent formal-codegree and weighted-indicator checks.
d=3+2*s.sqrt(2)+2*s.sqrt(3)+s.sqrt(6);aa=2+s.sqrt(2)+s.sqrt(3)+s.sqrt(6);bb=2+2*s.sqrt(2)+s.sqrt(3)+s.sqrt(6);D=s.expand(4*(1+d*d));W2=s.expand(2-s.sqrt(2)+(2+s.sqrt(2))*d)
indicator=[]
for nondual,other in [('a',bb),('b',aa)]:
 solutions=[]
 for u,sd,so in itertools.product([0,2],[-2,0,2],[-2,0,2]):
  if s.expand(u+sd*d+so*other-W2)==0:solutions.append([u,sd,so])
 indicator.append(dict(nondual_pair=nondual,solutions=solutions))
_audit_require(indicator[0]['solutions']==[] and indicator[1]['solutions']==[[2,2,2]], 'Exact audit check failed')
# Six character formal codegrees, using each root for X at sigma=±sqrt2.
codegrees=[s.expand(4*(1+x*x))for x in [d,d.xreplace({s.sqrt(3):-s.sqrt(3),s.sqrt(6):-s.sqrt(6)}),d.xreplace({s.sqrt(2):-s.sqrt(2),s.sqrt(6):-s.sqrt(6)}),d.xreplace({s.sqrt(2):-s.sqrt(2),s.sqrt(3):-s.sqrt(3)})]]
codegrees += [s.Integer(4),s.Integer(4)]
_audit_require(s.simplify(sum(D/f for f in codegrees)-D)==0, 'Exact audit check failed')
for mp,mm in [(1,1),(2,0),(0,2)]:
 _audit_require(s.simplify(sum(D/f for f in codegrees[:4])+(mp+mm)*D/4-D)==0, 'Exact audit check failed')
out=dict(passed=True,optimizer_used=False,seconds=time.time()-st,cases=receipts,indicator_enumeration=indicator,formal_codegree_saturation=True)
(HERE/'independent_audit_receipt.json').write_text(json.dumps(out,indent=2)+'\n');print('all pass',time.time()-st,flush=True)
