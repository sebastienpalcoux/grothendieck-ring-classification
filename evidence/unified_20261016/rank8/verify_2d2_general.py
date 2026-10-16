"""Source-bound replay of the unified four-case algebraic 2D2 obstruction."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', type=Path, required=True)
    repo = parser.parse_args().repo.resolve()
    folder = Path(__file__).resolve().parent
    interpreter = [sys.executable] + (['-O'] if sys.flags.optimize else [])
    jobs = [('source_graphs', 'verify_2d2_source_graphs.py', ['--repo', str(repo)]),
            ('rotation_one', 'verify_gpa_certificate.py', []),
            ('primitive_rotations', 'verify_gpa_omega_certificate.py', [])]
    results = {}
    for name, filename, args in jobs:
        run = subprocess.run(interpreter + [str(folder / filename)] + args,
                             capture_output=True, text=True, check=True)
        result = json.loads(run.stdout)
        require(result.get('status') == 'PASS', name + ': verifier did not pass')
        results[name] = result
    cases = results['source_graphs']['cases']
    require([c['id'] for c in cases] == ['R8_2_152', 'R8_2_153', 'R8_2_166', 'R8_2_495'],
            'four source-bound cases')
    require(all(c['both_even_ranks'] == 4 and c['both_even_parts_generated']
                and c['left_and_right_graph'] == '2D2' for c in cases), 'graph hypotheses')
    positive = results['rotation_one']
    require(positive['all_complex_ideal_equality'] and positive['self_adjoint_base_verified']
            and positive['complex_edge_gauge_verified']
            and positive['two_full_Laurent_families_verified']
            and positive['primitive_opposite_free_gauge_weights_verified'],
            'rotation-one rigidity')
    require(not positive['self_adjointness_imposed'], 'unexpected star hypothesis')
    primitive = results['primitive_rotations']
    require(primitive['both_primitive_cube_roots_excluded']
            and not primitive['self_adjointness_imposed'], 'primitive-rotation obstruction')
    filenames = [job[1] for job in jobs] + [
        'gpa_certificate.json', 'gpa_omega_certificate.json', 'FOUR_2D2_GENERAL_PROOF.md']
    hashes = {name: hashlib.sha256((folder / name).read_bytes()).hexdigest() for name in filenames}
    print(json.dumps({'status': 'PASS', 'criterion': 'algebraic_2D2_planar_algebra',
                      'cases': cases, 'components': results, 'artifact_sha256': hashes,
                      'scope': 'exact source and algebraic certificates; categorical argument is in FOUR_2D2_GENERAL_PROOF.md'}, indent=2))


if __name__ == '__main__':
    main()
