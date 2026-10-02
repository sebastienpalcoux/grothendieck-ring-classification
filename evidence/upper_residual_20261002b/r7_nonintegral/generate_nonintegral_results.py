"""Regenerate complete proof trees. A timeout/error is never an exclusion."""
import collections
import hashlib
import json
import sys
import time
from pathlib import Path
from case_source import ROOT, SOFTWARE, read_cases, require

sys.path.insert(0, str(SOFTWARE))
from exact import norm_failure, pc
from rings import Characters
import proofs
from oriented_signed import enumerate_all, from_values, validate_general

GENERAL = {'R7_3_1036': 8, 'R7_3_1044': 24,
           'R7_4_2510': 4, 'R7_4_2706': 48}
PIVOTAL = ('R7_4_1212', 'R7_4_1213', 'R7_4_1417', 'R7_4_1420')
HERE = Path(__file__).resolve().parent

def main():
    cases = read_cases(set(GENERAL) | set(PIVOTAL))
    receipts = []
    for case_id, expected_count in GENERAL.items():
        start = time.monotonic()
        case = cases[case_id]
        sphere = proofs.sphere_certificate(case['tensor'])
        require(sphere is not None, 'ordinary spherical character survives')
        values, problem, stats = enumerate_all(case['tensor'], 60)
        require(len(values) == expected_count, 'signed branch count changed')
        branches = []
        for value in values:
            signed_tensor = from_values(case['tensor'], problem, value)
            validate_general(signed_tensor)
            algebra = Characters(signed_tensor)
            components = [{'factor': pc(factor), 'obstruction':
                           proofs.signed_component_certificate(case['tensor'], signed_tensor,
                                                              algebra, factor, sphere)}
                          for factor, multiplicity in algebra.components]
            require(all(b['obstruction'] is not None for b in components), 'uncovered signed character')
            branches.append({'values': list(value), 'generator': algebra.k,
                             'characters': components})
        certificate = {'kind': 'oriented_signed', 'sphere': sphere, 'branches': branches}
        # These four proofs need no further positivity, indicator, field or
        # dimension-order inference: every dimension branch fails zero,
        # duality, or the formal-codegree norm necessary condition.
        kinds = collections.Counter()
        for branch in certificate['branches']:
            require('characters' in branch, 'unexpected branch strategy')
            for component in branch['characters']:
                kinds[component['obstruction']['kind']] += 1
        require(set(kinds) <= {'zero', 'duality', 'norm'}, 'unexpected scope-sensitive criterion')
        result = {'id': case_id, 'scope': 'general_complex',
                  'source_line': case['source_line'], 'tensor_sha256': case['tensor_sha256'],
                  'signed_table_count': expected_count, 'certificate': certificate}
        (HERE / f'{case_id}_general.json').write_text(json.dumps(result, indent=2) + '\n')
        receipts.append({'id': case_id, 'tables': expected_count, 'character_obstructions': dict(kinds),
                         'discovery_seconds': round(time.monotonic() - start, 3)})
        print(json.dumps(receipts[-1]), flush=True)
    pivotal = []
    for case_id in PIVOTAL:
        case = cases[case_id]
        algebra = Characters(case['tensor'])
        components = []
        for factor, multiplicity in algebra.components:
            field, dimensions, delta, delta_poly = algebra.component(factor)
            zero = next((i for i, dimension in enumerate(dimensions) if not dimension), None)
            obstruction = ({'kind': 'zero', 'object': zero} if zero is not None
                           else norm_failure(delta_poly, algebra.cf))
            require(obstruction is not None, 'pivotal character survives')
            components.append({'factor': pc(factor), 'obstruction': obstruction})
        pivotal.append({'id': case_id, 'scope': 'pivotal_only',
                        'general_status': 'unresolved', 'source_line': case['source_line'],
                        'tensor_sha256': case['tensor_sha256'], 'generator': algebra.k,
                        'characters': components})
    (HERE / 'pivotal_certificates.json').write_text(json.dumps(pivotal, indent=2) + '\n')
    (HERE / 'discovery_receipts.json').write_text(json.dumps(receipts, indent=2) + '\n')
    modules = {Path(module.__file__).resolve() for module in list(sys.modules.values())
               if getattr(module, '__file__', None)
               and Path(module.__file__).resolve().parent == SOFTWARE.resolve()
               and Path(module.__file__).suffix == '.py'}
    hashes = {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
              for path in sorted(modules)}
    (HERE / 'signed_engine_sources.json').write_text(json.dumps(hashes, indent=2) + '\n')

if __name__ == '__main__':
    main()
