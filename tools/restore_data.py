#!/usr/bin/env python3
"""Restore large source datasets from small, checksummed repository parts."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='verify every part and reconstructed file without writing')
    args = parser.parse_args()
    manifest = json.loads((ROOT / 'data/large_files_manifest.json').read_text())
    for item in manifest['files']:
        chunks = []
        for part in item['parts']:
            raw = (ROOT / part['path']).read_bytes()
            if len(raw) != part['bytes'] or digest(raw) != part['sha256']:
                raise ValueError('Corrupt payload part: ' + part['path'])
            chunks.append(raw)
        packed = b''.join(chunks)
        raw = gzip.decompress(packed) if item['encoding'] == 'gzip' else packed
        if len(raw) != item['bytes'] or digest(raw) != item['sha256']:
            raise ValueError('Reconstructed file checksum mismatch: ' + item['path'])
        target = ROOT / item['path']
        if not args.check:
            if target.exists() and digest(target.read_bytes()) != item['sha256']:
                raise FileExistsError('Refusing to overwrite a modified file: ' + str(target))
            if not target.exists():
                target.parent.mkdir(parents=True, exist_ok=True)
                temp = target.with_name(target.name + '.restoring')
                temp.write_bytes(raw)
                temp.replace(target)
        print(('Verified ' if args.check else 'Ready ') + item['path'])
    print('All ' + str(len(manifest['files'])) + ' large datasets match their released SHA-256 hashes.')


if __name__ == '__main__':
    main()
