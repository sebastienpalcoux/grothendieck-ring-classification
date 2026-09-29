import sys,json,math,itertools,time
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'))
from exact import field,evaluate,require
from round3_m4 import relative_root
import sympy as s
st=time.monotonic();out=[]
for F in [3,5,15]:
 C=field(s.Poly(s.cyclotomic_poly(F,s.Symbol('t')),s.Symbol('t')))
 ps=list(map(int,s.factorint(F)));orders=[]
 for es in itertools.product(range(4),repeat=len(ps)):
  n=math.prod(p**e for p,e in zip(ps,es));d=int(s.totient(math.lcm(F,n))//s.totient(F))
  if d<=9 and n<=135:orders.append((n,d))
 for n,d in orders:
  L=math.lcm(F,n);E=field(s.Poly(s.cyclotomic_poly(L,s.Symbol('t')),s.Symbol('t')));H=[a for a in range(L) if math.gcd(a,L)==1 and a%F==1%F];sq={a*a%L for a in H};require(len(H)==d and sq==set(H),'wrong odd square action')
  for a in range(n):
   if math.gcd(a,n)>1:continue
   for j in range(1,7):
    direct=sum((E.unit**((L//n*a*j*b)%L) for b in sq),E.zero)
    predicted=E(d)*evaluate(relative_root(C,F,n,a*j).to_list(),E.unit**(L//F),E)
    require(direct==predicted,'relative square-orbit trace mismatch')
  out.append({'F':F,'order':n,'orbit_size':d,'primitive_roots':int(s.totient(n)),'powers':6,'passed':True})
record={'scope':'exact cyclotomic arithmetic, independently summing modular square action','cases':out,'comparisons':sum(x['primitive_roots']*x['powers'] for x in out),'passed':True,'seconds':time.monotonic()-st};Path(__file__).with_name('audit_orbit_formula_O.json' if not __debug__ else 'audit_orbit_formula.json').write_text(json.dumps(record));print({k:v for k,v in record.items() if k!='cases'})
