"""Optimizer-free replay of further necessary checks, with no existence claim."""
import contextlib,hashlib,io,json,runpy,shutil,sys,tempfile,time
from pathlib import Path
P=Path(__file__).resolve().parents[3];here=Path(__file__).parent;sys.path.insert(0,str(P/'software'))
import scipy.optimize
def forbidden(*args,**kwargs):raise RuntimeError('Numerical optimizers disabled')
scipy.optimize.linprog=forbidden;scipy.optimize.milp=forbidden
from exact import require
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
chain=[('center_indicators.py','center_indicators.json'),('indicator_integrality.py','indicator_integrality.json'),('vafa_check.py','vafa_check.json'),('generalized_rotation_spectra.py','generalized_rotation_spectra.json'),('relative_rotation.py','relative_rotation.json')]
start=time.monotonic();checks=[]
with tempfile.TemporaryDirectory(dir=here.parent,prefix='m4_629_checks_') as tmp:
 work=Path(tmp)
 for name in ('decoded_twists.json','rank35_modular_completions.json','rank35_fusion_data.json'):shutil.copyfile(here/name,work/name)
 for script,output in chain:
  shutil.copyfile(here/script,work/script)
  with contextlib.redirect_stdout(io.StringIO()):runpy.run_path(str(work/script),run_name='__main__')
  record=load(work/output);require(record==load(here/output),'Additional check differs: '+output)
  if output=='center_indicators.json':require(record['valid_self_dual_indicators'],'second indicators fail')
  elif output=='vafa_check.json':require(not record['failures'],'Vafa congruences fail')
  elif output=='generalized_rotation_spectra.json':require(all(x['obstruction'] is None for x in record),'charged rotation spectrum fails')
  else:require(all(not x['failures'] for x in record),'indicator test fails')
  checks.append({'script':script,'script_sha256':sha(here/script),'output':output,'output_sha256':sha(here/output),'passed':True});print('Rebuilt',output,flush=True)
 receipt={'passed':True,'python_optimization_level':sys.flags.optimize,'optimizer_disabled':True,'scope':'additional necessary tests of the retained modular datum','category_constructed':False,'ring_status':'unresolved','checks':checks,'elapsed_seconds':round(time.monotonic()-start,3)}
 (here/'additional_tests_replay_O.json').write_text(json.dumps(receipt,indent=2));print(json.dumps({'passed':True,'elapsed_seconds':receipt['elapsed_seconds'],'ring_status':'unresolved'}),flush=True)
