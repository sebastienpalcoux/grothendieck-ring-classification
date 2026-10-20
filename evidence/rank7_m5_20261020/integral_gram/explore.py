"""Discovery only: exact integer domains for the two remaining q=5 rings."""
import argparse
import json
import math
import pathlib
import sys
import time

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'criteria'))
import q5_modular_low as m
q = m.q


def domains(rid):
    target = HERE / (rid + '_domains.json')
    if target.exists():
        return json.loads(target.read_text())
    N = next(r['tensor'] for r in json.loads((q.ROOT / 'supplements/rank7/output/m5/census.json').read_text()) if r['id'] == rid)
    d,D,B,zs,transport,signs = q.source_data(N,rid)
    table = m.ExactQuadraticCharacterTable(N,d,5)
    characters,codegrees,epairs = m.char_data(table)
    lows,nodes,forced = q.enumerate_low(B,d,zs,transport)
    rows = q.global_rows(B,d)
    result = []
    for ix, low in enumerate(lows):
        labels = table.assignments([(1,0,0,0,0,0,0)] + low)
        if not labels:
            continue
        R,bound,orbits,rank = q.compatible_orbits(rows,B,low,transport)
        columns = m.augmented_columns(orbits,D,characters,epairs,table.K)
        known = [tuple(sum(v[i+1]*z[k] for v,z in zip(low,zs)) for k in range(2)) for i in range(6)]
        cases = []
        for label in labels:
            for sign in signs:
                rhs = m.augmented_rhs(bound,known,D,sign,low,label,characters,codegrees,epairs,table.K)
                cols,target0 = m.integral_system(columns,rhs)
                cases.append({'label':label,'sign':sign,'rhs':target0})
        record = {'low_index':ix,'low':low,'bound':bound,'orbits':orbits,'columns':cols,'cases':cases}
        result.append(record)
        print(json.dumps({'event':'domain','ring':rid,'low':ix,'orbits':len(orbits),'cases':len(cases)}),flush=True)
    target.write_text(json.dumps(result) + '\n')
    return result


def lattice_contains(cols, rhs):
    from flint import fmpz_mat
    H = fmpz_mat(cols).hnf()
    v = rhs[:]
    for j in range(H.nrows()):
        row = [int(H[j,i]) for i in range(H.ncols())]
        pivot = next((i for i,x in enumerate(row) if x), None)
        if pivot is None:
            break
        if v[pivot] % row[pivot]:
            return False, {'pivot':pivot,'modulus':row[pivot],'residue':v[pivot] % row[pivot]}
        c = v[pivot] // row[pivot]
        v = [x-c*y for x,y in zip(v,row)]
    return not any(v), {'remainder':v}


def run(rid, mode):
    import numpy as np
    from scipy.optimize import milp, Bounds, LinearConstraint
    from scipy.sparse import csc_matrix
    ds = domains(rid)
    if mode in ('parity','compression','spectral'):
        N = next(r['tensor'] for r in json.loads((q.ROOT / 'supplements/rank7/output/m5/census.json').read_text()) if r['id'] == rid)
        d,D,B,zs,transport,signs = q.source_data(N,rid)
        table = m.ExactQuadraticCharacterTable(N,d,5)
    results = []
    for dom in ds:
        if mode in ('compression','spectral') and rid == 'R7_5_5039' and dom['low_index'] == 1:
            continue
        cols = dom['columns']
        multipliers = [1]*len(cols)
        if mode in ('parity','compression','spectral'):
            fixed = []
            for oi,orbit in enumerate(dom['orbits']):
                v = (0,)+tuple(orbit[0][0])
                tv = transport(v)
                if all(x<=0 for x in tv):
                    tv = tuple(-x for x in tv)
                dv = tuple(v[i] for i in transport.dual)
                if tv == v or tv == dv:
                    fixed.append(oi)
                    for phase in range(4,10):
                        multipliers[10*oi+phase] = 2
            cols = [[mul*x for x in col] for col,mul in zip(cols,multipliers)]
            print(json.dumps({'event':'parity','index':dom['low_index'],'fixed_orbits':len(fixed),'total':len(dom['orbits'])}),flush=True)
        if mode == 'gram':
            gramcols = [[sum(row[1][j] for row in orbit) for j in range(21)] for orbit in dom['orbits']]
            cases = [{'rhs':dom['bound']}]
            cols = gramcols
        else:
            cases = dom['cases']
        all_cols = cols
        forbidden_orbits = set()
        if mode == 'spectral':
            from spectral_induction import Spectrum
            sp = Spectrum(table,[(1,0,0,0,0,0,0)]+[tuple(v) for v in dom['low']],[(v,z) for orbit in dom['orbits'] for v,_,z in orbit])
            if sp.missing_low:
                result={'index':dom['low_index'],'spectral_low_excluded':sp.missing_low};results.append(result);print(json.dumps(result),flush=True);continue
            forbidden=set(map(tuple,sp.forbidden))
            forbidden_orbits={i for i,orbit in enumerate(dom['orbits']) if any(tuple(v) in forbidden for v,_,z in orbit)}
            print(json.dumps({'event':'spectral','index':dom['low_index'],'forbidden_orbits':len(forbidden_orbits)}),flush=True)
        for ci,case in enumerate(cases):
            selection = [k for k in range(len(all_cols)) if k//10 not in forbidden_orbits]
            if mode in ('compression','spectral'):
                delta = -1 if case['label'].index(5)<case['label'].index(6) else 1
                phase = 4 if delta == -1 else 7
                i,j = (3,4) if rid == 'R7_5_3895' else (2,3)
                selection = [k for k in selection if (all(row[0][i]==row[0][j] for row in dom['orbits'][k//10]) or k%10==phase)]
            cols = [all_cols[k] for k in selection]
            rhs = case['rhs']
            primes = [p for p in [2,3,5,7,11,13,17,19,23,29,31] if not q.base.span_contains(cols,rhs,p)]
            if primes:
                result = {'index':dom['low_index'],'case':ci,'modular_obstruction':primes}
                print(json.dumps(result),flush=True);results.append(result);continue
            lattice, why = lattice_contains(cols,rhs)
            if not lattice:
                result = {'index':dom['low_index'],'case':ci,'integer_lattice_obstruction':why}
                print(json.dumps(result),flush=True);results.append(result);continue
            ub = [min(rhs[i]//c[i] for i in range(min(21,len(rhs))) if c[i]>0) for c in cols]
            A = csc_matrix(np.array(cols,dtype=float).T)
            start = time.monotonic()
            solved = milp(np.ones(len(cols)),integrality=np.ones(len(cols)),bounds=Bounds(np.zeros(len(cols)),np.array(ub)),constraints=LinearConstraint(A,rhs,rhs),options={'time_limit':60})
            result = {'index':dom['low_index'],'case':ci,'status':int(solved.status),'message':solved.message,'seconds':time.monotonic()-start}
            if solved.x is not None:
                x = [round(float(v)) for v in solved.x]
                result['exact_feasible'] = all(sum(c[i]*v for c,v in zip(cols,x))==b for i,b in enumerate(rhs))
                result['support'] = [(selection[i],v) for i,v in enumerate(x) if v]
                result['actual_support'] = [(selection[i],v*multipliers[selection[i]]) for i,v in enumerate(x) if v]
            print(json.dumps(result),flush=True);results.append(result)
    (HERE / (rid+'_'+mode+'_discovery.json')).write_text(json.dumps(results,indent=2)+'\n')


if __name__ == '__main__':
    p=argparse.ArgumentParser();p.add_argument('ring',choices=q.CONFIG);p.add_argument('mode',choices=['gram','full','parity','compression','spectral']);a=p.parse_args();run(a.ring,a.mode)
