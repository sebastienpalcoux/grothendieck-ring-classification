#!/usr/bin/env python3
"""Check the R8_2_24 reopening and replay the frozen parent in isolation.

A historical PASS verifies only each checker's stated computational scope;
it does not reinstate the withdrawn categorical argument.
"""
from pathlib import Path
import argparse, collections, hashlib, json, shutil, subprocess, sys, tempfile, zipfile

ROOT = Path(__file__).resolve().parents[1]
STAGE = 'evidence/review_20261017'
UNIFIED_MANIFEST_SHA256 = 'aea53af376ee1622554e969a3d178b0c42124abd8da3eadc08d62cc5ee5cd851'
REVIEW_MANIFEST_SHA256 = 'c42ceb269f72760d53b374480dd97556ce8cb569774e2c360c3e16e1945c60d6'
PARENT_MANIFEST_SHA256 = '33d5b942f0a5882504d35198552c8f906f8a50adc102ea734ef10baa0cf62d64'


def need(ok, message):
    if not ok:
        raise ValueError(message)


def read(path):
    return json.loads(path.read_text())


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical(value):
    return sha(json.dumps(value, sort_keys=True, separators=(',', ':')).encode())


def check_sources(repo):
    for relative, identity in (('evidence/unified_20261016/source_files.json', UNIFIED_MANIFEST_SHA256),
                               (STAGE + '/source_files.json', REVIEW_MANIFEST_SHA256)):
        path = repo / relative
        need(sha(path.read_bytes()) == identity, 'Source manifest identity: ' + relative)
        for name, expected in read(path).items():
            need((repo / name).is_file() and sha((repo / name).read_bytes()) == expected,
                 'Changed or missing bound source: ' + name)


def restore_parent_files(source, destination):
    """Restore byte-exact pre-review files into a separate existing copy."""
    source, destination = source.resolve(), destination.resolve()
    need(source != destination and source not in destination.parents,
         'Historical restoration requires a separate directory outside the source')
    path = source / STAGE / 'parent_files.json'
    need(sha(path.read_bytes()) == PARENT_MANIFEST_SHA256, 'Parent manifest identity')
    manifest = read(path)
    with zipfile.ZipFile(source / STAGE / 'parent_files.zip') as archive:
        need(set(archive.namelist()) == set(manifest), 'Exact parent archive inventory')
        for relative, expected in manifest.items():
            target = (destination / relative).resolve()
            need(destination in target.parents, 'Unsafe historical path')
            raw = archive.read(relative)
            need(len(raw) == expected['bytes'] and sha(raw) == expected['sha256'],
                 'Historical parent byte identity: ' + relative)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(raw)
    return len(manifest)


def verify_current(repo):
    check_sources(repo)
    stage = repo / STAGE
    review = read(stage / 'review.json')
    need(review['reopened_ids'] == ['R8_2_24'] and review['historical_stage'] == 'unified_20261016',
         'Exact correction inventory')
    rows = read(repo / review['ledger'])
    need(len(rows) == len({r['id'] for r in rows}) == 973, 'Full rank-eight ledger inventory')
    changed = [r for r in rows if r['id'] == 'R8_2_24']
    need(changed == [review['current_record']], 'Exact reopened current record')
    need(changed[0]['status'] == 'unresolved' and 'certificate' not in changed[0],
         'Withdrawn exclusion must not remain a current certificate')
    need(canonical(rows) == review['current_ledger_canonical_sha256'], 'Current complete ledger hash')
    need(canonical([r for r in rows if r['id'] != 'R8_2_24']) == review['unchanged_records_canonical_sha256'],
         'All other rank-eight records unchanged')
    parent = [review['previous_record'] if r['id'] == 'R8_2_24' else r for r in rows]
    need(canonical(parent) == review['previous_ledger_canonical_sha256'], 'Exact previous complete ledger')
    unified = read(repo / 'evidence/unified_20261016/decisions.json')
    decisions = read(stage / 'decisions.json')
    need(len(unified) == 36 and decisions == [r for r in unified if r['id'] != 'R8_2_24'],
         '35 accepted decisions are the unchanged historical decisions except R8_2_24')
    need(collections.Counter(r['status'] for r in decisions) == {'excluded':28, 'unitarily_realized':7},
         'Current accepted continuation counts')
    remaining = read(stage / 'remaining_ids.json')
    need(remaining == {'6':['R6_4_155','R6_8_1660'], '7':[], '8':['R8_2_24']}, 'Three exact open IDs')
    expected = read(stage / 'expected_totals.json')
    paths = {'6':'supplements/rank6/data/decisions.json', '7':'supplements/rank7/output/rank7_ledger.json',
             '8':'supplements/rank8/data/decisions.json'}
    for rank, relative in paths.items():
        records = read(repo / relative)
        totals = collections.Counter(r['status'] for r in records)
        totals.setdefault('unresolved', 0)
        need(dict(totals) == expected[rank], 'Current partition: rank ' + rank)
        need([r['id'] for r in records if r['status'] == 'unresolved'] == remaining[rank],
             'Current unresolved inventory: rank ' + rank)
        current = {r['id']:r for r in records}
        need(all(current[d['id']]['status'] == d['status'] for d in decisions if str(d['rank']) == rank),
             'Accepted decisions match current ledger: rank ' + rank)
    all_cases = read(stage / 'all_cases.json')
    old_cases = read(repo / 'evidence/unified_20261016/all_cases.json')
    need(len(all_cases) == 38 and {r['id'] for r in all_cases} == {r['id'] for r in old_cases},
         'Complete original 38-case inventory')
    need({r['id'] for r in all_cases if r['status'] == 'unresolved'} == set(sum(remaining.values(), [])),
         'Current all-case unresolved statuses')
    need({r['id']:r['status'] for r in all_cases if r['status'] != 'unresolved'} ==
         {r['id']:r['status'] for r in decisions}, 'Current all-case accepted statuses')
    return {'status':'PASS', 'scope':'Correction, source identity and ledger consistency; no new categorification decision.',
            'accepted_decisions':35, 'accepted_exclusions':28, 'accepted_models':7,
            'remaining_ids':remaining, 'status_totals':expected}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=ROOT)
    parser.add_argument('--historical', action='store_true', help='Also run the full earlier historical update chain')
    parser.add_argument('--metadata-only', action='store_true', help='Check correction identities without computational historical replay')
    args = parser.parse_args()
    need(not (args.historical and args.metadata_only), 'Choose historical replay or metadata-only')
    repo = args.repo.resolve()
    report = verify_current(repo)
    with tempfile.TemporaryDirectory(prefix='grc-review-parent-') as temp:
        destination = Path(temp) / 'repo'
        if args.metadata_only:
            destination.mkdir()
        else:
            shutil.copytree(repo, destination, copy_function=shutil.copyfile,
                            ignore=shutil.ignore_patterns('.git','node_modules','__pycache__','work'))
        report['restored_parent_files'] = restore_parent_files(repo, destination)
        review = read(repo / STAGE / 'review.json')
        need(canonical(read(destination / review['ledger'])) == review['previous_ledger_canonical_sha256'],
             'Restored historical complete ledger')
        if not args.metadata_only:
            command = [sys.executable] + (['-O'] if not __debug__ else []) + [str(destination / 'tools/verify_unified_20261016.py'), '--repo', str(destination)]
            if args.historical:
                command.append('--historical')
            subprocess.run(command, cwd=destination, check=True)
            report['historical_replay'] = 'full earlier update chain' if args.historical else 'frozen unified stage'
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
