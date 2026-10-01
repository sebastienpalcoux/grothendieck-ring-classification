"""Independent exact bounded-deficit/triangle proof for two M9 rings.

No signed CSP, numerical optimizer, or discovery certificate is used to
enumerate the magnitude/sign domains. The retained spherical obstruction
is checked separately after proving a spherical section must exist.
"""
import argparse, hashlib, itertools, json, math, sys, time
from pathlib import Path
import sympy as s

HERE = Path(__file__).resolve().parent
def find_source():
    for path in HERE.parents:
        if (path/'software/replay_m9_structure.py').is_file():
            return path
    return None

TENSOR_HASHES = {'R6_9_7741': '02dde73bf8dd7f5247153f391734e56d0540a50cd7e7c04fc37334887010fbd5', 'R6_9_7742': '1954c96b8d9264aedd4cd183b7396fcd457a8c8c9b619db5d8f236559ee4c649'}

def need(condition, message):
    if not condition:
        raise ValueError(message)

def tensor(magnitudes, triples):
    R = [[[int(j == k) if i == 0 else int(i == k) if j == 0
           else int(i == j) if k == 0 else 0 for k in range(6)]
          for j in range(6)] for i in range(6)]
    for t, value in zip(triples, magnitudes):
        for i, j, k in set(itertools.permutations(t)):
            R[i][j][k] = value
    return R

def associative(R):
    for i, j, k, l in itertools.product(range(1, 6), repeat=4):
        if sum(R[i][j][a]*R[a][k][l] for a in range(6)) != sum(
                R[j][k][a]*R[i][a][l] for a in range(6)):
            return False
    return True

def run(row, package, check_spherical=True):
    R = row['N']; start = time.monotonic()
    need(hashlib.sha256(json.dumps(R,sort_keys=True,separators=(',',':')).encode()).hexdigest() == TENSOR_HASHES.get(row['id']), 'source tensor fingerprint')
    need(row['dual'] == list(range(6)), 'not self-dual')
    triples = list(itertools.combinations_with_replacement(range(1, 6), 3))
    bounds = [R[i][j][k] for i,j,k in triples]
    need(all(b > 0 for b in bounds), 'dense positivity hypothesis fails')
    need(tensor(bounds, triples) == R and associative(R), 'invalid tensor')
    matrices = [s.Matrix(x) for x in R]
    casimir = sum((a*a for a in matrices), s.zeros(6))
    trace = int(s.trace(casimir)); ideals = []
    for polynomial, multiplicity in casimir.charpoly().as_poly().factor_list()[1]:
        coefficients = list(map(int, polynomial.all_coeffs()))
        if polynomial.degree() == 1:
            ideals.append(-coefficients[1])
        elif polynomial.degree() == 2:
            A, B = -coefficients[1], coefficients[2]
            disc = A*A-4*B
            q = math.prod(int(p) for p, e in s.factorint(disc).items() if e % 2)
            b = math.isqrt(disc//q)
            need(b*b*q == disc and q % 4 == 1, 'quadratic integral basis')
            ideals.append(math.gcd(A, (A+b*q)//2))
        else:
            raise ValueError('unexpected formal codegree degree')
    lower = math.lcm(*ideals)
    budget = trace-lower
    need(budget >= 0, 'negative budget handled elsewhere')
    weights = [len(set(itertools.permutations(t))) for t in triples]
    profiles = []
    def visit(j, remaining, values):
        if j == len(triples):
            profiles.append(tuple(values)); return
        for v in range(bounds[j], -1, -2):
            cost = weights[j]*(bounds[j]**2-v**2)
            if cost <= remaining:
                visit(j+1, remaining-cost, values+[v])
    visit(0,budget,[])
    survivors = []; rejected = []
    for index, values in enumerate(profiles):
        A = tensor(values,triples)
        witness = None
        for i,j in itertools.combinations(range(1,6),2):
            lhs = sum(A[i][i][k]*A[j][j][k] for k in range(6))
            rhs = sum(A[i][j][k]**2 for k in range(6))
            if lhs < rhs:
                witness = [i,j,lhs,rhs]; break
        if witness is None:
            survivors.append(values)
        else:
            rejected.append([index,*witness])
    need(survivors == [tuple(bounds)], 'magnitude saturation unproved')
    # At saturation diagonal associativity attains its triangle upper bound.
    # Hence all t_iik with fixed k share a sign. A basis sign change makes
    # every repeated-index coefficient positive. Only 10 distinct triples
    # remain: enumerate all their signs, with no additional gauge assumption.
    distinct = [j for j,t in enumerate(triples) if len(set(t)) == 3]
    need(len(distinct) == 10, 'distinct-triple domain')
    solutions = []
    for signs in itertools.product((-1,1),repeat=len(distinct)):
        values = bounds.copy()
        for j, sign in zip(distinct,signs):
            values[j] *= sign
        if associative(tensor(values,triples)):
            solutions.append(list(signs))
    need(solutions == [[1]*10], 'nonpositive saturated signed table remains')
    spherical_sha = None
    if check_spherical:
        sys.path.insert(0,str(package/'software'))
        import scipy.optimize as opt
        def denied(*a,**k):
            raise RuntimeError('optimizer disabled during exact proof replay')
        opt.linprog = opt.milp = denied
        from replay_m9_structure import verify_record
        records = json.loads((HERE/'spherical_certificates.json').read_text())
        record = next(v for v in records if v['id'] == row['id'])
        need(verify_record(R,record), 'spherical obstruction failed')
        spherical_sha = hashlib.sha256(json.dumps(record['certificate'],sort_keys=True,separators=(',',':')).encode()).hexdigest()
    return dict(id=row['id'],general_excluded=check_spherical,
        tensor_sha256=hashlib.sha256(json.dumps(R,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
        casimir_trace=trace,trace_ideal_generators=ideals,trace_lower_bound=lower,
        deficit_budget=budget,magnitude_profiles=len(profiles),
        triangle_rejection_witnesses=rejected,saturated_sign_tables_checked=1024,
        normalized_solutions=solutions,spherical_certificate_sha256=spherical_sha,
        optimizer_disabled=check_spherical,optimized_python=not __debug__,
        seconds=time.monotonic()-start)

if __name__ == '__main__':
    p=argparse.ArgumentParser();p.add_argument('--source-root',type=Path,default=find_source())
    p.add_argument('--report',type=Path)
    args=p.parse_args()
    need(args.source_root is not None, 'supply --source-root for canonical mathematical primitives')
    rows=json.loads((HERE/'tensors.json').read_text())
    results=[run(row,args.source_root) for row in rows if row['id'] in ('R6_9_7741','R6_9_7742')]
    need(len(results)==2,'missing target tensor')
    if args.report:
        args.report.parent.mkdir(parents=True,exist_ok=True)
        args.report.write_text(json.dumps(dict(complete=True,results=results),indent=2)+'\n')
    for result in results:
        print({k:v for k,v in result.items() if k!='triangle_rejection_witnesses'})
