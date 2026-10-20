"""Close a spherical Casimir compression obstruction by complete signed lifts."""
import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

from quadratic_compression import HERE, ROOT, analyze, require, tensor_hash

sys.path.insert(0, str(ROOT / 'supplements/rank7/software'))
from oriented_signed import enumerate_all, from_values, validate_general
from signed import gauge_original


def certificate(R, timeout=180):
    report = analyze(R)
    require(any(row['spherical_violation'] for row in report['quadratic_checks']),
            'no spherical compression obstruction')
    values, problem, statistics = enumerate_all(R, timeout=timeout)
    branches = []
    for values_row in values:
        T = from_values(R, problem, values_row)
        validate_general(T)
        gauge = gauge_original(T, R)
        require(gauge is not None, 'a signed quotient is not gauge-equivalent to the source')
        branches.append({'values': list(values_row), 'gauge_to_original': gauge})
    return {'kind': 'oriented_signed_compression', 'scope': 'general_complex',
            'tensor_sha256': tensor_hash(R), 'spherical_compression': report,
            'branches': branches, 'statistics': statistics}


def verify(R, cert, timeout=180):
    require(cert.get('kind') == 'oriented_signed_compression', 'certificate kind')
    require(cert.get('scope') == 'general_complex', 'certificate scope')
    report = analyze(R)
    require(cert['tensor_sha256'] == tensor_hash(R), 'source tensor hash')
    require(report == cert['spherical_compression'], 'spherical compression arithmetic')
    require(any(row['spherical_violation'] for row in report['quadratic_checks']),
            'no spherical compression obstruction')
    values, problem, statistics = enumerate_all(R, timeout=timeout)
    require([list(v) for v in values] == [b['values'] for b in cert['branches']],
            'incomplete oriented signed quotient cover')
    require(statistics == cert['statistics'], 'enumeration statistics')
    for values_row, branch in zip(values, cert['branches']):
        T = from_values(R, problem, values_row)
        validate_general(T)
        gauge = gauge_original(T, R)
        require(gauge is not None and gauge == branch['gauge_to_original'],
                'signed quotient does not transfer the spherical structure')
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ring', default='R7_5_4569')
    parser.add_argument('--replay', action='store_true')
    parser.add_argument('--timeout', type=int, default=180)
    args = parser.parse_args()
    rows = json.loads((ROOT / 'supplements/rank7/output/m5/census.json').read_text())
    R = next(row['tensor'] for row in rows if row['id'] == args.ring)
    target = HERE / (args.ring + '_signed_compression.json')
    start = time.monotonic()
    if args.replay:
        cert = json.loads(target.read_text())['certificate']
        verify(R, cert, timeout=args.timeout)
    else:
        cert = certificate(R, timeout=args.timeout)
        target.write_text(json.dumps({'id': args.ring, 'certificate': cert}, indent=2) + '\n')
    receipt = {'status': 'PASS', 'id': args.ring, 'mode': 'replay' if args.replay else 'discovery',
               'optimized_python': not __debug__, 'source_tensor_sha256': tensor_hash(R),
               'certificate_file_sha256': hashlib.sha256(target.read_bytes()).hexdigest(),
               'signed_quotients': len(cert['branches']), 'seconds': time.monotonic() - start}
    suffix = '_optimized_replay.json' if not __debug__ else '_normal_replay.json' if args.replay else '_discovery.json'
    target.with_name(target.stem + suffix).write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt), flush=True)


if __name__ == '__main__':
    main()
