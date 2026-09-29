"""Budgeted optimizer-free exact replay of completed higher certificates.
Each conditional is an independent exhaustive finite subcertificate.
Checkpoint claims are tied to exact source certificate SHA-256.
"""
import argparse,hashlib,json,signal,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'software'))
import stabilizer_rotation_higher as H
import scipy.optimize as so
p=argparse.ArgumentParser();p.add_argument('id');p.add_argument('--conditional',type=int);p.add_argument('--outer',action='store_true');p.add_argument('--integral',action='store_true');a=p.parse_args()
DIR=Path(__file__).parent;path=DIR/(a.id+('_higher_h6_integral_resumed.json' if a.integral else '_higher_h6_resumed.json'));raw=path.read_bytes();pseudo=json.loads(raw)['certificate'];R=next(r['N']for r in json.load(open(ROOT/'data/census.json'))if r['id']==a.id);digest=hashlib.sha256(raw).hexdigest()
red=json.load(open(DIR/(a.id+'_galois_reduction.json')))['certificate'];c={'kind':('general_integral_morita_rotation' if a.integral else 'general_stabilizer_rotation_higher'),'version':1,'scope':'general','reduction':red,'pseudo':pseudo}
def block(*args,**kwargs):raise RuntimeError('optimizer used during exact replay')
so.linprog=so.milp=so.minimize=block;H.farkas=H.cached_farkas=H.C.farkas=H.I.farkas=block
import higher_traces;higher_traces.farkas=block
def end(*args):raise TimeoutError('890-second replay shard budget')
signal.signal(signal.SIGALRM,end);signal.alarm(890);t=time.monotonic()
if a.outer:
 def checkpoint(R,cc):
  i=pseudo['conditionals'].index(cc);r=json.load(open(DIR/(a.id+'_verify_conditional'+str(i)+'.json')))
  if r['source_sha256']!=digest or r['conditional']!=i or r['passed'] is not True or r['optimizer_disabled'] is not True or r['optimized_python'] is not True:raise ValueError('stale or invalid exact replay checkpoint')
  return True
 H.verify_conditional=checkpoint
 
 if a.integral:
  import round3_integral_morita as IM
  IM.verify_general(R,c)
 else:H.verify_general(R,c)
 out={'id':a.id,'certificate':c,'outcome':'general_excluded','verification':{'kind':'optimizer_free_sharded_replay','source_sha256':digest,'conditional_count':len(pseudo['conditionals']),'optimized_python':not __debug__,'optimizer_disabled':True,'seconds':time.monotonic()-t}}
 target=DIR/(a.id+'_general.json')
else:
 if a.conditional is None:raise ValueError('provide --conditional or --outer')
 H.verify_conditional(R,pseudo['conditionals'][a.conditional]);out={'id':a.id,'source_sha256':digest,'conditional':a.conditional,'passed':True,'optimized_python':not __debug__,'optimizer_disabled':True,'seconds':time.monotonic()-t};target=DIR/(a.id+'_verify_conditional'+str(a.conditional)+'.json')
signal.alarm(0);target.write_text(json.dumps(out,separators=(',',':'))+'\n');print({k:v for k,v in out.items()if k!='certificate'},flush=True)
