"""Exact negative-diagonal obstruction for R1154 center pattern3994."""
import sys,json,itertools,math
from pathlib import Path
from fractions import Fraction as F
UP=Path(__file__).resolve().with_name('joint_triple_after_a2.py')
exec(compile(UP.read_text().split('def main():')[0],str(UP),'exec'))
source=HERE/'group1_all_triples.json';record=json.load(open(source));need(record['all_histogram_solutions_enumerated'],'complete triple histograms');need(record['verifier_sha256']==digest(UP),'triple enumerator binding')
for path,sha in record['source_sha256'].items():need(digest(ROOT/path)==sha,'triple source binding '+path)
rr=record['results'][0];need(rr['index']==3994 and len(rr['witnesses'])==1,'unique group1 triple completion')
pairrow=next(z for z in fibers['results']if z['index']==3994);pair=pairrow['pair11_histogram_solutions_by_high_type'][0];ns=[1]+domain['completions'][3994]
# Extend exact scalar moments only as far as the invariant-action proof needs.
for deg in (7,8):
 for word in itertools.combinations_with_replacement(range(1,5),deg):
  val=K.zero
  for n,vs,wt in zip([1]*5+ns[1:],values,weights):
   z=K(n)*wt
   for i in word:z*=vs[i]
   val+=z
  raw=c.ec(val);need(len(raw)<=1,'rational scalar moment');v=F(raw[0])if raw else F(0);need(v.denominator==1,'integer scalar moment');moment_coefficients[word]=([[int(v)]],1)
signature=[];mom={}
for word,(co,den)in moment_coefficients.items():
 if len(co)==1 and len(co[0])==1:v=co[0][0]
 else:
  ir=sum(n*v[0]for n,v in zip(ns,co));ra=sum(n*v[1]for n,v in zip(ns,co));need(ir==0 and ra%den==0,'integer moments');v=ra//den
 mom[word]=v
 if len(word)<=6:signature.append(v)
inds,C,alpha,hh,oldmom=augmented(tuple(signature));X0=[[F(x)for x in row]for row in groups[1]['minimum_norm_rows_by_high_type']];h=list(map(F,quartic['h']))
basewords=[(),(1,),(2,),(3,),(4,),(1,1),(1,2),(2,2),(1,1,1),(1,1,2)]
labels=[];vectors=[]
for j in range(5):
 labels.append({'low':j});vectors.append([int(j==0)if not w else mom[tuple(sorted(w+((j,)if j else ())))] for w in basewords])
 # Vacuum/low word coefficient is delta, not the corresponding spectral moment.
 vectors[-1][:5]=[int(j==k)for k in range(5)]
for hist in rr['witnesses'][0]:
 typ,x=hist['type'],hist['pair11'];row,basis,q,vals=row_data(1,typ,x,tuple(signature));vb=[row[i]for i in inds];zs=[sum(x*C[k][j]for k,x in enumerate(vb))for j in range(20)]
 for val,n in hist['triple133_histogram']:
  triples_actual=[z+(F(val)-q)*hc for z,hc in zip(zs,hh)];allw={w:row[i]for i,w in enumerate(words)};allw.update(dict(zip(triples,triples_actual)))
  for k in range(n):labels.append({'type':typ,'pair11':x,'triple133':val,'copy':k});vectors.append([allw[w]for w in basewords])
V=s.Matrix(vectors);N=V.rows;moment=lambda w:mom[tuple(sorted(w))]
G=s.Matrix(10,10,lambda i,j:moment(basewords[i]+basewords[j]));need(V.T*V==G,'complete word Gram');Gi=G.inv();P=V*Gi*V.T;need(P*P==P and P.T==P,'cyclic projection')
Fs=[]
for obj in range(1,5):
 B=s.Matrix(10,10,lambda i,j:moment(basewords[i]+(obj,)+basewords[j]));B2=s.Matrix(10,10,lambda i,j:moment(basewords[i]+(obj,obj)+basewords[j]));need(B*Gi*B==B2,'exact cyclic-span invariance');Fs.append(V*Gi*B*Gi*V.T)
# The vacuum has nonzero component in every joint eigenspace, since its
# modular spectral weight is d_Z^2/D^2>0. Thus a cyclic invariant span of
# dimension equal to the number of distinct joint tuples contains one copy
# of each tuple; all further copies lie in its orthogonal complement.
spec={}
for n,vs in zip([1]*5+ns[1:],values):
 if n:
  key=tuple(tuple(c.ec(v))for v in vs)
  if key not in spec:spec[key]=[vs,n]
  else:spec[key][1]+=n
need(len(spec)==10==V.cols,'full vacuum cyclic span')
hidden=[]
for vs,n in spec.values():
 if n>1:
  need(a['embedding'].sign(vs[4])<=0,'nonpositive hidden A4 spectrum')
  hidden.append({'A4_eigenvalue':c.ec(vs[4]),'multiplicity':n-1})
need(sum(z['multiplicity']for z in hidden)==N-10,'complete hidden spectrum')
bad=[i for i in range(N)if Fs[3][i,i]<0]
need(bad,'strict negative fixed diagonal')
cert=[{'simple':labels[i],'fixed_A4_diagonal':str(Fs[3][i,i]),'actual_A4_diagonal_upper_bound':str(Fs[3][i,i])}for i in bad]
print(json.dumps({'schema':'r1154-group1-negative-diagonal/v1','index':3994,'center_rank':N,'pair_histograms':1,'triple_histograms':1,'cyclic_rank':10,'invariant_under_all_four_actions':True,'hidden_A4_spectrum':hidden,'negative_diagonal_certificates':cert,'status':'excluded_necessary_center_pattern','scope':'Excludes center pattern3994 only; no source-ring exclusion or categorification asserted','source_sha256':{p.relative_to(ROOT).as_posix():digest(p)for p in [source,UP]},'verifier_sha256':digest(Path(__file__))},indent=2))
