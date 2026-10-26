from pathlib import Path
import sys,json,time
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'d32'))
from nonsplit_ising import sparse_solve,feudal,common
for name in ['sylow_a10','sylow_a01']:
 R=json.loads((HERE/(name+'.json')).read_text());z=feudal.setup(R,variable_tau=True);q=16
 A=z['equations'];B=[b[0]*(q//2)for b in z['B']];x,stats=sparse_solve(A,B,q,len(z['keys']))
 out={'name':name,'modulus':q,'equations':len(A),'variables':len(z['keys']),'solution_exists_in_this_phase_grid':x is not None,'stats':stats,'finite_failure_is_not_exclusion':True}
 if x is not None:
  common.require(all((sum(v*x[k]for k,v in a.items())-b)%q==0 for a,b in zip(A,B)),'all original Liptrap equations')
  out['certificate']=dict(kind='liptrap_unitary_model',modulus=q,serfs=z['S'],lords=z['M'],stabilizer=z['H'],tau_times_tau_dual='1/2',tau='phase_times_inverse_square_root',bicharacter_assignment=list(z['assignments'][0]),phase_values=[list(k)+[x[i]]for i,k in enumerate(z['keys'])],reference='Liptrap 1002.3166v2 Definition4.3, Theorem4, Lemma5.4')
  out['verification']=feudal.check_positive(R,out['certificate'])
 (HERE/(name+'_test.json')).write_text(json.dumps(out,indent=2)+'\n')
 print(name,'positive?',x is not None)
