"""Fast adversarial controls for historical and M9 release receipt gates.

Run with ``python -B software/m9_release_controls.py``. All campaign records,
proof objects and replay receipts used here are synthetic temporary fixtures.
This tests receipt validation; it does not claim to verify synthetic proofs.
"""
import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import time
from types import SimpleNamespace
from unittest.mock import patch

sys.dont_write_bytecode = True
import release

P = Path(__file__).resolve().parents[1]
STAGES = [('control_a', 'Control A', 1), ('control_b', 'Control B', 1)]


def digest(value, sort_keys=False):
    return hashlib.sha256(json.dumps(value, sort_keys=sort_keys,
                                    separators=(',', ':')).encode()).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def reject(call, expected):
    try:
        call()
    except ValueError as exc:
        require(expected in str(exc), 'unexpected rejection: '+str(exc))
        return {'rejected': True, 'reason': str(exc)}
    raise ValueError('negative control accepted: '+expected)


def rows_fixture():
    return [dict(id=f'R6_{m}_{i}', m=m, index=i, source_label=label,
                 dual=list(range(6)), commutative=True,
                 N=[[[int(a == 0 and b == c) + int(a == b == c == 1)*m
                      for c in range(6)] for b in range(6)] for a in range(6)])
            for m, i, label in [(1, 1, 'historical-A'), (8, 1, None),
                                (9, 1, None), (9, 2, None)]]


def historical_controls():
    rows = rows_fixture()
    old = rows[:2]
    summary = {'source': {'counts': {'1': 1, '8': 1}, 'tensors': 2},
               'census_sha256': hashlib.sha256(
                   (json.dumps(old, separators=(',', ':'))+'\n').encode()).hexdigest()}
    require(release.historical_cohort(rows, summary) == old, 'historical positive control failed')
    output = {'valid_appended_m9_rows': {'accepted': True, 'historical_rows': 2}}
    changed = {
        'missing_source_label': lambda r: r[0].pop('source_label'),
        'changed_source_label': lambda r: r[0].update(source_label='changed'),
        'null_source_label': lambda r: r[0].update(source_label=None),
        'missing_null_source_label': lambda r: r[1].pop('source_label'),
        'changed_identifier': lambda r: r[0].update(id='R6_1_99'),
        'changed_index': lambda r: r[0].update(index=99),
        'changed_commutativity': lambda r: r[0].update(commutative=False),
        'changed_duality': lambda r: r[0]['dual'].__setitem__(1, 2),
        'changed_tensor': lambda r: r[0]['N'][1][1].__setitem__(1, 7),
        'added_metadata': lambda r: r[0].update(extra_provenance='unrecorded'),
        'reordered_historical_rows': lambda r: r.__setitem__(slice(0, 2), list(reversed(r[:2]))),
    }
    for name, mutate in changed.items():
        bad = copy.deepcopy(rows)
        mutate(bad)
        output[name] = reject(lambda: release.historical_cohort(bad, summary),
                              'historical census rows changed')
    for name, mutate in {
        'missing_historical_row': lambda r: r.pop(0),
        'duplicate_historical_row': lambda r: r.append(copy.deepcopy(r[0])),
        'changed_historical_multiplicity': lambda r: r[0].update(m=8),
    }.items():
        bad = copy.deepcopy(rows)
        mutate(bad)
        output[name] = reject(lambda: release.historical_cohort(bad, summary),
                              'historical census multiplicities changed')
    bad_summary = copy.deepcopy(summary)
    bad_summary['census_sha256'] = '0'*64
    output['stale_historical_hash'] = reject(
        lambda: release.historical_cohort(rows, bad_summary), 'historical census rows changed')
    return output


def retained_historical_controls(root):
    """Exercise the retained receipt guard with real fixture files and hashes."""
    results = {}
    mismatch = 'frozen historical continuation exact-replay receipt does not match current proofs/source'

    def case(mutate=None, expected=None):
        rows = rows_fixture()
        historical = rows[:2]
        records = [dict(id=r['id'], m=r['m'], stage='continuation_control',
                        status='excluded', exact_checked=True,
                        certificate={'kind': 'synthetic_retained_receipt_control', 'witness': r['id']})
                   for r in historical]
        original = {'source': {'counts': {'1': 1, '8': 1}, 'tensors': 2}, 'excluded': 0,
                    'census_sha256': hashlib.sha256(
                        (json.dumps(historical, separators=(',', ':'))+'\n').encode()).hexdigest()}
        canonical = root/'certificates/classification.jsonl'
        canonical.parent.mkdir(parents=True, exist_ok=True)
        canonical.write_text('')
        paths = (root/'certificates/continuation_first.jsonl',
                 root/'certificates/continuation_second.jsonl')
        for path, record in zip(paths, records):
            path.write_text(json.dumps(record, separators=(',', ':'))+'\n')
        original_path = root/'verification/classification/summary.json'
        original_path.parent.mkdir(parents=True, exist_ok=True)
        receipt_path = root/'verification/m9/retained_m8_release_summary.json'
        receipt_path.parent.mkdir(parents=True, exist_ok=True)
        receipt = dict(census_sha256=original['census_sha256'],
                       original_certificates_sha256=release.file_digest(canonical),
                       continuation_certificates_exactly_verified=True,
                       continuation_files_sha256={str(p.relative_to(root)): release.file_digest(p) for p in paths},
                       continuation_excluded=len(records), continuation_ids=[r['id'] for r in records],
                       original_campaign_excluded=original['excluded'])
        state = dict(rows=rows, original=original, receipt=receipt, paths=paths,
                     canonical=canonical, records=records)
        if mutate is not None:
            mutate(state)
        original_path.write_text(json.dumps(original)+'\n')
        receipt_path.write_text(json.dumps(receipt)+'\n')
        with patch.object(release, 'P', root), patch.object(release, 'HISTORICAL_REPLAY', receipt_path), \
                patch.object(release, 'CONTINUATION_PATHS', paths), \
                patch.object(release, 'continuation_records', return_value=records) as mocked:
            call = lambda: release.retained_historical_continuation(rows)
            if expected is not None:
                return reject(call, expected)
            accepted, evidence = call()
            require(accepted == records and evidence['certificates'] == len(records),
                    'retained historical positive control returned incorrect records')
            require(evidence['receipt_sha256'] == release.file_digest(receipt_path)
                    and evidence['historical_census_sha256'] == original['census_sha256']
                    and evidence['certificate_files_sha256'] == receipt['continuation_files_sha256'],
                    'retained historical returned receipt bindings differ')
            require(mocked.call_count == 1 and mocked.call_args.args == (rows,)
                    and mocked.call_args.kwargs == {'verify_certificates': False},
                    'retained historical control attempted a fresh proof replay')
            return {'accepted': True, 'records': len(records), 'proof_files': len(paths),
                    'fresh_replay_requested': False}

    results['valid_retained_exact_receipt'] = case()
    mutations = [
        ('changed_historical_metadata', lambda s: s['rows'][0].update(source_label='changed'),
         'historical census rows changed'),
        ('changed_historical_summary_hash', lambda s: s['original'].update(census_sha256='0'*64),
         'historical census rows changed'),
        ('stale_receipt_census_hash', lambda s: s['receipt'].update(census_sha256='0'*64), mismatch),
        ('changed_continuation_file_bytes', lambda s: s['paths'][0].write_text(
            s['paths'][0].read_text()+'\n'), mismatch),
        ('changed_original_certificate_bytes', lambda s: s['canonical'].write_text('\n'), mismatch),
        ('stale_original_certificate_hash', lambda s:
            s['receipt'].update(original_certificates_sha256='0'*64), mismatch),
        ('false_exact_verified_flag', lambda s:
            s['receipt'].update(continuation_certificates_exactly_verified=False), mismatch),
        ('missing_exact_verified_flag', lambda s:
            s['receipt'].pop('continuation_certificates_exactly_verified'), mismatch),
        ('omitted_proof_file_entry', lambda s: s['receipt']['continuation_files_sha256'].pop(
            str(s['paths'][0].relative_to(root))), mismatch),
        ('missing_proof_file', lambda s: s['paths'][0].unlink(), mismatch),
        ('missing_ordered_ids_field', lambda s: s['receipt'].pop('continuation_ids'), mismatch),
        ('missing_ordered_id', lambda s: s['receipt']['continuation_ids'].pop(), mismatch),
        ('changed_ordered_id', lambda s:
            s['receipt']['continuation_ids'].__setitem__(0, 'R6_1_999'), mismatch),
        ('reversed_ordered_ids', lambda s: s['receipt']['continuation_ids'].reverse(), mismatch),
        ('changed_continuation_count', lambda s: s['receipt'].update(continuation_excluded=1), mismatch),
        ('changed_original_campaign_count', lambda s: s['receipt'].update(original_campaign_excluded=1), mismatch),
    ]
    for name, mutate, reason in mutations:
        results[name] = case(mutate, reason)
    return results


class Fixture:
    def __init__(self, root, advanced=False):
        self.root = root
        self.rows = rows_fixture()
        self.paths = (root/'certificates/m9_classification.jsonl',
                      root/'certificates/m9_advanced.jsonl')
        self.files = {}
        self.source_hash = hashlib.sha256(
            (json.dumps(self.rows, separators=(',', ':'))+'\n').encode()).hexdigest()
        self.standard = [self.record(self.rows[2], 'control_a')]
        self.advanced = [self.record(self.rows[3], 'advanced_control')] if advanced else []
        self.rebuild()

    def record(self, row, stage):
        return dict(id=row['id'], m=row['m'], stage=stage, status='excluded', exact_checked=True,
                    census_sha256=self.source_hash, tensor_sha256=digest(row['N']),
                    certificate={'kind': 'synthetic_release_receipt_control', 'witness': row['id']})

    def replay(self, rec):
        return dict(id=rec['id'], m=rec['m'], passed=True, optimized_python=True,
                    optimizer_disabled=True, optimizer_used=False,
                    tensor_sha256=rec['tensor_sha256'],
                    certificate_sha256=release.certificate_digest(rec['certificate']))

    def rebuild(self):
        """Rebind outer counts/hashes, useful for isolating semantic failures."""
        cohort = [r for r in self.rows if r['m'] == 9]
        excluded = {r['id'] for r in self.standard}
        residual = [r for r in cohort if r['id'] not in excluded]
        cert_hashes = [hashlib.sha256(self.lines(rs).encode()).hexdigest()
                       for rs in (self.standard, self.advanced)]
        self.files = {
            'classification/summary.json': dict(complete=True, census_sha256=self.source_hash,
                certificates_sha256=cert_hashes[0], excluded=len(self.standard),
                completed_stages=len(STAGES), stages_total=len(STAGES),
                input_count=len(cohort), input_sha256=digest(cohort),
                unresolved=len(residual), unresolved_ids=[r['id'] for r in residual]),
            'replay/optimized_summary.json': dict(complete=True, failed=[], passed=len(self.standard),
                completed=len(self.standard), input_count=len(self.standard), optimized_python=True,
                optimizer_disabled=True, census_sha256=self.source_hash,
                certificate_file_sha256=cert_hashes[0]),
            'replay/optimized.jsonl': [self.replay(r) for r in self.standard],
            'advanced/summary.json': dict(complete=True, census_sha256=self.source_hash,
                certificates_sha256=cert_hashes[1], excluded=len(self.advanced),
                input_ids=[r['id'] for r in residual], input_count=len(residual),
                input_sha256=digest(residual, sort_keys=True), requested_stages=['advanced_control'],
                unresolved_ids=[r['id'] for r in residual if r['id'] not in {c['id'] for c in self.advanced}]),
            'advanced/replay_optimized.json': dict(complete=True, passed=True, count=len(self.advanced),
                optimized_python=True, optimizer_disabled=True, census_sha256=self.source_hash,
                certificates_sha256=cert_hashes[1], results=[self.replay(r) for r in self.advanced]),
        }
        self.files['advanced/input_manifest.json'] = {
            k: self.files['advanced/summary.json'][k]
            for k in ('census_sha256', 'input_count', 'input_ids', 'input_sha256')}

    @staticmethod
    def lines(records):
        return ''.join(json.dumps(r, separators=(',', ':'))+'\n' for r in records)

    def write(self):
        census = self.root/'data/census.json'
        census.parent.mkdir(parents=True, exist_ok=True)
        census.write_text(json.dumps(self.rows, separators=(',', ':'))+'\n')
        for path, records in zip(self.paths, (self.standard, self.advanced)):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(self.lines(records))
        for name, value in self.files.items():
            path = self.root/'verification/m9'/name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(self.lines(value) if name.endswith('.jsonl') else json.dumps(value)+'\n')

    def run(self):
        self.write()
        with patch.object(release, 'P', self.root), patch.object(release, 'M9_PATHS', self.paths), \
                patch.dict(sys.modules, {'classify_m9': SimpleNamespace(STAGES=STAGES)}):
            return release.m9_records(self.rows)


def m9_controls(root):
    results = {}
    for advanced, label, count in [(False, 'complete_standard_and_empty_advanced', 1),
                                   (True, 'complete_disjoint_standard_and_advanced', 2)]:
        fixture = Fixture(root, advanced)
        records, receipts = fixture.run()
        require(len(records) == count and len(receipts) == 2, 'positive release fixture failed')
        results[label] = {'accepted': True, 'records': count, 'campaign_receipts': len(receipts)}

    def test(name, mutate, reason, advanced=False):
        fixture = Fixture(root, advanced)
        mutate(fixture)
        results[name] = reject(fixture.run, reason)

    for kind in ('classification', 'advanced'):
        reason = 'M9 campaign is unfinished or bound to a different census: '+kind
        for field, value, label in [('complete', False, 'incomplete_summary'),
                                    ('census_sha256', '0'*64, 'stale_census_hash')]:
            test(kind+'_'+label,
                 lambda f, k=kind, a=field, v=value: f.files[k+'/summary.json'].__setitem__(a, v), reason)
        for field, value, label in [('certificates_sha256', '0'*64, 'stale_certificates_hash'),
                                    ('excluded', 999, 'incorrect_certificate_count')]:
            test(kind+'_'+label,
                 lambda f, k=kind, a=field, v=value: f.files[k+'/summary.json'].__setitem__(a, v),
                 'M9 certificate file/count changed: '+kind)
    for field, value in [('completed_stages', 1), ('stages_total', 1),
                         ('input_count', 1), ('input_sha256', '0'*64)]:
        test('standard_'+field, lambda f, k=field, v=value:
             f.files['classification/summary.json'].__setitem__(k, v),
             'M9 original campaign input/stage mismatch')
    test('standard_residual_ids', lambda f:
         f.files['classification/summary.json'].__setitem__('unresolved_ids', []),
         'M9 original campaign residual mismatch')

    for file, prefix, reason in [
            ('replay/optimized_summary.json', 'standard', 'M9 independent optimized replay is incomplete or stale'),
            ('advanced/replay_optimized.json', 'advanced', 'M9 advanced independent optimized replay is incomplete or stale')]:
        fields = [('complete', False), ('optimized_python', False), ('census_sha256', '0'*64)]
        fields += ([('failed', ['R6_9_1']), ('passed', 0), ('completed', 0), ('input_count', 0),
                    ('optimizer_disabled', False), ('certificate_file_sha256', '0'*64)]
                   if prefix == 'standard' else [('passed', False), ('count', 1),
                    ('optimizer_disabled', False), ('certificates_sha256', '0'*64)])
        for field, value in fields:
            test(prefix+'_replay_'+field,
                 lambda f, p=file, k=field, v=value: f.files[p].__setitem__(k, v), reason)
    for field, value in [('passed', False), ('m', 8), ('optimized_python', False),
                         ('certificate_sha256', '0'*64)]:
        test('standard_replay_record_'+field, lambda f, k=field, v=value:
             f.files['replay/optimized.jsonl'][0].__setitem__(k, v), 'M9 replay certificate mismatch')
    test('missing_replay_id', lambda f: f.files['replay/optimized.jsonl'].clear(),
         'M9 independent replay does not cover exactly the accepted IDs')
    test('duplicate_replay_id', lambda f: f.files['replay/optimized.jsonl'].append(
         copy.deepcopy(f.files['replay/optimized.jsonl'][0])),
         'M9 independent replay does not cover exactly the accepted IDs')
    test('standard_replay_record_optimizer_disabled', lambda f:
         f.files['replay/optimized.jsonl'][0].__setitem__('optimizer_disabled', False),
         'M9 exact replay did not disable numerical optimization')
    test('duplicate_m9_census_id', lambda f: f.rows.append(copy.deepcopy(f.rows[2])),
         'duplicate multiplicity-nine census identifier')

    def mutate_certificate(f):
        old_replay = copy.deepcopy(f.files['replay/optimized.jsonl'])
        f.standard[0]['certificate']['witness'] = 'mutated after replay'
        f.rebuild()
        f.files['replay/optimized.jsonl'] = old_replay
    test('mutated_proof_with_rebound_outer_hashes', mutate_certificate, 'M9 replay certificate mismatch')
    def swapped_replay_hashes(f):
        f.standard.append(f.record(f.rows[3], 'control_b'))
        f.rebuild()
        results = f.files['replay/optimized.jsonl']
        results[0]['certificate_sha256'], results[1]['certificate_sha256'] = (
            results[1]['certificate_sha256'], results[0]['certificate_sha256'])
    test('swapped_per_id_replay_proof_hashes', swapped_replay_hashes, 'M9 replay certificate mismatch')

    def duplicate_certificate(f):
        f.standard.append(copy.deepcopy(f.standard[0]))
        f.rebuild()
        f.files['replay/optimized.jsonl'].pop()
    test('duplicate_standard_certificate_id', duplicate_certificate, 'invalid or duplicate M9 negative')

    def overlap(f):
        f.advanced = [copy.deepcopy(f.standard[0])]
        f.rebuild()
    test('overlap_standard_advanced_id', overlap, 'invalid or duplicate M9 negative')

    def foreign(f):
        f.standard = [f.record(f.rows[1], 'control_a')]
        f.standard[0]['m'] = 9
        f.rebuild()
    test('foreign_lower_multiplicity_id', foreign, 'invalid or duplicate M9 negative')
    for field, value in [('m', 8), ('exact_checked', False), ('status', 'unresolved'), ('stage', '')]:
        def mutate(f, k=field, v=value):
            f.standard[0][k] = v
            f.rebuild()
        test('malformed_standard_'+field, mutate, 'invalid or duplicate M9 negative')
    def stale_record_source(f):
        f.standard[0]['census_sha256'] = '0'*64
        f.rebuild()
    test('stale_per_record_source', stale_record_source, 'M9 per-record source mismatch')

    for name, field, value, reason in [
            ('missing_advanced_input', 'input_ids', [], 'M9 advanced input does not match'),
            ('duplicate_advanced_input', 'input_ids', ['R6_9_2', 'R6_9_2'], 'M9 advanced input does not match'),
            ('wrong_advanced_input_count', 'input_count', 0, 'M9 advanced input tensor hash mismatch'),
            ('stale_advanced_input_hash', 'input_sha256', '0'*64, 'M9 advanced input tensor hash mismatch'),
            ('wrong_advanced_residual', 'unresolved_ids', [], 'M9 advanced campaign residual mismatch')]:
        test(name, lambda f, k=field, v=value: f.files['advanced/summary.json'].__setitem__(k, v), reason)
    test('stale_advanced_manifest', lambda f:
         f.files['advanced/input_manifest.json'].__setitem__('input_sha256', '0'*64),
         'M9 advanced input manifest mismatch')
    for field, value in [('passed', False), ('m', 8), ('optimized_python', False),
                         ('certificate_sha256', '0'*64)]:
        test('advanced_replay_record_'+field, lambda f, k=field, v=value:
             f.files['advanced/replay_optimized.json']['results'][0].__setitem__(k, v),
             'M9 replay certificate mismatch', advanced=True)
    test('advanced_replay_tensor_hash', lambda f:
         f.files['advanced/replay_optimized.json']['results'][0].__setitem__('tensor_sha256', '0'*64),
         'M9 advanced tensor mismatch', advanced=True)
    test('advanced_replay_record_optimizer_used', lambda f:
         f.files['advanced/replay_optimized.json']['results'][0].__setitem__('optimizer_used', True),
         'M9 exact replay did not disable numerical optimization', advanced=True)
    def mutate_tensor_hash(f):
        f.advanced[0]['tensor_sha256'] = '0'*64
        f.rebuild()
    test('advanced_certificate_tensor_hash', mutate_tensor_hash, 'M9 advanced tensor mismatch', advanced=True)
    return results


def scoped_claim_controls(root):
    """Use a real scoped proof/tensor inside separately rebound receipt fixtures."""
    actual = json.loads((P/'certificates/m9_structure_only.json').read_text())[0]
    actual_row = next(r for r in json.loads((P/'data/census.json').read_text()) if r['id'] == actual['id'])
    actual_receipt = json.loads((P/'verification/m9/structure_replay_optimized.json').read_text())
    actual_result = next(r for r in actual_receipt['results'] if r['id'] == actual['id'])
    output = {}

    def case(mutate=None, expected=None):
        fixture = Fixture(root)
        fixture.rows = [copy.deepcopy(actual_row)]
        fixture.source_hash = hashlib.sha256(
            (json.dumps(fixture.rows, separators=(',', ':'))+'\n').encode()).hexdigest()
        fixture.standard = []
        fixture.advanced = []
        fixture.rebuild()
        fixture.write()
        records = [copy.deepcopy(actual)]
        receipt = dict(complete=True, passed=True, optimized_python=True, optimizer_disabled=True,
                       count=1, census_sha256=fixture.source_hash, results=[copy.deepcopy(actual_result)])
        state = dict(records=records, receipt=receipt)
        if mutate is not None:
            mutate(state)
        proof_path = root/'certificates/m9_structure_only.json'
        proof_path.write_text(json.dumps(records, separators=(',', ':'))+'\n')
        receipt['certificates_sha256'] = release.file_digest(proof_path)
        receipt_path = root/'verification/m9/structure_replay_optimized.json'
        receipt_path.write_text(json.dumps(receipt)+'\n')
        with patch.object(release, 'P', root):
            call = lambda: release.m9_structure_records(fixture.rows)
            if expected is not None:
                return reject(call, expected)
            retained, bound = call()
        require(retained == records and bound['count'] == 1 and bound['ids'] == [actual['id']],
                'scoped positive receipt fixture failed')
        general, campaigns = fixture.run()
        require(general == [] and len(campaigns) == 2,
                'scoped proof was incorrectly added to the general M9 proof union')
        return dict(accepted=True, scoped_records=1, general_records=0,
                    declared_structure=actual['structure'],
                    original_tensor_sha256=actual['tensor_sha256'],
                    original_certificate_sha256=release.certificate_digest(actual['certificate']),
                    scope='Real tensor/proof with temporary receipt hashes; no new mathematical replay.')

    output['valid_scoped_receipt_kept_out_of_general_union'] = case()
    incomplete = 'M9 structure-only exact-replay receipt is incomplete or stale'
    mismatch = 'M9 structure-only proof/tensor replay mismatch'
    for field, value in [('complete', False), ('passed', False), ('optimized_python', False),
                         ('optimizer_disabled', False), ('count', 0), ('census_sha256', '0'*64)]:
        output['scoped_receipt_'+field] = case(
            lambda s, k=field, v=value: s['receipt'].__setitem__(k, v), incomplete)
    output['scoped_claim_promoted_to_general'] = case(
        lambda s: s['records'][0].update(structure='general'), 'invalid M9 structure-only claim')
    output['scoped_declared_scope_differs_from_replay'] = case(
        lambda s: s['records'][0].update(structure='spherical' if actual['structure'] == 'pivotal' else 'pivotal'),
        mismatch)
    def duplicate_scoped_claim(state):
        state['records'].append(copy.deepcopy(state['records'][0]))
        state['receipt']['count'] = 2
    output['duplicate_strongest_scoped_claim'] = case(duplicate_scoped_claim, 'invalid M9 structure-only claim')
    output['scoped_proof_mutated_after_replay'] = case(
        lambda s: s['records'][0]['certificate'].update(control_mutation=True), mismatch)
    output['scoped_record_tensor_hash'] = case(
        lambda s: s['records'][0].update(tensor_sha256='0'*64), mismatch)
    for field, value in [('tensor_sha256', '0'*64), ('certificate_sha256', '0'*64),
                         ('passed', False), ('m', 8), ('structure', 'general')]:
        output['scoped_replay_record_'+field] = case(
            lambda s, k=field, v=value: s['receipt']['results'][0].__setitem__(k, v), mismatch)
    output['scoped_replay_missing_id'] = case(
        lambda s: s['receipt']['results'].clear(), 'M9 structure-only replay coverage mismatch')
    return output


def main():
    start = time.monotonic()
    release_source_hash = release.file_digest(Path(release.__file__))
    historical = historical_controls()
    with tempfile.TemporaryDirectory(prefix='m9-release-controls-') as temporary:
        current = m9_controls(Path(temporary))
        retained = retained_historical_controls(Path(temporary)/'retained-history')
        scoped = scoped_claim_controls(Path(temporary)/'scoped-claims')
    require(release_source_hash == release.file_digest(Path(release.__file__)),
            'release source changed during controls; rerun on stable source')
    report = {'passed': True, 'optimized_python': not __debug__,
              'historical_controls': historical, 'm9_receipt_controls': current,
              'retained_historical_receipt_controls': retained,
              'scoped_nonexistence_receipt_controls': scoped,
              'rejected_mutations': sum(bool(r.get('rejected')) for r in [*historical.values(), *current.values(), *retained.values(), *scoped.values()]),
              'positive_fixtures': sum(bool(r.get('accepted')) for r in [*historical.values(), *current.values(), *retained.values(), *scoped.values()]),
              'release_source_sha256': release_source_hash,
              'controls_source_sha256': release.file_digest(Path(__file__)),
              'mock_standard_stage_count': len(STAGES),
              'scope': 'Synthetic isolated receipt controls; no mathematical proof replay or real census mutation.',
              'seconds': time.monotonic()-start}
    (P/'verification/m9/release_controls.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
