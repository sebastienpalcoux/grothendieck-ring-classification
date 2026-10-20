"""Read-only, source-bound replay of the complete R5039 C8 proof chain.

Public API: verify(rid, tensor, progress=None). This is a mathematical replay,
not the publication/acceptance dispatcher. Every branch is reconstructed;
neither solver status nor previously written PASS receipts are trusted.
The scoped interception of legacy receipt writes makes the API read-only.
Call serially: the legacy modules and their pathlib adapters are process-global.
"""
from contextlib import contextmanager, redirect_stdout
import hashlib
import importlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
import time

HERE = Path(__file__).resolve().parent
BASE = HERE.parents[1]
ROOT = BASE.parents[1]
RID = 'R7_5_5039'
SOURCE_SHA256 = '8606c63a2f02ea028185db755a4b055382073b94736d5040ee92f3eec07f450c'
for directory in (HERE, BASE/'modules', BASE/'integral_gram', BASE/'criteria', BASE/'computation'):
    if str(directory) not in sys.path:
        sys.path.insert(0, str(directory))


def require(value, message):
    if not value:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def canonical(value):
    return json.loads(json.dumps(value))


def load(path):
    return json.loads(path.read_text())


def unique_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@contextmanager
def readonly_legacy_io():
    """Capture documented legacy output only; reject any other write."""
    reads, captured = set(), {}
    temporary = tempfile.TemporaryDirectory(prefix='r5039_exact_replay_')
    temporary_root = Path(temporary.name).resolve()
    previous_tempdir = tempfile.tempdir
    tempfile.tempdir = str(temporary_root)
    previous_bytecode = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    original_spec = importlib.util.spec_from_file_location
    original_text, original_bytes = Path.read_text, Path.read_bytes
    original_write, original_write_bytes, original_open = Path.write_text, Path.write_bytes, Path.open
    allowed = {BASE/'modules/r5039_c2_independent_domain_audit.json': 'receipt'}
    for case in (0, 1):
        stem = f'{RID}_c8_case{case}_chi8_0'
        allowed[BASE/'integral_gram'/(stem+'_phi_cross_allocations.json')] = 'compare'
        for mode in ('normal', 'optimized'):
            for suffix in ('rotation_replay_', 'phi_farkas_replay_'):
                allowed[BASE/'criteria'/(stem+'_'+suffix+mode+'.json')] = 'receipt'

    def read_text(path, *args, **kwargs):
        reads.add(path.resolve())
        return original_text(path, *args, **kwargs)

    def read_bytes(path, *args, **kwargs):
        reads.add(path.resolve())
        return original_bytes(path, *args, **kwargs)

    def write_text(path, text, *args, **kwargs):
        path = path.resolve()
        if path.is_relative_to(temporary_root):
            return original_write(path, text, *args, **kwargs)
        require(path in allowed, 'Unexpected attempted write during read-only proof replay: '+str(path))
        value = json.loads(text)
        if allowed[path] == 'compare':
            reads.add(path)
            require(value == json.loads(original_text(path)), 'Regenerated complete inventory differs: '+str(path))
        captured[path] = value
        return len(text)

    def deny_write(path, *args, **kwargs):
        if path.resolve().is_relative_to(temporary_root):
            return original_write_bytes(path, *args, **kwargs)
        raise ValueError('Unexpected binary write during read-only proof replay: '+str(path))

    def guarded_open(path, mode='r', *args, **kwargs):
        require(not any(c in mode for c in 'wax+') or path.resolve().is_relative_to(temporary_root),
                'Unexpected file mutation during proof replay: '+str(path))
        if not any(c in mode for c in 'wax+'):
            reads.add(path.resolve())
        return original_open(path, mode, *args, **kwargs)

    def recorded_spec(name, location=None, *args, **kwargs):
        if location is not None:
            reads.add(Path(location).resolve())
        return original_spec(name, location, *args, **kwargs)

    Path.read_text, Path.read_bytes = read_text, read_bytes
    Path.write_text, Path.write_bytes, Path.open = write_text, deny_write, guarded_open
    importlib.util.spec_from_file_location = recorded_spec
    try:
        yield reads, captured
    finally:
        Path.read_text, Path.read_bytes = original_text, original_bytes
        Path.write_text, Path.write_bytes, Path.open = original_write, original_write_bytes, original_open
        importlib.util.spec_from_file_location = original_spec
        sys.dont_write_bytecode = previous_bytecode
        tempfile.tempdir = previous_tempdir
        temporary.cleanup()


PROOF_NOTES = [
    'models/sqrt5/CYCLIC_ROTATION_OBSTRUCTION.md',
    'models/sqrt5/POWER_MOMENT_PHASES_PROOF.md',
    'models/sqrt5/CONDUCTOR8_BUDGET_PROOF.md',
    'models/sqrt5/C0_FORCED_EIGHTH_PACKET.md',
    'models/sqrt5/INTEGRAL_FUSION_NORM_PROOF.md',
    'models/sqrt5/TRANSPORT_PROOF.md',
    'models/sqrt5/LOW_COMPRESSION_PROOF.md',
    'models/sqrt5/R5039_CYCLIC_CHAIN.md',
    'modules/EIGHTH_INDICATOR_SYSTEM.md',
    'modules/Q5_SATURATION_INDEPENDENT_AUDIT.md',
    'modules/CHI_MINUS8_SIGN_SAFE_DICHOTOMY.md',
    'modules/PRIME_PROJECTION_FP_WEIGHTS.md',
    'modules/FOURTH_INDICATOR_INDEPENDENT_AUDIT.md',
    'modules/ALL_WORD_UNIT_FUNCTIONAL.md',
]


def verify(rid, tensor, progress=None):
    """Return a complete exact receipt, or raise on any missing/changed step."""
    require(rid == RID, 'This verifier proves only R7_5_5039.')
    require(digest(tensor) == SOURCE_SHA256, 'Input tensor does not match the pinned original source.')
    started = time.monotonic()
    stages = []
    initial_modules = set(sys.modules)

    def stage(name, function):
        if progress:
            progress({'event': 'start', 'stage': name})
        begin = time.monotonic()
        with redirect_stdout(io.StringIO()):
            result = function()
        stages.append({'stage': name, 'seconds': time.monotonic()-begin, 'result': result})
        if progress:
            progress({'event': 'pass', 'stage': name, 'seconds': stages[-1]['seconds']})
        return result

    with readonly_legacy_io() as (reads, captured):
        declaration = load(HERE/'r5039_cyclic_dependencies.json')
        require(declaration['id'] == rid and declaration['tensor_sha256'] == SOURCE_SHA256,
                'Declared proof dependency inventory must bind the original tensor.')
        declared = declaration['files']
        require(declared == sorted(set(declared)), 'Canonical distinct declared proof paths.')
        declared_paths = {(ROOT/name).resolve() for name in declared}
        require(all(p.is_relative_to(ROOT) and p.is_file() for p in declared_paths),
                'Every declared dependency is a repository file.')
        census = load(ROOT/'supplements/rank7/output/m5/census.json')
        require(next(r['tensor'] for r in census if r['id'] == rid) == tensor,
                'Pinned input differs from the canonical census tensor.')
        reduction = unique_module('_r5039_chain_signed_reduction', BASE/'sqrt5_reduction/verify_reduction.py')
        reduced = stage('general_to_spherical_galois_pseudounitary', reduction.run)
        require(reduced['status'] == 'PASS', 'General categorification reduction failed.')
        branch = next(r for r in reduced['results'] if r['id'] == rid)
        require(branch['tensor_sha256'] == SOURCE_SHA256 and len(branch['branches']) == 4,
                'All four signed quotient branches must be covered.')

        phase_module = importlib.import_module('verify_power_phase_inventory')
        phase_receipt = load(HERE/'power_3_moment_phases_certificate.json')
        phases = stage('independent_all_order_c8_phase_inventory', lambda: phase_module.verify(phase_receipt))
        require(phases['status'] == 'PASS' and phases['phase_count'] == 61, 'Complete 61-phase inventory required.')

        domain = importlib.import_module('verify_r5039_c2_domain')
        coverage = stage('complete_frames_labels_indicators_and_c2_modular_proofs', lambda: domain.run(write_receipt=False))
        require(coverage['status'] == 'PASS' and coverage['source_sha256'] == SOURCE_SHA256,
                'Complete source-bound frame reconstruction required.')
        require(coverage['low_frames'] == 4 and coverage['global_rows'] == 142510,
                'Unexpected complete low/high domain sizes.')
        require(coverage['case_classes'] == [[0,2,4,6,8,10],[1,3,5,7,9,11]],
                'All twelve label assignments must be covered by two representatives.')

        search = importlib.import_module('q5_cyclic_eight_search')
        prepared = stage('prepare_source_bound_c0_domain', lambda: search.prepare(rid))
        # Large internal objects are used only for rebuilding, not receipt output.
        stages[-1]['result'] = {'source_sha256': SOURCE_SHA256, 'orbits': len(prepared['orbits'])}

        def rebuild_word_order():
            module = importlib.import_module('all_word_order')
            fixture = load(BASE/'integral_gram/R7_5_5039_full_field_verlinde_chi8_0_fp5.json')
            fresh = module.generate(fixture)
            old = prepared['word']
            require(fresh['status'] == 'STABILIZED', 'Finite all-word order closure did not stabilize.')
            for key in ('source_sha256','domain_sha256','constraints','degree','ambient_dimension','spectral_points'):
                require(fresh[key] == old[key], 'Recomputed all-word order differs: '+key)
            require([s['lattice_sha256'] for s in fresh['steps']] == [s['lattice_sha256'] for s in old['steps']],
                    'Every intermediate word-order lattice must agree.')
            return {'rounds': len(fresh['steps']), 'constraints': len(fresh['constraints']),
                    'domain_sha256': fresh['domain_sha256'], 'constraints_sha256': digest(fresh['constraints'])}
        stage('independent_all_word_congruence_regeneration', rebuild_word_order)

        norm = importlib.import_module('audit_c8_norm_cuts')
        for case in (0,1):
            def rebuild(case=case):
                path = BASE/'criteria'/f'{rid}_c8_case{case}_chi8_0_system.json'
                old = load(path)
                fresh = canonical(search.build(rid, case, 0, prepared))
                require(fresh == old, 'Entire c0 system must regenerate exactly, including source inputs.')
                require(old['phase_records'] == phase_receipt['phases'], 'C0 system uses the independently checked phase inventory.')
                return {'case': case, 'system_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                        'columns': len(old['columns']), 'equations': len(old['rhs'])}
            stage(f'c0_case{case}_full_system_regeneration', rebuild)
            for c in (0,2):
                path = BASE/'criteria'/f'{rid}_c8_case{case}_chi8_{c}_system.json'
                stage(f'case{case}_c{c}_independent_integer_norm_cut', lambda path=path: norm.audit(path))

        allocations = importlib.import_module('verify_chi8_allocations')
        stage('complete_c0_aggregate_allocations', lambda: allocations.run(0))
        lattice = importlib.import_module('chi8_phase_lattice')
        rotation = importlib.import_module('c8_c0_rotation_split')
        phi = importlib.import_module('chi8_phi_cross_allocations')
        farkas = importlib.import_module('chi8_phi_exact_farkas')
        forced = importlib.import_module('verify_c0_forced_eighth_packet')
        remaining = {}
        for case in (0,1):
            stem = f'{rid}_c8_case{case}_chi8_0'
            system_path = BASE/'criteria'/(stem+'_system.json')
            system = load(system_path)

            def replay_phases():
                lattice.run(system_path, replay=True)
                inventory = load(BASE/'integral_gram'/(stem+'_system_phase_lattice.json'))
                active = [j for j,l in enumerate(system['phase_labels'])
                          if any(v[0] != v[1] for v,g,z in system['orbits'][l['orbit']])]
                require(inventory['active_columns'] == active, 'Exact active column inventory.')
                total = sum(r['total'] for r in inventory['branches'])
                supports = [s for r in inventory['branches'] for s in r['remaining']]
                require(total == 615 and len(supports) == 4, 'Complete 615-to-four phase coverage.')
                grams = load(BASE/'integral_gram'/(stem+'_phase_gram.json'))
                require([b['support'] for b in grams] == supports, 'Gram branches cover exactly all surviving phase supports.')
                return {'case': case, 'complete_phase_allocations': total, 'remaining': len(supports)}
            stage(f'c0_case{case}_complete_phase_lattice', replay_phases)
            stage(f'c0_case{case}_five_C4_integer_branches', lambda case=case: rotation.run(case,replay=True))
            stage(f'c0_case{case}_raw_phi_allocation_regeneration', lambda case=case: phi.run(case))
            # The captured regeneration has already been compared to canonical data.
            stages[-1]['result'] = {'case': case, 'raw_allocations': 1004, 'psd_allocations': 50}
            stage(f'c0_case{case}_200_exact_phi_separations', lambda case=case: farkas.run(case,replay=True))
            final_phi = load(BASE/'criteria'/(stem+'_phi_exact_farkas.json'))
            remaining[case] = final_phi['unresolved']
            require(len(remaining[case]) == (16 if case == 0 else 8), 'Complete remaining phi/chi branch count.')
            stage(f'c0_case{case}_forced_eighth_packet', lambda case=case: forced.verify(case))

        trees = importlib.import_module('verify_c0_capacity_trees')
        final_trees = stage('independent_all_48_capacity_and_integer_tree_proofs', lambda: trees.verify_all(require_trees=True))
        require(final_trees['status'] == 'PASS' and final_trees['source_sha256'] == SOURCE_SHA256,
                'Every final conditional tree must pass independent replay.')
        expected = set()
        for case, records in remaining.items():
            for rec in records:
                for option in (0,1):
                    expected.add((case, 2*rec['chi_choice']+option, rec['phi_allocation']))
        actual = {(r['case'],r['packet'],r['phi']) for r in final_trees['trees']}
        require(actual == expected and len(expected) == 48 and final_trees['total_leaves'] == 96,
                'The final trees must cover every remaining conditional branch exactly.')

        # Include theorem notes and all source/code dependencies in the receipt.
        for name in PROOF_NOTES:
            path = BASE/name
            require(path.is_file(), 'Missing mathematical proof dependency: '+name)
            reads.add(path.resolve())
        reads.add(Path(__file__).resolve())
        reads.add((BASE/'sqrt5_reduction/verify_reduction.py').resolve())
        for path in (BASE/'sqrt5_reduction').glob('*.md'):
            reads.add(path.resolve())
        for name, module in tuple(sys.modules.items()):
            if name in initial_modules:
                continue
            path = getattr(module, '__file__', None)
            if path:
                path = Path(path).resolve()
                if path.suffix == '.py' and path.is_relative_to(ROOT):
                    reads.add(path)
        consumed = {p for p in reads if p.is_relative_to(ROOT) and p.is_file()}
        require(consumed <= declared_paths,
                'Undeclared proof dependencies: '+str(sorted(str(p.relative_to(ROOT)) for p in consumed-declared_paths)))
        manifest = {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
                    for path in sorted(declared_paths)}

    return {'status': 'PASS', 'id': rid, 'source_sha256': SOURCE_SHA256,
            'kind': 'q5_cyclic_rotation_general', 'scope': 'general_complex',
            'tensor_sha256': SOURCE_SHA256,
            'conclusion': 'The complete source-bound necessary categorical systems are inconsistent in every general-categorification branch.',
            'publication_acceptance': 'Separate root-owned decision; this receipt is exact verification evidence.',
            'arithmetic': 'Exact integer/rational/algebraic reconstruction; no solver status is used.',
            'read_only': True, 'optimized_python': not __debug__,
            'c2_representatives': 2, 'c0_complete_trees': 48, 'c0_exact_leaves': 96,
            'stages': stages, 'dependencies_sha256': manifest, 'proof_manifest': manifest,
            'seconds': time.monotonic()-started}


def main():
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, help='Optional receipt output; verification itself is read-only.')
    parser.add_argument('--quiet', action='store_true')
    parser.add_argument('--repeat', type=int, default=1, help='Repeat in the same process to test warmed-module replay.')
    args = parser.parse_args()
    tensor = next(r['tensor'] for r in load(ROOT/'supplements/rank7/output/m5/census.json') if r['id'] == RID)
    def progress(record):
        if not args.quiet:
            print(json.dumps(record), flush=True)
    require(args.repeat >= 1, 'At least one complete replay is required.')
    previous = None
    for repetition in range(args.repeat):
        result = verify(RID, tensor, progress)
        if previous is not None:
            require(result['proof_manifest'] == previous['proof_manifest'],
                    'Declared proof manifest must be stable across warmed-process replays.')
        previous = result
    result['same_process_replays'] = args.repeat
    if args.output:
        args.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('stages','dependencies_sha256','proof_manifest')}), flush=True)


if __name__ == '__main__':
    main()
