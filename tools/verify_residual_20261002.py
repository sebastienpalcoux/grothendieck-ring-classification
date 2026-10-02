"""Replay the residual update and reconstruct the exact historical ledger stage.

The manifest retains only the replaced original records. Restoring them
must recover both complete baseline canonical digests. This is also the bridge
used by the unchanged historical AnyonWiki preservation checks. No mathematical
exclusion is inferred from an unresolved status or an absent model.
"""
from pathlib import Path
import collections
import contextlib
import copy
import gzip
import hashlib
import importlib.util
import io
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / 'evidence/residual_20261002'
MANIFEST_SHA256 = '6629ae6d695fb42c7358bdb655e422590eff783c6040508c2b272702b251ab55'
LEDGER_PATHS = {
    7: 'supplements/rank7/output/rank7_ledger.json',
    8: 'supplements/rank8/data/decisions.json',
}
APPROVED_SOURCES = {
    7: ('supplements/rank7/data/residual_20261002_models.json',
        'supplements/rank7/data/residual_20261002_exclusions.json'),
    8: ('supplements/rank8/data/oct2_models.json',
        'supplements/rank8/data/oct2_exclusions.json'),
}


def approved_transitions(rank):
    """Read inventoried decisions only after their source hashes have been checked."""
    model_path, exclusion_path = APPROVED_SOURCES[rank]
    models, exclusions = load(ROOT / model_path), load(ROOT / exclusion_path)
    positives = [record['id'] for record in models]
    negatives = list(exclusions) if isinstance(exclusions, dict) else [record['id'] for record in exclusions]
    require(len(set(positives + negatives)) == len(positives) + len(negatives), 'approved source inventory')
    return dict([(rid, 'unitarily_realized') for rid in positives] + [(rid, 'excluded') for rid in negatives])


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load(path):
    return json.loads(path.read_text())


def canonical_digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def tensor_digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def file_digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_preservation(current_ledgers=None):
    """Check every ledger field and every replay source; return historical copies."""
    manifest_path = EVIDENCE / 'previous_records.json'
    require(file_digest(manifest_path) == MANIFEST_SHA256, 'preservation manifest hash')
    manifest = load(manifest_path)
    require(manifest['schema_version'] == 1 and set(manifest['ranks']) == {'7', '8'},
            'preservation manifest format')
    for relative_path, expected in manifest['source_files_sha256'].items():
        path = (ROOT / relative_path).resolve()
        require(ROOT in path.parents, 'source path outside repository')
        require(file_digest(path) == expected, 'replay source hash: ' + relative_path)
    if current_ledgers is None:
        current_ledgers = {rank: load(ROOT / path) for rank, path in LEDGER_PATHS.items()}
    require(set(current_ledgers) == {7, 8}, 'ledger rank inventory')
    restored = {}
    for rank, path in LEDGER_PATHS.items():
        meta = manifest['ranks'][str(rank)]
        require(meta['ledger_path'] == path, 'ledger path')
        ledger = current_ledgers[rank]
        by_id = {record['id']: record for record in ledger}
        require(len(by_id) == len(ledger) == meta['records'], 'ledger coverage')
        previous = meta['previous_records']
        originals = {record['id']: record for record in previous}
        approved = approved_transitions(rank)
        require(len(originals) == len(previous) == len(approved), 'original record coverage')
        require(set(originals) == set(meta['transitions']) == set(approved), 'approved transition inventory')
        require(set(approved) <= set(by_id), 'missing changed record')
        for rid, status in approved.items():
            old, new, transition = originals[rid], by_id[rid], meta['transitions'][rid]
            require(old['status'] == transition['from'] == 'unresolved', 'original status: ' + rid)
            require(new['status'] == transition['to'] == status, 'new status: ' + rid)
            require(canonical_digest(new) == transition['new_record_sha256'], 'changed record contents: ' + rid)
            stable_fields = (('id', 'rank', 'multiplicity', 'source_line', 'commutative', 'tensor')
                             if rank == 7 else ('id', 'multiplicity', 'index', 'tensor_sha256', 'commutative'))
            require(all(old[key] == new[key] for key in stable_fields), 'census identity changed: ' + rid)
        unaffected = [record for record in ledger if record['id'] not in approved]
        require(canonical_digest(unaffected) == meta['unchanged_records_sha256'], 'unaffected records changed')
        historical = [copy.deepcopy(originals.get(record['id'], record)) for record in ledger]
        require(canonical_digest(historical) == meta['baseline_canonical_sha256'], 'restored complete baseline digest')
        negatives = [record for record in historical if record['status'] == 'excluded']
        require(canonical_digest(negatives) == meta['previous_negative_records_sha256'], 'historical exclusions changed')
        require(all(by_id[record['id']] == record for record in negatives), 'prior exclusion altered')
        restored[rank] = historical
    return current_ledgers, restored, manifest


def replay_script(relative_path):
    command = [sys.executable] + (['-O'] if sys.flags.optimize else []) + [str(ROOT / relative_path)]
    # The supplement entrypoints also write their dated receipts. Preserve the
    # archived bytes: the normal and -O rank-seven receipts differ only in their
    # optimization flag. Verification below always uses the fresh subprocess
    # output, never the saved receipt.
    receipt_paths = {
        'supplements/rank7/software/verify_residual_20261002.py':
            'supplements/rank7/output/residual_20261002_verification.json',
        'supplements/rank8/software/verify_oct2.py':
            'supplements/rank8/verification/oct2_report.json',
    }
    receipt = ROOT / receipt_paths[relative_path]
    saved_receipt = receipt.read_bytes() if receipt.exists() else None
    try:
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    finally:
        if saved_receipt is not None:
            if not receipt.exists() or receipt.read_bytes() != saved_receipt:
                receipt.write_bytes(saved_receipt)
        elif receipt.exists():
            receipt.unlink()
    require(result.returncode == 0, relative_path + ' failed:\n' + result.stdout + result.stderr)
    report = json.loads(result.stdout)
    if relative_path.startswith('supplements/rank7/'):
        require(report.get('passed') is True, relative_path + ' did not pass')
        report = dict(report, status='PASS')
    else:
        require(report.get('status') == 'PASS', relative_path + ' did not pass')
    return report


def verify_update(current_ledgers=None):
    """Validate the full new stage, including finite mathematical replays.

    Returns (report, restored_ledgers). Historical callers must use this method,
    not restoration alone, so a historical pass also validates the later stage.
    """
    if (ROOT / "evidence/upper_residual_20261002c/source_files.json").exists():
        require(current_ledgers is None, "new-stage replay requires on-disk ledgers")
        spec = importlib.util.spec_from_file_location("upper_residual_c", ROOT / "tools/verify_upper_residual_20261002c.py")
        module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
        return module.verify_update()
    if (ROOT / "evidence/upper_residual_20261002b/source_files.json").exists():
        require(current_ledgers is None, "new-stage replay requires on-disk ledgers")
        spec = importlib.util.spec_from_file_location("upper_residual", ROOT / "tools/verify_upper_residual_20261002b.py")
        module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
        return module.verify_update()
    ledgers, restored, manifest = verify_preservation(current_ledgers)
    # Rank verifiers read the on-disk ledgers; an in-memory caller may not replace them.
    require(all(ledgers[rank] == load(ROOT / path) for rank, path in LEDGER_PATHS.items()),
            'semantic replay requires the on-disk current ledgers')
    rank_reports = {
        '7': replay_script('supplements/rank7/software/verify_residual_20261002.py'),
        '8': replay_script('supplements/rank8/software/verify_oct2.py'),
    }
    # Bind every portable obstruction to the actual census, before its exact replay.
    raw = gzip.open(ROOT / 'supplements/rank8/data/rank8_tables.txt.gz', 'rt')
    with raw:
        rank8_tensors = [json.loads(line.replace('{', '[').replace('}', ']'))
                         for line in raw if line.strip()]
    by_hash = {tensor_digest(tensor): tensor for tensor in rank8_tensors}
    require(len(by_hash) == len(rank8_tensors) == len(ledgers[8]), 'rank-eight tensor coverage')
    census = {record['id']: record['tensor'] for record in ledgers[7]}
    census.update({record['id']: by_hash[record['tensor_sha256']] for record in ledgers[8]})
    statuses = {record['id']: record['status'] for ledger in ledgers.values() for record in ledger}
    certificates = load(EVIDENCE / 'unitary/unitary_obstruction_certificates.json')
    for record in certificates:
        rid = record['id']
        require(rid in census and record['tensor'] == census[rid], 'portable census binding: ' + rid)
        require(statuses[rid] != 'unitarily_realized', 'obstruction conflicts with positive model: ' + rid)
    spec = importlib.util.spec_from_file_location('residual_unitary_exact', EVIDENCE / 'unitary/verify.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    with contextlib.redirect_stdout(io.StringIO()):
        unitary_report = module.main()
    require(unitary_report['status'] == 'PASS', 'portable obstruction replay')
    require({row['id'] for row in unitary_report['general_exclusions']} == {'R7_3_900', 'R7_3_991'},
            'portable general exclusion scope')
    transition_counts = collections.Counter(status for rank in LEDGER_PATHS
                                            for status in approved_transitions(rank).values())
    report = {
        'status': 'PASS',
        'previous_commit': manifest['previous_commit'],
        'changed_records': sum(transition_counts.values()),
        'new_unitary_models': transition_counts['unitarily_realized'],
        'new_general_exclusions': transition_counts['excluded'],
        'complete_historical_ledgers_restored': True,
        'unaffected_records_unchanged': True,
        'previous_negative_records_unchanged': True,
        'pinned_replay_source_files': len(manifest['source_files_sha256']),
        'portable_certificate_rings_bound_to_census': len(certificates),
        'portable_certificate_counts': unitary_report['certificate_counts'],
        'portable_braided_exclusions': len(unitary_report['braided_exclusions']),
        'portable_general_exclusions': [row['id'] for row in unitary_report['general_exclusions']],
        'status_totals': {str(rank): dict(collections.Counter(row['status'] for row in ledger))
                          for rank, ledger in ledgers.items()},
        'rank_replay_status': {rank: result['status'] for rank, result in rank_reports.items()},
        'scope': ('The source-inventoried cited unitary constructions and general exclusions are the only ledger transitions. '
                  'The other portable positivity/support obstructions have unitary scope; '
                  'the ten explicitly listed braided upgrades also exclude braided complex fusion categories.'),
    }
    return report, restored


def main():
    report, _ = verify_update()
    destination = ROOT / 'evidence/upper_residual_20261002c/verification_report.json' if (ROOT / 'evidence/upper_residual_20261002c/source_files.json').exists() else ROOT / 'evidence/upper_residual_20261002b/verification_report.json' if (ROOT / 'evidence/upper_residual_20261002b/source_files.json').exists() else EVIDENCE / 'verification_report.json'
    destination.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
    return report


if __name__ == '__main__':
    main()
