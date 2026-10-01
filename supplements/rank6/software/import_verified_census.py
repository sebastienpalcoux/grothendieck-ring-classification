"""Verify and import a supplied rank-six census, retaining all existing IDs.

Usage: python software/import_verified_census.py --source /path/to/rank6_M9_verified
       python software/import_verified_census.py --verify-only

Independent checks use exact signed 64-bit arithmetic, safe for rank six and
coefficients at most nine (an associativity sum is at most 6*9**2).
All 120 unit-fixing basis permutations are examined. Completeness of the
enumeration remains a claim of the supplied run; it is not re-enumerated here.
"""
import argparse
import collections
import csv
import gzip
import hashlib
import itertools
import json
from pathlib import Path
import shutil
import time

import numpy as np

from prepare import read_tables, flatten, dual

P = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def verified_manifest(source):
    """Validate every supplied checksum without trusting paths in the manifest."""
    source = source.resolve()
    checked = []
    for line in (source/'SHA256SUMS').read_text().splitlines():
        expected, name = line.split(maxsplit=1)
        name = name.lstrip('*')
        path = (source/name).resolve()
        require(path.is_relative_to(source), 'manifest path escapes source directory')
        require(path.is_file() and digest(path) == expected,
                'supplied checksum mismatch: '+name)
        checked.append(name)
    require(len(checked) == len(set(checked)), 'duplicate checksum path')
    for name in ['run.json', 'laptop_provenance.json',
                 'FusionRingMultiplicationTables.txt.gz',
                 'independent_check/summary.json', 'counts.csv']:
        require(name in checked, 'missing required checksum: '+name)
    return checked


def canonical_and_axioms(tables):
    """Return canonical tensor bytes and canonical-to-input permutations."""
    for R in tables:
        require(len(R) == 6 and all(len(M) == 6 and all(len(row) == 6
                for row in M) for M in R), 'invalid rank-six tensor shape')
        require(all(type(v) is int and 0 <= v <= 9 for v in flatten(R)),
                'coefficient outside supported exact range 0..9')
    a = np.asarray(tables, dtype=np.int64)
    require(np.all(a[:, 0] == np.eye(6, dtype=np.int64)), 'left unit')
    require(np.all(a[:, :, 0] == np.eye(6, dtype=np.int64)), 'right unit')
    unit = a[:, :, :, 0]
    require(np.all((unit == 0) | (unit == 1)) and np.all(unit.sum(axis=2) == 1),
            'unique dual basis with unit coefficient one')
    d = unit.argmax(axis=2)
    require(np.all(np.take_along_axis(d, d, axis=1) == np.arange(6)),
            'duality involution')
    for b in range(0, len(a), 256):
        block = a[b:b+256]
        ds = d[b:b+256]
        for i, j, k in itertools.product(range(6), repeat=3):
            require(np.all(block[:, i, j, k] == block[np.arange(len(block)),
                    ds[:, j], ds[:, i], ds[:, k]]), 'duality anti-involution')
            require(np.all(block[:, i, j, k] == block[np.arange(len(block)),
                    ds[:, i], k, j]), 'Frobenius reciprocity')
            require(np.all(block[:, i, j, k] == block[np.arange(len(block)),
                    k, ds[:, j], i]), 'right Frobenius reciprocity')
        left = np.einsum('bijm,bmkl->bijkl', block, block)
        right = np.einsum('bjkm,biml->bijkl', block, block)
        require(np.array_equal(left, right), 'associativity')
    raw = a.reshape((-1, 216)).astype(np.uint8)
    best = raw.copy()
    perms = np.tile(np.arange(6, dtype=np.uint8), (len(a), 1))
    rows = np.arange(len(a))
    positions = np.arange(216).reshape((6, 6, 6))
    for tail in itertools.permutations(range(1, 6)):
        perm = (0,)+tail
        indices = positions[np.ix_(perm, perm, perm)].reshape(216)
        candidate = raw[:, indices]
        first = np.argmax(candidate != best, axis=1)
        smaller = candidate[rows, first] < best[rows, first]
        best[smaller] = candidate[smaller]
        perms[smaller] = perm
    return [row.tobytes() for row in best], perms.tolist()


def table_digest(R):
    return hashlib.sha256(json.dumps(R, separators=(',', ':')).encode()).hexdigest()


def verify_archive(source):
    start = time.monotonic()
    checksums = verified_manifest(source)
    run = json.loads((source/'run.json').read_text())
    require(run['rank'] == 6 and run['bound'] == 9 and run['complete']
            and run['verified'], 'source does not claim verified complete bound nine')
    source_file = source/'FusionRingMultiplicationTables.txt.gz'
    require(hashlib.sha256(gzip.decompress(source_file.read_bytes())).hexdigest()
            == run['FusionRingMultiplicationTables.txt_sha256'],
            'uncompressed source checksum mismatch')
    raw = list(read_tables(source_file))
    counts = dict(sorted(collections.Counter(max(flatten(R)) for R in raw).items()))
    require(len(raw) == run['classes'] and counts ==
            {int(k): v for k, v in run['counts'].items()}, 'run counts mismatch')
    with (source/'counts.csv').open(newline='') as stream:
        csv_counts = {int(r['multiplicity']): int(r['classes'])
                      for r in csv.DictReader(stream) if int(r['rank']) == 6}
    require(counts == csv_counts, 'CSV counts mismatch')
    keys, permutations = canonical_and_axioms(raw)
    require(len(keys) == len(set(keys)), 'based-isomorphic source duplicates')
    evidence = json.loads((source/'independent_check/summary.json').read_text())
    require(evidence['input_records'] == len(raw) == evidence['distinct_rings']
            and evidence['duplicates'] == 0 and evidence['associativity_checked'],
            'supplied independent-check report mismatch')
    report = {
        'passed': True, 'rank': 6, 'bound': 9, 'tensors': len(raw), 'counts': counts,
        'checksum_files_verified': len(checksums), 'source_sha256': digest(source_file),
        'source_uncompressed_sha256': run['FusionRingMultiplicationTables.txt_sha256'],
        'independently_checked': ['integer_nonnegative_coefficients', 'left_and_right_unit',
            'unique_duality', 'duality_involution', 'duality_anti_involution',
            'left_and_right_Frobenius_reciprocity', 'associativity',
            'based_isomorphism_uniqueness'],
        'canonical_mode': 'all 120 unit-fixing permutations',
        'permutations_examined': len(raw)*120, 'duplicates': 0,
        'arithmetic': 'int64; each associativity sum is bounded by 486',
        'enumeration_repeated': False,
        'completeness_authority': 'supplied complete enumeration run and its provenance',
        'seconds': time.monotonic()-start,
    }
    return raw, keys, permutations, report


def import_archive(source):
    source = source.resolve()
    raw, keys, source_perms, report = verify_archive(source)
    census_path = P/'data/census.json'
    old_bytes = census_path.read_bytes()
    old = json.loads(old_bytes)
    require(len({r['id'] for r in old}) == len(old), 'duplicate existing identifier')
    old_keys, old_perms = canonical_and_axioms([r['N'] for r in old])
    require(len(old_keys) == len(set(old_keys)), 'duplicate existing based ring')
    source_by_key = {k: i for i, k in enumerate(keys)}
    require(all(k in source_by_key for k in old_keys), 'existing based ring absent')
    prior_max = max(r['m'] for r in old)
    require(prior_max in (8, 9), 'unexpected existing census bound')
    for r in old:
        require(r['m'] == max(flatten(r['N'])) and
                r['id'] == f"R6_{r['m']}_{r['index']}", 'invalid existing ID/multiplicity')
    old_by_key = {k: (r, p) for k, r, p in zip(old_keys, old, old_perms)}
    missing = [i for i, k in enumerate(keys) if k not in old_by_key]
    require(all(max(flatten(raw[i])) == 9 for i in missing),
            'old census does not cover every lower stratum')
    counter = collections.Counter(r['m'] for r in old)
    new = list(old)
    for i in sorted(missing, key=lambda i: flatten(raw[i])):
        R = raw[i]
        counter[9] += 1
        row = {'id': f'R6_9_{counter[9]}', 'm': 9, 'index': counter[9],
               'source_label': None, 'dual': dual(R),
               'commutative': all(R[a][b] == R[b][a] for a in range(6) for b in range(6)), 'N': R}
        new.append(row)
        old_by_key[keys[i]] = (row, source_perms[i])
    new.sort(key=lambda r: (r['m'], r['index']))
    require(len(new) == len(raw), 'import row count mismatch')
    provenance = P/'provenance/rank6_M9_verified'
    if source != provenance.resolve():
        shutil.copytree(source, provenance, dirs_exist_ok=True)
    verification = P/'verification/m9'
    verification.mkdir(parents=True, exist_ok=True)
    transport_path = provenance/'classification_transport.csv'
    exact = 0
    with transport_path.open('w', newline='') as stream:
        writer = csv.writer(stream)
        writer.writerow(['source_line', 'id', 'multiplicity',
            'permutation_classification_to_source', 'source_tensor_sha256',
            'classification_tensor_sha256'])
        for i, (R, key, sp) in enumerate(zip(raw, keys, source_perms), 1):
            row, cp = old_by_key[key]
            perm = [0]*6
            for s_index, c_index in zip(sp, cp):
                perm[c_index] = s_index
            require(tuple(R[a][b][c] for a in perm for b in perm for c in perm)
                    == flatten(row['N']), 'invalid computed basis transport')
            exact += R == row['N']
            writer.writerow([i, row['id'], row['m'], ';'.join(map(str, perm)),
                             table_digest(R), table_digest(row['N'])])
    old_meta_path = P/'provenance/repository_source.json'
    old_meta = json.loads(old_meta_path.read_text())
    if old_meta.get('bound') == 8:
        (provenance/'previous_repository_source.json').write_text(
            json.dumps(old_meta, indent=2)+'\n')
    source_file = source/'FusionRingMultiplicationTables.txt.gz'
    shutil.copy2(source_file, P/'data/rank6_tables.txt.gz')
    census_path.write_text(json.dumps(new, separators=(',', ':'))+'\n')
    laptop = json.loads((source/'laptop_provenance.json').read_text())
    meta = {
        'repository': laptop['source']['repository'],
        'source_commit': laptop['source']['commit'],
        'source_commit_scope': 'enumeration code and systems; tensor data supplied separately',
        'source_kind': 'user-supplied verified laptop census',
        'path': 'provenance/rank6_M9_verified/FusionRingMultiplicationTables.txt.gz',
        'sha256': report['source_sha256'],
        'uncompressed_sha256': report['source_uncompressed_sha256'],
        'tensors': len(raw), 'bound': 9, 'counts': report['counts'],
        'source_complete': True, 'source_verified': True,
        'classification_import': 'Existing IDs and tensors retained exactly; new multiplicity-nine representatives sorted by full tensor. Explicit basis transports cover every source row.',
        'classification_transport': str(transport_path.relative_to(P)),
        'classification_transport_sha256': digest(transport_path),
        'census_authority': 'Completeness is supplied by the verified enumeration. This package independently rechecks all ring axioms and all unit-fixing canonical forms, but does not re-enumerate.',
        'independent_verification': 'verification/m9/census_import.json',
    }
    old_meta_path.write_text(json.dumps(meta, indent=2)+'\n')
    lower_old = [r for r in old if r['m'] <= 8]
    lower_new = [r for r in new if r['m'] <= 8]
    require(lower_old == lower_new, 'lower census changed')
    report.update({
        'existing_rows_preserved': len(old), 'lower_rows_preserved': len(lower_old),
        'new_rows': len(missing), 'exact_representative_matches': exact,
        'basis_relabelled_matches': len(raw)-exact,
        'new_id_range': ['R6_9_1', f"R6_9_{counter[9]}"],
        'previous_census_sha256': hashlib.sha256(old_bytes).hexdigest(),
        'census_sha256': digest(census_path),
        'classification_transport_sha256': digest(transport_path),
        'verifier_source_sha256': digest(Path(__file__)),
    })
    (verification/'census_import.json').write_text(json.dumps(report, indent=2)+'\n')
    from import_repository import verify_source
    report['coverage_check'] = verify_source(new)
    (verification/'census_import.json').write_text(json.dumps(report, indent=2)+'\n')
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path)
    parser.add_argument('--verify-only', action='store_true')
    args = parser.parse_args()
    if args.verify_only:
        _, _, _, result = verify_archive(args.source or P/'provenance/rank6_M9_verified')
        from import_repository import verify_source
        result['coverage_check'] = verify_source()
    else:
        require(args.source is not None, '--source is required for import')
        result = import_archive(args.source)
    print(json.dumps(result, indent=2))
