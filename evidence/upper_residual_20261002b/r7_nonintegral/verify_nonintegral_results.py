"""Strict replay of four general and four explicitly pivotal-only exclusions."""
import argparse
import collections
import copy
import hashlib
import json
import sys
import time
from pathlib import Path
from case_source import ROOT, SOFTWARE, engine_source_path, fingerprint, read_cases, require

sys.path.insert(0, str(SOFTWARE))
from exact import VerificationError, check_norm, pc
from rings import Characters, validate
import oriented_extension
from verify_d12 import verify as verify_d12

HERE = Path(__file__).resolve().parent
GENERAL = {'R7_3_1036': 8, 'R7_3_1044': 24,
           'R7_4_2510': 4, 'R7_4_2706': 48}
PIVOTAL = ('R7_4_1212', 'R7_4_1213', 'R7_4_1417', 'R7_4_1420')

def check_engine_sources():
    hashes = json.loads((HERE / 'signed_engine_sources.json').read_text())
    require(bool(hashes), 'engine source bindings missing')
    for relative_path, expected_hash in hashes.items():
        path = engine_source_path(relative_path)
        require(path.resolve().is_relative_to(ROOT), 'source binding escapes repository')
        require(hashlib.sha256(path.read_bytes()).hexdigest() == expected_hash,
                f'signed engine source changed: {relative_path}')

def check_general(case, record):
    require(record['id'] == case['id'] and record['scope'] == 'general_complex', 'incorrect general scope')
    require(record['source_line'] == case['source_line'], 'source line changed')
    require(record['tensor_sha256'] == case['tensor_sha256'], 'source tensor changed')
    require(record['signed_table_count'] == GENERAL[case['id']], 'claimed branch count changed')
    require(record['certificate']['kind'] == 'oriented_signed', 'wrong proof tree')
    for branch in record['certificate']['branches']:
        require('characters' in branch and 'obstruction' not in branch,
                'proof must explicitly cover signed dimension characters')
        require(all(component['obstruction']['kind'] in ('zero', 'duality', 'norm')
                    for component in branch['characters']), 'unapproved necessary criterion')
    validate(case['tensor'])
    # Rebuild all oriented domains and all associativity equations. The
    # inherited strict verifier compares the complete enumeration to the
    # certificate and recomputes every character, duality and norm witness.
    oriented_extension.verify(case['tensor'], record['certificate'])
    require(len(record['certificate']['branches']) == GENERAL[case['id']], 'incomplete signed coverage')

def check_pivotal(case, record):
    require(record['id'] == case['id'] and record['scope'] == 'pivotal_only'
            and record['general_status'] == 'unresolved', 'scope-only evidence promoted to general')
    require(record['source_line'] == case['source_line']
            and record['tensor_sha256'] == case['tensor_sha256'], 'pivotal source binding changed')
    validate(case['tensor'])
    algebra = Characters(case['tensor'], record['generator'])
    require(len(algebra.components) == len(record['characters']), 'pivotal character branch omitted')
    for (factor, multiplicity), component in zip(algebra.components, record['characters']):
        require(pc(factor) == component['factor'], 'pivotal character factor changed')
        field, dimensions, delta, delta_poly = algebra.component(factor)
        obstruction = component['obstruction']
        if obstruction['kind'] == 'zero':
            require(not dimensions[obstruction['object']], 'pivotal dimension is nonzero')
        elif obstruction['kind'] == 'norm':
            check_norm(delta_poly, algebra.cf, obstruction)
        else:
            raise RuntimeError('pivotal test must use zero or norm, without spherical duality')

def must_reject(label, operation):
    try:
        operation()
    except (RuntimeError, ValueError, KeyError, IndexError):
        return label
    raise RuntimeError(f'tampering control accepted: {label}')

def verify_all(controls=True):
    check_engine_sources()
    cases = read_cases(set(GENERAL) | set(PIVOTAL))
    results = []
    for case_id in GENERAL:
        start = time.monotonic()
        record = json.loads((HERE / f'{case_id}_general.json').read_text())
        check_general(cases[case_id], record)
        results.append({'id': case_id, 'status': 'PASS', 'scope': 'general_complex',
                        'signed_tables': GENERAL[case_id],
                        'seconds': round(time.monotonic() - start, 3)})
    pivotal = json.loads((HERE / 'pivotal_certificates.json').read_text())
    require([record['id'] for record in pivotal] == list(PIVOTAL), 'pivotal inventory changed')
    for record in pivotal:
        check_pivotal(cases[record['id']], record)
        results.append({'id': record['id'], 'status': 'PASS', 'scope': 'pivotal_only',
                        'general_status': 'unresolved'})
    d12 = verify_d12()
    d12.pop('model_tensor')
    controls_passed = []
    if controls:
        case_id = 'R7_3_1036'
        good = json.loads((HERE / f'{case_id}_general.json').read_text())
        bad = copy.deepcopy(good)
        bad['certificate']['branches'].pop()
        controls_passed.append(must_reject('missing_signed_branch', lambda: check_general(cases[case_id], bad)))
        bad = copy.deepcopy(good)
        witness = next(component['obstruction']
                       for branch in bad['certificate']['branches'] for component in branch['characters']
                       if component['obstruction']['kind'] == 'norm')
        witness['prime'] = 53
        controls_passed.append(must_reject('invalid_norm_witness', lambda: check_general(cases[case_id], bad)))
        bad = copy.deepcopy(pivotal[0])
        bad['scope'] = 'general_complex'
        controls_passed.append(must_reject('pivotal_scope_promotion', lambda: check_pivotal(cases[bad['id']], bad)))
        bad = copy.deepcopy(pivotal[0])
        bad['characters'].pop()
        controls_passed.append(must_reject('missing_pivotal_character', lambda: check_pivotal(cases[bad['id']], bad)))
    return {'status': 'PASS', 'python_optimized': not __debug__,
            'general_exclusions': results[:4], 'pivotal_only_exclusions': results[4:],
            'unitary_modular_model': d12, 'tampering_controls': controls_passed}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repository', type=Path, help='Optional explicit repository root; must match source root.')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if args.repository:
        require(args.repository.resolve() == ROOT, 'repository root mismatch')
    result = verify_all()
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, sort_keys=True))

if __name__ == '__main__':
    main()
