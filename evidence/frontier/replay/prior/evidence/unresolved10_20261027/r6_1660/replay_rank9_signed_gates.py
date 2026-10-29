"""Source-bound fresh replay of the R137, R1607, R1976 signed gates.

Requires numpy, sympy, z3-solver. Hard limit: 20 seconds for all three
certificate checks. The archived verifier uses assertions; -O is refused.
"""
from pathlib import Path
import hashlib, json, runpy, signal, sys, time

if not __debug__:
    raise RuntimeError('Archived checks require assertions enabled')
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
BASE = HERE / 'r1975_gate_replay'
manifest = json.loads((HERE/'rank9_signed_gate_provenance.json').read_text())
for path, expected in manifest['extracted_files_sha256'].items():
    if hashlib.sha256((BASE/path).read_bytes()).hexdigest() != expected:
        raise ValueError('Archived input hash mismatch: '+path)
audit_dependencies = ROOT.parent / 'r1975-audit-deps'
if audit_dependencies.exists():
    sys.path.insert(0, str(audit_dependencies))
sys.path.insert(0, str(BASE/'phase2/signed'))
import verify_nonzero_products as verifier

inputs = runpy.run_path(str(ROOT/'data/current_remaining_cases.py'))['TENSORS']
def timeout(*args):
    raise TimeoutError('20-second certificate-check budget exceeded')
signal.signal(signal.SIGALRM, timeout)
signal.alarm(20)
rows = []
started = time.monotonic()
try:
    for number in (137, 1607, 1976):
        rid = f'R9_2_{number}'
        certificate = json.loads((BASE/f'phase2/signed/gate_{rid}.json').read_text())
        start = time.monotonic()
        row = verifier.check(inputs[rid], certificate, timeout=15000)
        row.update(seconds=time.monotonic()-start,
                   tensor_sha256=verifier.digest(inputs[rid]), assertions_enabled=True)
        rows.append(row)
        receipt = {'archive_sha256': manifest['archive_sha256'], 'rows': rows,
                   'seconds': time.monotonic()-started}
        (HERE/'rank9_signed_gates_replay_receipt.json').write_text(json.dumps(receipt, indent=2)+'\n')
        print(json.dumps(row), flush=True)
finally:
    signal.alarm(0)
