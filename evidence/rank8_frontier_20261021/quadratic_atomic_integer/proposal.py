"""Numerical proposals for an exact bounded integer necessary system.

Only an integer vector checked against the complete exact system is a
mathematical result. In particular, a numerical infeasibility status is
never an exclusion certificate.
"""
import math


def propose(system, seconds, exact_check):
    import numpy as np
    from scipy.optimize import Bounds, LinearConstraint, milp
    from scipy.sparse import csc_matrix

    rows = len(system.rhs)
    variables = len(system.columns)
    scales = [max(1, abs(b)) for b in system.rhs]
    for column in system.columns:
        for i, value in enumerate(column):
            scales[i] = max(scales[i], abs(value))
    values, indices, starts = [], [], [0]
    for column in system.columns:
        for i, value in enumerate(column):
            if value:
                values.append(float(value / scales[i]))
                indices.append(i)
        starts.append(len(values))
    matrix = csc_matrix((np.asarray(values), np.asarray(indices, dtype=np.int32),
                         np.asarray(starts, dtype=np.int32)),
                        shape=(rows, variables))
    target = np.asarray([float(b / scale) for b, scale in zip(system.rhs, scales)])
    print('MILP proposal', rows, 'rows', variables, 'integer variables',
          len(values), 'nonzeros', 'limit', seconds, flush=True)
    answer = milp(np.zeros(variables), integrality=np.ones(variables),
                  bounds=Bounds(np.zeros(variables), np.asarray(system.bounds, dtype=float)),
                  constraints=LinearConstraint(matrix, target, target),
                  options={'time_limit': float(seconds), 'presolve': True})
    result = {'method': 'scipy_highs_bounded_integer_proposal',
              'seconds_limit': seconds, 'solver_status': int(answer.status),
              'solver_message': str(answer.message),
              'numerical_infeasibility_is_not_a_certificate': True,
              'conclusion': 'no_exact_integer_witness_found'}
    if answer.x is None:
        return result
    if not all(math.isfinite(float(x)) for x in answer.x):
        result['candidate_rejection'] = 'nonfinite numerical entry'
        return result
    integer = [int(round(float(x))) for x in answer.x]
    result['maximum_rounding_distance'] = max(abs(float(x) - n)
                                               for x, n in zip(answer.x, integer))
    try:
        exact_check(system, integer)
    except (ValueError, AssertionError) as error:
        result['candidate_rejection'] = str(error)
        total = [0] * rows
        for value, column in zip(integer, system.columns):
            if value:
                for i, coefficient in enumerate(column):
                    total[i] += value * coefficient
        result['failed_exact_row_count'] = sum(a != b for a, b in zip(total, system.rhs))
        result['violated_bounds'] = sum(not 0 <= value <= upper
                                         for value, upper in zip(integer, system.bounds))
        return result
    result.update(conclusion='exact_integer_feasible_relaxation',
                  integer_values=integer)
    return result
