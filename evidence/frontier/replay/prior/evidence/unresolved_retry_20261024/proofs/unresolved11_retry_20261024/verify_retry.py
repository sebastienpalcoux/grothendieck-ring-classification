#!/usr/bin/env python3
"""Run portable exact checks; these supplement the categorical proofs."""
from pathlib import Path
import gzip
import hashlib
import json
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
CHECKS = [
    'rank10/verify_conformal_model.py',
    'rank10/verify_minimal_branching.py',
    'global/verify_r189_pieri_branching.py',
    'global/verify_r189_rank14_wzw.py',
    'quadratic8/verify_twisted_gh6.py',
    'quadratic8/verify_r1154_quantum_extensions.py',
    'global/verify_r1768_cubic_rotation.py',
    'rank9/verify_pointed_bimodule.py',
    'rank9/verify_source_local.py',
    'rank9/verify_discrete_witnesses.py',
    'rank9/verify_discrete_branch_restrictions.py',
    'quartic/verify_model_screen.py',
]

def run(script, args=()):
    p = HERE / script
    if not p.is_file():
        raise FileNotFoundError(p)
    r = subprocess.run([sys.executable, '-O', str(p), *map(str, args)],
                       cwd=HERE.parent, text=True, capture_output=True)
    if r.returncode:
        raise RuntimeError(f'{script}:\n{r.stdout}\n{r.stderr}')
    print('PASS', script, flush=True)
    return {'script': script, 'returncode': r.returncode,
            'stdout_sha256': hashlib.sha256(r.stdout.encode()).hexdigest()}

def main():
    receipts = [run(p) for p in CHECKS]
    raw = gzip.decompress((HERE/'reference/r155_generalized.gz').read_bytes())
    wanted = 'b76cdb3fbc8c4cc6c23d3e177be26d0a74d1adab114069b9e40b04b62678fca7'
    if hashlib.sha256(raw).hexdigest() != wanted:
        raise ValueError('R155 source certificate hash mismatch')
    with tempfile.TemporaryDirectory(prefix='fusion-retry-') as td:
        source = Path(td)/'r155_generalized.json'
        source.write_bytes(raw)
        receipts.append(run('rank6/verify_even_clifford.py',
                            [source, HERE/'rank6/even_clifford_receipt.json']))
    out = {'status': 'PASS', 'optimized_python': True, 'checks': receipts,
           'scope': 'Exact finite checks only; categorical proofs are in the accompanying notes.'}
    (HERE/'verification_receipt.json').write_text(json.dumps(out, indent=2)+'\n')
    print(f'PASS: {len(receipts)} portable exact verifiers.')

if __name__ == '__main__':
    main()
