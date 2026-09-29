"""Exact cyclic cocycle restrictions and fourth indicators, exponents modulo 4."""
import itertools,json
from pathlib import Path
out=[]
for k in range(4):
 def omega(a,b,c):return k*a*((b+c)//4)%4
 for a,b,c,d in itertools.product(range(4),repeat=4):
  if (omega(b,c,d)+omega(a,(b+c)%4,d)+omega(a,b,c)-omega((a+b)%4,c,d)-omega(a,b,(c+d)%4))%4:
   raise ValueError('cyclic cocycle equation failed')
 def nu4(a):return sum(omega(a,(j*a)%4,a) for j in range(4))%4
 rec={'class':k,'restriction_to_H_exponent_mod4':omega(2,2,2),'nu4_t_exponent_mod4':nu4(1),'nu4_inverse_exponent_mod4':nu4(3)}
 if rec['restriction_to_H_exponent_mod4']!=2*(k%2) or rec['nu4_t_exponent_mod4']!=k or rec['nu4_inverse_exponent_mod4']!=9*k%4:
  raise ValueError('wrong cyclic restriction or indicator')
 out.append(rec)
Path(__file__).with_suffix('.json').write_text(json.dumps({'convention':'omega_k(a,b,c)=i^(k*a*floor((b+c)/4)); normalized PU cyclic cocycle indicators','all_1024_cocycle_identities':True,'records':out,'forced_class':2,'forced_both_indicators':-1},indent=2)+'\n')
print('All 1024 cocycle identities, restrictions, and fourth indicators verified.')
