"""Exact model-scope check, not a nonexistence test.

Compare the frozen residuals with all registered rank-six models, their Morita
classes, and dimensions of relative centers over all fusion subcategories.
Run from any directory; output stays beside this research script.
"""
import hashlib
import itertools
import json
import sys
import time
from pathlib import Path

import sympy as s

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'software'))
from exact import embeddings, evaluate, field, require
from existence import REGISTRIES
from rings import dual, fingerprint
from subring_descent import closed_subrings

t, x = s.symbols('t x')


def polynomial(K, value):
    f = s.Poly.from_list(list(map(s.Rational, K.mod.to_list())), t)
    a = s.Poly.from_list(list(map(s.Rational, value.to_list())), t)
    resultant = s.Poly(s.resultant(f.as_expr(), x-a.as_expr(), t), x)
    hits = [g.monic() for g, _ in resultant.factor_list()[1]
            if not evaluate(g.all_coeffs(), value, K)]
    require(len(hits) == 1, 'minimal polynomial is ambiguous')
    return list(map(str, hits[0].all_coeffs()))


def fp(R):
    n = len(R)
    matrices = list(map(s.Matrix, R))
    H = sum(matrices, s.zeros(n))
    require(all(a > 0 for a in H), 'regular sum is not strictly positive')
    p = H.charpoly(t).as_poly()
    f, emb = max(((f, e) for f, _ in p.factor_list()[1]
                  for e in embeddings(f)), key=lambda fe: fe[1].hi)
    K = field(f)
    adj = (t*s.eye(n)-H).adjugate()
    denominator = evaluate(s.Poly(adj[0, 0], t).all_coeffs(), K.unit, K)
    require(bool(denominator), 'Perron projector has zero unit entry')
    ds = [evaluate(s.Poly(adj[i, 0], t).all_coeffs(), K.unit, K)/denominator
          for i in range(n)]
    require(ds[0] == K.one and all(emb.sign(d) > 0 for d in ds),
            'invalid Perron character')
    require(all(ds[i]*ds[j] == sum((K(R[i][j][k])*ds[k]
                                    for k in range(n)), K.zero)
                for i in range(n) for j in range(n)),
            'Perron vector is not a dimension character')
    require(all(ds[i] == ds[dual(R)[i]] for i in range(n)), 'dual dimension')
    return K, ds, sum((d*d for d in ds), K.zero)


def main():
    start = time.monotonic()
    manifest = ROOT/'verification/round4/campaign_manifest.json'
    source = json.loads(manifest.read_text())
    target_polys = {}
    inputs = []
    for record in source['tensors']:
        R = record['N']
        K, ds, D = fp(R)
        pD = polynomial(K, D)
        target_polys.setdefault(tuple(pD), []).append(record['id'])
        inputs.append(dict(id=record['id'], tensor_sha256=fingerprint(R),
                           dimension_polynomial=pD,
                           proper_fusion_subsets=[list(J) for J, _ in closed_subrings(R)]))
    constructions = []
    hashes = {}
    for name in REGISTRIES:
        path = ROOT/'data'/f'{name}.json'
        hashes[str(path.relative_to(ROOT))] = hashlib.sha256(path.read_bytes()).hexdigest()
        for model in json.loads(path.read_text()):
            R = model['N']
            require(len(R) == 6, 'registry contains a non-rank-six model')
            K, ds, D = fp(R)
            subsets = [(0,)] + [J for J, _ in closed_subrings(R)] + [tuple(range(6))]
            relatives = []
            for J in subsets:
                p = polynomial(K, D*sum((ds[j]*ds[j] for j in J), K.zero))
                relatives.append(dict(subset=list(J), dimension_polynomial=p,
                                      residual_matches=target_polys.get(tuple(p), [])))
            constructions.append(dict(registry=name, id=model['id'], name=model['name'],
                                      tensor_sha256=fingerprint(R), relative_centers=relatives))
    hits = [dict(model=r['id'], name=r['name'], **c) for r in constructions
            for c in r['relative_centers'] if c['residual_matches']]
    out = dict(scope='dimension-only necessary comparison; does not classify residuals',
               manifest_sha256=hashlib.sha256(manifest.read_bytes()).hexdigest(),
               registry_sha256=hashes, frozen_inputs=inputs,
               constructors=len(constructions), distinct_model_ids=len({r['id'] for r in constructions}),
               relative_center_dimension_checks=sum(len(r['relative_centers']) for r in constructions),
               matches=hits, models=constructions, seconds=time.monotonic()-start)
    Path(__file__).with_suffix('.json').write_text(json.dumps(out, indent=2)+'\n')
    print({k:out[k] for k in ('constructors','distinct_model_ids','relative_center_dimension_checks','matches','seconds')})


if __name__ == '__main__':
    main()
