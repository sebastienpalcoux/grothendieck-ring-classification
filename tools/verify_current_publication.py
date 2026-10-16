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
        restored = restore_replay_sources(repo, target, sources)
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
                  'accepted_decisions': 35, 'remaining_ids': documents['remaining_ids'],
                  'restored_replay_sources': restored,
                  'rank6_archive_checksums': 'not part of standalone metadata check' if args.metadata_only else 'PASS',
                  'mode': 'metadata' if args.metadata_only else ('full historical chain' if args.historical else 'unified proof replay'),
                  'scope': 'Publication identities and the stated exact calculations; no independent human or Lean verification.'}
        print(json.dumps(report, indent=2))

if __name__ == '__main__':
    main()
