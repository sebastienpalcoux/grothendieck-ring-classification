import sys,json,itertools,time,math
from fractions import Fraction
from pathlib import Path
import numpy as np
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'));from round5_629 import *
from exact import vector
here=Path(__file__).parent;R,d,cols,lab,src=source_data();C=d['C'];conj=lambda z:ambient.evaluate(z.to_list(),C.unit**14,C);f=json.load(open(here/'rank35_fusion_data.json'));N=np.array(f['fusion_tensor'],dtype=object);br=next(x for x in json.load(open(here/'rank35_modular_completions.json'))['branches'] if x['signs']==f['signs']);S=[[C([s.Rational(z) for z in v]) for v in row] for row in br['S']];rank=35
case=next(x for x in json.load(open(here/'decoded_twists.json')) if x['rank']==35 and x['solution']==0);theta=[0]*6
for o in case['orbits']:theta.extend([15//o['root_order']*o['root_power']%15]*o['copies'])
out=[];st=time.monotonic();lam=[[S[a][j]/S[0][j] for j in range(rank)] for a in range(rank)]
for m in (2,3,5,7,11,13):
 Q=[[sum((S[i][k]*C.unit**(m*theta[k])*S[k][j] for k in range(rank)),C.zero) for j in range(rank)] for i in range(rank)];pairs={(b,c):[Q[b][j]*conj(Q[c][j]) for j in range(rank)] for b in range(rank) for c in range(b,rank)};bad=None;count=0
 if m in (3,5):
  Z=C.unit**(15//m);B=s.Matrix.hstack(*(vector(Z**i,8) for i in range(m-1)));piv=(B.T).rref()[1];L=B.extract(piv,range(m-1)).inv();Lf=[[Fraction(z) for z in row] for row in L.tolist()]
 for a in range(1,rank):
  H=np.eye(rank,dtype=object)
  for _ in range(m):H=H@N[a]
  for (b,c),vv in pairs.items():
   count+=1;dim=int(H[b,c]);z=sum((x*y for x,y in zip(lam[a],vv)),C.zero);dt=theta[b]-theta[c]
   if m in (3,5) and dt%m:
    if z:bad={'object':a,'pair':[b,c],'reason':'prime_extension_field','value':list(map(str,z.to_list()))};break
    if dim%m:bad={'object':a,'pair':[b,c],'reason':'zero_trace_congruence','dimension':dim};break
    continue
   z*=C.unit**((pow(m,-1,15)*dt)%15 if math.gcd(m,15)==1 else dt//m)
   if math.gcd(m,15)==1:
    zz=z.to_list();cc=[Fraction(str(zz[0]))] if len(zz)==1 else [Fraction(0)] if not zz else None
    if cc is None:bad={'object':a,'pair':[b,c],'reason':'not_rational','value':list(map(str,zz))};break
   else:
    zz=list(reversed(z.to_list()));zz=[Fraction(str(x)) for x in zz]+[Fraction(0)]*(8-len(zz));pp=[zz[j] for j in piv];cc=[sum((x*y for x,y in zip(row,pp)),Fraction(0)) for row in Lf]
    if sum((C(s.Rational(x.numerator,x.denominator))*Z**i for i,x in enumerate(cc)),C.zero)!=z:bad={'object':a,'pair':[b,c],'reason':'not_prime_cyclotomic','value':list(map(str,z.to_list()))};break
   base=(dim-sum(cc))/m;mu=[base+x for x in cc]+[base]*(m-len(cc))
   if any(x.denominator!=1 or x<0 for x in mu):bad={'object':a,'pair':[b,c],'reason':'nonpositive_nonintegral_rotation_spectrum','multiplicities':list(map(str,mu)),'dimension':dim,'trace':list(map(str,z.to_list()))};break
  if bad:break
 rec={'power':m,'checked':count,'obstruction':bad};out.append(rec);print(rec,'seconds',time.monotonic()-st,flush=True);(here/'generalized_rotation_spectra.json').write_text(json.dumps(out,indent=2))
