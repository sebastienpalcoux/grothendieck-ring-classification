"""Replay the new continuation's exact checks, without optimization."""
from pathlib import Path
import sys, subprocess, json, time, tempfile, shutil, argparse
ROOT=Path(__file__).resolve().parent
checks=[
 "new/root/pivotal_conjugation_parity.py",
 "new/r155/verify_morita_ring_rigidity.py",
 "new/r1660_941/verify.py",
 "new/r1660_941/quantum_routes.py",
 "new/r1660_941/r941_galois_followup.py",
 "new/r928/verify_spectral_reduction.py",
 "new/r1154/verify_simple_center_inputs.py",
 "new/r1154/verify_conjugation_audit.py",
 "new/r137/verify_structural.py",
 "new/r155/verify_r137_forced_galois_audit.py",
 "new/r1768/verify_palindromic_exclusion.py",
 "new/r1768/replay_palindromic_center.py",
]
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output',type=Path,help='Write a fresh replay log outside the frozen proof inputs.')
args=parser.parse_args()
if args.output and args.output.resolve().is_relative_to(ROOT.resolve()):
 raise ValueError('Fresh output must be outside the frozen proof-input directory')
results=[]
with tempfile.TemporaryDirectory(prefix='fusion-frontier-replay-')as folder:
 target=Path(folder)/'replay'
 shutil.copytree(ROOT,target,ignore=shutil.ignore_patterns('__pycache__','*.pyc','gram_vectors_rank8'))
 for name in checks:
  start=time.monotonic()
  p=subprocess.run([sys.executable,str(target/name)],cwd=target,capture_output=True,text=True)
  results.append({'script':name,'exit_code':p.returncode,'seconds':round(time.monotonic()-start,3),'stdout':p.stdout,'stderr':p.stderr})
  print(('PASS'if p.returncode==0 else'FAIL')+' '+name,flush=True)
  if p.returncode:
   print(p.stdout);print(p.stderr);raise SystemExit(p.returncode)
receipt={'all_pass':all(r['exit_code']==0 for r in results),'checks':results,'frozen_inputs_modified':False}
if args.output:args.output.write_text(json.dumps(receipt,indent=2)+'\n')
print('All '+str(len(checks))+' replay checks passed; frozen input receipts preserved.')
