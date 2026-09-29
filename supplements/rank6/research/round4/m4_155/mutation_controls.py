import sys,json,copy
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'));base=Path(__file__).parent
import scipy.optimize

def disabled(*a,**kw):raise RuntimeError('optimizer disabled')
scipy.optimize.linprog=disabled;scipy.optimize.milp=disabled
import round4_155 as V
from exact import require,VerificationError
R=next(x['N'] for x in json.load(open(P/'data/census.json')) if x['id']=='R6_4_155');c=json.load(open(base/'exact_primal_certificates.json'))['certificates'][0];A,b,meta=V.primal_system(R,c);require(V.verify_primal_coordinates(R,c,A,b,meta)['passed'],'positive control failed');out=[]
for tag in ('nonzero_coordinate','missing_coordinate','nonintegral_coordinate','wrong_rank'):
 bad=copy.deepcopy(c)
 if tag=='nonzero_coordinate':bad['values'][0]=str(int(bad['values'][0])+1)
 elif tag=='missing_coordinate':bad['values'].pop()
 elif tag=='nonintegral_coordinate':bad['values'][0]='1/2'
 else:bad['center_rank']=str(int(bad['center_rank'])+1)
 try:V.verify_primal_coordinates(R,bad,A,b,meta)
 except VerificationError as e:out.append({'mutation':tag,'rejected':True,'reason':str(e)})
 else:raise RuntimeError('mutation accepted: '+tag)
(base/'mutation_controls.json').write_text(json.dumps({'passed':True,'optimized_python':not __debug__,'optimizer_used':False,'controls':out},indent=2)+'\n');print(out)
