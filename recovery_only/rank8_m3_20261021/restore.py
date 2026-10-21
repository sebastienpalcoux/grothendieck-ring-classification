#!/usr/bin/env python3
"""Restore exact oversized current-checkpoint snapshots in a fresh checkout."""
from pathlib import Path
import gzip,hashlib,json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
for item in json.loads((HERE/'manifest.json').read_text()):
    compressed=(HERE/item['archive']).read_bytes()
    if hashlib.sha256(compressed).hexdigest()!=item['archive_sha256']:raise ValueError('archive hash')
    raw=gzip.decompress(compressed)
    if hashlib.sha256(raw).hexdigest()!=item['raw_sha256']:raise ValueError('raw hash')
    target=ROOT/item['target'];target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw)
    print('Restored',item['target'])
