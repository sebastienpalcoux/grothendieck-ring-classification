"""Small adversarial controls for the bound-nine census import.

Run with ``python -B software/census_import_controls.py``. All corruptions are
in-memory or in disposable temporary fixtures; the real census is read only.
These controls exercise the importer, not the completeness of enumeration.
"""
import collections
import copy
import csv
import gzip
import itertools
import json
from pathlib import Path
import sys
import tempfile
import time

sys.dont_write_bytecode = True

import import_repository
import import_verified_census as importer
from prepare import dual, flatten, read_tables
from rings import canonical, permute

P = Path(__file__).resolve().parents[1]
FIELDS = ['source_line', 'id', 'multiplicity',
          'permutation_classification_to_source', 'source_tensor_sha256',
          'classification_tensor_sha256']


def require(condition, message):
    if not condition:
        raise ValueError(message)


def rejected(call, expected):
    """Only the intended ValueError is evidence for a negative control."""
    try:
        call()
    except ValueError as exc:
        require(str(exc) == expected,
                'wrong rejection: expected %r, got %r' % (expected, str(exc)))
        return {'rejected': True, 'reason': str(exc)}
    raise ValueError('negative control was accepted: '+expected)


def source_sample(source):
    """First/last from every exact stratum, plus explicit structural cases."""
    first, last, features = {}, {}, {}
    count = 0
    for count, R in enumerate(read_tables(source), 1):
        m = max(flatten(R))
        item = (count, R)
        first.setdefault(m, item)
        last[m] = item
        commutative = all(R[i][j] == R[j][i]
                          for i in range(6) for j in range(6))
        self_dual = dual(R) == list(range(6))
        if not commutative:
            features.setdefault('noncommutative', item)
        if self_dual:
            features.setdefault('self_dual', item)
        else:
            features.setdefault('non_self_dual', item)
    require(set(first) == set(range(1, 10)), 'missing source multiplicity stratum')
    require(len(features) == 3, 'missing required structural source sample')
    sample = dict(list(first.values()) + list(last.values()) + list(features.values()))
    return sorted(sample.items()), features, count


def canonical_controls(sample):
    permutations = [(0, 1, 2, 3, 4, 5), (0, 2, 1, 3, 4, 5),
                    (0, 5, 4, 3, 2, 1), (0, 2, 3, 4, 5, 1)]
    tensors, references = [], []
    changed = 0
    for line, R in sample:
        reference = canonical(R)
        for p in permutations:
            T = permute(R, p)
            require(canonical(T) == reference, 'reference canonical relabel mismatch')
            changed += T != R
            tensors.append(T)
            references.append(bytes(reference))
    keys, transports = importer.canonical_and_axioms(tensors)
    require(keys == references, 'NumPy and pure-Python canonical forms differ')
    for R, key, p in zip(tensors, keys, transports):
        require(p[0] == 0 and sorted(p) == list(range(6)),
                'returned canonical transport is not unit-fixing')
        require(bytes(flatten(permute(R, p))) == key,
                'returned canonical transport does not produce canonical tensor')
    # The axiom checker processes 256 tensors at a time. Exercise both sides
    # of that boundary with already independently checked references.
    batch = [tensors[i % len(tensors)] for i in range(257)]
    batch_keys, _ = importer.canonical_and_axioms(batch)
    require(batch_keys == [references[i % len(references)] for i in range(257)],
            'canonical form changed across batch boundary')
    return {'source_sample_size': len(sample), 'source_lines': [i for i, _ in sample],
            'multiplicities': sorted({max(flatten(R)) for _, R in sample}),
            'noncommutative_samples': sum(any(R[i][j] != R[j][i]
                for i in range(6) for j in range(6)) for _, R in sample),
            'self_dual_samples': sum(dual(R) == list(range(6)) for _, R in sample),
            'reference': 'rings.canonical: all 120 unit-fixing permutations',
            'reference_comparisons': len(tensors), 'changed_representatives': changed,
            'returned_transports_checked': len(transports),
            'batch_boundary_tensors': len(batch), 'passed': True}


def axiom_controls(self_dual):
    tests = {}
    for label, value in [('negative_coefficient', -1), ('coefficient_above_nine', 10),
                         ('float_coefficient', 1.0), ('boolean_coefficient', True)]:
        bad = copy.deepcopy(self_dual)
        bad[1][1][1] = value
        tests[label] = rejected(lambda: importer.canonical_and_axioms([bad]),
                               'coefficient outside supported exact range 0..9')
    for label, mutate in [('wrong_rank', lambda R: R.pop()),
                          ('ragged_matrix', lambda R: R[1].pop()),
                          ('ragged_row', lambda R: R[1][1].pop())]:
        bad = copy.deepcopy(self_dual)
        mutate(bad)
        tests[label] = rejected(lambda: importer.canonical_and_axioms([bad]),
                               'invalid rank-six tensor shape')
    bad = copy.deepcopy(self_dual)
    bad[0][1][1] = 0
    tests['left_unit'] = rejected(lambda: importer.canonical_and_axioms([bad]), 'left unit')
    bad = copy.deepcopy(self_dual)
    bad[1][0][1] = 0
    tests['right_unit'] = rejected(lambda: importer.canonical_and_axioms([bad]), 'right unit')
    # With identity duality, this symmetric nonunit perturbation preserves
    # both units, duality and both Frobenius identities. The exact rejection
    # proves that the associativity test itself is reached.
    bad = copy.deepcopy(self_dual)
    for i, j, k in set(itertools.permutations((1, 1, 1))):
        bad[i][j][k] += 1
    tests['associativity_after_other_axioms'] = rejected(
        lambda: importer.canonical_and_axioms([bad]), 'associativity')
    return tests


def transport_controls(raw):
    """Every semantic transport mutation gets a fresh, matching CSV hash."""
    tests = {}
    with tempfile.TemporaryDirectory(prefix='census-import-controls-') as temporary:
        root = Path(temporary)
        (root/'data').mkdir()
        (root/'provenance').mkdir()
        source = root/'data/rank6_tables.txt.gz'
        source.write_bytes(gzip.compress(('\n'.join(json.dumps(R) for R in raw)+'\n').encode(), mtime=0))
        transport = root/'provenance/transport.csv'
        meta_path = root/'provenance/repository_source.json'
        meta = {'sha256': importer.digest(source), 'tensors': len(raw),
                'counts': dict(collections.Counter(max(flatten(R)) for R in raw)),
                'source_commit': 'isolated-adversarial-fixture',
                'classification_transport': 'provenance/transport.csv'}
        rows, records = [], []
        indices = collections.Counter()
        for line, R in enumerate(raw, 1):
            m = max(flatten(R))
            indices[m] += 1
            rid = f'R6_{m}_{indices[m]}'
            rows.append({'id': rid, 'm': m, 'index': indices[m], 'N': copy.deepcopy(R)})
            records.append({'source_line': line, 'id': rid, 'multiplicity': m,
                'permutation_classification_to_source': '0;1;2;3;4;5',
                'source_tensor_sha256': importer.table_digest(R),
                'classification_tensor_sha256': importer.table_digest(R)})

        def write_fixture(chosen_records, chosen_meta=None):
            with transport.open('w', newline='') as stream:
                writer = csv.DictWriter(stream, fieldnames=FIELDS)
                writer.writeheader()
                writer.writerows(chosen_records)
            current = copy.deepcopy(meta if chosen_meta is None else chosen_meta)
            current['classification_transport_sha256'] = importer.digest(transport)
            meta_path.write_text(json.dumps(current))

        saved_root = import_repository.P
        import_repository.P = root
        try:
            write_fixture(records)
            result = import_repository.verify_source(rows)
            require(result['tensors'] == len(raw), 'identity fixture coverage mismatch')
            tests['valid_identity_transport'] = {'accepted': True, 'tensors': len(raw)}
            p = next((0,)+tail for tail in itertools.permutations(range(1, 6))
                     if permute(raw[1], (0,)+tail) != raw[1])
            relabelled = copy.deepcopy(rows)
            relabelled[1]['N'] = permute(raw[1], p)
            relabel_records = copy.deepcopy(records)
            relabel_records[1]['permutation_classification_to_source'] = ';'.join(map(str, p))
            relabel_records[1]['classification_tensor_sha256'] = importer.table_digest(relabelled[1]['N'])
            write_fixture(relabel_records)
            require(import_repository.verify_source(relabelled)['tensors'] == len(raw),
                    'relabelled fixture coverage mismatch')
            tests['valid_nontrivial_relabelling'] = {'accepted': True, 'permutation': list(p)}
            for label, bad_p in [('duplicate_basis_index', '0;1;1;3;4;5'),
                                 ('non_unit_fixing_permutation', '1;0;2;3;4;5')]:
                bad = copy.deepcopy(relabel_records)
                bad[1]['permutation_classification_to_source'] = bad_p
                write_fixture(bad)
                tests[label] = rejected(lambda: import_repository.verify_source(relabelled),
                                       'invalid unit-fixing basis transport')
            bad = copy.deepcopy(relabel_records)
            bad[1]['permutation_classification_to_source'] = '0;1;2;3;4;5'
            write_fixture(bad)
            tests['wrong_valid_permutation'] = rejected(lambda: import_repository.verify_source(relabelled),
                         'classification tensor does not match source basis transport')
            bad_meta = copy.deepcopy(meta)
            bad_meta['sha256'] = '0'*64
            write_fixture(relabel_records, bad_meta)
            tests['source_archive_digest'] = rejected(lambda: import_repository.verify_source(relabelled),
                                                     'trusted source archive checksum mismatch')
            write_fixture(relabel_records)
            with transport.open('a') as stream:
                stream.write('\n')
            tests['transport_archive_digest'] = rejected(lambda: import_repository.verify_source(relabelled),
                                                         'source transport checksum/path mismatch')
            write_fixture(relabel_records)
            bad_rows = copy.deepcopy(relabelled)
            bad_rows[1]['N'][1][1][1] += 1
            tests['classification_tensor'] = rejected(lambda: import_repository.verify_source(bad_rows),
                         'classification tensor does not match source basis transport')
            bad_rows = copy.deepcopy(relabelled)
            bad_rows[1]['id'] = bad_rows[0]['id']
            tests['duplicate_classification_id'] = rejected(lambda: import_repository.verify_source(bad_rows),
                                                            'repeated classification identifier')
            bad = copy.deepcopy(relabel_records)
            bad[1]['id'] = bad[0]['id']
            write_fixture(bad)
            tests['duplicate_transport_id'] = rejected(lambda: import_repository.verify_source(relabelled),
                                                      'classification source transport coverage mismatch')
            write_fixture(relabel_records[:-1])
            tests['missing_transport_row'] = rejected(lambda: import_repository.verify_source(relabelled),
                                                     'classification source transport coverage mismatch')
        finally:
            import_repository.P = saved_root
    return tests


def main():
    start = time.monotonic()
    source = P/'data/rank6_tables.txt.gz'
    import_report_path = P/'verification/m9/census_import.json'
    import_report = json.loads(import_report_path.read_text())
    source_sha256 = importer.digest(source)
    require(import_report['passed'] and import_report['source_sha256'] == source_sha256,
            'import report is not bound to current source archive')
    require(import_report['verifier_source_sha256'] == importer.digest(Path(importer.__file__)),
            'import report is not bound to current import verifier source')
    require(import_report['census_sha256'] == importer.digest(P/'data/census.json'),
            'import report is not bound to current census')
    sample, features, source_count = source_sample(source)
    require(source_count == import_report['tensors'], 'source count disagrees with import report')
    canonical_report = canonical_controls(sample)
    axioms = axiom_controls(features['self_dual'][1])
    transports = transport_controls([features['self_dual'][1], features['noncommutative'][1]])
    report = {'passed': True, 'source_sha256': source_sha256,
        'source_tensors': source_count, 'census_sha256': import_report['census_sha256'],
        'import_report_sha256': importer.digest(import_report_path),
        'import_verifier_source_sha256': importer.digest(Path(importer.__file__)),
        'coverage_verifier_source_sha256': importer.digest(Path(import_repository.__file__)),
        'reference_canonical_source_sha256': importer.digest(P/'software/rings.py'),
        'controls_source_sha256': importer.digest(Path(__file__)),
        'canonicalization': canonical_report, 'axiom_mutations': axioms,
        'transport_fixtures': transports,
        'rejected_mutations': len(axioms)+sum(bool(t.get('rejected')) for t in transports.values()),
        'scope': 'Importer regression controls; enumeration completeness is not re-proved.',
        'seconds': time.monotonic()-start}
    out = P/'verification/m9/census_import_controls.json'
    out.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
