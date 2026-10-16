#!/usr/bin/env python3
"""Replay the complete unchanged R446 certificate with its historical row order.

This opt-in command repeats the 97-second original check; the append-only
receipt already records that completed run. It does not change any ledger.
"""
import os
os.environ['SYMPY_GROUND_TYPES']='python'
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[key]='1'
import sys,json,time,argparse
from pathlib import Path
from common import PACKET,DEFAULT_REPO,bound_inputs,require,digest
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--repo',type=Path,default=DEFAULT_REPO)
p.add_argument('--output',type=Path)
a=p.parse_args()
base,row,entry,commitments=bound_inputs(a.repo)
sys.path.insert(0,str(base/'software'))
import sympy
import signed_spherical_traces as signed
from check import verify
require(sympy.__version__=='1.14.0','unexpected SymPy version')
require(sympy.external.gmpy.GROUND_TYPES=='python','backend pin did not take effect')
original=signed.check_farkas_sparse
count=0
def counted(A,b,y):
 global count
 original(A,b,y)
 count+=1
signed.check_farkas_sparse=counted
start=time.monotonic()
verify(row['N'],entry['certificate'])
require(count==128,'unexpected signed-spherical case count')
receipt={'status':'PASS','id':'R6_4_446','scope':'complete original general certificate',
         'entrypoint':'supplements/rank6/software/check.py:verify',
         'backend':'python','sympy':sympy.__version__,'python':sys.version,
         'tensor_sha256':commitments['tensor_sha256'],
         'certificate_sha256':commitments['certificate_sha256'],
         'commitments_sha256':digest(PACKET/'commitments.json'),
         'signed_spherical_cases':count,'seconds':time.monotonic()-start}
if a.output:
 a.output.parent.mkdir(parents=True,exist_ok=True)
 a.output.write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
