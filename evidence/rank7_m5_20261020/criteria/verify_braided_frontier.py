"""Exact braided-only exclusions for the two unresolved general tensors.

The signed/Galois reduction is replayed, not assumed. This file never writes
the general categorification ledger. It uses no numerical optimizer or asserts.
"""
import argparse
import contextlib
import importlib.util
import io
import json
from pathlib import Path

import sympy as s
import r3895_modular_probe as probe

q = probe.q
HERE = Path(__file__).resolve().parent


def closure(tensor, generator):
    n = len(tensor)
    dual = [next(j for j in range(n) if tensor[i][j][0]) for i in range(n)]
    support = {0, generator}
    while True:
        larger = support | {dual[i] for i in support} | {
            k for i in support for j in support for k in range(n) if tensor[i][j][k]
        }
        if larger == support:
            return sorted(support)
        support = larger


def verify_5039():
    from rings import Characters, validate
    rid = 'R7_5_5039'
    tensor = next(r['tensor'] for r in json.loads(
        (q.ROOT/'supplements/rank7/output/m5/census.json').read_text()) if r['id'] == rid)
    q.require(q.tensor_hash(tensor) == '8606c63a2f02ea028185db755a4b055382073b94736d5040ee92f3eec07f450c',
              'pinned R5039 source tensor')
    validate(tensor)
    dimensions, D, _, _, _, _ = q.source_data(tensor, rid)
    d = [s.Integer(a)+b*s.sqrt(5) for a,b in dimensions]
    total = s.Integer(D[0])+D[1]*s.sqrt(5)
    algebra = Characters(tensor)
    x = s.Symbol('x')
    cp = algebra.C.charpoly(x).as_poly()
    expected = s.Poly((x-8)**3*(x-5)**2*(x*x-1440*x+6400), x)
    q.require(cp == expected, 'exact R5039 formal-codegree polynomial')
    q.require(s.simplify(total/d[1]**2) == 16, 'required modular formal codegree is sixteen')
    q.require(cp.eval(16) != 0, 'sixteen is absent from the formal-codegree spectrum')
    closures = [closure(tensor, i) for i in range(1,7)]
    q.require(all(c == list(range(7)) for c in closures), 'every R5039 nonunit generates the whole ring')
    return {
        'id': rid, 'tensor_sha256': q.tensor_hash(tensor),
        'dimension_ratios': [str(s.simplify(total/z**2)) for z in d],
        'formal_codegree_polynomial': str(cp.as_expr()),
        'codegree_polynomial_at_16': int(cp.eval(16)),
        'nonunit_generated_subrings': closures,
        'obstruction': 'a modular simple of dimension 5+2sqrt(5) would have missing formal codegree 16',
    }


def verify():
    path = HERE.parent/'sqrt5_reduction/verify_reduction.py'
    spec = importlib.util.spec_from_file_location('braided_frontier_signed_reduction', path)
    reduction = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(reduction)
    structural = reduction.run()
    q.require(structural['status'] == 'PASS', 'general-to-Galois-pseudounitary reduction')
    with contextlib.redirect_stdout(io.StringIO()):
        modular = probe.run(write_receipt=False)
    simpler = verify_5039()
    q.require({r['id']:r['tensor_sha256'] for r in structural['results']} == {
        modular['id']:modular['source_sha256'], simpler['id']:simpler['tensor_sha256']},
        'structural reduction and braided obstructions use identical source tensors')
    modular.pop('seconds', None)
    return {
        'status':'PASS',
        'scope':'No braided fusion-category categorification over characteristic zero; general categorification remains unresolved.',
        'galois_pseudounitary_reduction':structural,
        'R7_5_3895':modular,
        'R7_5_5039':simpler,
    }


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    args=parser.parse_args()
    result=verify()
    text=json.dumps(result,indent=2)+'\n'
    if args.output:
        args.output.write_text(text)
    print(json.dumps({'status':result['status'],'scope':result['scope']}))
