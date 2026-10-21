"""Exact fourth spectral moment Gram on the new joint integer/phase pattern."""
from pathlib import Path
import json,itertools,time,sys,hashlib
import sympy as s
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import joint_galois_check as loader
T=loader.T;K=T.K;P=loader.P;original=loader.original;meta=loader.meta;Elist=[E for E in range(8)if E!=meta['FP_character']];du=meta['dual_characters'];pairs=list(itertools.combinations_with_replacement(Elist,2));start=time.monotonic()

def psd(M):
 M=s.Matrix(M);n=M.rows;remaining=list(range(n));pivots=[]
 while remaining:
  if any(M[i,i]<0 for i in remaining):return {'positive_semidefinite':False,'negative_diagonal_index':next(i for i in remaining if M[i,i]<0),'pivots':pivots}
  i=next((i for i in remaining if M[i,i]>0),None)
  if i is None:
   bad=next(((a,b)for a in remaining for b in remaining if M[a,b]),None)
   return {'positive_semidefinite':bad is None,'nonzero_zero_diagonal_pair':bad,'pivots':pivots,'nullity':len(remaining)}
  v=M[i,i];pivots.append([i,str(v)]);rest=[j for j in remaining if j!=i]
  for a in rest:
   for b in rest:M[a,b]-=M[a,i]*M[i,b]/v
  remaining=rest
 return {'positive_semidefinite':True,'pivots':pivots,'nullity':0}

def matrix_json(M):return [[str(x)for x in row]for row in M.tolist()]
cols=[tuple(v)for v in P['low_columns']];counts=[1]*8
for label,n in zip(loader.labels,original):
 if label[0]=='high_orbit'and n:
  cols.extend(label[2]);counts.extend([n]*len(label[2]))
values=[];denominators=[]
for v in cols:
 dim=sum((K(n)*d for n,d in zip(v,T.ds)),K.zero);chi=[sum((K(n)*a for n,a in zip(v,ch)),K.zero)for ch in T.characters]
 values.append([T.beta[E]*chi[E]for E in range(8)]);denominators.append(K.one/(T.D*T.D*dim*dim))
paired=[[row[E]*row[F]for E,F in pairs]for row in values];conjugatepaired=[[row[du[E]]*row[du[F]]for E,F in pairs]for row in values]
M=s.zeros(len(pairs));fail=[]
for a in range(len(pairs)):
 for b in range(a,len(pairs)):
  z=sum((K(n)*row[a]*other[b]*den for n,row,other,den in zip(counts,paired,conjugatepaired,denominators)),K.zero);co=z.to_list()
  if len(co)>1 or (co and s.Rational(str(co[0])).q!=1):fail.append({'left_pair':pairs[a],'right_pair':pairs[b],'field_polynomial_coefficients':list(map(str,co))});continue
  val=0 if not co else int(co[0]);M[a,b]=M[b,a]=val
  if val<0:fail.append({'left_pair':pairs[a],'right_pair':pairs[b],'negative_integer':val})
 print('fourth row',a,'failures',len(fail),flush=True)
out={'tensor_sha256':loader.source['tensor_sha256'],'integer_joint_witness_sha256':hashlib.sha256((HERE/'joint_integer_result.json').read_bytes()).hexdigest(),'scope':'fourth_product_Gram_necessary_test_on_one_selected_integer_pattern','pairs':pairs,'center_rank':sum(counts),'moment_entries':len(pairs)*(len(pairs)+1)//2,'moment_failures':fail}
if fail:out['outcome']='selected_joint_integer_pattern_fails_fourth_moments'
else:
 triples=[(E,F,G)for E,F in pairs for G in Elist];nh=len(P['duality_orbits']);fusion=dict(zip(triples,original[nh:nh+196]));known=s.Matrix(8,len(pairs),lambda g,j:int(pairs[j][1]==du[pairs[j][0]])if g==meta['FP_character']else fusion[pairs[j][0],pairs[j][1],g]);G=M-known.T*known
 V=s.Matrix.hstack(*(s.Matrix(v)for v in cols[8:]));Q=V*s.diag(*counts[8:])*V.T;I=list(Q.rref()[1]);Qb=Q.extract(I,I);prod=json.loads((HERE/'forgetful_product_probe.json').read_text())['pairs'];restriction=s.Matrix.hstack(*(s.Matrix(r['residual_high_restriction'])for r in prod));C=Qb.inv()*restriction[I,:]
 if Q[:,I]*C!=restriction:raise AssertionError('high product restrictions leave the full high Gram range')
 H=G-C.T*Qb*C;gramcheck=psd(G);residualcheck=psd(H);nonnegative=all(x>=0 for x in G)
 out.update(full_product_Gram=matrix_json(M),unknown_high_product_Gram=matrix_json(G),restriction_residual_Gram=matrix_json(H),source_high_restriction_rank=len(I),unknown_high_Gram_nonnegative=nonnegative,unknown_high_Gram_psd=gramcheck,restriction_residual_psd=residualcheck)
 out['outcome']='exact_fourth_moment_Gram_survivor'if gramcheck['positive_semidefinite']and residualcheck['positive_semidefinite']and nonnegative else'selected_joint_integer_pattern_fails_fourth_Gram'
(HERE/'fourth_moment.json').write_text(json.dumps(out,separators=(',',':'))+'\n');print(out['outcome'],'failures',len(fail),'seconds',time.monotonic()-start,flush=True)
