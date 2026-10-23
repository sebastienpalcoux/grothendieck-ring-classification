#!/usr/bin/env python3
"""Exact arithmetic obstruction inventory for the 182 supplied rank-11 rings.

Discovery writes certificates; --verify-only checks all accepted certificates.
The input order is never canonicalized: identifiers refer to physical lines.
"""
from pathlib import Path
import argparse, collections, gzip, hashlib, importlib.util, json, sys, time
import sympy as s

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
LEGACY = HERE / 'legacy'
sys.path.insert(0, str(LEGACY))
sys.path.insert(0, str(HERE.parent))
import common
import arithmetic as old
import exact
import gng
import noncomm_integral
import extra_arithmetic
import field_automorphisms as fa

def require(x, why):
    if not x:
        raise ValueError(why)

def rows():
    records = []
    for identifier, R in common.read().items():
        records.append({'id': identifier, 'rank': 11,
                        'tensor_sha256': old.sha(R), 'tensor': R})
    require(len(records) == 182, 'expected exactly 182 physical input lines')
    return records

def primitive_certificate(R):
    # Schopieray Theorem 4.4 and Corollary 4.3 apply to general fusion
    # categories.  The separate spherical restrictions begin at Section 4.2.
    if not old.comm(R):
        return None
    p = old.casimir(R).charpoly(old.t).as_poly()
    for q, e in p.factor_list()[1]:
        d, norm = q.degree(), abs(int(q.TC()))
        if all(v < d for v in s.factorint(norm).values()) and (d != len(R) or e != 1 or p != q):
            return {'kind': 'primitive_codegree', 'factor': list(map(int, q.all_coeffs())),
                    'degree': d, 'norm': norm, 'scope': 'general_complex_fusion_category',
                    'reference': 'Schopieray, Norm, trace, and formal codegrees, Corollary 4.3 and Theorem 4.4 (general fusion categories), arXiv:2005.13760v1'}

def extra_field(R):
    if not old.comm(R):
        return None
    for i, A in enumerate(R):
        for f, m in s.Matrix(A).charpoly(fa.x).as_poly().factor_list()[1]:
            c = extra_arithmetic.automorphism_obstruction(tuple(fa.coeff(f)))
            if c:
                c = dict(c, object=i, scope='general_complex_fusion_category')
                fa.verify(R, c)
                return c

def certificate_checks(R, c):
    k = c['kind']
    require(c['scope']=='general_complex_fusion_category','arithmetic certificate scope')
    if k == 'casimir_dnumber':
        q=s.Poly.from_list(c['factor'],old.t);p=old.casimir(R).charpoly(old.t).as_poly()
        co=list(map(int,q.all_coeffs()));d=q.degree();j=c['index'];N=abs(co[-1])
        require(q.is_irreducible and p.rem(q).is_zero and 1<=j<=d,'Casimir irreducible factor')
        rem=pow(co[j],d,N**j)
        require(rem and rem==c['nonzero_remainder'],'d-number divisibility fails')
    elif k == 'cyclotomic':
        require(old.comm(R),'matrix-eigenvalue criterion needs commutativity')
        exact.check_cyclotomic([s.Matrix(A).charpoly(old.t).as_poly() for A in R], c)
    elif k == 'noncommuting_field_automorphisms': fa.verify(R, c)
    else:
        fn = {'integral_drinfeld': old.integral_drinfeld,
              'near_group_small_m': old.near_group,
              'noncomm_integral_drinfeld': noncomm_integral.test,
              'generalized_near_group_divisibility': gng.certificate,
              'nonabelian_tambara_yamagami': gng.certificate,
              'primitive_codegree': primitive_certificate}[k]
        got = fn(R)
        if got is not None:got.setdefault('scope','general_complex_fusion_category')
        require(got == c, 'certificate replay mismatch')
        if 'dims' in c:
            ds=c['dims'];n=len(R)
            require(len(ds)==n and ds[0]==1 and all(type(x)is int and x>0 for x in ds),'positive integer dimensions')
            require(all(sum(R[i][j][k]*ds[k] for k in range(n))==ds[i]*ds[j] for i in range(n) for j in range(n)),'dimension homomorphism')

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--verify-only', action='store_true')
    ap.add_argument('--skip-extra-fields', action='store_true')
    args = ap.parse_args()
    records = rows()
    out = HERE / 'arithmetic.json'
    if args.verify_only:
        ledger = json.loads(out.read_text())
        require(len(ledger['records']) == len(records), 'complete ledger')
        for r, d in zip(records, ledger['records']):
            require(r['id'] == d['id'] and r['tensor_sha256'] == d['tensor_sha256'], 'input identity')
            for c in d['certificates']: certificate_checks(r['tensor'], c)
        print('PASS exact arithmetic certificates', sum(bool(r['certificates']) for r in ledger['records']))
        return
    start = time.monotonic()
    result = {'scope': 'Certificate-specific scopes; no-conclusion is never a realization.', 'records': []}
    for r in records:
        R = r['tensor']; cs = []; applicable = []
        comm = old.comm(R)
        dims = old.integral_dimensions(R)
        for name, fn in [('near_group_small_m', old.near_group), ('casimir_dnumber', old.dnumber),
                         ('cyclotomic', old.cyclotomic), ('integral_drinfeld', old.integral_drinfeld),
                         ('generalized_near_group_divisibility', gng.certificate)]:
            c = fn(R)
            if c:
                c.setdefault('scope', 'general_complex_fusion_category')
                certificate_checks(R, c); cs.append(c)
            applicable.append(name)
        if not comm:
            c = noncomm_integral.test(R)
            if c:
                c.setdefault('scope', 'general_complex_fusion_category')
                certificate_checks(R, c); cs.append(c)
        pc = primitive_certificate(R)
        if pc: certificate_checks(R, pc); cs.append(pc)
        if comm and not args.skip_extra_fields:
            c = extra_field(R)
            if c: cs.append(c)
        result['records'].append({k:v for k,v in r.items() if k != 'tensor'} | {
            'commutative':comm, 'integral_dimensions':dims, 'certificates':cs,
            'extended_field_automorphisms_searched':comm and not args.skip_extra_fields})
        out.write_text(json.dumps(result, indent=2)+'\n')
        if cs or len(result['records']) % 20 == 0:
            print(r['id'], [c['kind'] for c in cs], round(time.monotonic()-start,2), flush=True)
    result['elapsed_seconds'] = time.monotonic()-start
    result['counts'] = dict(collections.Counter(c['kind'] for r in result['records'] for c in r['certificates']))
    result['general_complex_excluded'] = sum(any(c['scope']=='general_complex_fusion_category' for c in r['certificates']) for r in result['records'])
    out.write_text(json.dumps(result, indent=2)+'\n')
    print('DONE', result['general_complex_excluded'], result['counts'], flush=True)

if __name__ == '__main__': main()
