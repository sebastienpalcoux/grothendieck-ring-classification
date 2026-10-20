"""Read-only source-bound R3895 whole-chain replay.

verify(rid, tensor) is strict: missing/incomplete final branches raise.
allow_incomplete=True is a development coverage audit and can never return
PASS while any final branch or the frozen dependency inventory is missing.
No numerical solver status or generated receipt is trusted as a premise.
Call serially: the legacy pathlib and import adapters are process-global.
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
RID = 'R7_5_3895'
SOURCE = '590b613093643a1c3047e866213050ba7fd87c211a42906de823d0c613d11ad0'
PHI = (0, 19, 160, 165)
EXPECTED = [(case, phi, r, 1) for case in (0, 2) for phi in PHI
            for r in (5, 6) if (case, phi, r) != (2, 0, 5)]
for directory in (HERE, BASE/'modules', BASE/'integral_gram', BASE/'criteria', BASE/'computation'):
    if str(directory) not in sys.path:
        sys.path.insert(0, str(directory))


def require(ok, message):
    if not ok:
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


def certificate_path(key):
    case, phi, r, s = key
    return BASE/'computation'/f'{RID}_c8_case{case}_phi{phi}_r{r}_s{s}_exact_probing.json'


def incomplete_branches():
    missing = []
    for key in EXPECTED:
        path = certificate_path(key)
        if not path.is_file():
            missing.append({'branch': list(key), 'reason': 'missing certificate'})
            continue
        try:
            record = load(path)
        except (ValueError, OSError):
            missing.append({'branch': list(key), 'reason': 'unreadable/incomplete certificate'})
            continue
        if record.get('status') != 'complete_conditional_exclusion' or 'terminal_y' not in record:
            missing.append({'branch': list(key), 'reason': 'no complete terminal proof'})
    return missing


@contextmanager
def readonly_legacy_io():
    """Keep legacy generated receipts in memory, including subsequent reads."""
    reads, captured = set(), {}
    temp = tempfile.TemporaryDirectory(prefix='r3895_exact_replay_')
    temp_root = Path(temp.name).resolve()
    old_temp, old_bytecode = tempfile.tempdir, sys.dont_write_bytecode
    tempfile.tempdir, sys.dont_write_bytecode = str(temp_root), True
    originals = (Path.read_text, Path.read_bytes, Path.write_text, Path.write_bytes,
                 Path.open, importlib.util.spec_from_file_location)
    rt, rb, wt, wb, op, spec = originals
    allowed = set()
    for suffix in ('normal', 'optimized'):
        for name in ('source_domain_replay_', 'negative_indicator_replay_', 'frame6_replay_'):
            allowed.add(BASE/'integral_gram'/(name+suffix+'.json'))
        for name in ('inactive_branch_replay_', 'branch_lattice_replay_', 'integer_trees_6_'):
            allowed.add(BASE/'computation'/(name+suffix+'.json'))
        for case in (0, 2):
            for phi in PHI:
                allowed.add(BASE/'criteria'/f'{RID}_c8_case{case}_branch{phi}_rotation_replay_{suffix}.json')

    def read_text(path, *args, **kwargs):
        path = path.resolve()
        if path in captured:
            return captured[path]
        reads.add(path)
        return rt(path, *args, **kwargs)

    def read_bytes(path, *args, **kwargs):
        path = path.resolve()
        if path in captured:
            return captured[path].encode()
        reads.add(path)
        return rb(path, *args, **kwargs)

    def write_text(path, text, *args, **kwargs):
        path = path.resolve()
        if path.is_relative_to(temp_root):
            return wt(path, text, *args, **kwargs)
        require(path in allowed, 'Unexpected repository mutation during replay: '+str(path))
        json.loads(text)
        captured[path] = text
        # A legacy verifier refers explicitly to its normal receipt even under
        # -O. Supply the freshly regenerated logical result, never disk status.
        for suffix, other in (('_normal.json', '_optimized.json'), ('_optimized.json', '_normal.json')):
            if path.name.endswith(suffix):
                captured[path.with_name(path.name[:-len(suffix)]+other)] = text
        return len(text)

    def write_bytes(path, *args, **kwargs):
        require(path.resolve().is_relative_to(temp_root), 'Unexpected binary write during replay.')
        return wb(path, *args, **kwargs)

    def open_file(path, mode='r', *args, **kwargs):
        path = path.resolve()
        require(not any(c in mode for c in 'wax+') or path.is_relative_to(temp_root),
                'Unexpected direct file mutation during replay: '+str(path))
        if path in captured:
            return io.BytesIO(captured[path].encode()) if 'b' in mode else io.StringIO(captured[path])
        reads.add(path)
        return op(path, mode, *args, **kwargs)

    def record_spec(name, location=None, *args, **kwargs):
        if location is not None:
            reads.add(Path(location).resolve())
        return spec(name, location, *args, **kwargs)

    Path.read_text, Path.read_bytes, Path.write_text = read_text, read_bytes, write_text
    Path.write_bytes, Path.open = write_bytes, open_file
    importlib.util.spec_from_file_location = record_spec
    try:
        yield reads, captured
    finally:
        Path.read_text, Path.read_bytes, Path.write_text, Path.write_bytes, Path.open = originals[:5]
        importlib.util.spec_from_file_location = originals[5]
        tempfile.tempdir, sys.dont_write_bytecode = old_temp, old_bytecode
        temp.cleanup()


def replay_frame8_farkas():
    """Derive precisely the four surviving phi allocations from all 32."""
    initial = load(BASE/'computation/inactive_branch_replay_normal.json')['results']
    record = load(BASE/'integral_gram/R7_5_3895_branch_farkas_8.json')
    allocations = load(BASE/'integral_gram/R7_5_3895_active_8.json')['branches']
    unresolved, covered = set(), set()
    expected_keys = set()
    for case in (0, 2, 4, 6):
        system = load(BASE/'integral_gram'/f'{RID}_system_8_{case}.json')
        cols, active = system['columns'], set(system['active_variables'])
        candidates = next(r['remaining_branch_indices'] for r in initial
                          if r['low_index'] == 8 and r['case'] == case)
        require(len(candidates) == 32, 'Complete frame-8 inactive lattice domain.')
        for phi in candidates:
            key = (case, phi)
            expected_keys.add(key)
            matches = [x for x in record['results'] if (x['case'], x['branch']) == key]
            require(len(matches) == 1, 'Unique exact frame-8 branch record.')
            entry = matches[0]
            rhs = [b-sum(n*cols[j][i] for j, n in allocations[phi]) for i, b in enumerate(system['rhs'])]
            keep = [j for j, col in enumerate(cols) if j not in active and all(col[i] <= rhs[i] for i in range(21))]
            require(entry['kept_columns'] == len(keep), 'Exact inactive nonnegative Gram removals.')
            if entry['separator'] is None:
                unresolved.add(key)
                continue
            y = record['separators'][entry['separator']]
            require(len(y) == len(rhs) and all(type(v) is int for v in y), 'Integral Farkas covector.')
            require(sum(a*b for a, b in zip(rhs, y)) < 0 and
                    all(sum(a*b for a, b in zip(cols[j], y)) >= 0 for j in keep),
                    'Exact complete frame-8 Farkas inequality.')
            covered.add(key)
    require({(r['case'], r['branch']) for r in record['results']} == expected_keys and len(record['results']) == 128,
            'No omitted or duplicate initial frame-8 alternatives.')
    require(unresolved == {(case, phi) for case in (0, 2, 4, 6) for phi in PHI}, 'Precisely all four phi allocations remain.')
    require(unresolved == {(r['case'], r['branch']) for r in record['unresolved']} and len(covered) == 112,
            'Complete source-bound frame-8 separation inventory.')
    return {'input_alternatives': 128, 'exact_farkas_exclusions': 112,
            'remaining_phi_allocations': list(PHI), 'positive_labels': [0, 2, 4, 6]}


NOTES = [
    'models/sqrt5/R3895_CHAIN_OBLIGATIONS.md',
    'models/sqrt5/R3895_CYCLIC_CHAIN.md',
    'models/sqrt5/CYCLIC_ROTATION_OBSTRUCTION.md',
    'models/sqrt5/POWER_MOMENT_PHASES_PROOF.md',
    'models/sqrt5/INTEGRAL_FUSION_NORM_PROOF.md',
    'models/sqrt5/TRANSPORT_PROOF.md',
    'models/sqrt5/LOW_COMPRESSION_PROOF.md',
    'modules/Q5_SATURATION_INDEPENDENT_AUDIT.md',
    'modules/PRIME_PROJECTION_FP_WEIGHTS.md',
    'modules/EIGHTH_INDICATOR_SYSTEM.md',
    'modules/FOURTH_INDICATOR_INDEPENDENT_AUDIT.md',
    'modules/ALL_WORD_UNIT_FUNCTIONAL.md',
    'modules/R3895_CHAIN_INDEPENDENT_AUDIT.md',
    'criteria/R3895_NORM_SLACK_PARITY.md',
    'criteria/R3895_PROBING_INDEPENDENT_AUDIT.md',
    'integral_gram/PROOF.md',
]


def verify(rid, tensor, progress=None, allow_incomplete=False):
    require(rid == RID and digest(tensor) == SOURCE, 'Pinned original R3895 tensor required.')
    missing = incomplete_branches()
    if missing and not allow_incomplete:
        raise ValueError('Incomplete whole-ring proof: '+json.dumps(missing))
    start = time.monotonic()
    stages, roots = [], []
    initial_modules = set(sys.modules)

    def module(name):
        result = importlib.import_module(name)
        roots.append(result)
        return result

    def stage(name, call):
        begin = time.monotonic()
        if progress:
            progress({'event': 'start', 'stage': name})
        with redirect_stdout(io.StringIO()):
            result = call()
        stages.append({'stage': name, 'seconds': time.monotonic()-begin, 'result': result})
        if progress:
            progress({'event': 'pass', 'stage': name, 'seconds': stages[-1]['seconds']})
        return result

    with readonly_legacy_io() as (reads, captured):
        require(next(r['tensor'] for r in load(ROOT/'supplements/rank7/output/m5/census.json') if r['id'] == rid) == tensor,
                'Canonical census must contain this original tensor.')
        reduction = unique_module('_r3895_chain_signed_reduction', BASE/'sqrt5_reduction/verify_reduction.py')
        roots.append(reduction)
        reduced = stage('general_to_spherical_galois_pseudounitary', reduction.run)
        require(reduced['status'] == 'PASS', 'Complete general categorification reduction.')
        branch = next(r for r in reduced['results'] if r['id'] == rid)
        require(branch['tensor_sha256'] == SOURCE and branch['branches'], 'Source-bound signed quotient coverage.')

        frame = module('verify_frame6')
        frame_result = stage('complete_source_domains_indicators_and_frame6_exclusion', frame.run)
        require(frame_result['status'] == 'PASS' and frame_result['source_sha256'] == SOURCE and
                frame_result['integer_trees'] == 16 and frame_result['integer_tree_leaves'] == 775,
                'All frame-6 alternatives must be excluded.')
        negative = load(BASE/'integral_gram/negative_indicator_replay_normal.json')
        negative_cases = load(BASE/'integral_gram/R7_5_3895_negative_indicator_certificate.json')['cases']
        negative_counts = {frame: sum(x['low_index'] == frame for x in negative_cases) for frame in (6, 8)}
        require(negative['status'] == 'PASS' and negative['negative_cases'] == 8 and negative_counts == {6: 4, 8: 4},
                'Both frames, including frame 8, require all four negative-indicator label exclusions.')
        frame_result['negative_indicator_cases_by_frame'] = negative_counts
        domains = load(BASE/'integral_gram/source_domain_replay_normal.json')
        require(domains['low_frames'] == 15 and domains['global_rows'] == 163766 and domains['surviving_frames'] == [6, 8],
                'Complete canonical low/high restriction domain.')
        stage('complete_frame8_phi_allocation_coverage', replay_frame8_farkas)
        labels = module('label_symmetry_audit')
        label_result = stage('complete_frame8_character_label_classes', lambda: labels.run(rid, 8))
        require(label_result['positive_indicator_case_classes'] == [[0, 4], [2, 6]], 'Both conductor-five sign classes required.')

        phase = module('verify_power_phase_inventory')
        phase_certificate = load(HERE/'power_3_moment_phases_certificate.json')
        phase_result = stage('independent_all_order_c8_phase_inventory', lambda: phase.verify(phase_certificate))
        require(phase_result['status'] == 'PASS' and phase_result['phase_count'] == 61, 'All-order 61-phase coverage.')
        search = module('q5_cyclic_eight_search')
        prepared = stage('prepare_source_bound_frame8_c8_domain', lambda: search.prepare(rid))
        stages[-1]['result'] = {'orbits': len(prepared['orbits']), 'source_sha256': SOURCE}

        def regenerate_filtered_verlinde():
            fresh = search.old.v.coefficients(prepared['table'],
                {'id': rid, 'low_index': 8, 'low': prepared['low'], 'orbits': prepared['orbits']},
                use_cache=False)
            require(canonical(fresh) == canonical(prepared['V']),
                    'Every filtered-domain low-Verlinde coefficient must regenerate from the original character table.')
            prepared['V'] = fresh
            return {'triples': len(fresh['triples']), 'orbits': len(fresh['orbits']),
                    'domain_sha256': fresh['domain_sha256'], 'coefficients_sha256': digest(canonical(fresh))}
        stage('filtered_c8_low_verlinde_coefficients_from_raw_source', regenerate_filtered_verlinde)

        def regenerate_words():
            order = module('all_word_order')
            fixture = load(BASE/'integral_gram/R7_5_3895_full_field_verlinde_branch0_fp5_words.json')
            fresh = order.generate(fixture)
            old = prepared['word']
            require(fresh['status'] == 'STABILIZED', 'Finite all-word order closure must stabilize.')
            for key in ('source_sha256', 'domain_sha256', 'constraints', 'degree', 'ambient_dimension', 'spectral_points'):
                require(fresh[key] == old[key], 'All-word source regeneration differs: '+key)
            require([s['lattice_sha256'] for s in fresh['steps']] == [s['lattice_sha256'] for s in old['steps']],
                    'Exact complete intermediate word-order lattices.')
            return {'rounds': len(fresh['steps']), 'constraints': len(fresh['constraints']), 'constraints_sha256': digest(fresh['constraints'])}
        stage('complete_all_word_congruence_regeneration', regenerate_words)
        norm = module('audit_c8_norm_cuts')
        parity = unique_module('_r3895_chain_norm_parity', BASE/'criteria/verify_r3895_norm_parity.py')
        roots.append(parity)
        rotation = module('r3895_c8_rotation_split')
        remaining = []
        for case in (0, 2):
            path = BASE/'criteria'/f'{RID}_c8_case{case}_system.json'
            def regenerate(case=case, path=path):
                old = load(path)
                fresh = canonical(search.build(rid, case, None, prepared))
                require(fresh == old, 'Entire frozen C8 system must regenerate from the source.')
                require(old['phase_records'] == phase_certificate['phases'], 'Independent phase inventory equality.')
                return {'case': case, 'columns': len(old['columns']), 'equations': len(old['rhs']),
                        'system_sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
            stage(f'case{case}_full_c8_system_regeneration', regenerate)
            stage(f'case{case}_independent_integer_fusion_norm_cut', lambda path=path: norm.audit(path))
            stage(f'case{case}_independent_norm_slack_parity', lambda case=case: parity.verify(case))
            for phi in PHI:
                stage(f'case{case}_phi{phi}_complete_thirty_C4_alternatives',
                      lambda case=case, phi=phi: rotation.run(case, phi, replay=True))
                record = load(BASE/'criteria'/f'{RID}_c8_case{case}_branch{phi}_rotation_split.json')
                require(len(record['results']) == 30, 'Every bounded C4 integer pair must occur.')
                remaining.extend((case, phi, x['r'], x['s']) for x in record['unresolved'])
        require(remaining == EXPECTED and len(remaining) == 15, 'Exactly all fifteen final conditional alternatives.')

        probing = unique_module('_r3895_chain_independent_probing', BASE/'criteria/verify_r3895_probing.py')
        roots.append(probing)
        final = []
        missing_keys = {tuple(x['branch']) for x in missing}
        for key in remaining:
            if key in missing_keys:
                continue
            result = stage('exact_conditional_probing_'+('_'.join(map(str, key))),
                           lambda key=key: probing.verify(*key, check_tree=False))
            require(result['status'] == 'PASS' and result['source_sha256'] == SOURCE, 'Complete independently reconstructed exact leaf proof.')
            final.append(result)
        require(len(final)+len(missing) == 15, 'Every final branch is replayed or explicitly incomplete.')

        for note in NOTES:
            path = BASE/note
            require(path.is_file(), 'Missing mathematical proof note: '+note)
            reads.add(path.resolve())
        for path in (BASE/'sqrt5_reduction').glob('*.md'):
            reads.add(path.resolve())
        reads.add(Path(__file__).resolve())
        # Explicit roots include unregistered importlib modules. Traverse their
        # module-valued globals, so warmed imports do not erase dependencies.
        seen = set()
        while roots:
            current = roots.pop()
            if id(current) in seen:
                continue
            seen.add(id(current))
            path = getattr(current, '__file__', None)
            if path and Path(path).resolve().is_relative_to(ROOT):
                reads.add(Path(path).resolve())
                roots.extend(v for v in vars(current).values() if isinstance(v, type(sys)))
        for name, imported in tuple(sys.modules.items()):
            if name not in initial_modules:
                path = getattr(imported, '__file__', None)
                if path and Path(path).suffix == '.py' and Path(path).resolve().is_relative_to(ROOT):
                    reads.add(Path(path).resolve())
        consumed = {p for p in reads if p.is_relative_to(ROOT) and p.is_file() and p not in captured}
        declaration_path = HERE/'r3895_cyclic_dependencies.json'
        frozen = declaration_path.is_file()
        if frozen:
            declaration = load(declaration_path)
            require(declaration['id'] == rid and declaration['tensor_sha256'] == SOURCE, 'Frozen dependency source identity.')
            names = declaration['files']
            require(names == sorted(set(names)), 'Canonical dependency inventory.')
            require(str(declaration_path.relative_to(ROOT)) in names, 'Frozen inventory must bind its own bytes.')
            declared = {(ROOT/name).resolve() for name in names}
            require(all(p.is_relative_to(ROOT) and p.is_file() for p in declared), 'Existing repository proof inputs.')
            require(consumed <= declared, 'Undeclared proof dependencies: '+str(sorted(str(p.relative_to(ROOT)) for p in consumed-declared)))
        else:
            declared = consumed
        manifest = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(declared)}

    complete = not missing and frozen
    require(allow_incomplete or complete, 'Complete finite proof and frozen dependency manifest required.')
    return {'status': 'PASS' if complete else 'INCOMPLETE', 'id': rid, 'source_sha256': SOURCE,
            'tensor_sha256': SOURCE, 'scope': 'general_complex', 'kind': 'q5_cyclic_rotation_general',
            'read_only': True, 'optimized_python': not __debug__, 'dependency_inventory_frozen': frozen,
            'expected_final_branches': [list(x) for x in EXPECTED], 'incomplete_final_branches': missing,
            'final_complete_branches': len(final), 'final_exact_leaves': sum(r['leaves'] for r in final),
            'publication_acceptance': 'Separate root-owned decision; incomplete receipts prove no whole-ring exclusion.',
            'stages': stages, 'proof_manifest': manifest, 'dependencies_sha256': manifest,
            'seconds': time.monotonic()-start}


def main():
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--allow-incomplete', action='store_true')
    parser.add_argument('--output', type=Path)
    parser.add_argument('--export-inventory', type=Path)
    parser.add_argument('--quiet', action='store_true')
    parser.add_argument('--repeat', type=int, default=1,
                        help='Repeat complete verification in one process to check warmed imports.')
    parser.add_argument('--block-scipy', action='store_true',
                        help='Reject every SciPy import throughout the exact replay.')
    args = parser.parse_args()
    require(args.repeat >= 1, 'At least one replay is required.')
    if args.block_scipy:
        import importlib.abc
        require(not any(name == 'scipy' or name.startswith('scipy.') for name in sys.modules),
                'The no-SciPy gate must begin before SciPy is imported.')
        class RejectScipy(importlib.abc.MetaPathFinder):
            def find_spec(self, fullname, path=None, target=None):
                if fullname == 'scipy' or fullname.startswith('scipy.'):
                    raise ImportError('SciPy is forbidden by this exact-replay gate.')
        sys.meta_path.insert(0, RejectScipy())
    tensor = next(r['tensor'] for r in load(ROOT/'supplements/rank7/output/m5/census.json') if r['id'] == RID)
    def progress(record):
        if not args.quiet:
            print(json.dumps(record), flush=True)
    previous = None
    for repetition in range(args.repeat):
        result = verify(RID, tensor, progress, args.allow_incomplete)
        if previous is not None:
            require(result['proof_manifest'] == previous['proof_manifest'],
                    'Proof manifest must remain identical with warmed imports and cached source calculations.')
        previous = result
    result['same_process_replays'] = args.repeat
    result['scipy_imports_blocked'] = args.block_scipy
    if args.export_inventory:
        names = set(result['proof_manifest'])
        names.add(str((HERE/'r3895_cyclic_dependencies.json').relative_to(ROOT)))
        inventory = {'id': RID, 'tensor_sha256': SOURCE, 'files': sorted(names)}
        args.export_inventory.write_text(json.dumps(inventory, indent=2)+'\n')
    if args.output:
        args.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('stages', 'proof_manifest', 'dependencies_sha256')}), flush=True)


if __name__ == '__main__':
    main()
