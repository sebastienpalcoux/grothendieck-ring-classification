#!/usr/bin/env python3
"""Verify every archived SHA-256 digest without altering the release."""
from pathlib import Path
import hashlib
import sys
ROOT = Path(__file__).resolve().parent

def main() -> int:
    failures = []
    manifest = ROOT / 'SHA256SUMS'
    if not manifest.is_file():
        print('Missing SHA256SUMS', file=sys.stderr)
        return 2
    rows = manifest.read_text().splitlines()
    for line in rows:
        digest, relative = line.split('  ', 1)
        path = ROOT / relative
        if not path.is_file():
            failures.append(f'MISSING {relative}')
            continue
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != digest:
            failures.append(f'MISMATCH {relative}')
    for message in failures:
        print(message, file=sys.stderr)
    print(f'Checked {len(rows)} files; {len(failures)} failures.')
    return int(bool(failures))

if __name__ == '__main__':
    raise SystemExit(main())
