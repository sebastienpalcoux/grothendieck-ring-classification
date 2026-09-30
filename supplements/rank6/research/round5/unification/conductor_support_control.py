"""Saturated support control on the realized Fibonacci center."""
import hashlib,json,sys
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'))
from exact import require
from round3_m4 import data_for
from dimension_block_support import restriction_order_bounds,phase_is_allowed,saturated_characters
from equality_modrep import identities,phase_equations

R=[[[1,0],[0,1]],[[0,1],[1,1]]]
d=data_for(R,2,5)
# Z(Fib)=Fib x Fib^rev: restrictions 1, X, X, 1+X.
columns=[[1,0],[0,1],[0,1],[1,1]]
support=restriction_order_bounds(d,columns)
require([x['order_bound'] for x in support['columns']]==[1,5,5,1],'Fibonacci saturated support')
C=d['C'];twists=[C.one,C.unit**2,C.unit**3,C.one]
require(all(phase_is_allowed(d,(z,z*z),r['order_bound'])for z,r in zip(twists,support['columns'])),'realized Fibonacci twists lost')
require(not phase_is_allowed(d,(-C.one,C.one),5),'order-two mutation not rejected')
moment_checks=[]
for ch in saturated_characters(d)['characters']:
 cert=identities(d,ch)
 rows,rhs,forbidden=phase_equations(d,[[1]],[[1,0],[1,1]],cert)
 point=[0]*len(d['phases'])
 for z in twists[1:3]:point[d['phases'].index((z,z*z))]+=1
 require(all(not point[j] for j in forbidden),'realized root forbidden by conductor support')
 require(all(sum((v*n for v,n in zip(row,point)),cert['lambda_value']*0)==b for row,b in zip(rows,rhs)),'Fibonacci saturated modular moment')
 zero=d['phases'].index((C.one,C.one))
 failures=sum(2*row[zero]!=b for row,b in zip(rows,rhs))
 if ch['conductor']==5:
  require(failures>0,'trivialized twists must violate saturated moments')
  require(cert['forbidden_root_powers']==[1,4],'Fibonacci spectral projector support')
 moment_checks.append(dict(conductor=ch['conductor'],induced_dimension=cert['induced_dimension'],equality_dimension=cert['equality_dimension'],cyclic_dimension=cert['cyclic_dimension'],moment_relations=len(rows),forbidden_root_powers=cert['forbidden_root_powers'],all_twists_one_failures=failures))
out=dict(passed=True,optimizer_used=False,python_optimized=not __debug__,category='Fibonacci',center='Fibonacci x Fibonacci^rev',support=support,order_two_mutation_rejected=True,source_sha256={})
out['modular_moment_controls']=moment_checks
for name in ['software/dimension_block_support.py','research/round5/unification/equality_modrep.py','research/round5/unification/conductor_support_control.py']:
 out['source_sha256'][name]=hashlib.sha256((P/name).read_bytes()).hexdigest()
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
