"""Exact spherical/Galois-pseudounitary reduction; not an exclusion certificate."""
from pathlib import Path
import json
import sys
import hashlib

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'supplements/rank7/software'))
from exact import require, pc
from rings import Characters, casimir
from oriented_signed import enumerate_all, from_values, validate_general
from signed import gauge_original
import sympy as s


def run():
    source = json.loads(Path(__file__).with_name('source_tensors.json').read_text())
    rings = {r['id']: r['tensor'] for r in source}
    canonical = {r['id']: r['tensor'] for r in json.loads(
        (ROOT / 'supplements/rank7/output/m5/census.json').read_text())}
    results = []
    for ident, expected in [('R7_5_3895', 2), ('R7_5_5039', 4)]:
        R = rings[ident]
        require(R == canonical.get(ident), 'pinned tensor differs from canonical census')
        a = Characters(R)
        fp = a.fp()[0]
        original = []
        for f, _ in a.components:
            K, ds, D, pD = a.component(f)
            zero = next((i for i, d in enumerate(ds) if not d), None)
            dual = next((i for i in range(7) if ds[i] != ds[a.du[i]]), None)
            require(f == fp or zero is not None or dual is not None,
                    'a non-FP spherical character remains')
            original.append({'factor': pc(f), 'fp_orbit': f == fp,
                             'zero_object': zero, 'unequal_dual': dual})
        vals, problem, stats = enumerate_all(R, timeout=600)
        require(len(vals) == expected, 'unexpected complete signed-quotient count')
        branches = []
        for v in vals:
            T = from_values(R, problem, v)
            validate_general(T)
            gauge = gauge_original(T, R)
            if gauge:
                branches.append({'gauge_original': gauge})
                continue
            require(ident == 'R7_5_5039', 'unexpected nongauge branch')
            b = Characters(T)
            require(all(f.degree() <= 2 for f, _ in b.components),
                    'signed character field can have degree above two')
            # The two sectors of sphericalization supply both quadratic fields.
            x = s.Symbol('x')
            unsigned_factor = s.Poly(x*x - 1440*x + 6400, x)
            signed_factor = s.Poly(x*x - 616*x + 1760, x)
            require(casimir(R).charpoly(x).as_poly().rem(unsigned_factor).is_zero,
                    'missing unsigned quadratic factor')
            require(casimir(T).charpoly(x).as_poly().rem(signed_factor).is_zero,
                    'missing signed quadratic factor')
            require(unsigned_factor.discriminant() == 5 * 640**2,
                    'incorrect unsigned field')
            require(signed_factor.discriminant() == 11 * 184**2,
                    'incorrect signed field')
            require(s.Poly(x**4 - 32*x*x + 36, x).is_irreducible,
                    'the compositum is not degree four')
            branches.append({'obstruction': 'dimension_field_degree',
                             'required_quadratic_fields': [5, 11],
                             'required_degree': 4,
                             'character_degrees': [f.degree() for f, _ in b.components]})
        results.append({'id': ident,
                        'tensor_sha256': hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest(),
                        'enumeration': stats, 'branches': branches,
                        'original_character_reduction': original,
                        'conclusion': 'Every categorification is spherical and Galois-pseudounitary.'})
    return {'status': 'PASS', 'scope': 'structural reduction only; no categorification or exclusion asserted',
            'results': results}


if __name__ == '__main__':
    print(json.dumps(run(), indent=2))
