import sys,json,time,copy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'software'))
import round3_commutative_sector as M
from exact import VerificationError
import scipy.optimize as opt
for name in ['linprog','milp','minimize','least_squares']:
 setattr(opt,name,lambda *a,**k:(_ for _ in ()).throw(RuntimeError('optimizer disabled')))
rings={r['id']:r['N']for r in json.load(open(ROOT/'data/census.json'))};out=[]
for rid in ['R6_7_200','R6_8_491']:
 c=json.load(open(Path(__file__).with_name(rid+'_comm_certificate.json')));start=time.monotonic();report=M.verify(rings[rid],c)
 mutations=[]
 if rid=='R6_7_200':
  bad=copy.deepcopy(c);bad['original_matrix_block_formal_codegree']='24'
  try:M.verify(rings[rid],bad);mutations.append(False)
  except VerificationError:mutations.append(True)
  bad=copy.deepcopy(c);bad['branches'].pop()
  try:M.verify(rings[rid],bad);mutations.append(False)
  except VerificationError:mutations.append(True)
  bad=copy.deepcopy(c);bad['all_values'].pop()
  try:M.verify(rings[rid],bad);mutations.append(False)
  except VerificationError:mutations.append(True)
 out.append({'id':rid,'report':report,'optimized_python':not __debug__,'optimizers_disabled':True,'mutation_controls':mutations,'seconds':time.monotonic()-start});print(out[-1],flush=True)
Path(__file__).with_suffix('.json').write_text(json.dumps({'passed':all(all(x['mutation_controls'])for x in out),'results':out},indent=2)+'\n')
