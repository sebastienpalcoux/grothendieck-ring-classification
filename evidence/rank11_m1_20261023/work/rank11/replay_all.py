#!/usr/bin/env python3
"""Replay accepted rank-eleven evidence, never discovery searches.

The package retains paths relative to the directory containing work/ and
repositories/. Run this file from any working directory. Both ordinary and
optimized Python are checked by default; the status/hash map must be unchanged.
"""
from pathlib import Path
import argparse, ast, hashlib, json, subprocess, sys, time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def need(value, message):
    if not value:
        raise ValueError(message)


def read_json(path):
    return json.loads(path.read_text())


def ledger_map():
    rows = read_json(HERE / 'ledger.json')['records']
    need(len(rows) == 182 and len({r['id'] for r in rows}) == 182,
         'ledger must have exactly 182 unique inputs')
    return {r['id']: {'status': r['status'],
                     'tensor_sha256_compact_json': r['tensor_sha256_compact_json'],
                     'tensor_sha256_uint8_flattened': r['tensor_sha256_uint8_flattened']}
            for r in rows}


def check_source():
    from common import read, sha, validate
    source = read()
    expected = ledger_map()
    profile = {r['id']: r for r in read_json(HERE / 'profile.json')['11']['rings']}
    need(set(source) == set(expected) == set(profile), 'source/profile/ledger domain')
    for rid, tensor in source.items():
        need(len(tensor) == 11, 'rank eleven')
        need(all(v in (0, 1) for row in tensor for col in row for v in col),
             'multiplicity one')
        validate(tensor)
        compact = sha(tensor)
        flat = hashlib.sha256(bytes(v for row in tensor for col in row for v in col)).hexdigest()
        need(expected[rid]['tensor_sha256_compact_json'] == compact ==
             profile[rid]['tensor_sha256_compact_json'], 'compact tensor identity')
        need(expected[rid]['tensor_sha256_uint8_flattened'] == flat ==
             profile[rid]['tensor_sha256_uint8_flattened'], 'flat tensor identity')
    for record in read_json(HERE / 'additional_accepted.json'):
        rid = record['id']
        need(rid in source and record['tensor_sha256'] == sha(source[rid]),
             'additional accepted evidence must bind the original tensor hash')
        need(record['status'] == expected[rid]['status'], 'additional accepted status')
    print('PASS: all 182 source axioms, multiplicity bounds and profile/ledger hashes')


def stages():
    prefix = 'work/rank11/'
    rows = [
        ('source', [prefix + 'replay_all.py', '--check-source']),
        ('arithmetic', [prefix + 'arithmetic/run.py', '--verify-only']),
        ('subring-indices', [prefix + 'arithmetic/subring_indices.py', '--verify-only']),
        ('cyclotomic', [prefix + 'arithmetic/cyclotomic_complete.py', '--verify-only']),
        ('noncomm-codegrees', [prefix + 'arithmetic/noncomm_codegrees.py', '--verify-only']),
        ('cyclic', [prefix + 'criteria_audit/verify_cyclic_independent.py']),
        ('compression', [prefix + 'criteria_audit/run_compression.py']),
        ('baseline-spectra', [prefix + 'structural/verify_baseline.py']),
        ('comm-module', [prefix + 'structural/verify_modules_independent.py']),
        ('noncomm-module', [prefix + 'structural/verify_noncomm_independent.py']),
        ('inherited-solvability', [prefix + 'structural/inherited_solvability.py']),
        ('signed-scalar-reduction', [prefix + 'nonintegral/verify_reduction.py']),
        ('spherical-lattice', [prefix + 'nonintegral/verify_spherical_lattice.py']),
        ('two-character', [prefix + 'nonintegral/verify_two_character.py']),
        ('selected-models', [prefix + 'known_models/select_and_verify.py']),
        ('independent-model-audit', [prefix + 'arithmetic/model_audit.py']),
        ('model-179', [prefix + 'nonintegral/integral179/verify.py']),
    ]
    manifest = HERE / 'additional_accepted.json'
    accepted = read_json(manifest) if manifest.exists() else []
    d120 = {r['id'] for r in accepted if r['status'] == 'excluded' and
            r['evidence'].get('proof') == 'criteria_audit/D120_THEORY.md'}
    need(not d120 or d120 == {'R11_1_40', 'R11_1_82'},
         'dimension-120 acceptance must cover exactly the reviewed pair')
    if d120:
        need((HERE / 'criteria_audit/D120_THEORY.md').is_file(),
             'accepted dimension-120 proof is missing')
        rows.append(('dimension-120', [prefix + 'induction/verify_dimension120.py']))
    accepted_by_id = {record['id']: record for record in accepted}
    if 'R11_1_104' in accepted_by_id:
        need(accepted_by_id['R11_1_104']['status'] == 'unitarily_realized',
             'Jordan model acceptance status')
        rows.extend([
            ('model-104-primary', [prefix + 'known_models/jordan_verify.py']),
            ('model-104-independent', [prefix + 'nonintegral/audit104/verify.py']),
        ])
    if 'R11_1_153' in accepted_by_id:
        need('R11_1_104' in accepted_by_id and
             accepted_by_id['R11_1_153']['status'] == 'excluded',
             'C4 exclusion requires the accepted reference model')
        rows.extend([
            ('c4-reduction', [prefix + 'integral/verify_c4_reduction.py']),
            ('c4-cohomology', [prefix + 'structural/verify_c4_cohomology_independent.py']),
            ('c4-torsor', [prefix + 'criteria_audit/verify_c4_torsor.py']),
            ('c4-exclusion', [prefix + 'integral/verify_c4_exclusion.py']),
        ])
    rows.append(('ledger', [prefix + 'build_ledger.py']))
    return rows


STAGE_DEPENDENCIES = {
    'spherical-lattice': ['signed-scalar-reduction'],
    'two-character': ['signed-scalar-reduction'],
    'independent-model-audit': ['selected-models'],
    'model-104-independent': ['model-104-primary'],
    'c4-exclusion': ['model-104-primary', 'model-104-independent',
                     'c4-reduction', 'c4-cohomology', 'c4-torsor'],
}


def select_stages(planned, only):
    if not only:
        return planned
    available = {name for name, command in planned}
    selected = {name.strip() for argument in only for name in argument.split(',') if name.strip()}
    need(selected and selected <= available,
         'unknown stage names: ' + ', '.join(sorted(selected - available)))
    # Even a partial replay rebinds the source and compares the regenerated
    # ledger. Required proof dependencies cannot be dropped by filtering.
    selected.update(['source', 'ledger'])
    while True:
        before = set(selected)
        for name in before:
            selected.update(STAGE_DEPENDENCIES.get(name, []))
        if before == selected:
            break
    need(selected <= available, 'selected proof has an unaccepted or unavailable dependency')
    return [(name, command) for name, command in planned if name in selected]


def audit_manifest():
    manifest = read_json(HERE / 'packaging_dependencies.json')
    missing = [p for p in manifest['files'] if not (ROOT / p).is_file()]
    need(not missing, 'missing package files: ' + ', '.join(missing))
    for p in manifest['files']:
        need(not Path(p).is_absolute() and '..' not in Path(p).parts,
             'nonportable manifest path')
    # Ordinary and -O runs alone do not reveal disabled assertions on valid
    # input. Reject assert statements in the entrypoints themselves as well.
    assertions = []
    for name, args in stages():
        path = ROOT / args[0]
        for node in ast.walk(ast.parse(path.read_text(), filename=str(path))):
            if isinstance(node, ast.Assert):
                assertions.append(f'{args[0]}:{node.lineno}')
    need(not assertions, 'verification entrypoints contain removable assert: ' +
         ', '.join(assertions))
    return {'required_files': len(manifest['files']),
            'entrypoint_assert_statements': 0,
            'python_packages': manifest['python_packages']}


def run_stage(name, args, mode, log_dir, timeout):
    command = [sys.executable] + (['-O'] if mode == 'optimized' else []) + args
    output = log_dir / f'{mode}-{name}.log'
    start = time.monotonic()
    print(f'[{mode}] {name}: started', flush=True)
    with output.open('w') as stream:
        proc = subprocess.Popen(command, cwd=ROOT, stdout=stream,
                                stderr=subprocess.STDOUT)
        try:
            while True:
                try:
                    code = proc.wait(timeout=min(30, timeout))
                    break
                except subprocess.TimeoutExpired:
                    elapsed = time.monotonic() - start
                    if elapsed >= timeout:
                        proc.kill()
                        proc.wait()
                        raise TimeoutError(f'{name} exceeded {timeout} seconds; see {output}')
                    print(f'[{mode}] {name}: still checking ({elapsed:.0f}s)', flush=True)
        except BaseException:
            if proc.poll() is None:
                proc.kill()
                proc.wait()
            raise
    need(code == 0, f'{mode} {name} failed with exit {code}; see {output}')
    elapsed = time.monotonic() - start
    print(f'[{mode}] {name}: PASS ({elapsed:.1f}s)', flush=True)
    return {'stage': name, 'mode': mode, 'status': 'PASS',
            'seconds': elapsed, 'command': command,
            'log': str(output.relative_to(HERE)) if output.is_relative_to(HERE) else str(output)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mode', choices=['both', 'normal', 'optimized'], default='both')
    parser.add_argument('--list', action='store_true', help='list commands without running checks')
    parser.add_argument('--only', action='append',
                        help='comma-separated stage names; repeatable; automatically includes dependencies, source and ledger')
    parser.add_argument('--check-source', action='store_true', help=argparse.SUPPRESS)
    parser.add_argument('--check-package', action='store_true', help='check dependency files and entrypoint assertion policy only')
    parser.add_argument('--timeout', type=float, default=3600, help='per-stage timeout in seconds')
    parser.add_argument('--log-dir', type=Path, default=HERE / 'replay_logs')
    args = parser.parse_args()
    need(args.timeout > 0, 'timeout must be positive')
    if args.check_source:
        check_source()
        return
    planned = select_stages(stages(), args.only)
    modes = ['normal', 'optimized'] if args.mode == 'both' else [args.mode]
    if args.list:
        for mode in modes:
            for name, command in planned:
                print(mode, name, ' '.join(['python'] + (['-O'] if mode == 'optimized' else []) + command))
        return
    package = audit_manifest()
    if args.check_package:
        print(json.dumps({'status': 'PASS', **package}, indent=2))
        return
    expected = ledger_map()
    log_dir = args.log_dir.resolve()
    log_dir.mkdir(parents=True, exist_ok=True)
    result = {'status': 'RUNNING', 'modes': modes, 'package': package,
              'partial_replay': bool(args.only), 'stages': [name for name, command in planned],
              'expected_status_hash_map': expected, 'checks': [],
              'note': 'Only accepted finite checks; no discovery or bounded search determines a status.'}
    report = log_dir / 'replay_report.json'
    def save():
        report.write_text(json.dumps(result, indent=2) + '\n')
    save()
    try:
        for mode in modes:
            for name, command in planned:
                result['checks'].append(run_stage(name, command, mode, log_dir, args.timeout))
                if name == 'ledger':
                    actual = ledger_map()
                    changed = sorted(rid for rid in set(expected) | set(actual)
                                     if expected.get(rid) != actual.get(rid))
                    need(not changed, 'regenerated status/hash mapping changed: ' + ', '.join(changed))
                save()
        result['status'] = 'PASS'
        result['status_hash_mapping_unchanged'] = True
        save()
        print(f'PASS: {len(result["checks"])} accepted checks; all 182 status/hash mappings unchanged')
        print(report)
    except BaseException as error:
        result['status'] = 'FAILED'
        result['error'] = f'{type(error).__name__}: {error}'
        save()
        raise


if __name__ == '__main__':
    main()
