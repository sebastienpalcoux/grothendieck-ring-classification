"""Exact, optimizer-free necessary Morita reduction for R7_5_443.

Regenerates the unique involution-module action, all joint four-index Gram
frames, and all based-ring completions of the resulting dual action. This
does NOT prove a categorification or nonexistence of the source ring.
Requires sympy; no z3, numerical optimizer, or floating point is used.
"""
import hashlib
import itertools
import json
import math
from pathlib import Path
import sys
import sympy as s

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO / 'supplements/rank7/software'))
from module_dual_gram import anti_representations, module_matrices
from rings import codegree_poly, dnumber
from subring_descent import certificate as subring_certificate
from subring_descent import verify as subring_verify

SOURCE_HASH = '2fac7e9b2ba6ee55e35443af3ac36221f20b56b60a6224e0137813bc2365fa8c'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(N):
    return hashlib.sha256(json.dumps(N, separators=(',', ':')).encode()).hexdigest()


def frames(M):
    """All positive integer dual-action Gram frames, including their unit."""
    r = M[0].rows
    h = r*r
    H = s.Matrix(h, h, lambda i, j:
                 sum(A[i//r,j//r]*A[i%r,j%r] for A in M))
    symbols = s.symbols('x:'+str(h))
    X = s.Matrix(r, r, symbols)
    equations = sum((list(X*A-A*X) for A in M), [])
    positions = list(itertools.combinations_with_replacement(range(h), 2))
    target = tuple(int(H[i,j]) for i,j in positions)
    domains = []
    pairs = []
    for typ in range(r):
        solutions = s.linsolve(equations+[X[0,j]-int(j==typ) for j in range(r)], symbols)
        require(len(solutions) == 1, 'commutant affine solution')
        solution = next(iter(solutions))
        free = sorted(set().union(*(e.free_symbols for e in solution)), key=str)
        # Each free variable is an actual nonnegative matrix entry, with its
        # diagonal Gram bound; thus this is the full finite integer domain.
        bounds = [math.isqrt(int(H[symbols.index(z),symbols.index(z)])) for z in free]
        domain = []
        for values in itertools.product(*(range(b+1) for b in bounds)):
            values = dict(zip(free, values))
            v = [e.subs(values) for e in solution]
            if all(x.q == 1 and 0 <= x <= math.isqrt(int(H[i,i])) for i,x in enumerate(v)):
                domain.append(tuple(map(int,v)))
        domains.append(domain)
        outer = [tuple(v[i]*v[j] for i,j in positions) for v in domain]
        choices = []
        identity = tuple(int(i==j) for i in range(r) for j in range(r))
        for a,b in itertools.combinations_with_replacement(range(len(domain)),2):
            if typ == 0 and identity not in (domain[a],domain[b]):
                continue
            q = tuple(x+y for x,y in zip(outer[a],outer[b]))
            if all(x<=y for x,y in zip(q,target)):
                choices.append(((a,b),q))
        pairs.append(choices)
    results = []
    for selection in itertools.product(*pairs):
        if tuple(sum(pair[1][k] for pair in selection) for k in range(len(target))) == target:
            results.append([pair[0] for pair in selection])
    require([len(d) for d in domains] == [2,4,5,6,6], 'dual action domains')
    require([len(p) for p in pairs] == [1,2,3,3,3], 'dual pair domains')
    require(len(results) == 1, 'unique full Morita Gram frame')
    actions = [s.Matrix(r,r,domains[t][i]) for t,pair in enumerate(results[0]) for i in pair]
    require(any(A*B != B*A for A in actions for B in actions), 'noncommutative dual action')
    return domains, results[0], actions


def completions(actions, swap):
    n=10
    dual=[0,1,2,3,5 if swap else 4,4 if swap else 5,6,8,7,9]
    left=[1,0,3,2,5,4,7,6,9,8]
    right=[1,0,3,2,5,4,8,9,6,7]
    require(all(actions[1]*actions[i] == actions[left[i]] and
                actions[i]*actions[1] == actions[right[i]] and
                actions[i].T == actions[dual[i]] for i in range(n)), 'dual/invertible actions')
    triples=list(itertools.product(range(n),repeat=3))
    parent={t:t for t in triples}
    def find(t):
        if parent[t]!=t:
            parent[t]=find(parent[t])
        return parent[t]
    def join(a,b):
        a,b=find(a),find(b)
        parent[max(a,b)]=min(a,b)
    for i,j,k in triples:
        join((i,j,k),(dual[i],k,j))
        join((i,j,k),(k,dual[j],i))
        join((i,j,k),(dual[j],dual[i],dual[k]))
        join((left[i],j,k),(i,j,left[k]))
        join((i,right[j],k),(i,j,right[k]))
        join((right[i],j,k),(i,left[j],k))
    fixed={}
    def fix(t,v):
        t=find(t)
        require(t not in fixed or fixed[t]==v, 'compatible fusion symmetries')
        fixed[t]=v
    for i,j in itertools.product(range(n),repeat=2):
        fix((0,i,j),int(i==j)); fix((i,0,j),int(i==j))
        fix((1,i,j),int(left[i]==j)); fix((i,1,j),int(right[i]==j))
        fix((i,j,0),int(j==dual[i]))
    unknown=sorted(set(map(find,triples))-fixed.keys())
    symbols=s.symbols('c:'+str(len(unknown)))
    variables=dict(zip(unknown,symbols))
    def N(i,j,k):
        t=find((i,j,k))
        return fixed[t] if t in fixed else variables[t]
    equations=[]
    bounds={t:10**9 for t in unknown}
    for i,j in itertools.product(range(n),repeat=2):
        target=actions[i]*actions[j]
        equations.extend(sum((N(i,j,k)*actions[k] for k in range(n)),s.zeros(5))-target)
        for k in range(n):
            bound=min(int(target[a,b])//int(actions[k][a,b])
                      for a,b in itertools.product(range(5),repeat=2) if actions[k][a,b])
            t=find((i,j,k))
            if t in bounds: bounds[t]=min(bounds[t],bound)
    solution_set=s.linsolve(equations,symbols)
    require(len(solution_set)==1, 'one affine completion system')
    solution=next(iter(solution_set))
    if swap:
        # The coefficient forced to 3/2 is a direct integer contradiction.
        require(s.Rational(3,2) in solution, 'paired-c duality contradiction')
        return {'paired_c_objects':True,'excluded':'forced fusion coefficient 3/2'},[]
    free=sorted(set().union(*(e.free_symbols for e in solution)),key=str)
    domains=[range(bounds[unknown[symbols.index(z)]]+1) for z in free]
    require(len(free)==4 and math.prod(map(len,domains))==72, 'complete four-parameter domain')
    found=[]
    integer_candidates=0
    for values in itertools.product(*domains):
        values=dict(zip(free,values))
        vector=[e.subs(values) for e in solution]
        if not all(x.q==1 and 0<=x<=bounds[t] for x,t in zip(vector,unknown)):
            continue
        integer_candidates+=1
        selected={t:int(v) for t,v in zip(unknown,vector)}
        def value(i,j,k):
            t=find((i,j,k))
            return fixed[t] if t in fixed else selected[t]
        tensor=[[[value(i,j,k) for k in range(n)] for j in range(n)] for i in range(n)]
        if any(sum(tensor[i][j][a]*tensor[a][k][l] for a in range(n)) !=
               sum(tensor[j][k][a]*tensor[i][a][l] for a in range(n))
               for i,j,k,l in itertools.product(range(n),repeat=4)):
            continue
        found.append(tensor)
    require(len(found)==10, 'exact associative completion count')
    return {'paired_c_objects':False,'free_coefficients':4,'finite_domain':72,
            'nonnegative_integer_candidates':integer_candidates,'associative_completions':10},found


def main():
    census=json.loads((REPO/'supplements/rank7/output/m5/census.json').read_text())
    R=next(row['tensor'] for row in census if row['id']=='R7_5_443')
    require(digest(R)==SOURCE_HASH,'pinned source tensor')
    fixed,seed,nodes,anti=anti_representations(R,1)
    require(fixed==[6] and len(anti)==1,'unique full anti-module action')
    labels,M=module_matrices(R,1,fixed,anti[0])
    require(M[1]==s.eye(5),'source involution acts trivially on module objects')
    domains,frame,actions=frames(M)
    search,tensors=completions(actions,False)
    other,_=completions(actions,True)
    records=[]
    for tensor in tensors:
        arithmetic=dnumber(tensor)
        lower=subring_certificate(tensor)
        if lower is not None:subring_verify(tensor,lower)
        records.append({'tensor_sha256':digest(tensor),'tensor':tensor,
                        'casimir_polynomial':str(codegree_poly(tensor).as_expr().factor()),
                        'dnumber_exclusion':arithmetic,'lower_rank_exclusion':lower})
    records.sort(key=lambda r:r['tensor_sha256'])
    require(sum(r['dnumber_exclusion'] is not None for r in records)==4,'four d-number exclusions')
    require(sum(r['lower_rank_exclusion'] is not None for r in records)==2,'two rank-five subring exclusions')
    remaining=[r for r in records if r['dnumber_exclusion'] is None and r['lower_rank_exclusion'] is None]
    require(len(remaining)==4,'four surviving labelled based-ring completions')
    report={'id':'R7_5_443','source_tensor_sha256':SOURCE_HASH,
            'scope':'necessary conditions for general complex categorification; no model or source exclusion claimed',
            'module_labels':labels,'anti_action':anti[0],
            'left_action':[[list(map(int,A.row(i))) for i in range(5)] for A in M],
            'dual_action_domains':domains,'unique_dual_frame':frame,
            'dual_action':[[list(map(int,A.row(i))) for i in range(5)] for A in actions],
            'completion_search':[search,other],'based_rings':records,
            'remaining_labelled_completions':len(remaining)}
    (HERE/'r443_morita_reduction.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'status':'PASS','anti_actions':1,'dual_frames':1,
                      'based_ring_completions':10,'general_exclusions_among_completions':6,
                      'remaining_labelled_completions':4}))


if __name__=='__main__':
    main()
