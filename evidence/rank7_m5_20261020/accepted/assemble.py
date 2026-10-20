"""Assemble reviewed decisions without changing any classification ledger."""
import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
EVIDENCE = HERE.parent


def require(value, message):
    if not value:
        raise ValueError(message)


def read(relative):
    return json.loads((EVIDENCE / relative).read_text())


def binding(relative):
    path = EVIDENCE / relative
    return {'path': str(path.relative_to(ROOT)),
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--include-4982', action='store_true')
    parser.add_argument('--include-character-triple', action='store_true',
                        help='Include reviewed R5343/R5623/R5778 after both exact replays pass.')
    parser.add_argument('--include-cyclic-5039', action='store_true',
                        help='Include the complete R5039 cyclic-rotation chain after both exact replays pass.')
    args = parser.parse_args()
    initial = {r['id']: r for r in read('computation/source_frontier.json')}
    decisions = []

    def add(rid, criterion, certificate):
        require(rid in initial and initial[rid]['status'] == 'unresolved',
                'decision is not from the initial open frontier')
        decisions.append({'id': rid, 'status': 'excluded', 'criterion': criterion,
                          'certificate': certificate, 'model_names': [],
                          'continuation_source': 'evidence/rank7_m5_20261020'})

    computational = [
            ('R7_5_1964', 'character', 'character'),
            ('R7_5_4530', 'oriented_dimension_order', 'oriented_dimension_order'),
            ('R7_5_4531', 'oriented_dimension_order', 'oriented_dimension_order')]
    if args.include_character_triple:
        computational += [(f'R7_5_{i}', 'character', 'character') for i in (5343,5623,5778)]
    for rid, stage, criterion in computational:
        candidate = read(f'computation/{rid}_{stage}_h6.json')
        require(candidate['status'] == 'candidate_exclusion', 'missing candidate')
        digest = binding(f'computation/{rid}_{stage}_h6.json')['sha256']
        for mode in ('normal', 'optimized'):
            receipt = read(f'computation/{rid}_{stage}_h6_{mode}_replay.json')
            require(receipt['status'] == 'PASS', 'missing exact replay')
            require(receipt['candidate_sha256'] == digest, 'replay is not bound to current candidate')
        add(rid, criterion, candidate['certificate'])
    for row in read('criteria/quadratic_compression_results.json')['certificates']:
        require(row['id'] in ('R7_5_4653', 'R7_5_5029', 'R7_5_5040'), 'unexpected quadratic decision')
        add(row['id'], 'quadratic_casimir_compression', row['certificate'])
    add('R7_5_4569', 'oriented_signed_compression',
        read('criteria/R7_5_4569_signed_compression.json')['certificate'])
    for rid in ('R7_5_443', 'R7_5_1214'):
        tensor = initial[rid]['tensor']
        certificate = {'kind': 'q60_center_trace_general', 'id': rid,
                       'scope': 'general_complex',
                       'tensor_sha256': hashlib.sha256(json.dumps(tensor, separators=(',', ':')).encode()).hexdigest(),
                       'trace_certificate': binding(f'criteria/{rid}_q60_trace.json'),
                       'general_reduction': binding('sqrt15_reduction/discovery.json')}
        add(rid, 'quadratic_center_Galois_two_moment_q60', certificate)
    if args.include_4982:
        add('R7_5_4982', 'cyclic3_full_morita_rank13_descent',
            read('modules/r4982_exclusion_certificate.json'))
    if args.include_cyclic_5039:
        rid = 'R7_5_5039'
        proof = read(f'accepted/{rid}_cyclic_rotation_certificate.json')
        for mode in ('normal', 'optimized'):
            receipt = read(f'models/sqrt5/r5039_cyclic_chain_{mode}.json')
            require(receipt['status'] == 'PASS' and receipt['id'] == rid and
                    receipt['scope'] == 'general_complex' and receipt['read_only'] is True,
                    'missing complete cyclic-rotation replay')
            require(receipt['proof_manifest'] == proof['proof_inputs'],
                    'cyclic-rotation replay does not bind the accepted proof')
            require(all(receipt[k] == v for k, v in proof['coverage'].items()),
                    'cyclic-rotation branch coverage differs')
            require([row['stage'] for row in receipt['stages']] == proof['stage_names'],
                    'cyclic-rotation stage coverage differs')
        add(rid, 'quadratic_center_coupled_cyclic_rotation', {
            'kind': 'q5_cyclic_rotation_general', 'id': rid, 'scope': 'general_complex',
            'tensor_sha256': proof['tensor_sha256'],
            'proof_manifest': binding(f'accepted/{rid}_cyclic_rotation_certificate.json')})
    decisions.sort(key=lambda r: int(r['id'].rsplit('_', 1)[1]))
    require(len({r['id'] for r in decisions}) == len(decisions), 'duplicate decision')
    (HERE / 'decisions.json').write_text(json.dumps(decisions, indent=2) + '\n')
    print(json.dumps({'accepted_exclusions': len(decisions),
                      'ids': [r['id'] for r in decisions]}))


if __name__ == '__main__':
    main()
