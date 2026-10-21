"""Independent reconstruction of central action and complete joint phase domain."""
from collections import Counter
from pathlib import Path
import json
from domain_probe import rows_for
from verify_frame01 import require
HERE=Path(__file__).resolve().parent

def verify(C,ring,central,domains):
 d=json.loads((HERE/'frame2_system.json').read_text());P=json.loads((HERE.parents[2]/'evidence/rank8_frontier_20261021/commutative_integer/R8_3_982_profile.json').read_text())['records'][2]
 low=Counter(map(tuple,P['low_columns']));unit=(1,0,0,0,0,0,0,0);require(low[unit]==1,'kernel low source unit not unique')
 actual_low=[unit]+[tuple(C.low[j][1])for j in C.frames[2]];require(list(map(list,actual_low))==P['low_columns'],'complete low source profile differs')
 perm=[]
 for row in ring['tensor'][6]:require(sum(row)==1 and 1 in row,'source g is not invertible');perm.append(row.index(1))
 dual=[next(j for j in range(8)if ring['tensor'][i][j][0])for i in range(8)]
 act=lambda v:tuple(v[perm[i]]for i in range(8));star=lambda v:tuple(v[dual[i]]for i in range(8))
 vs={r['index']:(0,)+tuple(r['vector'])for r in P['high_vectors']};orbits=[tuple(vs[j]for j in x['indices'])for x in P['duality_orbits']];lookup={v:j for j,o in enumerate(orbits)for v in o}
 keep=d['metadata']['source_metadata']['retained_indices'];pos={j:k for k,j in enumerate(keep)};lower=d['source_lower'];n=len(keep);equations=set();parities=set()
 def equation(coef,b):
  row=[0]*n
  for j,a in coef.items():
   b-=a*lower[j]
   if j in pos:row[pos[j]]+=a
  if any(row):equations.add(tuple(row+[b]))
  else:require(b==0,'forced central action scalar contradiction')
 for j,orbit in enumerate(orbits):
  for v in orbit:
   w=act(v)
   if v[6]:equation({j:1},low[w])
   elif w not in lookup:equation({j:1},0)
   elif lookup[w]!=j:equation({j:1,lookup[w]:-1},0)
   if w==v or w==star(v):
    if j in pos:parities.add((pos[j],(-lower[j])%2,j))
    else:require(lower[j]%2==0,'fixed invariant restriction has odd mass')
 basecount=len(d['rhs']);allrows=[tuple(row)+(b,)for row,b in zip(zip(*central['columns']),central['rhs'])]
 require(allrows[:basecount]==[tuple(row)+(b,)for row,b in zip(zip(*d['columns']),d['rhs'])],'central adapter altered base equations')
 require(set(allrows[basecount:])==equations,'central action equation coverage differs')
 require(set(map(tuple,central['central_action_parities']))==parities,'semion and duality parity coverage differs')
 _,derived,rank=rows_for('central_dual_frame2');rr=derived[len(central['rhs']):len(central['rhs'])+rank]
 J=json.loads((HERE/'joint_phase_system.json').read_text());phase_lookup={tuple(sorted((0,)+tuple(C.a['high'][i][0])for i in o)):j for j,o in enumerate(C.orbits)}
 highs=[]
 for j,o in enumerate(orbits):
  upper=lower[j]+max(domains[pos[j]])if j in pos else lower[j]
  if upper:highs.append((j,phase_lookup[tuple(sorted(o))],upper))
 require(len(highs)==J['high_orbits']and C.nt==J['phase_types'],'joint full-domain size mismatch')
 ep=J['indicators'];require(ep==[0,0,0,0,1,-1,-1],'wrong residual indicator assignment');fixed=C.column(2)
 rhs=[r[-1]for r in rr]+[lower[j]for j,o,u in highs]+[b-fixed.get(i,0)for i,b in enumerate(C.rhs_for(ep))]
 cols=[{i:r[j]for i,r in enumerate(rr)if r[j]}for j in range(n)];bounds=[(min(x),max(x))for x in domains];labels=[('integer_core',j)for j in range(n)]
 for h,(j,oi,u)in enumerate(highs):
  if j in pos:cols[pos[j]][rank+h]=-1
  for t in range(C.nt):
   col={rank+len(highs)+i:a for i,a in C.column(C.offset+oi*C.nt+t).items()};col[rank+h]=1;cols.append(col);bounds.append((0,u));labels.append(('high_phase',j,oi,t))
 for at in range(C.high_end,C.nvars):cols.append({rank+len(highs)+i:a for i,a in C.column(at).items()});bounds.append((0,None));labels.append(('phase_auxiliary',at))
 require(len(cols)==J['unshifted_variables'],'unshifted domain size differs')
 for j,(l,u)in enumerate(bounds):
  for i,a in list(cols[j].items()):rhs[i]-=a*l
  if u is not None:
   row=len(rhs);rhs.append(u-l);cols[j][row]=1;cols.append({row:1});labels.append(('bound_complement',j))
 require(rhs==J['rhs'],'joint source rhs differs')
 require(cols==[{int(i):a for i,a in c.items()}for c in J['columns']],'joint complete source columns differ')
 require([list(v)for v in labels]==J['labels']and [list(v)for v in bounds]==J['original_bounds'],'joint source labels or bounds differ')
 return {'central_action_equalities':len(equations),'semion_duality_parity_variables':len(parities),'joint_phase_complete_high_orbits':len(highs),'phase_types':C.nt,'joint_source_columns':len(cols),'joint_source_rows':len(rhs),'source_rebuilt_exactly':True}
