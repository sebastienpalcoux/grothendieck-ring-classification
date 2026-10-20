"""Explore based-ring completions of R443's unique Morita dual action frame.

This is a discovery script, not a categorification or exclusion verifier.
Requires sympy and z3-solver. All solver constraints are exact integer ones.
"""
import itertools
import json
from pathlib import Path
import sympy as s
import z3

HERE = Path(__file__).resolve().parent
data = json.loads((HERE / 'r443_dual_frames_exploration.json').read_text())
actions = [s.Matrix(5, 5, data['dual_action_domains'][t][i])
           for t, pair in enumerate(data['dual_frames'][0]) for i in pair]
L = [1, 0, 3, 2, 5, 4, 7, 6, 9, 8]
R = [1, 0, 3, 2, 5, 4, 8, 9, 6, 7]
triples = list(itertools.product(range(10), repeat=3))


def discover(dual, timeout_ms=120000):
    parent = {t:t for t in triples}
    def find(t):
        while parent[t] != t:
            parent[t] = parent[parent[t]]
            t = parent[t]
        return t
    def join(a, b):
        a, b = find(a), find(b)
        parent[max(a,b)] = min(a,b)
    for i,j,k in triples:
        join((i,j,k),(dual[i],k,j))
        join((i,j,k),(k,dual[j],i))
        join((i,j,k),(dual[j],dual[i],dual[k]))
        join((L[i],j,k),(i,j,L[k]))
        join((i,R[j],k),(i,j,R[k]))
        join((R[i],j,k),(i,L[j],k))
    roots = sorted(set(map(find, triples)))
    fixed = {}
    def fix(t, val):
        p = find(t)
        if p in fixed and fixed[p] != val:
            raise ValueError('inconsistent fusion symmetries')
        fixed[p] = val
    for i,j in itertools.product(range(10),repeat=2):
        fix((0,i,j),int(i==j));fix((i,0,j),int(i==j))
        fix((1,i,j),int(L[i]==j));fix((i,1,j),int(R[i]==j))
        fix((i,j,0),int(j==dual[i]))
    unknown = [t for t in roots if t not in fixed]
    variables = {t:z3.Int('n_'+'_'.join(map(str,t))) for t in unknown}
    def N(i,j,k):
        t=find((i,j,k))
        return fixed[t] if t in fixed else variables[t]
    solver = z3.Solver();solver.set(timeout=timeout_ms)
    bounds = {t:10**9 for t in unknown}
    for i,j in itertools.product(range(10),repeat=2):
        target=actions[i]*actions[j]
        for k in range(10):
            bound=min(int(target[a,b])//int(actions[k][a,b])
                      for a,b in itertools.product(range(5),repeat=2) if actions[k][a,b])
            t=find((i,j,k))
            if t in bounds:bounds[t]=min(bounds[t],bound)
        for a,b in itertools.product(range(5),repeat=2):
            solver.add(z3.Sum([N(i,j,k)*int(actions[k][a,b]) for k in range(10)])==int(target[a,b]))
    for t in unknown:
        solver.add(variables[t]>=0,variables[t]<=bounds[t])
    linear=solver.check()
    print('dual',dual,'classes',len(roots),'unknown',len(unknown),'bounds',bounds,'linear',linear,flush=True)
    if linear!=z3.sat:
        return {'dual':dual,'linear_result':str(linear),'unknown_classes':len(unknown)}
    # The unit and g identities already impose all associativities involving
    # an invertible. Keep every remaining coefficient equation.
    for i,j,k,l in itertools.product(range(2,10),range(2,10),range(2,10),range(10)):
        solver.add(z3.Sum([N(i,j,a)*N(a,k,l)-N(j,k,a)*N(i,a,l) for a in range(10)])==0)
    results=[]
    while True:
        answer=solver.check()
        print('associative',answer,'models',len(results),flush=True)
        if answer!=z3.sat:break
        model=solver.model()
        values={t:model.eval(variables[t]).as_long() for t in unknown}
        tensor=[[[int(N(i,j,k)) if isinstance(N(i,j,k),int) else values[find((i,j,k))]
                  for k in range(10)] for j in range(10)] for i in range(10)]
        results.append(tensor)
        solver.add(z3.Or([variables[t]!=values[t] for t in unknown]))
        if len(results)>=1000:
            answer='model limit';break
    return {'dual':dual,'unknown_classes':len(unknown),'models':results,'completion':str(answer)}


if __name__=='__main__':
    records=[]
    for swap in (False,True):
        dual=[0,1,2,3,5 if swap else 4,4 if swap else 5,6,8,7,9]
        records.append(discover(dual))
        (HERE/'r443_ring_completions_exploration.json').write_text(json.dumps(records,indent=2)+'\n')
