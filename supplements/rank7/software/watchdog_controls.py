"""Real, tiny subprocess controls for the classification process watchdog.

Temporary fixtures exercise transport and process termination only. No tensor
enumeration, certificate discovery, numerical optimizer, or census edit occurs.
Mathematical certificate checking is covered separately by automation_controls.
"""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import traceback
from unittest.mock import patch

import classify
from exact import require

ROOT = Path(__file__).resolve().parents[1]

FIXTURE = r'''
import ctypes, json, os, pathlib, signal, subprocess, sys
case, marker = sys.argv[1:]
task = json.load(sys.stdin)
stage, label, budget, row, cached, positive = task
result = dict(id=row['id'], m=row['m'], stage=stage,
              status='survives', seconds=0.0)
if case == 'exit':
    print(json.dumps(result), flush=True)
    print('deliberate fixture failure', file=sys.stderr, flush=True)
    sys.exit(7)
if case == 'malformed':
    print('{not json'); sys.exit(0)
if case == 'array':
    print('[]'); sys.exit(0)
if case == 'null':
    print('null'); sys.exit(0)
if case == 'unknown_status': result['status'] = 'unrecognized'
if case == 'wrong_id': result['id'] += '_wrong'
if case == 'wrong_m': result['m'] += 1
if case == 'wrong_stage': result['stage'] += '_wrong'
if case in ('excluded', 'unchecked', 'missing_certificate', 'blocking'):
    result.update(status='excluded', certificate={'kind':'transport_fixture'},
                  exact_checked=True)
if case == 'unchecked': result['exact_checked'] = False
if case == 'missing_certificate': del result['certificate']
if case == 'blocking':
    signal.signal(signal.SIGALRM, signal.SIG_IGN)
    signal.alarm(1)
    child = subprocess.Popen([sys.executable, '-c',
        'import ctypes; ctypes.CDLL(None).sleep(4)'])
    pathlib.Path(marker).write_text(json.dumps([os.getpid(), child.pid]))
    print(json.dumps(result), flush=True)
    ctypes.CDLL(None).sleep(4)
else:
    print(json.dumps(result), flush=True)
'''


def run():
    started = time.monotonic()
    controls = []
    real_popen = subprocess.Popen
    task = ('general_induction', 'watchdog control', 1,
            {'id': 'temporary_watchdog_fixture', 'm': 8}, None, False)
    with tempfile.TemporaryDirectory() as directory:
        fixture = Path(directory)/'worker_fixture.py'
        marker = Path(directory)/'processes.json'
        fixture.write_text(FIXTURE)

        def exercise(case, expected):
            launches = []

            def launch(command, *args, **kwargs):
                launches.append((command, kwargs))
                require(command[-1] == '--worker', 'watchdog omitted worker mode')
                require(('-O' in command) == (not __debug__),
                        'watchdog changed Python optimization mode')
                require(kwargs.get('start_new_session') is True,
                        'watchdog omitted the independent process group')
                command = [sys.executable]+([] if __debug__ else ['-O'])+[
                    str(fixture), case, str(marker)]
                return real_popen(command, *args, **kwargs)

            with patch.object(classify.subprocess, 'Popen', side_effect=launch):
                result = classify.hard_worker(task)
            require(len(launches) == 1, 'watchdog unexpectedly retried a task')
            require(result['status'] == expected,
                    case+': wrong classification outcome')
            require(result.get('id') == task[3]['id'] and result.get('m') == 8
                    and result.get('stage') == task[0],
                    case+': output identity was not preserved')
            if expected != 'excluded':
                require('certificate' not in result and not result.get('exact_checked'),
                        case+': incomplete output was accepted as a proof')
            controls.append(case)
            return result

        valid = exercise('valid', 'survives')
        require(valid['hard_deadline_seconds'] == 1 and
                valid['process_wall_seconds'] >= 0,
                'successful watchdog timing metadata missing')
        controls.append('deadline_and_timing_metadata')
        exercise('excluded', 'excluded')
        failed = exercise('exit', 'error')
        require(failed['returncode'] == 7 and 'fixture failure' in failed['stderr'],
                'unexpected process failure lost its diagnostics')
        controls.append('unexpected_exit_diagnostics')
        for case in ('malformed', 'array', 'null', 'unknown_status', 'wrong_id',
                     'wrong_m', 'wrong_stage', 'unchecked', 'missing_certificate'):
            exercise(case, 'error')

        blocked = exercise('blocking', 'budget_exhausted')
        require(blocked['budget']['type'] == 'hard_process_deadline',
                'native-like blockage did not reach the independent watchdog')
        require(0.9 <= blocked['seconds'] < 3.5,
                'the one-second watchdog failed to bound real wall time')
        controls.append('blocking_native_call_bounded')
        require(marker.exists(), 'blocking fixture did not start its descendant')
        processes = json.loads(marker.read_text())
        require(len(processes) == 2, 'missing parent or descendant process identity')
        for pid in processes:
            statefile = Path(f'/proc/{pid}/stat')
            if statefile.exists():
                state = statefile.read_text().rsplit(')', 1)[1].split()[0]
                require(state in ('Z', 'X'),
                        f'watchdog left live process {pid} in state {state}')
        controls.append('parent_and_descendant_terminated')

    return dict(passed=True, optimized_python=not __debug__,
                seconds=time.monotonic()-started, controls=len(controls),
                checked=controls, real_subprocesses=True,
                mathematical_computation=False, census_recomputed=False,
                real_data_modified=False)


if __name__ == '__main__':
    destination = ROOT/'verification/current'
    destination.mkdir(parents=True, exist_ok=True)
    mode = 'normal' if __debug__ else 'optimized'
    try:
        result = run()
    except Exception as error:
        result = dict(passed=False, optimized_python=not __debug__,
                      error=str(error), traceback=traceback.format_exc())
    (destination/f'watchdog_controls_{mode}.json').write_text(
        json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result['passed'] else 1)
