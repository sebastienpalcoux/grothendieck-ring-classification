"""Exact component audit, relabelling, and corrupt-certificate controls."""
import copy,hashlib,json,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'software'))
import round3_integral_morita as IM;import stabilizer_rotation_higher as H
from rings import permute
from exact import VerificationError
D=Path(__file__).parent;C={r['id']:r['N']for r in json.load(open(ROOT/'data/census.json'))};out=[]
for name in ['R6_5_638','R6_7_1225']:
 start=time.monotonic();R=C[name];p=D/(name+'_higher_h6_integral_resumed.json');c=json.load(open(p))['certificate'];fixed,seed,nodes,reps=H.anti_representations(R,c['involution']);checks=0;corruptions=0
 for T,b in zip(reps,c['branches']):
  if b['method']!='morita_integral':continue
  A,rhs=H.C.morita_system(R,c['involution'],fixed,T)[0];IM.verify_system(A,rhs,b['integral']);checks+=1
  if checks!=1:continue
  cc=copy.deepcopy(b['integral']);cc['y']=[0]*len(cc['y'])
  bad=[cc,dict(b['integral'],modulus=1),dict(b['integral'],y=b['integral']['y'][:-1])]
  for badc in bad:
   try:IM.verify_system(A,rhs,badc)
   except (ValueError,AssertionError,VerificationError):corruptions+=1
   else:raise RuntimeError('corrupt modular certificate accepted')
  aa,bb=IM.reduced(A,rhs);i=next(i for i,v in enumerate(b['integral']['y'])if v%2)
  aa2=copy.deepcopy(aa);aa2[i][0]+=1;bb2=bb[:];bb2[i]+=1
  # verify_system resorts rows, so reconstruct the same modular pairings
  # directly to isolate corruption of a coefficient or the right side.
  y=b['integral']['y'];mod=b['integral']['modulus']
  if all(sum(y[k]*aa2[k][j]for k in range(len(aa2)))%mod==0 for j in range(len(aa2[0]))):raise RuntimeError('coefficient corruption invisible')
  if sum(v*z for v,z in zip(y,bb2))%mod!=0:raise RuntimeError('right-side corruption invisible')
  corruptions+=2
 pmap=[0,1,4,5,2,3];RR=permute(R,pmap);ff,se,nd,tt=H.anti_representations(RR,1);methods=[]
 for T in tt:
  ab,meta=H.C.morita_system(RR,1,ff,T)
  if ab is None:methods.append('rank');continue
  cert=IM.modular_ray(*IM.reduced(*ab),2)
  if cert is None:methods.append('survives')
  else:IM.verify_system(*ab,cert);methods.append('modular')
 if (methods.count('rank'),methods.count('modular'),methods.count('survives'))!=(2,12,2):raise RuntimeError('relabelled exhaustive module coverage changed')
 out.append({'id':name,'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'modular_branches_checked':checks,'corruptions_detected':corruptions,'basis_permutation':pmap,'permuted_module_methods':methods,'seconds':time.monotonic()-start,'optimized_python':not __debug__})
 (D/'integral_audit.json').write_text(json.dumps({'passed':True,'scope':'integral Morita component; central trace and signed reduction replay recorded separately','results':out},indent=2)+'\n');print(name,'PASSED',out[-1]['seconds'],flush=True)
