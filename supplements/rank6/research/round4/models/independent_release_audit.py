"""Independent incremental release integrity audit; no mathematical solver calls.

The previous unpacked release is an explicit comparison input.  The checker
only writes a receipt when --output is supplied and all checks have passed.
It deliberately does not claim a fresh replay of inherited certificates or
PDF layout/ZIP integrity checks, which have separate release receipts.
"""
import argparse
import collections
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'software'))
from existence import REGISTRIES, STRUCTURES, POSITIVE_STATUSES, verify_ledger
from release_consistency import verify_consistency

NEW_IDS = ['R6_6_49', 'R6_6_1035', 'R6_8_311', 'R6_8_3664']
REMAINING = ['R6_4_22', 'R6_4_91', 'R6_4_155', 'R6_4_629',
             'R6_5_1204', 'R6_8_1660']


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text())


def jsonl(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line]


def audit(previous):
    bound = {}

    def bind(relative):
        bound[relative] = sha(ROOT / relative)

    # Require every inherited certificate, not just the four canonical JSONLs,
    # to survive unchanged.  A stronger statement is cheap to check here.
    preserved = {}
    for old in sorted((previous / 'certificates').rglob('*')):
        if old.is_file():
            relative = old.relative_to(previous).as_posix()
            require((ROOT / relative).is_file(), 'missing inherited ' + relative)
            require(sha(old) == sha(ROOT / relative), 'modified inherited ' + relative)
            preserved[relative] = sha(old)
            bind(relative)
    require(len(preserved) >= 4, 'empty inherited certificate comparison')
    census_files = ['data/census.json', 'data/rank6_tables.txt.gz',
                    'provenance/census_LICENSE.txt', 'provenance/repository_source.json']
    registries = ['data/' + name + '.json' for name in REGISTRIES]
    for relative in census_files + registries:
        require(sha(previous / relative) == sha(ROOT / relative),
                'changed census or positive registry: ' + relative)
        bind(relative)

    old = read(previous / 'data/decisions.json')
    new = read(ROOT / 'data/decisions.json')
    census = read(ROOT / 'data/census.json')
    require(len(new) == len(old) == len(census) == 16612, 'census cardinality')
    require([r['id'] for r in new] == [r['id'] for r in old] ==
            [r['id'] for r in census], 'ledger/census order or identifiers changed')
    require(len({r['id'] for r in new}) == 16612, 'duplicate ledger identifier')
    verify_ledger(new)
    moves = []
    for a, b in zip(old, new):
        require(set(b['existence']) == set(STRUCTURES), 'five-field scope')
        require(all(a[k] == b[k] for k in
                    ('id', 'm', 'index', 'source_label', 'dual', 'commutative')),
                'changed census identity: ' + b['id'])
        if a['status'] != b['status']:
            moves.append(b['id'])
            require(a['status'] == 'unresolved' and b['status'] == 'excluded',
                    'unexpected status transition: ' + b['id'])
            require(all(b['existence'][s] == 'no' for s in STRUCTURES),
                    'new general exclusion lacks five no values')
        else:
            require(a['existence'] == b['existence'],
                    'unrelated existence change: ' + b['id'])
    require(moves == NEW_IDS, 'status moves differ from exactly four accepted IDs')
    positive_old = [r for r in old if r['status'] in POSITIVE_STATUSES]
    positive_new = [r for r in new if r['status'] in POSITIVE_STATUSES]
    require(positive_new == positive_old, 'positive ledger records changed')
    model_old = read(previous / 'data/model_catalog.json')
    model_new = read(ROOT / 'data/model_catalog.json')
    require(model_old == model_new, 'positive model catalogue changed')
    require(len(model_new) == 54 and
            sum(len(r['constructors']) for r in model_new) == 61,
            'positive constructor count')
    status = dict(collections.Counter(r['status'] for r in new))
    require(status == {'excluded': 16552, 'unitarily_realized': 53,
                       'spherically_realized_nonpseudounitary': 1, 'unresolved': 6},
            'final classification counts')
    require([r['id'] for r in new if r['status'] == 'unresolved'] == REMAINING,
            'residual identities')
    completed = [m for m in range(1, 9)
                 if not any(r['m'] == m and r['status'] == 'unresolved' for r in new)]
    require(completed == [1, 2, 3, 6, 7], 'complete exact multiplicity bands')
    through3 = collections.Counter(r['status'] for r in new if r['m'] <= 3)
    require(through3 == {'excluded': 531, 'unitarily_realized': 45,
                         'spherically_realized_nonpseudounitary': 1},
            'classification through multiplicity three')

    frozen = read(ROOT / 'verification/round4/campaign_manifest.json')
    frozen_ids = [r['id'] for r in old if r['status'] == 'unresolved']
    require(frozen['previous_ledger_sha256'] == sha(previous / 'data/decisions.json'),
            'frozen previous ledger hash')
    require(frozen['input_count'] == 10 and frozen['ids'] == frozen_ids,
            'frozen ten-input domain')
    lookup = {r['id']: r for r in census}
    require(frozen['tensors'] == [lookup[rid] for rid in frozen_ids],
            'frozen tensors disagree with census')

    certificates = jsonl(ROOT / 'certificates/continuation_round4.jsonl')
    sources = read(ROOT / 'verification/round4/proof_sources.json')
    require([r['id'] for r in certificates] == NEW_IDS == [r['id'] for r in sources],
            'canonical allocation/source IDs')
    for record, source in zip(certificates, sources):
        path = ROOT / source['path']
        extracted = read(path)
        if 'field' in source:
            extracted = extracted[source['field']]
        require(record['certificate'] == extracted, 'canonical/source certificate mismatch')
        require(record['source'] == source['path'] and record['source_sha256'] == sha(path),
                'canonical proof source hash/path')
        require(record['status'] == 'excluded' and record['exact_checked'] is True
                and record['certificate']['scope'] == 'general'
                and record['stage'] == 'continuation_subcategory_projection',
                'canonical proof scope/status')
        require(record['m'] == lookup[record['id']]['m'], 'canonical multiplicity')
        bind(source['path'])
    replay = read(ROOT / 'verification/round4/release_replay.json')
    require(replay['passed'] and replay['optimized_python'] and replay['optimizer_disabled'],
            'canonical exact replay flags')
    require(replay['new_ids'] == NEW_IDS and replay['new_exclusions'] == 4,
            'canonical replay coverage')
    require(sorted(r['id'] for r in replay['replays']) == sorted(NEW_IDS)
            and all(r['passed'] and r['optimized_python'] and r['optimizer_disabled']
                    for r in replay['replays']), 'per-proof replay coverage')
    require(replay['certificate_sha256'] == sha(ROOT / replay['certificate_file'])
            and replay['ledger_sha256'] == sha(ROOT / 'data/decisions.json'),
            'canonical replay artifact hashes')
    require(replay['prior_continuation_certificates'] == 37
            and replay['prior_continuations_replayed'] is False,
            'historical replay scope incorrectly reported')

    summary = read(ROOT / 'verification/release_summary.json')
    require((summary['excluded'], summary['positive'], summary['unresolved']) ==
            (16552, 54, 6), 'summary totals')
    require(summary['unresolved_ids'] == REMAINING and
            summary['continuation_excluded'] == 41 and
            summary['fourth_continuation_excluded'] == 4,
            'summary continuation allocation')
    for relative, digest in summary['continuation_files_sha256'].items():
        require(sha(ROOT / relative) == digest, 'summary certificate digest')
    consistency = verify_consistency()

    counts = read(ROOT / 'data/classification_counts.json')
    for relative in ['README.md', 'REVISION_NOTES.md']:
        text = (ROOT / relative).read_text()
        require('**4 general exclusions**' in text and '**6 unresolved rings**' in text
                and '**16,552 general exclusions' in text
                and '54 realized rings**' in text and '16,612 census tensors' in text
                and '**1, 2, 3, 6, 7**' in text, 'current prose count/scope: ' + relative)
        for row in counts:
            models = row['unitarily_realized'] + row['spherically_realized_nonpseudounitary']
            expected = '| {} | {:,} | {:,} | {} | {} |'.format(
                row['multiplicity'], row['classes'], row['excluded'], models, row['unresolved'])
            require(expected in text, 'stale classification table: ' + relative)
        require('| **Total** | **16,612** | **16,552** | **54** | **6** |' in text,
                'current prose totals table')
        bind(relative)
    notes = (ROOT / 'REVISION_NOTES.md').read_text()
    require(all('`' + rid + '`' in notes for rid in NEW_IDS), 'revision accepted proof IDs')
    evidence = (ROOT / 'verification/README.md').read_text()
    require('16,552 exclusions, 54 realized rings and\n6 unresolved cases' in evidence
            and 'bands are 1, 2, 3, 6, 7' in evidence
            and '`round4/`' in evidence, 'verification README stale')
    macros = dict(re.findall(r'\\newcommand\{\\(\w+)\}\{(\d+)\}',
                            (ROOT / 'papers/generated_statistics.tex').read_text()))
    expected_macros = {'NegativeCount': '16552', 'UnitaryCount': '53',
                       'SphericalOnlyCount': '1', 'PositiveCount': '54',
                       'UnresolvedCount': '6', 'CompleteBound': '3',
                       'CensusCount': '16612', 'CensusBound': '8', 'ConstructorCount': '61'}
    require(all(macros.get(k) == v for k, v in expected_macros.items()), 'paper count macros')
    tex = (ROOT / 'papers/generated_classification.tex').read_text()
    for row in counts:
        expected = '{} & {} & {} & {} & {} & {}'.format(
            row['multiplicity'], row['classes'], row['excluded'], row['unitarily_realized'],
            row['spherically_realized_nonpseudounitary'], row['unresolved'])
        require(expected in tex, 'paper classification row')
    require('Total & 16612 & 16552 & 53 & 1 & 6' in tex, 'paper classification totals')
    coverage = read(ROOT / 'research/round4/coverage.json')
    require(coverage['canonical_allocation_available'] is True
            and coverage['canonical_new_exclusions'] == 4
            and coverage['canonical_remaining_count'] == 6
            and coverage['canonical_remaining_ids'] == REMAINING,
            'coverage has not been reconciled with canonical allocation')
    require(coverage['frozen_input_ids'] == frozen_ids
            and coverage['positive_control_ids'] == [r['id'] for r in positive_new],
            'coverage input or positive-control domain')

    for relative in ['data/decisions.json', 'data/decisions.csv', 'data/model_catalog.json',
                     'data/model_catalog.csv', 'data/unresolved_tensors.json',
                     'data/classification_counts.json', 'verification/release_summary.json',
                     'verification/round4/campaign_manifest.json',
                     'verification/round4/proof_sources.json',
                     'verification/round4/release_replay.json',
                     'certificates/continuation_round4.jsonl', 'verification/README.md',
                     'papers/generated_statistics.tex', 'papers/generated_classification.tex',
                     'papers/verification_guide.tex', 'papers/manuscript.tex',
                     'research/round4/coverage.json']:
        bind(relative)
    return {'schema': 'rank6-round4-independent-release-audit/v1', 'passed': True,
            'optimized_python': not __debug__,
            'scope': 'Old/new integrity, exact allocation, five existence fields, source-bound replay receipts and current derived data/prose. No repeated mathematical certificate replay, PDF layout or ZIP check.',
            'previous_ledger_sha256': sha(previous / 'data/decisions.json'),
            'census_rows': 16612, 'status_counts': status, 'new_general_exclusion_ids': moves,
            'remaining_ids': REMAINING, 'completed_exact_multiplicities': completed,
            'all_five_existence_fields_checked': True,
            'unchanged_prior_certificate_files': preserved,
            'unchanged_census_source_files': census_files,
            'unchanged_positive_registry_files': registries,
            'unchanged_positive_ids': [r['id'] for r in positive_new],
            'positive_constructors': 61, 'cross_export_consistency': consistency,
            'bound_file_sha256': bound}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--previous', type=Path, required=True)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = audit(args.previous.resolve())
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items()
                      if k not in ('unchanged_prior_certificate_files',
                                   'unchanged_positive_ids', 'bound_file_sha256')}, indent=2))
