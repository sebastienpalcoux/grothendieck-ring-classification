"""Exact pointed positive control: Semion tensor reverse Semion."""
from pathlib import Path
import itertools,json
HERE=Path(__file__).resolve().parent
objects=list(itertools.product(range(2),repeat=2))
def mul(x,y):return tuple((a+b)%2 for a,b in zip(x,y))
# Twists encoded as exponents of i; all simples are self-dual.
twist={(0,0):0,(1,0):1,(0,1):3,(1,1):0};G=(1,0)
# Explicit pointed associator and braiding: exponents modulo4 of i.
def omega(a,b,c):return 2*sum(x*y*z for x,y,z in zip(a,b,c))%4
def braid(a,b):return (a[0]*b[0]-a[1]*b[1])%4
for a,b,c,d in itertools.product(objects,repeat=4):
 if (omega(b,c,d)+omega(a,mul(b,c),d)+omega(a,b,c)-omega(mul(a,b),c,d)-omega(a,b,mul(c,d)))%4:raise AssertionError('pointed pentagon fails')
for a,b,c in itertools.product(objects,repeat=3):
 if (braid(a,mul(b,c))-braid(a,b)-braid(a,c)-omega(b,a,c)+omega(b,c,a)+omega(a,b,c))%4:raise AssertionError('first pointed hexagon fails')
 if (braid(mul(a,b),c)-braid(a,c)-braid(b,c)-omega(a,b,c)-omega(c,a,b)+omega(a,c,b))%4:raise AssertionError('second pointed hexagon fails')
# Nondegenerate monodromy bicharacter: each nontrivial simple pairs nontrivially.
for a in objects[1:]:
 if all((braid(a,b)+braid(b,a))%4==0 for b in objects):raise AssertionError('degenerate pointed braiding')
records=[]
for Z in objects:
 GZ=mul(G,Z);dual=Z;HZ=mul(G,dual)
 monodromy=(twist[GZ]-twist[G]-twist[Z])%4
 if monodromy not in(0,2):raise AssertionError('monodromy is not a sign')
 if GZ==Z or GZ==dual or HZ==Z:raise AssertionError('semion action unexpectedly fixed')
 if mul(G,GZ)!=Z or mul(G,HZ)!=Z:raise AssertionError('action is not involutive')
 records.append({'Z':Z,'theta_exponent':twist[Z],'GZ':GZ,'G_dual_Z':HZ,'monodromy_exponent':monodromy})
result={'model':'Semion tensor reverse Semion (double semion)','actual_modular_category':True,'explicit_associator_pentagons':256,'explicit_braiding_hexagons':128,'nondegenerate_braiding':True,'simple_count':4,'semion_G':G,'G_order':2,'G_twist_exponent':1,'G_free':True,'G_duality_free':True,'records':records}
(HERE/'semion_action_control.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS actual double-semion free central and central-duality actions')
