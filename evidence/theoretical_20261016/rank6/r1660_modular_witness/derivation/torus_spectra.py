"""Exact torus characters on U-fixed spaces from frozen finite-group tables."""
from pathlib import Path
import sys,json,itertools
import sympy as s
BASE=Path(__file__).resolve().parents[3]
P=BASE/'repo/supplements/rank6'
sys.path.insert(0,str(P/'research/round5/m8_modrep'))
import finite_spectra48 as F
C=F.coefficient_field()
units=[a for a in range(48) if s.gcd(a,48)==1]
fields=[1,8,12,24]
def require(x,message):
 if not x:raise ValueError(message)
local=[]
for m in (16,3):
 data=json.loads((P/f'research/round5/m8_modrep/sl2_{m}.json').read_text())
 ix={tuple(g):i for i,cl in enumerate(data['group']['classes']) for g in cl}
 rows=[]
 for r in data['irreps']:
  trace={}
  if r['T_multiplicities'][0]:
   ch=[C([s.Rational(a) for a in coeff]) for coeff in r['characters']]
   for a in sorted({b%m for b in units}):
    ai=pow(a,-1,m)
    trace[a]=sum((ch[ix[(a,a*j%m,0,ai)]] for j in range(m)),C.zero)/C(m)
  else:trace={a:C.zero for a in sorted({b%m for b in units})}
  require(trace[1]==C(r['T_multiplicities'][0]),'U-fixed dimension')
  rows.append((r,trace))
 local.append(rows)
records=[]
for i,(r,tr) in enumerate(local[0]):
 for j,(q,tq) in enumerate(local[1]):
  traces={a:tr[a%16]*tq[a%3] for a in units}
  weights=[]
  for f in fields:
   value=sum((C(int(s.kronecker_symbol(f,a)))*traces[a] for a in units),C.zero)/C(16)
   require(len(value.to_list())<=1,'nonrational torus multiplicity')
   v=s.Rational(value.to_list()[0]) if value.to_list() else s.S.Zero
   require(v.q==1 and v>=0,'torus multiplicity not a natural number')
   weights.append(int(v))
  t0=r['T_multiplicities'][0]*q['T_multiplicities'][0]
  spec=[0]*48
  for x,p in enumerate(r['T_multiplicities']):
   for y,v in enumerate(q['T_multiplicities']):spec[(3*x+16*y)%48]+=p*v
  records.append({'factors':[i,j],'degree':r['degree']*q['degree'],
                  'central_sign':r['central_sign']*q['central_sign'],
                  'spectrum':spec,'T0':t0,'torus_weights':weights,
                  'allowed':sum(weights)==t0})
out={'scope':'necessary torus character condition; no categorical conclusion',
     'target_weights':[3,1,1,1],'fundamental_discriminants':fields,
     'irreps':records}
(Path(__file__).parent/'torus_spectra.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':'PASS','irreps':len(records),
                  'allowed':sum(r['allowed'] for r in records),
                  'T0_positive_allowed':sum(r['allowed'] and r['T0']>0 for r in records),
                  'distinct_allowed_weights':sorted({tuple(r['torus_weights']) for r in records if r['allowed']})}))
