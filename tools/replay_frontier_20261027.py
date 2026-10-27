#!/usr/bin/env python3
"""Replay the new proofs in their frozen ten-tensor source context."""
from pathlib import Path
import argparse, hashlib, json, os, subprocess, sys, tempfile, zipfile
from frontier_20261027 import ROOT, EVIDENCE, read, sha

CHECKS = [
 'evidence/unresolved10_20261027/r9_noncommutative/verify_duality_obstruction.py',
 'evidence/unresolved10_20261027/r9_noncommutative/verify_galois_parity.py',
 'evidence/unresolved10_20261027/r9_commutative/verify_galois_fs2.py',
 'evidence/unresolved10_20261027/r6_1660/replay_r1975_gate.py',
 'evidence/unresolved10_20261027/r6_1660/replay_rank9_signed_gates.py',
 'evidence/unresolved7_20261027/audit_fs2/verify_r155_algebra_reduction.py',
 'evidence/unresolved7_20261027/audit_fs2/verify_r1660_bimodule_parity.py',
 'evidence/unresolved7_20261027/r6_1660/verify_spin_constraints.py',
 'evidence/unresolved7_20261027/r8_928_941/verify.py',
 'evidence/unresolved7_20261027/r8_1154/verify_odd_rotation.py',
 'evidence/unresolved7_20261027/r8_1154/verify_integral_center.py',
 'evidence/unresolved7_20261027/r8_1768/verify_morita_parity.py',
 'evidence/unresolved7_20261027/r8_928_941/audit_r1768_profiles.py',
 'evidence/unresolved7_20261027/audit_parity/verify_r137_positive_fs2.py',
]

def need(ok,message):
 if not ok:raise ValueError(message)

def main(output=None):
 a=read(ROOT/EVIDENCE/'accepted.json');entry=a['replay_archive'];archive=ROOT/entry['path']
 need(sha(archive)==entry['sha256'],'Frozen proof archive identity')
 records={}
 for name in ('unresolved_cases.json','rank9_m2.json'):
  for r in read(ROOT/'site/dist/data'/name)['cases']:records[r['id']]=r
 with tempfile.TemporaryDirectory(prefix='fusion-frontier-exact-')as tmp:
  folder=Path(tmp)
  with zipfile.ZipFile(archive)as z:
   need(z.testzip()is None,'Archive CRC')
   m=json.loads(z.read('CONTINUATION_MANIFEST.json'))
   for name,item in m['files'].items():
    p=Path(name);need(not p.is_absolute()and'..'not in p.parts,'Unsafe archive path')
    raw=z.read(name);need(len(raw)==item['size']and hashlib.sha256(raw).hexdigest()==item['sha256'],'Archived source identity: '+name)
   z.extractall(folder)
  import ast
  tree=ast.parse((folder/'data/current_remaining_cases.py').read_text())
  values={n.targets[0].id:ast.literal_eval(n.value)for n in tree.body if isinstance(n,ast.Assign)}
  need(len(values['TENSORS'])==10,'Frozen ten-case context')
  for rid,tensor in values['TENSORS'].items():
   need(rid in records and records[rid]['fusion_tensor']==tensor,'Current/archive tensor mismatch: '+rid)
  env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1'}
  env.pop('PYTHONOPTIMIZE',None);runs=[]
  for script in CHECKS:
   p=subprocess.run([sys.executable,script],cwd=folder,env=env,capture_output=True,text=True)
   need(p.returncode==0,script+'\n'+p.stdout+p.stderr)
   runs.append({'script':script,'status':'PASS','assertions_enabled':True,
                'source_sha256':sha(folder/script),'output_sha256':hashlib.sha256((p.stdout+p.stderr).encode()).hexdigest()})
   print('PASS',script,flush=True)
 receipt={'status':'PASS','schema':'frontier-exact-replay/v1','archive_sha256':sha(archive),
          'current_and_frozen_tensors_agree':10,'checks':runs,
          'scope':'Exact finite proof checks in their immutable source context; categorical premises are in the proofs, not inferred from these computations.'}
 if output:
  Path(output).parent.mkdir(parents=True,exist_ok=True);Path(output).write_text(json.dumps(receipt,indent=2)+'\n')
 return receipt

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path)
 args=p.parse_args();main(args.output)
