#!/usr/bin/env python3
"""Exact, interruptible necessary B3 spectral test for the R155 modular candidate.

Python 3.9+, standard library only. No representation or category is constructed.
Every constituent size is permitted; a timeout is UNKNOWN, never an exclusion.
"""
import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import json
from math import gcd
from pathlib import Path
import time

HERE = Path(__file__).resolve().parent
DATA_SHA256 = '769250938d8bd0c8a251aaacc18832174af8175ed9b44fc487ec3f6d04357353'
MOD = 144
ALGORITHM = 'bjt-scott-all-constituents-v1'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def save(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + '.tmp')
    temporary.write_text(json.dumps(value, indent=2) + '\n')
    temporary.replace(path)


class Cyclotomic:
    """Z[z]/(z^d-z^(d/2)+1), for (order,d)=(24,8),(72,24)."""
    def __init__(self, order, degree):
        self.order, self.degree = order, degree
        self.zero = (0,) * degree
        self.one = (1,) + (0,) * (degree - 1)
        powers = [self.one]
        for _ in range(1, order):
            powers.append(self.reduce([0] + list(powers[-1])))
        self.powers = powers
        require(self.reduce([0] + list(powers[-1])) == self.one, 'cyclotomic period')

    def reduce(self, values):
        out = list(values) + [0] * max(0, self.degree - len(values))
        for i in range(len(out) - 1, self.degree - 1, -1):
            c = out[i]
            out[i - self.degree // 2] += c
            out[i - self.degree] -= c
        return tuple(out[:self.degree])

    def multiply(self, left, right):
        out = [0] * (2 * self.degree - 1)
        for i, a in enumerate(left):
            if a:
                for j, b in enumerate(right):
                    if b:
                        out[i + j] += a * b
        return self.reduce(out)

    def rotate(self, value, exponent):
        return self.multiply(value, self.powers[exponent % self.order])

    def conjugate(self, value):
        out = [0] * self.degree
        for i, coefficient in enumerate(value):
            for j, c in enumerate(self.powers[-i % self.order]):
                out[j] += coefficient * c
        return tuple(out)


def add_scaled(out, value, scalar=1):
    for i, coefficient in enumerate(value):
        out[i] += scalar * coefficient


class Input:
    def __init__(self, data):
        self.N, self.twists, self.dual = data['fusion'], data['twists_mod24'], data['duality']
        self.unit = data['unit']
        self.n = len(self.N)
        self.ring24, self.ring72 = Cyclotomic(24, 8), Cyclotomic(72, 24)
        self.second = {(r['base'], r['target'][0], r['target'][1]): tuple(r['multiplicities'])
                       for r in data['second_indicator_rows']}
        fractions = [[[Fraction(c) for c in reversed(v)] for v in row]
                     for row in data['normalized_S_descending']]
        denominator = 1
        for row in fractions:
            for v in row:
                for c in v:
                    denominator = denominator * c.denominator // gcd(denominator, c.denominator)
        self.denominator = denominator
        self.S = [[tuple(int(c * denominator) for c in v) + (0,) * (8-len(v))
                   for v in row] for row in fractions]
        require(len(self.S) == self.n and all(len(row) == self.n for row in self.S), 'S size')
        for a in range(self.n):
            require(self.twists[self.dual[a]] == self.twists[a], 'dual twist')
            for b in range(self.n):
                require(len(self.N[a][b]) == self.n, 'fusion size')
                require(all(type(x) is int and x >= 0 for x in self.N[a][b]), 'fusion entry')
                require(sum(self.second[a, b, self.unit]) == self.N[a][a][b], 'self-braiding dimension')
        self.left = [self.ring24.rotate(self.S[self.unit][d], 3*self.twists[d])
                     for d in range(self.n)]
        self.right = [[self.ring24.rotate(self.ring24.conjugate(self.S[b][e]), -3*self.twists[e])
                       for e in range(self.n)] for b in range(self.n)]

    def dimension(self, a, b):
        return sum(self.N[a][a][c] * self.N[c][a][b] for c in range(self.n))

    def beta_trace(self, a, b):
        # BJT Cor.4.1: theta_a^-1 sum S_1d conj(S_be)(theta_d/theta_e)^3 N_de^a.
        out = [0] * 8
        for d in range(self.n):
            for e in range(self.n):
                if self.N[d][e][a]:
                    add_scaled(out, self.ring24.multiply(self.left[d], self.right[b][e]), self.N[d][e][a])
        return self.ring24.rotate(out, -self.twists[a])  # denominator is denominator^2

    def spectra(self, a, b):
        dimension = self.dimension(a, b)
        A = Counter()
        for c in range(self.n):
            for sign, multiplicity in enumerate(self.second[a, c, self.unit]):
                exponent = 3*((self.twists[c]-2*self.twists[a]+24*sign) % 48)
                A[exponent] += multiplicity * self.N[c][a][b]
        A = sorted((e, m) for e, m in A.items() if m)
        offset = self.twists[b] - 3*self.twists[a]
        # BJT Proposition4.2, using the reciprocal target (b,a*) already in the input.
        dm = self.second[a, b, self.dual[a]]
        D = sorted((3*((offset+24*s) % 48), m) for s, m in enumerate(dm))
        require(sum(m for _, m in A) == sum(dm) == dimension, 'A/Delta dimensions')
        trace24 = self.beta_trace(a, b)
        trace72 = [0] * 24
        for i, c in enumerate(trace24):
            trace72[3*i] = c
        inverse_trace72 = self.ring72.conjugate(trace72)
        denominator = 3*self.denominator**2
        B = []
        for j in range(3):
            exponent = (offset+24*j) % 72
            numerator = [0] * 24
            numerator[0] = dimension*self.denominator**2
            add_scaled(numerator, self.ring72.rotate(trace72, -exponent))
            add_scaled(numerator, self.ring72.rotate(inverse_trace72, exponent))
            require(all(c == 0 for c in numerator[1:]),
                    f'beta multiplicity is not rational: a={a}, b={b}, root={j}, numerator={numerator}, denominator={denominator}')
            require(numerator[0] >= 0 and numerator[0] % denominator == 0,
                    f'beta multiplicity is not a nonnegative integer: a={a}, b={b}, root={j}, numerator={numerator[0]}, denominator={denominator}')
            B.append((2*exponent, numerator[0]//denominator))
        B.sort()
        require(sum(m for _, m in B) == dimension, 'beta dimension')
        # Verify that the recovered multiplicities reconstruct the exact trace.
        recovered = [0] * 24
        for exponent, multiplicity in B:
            add_scaled(recovered, self.ring72.powers[exponent//2], multiplicity*self.denominator**2)
        require(tuple(recovered) == tuple(trace72), 'beta trace reconstruction')
        return A, B, D


def canonical(spectra):
    # Simultaneously A -> z^-e A, B -> z^-2e B, D -> z^-3e D.
    candidates = []
    for shift, _ in spectra[0]:
        candidates.append(tuple(tuple(sorted(((e-degree*shift) % MOD, m) for e, m in row))
                                for row, degree in zip(spectra, (1, 2, 3))))
    return min(candidates)


def admissible(exponents, counts):
    """Necessary conditions on ONE irreducible Jordan-Hoelder constituent."""
    a, b, d = counts
    r = sum(a)
    if r == 0 or sum(b) != r or sum(d) != r:
        return False
    determinant = sum(e*m for e, m in zip(exponents[0], a))
    determinant += sum(e*m for e, m in zip(exponents[1], b))
    determinant -= sum(e*m for e, m in zip(exponents[2], d))
    if determinant % MOD:
        return False
    if r == 1:
        return True
    maxima = [max(row) for row in counts]
    if any(maxima[i]+maxima[j] > r for i, j in ((0,1),(0,2),(1,2))):
        return False
    if sum(m*m for row in counts for m in row) > r*r+2:
        return False
    # Scott on the original space, after scalar normalization of the triple.
    d_lookup = dict(zip(exponents[2], d))
    for ea, ma in zip(exponents[0], a):
        if ma:
            for eb, mb in zip(exponents[1], b):
                if mb and ma+mb+d_lookup.get((ea+eb) % MOD, 0) > r:
                    return False
    return True


class BudgetExceeded(Exception):
    pass


class Search:
    def __init__(self, profile, seconds, max_states):
        self.exponents = tuple(tuple(e for e, _ in row) for row in profile)
        self.initial = tuple(tuple(m for _, m in row) for row in profile)
        self.deadline = time.monotonic()+seconds if seconds > 0 else float('inf')
        self.max_states = max_states
        self.failed = set()
        self.calls = self.candidates = self.ticks = 0

    def guard(self):
        self.ticks += 1
        if self.ticks % 128 == 0 and time.monotonic() >= self.deadline:
            raise BudgetExceeded('time limit')

    def compositions(self, bounds, total, pivot=None):
        suffix = [0]*(len(bounds)+1)
        for i in range(len(bounds)-1, -1, -1):
            suffix[i] = suffix[i+1]+bounds[i]
        out = [0]*len(bounds)
        def walk(i, left):
            self.guard()
            if i == len(bounds):
                if left == 0:
                    yield tuple(out)
                return
            low = max(0, left-suffix[i+1], int(i == pivot))
            high = min(bounds[i], left)
            for value in range(low, high+1):
                out[i] = value
                yield from walk(i+1, left-value)
        yield from walk(0, total)

    def constituents(self, state):
        aa, bb, dd = state
        n = sum(aa)
        pivot = next(i for i, m in enumerate(aa) if m)
        for r in range(1, n+1):
            # D has at most two eigenvalues, so rank-pair inequality bounds A.
            a_bounds = aa if r == 1 else tuple(min(x, r//2) for x in aa)
            if a_bounds[pivot] == 0 or sum(a_bounds) < r:
                continue
            for a in self.compositions(a_bounds, r, pivot):
                a_square = sum(x*x for x in a)
                for b in self.compositions(bb, r):
                    self.guard()
                    if r > 1 and max(a)+max(b) > r:
                        continue
                    low, high = max(0, r-dd[0]), min(r, dd[1])
                    for d1 in range(low, high+1):
                        self.guard()
                        d = (r-d1, d1)
                        if r > 1 and a_square+sum(x*x for x in b)+sum(x*x for x in d) > r*r+2:
                            continue
                        candidate = (a, b, d)
                        self.candidates += 1
                        if admissible(self.exponents, candidate):
                            yield candidate

    def solve(self, state=None):
        if state is None:
            state = self.initial
        self.guard()
        self.calls += 1
        if sum(state[0]) == 0:
            return []
        if state in self.failed:
            return None
        # This shortcut accepts only a necessary spectral pattern, not an irrep.
        if admissible(self.exponents, state):
            return [state]
        for part in self.constituents(state):
            remainder = tuple(tuple(x-y for x, y in zip(row, taken)) for row, taken in zip(state, part))
            answer = self.solve(remainder)
            if answer is not None:
                return [part]+answer
        self.failed.add(state)
        if self.max_states and len(self.failed) > self.max_states:
            raise BudgetExceeded('failed-state memory limit')
        return None

    def verify_witness(self, witness):
        require(all(admissible(self.exponents, part) for part in witness), 'invalid constituent witness')
        totals = tuple(tuple(sum(part[j][i] for part in witness) for i in range(len(row)))
                       for j, row in enumerate(self.initial))
        require(totals == self.initial, 'witness does not partition all three spectra')


def self_test():
    control_bytes = (HERE/'su2_4_control.json').read_bytes()
    require(hashlib.sha256(control_bytes).hexdigest() == 'cd2a7680a01f2ba9fce795c69260e51f653c9a0333207c88b3492c74db4193f0',
            'known-category control hash')
    known = Input(json.loads(control_bytes))
    # Known SU(2)_4 a=b=label1, from actual R/F matrices, in zeta144 units.
    profile = (((6,1),(54,1)), ((36,1),(84,1),(132,0)), ((54,1),(126,1)))
    require(tuple(tuple(row) for row in known.spectra(1,1)) == profile, 'SU2_level4 exact dimension2 spectra')
    profile3 = (((24,1),(48,1),(96,1)), ((16,1),(64,1),(112,1)), ((24,1),(96,2)))
    require(tuple(tuple(row) for row in known.spectra(2,2)) == profile3, 'SU2_level4 exact dimension3 spectra')
    control3 = Search(profile3, 2, 1000)
    answer3 = control3.solve()
    require(answer3 is not None, 'SU2_level4 dimension3 positive control')
    control3.verify_witness(answer3)
    search = Search(profile, 2, 1000)
    answer = search.solve()
    require(answer is not None, 'SU(2)_4 positive control')
    search.verify_witness(answer)
    doubled = tuple(tuple((e, 2*m) for e, m in row) for row in profile)
    reducible = Search(doubled, 2, 1000)
    answer = reducible.solve()
    require(answer is not None and len(answer) > 1, 'reducible positive control')
    reducible.verify_witness(answer)
    # Central scalar1; A=identity^2, B=nontrivial third roots, D=identity^2.
    # The whole determinant passes, but no one- or two-dimensional partition can.
    impossible = (((0,2),), ((0,0),(48,1),(96,1)), ((0,2),(72,0)))
    negative = Search(impossible, 2, 1000)
    require(negative.solve() is None, 'strictly stronger than determinant control')
    bounded = Search(impossible, 1, 1000)
    bounded.deadline = -1
    bounded.ticks = 127
    try:
        bounded.solve()
    except BudgetExceeded:
        pass
    else:
        raise ValueError('timeout control')
    return {'status':'PASS','controls':['SU2_level4_exact_spectra_dimensions2_and3','SU2_level4_positive','reducible_SU2_level4_positive','determinant_passes_Scott_partition_fails','timeout_is_unknown']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data', type=Path, default=HERE/'r155_data.json')
    parser.add_argument('--output', type=Path, default=Path('r155_braid_results.json'))
    parser.add_argument('--seconds-per-block', type=float, default=30)
    parser.add_argument('--budget-seconds', type=float, default=600)
    parser.add_argument('--max-states', type=int, default=50000)
    parser.add_argument('--min-dimension', type=int, default=5)
    parser.add_argument('--max-dimension', type=int, default=308)
    parser.add_argument('--only', help='one zero-based pair a,b, e.g.4,20')
    parser.add_argument('--resume', action='store_true')
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    if args.self_test:
        print(json.dumps(self_test(), indent=2))
        return
    require(args.seconds_per_block >= 0 and args.budget_seconds >= 0 and args.max_states >= 0, 'negative budget')
    raw = args.data.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == DATA_SHA256, 'input data hash mismatch')
    source = Input(json.loads(raw))
    if args.output.exists():
        require(args.resume, 'output exists; use --resume or another --output')
        report = json.loads(args.output.read_text())
        require(report['data_sha256'] == DATA_SHA256 and report['algorithm'] == ALGORITHM, 'incompatible checkpoint')
    else:
        report = {'algorithm':ALGORITHM,'data_sha256':DATA_SHA256,'modulus':MOD,'results':{},
                  'scope':'Necessary B3 spectral compatibility for the retained positive-ribbon rank26 modular candidate. Passing is not a model. A candidate obstruction requires independent exact replay before any classification change.'}
    deadline = time.monotonic()+args.budget_seconds if args.budget_seconds else float('inf')
    only = tuple(map(int, args.only.split(','))) if args.only else None
    if only is not None:
        require(len(only) == 2 and all(0 <= v < source.n for v in only), 'invalid pair')
    blocks = sorted((source.dimension(a,b), a,b) for a in range(source.n) for b in range(source.n)
                    if source.dimension(a,b) and (only == (a,b) if only else args.min_dimension <= source.dimension(a,b) <= args.max_dimension))
    reused = {}
    for row in report['results'].values():
        if row['verdict'] == 'PASS_NECESSARY':
            reused[row['profile_sha256']] = row['witness']
    for dimension, a,b in blocks:
        key = str(a)+','+str(b)
        previous = report['results'].get(key)
        if previous and previous['verdict'] in ('PASS_NECESSARY','CANDIDATE_OBSTRUCTION'):
            continue
        if time.monotonic() >= deadline:
            break
        started = time.monotonic()
        try:
            profile = canonical(source.spectra(a,b))
        except ValueError as exc:
            report['results'][key] = {'a':a,'b':b,'dimension':dimension,
                                      'verdict':'ERROR_REQUIRES_REVIEW','reason':str(exc)}
            save(args.output, report)
            print(f'{a},{b} ERROR_REQUIRES_REVIEW: {exc}', flush=True)
            continue
        profile_sha = digest(profile)
        seconds = min(args.seconds_per_block or float('inf'), max(0.001, deadline-time.monotonic()))
        search = Search(profile, seconds, args.max_states)
        row = {'a':a,'b':b,'dimension':dimension,'profile_sha256':profile_sha,'spectra_mod144':profile}
        try:
            witness = reused.get(profile_sha)
            if witness is None:
                witness = search.solve()
            if witness is None:
                row.update(verdict='CANDIDATE_OBSTRUCTION',search_exhaustive=True,
                           failed_states_sha256=digest(sorted(search.failed)))
            else:
                search.verify_witness(witness)
                row.update(verdict='PASS_NECESSARY',witness=witness)
                reused[profile_sha] = witness
        except BudgetExceeded as exc:
            row.update(verdict='UNKNOWN',reason=str(exc),search_exhaustive=False)
        row.update(elapsed_seconds=round(time.monotonic()-started,6),states_proved_impossible=len(search.failed),
                   recursive_calls=search.calls,constituent_patterns_checked=search.candidates)
        report['results'][key] = row
        counts = Counter(v['verdict'] for v in report['results'].values())
        report['summary'] = {'recorded_blocks':len(report['results']),'verdicts':dict(counts),
                             'requested_blocks_this_run':len(blocks),'not_completed_this_run':sum(
                                 report['results'].get(str(x)+','+str(y),{}).get('verdict') not in ('PASS_NECESSARY','CANDIDATE_OBSTRUCTION')
                                 for _,x,y in blocks)}
        save(args.output, report)
        print(f'{a},{b} dimension={dimension} {row["verdict"]} {row["elapsed_seconds"]:.2f}s', flush=True)
    counts = Counter(v['verdict'] for v in report['results'].values())
    report['summary'] = {'recorded_blocks':len(report['results']),'verdicts':dict(counts),
                         'requested_blocks_this_run':len(blocks),'not_completed_this_run':sum(
                             report['results'].get(str(x)+','+str(y),{}).get('verdict') not in ('PASS_NECESSARY','CANDIDATE_OBSTRUCTION')
                             for _,x,y in blocks)}
    report['last_run_parameters'] = {'seconds_per_block':args.seconds_per_block,'budget_seconds':args.budget_seconds,
                                    'max_states':args.max_states,'min_dimension':args.min_dimension,
                                    'max_dimension':args.max_dimension,'only':only}
    save(args.output, report)
    print(json.dumps(report.get('summary',{'message':'No blocks completed; increase budget.'}), indent=2))
    print('Send back the complete JSON file:', args.output)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nInterrupted. Completed blocks are saved; rerun with --resume. The current block restarts.')
