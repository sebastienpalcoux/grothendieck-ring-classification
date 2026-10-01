#!/usr/bin/env python3
"""Optimizer-free exact verifier for the general exclusion of R6_9_1060.

All correctness gates use require(), including under python -O.
The frozen tensor is independent of changing census classification status.
"""
import argparse
import ast
import hashlib
import importlib
import itertools
import json
import math
import os
from pathlib import Path
import sys
import tempfile
import time
from fractions import Fraction

sys.dont_write_bytecode = True
BUNDLE = Path(__file__).resolve().parent
RING_ID = 'R6_9_1060'
TENSOR_SHA256 = '3d6747c2494cb99ed76d977a7025d3ef2d399371a2069a67a6ce2964cad7b353'

class VerificationError(RuntimeError):
    pass

def require(condition, message):
    if not condition:
        raise VerificationError(message)

def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()

def read_json(path):
    with Path(path).open() as stream:
        return json.load(stream)

def source_root(argument):
    if argument:
        candidate = Path(argument).expanduser().resolve()
        require((candidate / 'software/character_induction.py').is_file(),
                'source root must contain software/character_induction.py')
        return candidate
    env = os.environ.get('RANK6_SOURCE_ROOT')
    if env:
        return source_root(env)
    for start in (BUNDLE, Path.cwd().resolve()):
        for candidate in (start, *start.parents):
            if (candidate / 'software/character_induction.py').is_file():
                return candidate
    raise VerificationError('specify --source-root PATH, or set RANK6_SOURCE_ROOT')

def load_dependencies(root):
    manifest = read_json(BUNDLE / 'source_manifest.json')['canonical_software']
    for filename, expected in manifest.items():
        path = root / 'software' / filename
        require(path.is_file(), f'missing canonical dependency: {filename}')
        raw = path.read_bytes()
        require(hashlib.sha256(raw).hexdigest() == expected,
                f'canonical source hash mismatch: {filename}')
        require(not any(isinstance(node, ast.Assert) for node in ast.walk(ast.parse(raw))),
                f'optimization-sensitive assertion in dependency: {filename}')
    sys.path.insert(0, str(BUNDLE))
    sys.path.insert(1, str(root / 'software'))
    modules = {Path(filename).stem: importlib.import_module(Path(filename).stem)
               for filename in manifest}
    for name, module in modules.items():
        require(Path(module.__file__).resolve() == (root / 'software' / (name + '.py')).resolve(),
                f'wrong imported dependency origin: {name}')
    def forbidden_optimizer(*args, **kwargs):
        raise VerificationError('an optimizer was invoked during exact replay')
    for module in modules.values():
        if hasattr(module, 'farkas'):
            module.farkas = forbidden_optimizer
    return modules, manifest

def load_tensor():
    frozen = read_json(BUNDLE / 'tensor.json')
    require(frozen['id'] == RING_ID, 'wrong frozen tensor identifier')
    R = frozen['N']
    require(len(R) == 6 and all(len(row) == 6 and all(len(v) == 6 for v in row) for row in R),
            'tensor must have shape 6 by 6 by 6')
    require(all(type(x) is int and x >= 0 for row in R for v in row for x in v),
            'tensor coefficients must be nonnegative integers')
    require(digest(R) == TENSOR_SHA256 == frozen['tensor_sha256'], 'frozen tensor hash mismatch')
    require(frozen['dual'] == list(range(6)), 'wrong duality')
    for i, j in itertools.product(range(6), repeat=2):
        require(R[0][i][j] == int(i == j), 'invalid tensor unit')
        require(R[i][j][0] == int(i == j), 'invalid self-duality')
        require(R[i][j] == R[j][i], 'tensor not commutative')
        for k, l in itertools.product(range(6), repeat=2):
            require(sum(R[i][j][h] * R[h][k][l] for h in range(6)) ==
                    sum(R[j][k][h] * R[i][h][l] for h in range(6)),
                    'tensor associativity fails')
    return R

def exact_psd(matrix):
    A = [[Fraction(x) for x in row] for row in matrix.tolist()]
    for k in range(len(A)):
        pivot = A[k][k]
        if pivot < 0:
            return False
        if not pivot:
            if any(A[k][j] for j in range(k + 1, len(A))):
                return False
            continue
        for i in range(k + 1, len(A)):
            for j in range(i, len(A)):
                A[i][j] -= A[i][k] * A[k][j] / pivot
                A[j][i] = A[i][j]
    return True

def frames_exact(R):
    import sympy as s
    z = s.sqrt(273)
    D = 2184 + 132*z
    factors = [D, 4, 6, 6, 12, 2184 - 132*z]
    characters = s.Matrix([
        [1, 1, 16+z, 17+z, 17+z, 16+z], [1, -1, 1, 0, 0, -1],
        [1, 1, 1, -1, -1, 1], [1, -1, -1, 1, -1, 1],
        [1, -1, -1, -2, 2, 1], [1, 1, 16-z, 17-z, 17-z, 16-z]])
    for h in range(6):
        require(s.expand(sum(characters[h, i]**2 for i in range(6)) - factors[h]) == 0,
                'incorrect formal codegree')
        for i, j in itertools.product(range(6), repeat=2):
            require(s.expand(characters[h, i]*characters[h, j] -
                             sum(R[i][j][k]*characters[h, k] for k in range(6))) == 0,
                    'character multiplication identity fails')
    require(characters.det() != 0, 'character table incomplete')
    M = sum((s.Matrix(n)**2 for n in R), s.zeros(6))
    require(list(M[:, 0]) == [6, 0, 32, 32, 34, 34], 'induction first column differs')
    T = s.Matrix([[1, -1, 0, 0, 0, 0], [0, 0, 1, 0, 0, -1], [0, 0, 0, 1, -1, 0]])
    require(T*M*T.T == s.Matrix([[12, -4, -4], [-4, 12, 4], [-4, 4, 20]]),
            'difference Gram differs')
    dimensions = [s.radsimp(D/f) for f in factors]
    Atot = (16, 11, 11, 6, 22)
    Btot = (17, 11, 11, 5, 22)
    for a, b, d in zip(Atot, Btot, dimensions[1:]):
        require(s.expand(1 + a*(16+z) + b*(17+z) - d) == 0, 'pair totals incorrect')
    us = [u for u in itertools.product(*[range(-3+(a+3)%2, 4, 2) for a in Atot])
          if sum(u) == -2 and sum(x*x for x in u) <= 12]
    vs = [v for v in itertools.product(*[range(-4+(b+4)%2, 5, 2) for b in Btot])
          if sum(v) == -2 and sum(x*x for x in v) <= 20]
    frames = []
    psd_count = 0
    for u, v in itertools.product(us, vs):
        rows = [[1, 0, 0, 0, 0, 0]] + [
            [1, 0, (a+x)//2, (b+y)//2, (b-y)//2, (a-x)//2]
            for a, b, x, y in zip(Atot, Btot, u, v)]
        F = s.Matrix(rows)
        residual = M - F.T*F
        if any(x < 0 for x in residual) or not exact_psd(residual):
            continue
        psd_count += 1
        H = characters*F.T
        if all(s.expand(dimensions[i]*H[i, j]-dimensions[j]*H[j, i]) == 0
               for i in range(6) for j in range(i)):
            frames.append(rows)
    require((len(us), len(vs), psd_count, len(frames)) == (18, 59, 369, 4),
            'exhaustive frame counts differ')
    return frames, {'difference_cases': len(us)*len(vs),
                    'exact_psd_survivors': psd_count, 'character_frames': len(frames)}

def dimension_reduction(R):
    q = 273
    D = (2184, 132)
    trace_bound = sum(x*x for row in R for vector in row for x in vector)
    require(trace_bound == 4396, 'incorrect signed Casimir trace bound')
    S_bound = (trace_bound - 5) // (2*q)
    require(S_bound == 8, 'incorrect norm-coordinate bound')
    def integral(a, b):
        return (2*a).denominator == 1 and (2*b).denominator == 1 and (a-b).denominator == 1
    def divide(x, y):
        a, b = x
        c, d = y
        norm = c*c-q*d*d
        require(norm != 0, 'zero quadratic divisor')
        return Fraction(a*c-q*b*d, norm), Fraction(b*c-a*d, norm)
    candidates, survivors = [], []
    for b, d in itertools.product(range(-math.isqrt(S_bound), math.isqrt(S_bound)+1), repeat=2):
        S = b*b+d*d
        if not 0 < S <= S_bound:
            continue
        target = q*S-4
        for a in range(-math.isqrt(target), math.isqrt(target)+1):
            if (a-b) % 2:
                continue
            cc = target-a*a
            c0 = math.isqrt(cc)
            if c0*c0 != cc:
                continue
            for c in sorted(set((c0, -c0))):
                if (c-d) % 2:
                    continue
                delta = (q*S, a*b+c*d)
                row = {'a': a, 'b': b, 'c': c, 'd': d, 'S': S, 'Delta': list(delta)}
                candidates.append(row)
                if integral(*divide(delta, D)) and integral(Fraction(delta[0], 12), Fraction(delta[1], 12)):
                    survivors.append(row)
    values = sorted(set(tuple(row['Delta']) for row in survivors))
    checks = []
    for a, b in values:
        norm, trace = a*a-q*b*b, 2*a
        require(b != 0 and norm > 0, 'unexpected degree or sign in d-number test')
        checks.append({'Delta': [a, b], 'trace': trace, 'norm': norm,
                       'trace_squared_mod_norm': trace*trace % norm,
                       'd_number': trace*trace % norm == 0})
    final_values = [item['Delta'] for item in checks if item['d_number']]
    require(len(candidates) == 144 and len(survivors) == 32, 'dimension candidate counts differ')
    require(final_values == [[2184, -132], [2184, 132]], 'general-to-pseudo-unitary reduction fails')
    expected = read_json(BUNDLE / 'general_dimension_certificate.json')
    require(expected['id'] == RING_ID and expected['proof_scope'] == 'general_dimension_reduction',
            'wrong general dimension certificate metadata')
    require(expected['norm_equation_candidates'] == len(candidates), 'incomplete norm candidates')
    require(expected['divisibility_survivors'] == survivors, 'dimension survivor list mismatch')
    require(expected['d_number_checks'] == checks and expected['final_dimension_values'] == final_values,
            'd-number certificate mismatch')
    return {'norm_candidates': len(candidates), 'divisibility_survivors': len(survivors),
            'final_dimension_values': final_values}

def endpoint_systems(ci, R, data, L, pruning):
    tail = len(R)-1
    plus_A, plus_b, plus_keep = ci.pruned_system(R, data, L, [1]*tail, 6, pruning)
    minus_A, minus_b, minus_keep = ci.pruned_system(R, data, L, [-1]*tail, 6, pruning)
    start = tail*(tail+1)//2 + 2*tail
    affected = set(range(start, start+2*tail))
    require(plus_keep == minus_keep and len(plus_b) == len(minus_b), 'endpoint shapes differ')
    require(all(plus_A[i] == minus_A[i] and plus_b[i] == minus_b[i]
                for i in range(len(plus_b)) if i not in affected),
            'unexpected indicator-dependent system row')
    def mixed(signs):
        require(len(signs) == tail and all(type(e) is int and e in (-1, 1) for e in signs),
                'invalid second-indicator vector')
        A, b = list(plus_A), list(plus_b)
        for j, sign in enumerate(signs):
            if sign == -1:
                for index in (start+2*j, start+2*j+1):
                    A[index], b[index] = minus_A[index], minus_b[index]
        return A, b
    test = [1, -1, 1, -1, 1]
    direct_A, direct_b, direct_keep = ci.pruned_system(R, data, L, test, 6, pruning)
    mixed_A, mixed_b = mixed(test)
    require(mixed_A == direct_A and mixed_b == direct_b and direct_keep == plus_keep,
            'mixed endpoint reconstruction disagrees with inherited system builder')
    return mixed

def verify(args):
    import sympy as s
    started = time.monotonic()
    root = source_root(args.source_root)
    modules, source_hashes = load_dependencies(root)
    ht, ci = modules['higher_traces'], modules['character_induction']
    R = load_tensor()
    cert = read_json(args.certificate)
    require(cert['id'] == RING_ID and cert['scope'] == 'pseudo_unitary' and cert['height'] == 6,
            'wrong induction certificate metadata')
    require(cert['tensor_sha256'] == TENSOR_SHA256, 'induction tensor hash mismatch')
    frames, enumeration = frames_exact(R)
    require(cert['enumeration'] == enumeration, 'enumeration receipt differs')
    require(len(cert['branches']) == 4 and [b['rows'] for b in cert['branches']] == frames,
            'missing or altered induction frames')
    general = dimension_reduction(R)
    old_low_matrices = ht.low_matrices
    try:
        # The complete low-frame domain was reconstructed above; supply it here.
        ht.low_matrices = lambda *a, **kw: frames
        data = ht.quadratic_data(R, gram_prune=True)
    finally:
        ht.low_matrices = old_low_matrices
    require(data is not None and data['q'] == 273 and data['lows'] == frames,
            'quadratic induction data differs')
    table = ci.CharacterTable(R, data)
    signs = list(map(list, itertools.product((-1, 1), repeat=5)))
    checked = []
    native = importlib.import_module('gram_vectors_general')
    require(Path(native.__file__).resolve() == BUNDLE/'gram_vectors_general.py',
            'native Gram adapter must come from this bundle')
    with tempfile.TemporaryDirectory(prefix='r6_9_1060_native_') as build_dir:
        native.BUILD_DIRECTORY = Path(build_dir)
        for frame_index, (rows, branch) in enumerate(zip(frames, cert['branches'])):
            L = s.Matrix(rows).T
            _, high = ht.high_columns(data, L)
            pruning = table.galois_pruning(rows, high)
            require(pruning == branch['galois'] and not pruning['missing_low'],
                    'high-column Galois pruning differs')
            require([case['ep'] for case in branch['cases']] == signs,
                    'all 32 second-indicator vectors must be present, without parity restrictions')
            systems = endpoint_systems(ci, R, data, L, pruning)
            for case in branch['cases']:
                A, b = systems(case['ep'])
                ray = case['y']
                require(isinstance(ray, list) and len(ray) == len(b) and
                        all(type(value) is int for value in ray), 'invalid integer ray shape')
                ci.check_farkas(A, b, ray)
                value = sum(x*y for x, y in zip(b, ray))
                require(type(case['bTy']) is int and value == case['bTy'] and value < 0,
                        'incorrect Farkas right-hand-side product')
                checked.append({'frame': frame_index, 'ep': case['ep'], 'bTy': value,
                                'rows': len(A), 'columns': len(A[0])})
            print(f'VERIFIED frame {frame_index}: all 32 indicator vectors', flush=True)
    require(len(checked) == 128, 'expected 128 exact systems')
    return {'status': 'verified', 'id': RING_ID, 'scope': 'general',
            'tensor_sha256': TENSOR_SHA256, 'enumeration': enumeration,
            'general_dimension_reduction': general, 'systems': checked,
            'optimizer_used': False, 'python_optimization_level': sys.flags.optimize,
            'canonical_source_hashes': source_hashes,
            'seconds': time.monotonic()-started}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-root', help='canonical package root (contains software/)')
    parser.add_argument('--certificate', type=Path, default=BUNDLE/'certificate.json')
    parser.add_argument('--report', type=Path, help='optional JSON replay report destination')
    args = parser.parse_args()
    try:
        result = verify(args)
    except Exception as error:
        print(f'REJECTED: {type(error).__name__}: {error}', file=sys.stderr, flush=True)
        return 2
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(result, indent=2)+'\n')
    print(f"VERIFIED GENERAL EXCLUSION: {len(result['systems'])} exact systems", flush=True)
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
