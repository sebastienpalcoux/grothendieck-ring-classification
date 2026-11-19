#!/usr/bin/env python3
"""Match all model tensors to the ordinary census and verify the dimension table."""
import argparse
import json
from pathlib import Path
import sys

import sympy as sp

HERE = Path(__file__).resolve().parent
CENSUS = HERE.parent / 'census'
sys.path.insert(0, str(CENSUS))
from rank4 import canonical, casimir, characteristic_polynomial, require, validate


def read_json(filename):
    return json.loads((HERE / filename).read_text())


def radical_tex(spec):
    a, b, c, n = (spec[k] for k in ('constant','coefficient','radicand','denominator'))
    value = str(a)
    if b:
        value += '+' + (str(b) if b != 1 else '') + r'\sqrt{' + str(c) + '}'
    return '(' + value + ')/' + str(n) if n != 1 else value


def run(manuscript=None, output=None):
    models = read_json('tensors.json')
    rows = read_json('table.json')
    characters = {r['model']: r for r in read_json('characters.json')}
    require(len(rows) == len(models) == len(characters) == 15, 'expected fifteen models')
    census = {}
    with (CENSUS / 'data/rings.jsonl').open() as data:
        for line in data:
            row = json.loads(line)
            key = canonical(row['tensor'])
            require(key not in census, 'based-isomorphic census records')
            census[key] = row['id']
    x, t = sp.symbols('x t')
    recorded = []
    tex_rows = []
    used = set()
    for model, row in zip(models, rows):
        name = model['model']
        require(name == row['model'], 'model order')
        tensor = model['matrices']
        validate(tensor)
        key = canonical(tensor)
        require(key in census and key not in used, 'missing or repeated model in ordinary census: '+name)
        used.add(key)
        source = characters[name]
        ds = [sp.sympify(z, locals={'t':t}) for z in source['fp_dimensions_in_model_basis']]
        require(len(ds) == 4 and ds[0] == 1 and all(z.is_positive is True for z in ds),
                'positive normalized character: '+name)
        generators = [d for d in ds if not d.is_rational]
        K = sp.QQ.algebraic_field(*generators) if generators else sp.QQ
        v = [K.from_sympy(d) for d in ds]
        for i in range(4):
            for j in range(4):
                require(v[i]*v[j] == sum((tensor[i][j][k]*v[k] for k in range(4)), K.zero),
                        'fusion character: '+name)
        dimension = sum((d*d for d in v), K.zero)
        require(dimension == K.from_sympy(sp.sympify(source['global_fp_dimension'],locals={'t':t})),
                'global dimension: '+name)
        spec = row['dimension']
        if 'polynomial' in spec:
            poly = sp.Poly.from_list(spec['polynomial'], x, domain=sp.QQ)
            cp = sp.Poly.from_list(characteristic_polynomial(casimir(tensor)),x,domain=sp.QQ)
            require(poly.is_irreducible and cp.rem(poly).is_zero, 'irreducible Casimir factor: '+name)
            result = K.zero
            for coefficient in poly.all_coeffs():
                result = result*dimension+K.from_sympy(coefficient)
            require(result == K.zero, 'dimension satisfies table polynomial: '+name)
            tex_dimension = spec['symbol']
            # Its positive normalized character places the Casimir eigenvalue at the spectral radius.
        else:
            a,b,c,n = (spec[k] for k in ('constant','coefficient','radicand','denominator'))
            require(n > 0 and dimension == K.from_sympy((sp.Integer(a)+b*sp.sqrt(c))/n),
                    'dimension equals radical: '+name)
            tex_dimension = radical_tex(spec)
        mult = max(k for matrix in tensor for line in matrix for k in line)
        require(mult == row['multiplicity'], 'multiplicity: '+name)
        tex_rows.append(f"${mult}$ & {row['name_tex']} & ${tex_dimension}$ & {row['reference_tex']}" + r' \\')
        recorded.append({'model':name,'census_id':census[key],'multiplicity':mult})
    if manuscript is not None:
        source = manuscript.read_text()
        for line in tex_rows:
            require(source.count(line) == 1, 'printed table differs from checked row: '+line)
    if output:
        output.write_text(json.dumps(recorded, indent=2)+'\n')
    print('PASS: 15 distinct census models, positive dimension characters, dimensions and multiplicities.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manuscript',type=Path)
    parser.add_argument('--output',type=Path)
    args = parser.parse_args()
    run(args.manuscript, args.output)
