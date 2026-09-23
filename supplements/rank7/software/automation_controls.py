"""Lightweight adversarial controls for source import and bounded discovery.

Only temporary source fixtures and mocked subprocesses are used. No census,
Gram enumeration, certificate discovery or numerical optimization is run.
"""
import collections
import copy
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import time
import traceback
from unittest.mock import patch

import sympy as s

import advanced_criteria
import check
import classify
from exact import VerificationError, require
import import_repository
import integer_gram

ROOT = Path(__file__).resolve().parents[1]


def run():
    start = time.monotonic()
    controls = []

    def rejects(name, exception, callback):
        try:
            callback()
        except exception:
            controls.append(name)
        else:
            raise VerificationError(f'{name}: invalid input was accepted')

    # Two existing tensors suffice for all source-interface mutations. Every
    # write is confined to the temporary fixture, never the supplied census.
    sample = json.loads((ROOT/'data/census.json').read_text())[:2]
    with tempfile.TemporaryDirectory() as directory:
        fixture = Path(directory)
        (fixture/'data').mkdir()
        (fixture/'provenance').mkdir()
        source = fixture/'data/rank6_tables.txt.gz'
        raw = ''.join(json.dumps(row['N'])+'\n' for row in sample).encode()
        source.write_bytes(gzip.compress(raw, mtime=0))
        pristine = source.read_bytes()
        metadata = {
            'sha256': hashlib.sha256(pristine).hexdigest(),
            'counts': dict(collections.Counter(row['m'] for row in sample)),
            'tensors': len(sample), 'source_commit': 'temporary-control-fixture',
        }
        (fixture/'provenance/repository_source.json').write_text(json.dumps(metadata))
        with patch.object(import_repository, 'P', fixture):
            report = import_repository.verify_source(sample)
            require(report['tensors'] == 2 and not report['independent_census_recomputed'],
                    'valid source fixture failed')
            controls.append('valid_source_fixture')
            source.write_bytes(pristine+b'tampered')
            rejects('source_digest_tampering', ValueError,
                    lambda: import_repository.verify_source(sample))
            source.write_bytes(pristine)
            duplicate = copy.deepcopy(sample)
            duplicate[1]['id'] = duplicate[0]['id']
            rejects('duplicate_tensor_identifier', ValueError,
                    lambda: import_repository.verify_source(duplicate))
            changed = copy.deepcopy(sample)
            changed[0]['N'][1][1][1] += 1
            rejects('changed_source_representative', ValueError,
                    lambda: import_repository.verify_source(changed))
            changed = copy.deepcopy(sample)
            changed[0]['m'] += 1
            rejects('changed_multiplicity_metadata', ValueError,
                    lambda: import_repository.verify_source(changed))

    row = sample[0]
    fake_certificate = {'kind': 'mocked_control_witness'}

    def task(stage='rank_two', cached=None, positive=False):
        return stage, 'control fixture', 1, row, cached, positive

    def check_outcome(name, result, status):
        require(result['status'] == status, name+': wrong outcome')
        require('seconds' in result and result['seconds'] >= 0,
                name+': elapsed time missing')
        if status != 'excluded':
            require('certificate' not in result and not result.get('exact_checked'),
                    name+': incomplete work was promoted to exclusion')
        controls.append(name)

    # Suppress actual POSIX timers while checking the worker's handling of
    # each real timeout exception and of invalid exact certificates.
    with patch.object(classify.signal, 'signal'), patch.object(classify.signal, 'alarm') as alarm:
        timeouts = (
            classify.DiscoveryBudget('mock discovery deadline'),
            TimeoutError('mock algorithm deadline'),
            subprocess.TimeoutExpired(['mock-tool'], 1),
            integer_gram.GramSearchBudget(1, nodes=12, frames=2),
        )
        for error in timeouts:
            with patch.object(classify, 'discover', side_effect=error):
                result = classify.worker(task())
            check_outcome('discovery_'+type(error).__name__, result, 'budget_exhausted')
            require(alarm.call_args.args == (0,), 'worker did not cancel its timer')
        with patch.object(classify, 'discover', side_effect=ValueError('unexpected failure')):
            check_outcome('unexpected_discovery_exception', classify.worker(task()), 'error')
        with patch.object(classify, 'discover', return_value=fake_certificate), \
             patch.object(check, 'verify', side_effect=VerificationError('invalid witness')):
            check_outcome('false_certificate_rejected', classify.worker(task()), 'error')
        with patch.object(classify, 'discover', return_value=fake_certificate), \
             patch.object(check, 'verify', side_effect=TimeoutError('checker deadline')):
            check_outcome('incomplete_certificate_check', classify.worker(task()), 'budget_exhausted')
        with patch.object(classify, 'discover', return_value=fake_certificate), \
             patch.object(check, 'verify') as verifier:
            result = classify.worker(task())
            verifier.assert_called_once_with(row['N'], fake_certificate)
            check_outcome('exact_checker_required_for_exclusion', result, 'excluded')
            require(result['exact_checked'] is True, 'successful exact check not recorded')

        import scipy.optimize
        original_lp, original_milp = scipy.optimize.linprog, scipy.optimize.milp
        with patch.object(classify, 'discover', return_value=fake_certificate), \
             patch.object(check, 'verify', side_effect=lambda *_: scipy.optimize.linprog([1])):
            check_outcome('floating_optimizer_forbidden_in_checker', classify.worker(task()), 'error')
        require(scipy.optimize.linprog is original_lp and scipy.optimize.milp is original_milp,
                'worker failed to restore discovery optimizers')

        for stage in ('dimension_order', 'character', 'tensor_rotation', 'modular'):
            eligible = {'eligible': False, 'reason': 'deliberately outside criterion scope'}
            with patch.object(advanced_criteria, 'eligibility', return_value=eligible), \
                 patch.object(advanced_criteria, 'general_certificate') as generator, \
                 patch.object(check, 'verify') as verifier:
                result = classify.worker(task(stage, cached=fake_certificate))
                check_outcome(stage+'_ineligible_not_excluded', result, 'ineligible')
                generator.assert_not_called()
                verifier.assert_not_called()
            with patch.object(advanced_criteria, 'eligibility') as eligibility, \
                 patch.object(advanced_criteria, 'general_certificate') as generator:
                result = classify.worker(task(stage, positive=True))
                check_outcome(stage+'_positive_skips_negative_search', result, 'survives')
                eligibility.assert_not_called()
                generator.assert_not_called()
        with patch.object(advanced_criteria, 'eligibility', return_value={'eligible': True}), \
             patch.object(advanced_criteria, 'general_certificate', return_value=fake_certificate) as generator, \
             patch.object(check, 'verify') as verifier:
            result = classify.worker(task('character'))
            check_outcome('eligible_advanced_witness_checked', result, 'excluded')
            generator.assert_called_once()
            verifier.assert_called_once_with(row['N'], fake_certificate)

    # The tiny Gram equation is x=1. All subprocess results are fixtures: no
    # compiler or enumerator can be launched inside these patched calls.
    Q = s.Matrix([[1]])
    columns = [((1,), 0)]

    def frames_result(code=0, stdout='1\n', stderr='complete 1 nodes 1 frames 1\n', exception=None):
        completed = subprocess.CompletedProcess(['mock-gram'], code, stdout, stderr)
        with patch.object(Path, 'exists', return_value=True), \
             patch.object(integer_gram.os, 'access', return_value=True), \
             patch.object(integer_gram.subprocess, 'run', return_value=completed,
                          side_effect=exception) as process:
            result = integer_gram.frames(Q, columns, seconds=1)
            process.assert_called_once()
            return result

    require(frames_result() == [(1,)], 'valid complete Gram fixture failed')
    controls.append('complete_Gram_result_accepted')
    rejects('Gram_incomplete_returncode3', integer_gram.GramSearchBudget,
            lambda: frames_result(3, '1\n', 'complete 0 nodes 12 frames 1\n'))
    rejects('Gram_process_timeout', integer_gram.GramSearchBudget,
            lambda: frames_result(exception=subprocess.TimeoutExpired(['mock-gram'], 6)))
    for name, code, stdout, stderr in (
        ('Gram_unexpected_returncode2', 2, '', 'complete 0 nodes 12 frames 0\n'),
        ('Gram_malformed_status', 0, '1\n', 'not a completion report\n'),
        ('Gram_false_success_incomplete', 0, '1\n', 'complete 0 nodes 12 frames 1\n'),
        ('Gram_false_timeout_complete', 3, '1\n', 'complete 1 nodes 12 frames 1\n'),
        ('Gram_invalid_equation_solution', 0, '2\n', 'complete 1 nodes 12 frames 1\n'),
    ):
        rejects(name, VerificationError,
                lambda code=code, stdout=stdout, stderr=stderr: frames_result(code, stdout, stderr))
    return dict(passed=True, optimized_python=not __debug__, seconds=time.monotonic()-start,
                controls=len(controls), checked=controls, census_recomputed=False,
                subprocesses_mocked=True, real_data_modified=False)


if __name__ == '__main__':
    destination = ROOT/'verification/current'
    destination.mkdir(parents=True, exist_ok=True)
    mode = 'normal' if __debug__ else 'optimized'
    try:
        result = run()
    except Exception as error:
        result = dict(passed=False, optimized_python=not __debug__, error=str(error),
                      traceback=traceback.format_exc())
    (destination/f'automation_controls_{mode}.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result['passed'] else 1)
