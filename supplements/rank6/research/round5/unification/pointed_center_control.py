"""Exact categorical controls: Z(Vec_Cn), n=2,3; no optimizer or assertions.

The low subcategory is Rep(Cn), so its words have zero high coefficients.
Consequently its low/low balancing equations alone do not detect a missing
star. The full-center ribbon check below separately tests that convention
on complex entries and records how many equations fail if the star is omitted.
"""
import hashlib
import itertools
import json
import sys
from collections import Counter
from pathlib import Path

import sympy as s

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'software'))
from character_induction import CharacterTable
from exact import field, require
from modular_character_induction import rational_rows
from round5_balancing import build_coupled
from round5_unified import low_word_data, joint_coefficient_domains, count_system


def run(n):
    C = field(s.Poly(s.cyclotomic_poly(n, s.Symbol('t')), s.Symbol('t')))
    zeta = C.unit
    R = [[[int(k == (i+j) % n) for k in range(n)]
          for j in range(n)] for i in range(n)]
    tab = CharacterTable.__new__(CharacterTable)
    tab.n, tab.du, tab.K = n, [(-i) % n for i in range(n)], C
    tab.rows = [tuple(zeta**((h*g) % n) for g in range(n)) for h in range(n)]
    tab.codegrees, tab.ds, tab.D, tab.fp = [C(n)]*n, [C.one]*n, C(n), 0
    tab.dims, tab.values, tab.allowed, tab.compatibility = {}, {}, {}, {}
    tab._automorphisms = [zeta**a for a in range(n) if s.gcd(a,n) == 1]
    low = [[1]+[0]*(n-1) for _ in range(n)]
    lab = [(-k) % n for k in range(n)]
    high = [[int(g == h) for h in range(1,n)] for g in range(1,n)]
    phase = [(zeta**t,) for t in range(n)]
    data = dict(C=C,F=n,tab=tab,dims=[C.one]*n,DD=C(n),phases=phase)
    require(tuple(lab) in tab.assignments(low), 'known low character labelling absent')
    words = [w for degree in (2,3) for w in
             itertools.combinations_with_replacement(range(n), degree)]
    wd = low_word_data(R,data,low,high,[n]*(n-1),lab,words=words)
    require(wd['low_duality'] == [(-k) % n for k in range(n)], 'complex low duality')
    require(wd['low_coefficients'] == [[int(k == sum(w) % n) for k in range(n)]
                                      for w in words], 'known word products')
    require(not any(x for row in wd['gram']+wd['restriction'] for x in row),
            'low words must remain in Rep(Cn)')
    domains = joint_coefficient_domains(wd, time_limit=15)
    require(domains['complete'] and not domains['impossible'], 'known category lost')
    for domain in domains['domains']:
        require(domain['domain']['candidates'] == [[0]*len(words)], 'zero high coefficients')
    gram = count_system(wd, domains)
    actual_gram = [n]*len(gram['labels'])
    require(all(sum(actual_gram[int(j)]*v for j,v in row.items()) == b
                for row,b in zip(gram['rows'],gram['rhs'])), 'joint count equations')

    # Actual central simples (g,k) have restriction e_g and twist zeta^(g*k).
    objects = list(itertools.product(range(n), repeat=2))
    labels = [(tuple(v),t) for v in high for t in range(n)]
    actual = Counter((tuple(high[g-1]), (g*k) % n) for g,k in objects if g)
    A,b = [],[]
    for v in high:
        A.append([int(v == list(w)) for w,t in labels]); b.append(n)
    # Low/low STS equations, unnormalized S and center square-root dimension n.
    # The known low contribution is n, and n*S_ab=n for these electric simples.
    paired_rows = 0
    for a,bb in itertools.combinations_with_replacement(range(n),2):
        coef = [zeta**((-a*sum((j+1)*x for j,x in enumerate(v))
                       -bb*sum((j+1)*x for j,x in enumerate(v))+t) % n)
                for v,t in labels]
        for row,value in rational_rows(coef,C.zero,C):
            A.append(row); b.append(value); paired_rows += 1
    require(all(sum(actual[label]*v for label,v in zip(labels,row)) == rhs
                for row,rhs in zip(A,b)), 'known restriction/twist equations')
    system = build_coupled(R,data,low,lab,A,b,labels,list(range(len(labels))),
                           [1]*len(labels),wd,domains)
    point = []
    for q,t in system['labels']:
        v,x = system['coefficient_labels'][q]
        require(x == [0]*len(words), 'actual high coefficients omitted')
        point.append(actual[(tuple(v[1:]),t)])
    require(all(type(x) is int and x >= 0 for x in point), 'nonnegative integral point')
    require(all(sum(point[int(j)]*v for j,v in row.items()) == rhs
                for row,rhs in zip(system['rows'],system['rhs'])), 'coupled equations')

    # Ribbon convention: theta_i theta_j S_ij = theta_(i* j).
    # Thus for a product ab the right index convention is S_(a*,b).
    theta = lambda a: zeta**((a[0]*a[1]) % n)
    star = lambda a: ((-a[0]) % n,(-a[1]) % n)
    add = lambda a,b: ((a[0]+b[0]) % n,(a[1]+b[1]) % n)
    S = lambda a,b: zeta**((-a[0]*b[1]-b[0]*a[1]) % n)
    wrong_star_failures = 0
    for a,bb in itertools.product(objects,repeat=2):
        require(theta(a)*theta(bb)*S(star(a),bb) == theta(add(a,bb)),
                'full-center ribbon/star convention')
        wrong_star_failures += theta(a)*theta(bb)*S(a,bb) != theta(add(a,bb))
    if n == 3:
        require(wrong_star_failures > 0, 'complex convention control is vacuous')
    return dict(category=f'Vec_C{n}',center_simples=len(objects),low_simples=n,
                low_duality=wd['low_duality'],quadratic_words=sum(len(w)==2 for w in words),
                cubic_words=sum(len(w)==3 for w in words),joint_domain_complete=True,
                gram_count_equations=len(gram['rows']),paired_twist_rows=paired_rows,
                coupled_rows=len(system['rows']),refined_variables=len(point),
                known_integer_point=point,full_center_ribbon_equations=len(objects)**2,
                wrong_star_failures=wrong_star_failures,
                limitation='Low words stay electric; high coefficients vanish. Full-center ribbon identities independently test the complex star convention.')


def main():
    result = dict(passed=True,optimizer_used=False,optimized_python=not __debug__,
                  cases=[run(2),run(3)],source_sha256={})
    for name in ['software/round5_unified.py','software/round5_balancing.py',
                 'research/round5/unification/pointed_center_control.py']:
        result['source_sha256'][name] = hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
    destination = Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_suffix('.json')
    destination.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
