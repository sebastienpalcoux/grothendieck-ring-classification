"""Replay the complete exact R4982 certificate from its original fusion tensor.

Requires Python 3 with sympy, numpy, networkx and a C++17 compiler.
No floating-point feasibility or numerical nonexistence inference is used.
Generated JSON and .in/.out certificates are deterministically refreshed here.
"""
if not __debug__:
 raise RuntimeError("This exact certificate requires Python assertions; disable optimization.")
import subprocess,sys,tempfile,time,os
from pathlib import Path
B=Path(__file__).parent;t=time.monotonic();env=dict(os.environ);env.pop("PYTHONOPTIMIZE",None)
def run(script):
 print('VERIFY',script,flush=True)
 subprocess.run([sys.executable,str(B/script)],cwd=B,check=True,env=env)
run('verify_fourier.py')
run('r4982_module.py')
run('prepare_rightactions.py')
with tempfile.TemporaryDirectory(prefix='r4982_exact_') as tmp:
 exe=Path(tmp)/'enumerate_rightactions'
 subprocess.run(['g++','-std=c++17','-O2',str(B/'enumerate_rightactions.cpp'),'-o',str(exe)],check=True)
 for anchor in [4,7,10]:
  with (B/f'rightaction_{anchor}.in').open('r') as inp,(B/f'rightaction_{anchor}.out').open('w') as out:
   subprocess.run([str(exe)],stdin=inp,stdout=out,check=True)
  assert len((B/f'rightaction_{anchor}.out').read_text().splitlines())==1
run('fullgram_completion.py')
run('normalization_check.py')
run('invertible_group_completion.py')
run('dual_fusion_completion.py')
run('certify_rank13.py')
print('R7_5_4982: exact general Morita-descent exclusion verified in %.2f seconds.'%(time.monotonic()-t),flush=True)
