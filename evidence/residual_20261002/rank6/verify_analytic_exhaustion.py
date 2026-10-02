"""Exact primary-3 and all-support limit checks for the two rank-six residuals.

Run from any directory with Python and SymPy. No numerical computation is used.
"""
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path
import sys
import sympy as s

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
SOFTWARE = REPO / 'supplements/rank8/software'
sys.path.insert(0, str(SOFTWARE))
from exact import Embedding, ec, require
from rings import Characters, validate

EXPECTED_HELPERS = {
    'exact.py': '7a7525840192647312de0c2206d1e83a5b1fd2f592a3fa4830c730aea3a225c7',
    'rings.py': 'a992210513c5a3ecad6d700dec3020789ee74972e158296f589fb9668799cf33',
}


def fingerprint(N):
    return hashlib.sha256(json.dumps(N, separators=(',', ':')).encode()).hexdigest()


def compute():
    helpers = {name: hashlib.sha256((SOFTWARE/name).read_bytes()).hexdigest()
               for name in EXPECTED_HELPERS}
    require(helpers == EXPECTED_HELPERS, 'arithmetic helper source changed')
    t = s.Symbol('t')
    Kr = s.QQ.algebraic_field(s.sqrt(2), s.sqrt(3))
    K = s.QQ.algebraic_field(s.sqrt(2), s.sqrt(3), s.I)
    p = s.Poly.from_list(Kr.mod.to_list(), t)
    require(p.as_expr() == t**4-10*t**2+1, 'unexpected real primitive element')
    # The root in (3,4) is sqrt(2)+sqrt(3).
    emb = Embedding(p, (3,4))
    tensors = json.loads((REPO/'supplements/rank6/data/unresolved_tensors.json').read_text())
    require({x['id'] for x in tensors} == {'R6_4_155','R6_8_1660'})
    out = []
    for record in sorted(tensors, key=lambda x:x['id']):
        N = record['N']; r = len(N); validate(N)
        if record['id'] == 'R6_4_155':
            d = 4+3*s.sqrt(2); expr = [1,d,d,1,1,1]
        else:
            d = 3+2*s.sqrt(2)+2*s.sqrt(3)+s.sqrt(6)
            expr = [1,1,d,d,s.sqrt(2),s.sqrt(2)*d]
        ds = [Kr.from_sympy(s.sympify(v)) for v in expr]
        require(all(emb.sign(v)>0 for v in ds), 'dimension not positive')
        require(all(ds[i]*ds[j] == sum((Kr(N[i][j][k])*ds[k] for k in range(r)),Kr.zero)
                    for i,j in itertools.product(range(r),repeat=2)), 'dimension not a character')
        C = Characters(N)
        factors = C.p.set_domain(K).factor_list()[1]
        require(all(q.degree()==1 and m==1 for q,m in factors), 'spectrum does not split')
        roots = [-K.from_sympy(q.all_coeffs()[1])/K.from_sympy(q.all_coeffs()[0]) for q,m in factors]
        rows = [[sum((K(v)*a**j for j,v in enumerate(co)),K.zero) for co in C.coeff]
                for a in roots]
        require(len(rows)==r and len({tuple(row) for row in rows})==r)
        require(all(row[i]*row[j] == sum((K(N[i][j][k])*row[k] for k in range(r)),K.zero)
                    for row in rows for i,j in itertools.product(range(r),repeat=2)), 'invalid character')
        complex_dims = [K.from_sympy(s.sympify(v)) for v in expr]
        require(complex_dims in rows, 'FP character missing')
        spectrum = Counter()
        for a,b,c in itertools.product(range(r),repeat=3):
            value = sum((rows[a][i]*rows[b][i]*rows[c][i]/complex_dims[i]
                         for i in range(r)),K.zero)
            real_value = Kr.from_sympy(K.to_sympy(value))
            require(emb.sign(real_value)>=0, 'negative primary-3 eigenvalue')
            spectrum[tuple(ec(real_value))] += 1
        primary = {'character_count':r, 'triples_checked':r**3,
                   'distinct_eigenvalues':len(spectrum),
                   'eigenvalues':[{'coefficients':list(co),'multiplicity':spectrum[co]}
                                  for co in sorted(spectrum)]}
        forms = set(); checks = 0
        for i,j,k,l in itertools.product(range(r),repeat=4):
            if not N[i][j][l]: continue
            for mask in range(1,2**r-1):
                S = [a for a in range(r) if mask>>a&1]
                T = [m for m in range(r) if N[j][k][m] and any(N[i][m][a] for a in S)]
                co = tuple(sum(N[j][k][m]*N[l][m][v] for m in T)
                           -sum(N[l][k][a]*N[j][a][v] for a in S) for v in range(r))
                forms.add(co); checks += 1
        values = set(); zero_forms = 0
        for co in sorted(forms):
            value = sum((Kr(a)*v for a,v in zip(co,ds)),Kr.zero)
            sign = emb.sign(value)
            require(sign>=0, 'negative support-limit gap')
            zero_forms += sign==0
            values.add(tuple(ec(value)))
        support = {'conditions_checked':checks, 'distinct_integer_forms':len(forms),
                   'distinct_values':len(values), 'zero_forms':zero_forms,
                   'forms':[list(co) for co in sorted(forms)],
                   'exact_values':[list(co) for co in sorted(values)]}
        out.append({'id':record['id'], 'tensor_sha256':fingerprint(N),
                    'positive_dimensions':[ec(v) for v in ds],
                    'primary_3':primary, 'support_limit':support})
    return {'scope':'Exhaustion of necessary tests only; no categorification or exclusion claimed',
            'real_field_primitive':'sqrt(2)+sqrt(3)',
            'minimal_polynomial':['1','0','-10','0','1'], 'isolating_interval':['3','4'],
            'helper_sha256':helpers, 'records':out}


def verify():
    result = compute()
    expected = json.loads((HERE/'analytic_exhaustion.json').read_text())
    require(result == expected, 'exact replay differs from stored certificate')
    return {'status':'PASS', 'records':[
        {'id':r['id'], 'primary_triples':r['primary_3']['triples_checked'],
         'support_conditions':r['support_limit']['conditions_checked']}
        for r in result['records']]}


if __name__ == '__main__':
    if sys.argv[1:] == ['--write']:
        (HERE/'analytic_exhaustion.json').write_text(json.dumps(compute(),indent=2)+'\n')
    else:
        require(not sys.argv[1:], 'usage: verify_analytic_exhaustion.py [--write]')
        print(json.dumps(verify(),indent=2))
