"""Exact Q(sqrt2,sqrt3) weighted central rotation; pseudo-unitary scope only."""
from pathlib import Path
import itertools,json,math,sys,time
from fractions import Fraction as F
import weighted_rank8 as w
from weighted_data_fast import low_frames
from exact import vector,discover_roots,ec,pc
from proofs import multiplication_matrix
sys.path.insert(0,str(Path(__file__).parent.parent/'performance'))
from gram_vectors_rank8 import native
s=w.s;require=w.require
def mul(a,b):
 out=[F(0)]*4
 for i,x in enumerate(a):
  for j,y in enumerate(b):out[i^j]+=x*y*(2 if i&j&1 else 1)*(3 if i&j&2 else 1)
 return tuple(out)
def trace_types(height,orders=None,powers=None):
 if powers is None:powers=list(range(1,height+1))
 if orders is None:
  bound=1
  for p,c in [(2,3),(3,1)]:
   e=0
   while p**(e+1)<=height:e+=1
   bound*=p**(c+e)
  orders=s.divisors(bound);out={tuple((F(0),)*4 for k in powers)}
 else:bound=None;out=set()
 for order in orders:
  order=int(order)
  for sign2,sign3 in itertools.product((-1,1),repeat=2):
   values=[]
   for k in powers:
    g=math.gcd(order,k);n=order//g;phi=int(s.totient(n));a=[F(int(s.mobius(n)),phi)]
    for q,conductor,sign in [(2,8,sign2),(3,12,sign3),(6,24,sign2*sign3)]:
     z=n//conductor;v=F(0)
     if n%conductor==0 and math.gcd(z,conductor)==1:
      v=F(sign*int(s.mobius(z))*int(s.kronecker_symbol(conductor,z))*int(s.kronecker_symbol(conductor,k//g))*math.isqrt(conductor//q),phi)
     a.append(v)
    values.append(tuple(a))
   out.add(tuple(values))
 return sorted(out),bound
def data(R):
 a=w.spectral(R);K=a['K'];f=a['factor'];emb=a['embedding'];require(f.degree()==4,'quartic FP field required');roots=[]
 for q in (2,3):
  rr=discover_roots(s.Poly(w.t*w.t-q,w.t),K);require(rr is not None and len(rr)==2,'required quadratic subfield absent')
  roots.append(next(x for x in rr if emb.sign(x)>0))
 basis=[K.one,roots[0],roots[1],roots[0]*roots[1]];V=s.Matrix.hstack(*(vector(x,4) for x in basis));require(V.det()!=0,'biquadratic basis singular');inverse=V.inv()
 def coords(x):return tuple(F(str(c)) for c in inverse*vector(x,4))
 norm=multiplication_matrix(a['D'],K,f).det();require(norm.q==1 and set(s.factorint(abs(int(norm))))<={2,3},'exponent prime support exceeds2,3')
 cs=[w.core.restriction(a['ds'],a['D']/fc,r,K,a['Gram']) for fc,r in zip(a['codegrees'][1:],a['multiplicities'][1:])]
 lows=low_frames(cs,a['multiplicities'][1:],a['Gram'])
 return dict(a,coords=coords,dimensions=list(map(coords,a['ds'])),global_dimension=coords(a['D']),columns=cs,lows=lows)
def high_columns(a,cols):
 L=s.Matrix.hstack(*map(s.Matrix,cols));Q=a['Gram']-L*L.T;high=[]
 for v in native(Q.extract(range(1,8),range(1,8))):
  z=sum((a['K'](v[i])*a['ds'][i+1] for i in range(7)),a['K'].zero)
  cp=multiplication_matrix(a['D']/z,a['K'],a['factor']).charpoly().as_poly()
  if any(x.q!=1 for x in cp.all_coeffs()):continue
  cp=multiplication_matrix(z,a['K'],a['factor']).charpoly().as_poly().sqf_part();co=cp.all_coeffs();degree=cp.degree();norm=abs(int(co[-1]))
  require(norm>0 and all(x.q==1 for x in co),'nonintegral central dimension')
  if any(int(c)**degree%norm**j for j,c in enumerate(co[1:],1)):continue
  high.append((tuple(v),a['coords'](z)))
 return L,Q,high
def system(R,a,cols,ep,height):
 L,Q,high=high_columns(a,cols);types,bound=trace_types(height)
 labels=[(v,z,ti) for v,z in high for ti in range(len(types))];nvars=len(labels);LL=L*L.T;d=a['dimensions'];D=a['global_dimension']
 low=[tuple(sum((F(int(LL[i,j]))*d[j][c] for j in range(8)),F(0)) for c in range(4)) for i in range(8)];require(low[0]==D,'weighted unit restriction dimension identity')
 rows=[];rhs=[]
 for i,j in itertools.combinations_with_replacement(range(7),2):
  rows.append({k:F(v[i]*v[j]) for k,(v,z,ti) in enumerate(labels) if v[i]*v[j]});rhs.append(F(int(Q[i+1,j+1])))
 moments=[[mul(z,tt) for tt in types[ti]] for v,z,ti in labels]
 for power in (1,2):
  for i in range(7):
   for c in range(4):
    rows.append({k:v[i]*moments[k][power-1][c] for k,(v,z,ti) in enumerate(labels) if v[i]*moments[k][power-1][c]});rhs.append(-low[i+1][c]+(ep[i]*D[c] if power==2 else 0))
 for obj in range(1,8):
  powers=[[1]+[0]*7]
  for order in range(1,height+1):powers.append([sum(powers[-1][i]*R[i][obj][j] for i in range(8)) for j in range(8)])
  for order in range(3,height+1):
   rs=[int(r) for r in s.divisors(order) if r<order];rot,_=trace_types(height,s.divisors(order),rs);start=nvars;nvars+=len(rot)
   rows.append({start+k:F(1) for k in range(len(rot))});rhs.append(F(powers[order][0]))
   for at,r in enumerate(rs):
    power=order//r
    for c in range(4):
     row={};constant=sum((F(powers[r][i])*low[i][c] for i in range(8)),F(0))
     for k,(v,z,ti) in enumerate(labels):
      coeff=sum(powers[r][i]*v[i-1] for i in range(1,8));value=-coeff*moments[k][power-1][c]
      if value:row[k]=value
     for k,tt in enumerate(rot):
      value=mul(D,tt[at])[c]
      if value:row[start+k]=value
     rows.append(row);rhs.append(constant)
 A=[];b=[]
 for sparse,constant in zip(rows,rhs):
  den=math.lcm(constant.denominator,*(x.denominator for x in sparse.values()));row=[0]*nvars
  for j,x in sparse.items():row[j]=int(x*den)
  constant=int(constant*den);g=math.gcd(constant,*row) or 1;A.append([x//g for x in row]);b.append(constant//g)
 return A,b,{'high_columns':len(high),'trace_types':len(types),'order_bound':bound,'rows':len(A),'variables':nvars}
def discover(R,height=6):
 a=data(R);branches=[];reports=[]
 for cols in a['lows']:
  why=w.core.low_failure(cols,a['Gram'],a['ds'],a['D'],a['K'],a['embedding'],a['du']);branch={'columns':list(map(list,cols))}
  if why:branch['ordinary']=why
  else:
   cases=[]
   for ep in w.core.indicator_choices(R):
    A,b,meta=system(R,a,cols,ep,height);y=w.core.farkas(A,b);reports.append(dict(meta,indicators=list(ep),farkas_found=y is not None))
    if y is None:return None,{'column_counts':list(map(len,a['columns'])),'low_count':len(a['lows']),'systems':reports}
    w.core.check_farkas(A,b,y);cases.append({'indicators':list(ep),'y':y,'metadata':meta})
   branch['rotation']=cases
  branches.append(branch)
 return {'kind':'biquadratic_weighted_rotation','scope':'pseudo_unitary_only','height':height,'column_counts':list(map(len,a['columns'])),'branches':branches},{'systems':reports}
def verify(R,c):
 require(c['kind']=='biquadratic_weighted_rotation' and c['scope']=='pseudo_unitary_only','incorrect scope');a=data(R)
 require(c['column_counts']==list(map(len,a['columns'])),'incomplete restriction columns');require(len(c['branches'])==len(a['lows']),'incomplete low frames')
 for cols,b in zip(a['lows'],c['branches']):
  require(b['columns']==list(map(list,cols)),'changed low frame');why=w.core.low_failure(cols,a['Gram'],a['ds'],a['D'],a['K'],a['embedding'],a['du'])
  if why:require(b.get('ordinary')==why,'incorrect ordinary obstruction');continue
  eps=w.core.indicator_choices(R);require([x['indicators'] for x in b['rotation']]==list(map(list,eps)),'incomplete indicator choices')
  for ep,case in zip(eps,b['rotation']):
   A,rhs,meta=system(R,a,cols,ep,c['height']);require(meta==case['metadata'],'system metadata changed');w.core.check_farkas(A,rhs,case['y'])
