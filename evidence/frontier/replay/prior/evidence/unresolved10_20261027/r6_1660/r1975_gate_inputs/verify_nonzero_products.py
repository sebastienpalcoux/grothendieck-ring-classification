"""Fresh replay using independent eight-bit associativity encoding.

No discovery solver receipts are trusted. Rebuild all associativity equations,
add the proved nonzero-product clauses, replay every algebraic obstruction,
block precisely dual-compatible gauges and source based automorphisms, then
require UNSAT. Each integer associativity equation is bounded by 72, so an
eight-bit zero equation is equivalent to the integer equation.
"""
from nonzero_products import *
from signed_sieve import problem
from arithmetic import verify_dnumber
from verify_results import check_spherical_report

def check(R,report,timeout=60000):
    gate_mode=report['outcome']=='galois_pseudo_unitarity'
    assert report['outcome']in ('excluded','galois_pseudo_unitarity') and report['complete']
    assert digest(R)==report['tensor_sha256']
    S,vs,active,mapping,bounds,gauge,eqcount=problem(R)
    S.set(timeout=timeout)
    assert len(vs)==report['variables'] and eqcount==report['equations']
    assert gauge==report['gauge_coordinates']
    n=len(R);pairs=[]
    for i,j in itertools.product(range(1,n),repeat=2):
        if R[i][j][0] or any(c%2 for c in R[i][j]):continue
        coords=sorted({mapping[i,j,k]for k in range(1,n)if R[i][j][k]})
        S.add(z3.Or(*(vs[v]!=0 for v in coords)))
        pairs.append({'objects':[i,j],'coordinates':coords})
    assert pairs==report['nonzero_pair_constraints']
    du=[next(j for j in range(n)if R[i][j][0])for i in range(n)]
    sig=signature(R);groups=[[i for i in range(1,n)if sig[i]==q]for q in sorted(set(sig[1:]))]
    automorphisms=[]
    for parts in itertools.product(*(itertools.permutations(g)for g in groups)):
        p=list(range(n))
        for group,part in zip(groups,parts):
            for i,j in zip(group,part):p[i]=j
        if all(R[i][j][k]==R[p[i]][p[j]][p[k]]for i,j,k in itertools.product(range(n),repeat=3)):
            automorphisms.append(p)
    signs=[(1,)+q for q in itertools.product((-1,1),repeat=n-1)
           if all(((1,)+q)[i]==((1,)+q)[du[i]]for i in range(n))]
    source=chars(R);source_checked=False;covered=set();checked=0
    if gate_mode:
        fp_minpoly=source.fp()[4]
        assert pc(fp_minpoly)==report['fp_global_minimal_polynomial']
    for branch in report['branches']:
        values=branch['values']
        assert all(v in range(-b,b+1,2)for v,b in zip(values,bounds))
        assert all(values[i]>=0 for i in gauge)
        T=tensor(R,mapping,values)
        assert all(any(T[i][j]) for i,j in itertools.product(range(n),repeat=2))
        c=branch['obstruction'];kind=c['kind']
        if kind=='original_gauge':
            assert original_gauge(R,T)is not None
            if not source_checked:
                check_spherical_report(R,c['spherical_report']);source_checked=True
        elif kind=='casimir_dnumber':verify_dnumber(T,c)
        elif kind=='all_signed_scalar_characters_excluded':
            a=chars(T);assert len(a.components)==len(c['characters'])
            for (f,m),b in zip(a.components,c['characters']):
                assert pc(f)==b['factor']
                assert char_obstruction(a,f,list(source.cf)+list(a.cf))==b['obstruction']
        elif kind=='signed_scalar_characters_gated':
            assert gate_mode
            from galois_pu_gate import unique_required
            a=chars(T);assert len(a.components)==len(c['characters'])
            for (f,m),b in zip(a.components,c['characters']):
                assert pc(f)==b['factor']
                actual=char_obstruction(a,f,unique_required(source,a))
                assert actual==b['obstruction']
                if actual is None:
                    assert b['gate']['kind']=='global_dimension_Galois_FP'
                    assert a.component(f)[3]==fp_minpoly
                    assert b['gate']['polynomial']==pc(fp_minpoly)
        else:raise ValueError(kind)
        orbit=set()
        for p in automorphisms:
            for eps in signs:
                vv=tuple(eps[a]*eps[b]*eps[d]*T[p[a]][p[b]][p[du[d]]]
                         for o in active for a,b,d in [o[0]])
                if any(vv[i]<0 for i in gauge):continue
                orbit.add(vv)
        assert len(orbit)==branch['gauge_orbit_size']
        for vv in orbit-covered:S.add(z3.Or(*(v!=x for v,x in zip(vs,vv))))
        covered|=orbit;checked+=1
    final=str(S.check());assert final=='unsat',f'independent completeness returned {final}: {S.reason_unknown()}'
    return {'id':report['id'],'status':'PASS','branches_replayed':checked,
            'gauge_and_automorphism_tables_blocked':len(covered),
            'nonzero_product_clauses':len(pairs),'independent_completeness':'UNSAT',
            'scope':'general complex fusion categories',
            'conclusion':report['outcome'],
            'criterion':'signed global-dimension Galois-FP gate'if gate_mode else'nonzero products in the signed sphericalization quotient'}

if __name__=='__main__':
    from galois_pu_gate import GATE_TARGETS
    gate_mode='--gates'in sys.argv
    rows={r['id']:r['tensor']for r in read()};out=[]
    for i in (GATE_TARGETS if gate_mode else TARGETS):
        rid=f'R9_2_{i}';start=time.time()
        report=json.loads((HERE/(('gate_'if gate_mode else'')+rid+'.json')).read_text())
        if not report['complete']:continue
        result=check(rows[rid],report,timeout=300000 if i==920 else 120000);result['seconds']=round(time.time()-start,3)
        out.append(result);print(json.dumps(result),flush=True)
        (HERE/('gate_verification.json'if gate_mode else'verification.json')).write_text(json.dumps(out,indent=2)+'\n')
