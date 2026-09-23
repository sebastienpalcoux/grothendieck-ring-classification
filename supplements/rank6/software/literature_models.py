"""Published models and a central-boson quotient, independent of census labels.

Existence is a cited categorical input; these routines reconstruct fusion rules.
The source basis and all 216 structure constants are checked on identification.
No dimension-only or catalogue-index recognition is used.
"""
from pathlib import Path
import itertools
import json
from exact import require
from oriented_signed import validate_general
from positive_models import product, ng2, su2
from rings import permute

ROOT = Path(__file__).resolve().parents[1]
STRUCTURES = ('general', 'pivotal', 'spherical', 'pseudo_unitary', 'unitary')
UNITARY = {k: 'yes' for k in STRUCTURES}
NONPSEUDO = dict(UNITARY, pseudo_unitary='no', unitary='no')


def schopieray():
    """Example 1, equations (1)--(2), arXiv:2010.02958v1, printed page 3."""
    matrices = [
        '100000 010000 001000 000100 000010 000001',
        '010000 101100 010010 010110 001111 000011',
        '001000 010010 100101 001110 010111 001010',
        '000100 010110 001110 111111 011121 000111',
        '000010 001111 010111 011121 111221 011110',
        '000001 000011 001010 000111 011110 110100',
    ]
    return [[list(map(int, row)) for row in matrix.split()] for matrix in matrices]


def h8_extension():
    """Choi--Lu--Sun, equation (1.4); basis (1,a,b,ab,N,D)."""
    R = [[[0] * 6 for _ in range(6)] for _ in range(6)]
    for i, j in itertools.product(range(4), repeat=2):
        R[i][j][i ^ j] = 1
    for g in range(4):
        for x in (4, 5):
            R[g][x][x] = R[x][g][x] = 1
        R[4][4][g] = R[5][5][g] = 1
    R[4][5][5] = R[5][4][5] = R[5][5][4] = 2
    return R


def izumi_c4_dual():
    """Izumi--Morrison--Penneys, arXiv:1308.5723v1, page 27.

    Basis (1,kappa,beta*kappa,chi,sigma,beta); abbreviate by (1,k,l,c,s,b).
    """
    entries = [
        ['1', 'k', 'l', 'c', 's', 'b'],
        ['k', '1 k c s l', 'k c s b l', 'k 2c s l', 'k c l', 'l'],
        ['l', 'k c s b l', '1 k c s l', 'k 2c s l', 'k c l', 'k'],
        ['c', 'k 2c s l', 'k 2c s l', '1 2k c s b 2l', 'k c s l', 'c'],
        ['s', 'k c l', 'k c l', 'k c s l', '1 c s b', 's'],
        ['b', 'l', 'k', 'c', 's', '1'],
    ]
    ix = {x: i for i, x in enumerate(('1', 'k', 'l', 'c', 's', 'b'))}
    R = [[[0] * 6 for _ in range(6)] for _ in range(6)]
    for i, j in itertools.product(range(6), repeat=2):
        for term in entries[i][j].split():
            R[i][j][ix[term[-1]]] += int(term[:-1]) if len(term) > 1 else 1
    return R


def free_involution_quotient(R, g):
    """Compute orbit rules, conditional on a specified categorical central boson.

    This function checks the based-ring hypotheses. It DOES NOT infer the
    existence of a central boson from commutativity or from a permutation.
    The categorical hypothesis is supplied in Proposition central-boson in TeX.
    """
    validate_general(R)
    n = len(R)
    require(type(g) is int and 0 < g < n, 'invalid involution label')
    require(R[g][g] == [1] + [0] * (n - 1), 'object not order two')
    require(all(R[g][i] == R[i][g] and sum(R[g][i]) == 1 for i in range(n)),
            'object not a central based-ring invertible')
    action = [R[g][i].index(1) for i in range(n)]
    require(all(action[i] != i and action[action[i]] == i for i in range(n)),
            'the action is not free and involutive')
    reps = [i for i in range(n) if i < action[i]]
    Q = [[[R[i][j][k] + R[i][j][action[k]] for k in reps] for j in reps] for i in reps]
    # Independence of representative choices is checked explicitly.
    for i, j, k in itertools.product(reps, repeat=3):
        value = R[i][j][k] + R[i][j][action[k]]
        for ii, jj in itertools.product((i, action[i]), (j, action[j])):
            require(R[ii][jj][k] + R[ii][jj][action[k]] == value,
                    'orbit coefficients depend on representatives')
    validate_general(Q)
    return Q, {'boson_index': g, 'action': action, 'representatives': reps,
               'parent_rank': n, 'quotient_rank': len(reps)}


def diagonal_fermion():
    """Ising x PSU(2)_6, condensed by (psi,V6); see manuscript proof."""
    parent = product(ng2(0), su2(6, True))
    return free_involution_quotient(parent, 7)


def examples():
    """Yield (name, tensor, primary source, five existence statuses)."""
    yield ('Schopieray non-pseudounitary modular category', schopieray(),
           'Schopieray, Non-pseudounitary fusion, arXiv:2010.02958v1, '
           'Example 1 and Theorem 1; basis X0,...,X5', dict(NONPSEUDO))
    yield ('Rank-one C2-extension of Rep(H8)', h8_extension(),
           'Choi--Lu--Sun, arXiv:2310.19867v2, equation (1.4), '
           'Section 7.1 and Tables 3--4; unitary Ising-squared realization', dict(UNITARY))
    yield ('Izumi C4 dual even part', izumi_c4_dual(),
           'Izumi--Morrison--Penneys, arXiv:1308.5723v1, printed page 27, '
           'dual even-half fusion table of the 3^(Z/4) subfactor', dict(UNITARY))
    yield ('Diagonal-fermion quotient of Ising x PSU(2)_6', diagonal_fermion()[0],
           'Central-boson quotient proposition in the manuscript; '
           'EGNO, Tensor Categories, Section 8.23', dict(UNITARY))


def generate():
    from prepare import key
    census = json.loads((ROOT / 'data/census.json').read_text())
    index = {key(r['N']): r for r in census}
    records = []
    for name, N, source, existence in examples():
        validate_general(N)
        r = index.get(key(N))
        require(r is not None, 'published tensor is absent from census: ' + name)
        matches = [(0,) + p for p in itertools.permutations(range(1, 6))
                   if permute(N, (0,) + p) == r['N']]
        require(matches, 'no full tensor match')
        records.append({'name': name, 'id': r['id'], 'N': N, 'reference': source,
                        'existence': existence, 'basis_permutation': list(min(matches))})
        print(name, r['id'], min(matches), existence, flush=True)
    (ROOT / 'data/literature_positive_models.json').write_text(json.dumps(records, indent=2) + '\n')
    (ROOT / 'data/diagonal_fermion_quotient.json').write_text(
        json.dumps(diagonal_fermion()[1], indent=2) + '\n')
    return records


if __name__ == '__main__':
    generate()
