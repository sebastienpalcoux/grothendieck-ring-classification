"""Complete rank-two based-module and generalized-near-group dimension searches.

Every domain is derived from a theorem, with no parameter cutoff.  Feasible
based modules are NOT module-category constructions or categorifications.
No general ring exclusion is claimed by this file.
"""
from pathlib import Path
import argparse
import hashlib
import itertools
import json
import math
import sympy as s

HERE = Path(__file__).resolve().parent
TARGETS = [1055, 1768, 1795, 3258, 3413, 3472]


def need(v, message):
    if not v:
        raise ValueError(message)


def exact_dimensions(index):
    a = 5 + s.sqrt(37)
    b = 6 + 3*s.sqrt(5)
    c = (5 + 3*s.sqrt(5))/2
    d = 6 + 5*s.sqrt(2)
    return {
        1055: [1, a, a, 1, a+1, a+1, a+2, a+2],
        1768: [1, 1, a, a+1, a+2, a+2, a+1, a],
        1795: [1, 1, b, b+1, b+1, b+1, b+1, b],
        3258: [1, c, c+1, c, c, c, c+2, c+2],
        3413: [1, c, c, c+1, c, c, c+2, c+2],
        3472: [1, d, d, d+1, d, d+2, d+2, d+2],
    }[index]


def rat(value):
    value = s.Rational(value)
    return [int(value.p), int(value.q)]


def matrix_json(M):
    return [[int(z) for z in row] for row in M.tolist()]


def rank_two(R, dims):
    # Choose a self-dual irrational generator.  The entire quadratic
    # dimension field acts faithfully on any rank-two based module.
    x = next(i for i, d in enumerate(dims) if not s.sympify(d).is_Rational and R[i][i][0])
    t = s.Symbol('t')
    p = s.Poly(s.minpoly(dims[x], t), t)
    need(p.degree() == 2, 'quadratic FP field required')
    lead, negative_trace, norm = map(s.Rational, p.all_coeffs())
    need(lead == 1 and negative_trace.q == norm.q == 1, 'integral quadratic dimensions required')
    T, U = -int(negative_trace), int(norm)
    z = s.Symbol('z')
    # Solve affine expressions in the chosen irrational generator over QQ.
    coords = []
    field = s.QQ.algebraic_field(dims[x])
    for dim in dims:
        coeff = field.from_sympy(dim).to_list()
        coeff = [s.Rational(c.numerator, c.denominator) for c in coeff]
        coeff = [s.Rational(0)] * (2-len(coeff)) + coeff
        slope, intercept = coeff
        need(s.simplify(slope*dims[x] + intercept - dim) == 0, 'field coordinates failed')
        coords.append((intercept, slope))
    tested, solutions = 0, []
    for diagonal in range(T+1):
        tested += 1
        other = T-diagonal
        square = diagonal*other-U
        if square <= 0:
            continue
        off = math.isqrt(square)
        if off*off != square or diagonal < other:
            continue  # representative under swapping the two module vertices
        B = s.Matrix([[diagonal, off], [off, other]])
        matrices = [intercept*s.eye(2) + slope*B for intercept, slope in coords]
        if any(not z.is_Integer or z < 0 for M in matrices for z in M):
            continue
        dual = [next(j for j in range(8) if R[i][j][0]) for i in range(8)]
        need(all(matrices[dual[i]] == matrices[i].T for i in range(8)), 'based-module duality failed')
        need(all(matrices[i]*matrices[j] == sum((R[i][j][k]*matrices[k] for k in range(8)), s.zeros(2))
                 for i,j in itertools.product(range(8), repeat=2)), 'based-module multiplication failed')
        need(matrices[0] == s.eye(2) and off > 0, 'module not unital/connected')
        solutions.append({'generator_matrix': matrix_json(B),
                          'action_matrices': [matrix_json(M) for M in matrices],
                          'internal_end_candidates': [[int(M[v,v]) for M in matrices] for v in range(2)]})
    return {'scope': 'all connected rank-two based modules, up to vertex permutation',
            'reference_basis_index': x, 'dimension_minpoly': [1,-T,U],
            'complete_diagonal_domain': [0,T], 'tested_diagonal_values': tested,
            'affine_dimension_coordinates': [{'constant':rat(a),'slope':rat(b)} for a,b in coords],
            'classes': solutions, 'class_count': len(solutions),
            'outcome': 'exact_feasible_based_modules_not_categorifications'}


def generalized_near_group(dims):
    D = s.expand(sum(s.sympify(d)**2 for d in dims))
    t = s.Symbol('t')
    p = s.Poly(s.minpoly(D,t),t)
    need(p.degree()==2, 'quadratic global FP dimension required')
    A = -p.all_coeffs()[1]/2
    norm = p.all_coeffs()[2]
    G = s.cancel(norm/(2*A))
    families = []
    if G.is_Integer and G > 0:
        G = int(G)
        # An integer multiplier k includes pointed products and any tower
        # of extensions/equivariantizations; subsequent Morita equivalence
        # preserves FP dimension. Necessarily k divides G.
        for multiplier in s.divisors(G):
            group_order = G // multiplier
            for stabilizer in s.divisors(group_order):
                orbit = group_order // stabilizer
                K2 = s.cancel(2*A/(multiplier*orbit) - 4*stabilizer)
                if not K2.is_Integer or K2 < 0:
                    continue
                K = math.isqrt(int(K2))
                if K*K != K2:
                    continue
                delta = (K+s.sqrt(K*K+4*stabilizer))/2
                need(s.simplify(multiplier*orbit*(stabilizer+delta**2)-D)==0,'model dimension mismatch')
                rank_two_excluded = group_order == orbit == stabilizer == 1 and K > 1
                families.append({'integer_dimension_multiplier': int(multiplier),
                                 'invertible_group_order': group_order,
                                 'stabilizer_order': int(stabilizer),
                                 'noninvertible_orbit_size': orbit,
                                 'total_noninvertible_multiplicity': K,
                                 'base_rank': group_order+orbit,
                                 'base_rank_two_classification_excludes': rank_two_excluded,
                                 'status': 'impossible_rank_two_base' if rank_two_excluded else
                                           'dimension_match_only_no_model_or_Morita_equivalence'})
    return {'global_dimension':str(D),'global_dimension_minpoly':[rat(c) for c in p.all_coeffs()],
            'forced_group_order_before_integer_multiplier':rat(G),
            'scope':'all generalized-near-group base dimensions, arbitrary finite-group extensions/equivariantizations/pointed products and Morita equivalence; no de-equivariantization division',
            'finite_domain_justification':'k divides G=Norm(D)/Trace(D); stabilizer divides G/k; K squared then uniquely determined',
            'families':families,
            'outcome':'family_dimension_excluded' if not families else 'finite_family_dimension_matches_only'}


def run():
    rows={r['id']:r for r in json.loads((HERE.parents[1]/'rank8_m3_20261021/pipeline/census_m3.json').read_text())}
    out=[]
    for index in TARGETS:
        row=rows[f'R8_3_{index}'];R=row['tensor'];dims=list(map(s.sympify,exact_dimensions(index)))
        digest=hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()
        need(digest==row['tensor_sha256'],'tensor hash mismatch')
        need(all(d>0 for d in dims),'FP dimensions not positive')
        need(all(s.expand(dims[i]*dims[j]-sum(R[i][j][k]*dims[k] for k in range(8)))==0
                 for i,j in itertools.product(range(8),repeat=2)),'FP dimension homomorphism failed')
        out.append({'id':row['id'],'tensor_sha256':digest,'exact_fp_dimensions':list(map(str,dims)),
                    'rank_two_module_search':rank_two(R,dims),
                    'generalized_near_group_model_search':generalized_near_group(dims),
                    'classification_status':'unresolved; based modules and dimension matches are not models'})
    return {'kind':'complete_quadratic_rank_two_modules_and_generalized_near_group_dimension_search',
            'records':out}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--write',action='store_true')
    args=parser.parse_args();actual=run();path=HERE/'rank_two_and_models_results.json'
    if args.write:path.write_text(json.dumps(actual,indent=2)+'\n')
    else:need(json.loads(path.read_text())==actual,'saved evidence did not replay')
    print('PASS: complete rank-two based-module and unbounded-family dimension searches for six quadratic residuals')
