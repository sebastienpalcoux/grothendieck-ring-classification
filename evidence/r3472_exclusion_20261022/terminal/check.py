"""Exact bounded-integer certificate replay; standard library only, no solver."""

if not __debug__:
    raise RuntimeError('Proof verification requires assertions enabled; run without -O.')
from pathlib import Path
from fractions import Fraction as Q
import json,math,hashlib
import sys
B=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).resolve().parent
used=[]
def read(name):
 p=B/name;used.append(p);return json.loads(p.read_text())
models=read('models.json');base=models['base'];field=models['field']
for model in (base,field):model['rows']=[dict(r)for r in model['rows']]
assert field['orders']==base['orders']
assert field['rows'][:len(base['rows'])]==base['rows'] and field['rhs'][:len(base['rhs'])]==base['rhs']
rows=[{int(k):int(v)for k,v in r.items()}for r in base['rows']];rhs=list(map(int,base['rhs']));bounds=[(int(l),int(u))for l,u in zip(base['lo'],base['up'])]
def interval_bound(covector,objective=None,upper=False):
 a=[Q(0)for _ in bounds];v=Q(0);assert len({i for i,z in covector})==len(covector)
 for i,z in covector:
  z=Q(z);v+=z*rhs[i]
  for j,k in rows[i].items():a[j]+=z*k
 if objective is None:return v-sum(max(c*l,c*u)for c,(l,u)in zip(a,bounds))
 j,sign=objective;a=[Q(sign*int(k==j))-c for k,c in enumerate(a)]
 return v+sum(min(c*l,c*u)for c,(l,u)in zip(a,bounds))
first=read('certified_orbit_bounds.json')
for c in first['changes']:
 j=c['variable'];v=interval_bound(c['covector'],(j,-1));assert -v==Q(c['exact_upper']);u=math.floor(-v);assert u==c['new_upper']and bounds[j][0]<=u<=bounds[j][1];bounds[j]=(bounds[j][0],u)
assert bounds==list(map(tuple,first['bounds']))
counts=[len(first['changes'])]
for filename,extend in [('certified_all_bounds.json',False),('certified_field_bounds.json',True)]:
 if extend:
  assert bounds==list(zip(field['lo'],field['up']));rows=[{int(k):int(v)for k,v in r.items()}for r in field['rows']];rhs=list(map(int,field['rhs']))
 cert=read(filename);count=0
 for changes in cert['history']:
  for c in changes:
   j=c['variable'];sign=c['sign'];assert sign in(1,-1)and bounds[j]==tuple(c['old_bounds']);v=interval_bound(c['covector'],(j,sign));assert v==Q(c['exact_opt_bound']);b=math.ceil(v)if sign==1 else math.floor(-v);assert b==c['new_bound']and bounds[j][0]<=b<=bounds[j][1]
   bounds[j]=(b,bounds[j][1])if sign==1 else(bounds[j][0],b);count+=1
 assert bounds==list(map(tuple,cert['bounds']));counts.append(count)
final=read('final_field_farkas.json');assert bounds==list(map(tuple,final['bounds']));gap=interval_bound(final['covector']);assert gap==Q(final['exact_separation'])and gap>0
out={'status':'PASS_EXACT_TERMINAL_CONTRADICTION','cut_counts':counts,'total_integer_rounding_cuts':sum(counts),'final_rows':len(rows),'variables':len(bounds),'final_positive_separation':str(gap),'final_covector_support':len(final['covector']),'sha256':{str(p):hashlib.sha256(p.read_bytes()).hexdigest()for p in used},'scope':'Entire cut chain and terminal contradiction verified with Fraction arithmetic, against the bundled integer models; no numerical solver used.'}
print(json.dumps({k:v for k,v in out.items()if k!='sha256'},indent=2))
