from verlinde_probe import *
from exact import field,vector,key
from fractions import Fraction as Q
import sympy as s
from functools import lru_cache

@lru_cache(None)
def rotation_types(F,order,rs):
 t=s.Symbol('t');C=field(s.Poly(s.cyclotomic_poly(F,t),t));bound=math.lcm(F,order);W=field(s.Poly(s.cyclotomic_poly(bound,t),t));w=W.unit;powers=[w**i for i in range(bound)];step=bound//F
 M=s.Matrix.hstack(*(vector(powers[(step*i)%bound],W.mod.degree()) for i in range(C.mod.degree())));ix=list(M.T.rref()[1]);left=M.extract(ix,range(M.cols)).inv();kernel=[a for a in range(bound) if math.gcd(a,bound)==1 and a%F==1]
 def down(v):
  rhs=vector(v,W.mod.degree());x=left*rhs.extract(ix,[0]);require(M*x==rhs,'bad relative trace');return sum((C(x[i])*C.unit**i for i in range(len(x))),C.zero)
 ans=set()
 for a in range(order):
  ans.add(tuple(down(sum((powers[(a*r*u*(bound//order))%bound] for u in kernel),W.zero)/W(len(kernel))) for r in rs))
 return sorted(ans,key=str)

def rotations(R,data,cols,A,b,labels,height):
 C=data['C'];D=data['DD'];n=len(R);low=[sum((C(sum(c[i]*c[j] for c in cols))*data['dims'][j] for j in range(n)),C.zero) for i in range(n)];zv={v:sum((C(v[i])*data['dims'][i+1] for i in range(n-1)),C.zero) for v,ti in labels};nh=len(labels)
 for obj in range(1,n):
  powers=[[1]+[0]*(n-1)]
  for r in range(1,height+1):powers.append([sum(powers[-1][i]*R[i][obj][j] for i in range(n)) for j in range(n)])
  for order in range(4,height+1):
   rs=tuple(int(r) for r in s.divisors(order) if r<order);types=rotation_types(data['F'],order,rs);nv=len(A[0]);nn=len(types)
   for row in A:row.extend([0]*nn)
   A.append([0]*nv+[1]*nn);b.append(powers[order][0])
   for at,r in enumerate(rs):
    k=order//r;co=[C(sum(powers[r][i]*v[i-1] for i in range(1,n)))*zv[v]*data['phases'][ti][k-1] for v,ti in labels]+[C.zero]*(nv-nh)+[-D*tt[at] for tt in types];rhs=-sum((C(powers[r][i])*low[i] for i in range(n)),C.zero)
    for row,val in rational_rows(co,rhs,C):A.append(row);b.append(val)
 return A,b

if __name__=='__main__':
 rid=sys.argv[1] if len(sys.argv)>1 else 'R6_4_22';height=int(sys.argv[2]) if len(sys.argv)>2 else 6;R=next(r['N'] for r in json.load(open(ROOT/'data/census.json')) if r['id']==rid);m.R=R
 start=time.monotonic();data=data_for(R,height);print('data',time.monotonic()-start,'types',len(data['phases']),flush=True);tab=table_for(R,data);cols=data['lows'][1];ep=(0,0,1,1,1) if rid.endswith('_22') else (0,0,-1,1,1);mod=forced_module_data(R);out=[]
 for lab in tab.assignments(cols):
  A,b,meta,labels=system(R,data,cols,ep,mod['objects'],True);A,b=rotations(R,data,cols,A,b,labels,height);A,b,meta=stronger_system(data,tab,cols,lab,A,b,labels);A,b,n=coupled(data,tab,cols,A,b,labels);A,b,labels,base=verlinde(R,data,tab,cols,lab,A,b,labels)
  if rid.endswith('_91'):
   C=data['C'];allowed={j for j,t in enumerate(data['phases']) if t in {tuple(C.unit**(a*k%16) for k in range(1,height+1)) for a in range(1,16,2)}};keep=[j for j in range(len(A[0])) if j>=len(labels) or not labels[j][0][2] or labels[j][1] in allowed];A=[[row[j] for j in keep] for row in A]
  print('startlp',rid,lab,len(A),len(A[0]),flush=True);aa=np.array(A,dtype=float);bb=np.array(b,dtype=float);scale=np.maximum(1,np.maximum(abs(aa).max(axis=1),abs(bb)));sol=linprog(np.zeros(len(A[0])),A_eq=aa/scale[:,None],b_eq=bb/scale,bounds=(0,None),options={'time_limit':120},method='highs');print('lp',sol.status,sol.message,flush=True)
  y=None
  if sol.status==2:
   y=farkas(A,b)
   if y is not None:check_farkas(A,b,y)
  out.append(dict(id=rid,height=height,lab=lab,status=sol.status,ray=y));Path(__file__).with_name(rid+'_h'+str(height)+'.json').write_text(json.dumps(out,indent=2))
