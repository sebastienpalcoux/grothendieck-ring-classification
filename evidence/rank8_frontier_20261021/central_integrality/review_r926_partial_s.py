"""Independent checks of the new R926 partial-S layer and whole-column rays.

The certified domain and character reconstruction are shared with the
producer. This audit independently recalculates every eigenvalue-integrality
test, enumerates flat character-label permutations (not the producer's
backtracking), and scans every actual cone column (not its factorized oracle).
The separate producer replay checks the complete oriented general lift.
"""
from pathlib import Path
import argparse
import hashlib
import itertools
import json
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'global_induction'))
import spectral_frame
import partial_s
import streaming as st


def need(ok, message):
    if not ok:
        raise ValueError(message)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    source = st.load_ring('R8_3_926')
    path = st.HERE / 'spectral_results/R8_3_926_h4.json'
    saved = json.loads(path.read_text())
    need(saved['tensor_sha256'] == source['tensor_sha256'], 'Source tensor identity')
    pseudo = saved['certificate']['general']['sphere']['pseudo']
    R = source['tensor']
    a = st.old.setup(R)
    T = partial_s.Table(R, a)
    K = T.K
    C = spectral_frame.SpectralFrameCone(R, 4)
    need(C.meta == pseudo['metadata'], 'Certified domain identity')
    values = {}

    def data(v):
        v = tuple(v)
        if v not in values:
            dim = sum((K(n) * d for n, d in zip(v, T.ds)), K.zero)
            evaluations = [sum((K(n) * d for n, d in zip(v, character)), K.zero)
                           for character in T.characters]
            entries = [T.D * x / f for x, f in zip(evaluations, T.codegrees)]
            values[v] = dim, entries
        return values[v]

    def allowed(v):
        dim, entries = data(v)
        return all(all(co.denominator == 1 for co in (entry / dim).to_list()) for entry in entries)

    independently_kept_high = []
    rejected_high = 0
    for vector, dimension in a['high']:
        if allowed((0,) + tuple(vector)):
            independently_kept_high.append((vector, dimension))
        else:
            rejected_high += 1
    need(independently_kept_high == C.a['high'], 'All high-column filters independently agree')
    need(all(allowed(v) for columns in a['columns'] for v in columns), 'No hidden low-column rejection')
    import low_frames_rank8 as native
    frames = native.low_matrices(a['columns'], a['B'], gram_prune=True)
    need(len(frames) == 6891, 'Complete low-frame count')
    dimensions = [data(v)[0] for v in frames[0]]
    permutations = [p for p in itertools.permutations(range(8))
                    if all(T.beta[E] == d for E, d in zip(p, dimensions))]
    need(len(permutations) == 24, 'Complete dimension-compatible label permutations')
    kept, assignments = [], []
    for index, frame in enumerate(frames):
        need([data(v)[0] for v in frame] == dimensions, 'Frame dimension order')
        entries = [data(v)[1] for v in frame]
        labels = [list(p) for p in permutations
                  if all(entries[j][p[i]] == entries[i][p[j]]
                         for i, j in itertools.combinations(range(8), 2))]
        if labels:
            kept.append(index)
            assignments.append(labels)
    need(kept == C.meta['retained_frame_indices'], 'All low-frame labels independently agree')
    need(assignments == C.meta['symmetric_character_assignments'], 'Complete symmetric assignments')
    ray_results = []
    for case in pseudo['cases']:
        y = case['y']
        minimum = None
        for index in range(C.nvars):
            value = sum(y[row] * coefficient for row, coefficient in C.column(index).items())
            need(value >= 0, 'Direct column violates certificate')
            minimum = value if minimum is None else min(minimum, value)
        rhs_value = sum(x * z for x, z in zip(C.rhs_for(case['indicators']), y))
        need(rhs_value == case['bTy'] < 0, 'Strict exact separation')
        ray_results.append({'indicators': case['indicators'], 'columns_checked': C.nvars,
                            'minimum_column_pairing': minimum, 'rhs_pairing': rhs_value})
    result = {'id': source['id'], 'tensor_sha256': source['tensor_sha256'],
              'certificate_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
              'status': 'PASS', 'scope': 'new partial-S layer and direct whole-domain ray audit',
              'character_count': 8, 'original_high_columns': len(a['high']),
              'rejected_high_columns': rejected_high, 'retained_high_columns': len(C.a['high']),
              'low_frames': len(frames), 'dimension_label_permutations': len(permutations),
              'retained_frames': kept, 'ray_checks': ray_results,
              'general_scope': 'Complete oriented lift is checked separately by spectral_generation.py --verify.'}
    target = HERE / 'review_r926_partial_s.json'
    if args.write:
        target.write_text(json.dumps(result, indent=2) + '\n')
    else:
        need(result == json.loads(target.read_text()), 'Recorded audit differs')
    print('PASS R926 independent partial-S/permutation/direct-column audit:',
          rejected_high, 'high rejections;', len(frames), 'frames;', len(kept),
          'retained;', len(ray_results), 'whole-domain rays')


if __name__ == '__main__':
    main()
