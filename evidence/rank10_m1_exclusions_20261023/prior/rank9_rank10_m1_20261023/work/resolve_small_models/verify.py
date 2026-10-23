"""Deterministic replay of all eight categorical realization certificates."""
import subprocess,sys,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
for name in ['work/audit_new_models/verify_c2.py','work/audit_new_models/verify_s3.py','work/audit_new_models/verify_s4.py','work/resolve_small_models/triality_ring.py']:
 subprocess.run([sys.executable,str(ROOT/name)],cwd=ROOT,check=True)
print('PASS: all eight small integral realizations; see THEORY.md for the triality existence theorem.')
