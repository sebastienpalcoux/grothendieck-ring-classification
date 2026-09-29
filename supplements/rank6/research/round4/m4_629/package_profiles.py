import sys,json,time,signal
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'))
import scipy.optimize as op
def denied(*a,**k):raise RuntimeError('numeric optimizers disabled')
op.linprog=op.milp=denied
from round4_quartic_profiles import certificate
from exact import require
R=next(x['N'] for x in json.load(open(P/'data/unresolved_tensors.json')) if x['id']=='R6_4_629');st=time.monotonic()
def stop(*a):raise TimeoutError('840 second exact verification budget')
signal.signal(signal.SIGALRM,stop);signal.alarm(840)
try:
 c=certificate(R,6,node_limit=30000000,progress=lambda *v:print(v,flush=True));cpp=sorted(json.loads(l) for l in open(Path(__file__).with_name('profiles_counts.jsonl')));require(c['branches'][3]['gram_galois_profiles']==cpp,'independent C++/Python enumeration mismatch');rec={'id':'R6_4_629','outcome':'exact_necessary_profile_reduction','certificate':c,'optimizer_used':False,'independent_cpp_match':True,'optimized_python':not __debug__}
except Exception as e:rec={'id':'R6_4_629','outcome':'budget_incomplete' if isinstance(e,TimeoutError) else 'error','reason':repr(e)}
finally:signal.alarm(0)
rec['seconds']=time.monotonic()-st;Path(__file__).with_name('R6_4_629_exact_profiles.json').write_text(json.dumps(rec));print({k:v for k,v in rec.items() if k!='certificate'},flush=True)
