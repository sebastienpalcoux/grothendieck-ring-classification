# Locate the enclosing frozen release or the explicitly supplied base.
import os as _task_os
from pathlib import Path as _TaskPath
def _find_release():
    if _task_os.environ.get("RANK6_PACKAGE"):
        return _TaskPath(_task_os.environ["RANK6_PACKAGE"]).resolve()
    for _p in _TaskPath(__file__).resolve().parents:
        for _c in (_p, _p / "Rank6_Categorification_M9"):
            if (_c / "software/round3_m4.py").is_file() and (_c / "data/census.json").is_file():
                return _c
    raise FileNotFoundError("Set RANK6_PACKAGE to the extracted multiplicity-nine package")
_TASK_PACKAGE = _find_release()

"""Independent tiny replay of the R1660 low-frame-zero profile-133 cut."""
from pathlib import Path
import hashlib,itertools,json
HERE=Path(__file__).resolve().parent
P=_TASK_PACKAGE
source=P/'research/round5/m8_1660/low0_profiles.json'
raw=json.loads(source.read_text())['branches'][0]
case=next(x for x in raw['cases']if x['labelling']==[0,5,4,1,3,2])
counts={tuple(v):n for v,n in zip(raw['high_vectors'],case['profiles'][133])if n}
for low in raw['columns'][:4]:
 v=(low[0],low[3],low[2],low[4],low[5])
 counts[v]-=1
counts={v:n for v,n in counts.items()if n}
vectors=[(0,0,0,0,1),(0,1,1,0,2),(0,2,2,0,2),(0,2,2,0,3),
         (0,2,2,1,3),(0,4,4,0,4),(0,4,4,0,8)]
n=[2,2,1,2,8,2,1]
if counts!=dict(zip(vectors,n)):raise ValueError('Unexpected residual profile')
weights=[(2,0),(12,8),(24,16),(34,24),(36,24),(96,64),(192,128)]
for v,(a,b)in zip(vectors,weights):
 if not v[3]:
  x=v[1]+v[2];y=v[4]
  if(a,b)!=(x*x+2*y*y,2*x*y):raise ValueError('Weight mismatch')

even=[]
for e in itertools.product(range(2),range(2),(0,),range(2),(0,2,4),range(2),(0,)):
 if tuple(sum(e[i]*weights[i][j]for i in range(7))for j in range(2))==(180,120):
  E=sum(e);O=sum(n)-3*E-3;T=4*E+6-sum(n)
  even.append({'e':e,'E':E,'O':O,'T':T})
if len(even)!=2:raise ValueError('Unexpected dimension solutions')
admissible=[x for x in even if min(x['O'],x['T'])>=0]
if len(admissible)!=1:raise ValueError('Unexpected nonnegative rank solution')
row=admissible[0];e=row['e'];before=[];after=[]
for o in itertools.product(*(range((n[i]-2*e[i])//2+1)for i in range(7))):
 t=[n[i]-2*e[i]-2*o[i]for i in range(7)]
 if sum(o)!=row['O'] or sum(t)!=row['T']:continue
 if o[0]!=o[3] or t[0]!=t[3]:continue # Galois swaps types zero and three.
 before.append({'o':o,'t':t})
 if t[4]%4==0:after.append({'o':o,'t':t})
if len(before)!=1 or before[0]['t'][4]!=2 or after:
 raise ValueError('One-profile contradiction was not reproduced')
out={'ring':'R6_8_1660','low_frame':0,'labelling':case['labelling'],
 'profile_index_zero_based':133,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
 'residual_vectors':vectors,'multiplicities':n,'even_dimension_solutions':even,
 'rank_and_galois_compatible_orbit_assignment':before,
 'forced_sigma_h_fixed_count':2,'necessary_sigma_h_fixed_divisor':4,
 'excluded':True,'optimizer_used':False,
 'independence':'Does not import the new Galois verifier or its dynamic program.'}
(HERE/'galois_cut_audit.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
