import sys,time,json,itertools,math
from pathlib import Path
import sympy as s
from sympy.polys.numberfields import round_two
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[3]/'software'))
from exact import field,embeddings,key,pc,evaluate,t
from new_biquadratic_trace import squarefree
start=time.monotonic()
for M,ys in [(5,[5,10]),(21,[7])]:
 print('FIELD',M,flush=True)
 f=s.Poly(t**4-41*M*t*t+164*M*M,t);K=field(f);a=K([1,0]);rt=(K(2)*a*a/K(M)-K(41))/K(5);D=K(3690)+K(576)*rt
 beta=(a*a*a-K(33*M)*a)/K(10*M)
 bas0=[K.one,(K.one+rt)/K(2),(K.one+rt+K(2)*a)/K(4),(K.one-rt+K(2)*beta)/K(4)]
 B=s.Matrix.hstack(*(s.Matrix(list(reversed([s.S.Zero]*(4-len(key(z)))+list(key(z))))) for z in bas0));disc=41**3*M**2;print('disc',disc,'basis',B,flush=True)
 E=embeddings(f)
 # numerical embedding matrix of O basis, solely discover a convenient unimodular basis
 def elem(v):return K(list(reversed(v)))
 bas=[elem(list(B[:,j])) for j in range(4)]
 def approx(e,z):return float(sum(s.Rational(c)*((e.lo+e.hi)/2)**i for i,c in enumerate(reversed(key(z)))))
 em=s.Matrix([[round(100000*approx(e,b)) for e in E] for b in bas])
 _,U=em.lll_transform();B=B*U.T;bas=[elem(list(B[:,j])) for j in range(4)]
 emb=np.array([[approx(e,b) for b in bas] for e in E]);weights=np.linalg.inv(emb)@np.diag([1/(18*approx(e,rt)) for e in E])
 trace=lambda z:sum(K.to_sympy(z).subs(K.ext.as_expr(),x) for x in s.nroots(f.as_expr()))
 # exact regular trace
 def tr(z):
  powers=[K.one,a,a*a,a*a*a]
  A=s.Matrix.hstack(*(s.Matrix(list(reversed([s.S.Zero]*(4-len(key(z*v)))+list(key(z*v))))) for v in powers))
  return int(s.trace(A))
 tracevec=[tr(K(18)*rt*b) for b in bas];print('B',B,'trace',tracevec,flush=True)
 counts=[0,0,0];survive=[]
 for y in ys:
  T=738*y
  bounds=[(math.floor(T*min(row))-2,math.ceil(T*max(row))+2) for row in weights]
  pivot=max(range(4),key=lambda j:abs(tracevec[j]));others=[j for j in range(4) if j!=pivot]
  print('Y',y,'bounds',bounds,'pivot',pivot,'box',math.prod(bounds[j][1]-bounds[j][0]+1 for j in others),flush=True)
  for zs in itertools.product(*(range(bounds[j][0],bounds[j][1]+1) for j in others)):
   top=T-sum(tracevec[j]*v for j,v in zip(others,zs))
   if top%tracevec[pivot]:continue
   z=[0]*4
   for j,v in zip(others,zs):z[j]=v
   z[pivot]=top//tracevec[pivot]
   if not bounds[pivot][0]<=z[pivot]<=bounds[pivot][1]:continue
   # cheap float rejection well away from boundary; exact positive tests below
   vals=emb@np.array(z)
   if any(vals[i]*approx(E[i],rt)<-1e-5 for i in range(4)):continue
   theta=sum((K(v)*b for v,b in zip(z,bas)),K.zero);delta=K(18)*rt*theta
   if any(e.sign(delta)<=0 for e in E):continue
   counts[0]+=1
   pp=s.Poly(s.minpoly(K.to_sympy(delta),t),t)
   # dimension codegrees use all four K embeddings, even if delta nonprimitive
   P=pp**(4//pp.degree());co=list(map(int,P.all_coeffs()));norm=co[-1]
   if any(co[j]**4%norm**j for j in range(1,5)):continue
   counts[1]+=1
   inv=tr(K.one/delta); # NOT integral in general! handle below
   # trace rational exact instead
   powers=[K.one,a,a*a,a*a*a];zz=K.one/delta
   A=s.Matrix.hstack(*(s.Matrix(list(reversed([s.S.Zero]*(4-len(key(zz*v)))+list(key(zz*v))))) for v in powers))
   remain=1-s.trace(A)
   if remain<=0:continue
   AA,BB=map(int,s.fraction(remain));pairs=[]
   for j in range(1,(7416-T)//AA+1):
    S,P=AA*j,BB*j;dis=S*S-4*P
    if dis<0 or S<=2 or P-S+1<=0:continue
    sq=math.isqrt(dis)
    if sq*sq==dis:
     if (S-sq)%2 or (S-sq)//2<=1:continue
    elif S*S%P or squarefree(dis)[1]!=41:continue
    pairs.append([S,P])
   if pairs:counts[2]+=1;survive.append({'M':M,'y':y,'theta_coordinates':z,'theta_power':[str(c) for c in key(theta)],'delta_polynomial':co,'pairs':pairs})
  print('YDONE',y,counts,'seconds',time.monotonic()-start,flush=True)
 Path(f'research/round3/arithmetic/quartic_{M}_exploration.json').write_text(json.dumps({'M':M,'discriminant':int(disc),'basis':[[str(x) for x in row] for row in B.tolist()],'trace':tracevec,'counts':counts,'survivors':survive},indent=2)+'\n')
 print('SURVIVORS',M,len(survive),flush=True)
