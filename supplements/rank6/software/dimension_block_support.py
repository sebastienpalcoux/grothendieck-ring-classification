"""Exact twist support from a saturated dimension-block conductor bound.

The equality lemma is proved in the manuscript's signed-character chapter.
This module uses dimension-field Galois characters, not center labels.
"""
import itertools,math
import sympy as s
from exact import require,evaluate,field

def saturated_characters(data):
 C=data['C'];F=data['F'];D=data['DD'];dims=data['dims']
 units=[a for a in range(F) if math.gcd(a,F)==1]
 auto=lambda x,a:evaluate(x.to_list(),C.unit**a,C)
 orbit=list(dict.fromkeys(tuple(auto(x,a) for x in dims) for a in units))
 reps=[next(a for a in units if tuple(auto(x,a) for x in dims)==v) for v in orbit]
 ix={a:orbit.index(tuple(auto(x,a) for x in dims)) for a in units};n=len(orbit)
 require(n<=6,'dimension-field character enumeration unsupported beyond degree six')
 identity=ix[1];mult=[[ix[a*b%F] for b in reps] for a in reps];orders=[]
 for j in range(n):
  a=j;k=1
  while a!=identity:a=mult[a][j];k+=1
  orders.append(k)
 L=math.lcm(*orders);EF=math.lcm(F,L)
 E=C if EF==F else field(s.Poly(s.cyclotomic_poly(EF,s.Symbol('t')),s.Symbol('t')))
 embed=lambda x:x if E==C else evaluate(x.to_list(),E.unit**(EF//F),E)
 values=[embed(auto(D,a)) for a in reps];chars=[];total_count=0
 for phase in itertools.product(range(L),repeat=n):
  if phase[identity] or any((phase[i]+phase[j]-phase[mult[i][j]])%L for i in range(n) for j in range(n)):continue
  total_count+=1
  f=next(int(d) for d in s.divisors(F) if all(a%d!=b%d or phase[ix[a]]==phase[ix[b]] for a in units for b in units))
  weights=[E.unit**(EF//L*k) for k in phase]
  value=sum((w/v for w,v in zip(weights,values)),E.zero)
  square=value*evaluate(value.to_list(),E.unit**(EF-1),E)
  if square==E.one/E(f):chars.append(dict(conductor=f,phases=list(phase),weights=weights,fourier=value))
 require(total_count==n,'incomplete Galois character enumeration')
 return dict(C=C,E=E,F=F,EF=EF,D=D,dims=dims,reps=reps,root_order=L,characters=chars)

def restriction_order_bounds(data,columns):
 """Return m_v: every simple with column v has theta^m_v=1; 0=no bound."""
 pack=saturated_characters(data);C=pack['C'];E=pack['E'];F=pack['F'];EF=pack['EF'];D=pack['D']
 embed=lambda x:x if E==C else evaluate(x.to_list(),E.unit**(EF//F),E)
 answer=[]
 for v in columns:
  require(len(v)==len(data['dims']),'full restriction column required')
  x=sum((C(k)*d for k,d in zip(v,data['dims'])),C.zero)/D
  values=[embed(evaluate(x.to_list(),C.unit**a,C)) for a in pack['reps']]
  active=[];coefficients=[]
  for ch in pack['characters']:
   z=sum((a*b for a,b in zip(ch['weights'],values)),E.zero)
   coefficients.append(list(map(str,z.to_list())))
   if z:active.append(ch['conductor'])
  answer.append(dict(column=list(v),order_bound=math.gcd(*active) if active else 0,active_conductors=active,coefficients=coefficients))
 metadata=dict(ambient_conductor=F,calculation_conductor=EF,galois_representatives=pack['reps'],character_root_order=pack['root_order'],
   saturated_characters=[dict(conductor=ch['conductor'],phases=ch['phases'],fourier=list(map(str,ch['fourier'].to_list()))) for ch in pack['characters']])
 return dict(metadata=metadata,columns=answer)

def phase_is_allowed(data,phase,order_bound):
 """Exact projected trace tuple filter when forced roots lie in the ambient field."""
 if not order_bound:return True
 C=data['C'];F=data['F'];require(F%order_bound==0,'forced roots require a larger retained field')
 return any(tuple(C.unit**((F//order_bound)*k*j) for j in range(1,len(phase)+1))==tuple(phase) for k in range(order_bound))
