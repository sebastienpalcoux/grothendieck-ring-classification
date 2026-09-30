"""Rebuild the complete R6_4_629 frontier reduction with optimizers disabled.

Run from any directory, preferably ``python -O replay_modular_chain.py``.
All generated computations run in an automatically removed temporary directory.
The inherited exact reduction to the three input profiles has its own replay;
this file verifies the new consequences of those three retained profiles.
"""
from pathlib import Path
import contextlib,hashlib,io,json,runpy,shutil,sys,tempfile,time
P=Path(__file__).resolve().parents[3];here=Path(__file__).parent
sys.path.insert(0,str(P/'software'))
import scipy.optimize
def forbidden(*args,**kwargs):raise RuntimeError('Numerical optimization is disabled during exact replay')
scipy.optimize.linprog=forbidden;scipy.optimize.milp=forbidden
from round5_629 import require,verify_rank30,verify_fixed_profile

def load(path):return json.loads(path.read_text())
def strip_seconds(value):
 if isinstance(value,dict):return {k:strip_seconds(v) for k,v in value.items() if k!='seconds'}
 if isinstance(value,list):return list(map(strip_seconds,value))
 return value
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

started=time.monotonic();checks=[]
for name,verify in [('rank30_certificate.json',verify_rank30),('exact_rank35_h10.json',verify_fixed_profile),('exact_rank38_h10.json',verify_fixed_profile)]:
 result=verify(load(here/name));checks.append({'input':name,'result':result});print('Verified',name,flush=True)

chain=[
 ('decode_twists.py','decoded_twists.json'),
 ('modular_closure.py','modular_closure.json'),
 ('known_verlinde.py','known_verlinde.json'),
 ('independent_fraction.py','independent_fraction.json'),
 ('finite_modular_reps.py','finite_modular_reps.json'),
 ('complete_rank35.py','rank35_modular_completions.json'),
 ('fusion_completion_analysis.py','rank35_fusion_data.json'),
 ('equivalences.py','equivalences.json'),
 ('full_restriction_check.py','full_restriction_check.json'),
]
with tempfile.TemporaryDirectory(dir=here.parent,prefix='m4_629_replay_') as tmp:
 work=Path(tmp)
 for name in ('exact_rank35_h10.json','exact_rank38_h10.json'):shutil.copyfile(here/name,work/name)
 for script,output in chain:
  shutil.copyfile(here/script,work/script)
  with contextlib.redirect_stdout(io.StringIO()):runpy.run_path(str(work/script),run_name='__main__')
  require(strip_seconds(load(work/output))==strip_seconds(load(here/output)),'Rebuilt artifact differs: '+output)
  checks.append({'script':script,'output':output,'passed':True});print('Rebuilt',output,flush=True)
 for branch in load(work/'modular_closure.json'):
  require(branch['linear_failure'] is None and all(branch['checks'].values()),'inconsistent modular closure')
  require(branch['known_span_rank']==30,'unexpected modular span dimension')
 require(load(work/'independent_fraction.json')['coefficient_ascending']==['1/3']+['0']*7,'missing independent rank38 obstruction')
 require(load(work/'equivalences.json')['one_class_under_twins'],'rank35 equivalence coverage missing')
 record={'id':'R6_4_629','kind':'exact_modular_frontier_reduction','version':1,'scope':'all three inherited retained induction profiles','excluded_profile_ranks':[30,38],'remaining_profile_ranks':[35],'twist_exponent':15,'twist_branches':'one complex-conjugate pair','modular_completions_up_to_conjugation_and_twin_relabelling':1,'remaining_central_fusion_rank':35,'ring_status':'unresolved','category_constructed':False,'optimizer_used':False,'checks':checks}
 certificate=here/'modular_reduction_certificate.json'
 if certificate.exists():require(load(certificate)==record,'reduction certificate changed')
 else:certificate.write_text(json.dumps(record,indent=2))
 sources=[P/'software'/name for name in ('round5_629.py','round4_629_orbits.py','round4_quartic_profiles.py','round3_m4.py','spectral_induction.py','exact.py')]+[here/script for script,_ in chain]+[Path(__file__)]
 inputs=[P/'data/unresolved_tensors.json',P/'research/round4/m4_629/filtered_profiles.json',P/'research/round4/m4_629/fixed_twist_h6.json']+[here/name for name in ('rank30_certificate.json','exact_rank35_h10.json','exact_rank38_h10.json')]
 receipt={'passed':True,'python_optimization_level':sys.flags.optimize,'optimizer_disabled':True,'elapsed_seconds':round(time.monotonic()-started,3),'certificate':certificate.name,'certificate_sha256':sha(certificate),'sources_sha256':{str(path.relative_to(P)):sha(path) for path in sources},'inputs_sha256':{str(path.relative_to(P)):sha(path) for path in inputs},'output_sha256':{name:sha(here/name) for _,name in chain}}
 (here/'modular_chain_replay_O.json').write_text(json.dumps(receipt,indent=2));print(json.dumps({'passed':True,'elapsed_seconds':receipt['elapsed_seconds'],'remaining_profile_ranks':[35],'ring_status':'unresolved'}),flush=True)
