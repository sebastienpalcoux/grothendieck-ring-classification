#!/usr/bin/env python3
"""Verify current manuscripts, website copies, decisions and immutable proof replays.

Metadata-only mode is standalone in the current download. The complete earlier
replay chain requires the full repository. Replay sources are restored only in
a temporary directory; no published manuscript is replaced.
"""
from pathlib import Path
import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from current_publication import validate_documents, replay_sources, restore_replay_sources, need
from reader_resources import validate_reader_resources
from rank7_publication import extension, historical_rank7_bytes, LEDGER
from rank8_publication import extension as rank8_extension
from verify_rigidity_20261017 import verify_current as verify_rigidity, restore_parent_files as restore_rigidity_parent

ROOT = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=ROOT)
    parser.add_argument('--metadata-only', action='store_true')
    parser.add_argument('--historical', action='store_true')
    args = parser.parse_args()
    need(not (args.metadata_only and args.historical), 'Choose metadata-only or full historical replay')
    repo = args.repo.resolve()
    has_website = (repo / 'site/dist/papers').is_dir()
    documents = validate_documents(repo, check_web=has_website)
    reader_resources = validate_reader_resources(repo, check_web=has_website)
    rank7_update = extension(repo)
    historical = historical_rank7_bytes(repo) if rank7_update else None
    rank7_metadata = None
    if rank7_update:
        with tempfile.TemporaryDirectory(prefix='rank7-m5-metadata-') as directory:
            command = [sys.executable] + (['-O'] if sys.flags.optimize else [])
            command += [str(repo/'supplements/rank7/software/verify_m5.py'), '--metadata-only',
                        '--output', str(Path(directory)/'receipt.json')]
            check = subprocess.run(command, cwd=repo, text=True, capture_output=True)
            need(check.returncode == 0, 'Rank-seven M5 metadata check failed:\n' + check.stdout + check.stderr)
            rank7_metadata = json.loads(check.stdout)
    rank8_update = rank8_extension(repo)
    rank8_check_receipt = None
    if rank8_update:
        with tempfile.TemporaryDirectory(prefix='rank8-m3-check-') as directory:
            command = [sys.executable] + (['-O'] if sys.flags.optimize else [])
            command += [str(repo/'supplements/rank8/software/verify_m3_continuation.py'), '--output', str(Path(directory)/'receipt.json')]
            if args.metadata_only: command.append('--metadata-only')
            check = subprocess.run(command,cwd=repo,text=True,capture_output=True)
            need(check.returncode==0,'Rank-eight M3 check failed:\n'+check.stdout+check.stderr)
            rank8_check_receipt=json.loads((Path(directory)/'receipt.json').read_text())
    rigidity = verify_rigidity(repo, replay=not args.metadata_only,
                              historical_rank7=json.loads(historical) if historical else None)
    rank6_command = [sys.executable] + (['-O'] if sys.flags.optimize else [])
    rank6_command += [str(repo / 'evidence/rigidity_20261017/rank6/run_checks.py'),
                      '--repo', str(repo)]
    if args.metadata_only:
        rank6_command.append('--metadata-only')
    rank6_check = subprocess.run(rank6_command, cwd=repo, text=True, capture_output=True)
    need(rank6_check.returncode == 0, 'Rank-six necessary-condition evidence failed:\n'
         + rank6_check.stdout + rank6_check.stderr)
    rank6_progress = json.loads(rank6_check.stdout)
    rank4_package = repo / 'supplements/rank4/unrestricted'
    rank4_check = subprocess.run(
        [sys.executable, str(rank4_package / 'verify_package.py'),
         '--manuscript-root', str(repo / 'manuscripts/rank4/papers')],
        cwd=repo, text=True, capture_output=True)
    need(rank4_check.returncode == 0, 'Unrestricted rank-four publication binding failed:\n'
         + rank4_check.stdout + rank4_check.stderr)
    sources = replay_sources(repo)
    with tempfile.TemporaryDirectory(prefix='grc-current-publication-') as folder:
        target = Path(folder) / 'repo'
        if args.metadata_only:
            names = {'tools/verify_review_20261017.py',
                     'evidence/unified_20261016/source_files.json',
                     'evidence/review_20261017/source_files.json',
                     'evidence/review_20261017/parent_files.json',
                     'evidence/review_20261017/parent_files.zip',
                     'supplements/rank6/data/decisions.json',
                     'supplements/rank7/output/rank7_ledger.json',
                     'supplements/rank8/data/decisions.json'}
            for name in ('evidence/unified_20261016/source_files.json',
                         'evidence/review_20261017/source_files.json'):
                names.update(json.loads((repo / name).read_text()))
            for name in names:
                raw = sources[name] if name in sources else (repo / name).read_bytes()
                path = target / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(raw)
        else:
            shutil.copytree(repo, target, copy_function=shutil.copyfile,
                            ignore=shutil.ignore_patterns('.git', 'node_modules', '__pycache__',
                                                         'work', 'site', '*.bin', '*.aux',
                                                         '*.out', '*.toc', '*.fls', '*.fdb_latexmk'))
        if historical:
            (target / LEDGER).write_bytes(historical)
        restored = restore_replay_sources(repo, target, sources)
        restored += restore_rigidity_parent(repo, target)
        if not args.metadata_only:
            archived = subprocess.run([sys.executable, str(target / 'supplements/rank6/check_manifest.py')],
                                      cwd=target, text=True, capture_output=True)
            need(archived.returncode == 0, 'Immutable rank-six archive check failed:\n' + archived.stdout + archived.stderr)
        command = [sys.executable] + (['-O'] if sys.flags.optimize else [])
        command += [str(target / 'tools/verify_review_20261017.py'), '--repo', str(target)]
        if args.metadata_only:
            command.append('--metadata-only')
        if args.historical:
            command.append('--historical')
        result = subprocess.run(command, cwd=target, text=True, capture_output=True)
        need(result.returncode == 0, 'Proof/decision replay failed:\n' + result.stdout + result.stderr)
        # The historical dispatcher may print several JSON receipts; retain the
        # complete stream rather than selecting a convenient intermediate PASS.
        if not args.metadata_only:
            print(result.stdout, end='')
        report = {'status': 'PASS', 'current_documents': len(documents['documents']),
                  'website_pdf_copies_checked': len(documents['web_copies']) if has_website else 0,
                  'declared_website_pdf_copies': len(documents['web_copies']),
                  'historical_accepted_decisions': 36,
                  'historical_decision_scope': 'The earlier 38-case continuation; M5 decisions are separate',
                  'remaining_ids': documents['remaining_ids'],
                  'historical_rigidity_stage': rigidity,
                  'rank7_m5_update': rank7_update,
                  'rank8_m3_update': rank8_update, 'rank8_m3_check': rank8_check_receipt,
                  'rank7_m5_metadata_check': rank7_metadata,
                  'rank6_necessary_conditions': rank6_progress,
                  'reader_resources': reader_resources,
                  'rank4_unrestricted_package': 'PASS: source/data identities and generated manuscript tables; exact replay is a separate check',
                  'restored_replay_sources': restored,
                  'rank6_archive_checksums': 'not part of standalone metadata check' if args.metadata_only else 'PASS',
                  'mode': 'metadata' if args.metadata_only else ('full historical chain' if args.historical else 'unified proof replay'),
                  'scope': 'Publication identities and the stated exact calculations; no independent human or Lean verification.'}
        print(json.dumps(report, indent=2))

if __name__ == '__main__':
    main()
