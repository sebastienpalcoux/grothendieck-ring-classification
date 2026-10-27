"""Replay the source-bound archived R1975 signed gate only.

Requires numpy, sympy, z3-solver. Do not run with Python -O: the unchanged
archived verifier uses assertions. The wrapper refuses optimized execution.
"""
from pathlib import Path
import hashlib, json, runpy, sys, time

if not __debug__:
    raise RuntimeError('Archived checks require assertions enabled')
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
BASE = HERE / 'r1975_gate_replay'
manifest = json.loads((HERE/'r1975_gate_provenance.json').read_text())
for path, expected in manifest['extracted_files_sha256'].items():
    actual = hashlib.sha256((BASE/path).read_bytes()).hexdigest()
    if actual != expected:
        raise ValueError('Archived input hash mismatch: '+path)

# Optional local dependency target used during this audit; ordinary installed
# z3-solver works equally well when that transient target does not exist.
audit_dependencies = ROOT.parent / 'r1975-audit-deps'
if audit_dependencies.exists():
    sys.path.insert(0, str(audit_dependencies))
sys.path.insert(0, str(BASE/'phase2/signed'))
import verify_nonzero_products as verifier

tensor = runpy.run_path(str(ROOT/'data/current_remaining_cases.py'))['TENSORS']['R9_2_1975']
certificate = json.loads((BASE/'phase2/signed/gate_R9_2_1975.json').read_text())
started = time.monotonic()
receipt = verifier.check(tensor, certificate, timeout=30000)
receipt.update(seconds=time.monotonic()-started,
               archive_sha256=manifest['archive_sha256'],
               tensor_sha256=verifier.digest(tensor), assertions_enabled=True)
(HERE/'r1975_gate_replay_receipt.json').write_text(json.dumps(receipt, indent=2)+'\n')
print(json.dumps(receipt, indent=2))
