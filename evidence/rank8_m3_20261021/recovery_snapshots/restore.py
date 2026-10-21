#!/usr/bin/env python3
"""Restore exact oversized JSON snapshots from this recovery checkpoint."""
from pathlib import Path
import gzip,hashlib,json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
for item in json.loads((HERE/'manifest.json').read_text()):
    blob=(HERE/item['archive']).read_bytes()
    if hashlib.sha256(blob).hexdigest()!=item['archive_sha256']:raise ValueError('archive hash')
    raw=gzip.decompress(blob)
    if hashlib.sha256(raw).hexdigest()!=item['raw_sha256']:raise ValueError('raw hash')
    target=ROOT/item['target'];target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw)
    print('Restored',item['target'])
