#!/usr/bin/env python3
"""Targeted coverage and fail-closed checks for the staged interface."""
import argparse
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import stages


def require(test, message):
    if not test:
        raise RuntimeError(message)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT/'tests/stages_results.json')
    args = parser.parse_args()
    report = {'all_checks_passed': False, 'status': 'running', 'checks': []}
    stages.write(args.output, report)
    try:
        results = ROOT/'classification/results'
        ledger = [json.loads(line) for line in (results/'certificates.jsonl').read_text().splitlines()]
        summary = stages.load(results/'summary.json')
        rows = [json.loads(line) for line in (ROOT/'census/data/rings.jsonl').read_text().splitlines()]
        models = stages.load(ROOT/'classification/models.json')
        endpoint = [row for row, item in zip(rows, ledger) if item['stage'] == 'model']
        require(len(stages.identify_endpoint(endpoint, models)['models']) == 15,
                'valid endpoint rejected')
        report['checks'].append('valid_fifteen_models')
        for name, selection in [
            ('missing_model', endpoint[:-1]),
            ('extra_nonmodel', endpoint+[next(row for row, item in zip(rows, ledger)
                                              if item['stage'] == 'rank_two')]),
        ]:
            try:
                stages.identify_endpoint(selection, models)
            except Exception:
                report['checks'].append(name)
            else:
                raise RuntimeError('invalid endpoint accepted: '+name)
        cases = []
        cases.append(('missing_ledger_record', ledger[:-1], summary))
        duplicate = copy.deepcopy(ledger)
        duplicate[-1] = copy.deepcopy(duplicate[0])
        cases.append(('duplicate_ledger_record', duplicate, summary))
        bad_summary = copy.deepcopy(summary)
        bad_summary['stages'][0]['excluded'] += 1
        cases.append(('false_stage_count', ledger, bad_summary))
        wrong_stage = copy.deepcopy(ledger)
        next(item for item in wrong_stage if item['stage'] == 'rank_two')['stage'] = 'formal_codegree_dnumber'
        cases.append(('misassigned_stage', wrong_stage, summary))
        with tempfile.TemporaryDirectory(prefix='rank4-stage-regression-') as temporary:
            work = Path(temporary)
            flags = ['-O'] if sys.flags.optimize else []
            for name, records, claimed in cases:
                (work/'certificates.jsonl').write_text(''.join(json.dumps(item)+'\n' for item in records))
                stages.write(work/'summary.json', claimed)
                output = work/'report.json'
                stages.write(output, {'all_checks_passed': True, 'status': 'passed'})
                result = subprocess.run([sys.executable, *flags, str(ROOT/'stages.py'), 'rank-two',
                                         '--results', str(work), '--output', str(output), '--workers', '2'],
                                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                require(result.returncode != 0, 'invalid input accepted: '+name)
                status = stages.load(output)
                require(status['all_checks_passed'] is False and status['status'] == 'failed',
                        'stale PASS retained: '+name)
                report['checks'].append(name)
        report.update({'all_checks_passed': True, 'status': 'passed',
                       'optimized_python': bool(sys.flags.optimize), 'tests': len(report['checks'])})
    except Exception as exc:
        report.update({'all_checks_passed': False, 'status': 'failed', 'error': str(exc)})
        raise
    finally:
        stages.write(args.output, report)
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
