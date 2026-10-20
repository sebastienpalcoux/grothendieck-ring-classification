#!/usr/bin/env python3
"""Package current manuscripts, proof sources and exact verification evidence.

The standalone extraction test checks current documents and decision metadata. Full historical
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
    from current_publication import DOCUMENT_REVISION, validate_documents, replay_sources
    from reader_resources import validate_reader_resources
    revision = validate_documents(root)
    validate_reader_resources(root)
    preserved = replay_sources(root)
    spec = importlib.util.spec_from_file_location('frozen_bundle', root / 'tools/build_unified_20261016_archive.py')
    old = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(old)
    paths = set(old.REQUIRED)
    for folder in ('evidence/unified_20261016', 'evidence/theoretical_20261016',
                   'evidence/review_20261017', 'evidence/prepublication_20261017',
                   'evidence/publication_20261017', 'evidence/rank4_unrestricted_20261017',
                   'evidence/rigidity_20261017', 'evidence/citation_20261019',
                   'evidence/rank7_m5_20261019', 'evidence/rank7_m5_20261020', 'supplements/rank7/output/m5',
                   'supplements/rank7/provenance', 'supplements/rank7/output'):
        paths.update(path.relative_to(root).as_posix() for path in (root / folder).rglob('*')
                     if path.is_file() and not {'__pycache__', '.pytest_cache'}.intersection(path.parts)
                     and not any(part.startswith('.') for part in path.relative_to(root).parts)
                     and path.suffix not in ('.pyc', '.pyo', '.tmp', '.writing', '.swp', '.log')
                     and not (folder == 'evidence/rank7_m5_20261020' and not path.suffix)
                     and path.name != '.DS_Store')
    paths.update(revision['documents'])
    for folder in ('supplements/rank6/software','supplements/rank7/software','supplements/rank7/data'):
        paths.update(path.relative_to(root).as_posix() for path in (root/folder).rglob('*')
                     if path.is_file() and path.suffix in ('.py','.cpp','.h','.hpp','.json','.gz','.txt','.csv','.md'))
    paths.update(path.relative_to(root).as_posix() for path in (root/'supplements/rank7').glob('*')
                 if path.is_file() and path.suffix in ('.py','.cpp','.md','.txt'))
    paths.update(('tools/sync_rank7_m5_publication.py', 'tools/import_rank7_m5_counts.py',
                  'tools/build_novelty_frontier_brief.py', 'tools/build_rank7_m5_continuation_overview.py',
                  'tools/audit_rank7_manuscript.py',
                  'data/counts.json', 'data/classification_status.json'))
    paths.update(json.loads((root / 'evidence/rigidity_20261017/source_files.json').read_text()))
    necessary = json.loads((root / 'evidence/rigidity_20261017/rank6/MANIFEST.json').read_text())
    paths.update(item['path'] for item in necessary['external_inputs'])
    paths.update(path.relative_to(root).as_posix()
                 for path in (root / 'supplements/rank4/unrestricted').rglob('*')
                 if path.is_file() and not {'__pycache__', '.pytest_cache'}.intersection(path.parts)
                 and path.suffix not in ('.pyc', '.pyo', '.o', '.aux', '.log', '.out', '.toc')
                 and path.name not in ('enumerate', 'enumerate_signed'))
    paths.update(path.relative_to(root).as_posix() for path in (root / 'docs').glob('*.md'))
    paths.update(path.relative_to(root).as_posix() for path in (root / 'supplements').glob('rank*/README.md'))
    # Include the current reader indexes and the clean status-PDF source, so the
    # downloaded edition has the same navigation and rebuild inputs as GitHub.
    paths.update(('manuscripts/README.md', 'manuscripts/prepublication-review-2026-10-17.pdf', 'supplements/README.md',
                  'tools/build_prepublication_review.py', 'docs/prepublication_review_content.json'))
    paths.update(path.relative_to(root).as_posix() for path in (root / 'supplements/rank6').rglob('*.md')
                 if path.name in ('README.md', 'CURRENT_STATUS.md'))
    paths.update((DOCUMENT_REVISION, 'tools/verify_current_publication.py',
                  'tools/current_publication.py', 'tools/verify_review_20261017.py',
                  'tools/verify_rigidity_20261017.py',
                  'tools/build_review_20261017_archive.py', 'tools/build_current_document_revision.py',
                  'tools/reader_resources.py', 'data/remaining_cases.py', 'data/manuscript_page_counts.json',
                  'docs/PREPUBLICATION_REVIEW.md', 'docs/RESEARCH_STATUS.md', 'docs/VERIFY.md'))
    paths.update(('tools/rank7_publication.py',
                  'supplements/rank7/output/rank7_ledger.json',
                  'supplements/rank7/output/rank7_ledger_through_m4.json',
                  'supplements/rank7/data/rank7_tables_through_m4.txt.gz'))
    payload = {name: (root / name).read_bytes() for name in sorted(paths)}
    # The immutable proof manifest keeps its exact original hashes. Revised
    # documents are verified separately; their original replay bytes are in the
    # independently pinned archive and are restored only by the dispatcher.
    frozen = json.loads(payload['evidence/unified_20261016/source_files.json'])
    for name, expected in frozen.items():
        raw = preserved[name] if name in preserved else payload.get(name)
        if raw is None or digest(raw) != expected:
            raise ValueError('Missing or changed immutable proof source: ' + name)
    for source in revision['web_copies'].values():
        if source not in payload or not payload[source].startswith(b'%PDF-'):
            raise ValueError('Current downloadable manuscript missing: ' + source)
    return payload


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=ROOT)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    root = args.repo.resolve()
    payload = collect(root)
    inputs = {name: digest(raw) for name, raw in payload.items()}
    payload['README.md'] = ("""# Grothendieck-ring classification · manuscripts and verification

This package contains the current manuscript sources and PDFs for ranks two
through eight, verification guides, proof sources, exact computational evidence,
and the publication identity manifest data/current_document_revision.json.

Ranks two, three and four have unrestricted complex classifications. The
rank-four article proves a theoretical dimension bound without pivotality
or a multiplicity restriction, then classifies its complete 1,692-ring
finite census into 1,677 exclusions and 15 models. Its replay package is
supplements/rank4/unrestricted; the sharp multiplicity bound is six.

The 38-case continuation has 36 accepted decisions (29 proposed exclusions and
7 constructions). R6_4_155 and R6_8_1660 remain unresolved. Rank eight is complete
through multiplicity two: 896 exclusions and 77 unitary models. The inner-square
obstruction for R8_2_24 uses pivotal duality, short gauge weights and tensor-functor rigidity.
Treat these AI-generated results and data with caution: independent human
verification and Lean formalization have not been completed.

Start with docs/RESEARCH_STATUS.md and the manuscripts directory.
The verification procedures and their precise limits are in docs/VERIFY.md.
The exact tensors of the current open cases are plain Python nested lists in
data/remaining_cases.py, with unit, duality, convention and source hashes.
data/manuscript_page_counts.json counts each distinct current PDF once.

Standalone publication, source-identity and decision check:
    python3 tools/verify_current_publication.py --metadata-only

Full proof-history replay, from a complete repository checkout:
    python3 tools/verify_current_publication.py --historical

The dispatcher reconstructs each immutable proof stage in an isolated temporary
workspace. It never replaces the current manuscripts. A computational PASS
certifies the stated checks, not the mathematical correctness of every argument.

ARCHIVE_MANIFEST.json records each included source's SHA-256 and byte size.
Fixed timestamps and sorted paths make identical inputs produce identical ZIP bytes.
""").encode()
    from rank7_publication import summary
    payload['README.md'] += ('\n' + summary(root) + '\n').encode()
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
        run = subprocess.run([sys.executable, str(isolated / 'tools/verify_current_publication.py'), '--metadata-only'],
                             cwd=isolated, text=True, capture_output=True)
        if run.returncode:
            raise ValueError('Standalone publication check failed:\n' + run.stdout + run.stderr)
        receipt = json.loads(run.stdout)
        if receipt['status'] != 'PASS' or receipt['historical_accepted_decisions'] != 36:
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
