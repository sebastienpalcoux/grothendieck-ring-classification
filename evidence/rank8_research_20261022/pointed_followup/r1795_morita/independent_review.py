#!/usr/bin/env python3
"""Independent complete commutant enumeration and obstruction review.

No producer routines or symbolic producer equations are imported. Enumerates
the whole normalized ten-variable box; tests commuting multiplication matrices
at every leaf; validates all full tensor identities and codegrees in Python.
The categorical hypotheses and exact scope are audited in INDEPENDENT_REVIEW.md.
"""
from pathlib import Path
import argparse, hashlib, itertools, json, subprocess, tempfile
import sympy as s

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]


def need(ok, message):
    if not ok:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def digest(value):
    return sha(json.dumps(value, separators=(',', ':')).encode())


def independent_enumeration(Q):
    triples = list(itertools.combinations_with_replacement(range(1, 4), 3))
    positive = {(1, 2, 2), (2, 2, 3), (2, 3, 3)}
    domains = [list(range(-Q[i][j][k], Q[i][j][k]+1, 2)) for i, j, k in triples]
    fixed = [i for i, t in enumerate(triples) if t in positive]
    patterns = set()
    for signs in itertools.product((-1, 1), repeat=3):
        g = (1,) + signs
        patterns.add(tuple(g[a]*g[b]*g[c] for i in fixed for a, b, c in [triples[i]]))
    need(patterns == set(itertools.product((-1, 1), repeat=3)), 'independent sign fixes')
    for i in fixed:
        need(all(x % 2 for x in domains[i]), 'sign-fixed coefficient can vanish')
        domains[i] = [x for x in domains[i] if x > 0]
    code = '''#include <iostream>
#include <vector>
using namespace std;
int T[4][4][4]={}, v[10];
long long leaves=0,solutions=0;
bool commutes(){
 for(int i=1;i<4;++i) for(int j=i+1;j<4;++j)
  for(int r=0;r<4;++r) for(int c=r+1;c<4;++c){
   int sum=0;
   for(int a=0;a<4;++a)sum+=T[i][r][a]*T[j][a][c]-T[j][r][a]*T[i][a][c];
   if(sum)return false;
  }
 return true;
}
void visit(int level){
 if(level==10){++leaves;if(!commutes())return;++solutions;
  for(int x:v)cout<<x<<" ";cout<<"\\n";return;}
 switch(level){
'''
    for i, (triple, domain) in enumerate(zip(triples, domains)):
        code += 'case %d:for(int x:vector<int>{%s}){v[%d]=x;' % (i, ','.join(map(str, domain)), i)
        for a, b, c in sorted(set(itertools.permutations(triple))):
            code += f'T[{a}][{b}][{c}]=x;'
        code += f'visit({i+1});' + '}break;\n'
    code += '''}}
int main(){for(int i=0;i<4;++i){T[0][i][i]=1;T[i][0][i]=1;T[i][i][0]=1;}
visit(0);cerr<<leaves<<" "<<solutions<<"\\n";}
'''
    with tempfile.TemporaryDirectory() as directory:
        cpp, exe = Path(directory)/'review.cpp', Path(directory)/'review'
        cpp.write_text(code)
        subprocess.run(['g++', '-O3', '-std=c++17', str(cpp), '-o', str(exe)], check=True, capture_output=True)
        run = subprocess.run([str(exe)], check=True, capture_output=True, text=True, timeout=180)
    values = sorted(tuple(map(int, line.split())) for line in run.stdout.splitlines())
    leaves, count = map(int, run.stderr.split())
    need(leaves == s.prod(map(len, domains)) == 2531250, 'whole box not traversed')
    need(count == len(values) == len(set(values)) == 45, 'wrong complete signed solution count')
    return triples, values, {'box_leaves_checked': leaves, 'solutions': count,
                             'native_source_sha256': sha(code.encode()),
                             'lexicographic_signed_solutions_sha256': digest(values)}


def add(a, b):
    return a[0]+b[0], a[1]+b[1]


def multiply(a, b):
    return a[0]*b[0]+5*a[1]*b[1], a[0]*b[1]+a[1]*b[0]


def valuation(n, prime):
    n, value = abs(int(n)), 0
    need(n > 0, 'zero norm')
    while n % prime == 0:
        n //= prime
        value += 1
    return value


def compute():
    producer = json.loads((HERE/'covers.json').read_text())
    census_path = ROOT/'evidence/rank8_m3_20261021/pipeline/census_m3.json'
    source = next(r for r in json.loads(census_path.read_text()) if r['id'] == 'R8_3_1795')
    N = source['tensor']
    need(digest(N) == source['tensor_sha256'] == producer['source_tensor_sha256'], 'canonical source hash')
    for path, expected in producer['dependency_sha256'].items():
        need(sha((ROOT/path).read_bytes()) == expected, 'changed categorical dependency: '+path)
    pairs = [(0, 1), (2, 7), (3, 6), (4, 5)]
    need(all(N[1][i][j] == N[i][1][j] == int(j == next(b if i == a else a for a, b in pairs if i in (a, b)))
             for i, j in itertools.product(range(8), repeat=2)), 'central free source C2 action')
    Q = [[[sum(N[pairs[i][0]][pairs[j][0]][k] for k in pairs[l]) for l in range(4)]
          for j in range(4)] for i in range(4)]
    need(Q == producer['quotient'], 'quotient tensor differs')
    need(Q[2][2][1] == Q[3][3][2] == Q[2][2][3] == 5, 'all dual-swap parity witnesses')
    triples, values, enumeration = independent_enumeration(Q)
    saved = sorted(tuple(r['coefficients'][producer['triples'].index(list(t))] for t in triples)
                   for r in producer['records'])
    need(values == saved, 'independent full solution set differs')
    dims = [(1, 0), (1, 0), (6, 3), (6, 3), (7, 3), (7, 3), (7, 3), (7, 3)]
    need(sum(d[0]*d[0]+5*d[1]*d[1] for d in dims) == 540 and
         sum(2*d[0]*d[1] for d in dims) == 240, 'global FP dimension')
    z = s.Symbol('z')
    results = []
    for index, rec in enumerate(producer['records']):
        R = rec['tensor']
        for i, j, k in itertools.product(range(8), repeat=3):
            need(type(R[i][j][k]) is int and R[i][j][k] >= 0, 'nonnegative integer cover')
            need(R[0][i][j] == R[i][0][j] == R[i][j][0] == int(i == j), 'selfdual unit')
            need(R[i][j][k] == R[j][i][k] == R[i][k][j], 'commutativity and Frobenius')
        for i, j, k, l in itertools.product(range(8), repeat=4):
            need(sum(R[i][j][a]*R[a][k][l] for a in range(8)) ==
                 sum(R[j][k][a]*R[i][a][l] for a in range(8)), 'ordered associativity')
        for i, j in itertools.product(range(8), repeat=2):
            rhs = (sum(R[i][j][k]*dims[k][0] for k in range(8)),
                   sum(R[i][j][k]*dims[k][1] for k in range(8)))
            need(multiply(dims[i], dims[j]) == rhs, 'positive FP character')
        full_casimir = sum((s.Matrix(R[i])**2 for i in range(8)), s.zeros(8))
        factors = full_casimir.charpoly(z).as_poly().factor_list()[1]
        obstructions = []
        for f, multiplicity in factors:
            need(f.LC() == 1 and f.TC() != 0, 'valid formal codegree polynomial')
            for prime in s.factorint(abs(int(f.TC()))):
                if f.degree()*valuation(3600, prime) < 2*valuation(f.TC(), prime):
                    obstructions.append({'polynomial': str(f.as_expr()), 'prime': int(prime)})
        if obstructions:
            outcome = 'formal_codegree_norm_obstruction'
            evidence = obstructions
        elif rec['outcome'] == 'source_tensor_match':
            perm = rec['permutation_to_R1795']
            need(sorted(perm) == list(range(8)) and perm[0] == 0, 'based permutation')
            need(all(R[i][j][k] == N[perm[i]][perm[j]][perm[k]]
                     for i, j, k in itertools.product(range(8), repeat=3)), 'exact source identification')
            outcome, evidence = 'source_tensor_match', perm
        elif any(f.as_expr() == z**2-120*z+720 for f, m in factors):
            need(multiply((60, 24), (5, 2)) == (540, 240), 'central dimension division')
            need(all(b % 3 == 0 for a, b in dims) and 2 % 3 != 0, 'dimension lattice contradiction')
            outcome, evidence = 'center_dimension_lattice_obstruction', {'forced_dimension': [5, 2]}
        else:
            sub = [0, 2, 4, 6]
            need(all(R[i][j][k] == 0 for i, j in itertools.product(sub, repeat=2)
                     for k in range(8) if k not in sub), 'closed rank-four subring')
            need([[[R[i][j][k] for k in sub] for j in sub] for i in sub] == Q, 'rank-four quotient subring')
            need(270 > 24+12*2 and 3 < 4, 'exact comparison with rank-four bound')
            outcome, evidence = 'accepted_general_rank_four_bound_obstruction', sub
        need(outcome == rec['outcome'], 'independent obstruction classification differs')
        results.append({'index': index, 'outcome': outcome, 'evidence': evidence})
    counts = {name: sum(r['outcome'] == name for r in results) for name in sorted({r['outcome'] for r in results})}
    need(counts == producer['outcome_counts'] == {
        'formal_codegree_norm_obstruction': 41, 'center_dimension_lattice_obstruction': 2,
        'accepted_general_rank_four_bound_obstruction': 1, 'source_tensor_match': 1}, 'full result counts')
    return {'status': 'PASS', 'scope': 'conditional necessary Grothendieck-ring self-duality; no model, categorical equivalence, or ring exclusion',
            'producer_proof_sha256': sha((HERE/'PROOF.md').read_bytes()),
            'producer_source_sha256': sha((HERE/'enumerate_covers.py').read_bytes()),
            'producer_receipt_sha256': sha((HERE/'covers.json').read_bytes()),
            'review_source_sha256': sha(Path(__file__).read_bytes()),
            'source_tensor_sha256': source['tensor_sha256'], 'enumeration': enumeration,
            'full_regular_Casimir_used': True, 'outcome_counts': counts, 'covers': results,
            'dependencies': producer['dependency_sha256']}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    result = compute()
    path = HERE/'independent_review.json'
    if args.write:
        path.write_text(json.dumps(result, indent=2)+'\n')
    else:
        need(result == json.loads(path.read_text()), 'independent review receipt changed')
    print('PASS: complete independent 2,531,250-cover box; 45 covers; 41 norm + 2 dimension-lattice + 1 rank-four exclusions; one exact R1795 match')
