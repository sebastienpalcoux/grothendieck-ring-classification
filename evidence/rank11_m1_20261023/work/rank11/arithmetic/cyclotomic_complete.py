#!/usr/bin/env python3
"""Complete exact cyclotomic-field decisions on all commutative spectra.

Every affirmative irreducible factor is certified by its full list of roots
in Q[a] and commuting substitution automorphisms. Negative factors have a
modular nonuniform Frobenius-cycle witness or a nonabelian-field witness.
For noncommutative rings a separating central element tests the complete
irreducible character-trace field. FP and Casimir factors are also recorded.
"""
import argparse, itertools, json, time
import sympy as s
from run import HERE, rows, old, exact, fa, require
from subring_indices import fp_character

def field_factor(co):
    f=fa.parse(co); K=s.QQ.alg_field_from_poly(f)
    fac=s.Poly(f,fa.x,domain=K).factor_list()[1]
    return f,K,fac

def decide(co):
    f=fa.parse(co); d=f.degree()
    if d<=2:return {'abelian':True,'reason':'degree_at_most_two'}
    c=exact.cyclotomic_failure([exact.poly(co)],limit=1000)
    if c:return {'abelian':False,'reason':'nonuniform_Frobenius_cycles','certificate':c}
    f,K,fac=field_factor(co)
    if any(q.degree()>1 for q,m in fac):
        return {'abelian':False,'reason':'root_field_not_normal',
                'relative_factor_degrees':[[q.degree(),m] for q,m in fac]}
    roots=[]
    for q,m in fac:
        require(m==1 and q.degree()==1,'separable complete linear factors')
        a=-q.rep.to_list()[-1]/q.rep.to_list()[0]
        roots.append(s.Poly.from_list([s.Rational(v.numerator,v.denominator) for v in a.to_list()],fa.x,domain=s.QQ))
    roots.sort(key=lambda q:tuple(q.all_coeffs()))
    for a,b in itertools.combinations(roots,2):
        v=fa.compose(a,b,f)-fa.compose(b,a,f)
        if v:return {'abelian':False,'reason':'noncommuting_automorphisms',
                     'automorphisms':[fa.coeff(a),fa.coeff(b)],'difference':fa.coeff(v)}
    return {'abelian':True,'reason':'complete_commuting_root_substitutions',
            'root_polynomials':[fa.coeff(a) for a in roots]}

def verify_decision(co,c):
    f=fa.parse(co); require(f.is_irreducible,'Q irreducibility')
    if c['reason']=='degree_at_most_two':
        require(c['abelian'] and f.degree()<=2,'elementary abelian case');return
    if c['reason']=='nonuniform_Frobenius_cycles':
        require(not c['abelian'],'negative declaration'); exact.check_cyclotomic([exact.poly(co)],c['certificate']);return
    if c['reason']=='root_field_not_normal':
        _,_,fac=field_factor(co)
        ds=[[q.degree(),m] for q,m in fac]
        require(not c['abelian'] and ds==c['relative_factor_degrees'] and any(d>1 for d,m in ds),'nonnormal field factorization');return
    if c['reason']=='noncommuting_automorphisms':
        a,b=map(fa.parse,c['automorphisms'])
        require(not fa.compose(f,a,f) and not fa.compose(f,b,f),'field embeddings')
        v=fa.compose(a,b,f)-fa.compose(b,a,f)
        require(not c['abelian'] and v and fa.coeff(v)==c['difference'],'noncommuting embeddings');return
    require(c['reason']=='complete_commuting_root_substitutions' and c['abelian'],'complete abelian case')
    roots=list(map(fa.parse,c['root_polynomials']))
    require(len(roots)==f.degree() and len({tuple(q.all_coeffs()) for q in roots})==f.degree(),'full distinct roots')
    require(all(not fa.compose(f,a,f) for a in roots),'all substitutions roots')
    require(all(fa.compose(a,b,f)==fa.compose(b,a,f) for a,b in itertools.combinations(roots,2)),'abelian automorphisms')

def centre_separator(R):
    n=len(R); N=list(map(s.Matrix,R))
    M=s.Matrix([[R[i][j][k]-R[j][i][k] for i in range(n)] for j in range(n) for k in range(n)])
    basis=M.nullspace(); z=len(basis)
    for scale in range(1,z*(z-1)*(z-1)//2+3):
        v=sum((scale**j*b for j,b in enumerate(basis)),s.zeros(n,1))
        H=sum((v[i]*N[i] for i in range(n)),s.zeros(n))
        require(all(H*A==A*H for A in N),'central separating matrix')
        p=H.charpoly(fa.x).as_poly(); fac=p.factor_list()[1]
        if sum(f.degree() for f,m in fac)==z:break
    else: raise ValueError('no central separating element')
    require(all(s.integer_nthroot(m,2)[1] for f,m in fac),'primitive block multiplicities must be squares')
    return {'centre_dimension':z,'scale':scale,'central_coefficients':[str(x) for x in v],
            'centre_basis':[[str(x) for x in b] for b in basis]},fac

def inventory():
    rings=[]; polys={}
    for r in rows():
        R=r['tensor'];comm=old.comm(R); entries=[]
        if comm:
            for i,A in enumerate(R):
                for f,m in s.Matrix(A).charpoly(fa.x).as_poly().factor_list()[1]:
                    co=fa.coeff(f);key=','.join(co);polys[key]=co
                    entries.append({'object':i,'polynomial':co,'multiplicity':m})
        else:
            f,K,u,d,D,e=fp_character(R);co=[str(x) for x in f.all_coeffs()]
            key=','.join(co);polys[key]=co
            entries.append({'object':'FP_sum','polynomial':co,'multiplicity':1})
            for f,m in old.casimir(R).charpoly(fa.x).as_poly().factor_list()[1]:
                co=fa.coeff(f);key=','.join(co);polys[key]=co
                entries.append({'object':'Casimir','polynomial':co,'multiplicity':m})
            centre,fac=centre_separator(R)
            for f,m in fac:
                co=fa.coeff(f);key=','.join(co);polys[key]=co
                entries.append({'object':'separating_centre','polynomial':co,'multiplicity':m})
        rec={k:v for k,v in r.items() if k!='tensor'}|{'commutative':comm,'factors':entries}
        if not comm:rec['centre_certificate']=centre
        rings.append(rec)
    return rings,polys

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--verify-only',action='store_true');ap.add_argument('--reuse-verified-decisions',action='store_true');args=ap.parse_args()
    out=HERE/'cyclotomic_complete.json';rings,polys=inventory()
    if args.verify_only:
        data=json.loads(out.read_text());require(data['rings']==rings,'complete input spectral inventory')
        require(set(data['decisions'])==set(polys),'all distinct factors tested')
        for k,co in polys.items():verify_decision(co,data['decisions'][k])
        print('PASS exact complete cyclotomic decisions',len(polys));return
    previous=json.loads(out.read_text())['decisions'] if args.reuse_verified_decisions and out.exists() else {}
    data={'scope':'All spectra for commutative rings; full irreducible character-trace field via separating centre for noncommutative rings',
          'rings':rings,'decisions':{}};start=time.monotonic()
    for k,co in sorted(polys.items(),key=lambda x:(len(x[1]),x[1])):
        c=previous[k] if k in previous else decide(co)
        verify_decision(co,c);data['decisions'][k]=c
        out.write_text(json.dumps(data,indent=2)+'\n')
        if len(co)>3:print(co,c['reason'],round(time.monotonic()-start,2),flush=True)
    data['excluded_ids']=[r['id'] for r in rings if any(not data['decisions'][','.join(a['polynomial'])]['abelian'] for a in r['factors'])]
    data['elapsed_seconds']=time.monotonic()-start
    out.write_text(json.dumps(data,indent=2)+'\n')
    print('DONE',len(polys),'distinct polynomials',len(data['excluded_ids']),'excluded',flush=True)
if __name__=='__main__':main()
