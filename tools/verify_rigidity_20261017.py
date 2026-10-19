#!/usr/bin/env python3
"""Verify source-bound R24 theory evidence, its single ledger decision, and finite replays.

The categorical exclusion is a mathematical proof, not a computational theorem.
This verifier checks source identity, preservation, partitions, and stated finite claims.
"""
from pathlib import Path, PurePosixPath
import argparse
import collections
import gzip
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
STAGE = 'evidence/rigidity_20261017'
MANIFEST_SHA256 = '84015bd61fd627d19487e64ba1309c3edfaed5a78c9f8c5c6d8666dc6cb6991b'
PARENT_MANIFEST_SHA256 = '22b0b4d9248cba76873718b23022542d039b3d13092e38de12ad46b50bfa4f11'
PARENT_ARCHIVE_SHA256 = '7e0b4fac7f0c9678cb90166b06edf88f266e8841ed084ac720a044efd7dd9013'
SOURCE_ID = 'R8_2_24'
TENSOR_SHA256 = '2b4780441d9590e8e7269cd82b7675aa75cec11c39bd3e94bb372cca1ada6738'
REVIEWED_PROOF_SHA256 = '3492f0ab0679286f8f15fec4a8c0ac5fa46277cebf240ea250b82a67a666863c'
LEDGERS = {'6': 'supplements/rank6/data/decisions.json',
           '7': 'supplements/rank7/output/rank7_ledger.json',
           '8': 'supplements/rank8/data/decisions.json'}
REMAINING = {'6': ['R6_4_155', 'R6_8_1660'], '7': [], '8': []}
AUDITS = ('rank8/final_prerequisite_audit.md', 'rank8/final_structural_audit.md',
          'rank8/final_torus_audit.md')


def need(ok, message):
    if not ok:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read(path):
    return json.loads(path.read_text())


def canonical(value):
    return sha(json.dumps(value, sort_keys=True, separators=(',', ':')).encode())


def safe_relative(name):
    path = PurePosixPath(name)
    return bool(name) and not path.is_absolute() and '..' not in path.parts and path.as_posix() == name


def verify_sources(repo):
    """Bind the R24 evidence without importing mutable publication or rank-six prose."""
    repo = Path(repo).resolve()
    path = repo / STAGE / 'source_files.json'
    raw = path.read_bytes()
    need(sha(raw) == MANIFEST_SHA256, 'Rigidity source manifest identity')
    manifest = json.loads(raw)
    need(isinstance(manifest, dict) and manifest, 'Nonempty rigidity source manifest')
    for name, expected in manifest.items():
        need(safe_relative(name), 'Unsafe source manifest path')
        source = repo / name
        need(source.is_file() and sha(source.read_bytes()) == expected,
             'Changed or missing rigidity source: ' + name)
    required = [STAGE + '/rank8/R24_TORUS_RIGIDITY_PROOF.md'] + [STAGE + '/' + p for p in AUDITS]
    need(all(p in manifest for p in required), 'Full proof and all three fresh audits are bound')
    return {'source_files': len(manifest), 'manifest_sha256': MANIFEST_SHA256}


# Consistent with the interface used by earlier stage verifiers.
check_sources = verify_sources


def _parent_contents(source):
    source = Path(source).resolve()
    manifest_path = source / STAGE / 'parent_files.json'
    archive_path = source / STAGE / 'parent_files.zip'
    need(sha(manifest_path.read_bytes()) == PARENT_MANIFEST_SHA256, 'Parent ledger manifest identity')
    need(sha(archive_path.read_bytes()) == PARENT_ARCHIVE_SHA256, 'Parent ledger archive identity')
    manifest = read(manifest_path)
    need(set(manifest) == {LEDGERS['8']}, 'Exact parent ledger inventory')
    result = {}
    with zipfile.ZipFile(archive_path) as archive:
        names = archive.namelist()
        need(len(names) == len(set(names)) and set(names) == set(manifest), 'Exact parent archive inventory')
        for name, expected in manifest.items():
            need(safe_relative(name), 'Unsafe parent ledger path')
            raw = archive.read(name)
            need(len(raw) == expected['bytes'] and sha(raw) == expected['sha256'],
                 'Byte-exact parent ledger: ' + name)
            result[name] = raw
    return result


def restore_parent_files(source, destination):
    """Restore the exact reviewed rank-eight ledger only in a separate replay directory."""
    source, destination = Path(source).resolve(), Path(destination).resolve()
    need(source != destination and source not in destination.parents,
         'Parent replay requires an isolated destination outside the source')
    for name, raw in _parent_contents(source).items():
        target = (destination / name).resolve()
        need(destination in target.parents, 'Unsafe parent replay destination')
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
    return 1


def _proof_presentation(repo):
    folder = repo / STAGE / 'rank8'
    spec = read(folder / 'proof_presentation.json')
    raw = (folder / 'audited_proof_source.md').read_bytes()
    need(sha(raw) == REVIEWED_PROOF_SHA256 == spec['reviewed_source_sha256'],
         'Exact source reviewed by the three independent audits')
    text = raw.decode()
    for item in spec['clarifications'] + spec['replacements']:
        need(text.count(item['before']) == 1, 'Exact proof presentation substitution')
        text = text.replace(item['before'], item['after'])
    need(text.count(spec['insert_after']) == 1, 'Exact inner-functor convention location')
    text = text.replace(spec['insert_after'], spec['insert_after'] + spec['insertion'])
    actual = (folder / 'R24_TORUS_RIGIDITY_PROOF.md').read_bytes()
    need(text.encode() == actual and sha(actual) == spec['published_proof_sha256'],
         'Full proof has only the recorded audited clarifications and publication edits')
    return sha(actual)


def _source_tensor(repo):
    with gzip.open(repo / 'supplements/rank8/data/rank8_tables.txt.gz', 'rt') as stream:
        tensors = [json.loads(line.translate(str.maketrans('{}', '[]')))
                   for line in stream if line.strip()]
    need(len(tensors) == 973, 'Complete rank-eight source census')
    selected = sorted(t for t in tensors if max(v for plane in t for row in plane for v in row) == 2)
    need(len(selected) == 877, 'Complete multiplicity-two source band')
    tensor = selected[23]
    need(sha(json.dumps(tensor, separators=(',', ':')).encode()) == TENSOR_SHA256,
         'Canonical source tensor identity for R8_2_24')
    return tensor


def _receipts(repo, replay):
    stage = repo / STAGE
    inventory = read(stage / 'checker_receipts.json')
    need([x['name'] for x in inventory] == ['source', 'prerequisites', 'weights', 'independent_weights'],
         'Exact four-checker inventory')
    results = {}
    for item in inventory:
        for key in ('checker', 'normal_receipt', 'optimized_receipt'):
            need(safe_relative(item[key]), 'Unsafe checker or receipt path')
        normal, optimized = [read(stage / item[key]) for key in ('normal_receipt', 'optimized_receipt')]
        for mode, stored in enumerate((normal, optimized)):
            need(stored['checker'] == item['checker'] and stored['python_optimization'] == mode,
                 'Checker receipt execution mode')
            need(stored['result']['status'] == 'PASS' and stored['scope'] == item['scope'],
                 'Checker receipt scope and status')
        need(normal['result'] == optimized['result'], 'Normal and optimized finite results agree')
        results[item['name']] = normal['result']
    need(results['source']['tensor_sha256'] == TENSOR_SHA256 and
         results['source']['neutral_coefficients_checked'] == 64 and
         results['source']['source_associativity_checked'] is True, 'Source receipt claims')
    need(results['prerequisites']['check_count'] == 32 and
         results['prerequisites']['tensor_sha256'] == TENSOR_SHA256 and
         results['prerequisites']['forced_indicators_g_r_s'] == [-1, 1, 1], 'Prerequisite arithmetic receipt')
    need(results['weights']['nonempty_F_blocks'] == 136 and
         results['weights']['full_F_coefficient_slots'] == 1472 and
         results['weights']['independent_weight_pairs_checked'] == 104 and
         results['weights']['J_reflection_phase_checks'] == 5888 and
         results['weights']['categorical_normalization_certified'] is False and
         results['weights']['classification_decisions'] == 0, 'Full-weight replay scope')
    need(results['independent_weights']['nonempty_blocks'] == 136 and
         results['independent_weights']['F_coefficient_slots'] == 1472 and
         results['independent_weights']['reflection_phase_checks'] == 5888 and
         results['independent_weights']['independent_pair_checks'] == 104 and
         results['independent_weights']['categorical_claims_automatically_verified'] is False and
         results['independent_weights']['source_sha256'] == sha((stage / 'rank8/R24_TORUS_RIGIDITY_PROOF.md').read_bytes()),
         'Independent all-F replay scope and proof binding')
    if replay:
        # The copies isolate any checker output from the hash-bound evidence.
        with tempfile.TemporaryDirectory(prefix='grc-rigidity-checkers-') as temp:
            copied = Path(temp) / 'rank8'
            shutil.copytree(stage / 'rank8', copied)
            for item in inventory:
                command = [sys.executable] + ([] if __debug__ else ['-O']) + [str(copied / Path(item['checker']).name)]
                command += [str(repo) if a == '{repo}' else a for a in item['arguments']]
                result = subprocess.run(command, cwd=repo, env=dict(os.environ, SYMPY_GROUND_TYPES='python'),
                                        check=True, capture_output=True, text=True)
                need(json.loads(result.stdout) == results[item['name']],
                     'Finite checker replay differs from retained receipt: ' + item['name'])
    return {'replayed': bool(replay), 'checkers': len(inventory), 'python_optimization': int(not __debug__),
            'scope': 'Source, arithmetic, and finite F-slot consistency only; no categorical proof is machine-certified.'}


def verify_current(repo, replay=True, historical_rank7=None):
    repo = Path(repo).resolve()
    sources = verify_sources(repo)
    stage = repo / STAGE
    meta = read(stage / 'rigidity.json')
    need(meta['schema'] == 'categorification-rigidity-stage/v1' and
         meta['parent_stage'] == 'review_20261017' and meta['decision_ids'] == [SOURCE_ID] and
         meta['ledger'] == LEDGERS['8'], 'Exact rigidity-stage identity')
    proof_hash = _proof_presentation(repo)
    _source_tensor(repo)
    parent_raw = _parent_contents(repo)[LEDGERS['8']]
    current_raw = (repo / LEDGERS['8']).read_bytes()
    parent, current = json.loads(parent_raw), json.loads(current_raw)
    need(sha(parent_raw) == meta['previous_ledger_sha256'] and
         sha(current_raw) == meta['current_ledger_sha256'], 'Complete parent/current ledger byte identities')
    need(canonical(parent) == meta['previous_ledger_canonical_sha256'] and
         canonical(current) == meta['current_ledger_canonical_sha256'], 'Complete parent/current canonical identities')
    need(len(parent) == len(current) == len({x['id'] for x in current}) == 973 and
         [x['id'] for x in parent] == [x['id'] for x in current], 'All 973 ledger IDs and their order preserved')
    need([a['id'] for a, b in zip(parent, current) if a != b] == [SOURCE_ID],
         'Exactly one rank-eight record changed')
    need(canonical([x for x in current if x['id'] != SOURCE_ID]) == meta['unchanged_records_canonical_sha256'],
         'Every other rank-eight record preserved exactly')
    previous = next(x for x in parent if x['id'] == SOURCE_ID)
    changed = next(x for x in current if x['id'] == SOURCE_ID)
    need(previous == meta['previous_record'] and changed == meta['current_record'], 'Exact source-bound record transition')
    review = read(repo / 'evidence/review_20261017/review.json')
    need(previous == review['current_record'] and canonical(parent) == review['current_ledger_canonical_sha256'],
         'Frozen parent is the reviewed canonical ledger')
    need(changed['status'] == 'excluded' and changed['criterion'] == 'inner_square_torus_rigidity' and
         changed['tensor_sha256'] == TENSOR_SHA256 and 'review' not in changed, 'Current R24 theoretical exclusion')
    cert = changed['certificate']
    need(cert['scope'] == 'general_complex' and cert['kind'] == 'theoretical_no_go' and
         cert['proof'] == STAGE + '/rank8/R24_TORUS_RIGIDITY_PROOF.md' and
         cert['verifier'] == 'tools/verify_rigidity_20261017.py', 'Current theoretical certificate scope')
    accepted = read(stage / 'decisions.json')
    old = read(repo / 'evidence/review_20261017/decisions.json')
    new = read(stage / 'new_decisions.json')
    need(len(old) == 35 and len(new) == 1 and new[0]['id'] == SOURCE_ID and
         accepted == old + new and len({x['id'] for x in accepted}) == 36,
         'All 35 accepted parent decisions retained plus exactly R24')
    need(collections.Counter(x['status'] for x in accepted) == {'excluded': 29, 'unitarily_realized': 7},
         '36-case accepted continuation partition')
    need(new[0]['scope'] == 'general_complex' and new[0]['criterion'] == changed['criterion'] and
         new[0]['proof_source'] == STAGE and new[0]['proof'] == 'rank8/R24_TORUS_RIGIDITY_PROOF.md',
         'New decision proof source binding')
    for item in accepted:
        base = item.get('proof_source', 'evidence/unified_20261016')
        need(safe_relative(base) and safe_relative(item['proof']) and (repo / base / item['proof']).is_file(),
             'Accepted decision proof resolves: ' + item['id'])
    remaining = read(stage / 'remaining_ids.json')
    expected = read(stage / 'expected_totals.json')
    need(remaining == REMAINING, 'Exactly two remaining rank-six cases')
    for rank, name in LEDGERS.items():
        rows = historical_rank7 if rank == '7' and historical_rank7 is not None else read(repo / name)
        if rank == '7' and any(row['multiplicity'] > 4 for row in rows):
            from rank7_publication import historical_rank7_bytes
            rows = json.loads(historical_rank7_bytes(repo))
        totals = collections.Counter(x['status'] for x in rows)
        totals.setdefault('unresolved', 0)
        need(dict(totals) == expected[rank], 'Complete current rank partition: ' + rank)
        need([x['id'] for x in rows if x['status'] == 'unresolved'] == remaining[rank],
             'Complete current unresolved inventory: ' + rank)
        lookup = {x['id']: x for x in rows}
        need(all(lookup[x['id']]['status'] == x['status'] for x in accepted if str(x['rank']) == rank),
             'Accepted decisions match complete ledger: ' + rank)
    need(expected['8'] == {'unitarily_realized': 77, 'excluded': 896, 'unresolved': 0},
         'Rank-eight completed bounded classification counts')
    cases = read(stage / 'all_cases.json')
    old_cases = read(repo / 'evidence/review_20261017/all_cases.json')
    need(len(cases) == 38 and [x['id'] for x in cases] == [x['id'] for x in old_cases], 'Exact 38-case inventory')
    need([a['id'] for a, b in zip(cases, old_cases) if a != b] == [SOURCE_ID], 'All-case inventory changes only R24')
    need({x['id'] for x in cases if x['status'] == 'unresolved'} == set(sum(remaining.values(), [])),
         '38-case remaining inventory')
    need({x['id']: x['status'] for x in cases if x['status'] != 'unresolved'} ==
         {x['id']: x['status'] for x in accepted}, '38-case accepted status partition')
    combined = []
    for name in ('upper_residual_20261002b', 'upper_residual_20261002c', 'theoretical_20261016'):
        combined += read(repo / 'evidence' / name / 'decisions.json')
    combined += accepted
    need(len(combined) == len({x['id'] for x in combined}) == 140 and
         collections.Counter(x['status'] for x in combined) == {'excluded': 120, 'unitarily_realized': 20},
         'Combined residual program has 140 = 120 + 20 decisions')
    receipts = _receipts(repo, replay)
    return {'status': 'PASS', 'stage': STAGE, 'scope': meta['scope'],
            'categorical_proof_machine_verified': False, 'proof_sha256': proof_hash,
            'new_general_exclusions': 1, 'new_unitary_models': 0, 'changed_records': 1,
            'accepted_decisions': 36, 'accepted_exclusions': 29, 'accepted_models': 7,
            'combined_decisions': 140, 'combined_exclusions': 120, 'combined_models': 20,
            'remaining_ids': remaining, 'status_totals': expected,
            'sources': sources, 'finite_checker_replay': receipts}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=ROOT)
    parser.add_argument('--metadata-only', action='store_true', help='Check source and ledger identities without subprocess replays')
    args = parser.parse_args()
    print(json.dumps(verify_current(args.repo, replay=not args.metadata_only), indent=2))


if __name__ == '__main__':
    main()
