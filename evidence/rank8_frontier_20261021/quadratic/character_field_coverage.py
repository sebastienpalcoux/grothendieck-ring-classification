"""Exact source-bound character splitting coverage for seven residual rings.

This is a field-scope receipt, not a categorifiability criterion.
"""
from pathlib import Path
import argparse
import hashlib
import itertools
import json
import sympy as s

HERE=Path(__file__).resolve().parent
FIELDS={65:5,1055:37,1768:37,1795:5,3258:5,3413:5,3472:2}


def need(v,m):
    if not v:raise ValueError(m)


def run():
    rows={int(r['id'].rsplit('_',1)[1]):r for r in json.loads((HERE.parents[1]/'rank8_m3_20261021/pipeline/census_m3.json').read_text())}
    x=s.Symbol('x');out=[]
    for index,q in FIELDS.items():
        row=rows[index];R=row['tensor'];N=list(map(s.Matrix,R))
        sha=hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()
        need(sha==row['tensor_sha256'],'source tensor digest mismatch')
        need(all(R[i][j]==R[j][i] for i,j in itertools.product(range(8),repeat=2)),'commutativity required')
        coefficients=[(j+1)**2 for j in range(8)]
        H=sum((c*A for c,A in zip(coefficients,N)),s.zeros(8));p=H.charpoly(x).as_poly()
        need(s.gcd(p,p.diff()).degree()==0,'H is not separating')
        powers=[H**j for j in range(8)]
        V=s.Matrix.hstack(*(P[0,:].T for P in powers));need(V.det()!=0,'H does not generate source algebra')
        coords=[list(V.inv()*A[0,:].T) for A in N]
        need(all(sum((c*P for c,P in zip(v,powers)),s.zeros(8))==A for v,A in zip(coords,N)),
             'character polynomial interpolation failed')
        scalar,factors=s.factor_list(p.as_expr(),extension=s.sqrt(q))
        need(s.expand(scalar*s.prod(f**m for f,m in factors)-p.as_expr())==0,'field factorization product failed')
        records=[]
        for f,m in factors:
            poly=s.Poly(f,x,extension=s.sqrt(q));degree=poly.degree()
            need(m==1,'unexpected repeated factor')
            records.append({'degree':degree,'polynomial':str(poly.as_expr()),
                            'monic_coefficients':list(map(str,poly.all_coeffs()))})
        eligible=sum(f['degree']==1 for f in records)
        out.append({'id':row['id'],'tensor_sha256':sha,'FP_quadratic_radicand':q,
                    'separating_basis_coefficients':coefficients,
                    'separating_charpoly_coefficients':list(map(int,p.all_coeffs())),
                    'rational_factorization':str(s.factor(p.as_expr())),
                    'factorization_over_FP_quadratic_field':records,
                    'basis_polynomial_coordinates_in_H':[[str(c)for c in v]for v in coords],
                    'characters_with_all_values_in_FP_field':eligible,
                    'all_eight_characters_split_in_FP_field':eligible==8,
                    'scope':'Exact factorization and interpolation establish full character-field coverage; no categorification assertion'})
    return {'kind':'source_bound_character_field_coverage','records':out}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--write',action='store_true');a=p.parse_args()
    actual=run();path=HERE/'character_field_coverage_results.json'
    if a.write:path.write_text(json.dumps(actual,indent=2)+'\n')
    else:need(json.loads(path.read_text())==actual,'field coverage receipt changed')
    print('PASS: exact complete character-field coverage for seven residual rings')
