#!/usr/bin/env python3
"""Create an isolated pre-stage-b snapshot for a fresh full base replay.

This reuses each stage's exact prior-record and prior-file manifests. It does
not modify the source repository, infer any new classification, or change
any frozen verifier. The fresh base replay must be followed by the current
unified --historical replay to cover subsequent decisions.
"""
from pathlib import Path
import argparse, collections, copy, hashlib, importlib.util, json, shutil, zipfile

ROOT = Path(__file__).resolve().parents[2]
MANIFESTS = {
    'unified_20261016': 'aea53af376ee1622554e969a3d178b0c42124abd8da3eadc08d62cc5ee5cd851',
    'theoretical_20261016': 'a34df291f7ca848d0f877cd994b923e41ba0d0fc496c79a65612d1542941335b',
    'upper_residual_20261002c': '409c58594d1d004678becac5459df375c5a99c9d4e18c5ba99f0bb7881c7db04',
    'upper_residual_20261002b': 'b595f524ce8f19285e51bc2daf665393731553c1c95558217d094b8d28861315',
}


def read(path):
    return json.loads(path.read_text())


def canonical(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def need(ok, message):
    if not ok:
        raise ValueError(message)


def check_manifest(root, stage):
    manifest = root / 'evidence' / stage / 'source_files.json'
    need(hashlib.sha256(manifest.read_bytes()).hexdigest() == MANIFESTS[stage],
         stage + ': frozen source-manifest identity')
    files = read(manifest)
    for relative, expected in files.items():
        path = root / relative
        need(path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() == expected,
             stage + ': changed or missing source ' + relative)
    return len(files)


def restore(source, destination):
    source = source.resolve()
    destination = destination.resolve()
    need(source != destination and source not in destination.parents,
         'The audit copy must be outside the source repository')
    need(not destination.exists(), 'Audit destination already exists')
    check_manifest(source, 'unified_20261016')
    shutil.copytree(source, destination, ignore=shutil.ignore_patterns(
        '.git', '__pycache__', 'node_modules', 'work', 'verification-repository',
        '*.pdf', '*.zip', '*.bin', '*.o', '*.log', '*.aux', '*.out', '*.toc',
        '*.fls', '*.fdb_latexmk'), copy_function=shutil.copyfile)
    receipts = []
    if (source / 'evidence/review_20261017/review.json').is_file():
        spec = importlib.util.spec_from_file_location('prepublication_review', source / 'tools/verify_review_20261017.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        module.verify_current(source)
        restored_count = module.restore_parent_files(source, destination)
        receipts.append({'stage_undone':'review_20261017', 'parent_files_restored':restored_count,
                         'scope':'R8_2_24 correction undone only inside this historical replay copy'})
    stages = ['unified_20261016', 'theoretical_20261016',
              'upper_residual_20261002c', 'upper_residual_20261002b']
    for stage in stages:
        manifest_root = source if stage == 'unified_20261016' else destination
        checked_files = check_manifest(manifest_root, stage)
        evidence = manifest_root / 'evidence' / stage
        prior = read(evidence / 'previous_records.json')
        restored = {}
        stage_receipt = {'stage_undone': stage,
                         'source_manifest_sha256': MANIFESTS[stage],
                         'source_files_checked': checked_files, 'ranks': {}}
        for rank, metadata in prior['ranks'].items():
            relative = metadata.get('ledger', metadata.get('ledger_path'))
            if not relative:
                relative = {'7': 'supplements/rank7/output/rank7_ledger.json',
                            '8': 'supplements/rank8/data/decisions.json'}[rank]
            rows = read(destination / relative)
            originals = {row['id']: row for row in metadata['previous_records']}
            need(len(rows) == metadata['records'], stage + ': complete record count')
            need(canonical([row for row in rows if row['id'] not in originals])
                 == metadata['unchanged_records_sha256'], stage + ': unchanged records')
            for row in rows:
                if row['id'] in originals:
                    need(canonical(row) == metadata['transitions'][row['id']]['new_record_sha256'],
                         stage + ': current transition ' + row['id'])
            historical = [copy.deepcopy(originals.get(row['id'], row)) for row in rows]
            need(canonical(historical) == metadata['baseline_canonical_sha256'],
                 stage + ': exact complete parent ledger')
            restored[relative] = historical
            stage_receipt['ranks'][rank] = {
                'records': len(historical),
                'counts': dict(collections.Counter(row['status'] for row in historical)),
                'baseline_canonical_sha256': canonical(historical),
            }
        if stage == 'unified_20261016':
            parent = read(evidence / 'parent_files.json')
            with zipfile.ZipFile(evidence / 'parent_files.zip') as archive:
                need(set(archive.namelist()) == set(parent), 'Exact unified parent-file inventory')
                for relative, metadata in parent.items():
                    raw = archive.read(relative)
                    need(len(raw) == metadata['bytes'] and hashlib.sha256(raw).hexdigest() == metadata['sha256'],
                         'Exact unified parent file ' + relative)
                    target = destination / relative
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(raw)
            decisions = read(evidence / 'decisions.json')
            for rank in (7, 8):
                relative = f'supplements/rank{rank}/data/model_catalog.json'
                new = {row['id'] for row in decisions
                       if row['rank'] == rank and row['status'] == 'unitarily_realized'}
                old = [row for row in read(source / relative) if row['id'] not in new]
                need(canonical(old) == prior[f'rank{rank}_previous_models_canonical_sha256'],
                     'Exact previous model catalogue')
                (destination / relative).write_text(json.dumps(old, indent=2) + '\n')
        baseline = evidence / 'baseline_files'
        if baseline.exists():
            for path in baseline.rglob('*'):
                if path.is_file():
                    target = destination / path.relative_to(baseline)
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(path.read_bytes())
        for relative, historical in restored.items():
            (destination / relative).write_text(json.dumps(historical, indent=2) + '\n')
        receipts.append(stage_receipt)
    # Reassert the terminal historical files byte-for-byte; ledger reconstruction
    # above is canonical JSON, while these model/driver files require exact bytes.
    terminal = destination / 'evidence/upper_residual_20261002b/baseline_files'
    final_files = {}
    for path in terminal.rglob('*'):
        if path.is_file():
            relative = path.relative_to(terminal)
            target = destination / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(path.read_bytes())
            need(target.read_bytes() == path.read_bytes(), 'Final baseline file ' + str(relative))
            final_files[str(relative)] = hashlib.sha256(target.read_bytes()).hexdigest()
    report = {'status': 'PASS', 'source': str(source), 'destination': str(destination),
              'scope': 'Exact pre-stage-b files and ledgers reconstructed in an isolated copy; no mathematical replay performed by this helper.',
              'final_baseline_files_sha256': final_files,
              'stages': receipts}
    (destination.parent / (destination.name + '_restoration.json')).write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=ROOT,
                        help='Current classification repository (default: this checkout)')
    parser.add_argument('--output', type=Path, required=True,
                        help='New isolated directory outside the repository; must not exist')
    args = parser.parse_args()
    restore(args.repo, args.output)
