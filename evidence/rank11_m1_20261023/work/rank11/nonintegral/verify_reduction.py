"""Independent exact replay of every accepted sign and scalar-character receipt.

Reuses the project's independently written verifiers, never their discovery
or scalar-restriction solvers. Checks all 182 source input identities elsewhere;
this replay binds each of its 59 records to the full original rank11 tensor.
"""
from pathlib import Path
import sys,json,time,importlib.util
P=Path(__file__).resolve().parent;ROOT=P.parents[2]
sys.path[:0]=[str(ROOT/'work/general_signed'),str(ROOT/'work/obstructions'),str(ROOT/'work/rank11')]
from common import read,sha,require
from verify import verify_record
from verify_characters import verify_original,verify_signed
from branches import signed_tensor
rows=read();signs=json.load(open(P/'signed.json'));original=json.load(open(P/'original.json'));start=time.monotonic();ss=0
require({r['id'] for r in signs}=={r['id'] for r in original},'matching receipt domains')
for r in signs:
 R=rows[r['id']];require(r['tensor_sha256']==sha(R),'original tensor identity');verify_record(R,r)
 for b in r['branches']:
  if b['outcome']=='excluded_dimension_characters':
   du=r['gauge_dual_orbits'];n=len(R);dual=[next(j for j in range(n) if R[i][j][0]) for i in range(n)];mapping={}
   for j,orb in enumerate(r['oriented_orbits']):
    for i,k,l in orb:mapping[i,k,dual[l]]=j
   T=signed_tensor(R,{'mapping':mapping},b['sign_assignment']);verify_signed(R,T,b['dimension_test']);ss+=1
for r in original:
 R=rows[r['id']];require(r['tensor_sha256']==sha(R),'original tensor identity');verify_original(R,r)
result=dict(status='PASS',sign_records=len(signs),alternate_signed_character_records=ss,original_character_records=len(original),seconds=time.monotonic()-start,all_signed_categorical_original=all(r['all_categorical_signed_tables_are_gauge_original'] for r in signs),non_FP_spherical_branch_ids=[r['id'] for r in original if not r['all_spherical_characters_reduce_to_pseudo_unitary']],no_spherical_character_ids=[r['id'] for r in original if all(b['obstruction'] for b in r['branches'])])
(P/'reduction_replay.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2),flush=True)
