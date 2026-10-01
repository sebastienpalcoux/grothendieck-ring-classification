"""Preserve historical frontier receipts and describe the separate M9 frontier.

``--audit-only`` checks retained hashes/predicates without mathematical replay.
The default build requires the completed source-bound M9 campaigns and ledger.
Historical coverage, inputs and mathematical receipts are never rewritten.
"""
import argparse
import collections
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ADAPTER = 'research/frontier/m9_adapter/manifest.json'
HISTORICAL_COVERAGE = 'research/frontier/coverage.json'
AUDIT = 'research/frontier/m9_adapter/receipt_audit.json'
EXTENSION = 'research/frontier/m9/coverage.json'
INPUTS = 'research/frontier/m9/inputs.json'

# An exact, closed patch against the frozen historical driver is stronger than
# allowing arbitrary edits to selected AST functions. No mathematical verifier,
# command, predicate parser or replay subprocess implementation is changed.
DRIVER_PATCH = (
    ('def audit(entry):', 'def audit(entry, binding_check=None):'),
    ("    frozen = binding.get('files_sha256', {})\n",
     "    check = binding_check or (lambda name, expected: (ROOT/name).exists() and sha(ROOT/name) == expected)\n"
     "    frozen = binding.get('files_sha256', {})\n"),
    ('        if not path.exists() or sha(path) != expected:\n',
     '        if not check(name, expected):\n'),
    ('                if not item.exists() or sha(item) != digest:\n',
     '                if not check(name, digest):\n'),
    ("    manifest = json.loads(manifest_path.read_text())\n"
     "    if sha(ROOT/manifest['source_census']) != manifest['source_census_sha256']:\n",
     "    manifest = json.loads(manifest_path.read_text())\n"
     "    from frontier_m9 import HistoricalBinding\n"
     "    historical = HistoricalBinding(ROOT)\n"
     "    historical.validate_inventory()\n"
     "    if not historical.check(manifest['source_census'], manifest['source_census_sha256']):\n"),
    ('        results = [audit(entry) for entry in entries]\n',
     '        results = [audit(entry, historical.check) for entry in entries]\n'),
    ('                  mathematical_replay_performed=not args.check_receipts,\n',
     '                  mathematical_replay_performed=not args.check_receipts,\n'
     '                  historical_binding=historical.report(),\n'),
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def object_sha(value, sort_keys=False):
    return hashlib.sha256(json.dumps(value, sort_keys=sort_keys,
                                    separators=(',', ':')).encode()).hexdigest()


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2)+'\n')


def patched_driver(source):
    for before, after in DRIVER_PATCH:
        require(source.count(before) == 1, 'historical frontier driver patch anchor changed')
        source = source.replace(before, after)
    return source


class HistoricalBinding:
    """Resolve an old digest only by exact bytes or an explicitly checked adapter."""
    def __init__(self, root=ROOT):
        self.root = Path(root).resolve()
        self.adapter = json.loads(self.path(ADAPTER).read_text())
        require(self.adapter['schema'] == 'rank6-historical-frontier-adapter/v1',
                'unsupported historical frontier adapter')
        require(sha(self.path(HISTORICAL_COVERAGE)) == self.adapter['historical_coverage_sha256'],
                'historical frontier coverage changed')
        self.coverage = json.loads(self.path(HISTORICAL_COVERAGE).read_text())
        self.manifest_path = self.coverage['input_manifest']
        require(sha(self.path(self.manifest_path)) == self.coverage['input_manifest_sha256']
                == self.adapter['historical_input_manifest_sha256'],
                'historical frontier input manifest changed')
        self.inputs = json.loads(self.path(self.manifest_path).read_text())
        require(sha(Path(__file__)) == self.adapter['adapter_implementation_sha256'],
                'historical frontier adapter implementation changed')
        self.bindings = {}
        self.prefixes = {}
        census_spec = self.adapter['historical_census']
        require(census_spec['path'] == self.inputs['source_census']
                and census_spec['sha256'] == self.inputs['source_census_sha256'],
                'historical census adapter disagrees with frozen inputs')
        census = self.prefix(census_spec)
        ledger_spec = self.adapter['historical_ledger']
        require(ledger_spec['path'] == self.inputs['input_ledger']
                and ledger_spec['sha256'] == self.inputs['input_ledger_sha256'],
                'historical ledger adapter disagrees with frozen inputs')
        ledger = self.prefix(ledger_spec)
        require([r['id'] for r in census] == [r['id'] for r in ledger],
                'historical census/ledger prefix ordering differs')
        by_id = {r['id']: r for r in census}
        require(len(by_id) == len(census), 'duplicate historical census identifier')
        require(self.inputs['ids'] == [e['id'] for e in self.coverage['cases']]
                == [r['id'] for r in ledger if r['status'] == 'unresolved'],
                'historical frontier domain differs from historical ledger')
        for row in self.inputs['tensors']:
            require(row['id'] in by_id and by_id[row['id']]['N'] == row['N']
                    and object_sha(row['N'], sort_keys=True) == row['tensor_sha256'],
                    'historical frontier tensor changed: '+row['id'])
        self.source_adapters = self.adapter['source_adapters']
        require(set(self.source_adapters) == {'software/frontier_replay.py'},
                'undeclared historical source adapter; audit any additional source edit explicitly')
        spec = self.source_adapters['software/frontier_replay.py']
        frozen = self.path(spec['frozen_source'])
        require(spec['kind'] == 'closed_exact_driver_patch'
                and sha(frozen) == spec['historical_sha256'], 'frozen historical driver changed')
        current = self.path('software/frontier_replay.py')
        require(current.read_text() == patched_driver(frozen.read_text())
                and sha(current) == spec['adapted_sha256'],
                'frontier driver differs from the explicitly audited historical patch')

    def path(self, name):
        path = (self.root/name).resolve()
        require(path.is_relative_to(self.root), 'historical frontier path escapes package')
        return path

    def prefix(self, spec):
        path = self.path(spec['path'])
        rows = json.loads(path.read_text())
        n = spec['rows']
        require(len(rows) >= n and all(r['m'] <= spec['bound'] for r in rows[:n])
                and all(r['m'] > spec['bound'] for r in rows[n:]),
                'historical prefix boundary changed: '+spec['path'])
        original = rows[:n]
        require(dict(collections.Counter(r['m'] for r in original)) ==
                {int(m): count for m, count in spec['counts'].items()},
                'historical prefix multiplicities changed: '+spec['path'])
        reconstructed = (json.dumps(original, separators=(',', ':'))+'\n').encode()
        require(hashlib.sha256(reconstructed).hexdigest() == spec['sha256'],
                'historical prefix rows or metadata changed: '+spec['path'])
        self.prefixes[spec['path']] = dict(expected_sha256=spec['sha256'],
            current_file_sha256=sha(path), historical_rows=n, current_rows=len(rows),
            method='exact ordered prefix serialized with compact JSON and one newline')
        return original

    def check(self, name, expected):
        path = self.path(name)
        mode = None
        if path.is_file() and sha(path) == expected:
            mode = 'unchanged_exact_file'
        elif (name in self.prefixes and self.prefixes[name]['expected_sha256'] == expected
              and path.is_file() and sha(path) == self.prefixes[name]['current_file_sha256']):
            mode = 'exact_historical_prefix'
        elif (name in self.source_adapters and self.source_adapters[name]['historical_sha256'] == expected
              and path.is_file() and sha(path) == self.source_adapters[name]['adapted_sha256']):
            mode = 'declared_closed_source_adapter'
        if mode is not None:
            self.bindings[name] = dict(expected_sha256=expected, method=mode)
            return True
        return False

    def validate_inventory(self):
        import frontier_replay as replay
        require(replay.ROOT.resolve() == self.root, 'frontier audit must use its own package root')
        inventory = {}
        for entry in self.coverage['cases']:
            groups = [entry['binding']['files_sha256']]
            for receipt in entry['retained_receipts']:
                path = self.path(receipt['path'])
                require(path.is_file(), 'retained frontier receipt missing: '+receipt['path'])
                groups.append(replay.embedded_hashes(path))
            for group in groups:
                for name, expected in group.items():
                    require(name not in inventory or inventory[name] == expected,
                            'conflicting historical frontier hashes: '+name)
                    inventory[name] = expected
        require(len(inventory) == self.adapter['protected_inventory_count']
                and object_sha(inventory, sort_keys=True) == self.adapter['protected_inventory_sha256'],
                'historical frozen/embedded source inventory changed')
        for name, expected in inventory.items():
            require(self.check(name, expected), 'unapproved historical frontier hash mismatch: '+name)
        for name, spec in self.prefixes.items():
            require(self.check(name, spec['expected_sha256']), 'historical prefix binding failed: '+name)
        return inventory

    def report(self):
        return dict(adapter=ADAPTER, adapter_sha256=sha(self.path(ADAPTER)),
            implementation_sha256=sha(Path(__file__)), historical_prefixes=self.prefixes,
            protected_bindings=self.bindings,
            mathematical_replay_performed=False,
            interpretation='Old receipts retain their original hashes. Exact historical prefixes and a closed driver patch explain the extension; no historical mathematical replay is claimed.')


def audit_historical(root=ROOT, save=True):
    import frontier_replay as replay
    binding = HistoricalBinding(root)
    inventory = binding.validate_inventory()
    results = [replay.audit(entry, binding.check) for entry in binding.coverage['cases']]
    require(all(r['passed'] for r in results), 'historical retained frontier receipt audit failed')
    report = dict(schema='rank6-historical-frontier-audit/v1', passed=True,
                  mode='retained_receipt_and_source_adapter_audit', mathematical_replay_performed=False,
                  coverage_sha256=sha(binding.path(HISTORICAL_COVERAGE)),
                  protected_inventory_count=len(inventory),
                  retained_receipt_count=sum(len(r['receipts']) for r in results),
                  historical_binding=binding.report(), results=results)
    if save:
        write(binding.path(AUDIT), report)
    return report


def scoped_existence(record):
    structures = ('general', 'pivotal', 'spherical', 'pseudo_unitary', 'unitary')
    scope = record.get('structure')
    require(scope in ('pivotal', 'spherical', 'pseudo_unitary'), 'unsupported M9 frontier scoped claim')
    first = structures.index(scope)
    return {name: 'no' if i >= first else 'unknown' for i, name in enumerate(structures)}


def scoped_summary(record):
    scoped_existence(record)
    return {
        'pivotal': 'Pivotal, spherical, pseudo-unitary and unitary categorifications are ruled out by a retained exact certificate. General existence remains unknown.',
        'spherical': 'Spherical, pseudo-unitary and unitary categorifications are ruled out by a retained exact certificate. General and pivotal existence remain unknown.',
        'pseudo_unitary': 'Pseudo-unitary and unitary categorifications are ruled out by a retained exact certificate. General, pivotal and spherical existence remain unknown.',
    }[record['structure']]


def scoped_evidence(record, receipt):
    existence = scoped_existence(record)
    return dict(declared_structure=record['structure'],
                excluded_structures=[name for name, value in existence.items() if value == 'no'],
                unknown_structures=[name for name, value in existence.items() if value == 'unknown'],
                certificate_kind=record['certificate']['kind'],
                certificate_sha256=object_sha(record['certificate'], sort_keys=True),
                tensor_sha256=record['tensor_sha256'], retained_exact_replay=receipt,
                general_exclusion=False)


def braided_evidence(tensor):
    """Check the based-ring hypotheses of the R6_9_3748 braided obstruction."""
    labels = [0, 1, 5]
    expected = [[[1, 0, 0], [0, 1, 0], [0, 0, 1]],
                [[0, 1, 0], [1, 0, 1], [0, 1, 1]],
                [[0, 0, 1], [0, 1, 1], [1, 1, 1]]]
    for i, a in enumerate(labels):
        for j, b in enumerate(labels):
            product = [0] * 6
            for k, c in enumerate(labels):
                product[c] = expected[i][j][k]
            require(tensor[a][b] == product, 'braided obstruction rank-three product changed')
    require(all(tensor[a][b][0] == int(a == b) for a in labels for b in range(6)),
            'braided obstruction subring is not dual closed')
    supports = [[k for k, value in enumerate(tensor[j][j]) if value] for j in range(1, 6)]
    require(supports == [[0, 5], [0, 2, 3, 4], [0, 2, 3, 4, 5],
                         [0, 1, 2, 3, 4, 5], [0, 1, 5]]
            and all(not set(support) <= {0, j} for j, support in enumerate(supports, 1)),
            'braided obstruction no-rank-two-subring test failed')
    # The displayed products give a^3-a^2-2a+1=0. Its only possible
    # rational roots are +/-1, and both fail, so FPdim(a) is not integral.
    require(all(t**3-t**2-2*t+1 != 0 for t in (-1, 1)), 'nonintegrality test failed')
    return dict(kind='nondegenerate_rank_three_centralizer_obstruction',
                braided_existence='no', general_exclusion=False,
                subring_labels=labels, subring_products=expected,
                square_supports=supports, exact_based_ring_checks_passed=True,
                dimension_polynomial=[1, -1, -2, 1],
                proof_path='papers/chapters/multiplicity9.tex',
                theorem_references='DGNO, Corollary 2.46 and Theorem 3.13',
                tensor_sha256=object_sha(tensor, sort_keys=True))


BRAIDED_SUMMARY = ('Braided categorifications are ruled out by the rank-three subcategory '
                   'and centralizer obstruction. General, pivotal, spherical, pseudo-unitary '
                   'and unitary existence remain unknown.')


def public_cases(historical, cases):
    summaries = [dict(id=e['id'], categorical_status='unresolved', public_summary=e['public_summary'],
                     coverage=HISTORICAL_COVERAGE, evidence_mode='retained_historical_receipt_audit')
                 for e in historical['cases']]
    for case in cases:
        item = dict(id=case['id'], categorical_status='unresolved', public_summary=case['public_summary'],
                    coverage=EXTENSION, general_reduction_status='not_established')
        if case.get('scoped_nonexistence') is not None:
            item['scoped_nonexistence'] = case['scoped_nonexistence']
        if case.get('braided_nonexistence') is not None:
            item['braided_existence'] = 'no'
            item['braided_nonexistence'] = case['braided_nonexistence']
        summaries.append(item)
    return summaries


def build():
    """Build only after the complete M9 ledger and both campaigns are committed."""
    import release
    rows = json.loads((ROOT/'data/census.json').read_text())
    ledger = json.loads((ROOT/'data/decisions.json').read_text())
    require([r['id'] for r in rows] == [r['id'] for r in ledger]
            and len({r['id'] for r in rows}) == len(rows), 'frontier requires the complete ordered census ledger')
    require(max(r['m'] for r in rows) == 9, 'frontier extension requires bound nine')
    report = json.loads((ROOT/'verification/release_summary.json').read_text())
    census_hash, ledger_hash = sha(ROOT/'data/census.json'), sha(ROOT/'data/decisions.json')
    require(report['census_sha256'] == census_hash and report['ledger_sha256'] == ledger_hash,
            'frontier requires the final source-bound release summary')
    accepted, campaign_receipts = release.m9_records(rows)
    scoped, scoped_receipt = release.m9_structure_records(rows)
    scoped_by = {r['id']: r for r in scoped}
    require(len(scoped_by) == len(scoped), 'duplicate strongest M9 frontier scoped claim')
    stages = release.m9_stage_reports(rows, ledger)
    require(report['m9_campaigns'] == campaign_receipts,
            'frontier campaign receipts differ from the final release')
    require(report.get('m9_structure_only_receipt') == scoped_receipt,
            'frontier structure-only receipt differs from the final release')
    new_negatives = {r['id']: r['certificate'] for r in ledger if r['m'] == 9 and r['status'] == 'excluded'}
    require(new_negatives == {r['id']: r['certificate'] for r in accepted},
            'frontier ledger exclusions differ from replayed M9 proofs')
    old_audit = audit_historical(save=True)
    historical = json.loads((ROOT/HISTORICAL_COVERAGE).read_text())
    old_ids = [e['id'] for e in historical['cases']]
    unresolved = [r for r in ledger if r['status'] == 'unresolved']
    require([r['id'] for r in unresolved if r['m'] <= 8] == old_ids,
            'historical unresolved frontier changed')
    by_id = {r['id']: r for r in rows}
    new = [r for r in unresolved if r['m'] == 9]
    new_ids = {r['id'] for r in new}
    observations = {rid: [] for rid in new_ids}
    attempts_sources = {}
    for campaign in ('classification', 'advanced'):
        path = ROOT/'verification/m9'/campaign/'attempts.jsonl'
        attempts_sources[str(path.relative_to(ROOT))] = sha(path)
        for line in path.read_text().splitlines():
            record = json.loads(line)
            if record['id'] in new_ids:
                require(record['status'] != 'excluded', 'unresolved frontier contains an accepted exclusion')
                observations[record['id']].append(dict(campaign=campaign, stage=record['stage'],
                    status=record['status'], diagnostic=record.get('diagnostic'),
                    interpretation='Recorded discovery outcome; no general reduction is inferred.'))
    cases = []
    for row in new:
        require(len(observations[row['id']]) == len(stages),
                'M9 survivor lacks a recorded outcome at every executed stage')
        cases.append(dict(id=row['id'], multiplicity=9, categorical_status='unresolved',
            existence=row['existence'], tensor_sha256=object_sha(by_id[row['id']]['N'], sort_keys=True),
            whole_ring_exclusion=False, general_reduction_status='not_established',
            frontier_reduction_claimed=False, mathematical_frontier_replay_performed=False,
            public_summary='Recorded multiplicity-nine searches leave this ring unresolved. No additional structural frontier reduction is asserted.',
            scope='No inherited spherical, pseudo-unitary or Galois reduction is claimed for this new tensor.',
            observations=observations[row['id']]))
        if row['id'] in scoped_by:
            require(row['existence'] == scoped_existence(scoped_by[row['id']]),
                    'scoped M9 frontier claim does not match the five existence columns')
            cases[-1].update(scoped_nonexistence=scoped_evidence(scoped_by[row['id']], scoped_receipt),
                public_summary=scoped_summary(scoped_by[row['id']]),
                scope='Scoped nonexistence only. No general exclusion or inherited spherical or Galois reduction is claimed.')
        if row['id'] == 'R6_9_3748':
            require(all(value == 'unknown' for value in row['existence'].values()),
                    'braided obstruction must not change the five existence columns')
            cases[-1].update(braided_existence='no',
                braided_nonexistence=braided_evidence(by_id[row['id']]['N']),
                public_summary=BRAIDED_SUMMARY,
                scope='Braided nonexistence only; all five recorded categorical existence questions remain open.')
    inputs = dict(schema='rank6-m9-frontier-inputs/v1', source_census='data/census.json',
        source_census_sha256=census_hash, input_ledger='data/decisions.json', input_ledger_sha256=ledger_hash,
        input_count=len(new), ids=[r['id'] for r in new],
        tensors=[dict(id=r['id'], N=by_id[r['id']]['N'], tensor_sha256=object_sha(by_id[r['id']]['N'], sort_keys=True)) for r in new],
        scope='Exact final unresolved multiplicity-nine tensors; identities and search outcomes only.')
    write(ROOT/INPUTS, inputs)
    extension = dict(schema='rank6-m9-frontier-coverage/v1', input_manifest=INPUTS,
        input_manifest_sha256=sha(ROOT/INPUTS), census_sha256=census_hash, ledger_sha256=ledger_hash,
        historical_coverage=HISTORICAL_COVERAGE, historical_coverage_sha256=sha(ROOT/HISTORICAL_COVERAGE),
        historical_retained_audit=AUDIT, historical_retained_audit_sha256=sha(ROOT/AUDIT),
        campaign_receipts=campaign_receipts, structure_only_receipt=scoped_receipt,
        attempts_sources_sha256=attempts_sources,
        cases=cases, case_count=len(cases), mathematical_frontier_replay_performed=False,
        scope='Separate M9 unresolved ledger coverage. Historical reductions apply only to the two historical tensors. Search survival proves neither existence nor a structural reduction.')
    write(ROOT/EXTENSION, extension)
    summaries = public_cases(historical, cases)
    require([r['id'] for r in summaries] == [r['id'] for r in unresolved],
            'combined frontier omits or duplicates an unresolved ledger record')
    public = dict(schema='rank6-current-frontier/v2', census_sha256=census_hash, ledger_sha256=ledger_hash,
        historical_coverage_sha256=sha(ROOT/HISTORICAL_COVERAGE), extension_coverage_sha256=sha(ROOT/EXTENSION),
        scope='Every currently unresolved ring. Necessary historical reductions and new search outcomes are kept distinct; survival establishes neither existence nor exclusion.',
        cases=summaries)
    write(ROOT/'data/frontier_summary.json', public)
    return dict(passed=True, historical_cases=len(old_ids), m9_cases=len(cases), total_cases=len(summaries),
                historical_receipts_checked=old_audit['retained_receipt_count'],
                historical_mathematical_replay_performed=False, frontier_summary_sha256=sha(ROOT/'data/frontier_summary.json'))


def verify_current():
    """Check the generated combined frontier without refreshing any evidence."""
    import release
    summary = json.loads((ROOT/'data/frontier_summary.json').read_text())
    extension = json.loads((ROOT/EXTENSION).read_text())
    inputs = json.loads((ROOT/INPUTS).read_text())
    rows = json.loads((ROOT/'data/census.json').read_text())
    ledger = json.loads((ROOT/'data/decisions.json').read_text())
    census = {r['id']: r for r in rows}
    unresolved = [r for r in ledger if r['status'] == 'unresolved']
    new = [r for r in unresolved if r['m'] == 9]
    scoped, scoped_receipt = release.m9_structure_records(rows)
    scoped_by = {r['id']: r for r in scoped}
    require(len(scoped_by) == len(scoped), 'duplicate strongest M9 frontier scoped claim')
    require(summary['schema'] == 'rank6-current-frontier/v2'
            and summary['census_sha256'] == extension['census_sha256'] == inputs['source_census_sha256'] == sha(ROOT/'data/census.json')
            and summary['ledger_sha256'] == extension['ledger_sha256'] == inputs['input_ledger_sha256'] == sha(ROOT/'data/decisions.json'),
            'current frontier source or ledger binding changed')
    require(summary['extension_coverage_sha256'] == sha(ROOT/EXTENSION)
            and extension['input_manifest'] == INPUTS and extension['input_manifest_sha256'] == sha(ROOT/INPUTS)
            and summary['historical_coverage_sha256'] == extension['historical_coverage_sha256'] == sha(ROOT/HISTORICAL_COVERAGE)
            and extension['historical_retained_audit_sha256'] == sha(ROOT/AUDIT),
            'current frontier evidence artifact changed')
    require([r['id'] for r in summary['cases']] == [r['id'] for r in unresolved]
            and [r['id'] for r in extension['cases']] == inputs['ids'] == [r['id'] for r in new]
            and extension['case_count'] == inputs['input_count'] == len(new),
            'current frontier does not exactly cover unresolved ledger IDs')
    for case, row, tensor in zip(extension['cases'], new, inputs['tensors']):
        require(case['categorical_status'] == 'unresolved' and case['existence'] == row['existence']
                and case['whole_ring_exclusion'] is False and case['general_reduction_status'] == 'not_established'
                and case['frontier_reduction_claimed'] is False
                and case['mathematical_frontier_replay_performed'] is False,
                'M9 frontier makes an unsupported reduction or status claim')
        require(tensor['id'] == row['id'] and tensor['N'] == census[row['id']]['N']
                and tensor['tensor_sha256'] == case['tensor_sha256'] == object_sha(tensor['N'], sort_keys=True),
                'current frontier tensor binding changed')
        require(case.get('scoped_nonexistence') == (scoped_evidence(scoped_by[row['id']], scoped_receipt)
                if row['id'] in scoped_by else None), 'M9 frontier scoped nonexistence receipt changed')
        if row['id'] in scoped_by:
            require(row['existence'] == scoped_existence(scoped_by[row['id']])
                    and case['public_summary'] == scoped_summary(scoped_by[row['id']]),
                    'M9 frontier improperly promotes scoped nonexistence')
        expected_braided = braided_evidence(tensor['N']) if row['id'] == 'R6_9_3748' else None
        require(case.get('braided_nonexistence') == expected_braided
                and case.get('braided_existence') == ('no' if expected_braided else None),
                'M9 frontier braided obstruction changed')
        if expected_braided:
            require(all(value == 'unknown' for value in row['existence'].values())
                    and case['public_summary'] == BRAIDED_SUMMARY
                    and (ROOT/expected_braided['proof_path']).is_file(),
                    'M9 frontier improperly promotes braided nonexistence')
    require(len(inputs['tensors']) == len(new), 'current frontier tensor cardinality changed')
    for name, expected in extension['attempts_sources_sha256'].items():
        require(sha(ROOT/name) == expected, 'current frontier recorded attempts changed: '+name)
    current_release = json.loads((ROOT/'verification/release_summary.json').read_text())
    require(extension['campaign_receipts'] == current_release['m9_campaigns'],
            'current frontier campaign receipts differ from release')
    require(extension.get('structure_only_receipt') == current_release.get('m9_structure_only_receipt')
            == scoped_receipt, 'current frontier structure-only receipt differs from release')
    historical = json.loads((ROOT/HISTORICAL_COVERAGE).read_text())
    require(summary['cases'] == public_cases(historical, extension['cases']),
            'current public frontier summaries differ from their scoped coverage')
    require(json.loads((ROOT/AUDIT).read_text()) == audit_historical(save=False),
            'retained historical frontier audit is stale')
    return dict(passed=True, total_cases=len(unresolved), m9_cases=len(new),
                historical_mathematical_replay_performed=False)


def binding_controls():
    """Targeted temporary controls for the two new integrity mechanisms."""
    import copy
    import tempfile
    results = {}
    with tempfile.TemporaryDirectory(prefix='frontier-binding-controls-') as temporary:
        root = Path(temporary)
        old = [dict(id='old1', m=1, source_label='kept'), dict(id='old8', m=8, source_label=None)]
        expected = hashlib.sha256((json.dumps(old, separators=(',', ':'))+'\n').encode()).hexdigest()
        spec = dict(path='rows.json', rows=2, bound=8, counts={'1': 1, '8': 1}, sha256=expected)
        binding = HistoricalBinding.__new__(HistoricalBinding)
        binding.root, binding.prefixes, binding.source_adapters, binding.bindings = root, {}, {}, {}
        def check_rows(rows):
            (root/'rows.json').write_text(json.dumps(rows))
            return binding.prefix(spec)
        require(check_rows(old+[dict(id='new9', m=9)]) == old, 'valid historical prefix rejected')
        results['unchanged_history_with_appended_m9'] = 'accepted'
        for name, mutation in [
                ('changed_metadata', lambda r: r[0].update(source_label='changed')),
                ('missing_metadata', lambda r: r[1].pop('source_label')),
                ('reordered_history', lambda r: r.reverse()),
                ('missing_historical_row', lambda r: r.pop()),
                ('m9_inside_historical_prefix', lambda r: r[0].update(m=9)),
                ('historical_row_in_suffix', lambda r: r.append(copy.deepcopy(r[0])))]:
            rows = copy.deepcopy(old)
            mutation(rows)
            try:
                check_rows(rows)
            except ValueError as exc:
                require('historical prefix' in str(exc), 'unexpected prefix control failure')
                results[name] = 'rejected'
            else:
                raise ValueError('historical prefix mutation accepted: '+name)
        check_rows(old+[dict(id='new9', m=9)])
        (root/'rows.json').write_text('[]')
        require(not binding.check('rows.json', expected), 'post-audit prefix mutation accepted')
        results['prefix_changed_after_validation'] = 'rejected'
    spec = json.loads((ROOT/ADAPTER).read_text())['source_adapters']['software/frontier_replay.py']
    frozen = (ROOT/spec['frozen_source']).read_text()
    require(patched_driver(frozen) == (ROOT/'software/frontier_replay.py').read_text(),
            'approved driver patch differs')
    results['closed_declared_driver_patch'] = 'accepted'
    require(patched_driver(frozen) != (ROOT/'software/frontier_replay.py').read_text()+'\n# unapproved change\n',
            'extra driver change accepted')
    results['undeclared_driver_change'] = 'rejected'
    for name, source in [('missing_patch_anchor', frozen.replace(DRIVER_PATCH[0][0], 'def other(entry):')),
                         ('duplicate_patch_anchor', frozen+'\n'+DRIVER_PATCH[0][0]+'\n')]:
        try:
            patched_driver(source)
        except ValueError:
            results[name] = 'rejected'
        else:
            raise ValueError('ambiguous historical driver patch accepted')
    for scope, denied in [('pivotal', 4), ('spherical', 3), ('pseudo_unitary', 2)]:
        existence = scoped_existence({'structure': scope})
        require(existence['general'] == 'unknown' and sum(v == 'no' for v in existence.values()) == denied,
                'scoped frontier implications changed')
        results[scope+'_scope_keeps_general_unknown'] = 'accepted'
    try:
        scoped_existence({'structure': 'general'})
    except ValueError:
        results['scoped_claim_promoted_to_general'] = 'rejected'
    else:
        raise ValueError('frontier scoped claim promoted to a general exclusion')
    report = dict(passed=True, results=results, mathematical_replay_performed=False,
                  adapter_implementation_sha256=sha(Path(__file__)), adapter_manifest_sha256=sha(ROOT/ADAPTER))
    write(ROOT/'research/frontier/m9_adapter/controls.json', report)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--audit-only', action='store_true')
    mode.add_argument('--check-current', action='store_true')
    mode.add_argument('--controls', action='store_true')
    args = parser.parse_args()
    result = (audit_historical() if args.audit_only else verify_current() if args.check_current
              else binding_controls() if args.controls else build())
    if args.audit_only:
        result = {k: result[k] for k in ('passed', 'mode', 'protected_inventory_count', 'retained_receipt_count', 'mathematical_replay_performed')}
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
