"""Independent closed-form check of the finite quartic trace domains."""
import json,sys,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'software'))
import sympy as s
from exact import field,require
from cyclotomic_stabilizer_trace import trace_domain
reports=[]
for F,primes,outside in ((16,[2],[64,128]),(20,[2,5],[16,80,25,50,100,200])):
 K,actual,bound=trace_domain(F,primes,3);z=K.unit
 require(bound==2*F,'unexpected order-three conductor box')
 # The two relative conjugates of a primitive 2F-th root are theta,-theta.
 # Roots already in Q(zeta_F) have their ordinary powers as traces.
 expected={tuple(z**(j*a) for j in (1,2,3)) for a in range(F)}
 expected|={(K.zero,z**a,K.zero) for a in range(1,F,2)}
 expected.add((K.zero,K.zero,K.zero))
 require(set(actual)==expected,'kernel-generated phase set differs from closed form')
 require(len(actual)==3*F//2+1,'wrong closed-form phase count')
 controls=[]
 for order in outside:
  L=math.lcm(F,order);t=s.Symbol('t');W=field(s.Poly(s.cyclotomic_poly(L,t),t));w=W.unit
  kernel=[u for u in range(L) if math.gcd(u,L)==1 and u%F==1]
  for j in (1,2,3):
   total=sum((w**((u*j*(L//order))%L) for u in kernel),W.zero)
   require(total==W.zero,'outside-box root has nonzero relative trace')
  controls.append(order)
 reports.append({'ambient_conductor':F,'height':3,'order_bound':bound,'closed_form_phase_count':len(expected),'phase_sets_equal':True,'outside_orders_with_three_zero_traces':controls})
print(json.dumps({'complete':True,'reports':reports},indent=2))
