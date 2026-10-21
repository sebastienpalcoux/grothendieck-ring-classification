#!/usr/bin/env python3
"""Build a distinct frontier archive over the immutable, replayed M3 archive.

The existing M3 archive is input only. Its proof sources, evidence, data and
replay logs remain byte-identical in the new archive. Current publication tools
and manuscript files may supersede old copies; every superseded byte stream is
retained under publication/baseline_members. Both extracted metadata verifiers
and a fresh full frontier replay must pass before the new archive is written.
"""
from pathlib import Path
import argparse
import json
import os
import subprocess
import sys
import tempfile
import zipfile

from rank8_frontier import (ROOT, ARCHIVE, EVIDENCE, PUBLICATION, LEDGER,
                            commands, need, safe_path, sha, source_inventory,
                            validate_ledger)


BASELINE_ARCHIVE = 'supplements/rank8/release/rank8-certified-through-m3.zip'
BASELINE_ARCHIVE_SHA256 = '7bbc31e24113a2f41315d74d45fa499638b7d5b7185f659d5e3ed468ad7e8341'
BASELINE_PREFIX = 'rank8-certified-through-m3/'
ARCHIVE_PREFIX = 'rank8-certified-frontier-20261021/'
OLD_RECEIPTS = (
    'evidence/rank8_m3_20261021/pipeline/continuation_replay.json',
    'evidence/rank8_m3_20261021/pipeline/continuation_replay_optimized_invocation.json',
)
SUFFIXES = {'.py', '.cpp', '.h', '.hpp', '.json', '.jsonl', '.gz', '.txt',
            '.md', '.tex', '.pdf', '.csv', '.sage', '.g', '.log', '.bib'}


def read_baseline(repo):
    path = repo / BASELINE_ARCHIVE
    raw = path.read_bytes()
    need(sha(raw) == BASELINE_ARCHIVE_SHA256, 'Immutable baseline archive changed')
    files = {}
    with zipfile.ZipFile(path) as archive:
        for item in archive.infolist():
            need(not item.is_dir(), 'Unexpected directory entry in baseline archive')
            need(item.filename.startswith(BASELINE_PREFIX), 'Unexpected baseline archive root')
            name = item.filename[len(BASELINE_PREFIX):]
            need(safe_path(name) and name not in files, 'Unsafe or duplicate baseline member')
            need((item.external_attr >> 16) & 0o170000 != 0o120000, 'Symlink in baseline archive')
            files[name] = archive.read(item)
    hashes = json.loads(files['SHA256SUMS.json'])
    need(set(hashes) == set(files) - {'SHA256SUMS.json'}, 'Baseline checksum coverage')
    need(all(sha(files[p]) == digest for p, digest in hashes.items()), 'Baseline checksum mismatch')
    protected = set()
    reports = [json.loads(files[name]) for name in OLD_RECEIPTS]
    for report in reports:
        need(report['status'] == 'PASS', 'Baseline full replay required')
        for field in ('proof_source_sha256', 'source_manifests_sha256'):
            for name, digest in report[field].items():
                need(name in files and sha(files[name]) == digest, 'Baseline proof binding: ' + name)
                protected.add(name)
        for section in report['sections']:
            name = section['log']
            need(name in files and sha(files[name]) == section['log_sha256'], 'Baseline log binding: ' + name)
            protected.add(name)
    need(reports[0]['ledger_digest'] == reports[1]['ledger_digest'], 'Baseline replay ledger mismatch')
    for field in ('proof_source_sha256', 'source_manifests_sha256'):
        need(reports[0][field] == reports[1][field], 'Baseline replay source mismatch')
    protected.update(OLD_RECEIPTS)
    return files, protected


def frontier_inputs(repo):
    summary = validate_ledger(repo)
    manifest_name = PUBLICATION + '/source_manifest.json'
    manifest_raw = (repo / manifest_name).read_bytes()
    manifest = json.loads(manifest_raw)
    need(manifest == source_inventory(repo), 'Frontier source manifest changed; replay required')
    paths = {manifest_name, LEDGER, 'tools/build_rank8_frontier_release.py'} | set(manifest)
    reports = []
    for filename, optimized in (('replay_normal.json', False), ('replay_optimized.json', True)):
        name = PUBLICATION + '/' + filename
        raw = (repo / name).read_bytes()
        report = json.loads(raw)
        need(report['status'] == 'PASS' and report['mathematical_replay_performed'] is True,
             'Full frontier replay required: ' + name)
        need(report['optimized_python'] is optimized, 'Incorrect frontier replay lane: ' + name)
        need(report['source_manifest_sha256'] == sha(manifest_raw), 'Frontier replay source mismatch')
        need(report['ledger_sha256'] == summary['ledger_sha256'], 'Frontier replay ledger mismatch')
        paths.add(name)
        for section in report['sections']:
            log = section['log']
            need(safe_path(log) and section['returncode'] == 0, 'Invalid frontier replay section')
            need(sha((repo / log).read_bytes()) == section['log_sha256'], 'Frontier replay log changed: ' + log)
            paths.add(log)
        reports.append({'path': name, 'sha256': sha(raw), 'optimized_python': optimized})
    # Do not rely on a suffix allowlist for manifest-bound inputs or logs.
    for folder in (EVIDENCE, 'supplements/rank8/output/frontier_20261021',
                   'tools', 'manuscripts/rank8/paper'):
        for path in (repo / folder).rglob('*'):
            name = path.relative_to(repo).as_posix()
            if (path.is_file() and path.suffix in SUFFIXES and
                    '__pycache__' not in path.parts and
                    not name.startswith(PUBLICATION + '/') and
                    path.name != 'release_manifest.json' and
                    not any(part.startswith('.') for part in path.relative_to(repo).parts)):
                paths.add(name)
    for name in paths:
        need(safe_path(name) and (repo / name).is_file(), 'Missing or unsafe package input: ' + name)
    return paths, summary, reports, sha(manifest_raw)


def collect(repo):
    baseline, protected = read_baseline(repo)
    paths, summary, reports, manifest_sha = frontier_inputs(repo)
    files = dict(baseline)
    replacements = {}
    for name in sorted(paths):
        raw = (repo / name).read_bytes()
        if name in baseline and raw != baseline[name]:
            need(name not in protected, 'Refusing to alter a baseline proof input: ' + name)
            need(name.startswith(('tools/', 'manuscripts/rank8/paper/')),
                 'Refusing to alter a baseline evidence/data member: ' + name)
            replacements[name] = {'baseline_sha256': sha(baseline[name]), 'current_sha256': sha(raw)}
            files[PUBLICATION + '/baseline_members/' + name] = baseline[name]
        files[name] = raw
    files[PUBLICATION + '/baseline_members/README.md'] = baseline['README.md']
    files[PUBLICATION + '/baseline_members/SHA256SUMS.json'] = baseline['SHA256SUMS.json']
    need(all(files[p] == baseline[p] for p in protected), 'Baseline proof byte preservation failed')
    for name in baseline:
        if name not in {'README.md', 'SHA256SUMS.json'} and name not in replacements:
            need(files[name] == baseline[name], 'Unexpected baseline member replacement: ' + name)
    counts = summary['counts']
    files['README.md'] = (
        '# Rank-eight certified frontier, 21 October 2026\n\n'
        'This separately replayed continuation overlays the immutable multiplicity-three release. '
        f"It records {summary['new_decisions']} new decisions; current M3 counts are "
        + ', '.join(f'{key}: {value}' for key, value in sorted(counts.items())) + '.\n\n'
        'The original M3 ledger, all baseline proof inputs, and both baseline replay receipts '
        'are preserved byte-for-byte. Current decisions are in '
        f'`{LEDGER}`. Current article: `manuscripts/rank8/paper/rank8.pdf`. '
        'Source-bound attempt records distinguish exhaustive proofs, bounded searches and unresolved cases.\n\n'
        'With Python 3.12, a C++17 compiler, and the listed Python dependencies:\n\n'
        '```sh\npython -m pip install -r supplements/rank7/requirements-m5.txt\n'
        'python supplements/rank8/software/verify_m3_continuation.py --output frontier-validation/baseline_normal.json\n'
        'python -O supplements/rank8/software/verify_m3_continuation.py --output frontier-validation/baseline_optimized.json\n'
        'python tools/verify_rank8_frontier.py\n'
        'python -O tools/verify_rank8_frontier.py\n```\n\n'
        'The explicit baseline output paths retain the frozen publication receipts and their logs. '
        'The old optimized lane starts assertion-enabled inherited checks; the new lane directly '
        'replays the frontier verifiers under `-O`. For a source/receipt check without redoing the '
        'mathematics, append `--metadata-only` to either verifier. Optional fresh group enumeration '
        'uses GAP with SmallGrp; the exact stored group transcript is included.\n\n'
        'This archive was checked after extraction with both old and new metadata verifiers '
        'in normal and optimized Python, followed by a fresh full normal-Python replay of '
        'every frontier command. The fresh extracted replay and its logs are included; '
        'the immutable baseline mathematics is protected by its existing full replay hashes. '
        'Superseded publication tools and papers are retained under '
        f'`{PUBLICATION}/baseline_members/`. AI-assisted research remains subject to '
        'independent mathematical scrutiny; no Lean formalization is asserted.\n'
    ).encode()
    package = {
        'schema': 'rank8-frontier-package/v1', 'date': '2026-10-21',
        'baseline_archive': BASELINE_ARCHIVE,
        'baseline_archive_sha256': BASELINE_ARCHIVE_SHA256,
        'baseline_members': len(baseline),
        'baseline_proof_members_preserved': len(protected),
        'publication_replacements': replacements,
        'frontier_summary': summary, 'frontier_replays': reports,
        'frontier_source_manifest_sha256': manifest_sha,
        'baseline_replays': {name: sha(files[name]) for name in OLD_RECEIPTS},
    }
    files[PUBLICATION + '/package_manifest.json'] = (json.dumps(package, indent=2) + '\n').encode()
    files['SHA256SUMS.json'] = (json.dumps({p: sha(raw) for p, raw in sorted(files.items())
                                         if p != 'SHA256SUMS.json'}, indent=2) + '\n').encode()
    return files, package


def standalone_checks(files):
    results = []
    full_results = []
    with tempfile.TemporaryDirectory(prefix='rank8-frontier-package-') as directory, \
            tempfile.TemporaryDirectory(prefix='rank8-frontier-extracted-replay-') as replay_directory:
        repo = Path(directory)
        for name, raw in files.items():
            need(safe_path(name), 'Unsafe extracted package path')
            target = repo / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(raw)
        for script in ('supplements/rank8/software/verify_m3_continuation.py',
                       'tools/verify_rank8_frontier.py'):
            for optimized in (False, True):
                command = [sys.executable] + (['-O'] if optimized else []) + [str(repo / script), '--metadata-only']
                env = dict(os.environ)
                env.pop('PYTHONOPTIMIZE', None)
                env.pop('PYTHONPATH', None)
                run = subprocess.run(command, cwd=repo, env=env, text=True, capture_output=True)
                need(run.returncode == 0, 'Standalone metadata failed: ' + script + '\n' + run.stdout + run.stderr)
                report = json.loads(run.stdout)
                need(report['status'] == 'METADATA_PASS', 'Standalone metadata receipt missing')
                results.append({'script': script, 'optimized_python': optimized,
                                'status': 'METADATA_PASS', 'report_sha256': sha(run.stdout.encode())})
        # Run from only the extracted package. Output and logs live outside it,
        # so neither frozen publication replay lane can be overwritten.
        before = source_inventory(repo)
        expected_scripts = commands(repo)
        output = Path(replay_directory) / 'frontier_normal.json'
        script = 'tools/verify_rank8_frontier.py'
        command = [sys.executable, str(repo / script), '--output', str(output)]
        env = dict(os.environ)
        env.pop('PYTHONOPTIMIZE', None)
        env.pop('PYTHONPATH', None)
        env.update(OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1')
        run = subprocess.run(command, cwd=repo, env=env, text=True, capture_output=True)
        need(run.returncode == 0, 'Extracted full frontier replay failed:\n' + run.stdout + run.stderr)
        raw = output.read_bytes()
        report = json.loads(raw)
        need(report['status'] == 'PASS' and report['mathematical_replay_performed'] is True and
             report['optimized_python'] is False, 'Extracted full replay did not verify the normal lane')
        need([item['script'] for item in report['sections']] == expected_scripts and
             all(item['returncode'] == 0 for item in report['sections']),
             'Extracted full replay command coverage differs')
        need(source_inventory(repo) == before, 'Extracted full replay changed a source input')
        # Preserve the actual logs, relocating only their paths in the package
        # copy of the new receipt. The original raw report digest is retained.
        for item in report['sections']:
            log = Path(item['log'])
            need(log.is_absolute() and log.is_relative_to(Path(replay_directory)),
                 'Extracted full replay log escaped its temporary output folder')
            content = log.read_bytes()
            need(sha(content) == item['log_sha256'], 'Extracted full replay log hash differs')
            name = PUBLICATION + '/standalone_full_replay_normal_logs/' + log.name
            need(name not in files, 'Duplicate extracted full replay log')
            files[name] = content
            item['log'] = name
        report['extracted_replay_original_report_sha256'] = sha(raw)
        report['log_paths_relocated_for_package'] = True
        report_name = PUBLICATION + '/standalone_full_replay_normal.json'
        report_raw = (json.dumps(report, indent=2) + '\n').encode()
        files[report_name] = report_raw
        full_results.append({'script': script, 'optimized_python': False,
                             'status': 'PASS', 'mathematical_replay_performed': True,
                             'source_inventory_unchanged': True,
                             'source_manifest_sha256': report['source_manifest_sha256'],
                             'ledger_sha256': report['ledger_sha256'],
                             'section_count': len(report['sections']),
                             'sections': report['sections'],
                             'original_report_sha256': sha(raw),
                             'packaged_report': report_name,
                             'packaged_report_sha256': sha(report_raw)})
    return results, full_results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=ROOT)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    repo = args.repo.resolve()
    output = (args.output or repo / ARCHIVE).resolve()
    need(output != (repo / BASELINE_ARCHIVE).resolve(), 'Cannot overwrite the immutable M3 archive')
    need(not output.is_relative_to(repo / 'evidence/rank8_m3_20261021'), 'Cannot write into baseline evidence')
    files, package = collect(repo)
    checks, full_checks = standalone_checks(files)
    package.update(standalone_metadata_checks=checks,
                   standalone_full_replay_checks=full_checks)
    files[PUBLICATION + '/package_manifest.json'] = (json.dumps(package, indent=2) + '\n').encode()
    files['SHA256SUMS.json'] = (json.dumps({p: sha(raw) for p, raw in sorted(files.items())
                                         if p != 'SHA256SUMS.json'}, indent=2) + '\n').encode()
    # Check source stability once more after extracted validation and before publication.
    need(sha((repo / BASELINE_ARCHIVE).read_bytes()) == BASELINE_ARCHIVE_SHA256,
         'Baseline archive changed during packaging')
    need(source_inventory(repo) == json.loads(files[PUBLICATION + '/source_manifest.json']),
         'Frontier sources changed during packaging')
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(prefix=output.name + '.', suffix='.tmp', dir=output.parent, delete=False) as handle:
        temporary = Path(handle.name)
    try:
        with zipfile.ZipFile(temporary, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for name, raw in sorted(files.items()):
                info = zipfile.ZipInfo(ARCHIVE_PREFIX + name, date_time=(2026, 10, 21, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o644 << 16
                archive.writestr(info, raw, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
        temporary.replace(output)
    finally:
        temporary.unlink(missing_ok=True)
    manifest = dict(package, files_sha256={p: sha(raw) for p, raw in sorted(files.items())},
                    archive_sha256=sha(output.read_bytes()))
    target = repo / PUBLICATION / 'release_manifest.json'
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(manifest, indent=2) + '\n')
    print(json.dumps({'output': str(output), 'files': len(files), 'bytes': output.stat().st_size,
                      'sha256': manifest['archive_sha256'], 'standalone_metadata_checks': checks,
                      'standalone_full_replay_checks': [
                          {key: value for key, value in check.items() if key != 'sections'}
                          for check in full_checks],
                      'baseline_proof_members_preserved': package['baseline_proof_members_preserved']}, indent=2))


if __name__ == '__main__':
    main()
