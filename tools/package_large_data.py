#!/usr/bin/env python3
"""Repack the repository's declared generated datasets after a verified release."""
import gzip
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'data/large_files_manifest.json'
CHUNK_SIZE = 512 * 1024


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    manifest = json.loads(MANIFEST.read_text())
    for item in manifest['files']:
        raw = (ROOT / item['path']).read_bytes()
        current = digest(raw)
        if current == item.get('sha256') and all((ROOT / part['path']).is_file() for part in item.get('parts', [])):
            continue
        previous = list(item.get('previous_sha256', []))
        if item.get('sha256') and item['sha256'] != current and item['sha256'] not in previous:
            previous.append(item['sha256'])
        if previous:
            item['previous_sha256'] = previous
        packed = gzip.compress(raw, compresslevel=9, mtime=0) if item['encoding'] == 'gzip' else raw
        part_dir = ROOT / 'data/payloads' / item['path'].replace('/', '__').replace('.', '_')
        part_dir.mkdir(parents=True, exist_ok=True)
        for old in part_dir.glob('part-*.bin'):
            old.unlink()
        item.update(bytes=len(raw), sha256=current, parts=[])
        for index, start in enumerate(range(0, len(packed), CHUNK_SIZE), 1):
            part = packed[start:start + CHUNK_SIZE]
            target = part_dir / f'part-{index:03}.bin'
            target.write_bytes(part)
            item['parts'].append(dict(path=target.relative_to(ROOT).as_posix(), bytes=len(part), sha256=digest(part)))
    MANIFEST.write_text(json.dumps(manifest, indent=2) + '\n')
    print(f"Packed {len(manifest['files'])} declared datasets.")


if __name__ == '__main__':
    main()
