"""Independent Sturm/Galois audit of the quartic trace chart.
Coefficient search, exact Sturm root counts and SymPy Galois groups do not
use the submitted resolvent witnesses or its positivity/normality tests.
"""
import json, hashlib, time
from pathlib import Path
import sympy as S
from sympy.polys.numberfields import galois_group
from paths import repository_root
ROOT=repository_root()
x=S.Symbol('x'); start=time.monotonic(); rows=[]; counts=dict(coefficients=0,newton=0,discriminant=0,totally_positive=0,irreducible=0)
for h in (1,4):
 for t in range(4,14):
  for s in range(1,3*t*t//8+1):
   for r in range(1,t**3//16+1):
    counts['coefficients']+=1
    if h==4 and (t%2 or s%2 or r%4): continue
    if 4*s*s<9*t*r or 3*r*r<8*s*h: continue
    counts['newton']+=1
    # Standard discriminant of x^4-t*x^3+s*x^2-r*x+h.
    disc=256*h**3-192*t*r*h*h-128*s*s*h*h+144*s*r*r*h-27*r**4+144*t*t*s*h*h-6*t*t*r*r*h-80*t*s*s*r*h+18*t*s*r**3+16*s**4*h-4*s**3*r*r-27*t**4*h*h+18*t**3*s*r*h-4*t**3*r**3-4*t*t*s**3*h+t*t*s*s*r*r
    if disc<=0: continue
    counts['discriminant']+=1
    f=S.Poly([1,-t,s,-r,h],x)
    if f.count_roots(0,S.oo)!=4: continue
    counts['totally_positive']+=1
    if not f.is_irreducible: continue
    counts['irreducible']+=1
    G,_=galois_group(f)
    if not G.is_abelian: continue
    rows.append({'polynomial':[1,-t,s,-r,h], 'group':'C4' if G.is_cyclic else 'V4'})
reference=ROOT/'supplements/rank4/unrestricted/audit/quartic_trace13_exact_resolvent_chart.json'
expected=[{'polynomial':a['polynomial'],'group':a['group']} for a in json.loads(reference.read_text())]
rows.sort(key=lambda a:(-a['polynomial'][1],a['polynomial'][2],-a['polynomial'][3],a['polynomial'][4]))
if rows!=expected: raise RuntimeError({'computed':rows,'expected':expected})
out={'status':'PASS','counts':counts,'rows':rows,'elapsed_seconds':time.monotonic()-start,'reference_sha256':hashlib.sha256(reference.read_bytes()).hexdigest()}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
