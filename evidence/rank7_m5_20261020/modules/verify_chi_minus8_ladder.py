"""Independent exact finite checks supplementing the all-level proof."""
import json
from pathlib import Path
import sympy as s

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def chi(value):
    return {1: 1, 3: 1, 5: -1, 7: -1}[value % 8]

def check(modulus):
    points = [(p, q) for p in range(modulus) for q in range(modulus)
              if p % 2 or q % 2]
    index = {point: i for i, point in enumerate(points)}
    size = len(points)

    def action(a, b, c, d):
        return s.SparseMatrix(size, size, {
            (i, index[((a*p+b*q) % modulus, (c*p+d*q) % modulus)]): 1
            for i, (p, q) in enumerate(points)})

    S = action(0, -1, 1, 0)
    T = action(1, 1, 0, 1)
    zero = s.SparseMatrix(size, size, {})
    PU = sum((T**k for k in range(modulus)), zero) / modulus
    units = list(range(1, modulus, 2))
    Pchi = sum((chi(a)*action(a, 0, 0, pow(a, -1, modulus))
                for a in units), zero) / len(units)
    P = PU*Pchi
    require(P.T == P and P*P == P, 'The domain projector is invalid.')
    gram = []
    for r in range(4):
        step = 2**r
        Q = sum((T**k for k in range(0, modulus, step)), zero) / (modulus//step)
        R = Q*S*P
        gram.append(R.T*R)
    require(gram[1] == 2*gram[0], 'The first exact norm ratio failed.')
    require(gram[2] == 4*gram[0], 'The second exact norm ratio failed.')
    require(gram[3] == 8*gram[0], 'The third exact norm ratio failed.')
    require(gram[0]*gram[0] == gram[0]/8,
            'The singular spectrum is not zero and one eighth.')
    require(s.trace(gram[0]) == s.Rational(1, 4),
            'The maximal singular space does not have dimension two.')
    F = s.Matrix([chi(q) if q % 2 else 0 for p, q in points])
    G = s.Matrix([chi(p) if q % 8 == 0 else 0 for p, q in points])
    require(P*F == F and P*G == G, 'The equality vectors are not in the domain.')
    require(gram[0]*F == F/8 and gram[0]*G == G/8,
            'The predicted equality vectors do not attain the bound.')
    return {'modulus': modulus, 'primitive_vectors': size,
            'domain_dimension': int(s.trace(P)),
            'largest_singular_space_dimension': 2,
            'squared_norm_bounds': ['1/8', '1/4', '1/2', '1'],
            'exact_squared_norm_ratios': [1, 2, 4, 8]}

if __name__ == '__main__':
    results = [check(modulus) for modulus in (8, 16)]
    receipt = {'status': 'PASS', 'scope': 'Finite checks supplement the independent all-level proof.',
               'checks': results}
    Path(__file__).with_name('chi_minus8_ladder_finite_check.json').write_text(
        json.dumps(receipt, indent=2)+'\n')
    print(json.dumps(receipt))
