#!/usr/bin/env python3
"""Recompute and verify successive finite-classification stages.

Each invocation starts from the census and recomputes the requested prefix;
previous report files are never trusted. The stage labels and memberships
must agree with the release ledger, but the new witnesses are checked exactly.
The central endpoint identifies exactly the fifteen model fusion rings;
the models stage also replays their model certificates.
"""
import argparse
from collections import Counter
import hashlib
import json
import multiprocessing
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT/'classification'))
from verify import (Characters, arithmetic_failure, canonical,
                    initialize, ns_tensor, pc, rank_two, rapid, require,
                    sd_tensor, small_families, sphere_certificate, validate,
                    verify_record)

STAGES = [
    ('rank-two', 'rank_two'),
    ('d-number', 'formal_codegree_dnumber'),
    ('spherical', 'spherical_arithmetic'),
    ('families', 'published_rank_four_families'),
    ('central', 'central_induction'),
]


def load(path):
    return json.loads(path.read_text())


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2)+'\n')


def spherical_task(row):
    return row['id'], sphere_certificate(row['tensor'])


def arithmetic_task(row):
    """Apply only character arithmetic, without attempting central induction."""
    analysis = Characters(row['tensor'])
    branches = [{'factor': pc(factor), 'obstruction': arithmetic_failure(analysis, factor)}
                for factor, multiplicity in analysis.components]
    certificate = None
    if all(branch['obstruction'] is not None for branch in branches):
        certificate = {'kind': 'spherical', 'generator': analysis.k,
                       'characters': branches, 'pseudo': None}
    return row['id'], certificate


def validate_row(row):
    require(row['tag'] in ('S', 'N'), 'unknown census duality tag')
    constructor = sd_tensor if row['tag'] == 'S' else ns_tensor
    require(row['tensor'] == constructor(row['parameters']), 'tensor/parameter mismatch')
    validate(row['tensor'])
    return canonical(row['tensor'])


def record(row, stage, certificate):
    return {key: row[key] for key in ('id', 'tag', 'parameters')} | {
        'stage': stage, 'certificate': certificate}


def identify_endpoint(rows, models):
    """Only called after all five computational filters have been applied."""
    by_key = {canonical(model['matrices']): model['model'] for model in models}
    require(len(by_key) == len(models), 'duplicate model fusion rings')
    found = []
    for row in rows:
        model = by_key.get(canonical(row['tensor']))
        require(model is not None, 'unidentified survivor of the five computational filters')
        found.append({'id': row['id'], 'model': model})
    require(len(rows) == len(found) == len(models) == 15 and
            {item['model'] for item in found} == set(by_key.values()), 'model coverage differs')
    return {'models': found}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('stage', nargs='?', choices=[item[0] for item in STAGES]+['models'])
    parser.add_argument('--all', action='store_true', help='Run all five exclusion stages and model replay.')
    parser.add_argument('--workers', type=int, default=4)
    parser.add_argument('--input', type=Path, default=ROOT/'census/data/rings.jsonl')
    parser.add_argument('--results', type=Path, default=ROOT/'classification/results')
    parser.add_argument('--models', type=Path, default=ROOT/'classification/models.json')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    require(args.workers >= 1, '--workers must be positive')
    require(bool(args.stage) != bool(args.all), 'choose one stage or --all')
    replay_models = args.all or args.stage == 'models'
    stop = len(STAGES)-1 if replay_models else [item[0] for item in STAGES].index(args.stage)
    label = 'all' if args.all else args.stage
    output = args.output or ROOT/'validation/stages'/f'{label}.json'
    started = time.monotonic()
    report = {'all_checks_passed': False, 'status': 'running', 'requested_stage': label,
              'fresh_prefix': True, 'stages': []}
    write(output, report)  # Never preserve an old PASS on failure or interruption.
    try:
        rows = [json.loads(line) for line in args.input.read_text().splitlines()]
        ledger = [json.loads(line) for line in (args.results/'certificates.jsonl').read_text().splitlines()]
        summary = load(args.results/'summary.json')
        models = load(args.models)
        require(summary.get('schema_version') == 5, 'unsupported classification schema')
        require(len(rows) == len(ledger) == summary['census_count'], 'census/ledger coverage differs')
        ids = [row['id'] for row in rows]
        require(len(set(ids)) == len(ids), 'duplicate census identifiers')
        require(ids == [item['id'] for item in ledger], 'certificate coverage/order differs')
        require(all(all(row[key] == item[key] for key in ('id', 'tag', 'parameters'))
                    for row, item in zip(rows, ledger)), 'certificate identifies a different census ring')
        require([item['filter'] for item in summary['stages']] == [item[1] for item in STAGES],
                'summary stages omitted, duplicated, or out of order')
        allowed = {item[1] for item in STAGES} | {'model'}
        require(all(item['stage'] in allowed for item in ledger), 'unknown ledger stage')
        require(len({model['model'] for model in models}) == len(models), 'duplicate model names')
        remaining = list(rows)
        report['census_count'] = len(rows)
        report['input_sha256'] = hashlib.sha256(args.input.read_bytes()).hexdigest()
        report['ledger_sha256'] = hashlib.sha256((args.results/'certificates.jsonl').read_bytes()).hexdigest()
        arithmetic_kinds = Counter()
        with multiprocessing.Pool(args.workers, initializer=initialize, initargs=(models,)) as pool:
            keys = list(pool.imap(validate_row, rows, chunksize=30))
            require(len(set(keys)) == len(rows), 'isomorphic duplicates in census')
            for index, (name, stage) in enumerate(STAGES[:stop+1]):
                stage_start = time.monotonic()
                if index in (0,1,3):
                    producer = {0:rank_two,1:rapid.dnumber,3:small_families}[index]
                    generated = {row['id']: producer(row['tensor']) for row in remaining}
                else:
                    task = arithmetic_task if index == 2 else spherical_task
                    generated = dict(pool.imap_unordered(task, remaining))
                    if index == 4:
                        require(all(certificate is None or certificate['pseudo'] is not None
                                    for certificate in generated.values()),
                                'central stage received an arithmetic-only exclusion')
                excluded = [row for row in remaining if generated[row['id']] is not None]
                excluded_ids = [row['id'] for row in excluded]
                require(excluded_ids == [item['id'] for item in ledger if item['stage'] == stage],
                        'fresh stage membership differs from ledger: '+stage)
                pairs = [(row, record(row, stage, generated[row['id']])) for row in excluded]
                checked = list(pool.imap(verify_record, pairs, chunksize=20))
                require(checked == [stage]*len(excluded), 'wrong replay stage')
                if stage == 'spherical_arithmetic':
                    for row in excluded:
                        arithmetic_kinds.update(branch['obstruction']['kind']
                                                for branch in generated[row['id']]['characters'])
                remaining = [row for row in remaining if generated[row['id']] is None]
                advertised = summary['stages'][index]
                require(advertised['excluded'] == len(excluded) and advertised['remaining'] == len(remaining),
                        'summary count differs: '+stage)
                item = {'command': name, 'filter': stage, 'excluded': len(excluded),
                        'remaining': len(remaining), 'excluded_ids': excluded_ids,
                        'seconds': round(time.monotonic()-stage_start, 6)}
                report['stages'].append(item)
                print(f'{name}: excluded {len(excluded)}; remaining {len(remaining)}', flush=True)
                if stage == 'central_induction':
                    report['model_endpoint'] = identify_endpoint(remaining, models)
                    print('Endpoint checked: exactly fifteen model fusion rings.', flush=True)
            if replay_models:
                model_records = [item for item in ledger if item['stage'] == 'model']
                require([row['id'] for row in remaining] == [item['id'] for item in model_records],
                        'final survivor membership differs')
                checked = list(pool.imap(verify_record, zip(remaining, model_records)))
                require(checked == ['model']*len(models), 'model replay failed')
                report['model_records_replayed'] = len(checked)
                print(f'models: replayed {len(checked)} model certificates.', flush=True)
        report.update({'all_checks_passed': True, 'status': 'passed',
                       'remaining_ids': [row['id'] for row in remaining],
                       'arithmetic_branch_counts': dict(arithmetic_kinds),
                       'scope': 'Fresh finite filters and exact certificate replay; model existence uses the cited mathematical constructions.'})
    except Exception as exc:
        report.update({'all_checks_passed': False, 'status': 'failed', 'error': str(exc)})
        raise
    finally:
        report['seconds'] = round(time.monotonic()-started, 6)
        write(output, report)
    print(f'PASS: fresh prefix through {label}; report {output.name}.')


if __name__ == '__main__':
    main()
