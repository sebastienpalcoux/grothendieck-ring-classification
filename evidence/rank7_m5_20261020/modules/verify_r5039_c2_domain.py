"""Independent coverage and modular replay of the R5039 c=2 branch.

No optimizer is imported. This checks a conditional branch exclusion, not
the c=0 branch or a whole-ring classification.
"""
import hashlib
import json
from pathlib import Path
import sys
import time

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
sys.path.insert(0, str(BASE / 'criteria'))
import q5_cyclic_eight_search as search

q, m = search.q, search.m


def require(condition, message):
    if not condition:
        raise ValueError(message)


def canonical(value):
    return json.loads(json.dumps(value))


def run(write_receipt=True):
    started = time.monotonic()
    rid = 'R7_5_5039'
    N = next(r['tensor'] for r in json.loads(
        (q.ROOT / 'supplements/rank7/output/m5/census.json').read_text())
        if r['id'] == rid)
    d, D, B, zs, T, signs = q.source_data(N, rid)
    require(signs == [[1, 0, 0, 1, 1, 1, 1]], 'complete second-indicator choices')
    table = m.ExactQuadraticCharacterTable(N, d, 5)
    lows, nodes, forced = q.enumerate_low(B, d, zs, T)
    rows = q.global_rows(B, d)
    recorded = search.e.domains(rid)
    characters, codegrees, pairs = m.char_data(table)
    actual = []
    frame_records = []
    for ix, low in enumerate(lows):
        assignments = table.assignments([(1, 0, 0, 0, 0, 0, 0)] + low)
        if not assignments:
            continue
        actual.append(ix)
        dom = next((z for z in recorded if z['low_index'] == ix), None)
        require(dom is not None, 'all eligible low frames recorded')
        _, bound, orbits, _ = q.compatible_orbits(rows, B, low, T)
        cols = m.augmented_columns(orbits, D, characters, pairs, table.K)
        known = [tuple(sum(v[i+1]*z[h] for v,z in zip(low,zs))
                       for h in range(2)) for i in range(6)]
        cases = []
        for label in assignments:
            for sign in signs:
                rhs = m.augmented_rhs(bound, known, D, sign, low, label,
                                      characters, codegrees, pairs, table.K)
                integer, target = m.integral_system(cols, rhs)
                cases.append({'label':label, 'sign':sign, 'rhs':target})
        fresh = dict(low_index=ix, low=low, bound=bound, orbits=orbits,
                     columns=integer, cases=cases)
        require(canonical(fresh) == dom, 'complete raw-source domain regeneration')
        weight = sum((v[1]-v[2])**2 for v in low)
        frame_records.append(dict(low_index=ix, low_weight=weight,
                                  assignments=len(assignments), orbits=len(orbits)))
    require(actual == [1, 3] and len(recorded) == 2, 'complete low-frame inventory')
    require([r['low_weight'] for r in frame_records] == [8, 0],
            'frame one violates the exact twist-one upper bound two')

    dom = next(z for z in recorded if z['low_index'] == 3)
    low = [(1,0,0,0,0,0,0)] + list(map(tuple,dom['low']))
    classes = {}
    for ci, case in enumerate(dom['cases']):
        key = tuple(sorted(zip(case['label'], low)))
        classes.setdefault(key, []).append(ci)
    require(len(classes) == 2, 'two complete character-to-row assignments')
    representatives = [v[0] for v in classes.values()]
    require(representatives == [0,1], 'both conductor-five signs represented')

    prepared = search.prepare(rid)
    proofs = []
    for case in representatives:
        stem = f'{rid}_c8_case{case}_chi8_2_system'
        path = BASE / 'criteria' / (stem + '.json')
        raw = path.read_bytes()
        system = json.loads(raw)
        rebuilt = canonical(search.build(rid,case,2,prepared))
        require(set(rebuilt)==set(system), 'same complete system schema')
        require(all(rebuilt[k]==v for k,v in system.items()),
                'entire frozen system and input hashes regenerated')
        cert_path = BASE / 'computation' / (stem+'_modular_certificate.json')
        cert = json.loads(cert_path.read_text())
        require(cert['system_sha256']==hashlib.sha256(raw).hexdigest(),
                'certificate bound to exact system bytes')
        c = cert['certificate']; modulus=c['modulus']
        require(type(modulus) is int and modulus>1, 'positive nontrivial modulus')
        functional = c['functional']
        require(len({a for a,b in functional})==len(functional), 'unique indices')
        require(all(type(a) is int and 0<=a<len(system['rhs']) and type(b) is int
                    for a,b in functional), 'integral bounded functional')
        value = lambda col: sum(b*col[a] for a,b in functional)%modulus
        require(all(value(col)==0 for col in system['columns']),
                'every original column annihilated modulo the modulus')
        residual = value(system['rhs'])
        require(residual == c['target_residue'] and residual != 0,
                'right hand side strictly outside the column lattice')
        proofs.append(dict(case=case, system_sha256=hashlib.sha256(raw).hexdigest(),
                           modulus=modulus, target_residue=residual,
                           support=len(functional), columns=len(system['columns'])))
    out = dict(status='PASS', id=rid, scope='Conditional exclusion of c=2 only; c=0 is not covered.',
               source_sha256=q.tensor_hash(N), optimized_python=not __debug__,
               low_frames=len(lows), global_rows=len(rows), frames=frame_records,
               case_classes=list(classes.values()), proofs=proofs,
               seconds=time.monotonic()-started)
    if write_receipt:
        (HERE/'r5039_c2_independent_domain_audit.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out),flush=True)
    return out


if __name__=='__main__':
    run()
