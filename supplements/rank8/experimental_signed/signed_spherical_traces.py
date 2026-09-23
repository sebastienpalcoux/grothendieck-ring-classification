"""Exact central trace equations for arbitrary real quadratic spherical dimensions.

Unlike the pseudo-unitary systems, no triangle/moment inequality or positive
Galois-dimension rule is imposed. Gram positivity concerns integer restriction
multiplicities only. Indicators are exhausted with both signs on self-dual
objects; dimensions can be negative.
"""
import itertools,math
from fractions import Fraction as Q
import sympy as s
from exact import require,pc,ec,evaluate,discover_roots,check_roots
from rings import Characters,codegree_poly
from induction import restriction_columns,low_matrices
from higher_traces import high_columns,trace_types,build_system,check_farkas
from character_induction import CharacterTable
from spectral_induction import Spectrum
from modular_character_induction import rational_rows

def data_and_table(R,a,f,metadata):
 K,ds,D,pD=a.component(f);degree=f.degree()
 require(degree in (1,2),'signed trace field must be rational or quadratic')
 require(all(ds) and all(ds[i]==ds[a.du[i]] for i in range(a.n)),'not a spherical dimension character')
 if degree==1:
  q=1;F=1
  def coords(x):return Q(str(ec(x)[0])) if x else Q(0),Q(0)
 else:
  co=f.all_coeffs();disc=co[1]**2-4*co[2];require(disc>0,'character field not real')
  q=math.prod(int(p) for p,e in s.factorint(disc).items() if e%2);h=math.isqrt(int(disc)//q);F=q if q%4==1 else 4*q
  def coords(x):
   v=list(map(Q,ec(x)));v=[Q(0)]*(2-len(v))+v
   return v[1]-Q(str(co[1]))*v[0]/2,Q(h,2)*v[0]
 d=list(map(coords,ds));dd=coords(D);norm=dd[0]**2-q*dd[1]**2
 require(norm.denominator==1 and norm,'nonintegral or zero global-dimension norm')
 # Both real embeddings of a spherical global dimension are positive.
 from exact import embeddings
 require(all(e.sign(D)>0 for e in embeddings(f)),'global dimension not totally positive')
 roots=discover_roots(codegree_poly(R),K);require(roots is not None,'codegrees do not split')
 check_roots(codegree_poly(R),K,roots);roots.remove(D)
 cs=[restriction_columns(ds,D/r,K,a.C) for r in roots]
 lows=low_matrices(cs,a.C,gram_prune=True) if all(cs) else []
 data=dict(ch=a,factor=f,K=K,ds=ds,D=D,q=q,conductor=F,dimensions=d,global_dimension=dd,
           primes=sorted(map(int,s.factorint(abs(norm.numerator)))),columns=cs,lows=lows)
 # The proposed table is a certificate, not trusted input: six distinct
 # unital ring characters give the entire character table of this rank-six
 # commutative semisimple algebra. Field automorphisms are reconstructed.
 tab=CharacterTable.__new__(CharacterTable);tab.n=a.n;tab.du=a.du;tab.K=K;tab.seed=[]
 require(metadata['field_polynomial']==pc(f) and metadata['seed']==[],'wrong signed character field')
 tab.rows=[tuple(K([s.Rational(x) for x in z]) for z in row) for row in metadata['characters']]
 require(len(tab.rows)==a.n and len(set(tab.rows))==a.n and all(len(row)==a.n and row[0]==K.one for row in tab.rows),'incomplete character table')
 for row in tab.rows:
  require(all(row[i]*row[j]==sum((K(R[i][j][k])*row[k] for k in range(a.n)),K.zero) for i in range(a.n) for j in range(a.n)),'row is not a ring character')
 tab.codegrees=[sum((row[i]*row[a.du[i]] for i in range(a.n)),K.zero) for row in tab.rows]
 check_roots(codegree_poly(R),K,tab.codegrees)
 tab.ds=ds;tab.D=D;tab.fp=next((i for i,row in enumerate(tab.rows) if list(row)==ds),None)
 require(tab.fp is not None,'dimension character absent')
 tab.dims={};tab.values={};tab.allowed={};tab.compatibility={}
 require(tab.metadata()==metadata,'field automorphisms or table metadata incorrect')
 return data,tab

def equation_system(R,data,tab,cols,ep,height,lab,sp):
 K=tab.K;n=len(R);types,_=trace_types(data['q'],data['primes'],height)
 one=types.index(tuple((Q(1),Q(0)) for _ in range(height)))
 # Represent sqrt(q) using the chosen positive root of the generator.
 f=data['factor']
 if f.degree()==1:sq=K.one
 else:
  co=f.all_coeffs();h=math.isqrt(int(co[1]**2-4*co[2])//data['q']);sq=(K(2)*K([1,0])+K(co[1]))/K(h)
 phases=[K(tt[0][0])+K(tt[0][1])*sq for tt in types]
 L=s.Matrix.hstack(*map(s.Matrix,cols));A,b,meta=build_system(R,data,L,ep,height);labels=meta['labels']
 rows,rhs=sp.balance(labels,len(A[0]),one);A+=rows;b+=rhs
 forbidden=set(map(tuple,sp.forbidden));keep=[j for j in range(len(A[0])) if j>=len(labels) or tuple(labels[j][0]) not in forbidden]
 A=[[row[j] for j in keep] for row in A]
 tuples=dict(zip(sp.vectors,sp.types))
 for aa,bb in itertools.combinations_with_replacement(range(1,n),2):
  ha,hb=lab[aa],lab[bb]
  weights={v:tuples[v][ha]*tuples[v][hb]*tab.dims[v]**2 for v in set(sp.vectors)}
  rhs=tab.D*tab.dims[tuple(cols[aa])]*tab.values[ha,tuple(cols[bb])]-sum((weights[v] for v in sp.low),K.zero)
  coeff=[weights[(0,)+tuple(labels[j][0])]*phases[labels[j][1]] if j<len(labels) else K.zero for j in keep]
  for row,value in rational_rows(coeff,rhs,K):A.append(row);b.append(value)
 return A,b

def check_farkas_sparse(A,b,y):
 """The same exact Farkas inequalities, omitting zero summands only."""
 require(len(y)==len(b) and all(type(t) is int for t in y),'malformed signed Farkas vector')
 support=[(i,v) for i,v in enumerate(y) if v]
 require(all(sum(A[i][j]*v for i,v in support)>=0 for j in range(len(A[0]))),'signed Farkas coefficient is negative')
 require(sum(b[i]*v for i,v in support)<0,'signed Farkas right side is not negative')

class IndicatorSystems:
 """Reconstruct all sign systems from their two rowwise endpoints.

 In higher_traces.build_system the second-indicator rows are the only
 rows depending on indicators. Each such row depends on exactly one
 object's sign, including its primitive integer normalization. All
 appended spectrum/modular rows are independent of these signs. Thus
 the two endpoint matrices contain every possible exact normalized row.
 This caches equation reconstruction, not any proof verdict.
 """
 def __init__(self,R,data,tab,cols,height,lab,sp):
  self.du=data['ch'].du;self.n=len(R);tail=self.n-1
  self.lo=tuple(0 if self.du[i]!=i else -1 for i in range(1,self.n))
  self.hi=tuple(0 if self.du[i]!=i else 1 for i in range(1,self.n))
  self.A0,self.b0=equation_system(R,data,tab,cols,self.lo,height,lab,sp)
  self.A1,self.b1=equation_system(R,data,tab,cols,self.hi,height,lab,sp)
  self.offset=tail*(tail+1)//2+2*tail;self.stop=self.offset+2*tail
  require(len(self.A0)==len(self.A1) and all(len(a)==len(b) for a,b in zip(self.A0,self.A1)),'indicator-dependent variable inventory')
  require(all(self.A0[r]==self.A1[r] and self.b0[r]==self.b1[r] for r in range(len(self.A0)) if not self.offset<=r<self.stop),'an additional equation depends on indicator signs')
 def system(self,ep):
  require(len(ep)==self.n-1 and all(e in {l,h} for e,l,h in zip(ep,self.lo,self.hi)),'invalid second indicator')
  A=list(self.A0);b=list(self.b0)
  for r in range(self.offset,self.stop):
   i=(r-self.offset)//2
   if ep[i]==self.hi[i]:A[r]=self.A1[r];b[r]=self.b1[r]
  return A,b

def verify(R,a,f,c):
 require(c['kind']=='signed_spherical_traces' and c['factor']==pc(f),'wrong signed trace certificate')
 require(type(c['height']) is int and 2<=c['height']<=12,'invalid trace height')
 data,tab=data_and_table(R,a,f,c['table'])
 require(c['q']==data['q'] and c['delta']==ec(data['D']),'wrong dimension data')
 require(c['column_counts']==list(map(len,data['columns'])) and len(c['branches'])==len(data['lows']),'incomplete low enumeration')
 eps=list(itertools.product(*([0] if a.du[i]!=i else [-1,1] for i in range(1,a.n))))
 for cols,branch in zip(data['lows'],c['branches']):
  require(branch['columns']==list(map(list,cols)),'wrong low frame')
  labs=tab.assignments(cols);require(branch['labellings']==list(map(list,labs)),'missing or wrong labelling')
  if not labs:require(not branch['cases'],'unlabelled cases');continue
  L=s.Matrix.hstack(*map(s.Matrix,cols));_,high=high_columns(data,L);sp=Spectrum(tab,cols,high)
  require(branch['spectrum']==sp.metadata(),'incorrect signed spectrum filter')
  if sp.missing_low:continue
  require([(x['labelling'],x['indicators']) for x in branch['cases']]==[(list(l),list(e)) for l in labs for e in eps],'incomplete joint labelling/indicator coverage')
  systems={}
  for case in branch['cases']:
   lab=tuple(case['labelling'])
   if lab not in systems:systems[lab]=IndicatorSystems(R,data,tab,cols,c['height'],lab,sp)
   A,b=systems[lab].system(case['indicators'])
   check_farkas_sparse(A,b,case['y']);require(case['bTy']==sum(x*y for x,y in zip(b,case['y'])),'wrong exact separation value')
