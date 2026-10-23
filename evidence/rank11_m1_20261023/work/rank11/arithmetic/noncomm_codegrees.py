#!/usr/bin/env python3
"""Exact irreducible formal codegrees for all 29 noncommutative inputs.

The central Casimir is expressed as a rational polynomial in a separating
central element. A factor of multiplicity e^2 gives degree-e irreducibles;
divide the corresponding Casimir value by e (Ostrik Lemma 2.6).
"""
import argparse, collections, json, time
import sympy as s
from run import HERE, rows, old, exact, require
from cyclotomic_complete import centre_separator
from subring_indices import polynomial_of

def data(R):
    n=len(R); centre,fac=centre_separator(R);c=centre['centre_dimension']
    v=list(map(s.Rational,centre['central_coefficients'])); N=list(map(s.Matrix,R))
    H=sum((v[i]*N[i] for i in range(n)),s.zeros(n)); C=old.casimir(R)
    powers=[H**j for j in range(c)]
    V=s.Matrix.hstack(*(M[0,:].T for M in powers))
    cc,free=V.gauss_jordan_solve(C[0,:].T)
    require(free.rows==0,'unique central Casimir coordinates')
    require(sum((cc[j]*powers[j] for j in range(c)),s.zeros(n))==C,'Casimir polynomial equality')
    out=[]
    for q,m in fac:
        e,perfect=s.integer_nthroot(m,2);require(perfect,'square regular block multiplicity')
        f=exact.poly([str(x) for x in q.all_coeffs()]);K=exact.field(f)
        u=K(s.Poly(exact.t,exact.t).rem(f).all_coeffs())
        lam=sum((K(cc[j])*u**j for j in range(c)),K.zero);a=lam/K(e)
        cp=polynomial_of(a,f,K,u);p=cp.sqf_part()
        require(p.is_irreducible,'formal codegree minimal polynomial')
        co=p.all_coeffs();require(all(x.q==1 for x in co),'formal codegree is algebraic integer')
        norm=abs(int(p.TC()));d=p.degree();bad=[]
        for j in range(1,d+1):
            if int(co[j])**d % norm**j:bad.append(j)
        primitive=all(v<d for v in s.factorint(norm).values())
        out.append({'central_factor':[str(x) for x in q.all_coeffs()],
                    'regular_multiplicity':m,'irrep_dimension':int(e),
                    'galois_orbit_size':q.degree(),'formal_codegree_in_field':exact.ec(a),
                    'formal_codegree_minimal_polynomial':exact.pc(p),
                    'dnumber_failure_indices':bad,'primitive_integer_divisor_obstruction':primitive})
    require(sum(x['galois_orbit_size']*x['irrep_dimension']**2 for x in out)==n,'complete algebra decomposition')
    return {'centre_certificate':centre,'casimir_polynomial_coordinates':[str(x) for x in cc],
            'irreducible_components':out}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--verify-only',action='store_true');args=ap.parse_args()
    allrows=[r for r in rows() if not old.comm(r['tensor'])];out=HERE/'noncomm_codegrees.json'
    if args.verify_only:
        recs=json.loads(out.read_text())['records'];require(len(recs)==29,'complete noncommutative inventory')
        for r,z in zip(allrows,recs):
            require(r['id']==z['id'] and r['tensor_sha256']==z['tensor_sha256'],'input identity')
            require(data(r['tensor'])==z['data'],'exact codegree recomputation')
        print('PASS complete noncommutative formal codegrees');return
    start=time.monotonic();result={'records':[]}
    for r in allrows:
        d=data(r['tensor']);result['records'].append({k:v for k,v in r.items() if k!='tensor'}|{'data':d})
        out.write_text(json.dumps(result,indent=2)+'\n')
        print(r['id'],len(d['irreducible_components']),round(time.monotonic()-start,2),flush=True)
    result['elapsed_seconds']=time.monotonic()-start
    result['excluded_ids']=[r['id'] for r in result['records'] if any(x['dnumber_failure_indices'] or x['primitive_integer_divisor_obstruction'] for x in r['data']['irreducible_components'])]
    out.write_text(json.dumps(result,indent=2)+'\n');print('DONE',result['excluded_ids'],flush=True)
if __name__=='__main__':main()
