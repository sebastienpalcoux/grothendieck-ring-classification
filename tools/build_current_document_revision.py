#!/usr/bin/env python3
"""Bind every current manuscript and supplement copy after the PDF builds."""
from pathlib import Path
import argparse
import json
from current_publication import DOCUMENT_REVISION, document_paths, sha, need

ROOT = Path(__file__).resolve().parents[1]
WEB_COPIES = {
    'papers/rank2.pdf': 'manuscripts/rank2.pdf',
    'papers/rank3.pdf': 'manuscripts/rank3.pdf',
    'papers/rank4.pdf': 'manuscripts/rank4/papers/companion.pdf',
    'papers/rank4_finite.pdf': 'manuscripts/rank4/papers/finite.pdf',
    'papers/rank4_companion.pdf': 'manuscripts/rank4/papers/companion.pdf',
    'papers/rank4_guide.pdf': 'manuscripts/rank4/papers/verification_guide.pdf',
    'papers/rank5.pdf': 'manuscripts/rank5/papers/manuscript.pdf',
    'papers/rank5_guide.pdf': 'manuscripts/rank5/papers/verification_guide.pdf',
    'papers/rank6.pdf': 'manuscripts/rank6/papers/manuscript.pdf',
    'papers/rank6_guide.pdf': 'manuscripts/rank6/papers/verification_guide.pdf',
    'papers/rank7.pdf': 'manuscripts/rank7/papers/manuscript.pdf',
    'papers/rank8.pdf': 'manuscripts/rank8/paper/rank8.pdf',
    'papers/rank8-reviewed.pdf': 'manuscripts/rank8/paper/rank8.pdf',
    'papers/rank6_addendum_20261002.pdf': 'manuscripts/rank6/papers/manuscript.pdf',
    'papers/prepublication-review-2026-10-17.pdf': 'manuscripts/prepublication-review-2026-10-17.pdf',
}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=ROOT)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    repo = args.repo.resolve()
    documents = {}
    for name in sorted(document_paths(repo)):
        raw = (repo / name).read_bytes()
        documents[name] = {'sha256': sha(raw), 'bytes': len(raw)}
    need(set(WEB_COPIES.values()) <= set(documents), 'Compile every current manuscript and guide before binding the revision')
    revision = {'schema': 'current-document-revision/v1', 'date': '2026-10-17',
                'accepted_decisions': 36,
                'remaining_ids': ['R6_4_155', 'R6_8_1660'],
                'research_progress': 'evidence/rigidity_20261017/rank6/research_progress.json',
                'research_progress_sha256': sha((repo / 'evidence/rigidity_20261017/rank6/research_progress.json').read_bytes()),
                'documents': documents, 'web_copies': WEB_COPIES}
    text = json.dumps(revision, indent=2) + '\n'
    target = repo / DOCUMENT_REVISION
    if args.check:
        need(target.is_file() and target.read_text() == text, 'Current document manifest is stale')
    else:
        target.write_text(text)
    print(json.dumps({'status': 'PASS', 'documents': len(documents), 'website_copies': len(WEB_COPIES),
                      'manifest': DOCUMENT_REVISION, 'sha256': sha(text.encode())}, indent=2))

if __name__ == '__main__':
    main()
