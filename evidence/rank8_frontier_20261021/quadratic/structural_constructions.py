"""Complete subring audit and scoped construction obstructions for six residuals.

No whole-ring noncategorifiability is claimed.  Two equivariantization
obstructions and two generalized-near-group branches explicitly depend on
the repository's unrestricted rank-four theorem, pinned below.
"""
from pathlib import Path
import argparse
import hashlib
import itertools
import json
import sympy as s
from rank_two_and_models import TARGETS, exact_dimensions, generalized_near_group, need
from residual_split_1055 import run as split_1055

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RANK4_SOURCE = 'manuscripts/rank4/papers/companion_sections/14_finite_certification.tex'
RANK4_SHA = '0ec47c3c3da2c46bfee20b06214b9f7704edea841955cb2c86b7b0522f199e8b'


def fusion_subrings(R):
    dual = [next(j for j in range(8) if R[i][j][0]) for i in range(8)]
    accepted = []
    for mask in range(128):
        J = [0] + [i for i in range(1, 8) if mask & (1 << (i-1))]
        if any(dual[i] not in J for i in J):
            continue
        if any(R[i][j][k] for i in J for j in J for k in range(8) if k not in J):
            continue
        accepted.append(J)
    return accepted


def quotient_free_involution(R, g, dims):
    permutation = [next(k for k in range(8) if R[g][i][k]) for i in range(8)]
    need(all(R[g][i] == [int(k == permutation[i]) for k in range(8)] for i in range(8)),
         'involution must permute simples')
    need(all(permutation[permutation[i]] == i and permutation[i] != i for i in range(8)),
         'free involution required')
    orbits = sorted({tuple(sorted([i, permutation[i]])) for i in range(8)})
    need(len(orbits) == 4, 'wrong orbit rank')
    Q = [[[sum(R[a[0]][b[0]][k] for k in c) for c in orbits] for b in orbits] for a in orbits]
    # All orbit representative choices give the same quotient coefficient.
    need(all(sum(R[i][j][k] for k in c) == Q[a][b][h]
             for a,A in enumerate(orbits) for b,B in enumerate(orbits)
             for h,c in enumerate(orbits) for i in A for j in B), 'ill-defined quotient')
    qdims = [dims[o[0]] for o in orbits]
    qdual = [next(j for j in range(4) if Q[i][j][0]) for i in range(4)]
    need(all(Q[0][i][j] == int(i == j) and Q[i][0][j] == int(i == j)
             and Q[i][j][0] == int(j == qdual[i]) for i,j in itertools.product(range(4),repeat=2)),
         'quotient based-ring unit/duality failed')
    need(all(sum(Q[i][j][a]*Q[a][k][h] for a in range(4)) ==
             sum(Q[j][k][a]*Q[i][a][h] for a in range(4))
             for i,j,k,h in itertools.product(range(4), repeat=4)), 'quotient associativity failed')
    need(all(s.expand(qdims[i]*qdims[j]-sum(Q[i][j][k]*qdims[k] for k in range(4))) == 0
             for i,j in itertools.product(range(4), repeat=2)), 'quotient dimensions failed')
    D = s.expand(sum(d*d for d in dims)); baseD = s.expand(sum(d*d for d in qdims))
    need(s.expand(D-2*baseD) == 0 and baseD > 45, 'dimension bound failed')
    # 24 + 12 sqrt(3) < 45, since 21^2 > 12^2 * 3.
    need(21*21 > 12*12*3, 'rational upper comparison failed')
    return {'free_involution':g, 'orbits':[list(o) for o in orbits],
            'forced_equivariantization_base_rank':4, 'base_tensor':Q,
            'base_fp_dimensions':list(map(str, qdims)), 'base_global_dimension':str(baseD),
            'scope':'hypothetical C2-equivariantization or central Tannakian C2 condensation only',
            'outcome':'excluded_by_pinned_unrestricted_rank_four_dimension_bound'}


def run():
    rank4text = (ROOT/RANK4_SOURCE).read_bytes()
    need(hashlib.sha256(rank4text).hexdigest() == RANK4_SHA, 'rank-four theorem source changed')
    need(b'Every rank-four complex fusion category satisfies' in rank4text,
         'unrestricted rank-four theorem statement not found')
    split = split_1055()
    need(all(S[3] == [[-1,0],[0,-1]] for S in split['exact_simultaneous_representations']),
         'central Tannakian obstruction for 1055 failed')
    rows = {r['id']:r for r in json.loads((HERE.parents[1]/'rank8_m3_20261021/pipeline/census_m3.json').read_text())}
    records = []
    for index in TARGETS:
        row = rows[f'R8_3_{index}']; R = row['tensor']; dims = list(map(s.sympify,exact_dimensions(index)))
        digest = hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()
        need(digest == row['tensor_sha256'], 'tensor hash mismatch')
        need(all(d > 0 for d in dims) and all(s.expand(dims[i]*dims[j]-sum(R[i][j][k]*dims[k] for k in range(8))) == 0
             for i,j in itertools.product(range(8),repeat=2)), 'positive FP homomorphism failed')
        D = s.expand(sum(d*d for d in dims)); need(D.is_Rational is False, 'global dimension must be irrational')
        subrings = fusion_subrings(R); proper = [J for J in subrings if len(J) < 8]
        need(all(len(J) <= 2 and all(dims[i] == 1 for i in J) for J in proper), 'unexpected proper subring')
        item = {'id':row['id'], 'tensor_sha256':digest,
                'all_unit_containing_subsets_tested':128, 'fusion_subrings':subrings,
                'proper_subring_dimensions':[len(J) for J in proper], 'global_dimension':str(D),
                'faithful_nontrivial_finite_group_gradings':'excluded: neutral proper subring pointed, total FP dimension irrational',
                'nontrivial_finite_group_equivariantizations':None,
                'classification_status':'unresolved; these exclude construction routes only'}
        if all(len(J) == 1 for J in proper):
            item['nontrivial_finite_group_equivariantizations'] = {
                'outcome':'excluded', 'reason':'no proper nontrivial fusion subring can contain Rep(G); full ring nonintegral'}
        elif index == 1055:
            item['nontrivial_finite_group_equivariantizations'] = {
                'outcome':'excluded', 'only_possible_group':'C2',
                'reason':'central Tannakian quotient forces S_g=I, but all complete split solutions have S_g=-I',
                'split_complete_domain':split['reduced_simultaneous_domain'],
                'split_solution_count':split['representation_count'],
                'source':'residual_split_1055.py'}
        else:
            need(index in [1768,1795], 'unexpected rank-two proper subring')
            item['nontrivial_finite_group_equivariantizations'] = {
                'outcome':'excluded', 'only_possible_group':'C2',
                'rank_four_quotient':quotient_free_involution(R,1,dims)}
        branches=[]
        for branch in generalized_near_group(dims)['families']:
            if branch['base_rank'] == 4:
                k=branch['integer_dimension_multiplier']; baseD=s.expand(D/k)
                need(baseD > 45, 'rank-four base not beyond bound')
                branches.append({'integer_dimension_multiplier':k,
                                 'invertible_group_order':branch['invertible_group_order'],
                                 'base_rank':4, 'base_global_dimension':str(baseD),
                                 'outcome':'excluded_by_pinned_unrestricted_rank_four_dimension_bound'})
        item['additional_generalized_near_group_branches_excluded']=branches
        records.append(item)
    return {'kind':'complete_quadratic_subring_and_construction_audit',
            'rank_four_dependency':{'path':RANK4_SOURCE,'sha256':RANK4_SHA,
                'label':'finite:cor:sharp-bounds','statement':'Every rank-four complex fusion category has FPdim <= 24+12sqrt(3)',
                'scope':'repository theorem dependency, not independently re-proved by this verifier'},
            'records':records}


if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--write',action='store_true');a=p.parse_args()
    actual=run();path=HERE/'structural_constructions_results.json'
    if a.write:path.write_text(json.dumps(actual,indent=2)+'\n')
    else:need(json.loads(path.read_text()) == actual, 'saved structural evidence did not replay')
    print('PASS: complete subring, grading and equivariantization audits for six unresolved quadratic rings')
