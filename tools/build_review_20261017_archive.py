#!/usr/bin/env python3
"""Package the corrected record, dated errata, audit receipts and frozen parent.

The standalone extraction test checks correction metadata only. Full historical
replay is a separate command requiring the complete repository. Repository
archives above 12 MiB are stored as raw 6 MiB parts for tools/restore_data.py;
the generated ZIP remains available locally for the site but is ignored by Git.
An --output outside the repository creates a draft without registering parts.
"""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PREFIX = 'review-update-2026-10-17'
PART_THRESHOLD = 12 * 1024 * 1024
PART_BYTES = 6 * 1024 * 1024


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def package_publication_archive(root, output):
    """Register only this generated ZIP; preserve every other restoration entry."""
    try:
        relative = output.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return {'storage': 'external draft', 'parts': 0}
    manifest_path = root / 'data/large_files_manifest.json'
    manifest = json.loads(manifest_path.read_text())
    matches = [item for item in manifest['files'] if item['path'] == relative]
    if len(matches) > 1:
        raise ValueError('Duplicate archive restoration entries: ' + relative)
    raw = output.read_bytes()
    previous = matches[0] if matches else None
    if len(raw) <= PART_THRESHOLD and previous is None:
        return {'storage': 'direct file', 'parts': 0}
    part_dir = root / 'data/payloads' / relative.replace('/', '__').replace('.', '_')
    part_dir.mkdir(parents=True, exist_ok=True)
    parts = []
    for index, start in enumerate(range(0, len(raw), PART_BYTES), 1):
        chunk = raw[start:start + PART_BYTES]
        path = part_dir / f'part-{index:03}.bin'
        temporary = path.with_suffix('.writing')
        temporary.write_bytes(chunk)
        temporary.replace(path)
        parts.append({'path': path.relative_to(root).as_posix(),
                      'bytes': len(chunk), 'sha256': digest(chunk)})
    current_sha = digest(raw)
    item = {'path': relative, 'bytes': len(raw), 'sha256': current_sha,
            'encoding': 'raw', 'parts': parts}
    if previous:
        historical = list(previous.get('previous_sha256', []))
        if previous['sha256'] != current_sha and previous['sha256'] not in historical:
            historical.append(previous['sha256'])
        if historical:
            item['previous_sha256'] = historical
        manifest['files'][manifest['files'].index(previous)] = item
    else:
        manifest['files'].append(item)
    # Match restore_data's public format, including per-part and final identities.
    packed = b''.join((root / part['path']).read_bytes() for part in parts)
    if packed != raw:
        raise ValueError('Raw archive parts do not reconstruct the ZIP')
    temporary = manifest_path.with_suffix('.writing')
    temporary.write_text(json.dumps(manifest, indent=2) + '\n')
    temporary.replace(manifest_path)
    retained = {Path(part['path']).name for part in parts}
    for stale in part_dir.glob('part-*.bin'):
        if stale.name not in retained:
            stale.unlink()
    ignore = root / '.gitignore'
    text = ignore.read_text() if ignore.exists() else ''
    rule = '/' + relative
    if rule not in text.splitlines():
        text = text.rstrip() + ('\n\n' if text.strip() else '')
        text += '# Restored from checksummed repository parts; generated for GitHub Pages.\n' + rule + '\n'
        ignore.write_text(text)
    return {'storage': 'raw repository parts', 'parts': len(parts),
            'part_bytes': PART_BYTES, 'manifest': 'data/large_files_manifest.json',
            'omit_from_git': relative}


def collect(root):
    spec = importlib.util.spec_from_file_location('frozen_bundle', root / 'tools/build_unified_20261016_archive.py')
    old = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(old)
    payload = old.collect(root)
    # Include the public audit record, receipts and reproduction instructions.
    # Full historical replay still requires a complete repository checkout.
    for folder in ('evidence/review_20261017', 'evidence/prepublication_20261017'):
        for path in (root / folder).rglob('*'):
            if (path.is_file() and not {'__pycache__', '.pytest_cache'}.intersection(path.parts)
                    and path.suffix not in ('.pyc', '.pyo', '.tmp', '.writing', '.swp')
                    and path.name != '.DS_Store'):
                payload[path.relative_to(root).as_posix()] = path.read_bytes()
    for relative in ('tools/verify_review_20261017.py', 'tools/build_review_20261017_archive.py',
                     'tools/build_prepublication_review.py', 'docs/prepublication_review_content.json',
                     'docs/PREPUBLICATION_REVIEW.md', 'docs/RESEARCH_STATUS.md', 'docs/VERIFY.md',
                     'manuscripts/prepublication-review-2026-10-17.pdf',
                     'manuscripts/rank8/paper/rank8-reviewed.pdf'):
        payload[relative] = (root / relative).read_bytes()
    for relative in ('manuscripts/prepublication-review-2026-10-17.pdf',
                     'manuscripts/rank8/paper/rank8-reviewed.pdf'):
        if not payload[relative].startswith(b'%PDF-'):
            raise ValueError('Required review document is not a PDF: ' + relative)
    # Both review PDFs are mandatory; the frozen source-file manifest and the
    # original rank-eight PDF identity remain unchanged.
    return payload


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=ROOT)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    root = args.repo.resolve()
    payload = collect(root)
    inputs = {name: digest(raw) for name, raw in payload.items()}
    payload['README.md'] = ('''# Corrected research record · 17 October 2026

R8_2_24 is reopened: its proposed categorical-to-linear exclusion bridge is unproved.
The current continuation retains 35 accepted decisions (28 exclusions and 7 models),
with R6_4_155, R6_8_1660 and R8_2_24 unresolved. All claims remain AI-generated,
not independently human-verified and not Lean-formalized.

Start with manuscripts/prepublication-review-2026-10-17.pdf and
docs/PREPUBLICATION_REVIEW.md, then evidence/review_20261017/README.md.
The included manuscripts/rank8/paper/rank8-reviewed.pdf places the dated
errata before the unchanged historical paper. The inherited manuscripts and
original 36-decision records are superseded historical snapshots for R8_2_24.
The public audit reports, replay receipts and reconstruction instructions
are included under evidence/prepublication_20261017/.

Standalone correction and source-identity check:
    python3 tools/verify_review_20261017.py --metadata-only

The full historical replay requires a complete repository checkout:
    python3 tools/verify_review_20261017.py --historical

A historical calculation PASS does not reinstate the withdrawn proof. Full base
checks are separately documented in evidence/prepublication_20261017/FULL_REPLAY.md.

ARCHIVE_MANIFEST.json records each included source's SHA-256 and byte size.
Fixed timestamps and sorted paths make identical inputs produce identical ZIP bytes.
''').encode()
    payload['ARCHIVE_MANIFEST.json'] = (json.dumps({name: {'bytes': len(raw), 'sha256': digest(raw)}
                                                   for name, raw in sorted(payload.items())}, indent=2) + '\n').encode()
    output = (args.output or root / 'site/dist/downloads' / f'{PREFIX}.zip').resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='review-bundle-') as directory:
        temp = Path(directory)
        archive = temp / output.name
        with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as bundle:
            for name, raw in sorted(payload.items()):
                info = zipfile.ZipInfo(PREFIX + '/' + name, date_time=(2026, 10, 17, 0, 0, 0))
                info.external_attr = 0o100644 << 16
                info.create_system = 3
                bundle.writestr(info, raw, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
        extracted = temp / 'extracted'
        with zipfile.ZipFile(archive) as bundle:
            if bundle.testzip() is not None:
                raise ValueError('ZIP integrity')
            bundle.extractall(extracted)
        isolated = extracted / PREFIX
        inventory = json.loads((isolated / 'ARCHIVE_MANIFEST.json').read_text())
        actual = {path.relative_to(isolated).as_posix() for path in isolated.rglob('*') if path.is_file()}
        if actual != set(inventory) | {'ARCHIVE_MANIFEST.json'}:
            raise ValueError('Extracted archive inventory differs from its manifest')
        for name, expected in inventory.items():
            raw = (isolated / name).read_bytes()
            if len(raw) != expected['bytes'] or digest(raw) != expected['sha256']:
                raise ValueError('Extracted archive source identity: ' + name)
        run = subprocess.run([sys.executable, str(isolated / 'tools/verify_review_20261017.py'), '--metadata-only'],
                             cwd=isolated, text=True, capture_output=True)
        if run.returncode:
            raise ValueError('Standalone correction check failed:\n' + run.stdout + run.stderr)
        receipt = json.loads(run.stdout)
        if receipt['status'] != 'PASS' or receipt['accepted_decisions'] != 35:
            raise ValueError('Inconsistent receipt')
        for name, expected in inputs.items():
            if digest((root / name).read_bytes()) != expected:
                raise ValueError('Input changed during packaging: ' + name)
        temporary = output.with_suffix('.writing')
        temporary.write_bytes(archive.read_bytes())
        temporary.replace(output)
    storage = package_publication_archive(root, output)
    print(json.dumps({'status': 'PASS', 'files': len(payload), 'archive': str(output),
                      'sha256': digest(output.read_bytes()), 'bytes': output.stat().st_size,
                      'publication_storage': storage, 'standalone_metadata_check': receipt}, indent=2))


if __name__ == '__main__':
    main()
