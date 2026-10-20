"""Every categorification of either sqrt(15) candidate is Galois-pseudounitary."""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / 'supplements/rank7/software'))
from exact import require, pc
from rings import Characters
from oriented_signed import enumerate_all, from_values, validate_general
from signed import gauge_original


def run():
    results = []
    canonical = {r['id']: r['tensor'] for r in json.loads(
        (ROOT / 'supplements/rank7/output/m5/census.json').read_text())}
    for record in json.loads((HERE / 'discovery.json').read_text()):
        R = record['tensor']
        require(R == canonical.get(record['id']), 'pinned tensor differs from canonical census')
        vals, problem, stats = enumerate_all(R, timeout=600)
        require(len(vals) == 1, 'the signed quotient is not unique')
        T = from_values(R, problem, vals[0])
        validate_general(T)
        require(T == R, 'the unique signed quotient is not original')
        require(gauge_original(T, R) == [1]*7, 'incorrect original gauge')
        a = Characters(R)
        fp = a.fp()[0]
        branches = []
        for f, _ in a.components:
            K, ds, D, pD = a.component(f)
            zero = next((i for i, d in enumerate(ds) if not d), None)
            require(f == fp or zero is not None, 'another nonzero character remains')
            branches.append({'factor': pc(f), 'fp_orbit': f == fp, 'zero_object': zero})
        results.append({'id': record['id'], 'enumeration': stats,
                        'character_branches': branches,
                        'conclusion': 'Every categorification is spherical and Galois-pseudounitary.'})
    require([x['id'] for x in results] == ['R7_5_443', 'R7_5_1214'], 'incorrect input set')
    return {'status': 'PASS', 'scope': 'structural reduction; combine with independently verified pseudo-unitary obstruction',
            'results': results}


if __name__ == '__main__':
    print(json.dumps(run(), indent=2))
