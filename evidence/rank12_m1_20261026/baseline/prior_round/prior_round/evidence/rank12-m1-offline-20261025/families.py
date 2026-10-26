"""Exact positive FP characters and patterns for every unresolved case."""
from pathlib import Path
import collections,itertools,json
import sympy as s
from state import current
from fp import exact,require
ROOT=Path(__file__).resolve().parent;t=exact.t

def patterns():
    # Polynomial, positive embedding, exact expressions, multiplicities.
    a=s.Symbol('a')
    return [
      ('D120',[1,-1],[1,2,5],[4,4,4]),
      ('D48',[1,-1],[1,2,4],[8,2,2]),
      ('cubic_C7',[1,-1,-2,1],[1,2*a,2*(a*a-1)],[8,2,2]),
      ('cubic_C9',[1,0,-3,-1],[1,2,1+2*a,2*a*a-2],[4,2,4,2]),
      ('quadratic_C2',[1,0,-2],[1,4+3*a,5+3*a],[2,8,2]),
      ('D144',[1,0,-2],[1,2,3,4,3*a],[2,1,2,3,4]),
      ('D32',[1,0,-2],[1,2,2*a],[8,2,2]),
      ('D24',[1,-1],[1,2],[8,4]),
      ('D40',[1,0,-5],[1,2,a],[4,4,4]),
      ('quadratic_C6_sqrt10',[1,0,-10],[1,3+a],[6,6]),
      ('quadratic_C6_sqrt13',[1,0,-13],[1,(3+a)/2],[6,6]),
    ]

def build():
    ex,mo=current();data=json.loads((ROOT/'tensors.json').read_text());profiles=json.loads((ROOT/'profile.json').read_text())['records'];cache=[];a=s.Symbol('a')
    for name,co,expr,mult in patterns():
        f=exact.poly(co);K=exact.field(f);u=K(s.Poly(t,t).rem(f).all_coeffs());emb=max(exact.embeddings(f),key=lambda e:e.hi)
        vals=[]
        for v in expr:
            p=s.Poly(v,a,domain=s.QQ);vals.append(K(p.all_coeffs()))
        approximation=[float(s.N(s.sympify(v).subs(a,float(emb.hi)),16))for v in expr]
        cache.append((name,f,K,u,emb,vals,approximation,mult))
    out=[]
    for p in profiles:
        if p['id']in ex or p['id']in mo:continue
        matched=None
        for name,f,K,u,emb,vals,approx,mult in cache:
            indices=[min(range(len(vals)),key=lambda i:abs(d-approx[i]))for d in p['fp_hint']]
            if any(abs(d-approx[i])>1e-5 for d,i in zip(p['fp_hint'],indices)):continue
            if [indices.count(i)for i in range(len(vals))]!=mult:continue
            ds=[vals[i]for i in indices];R=data[p['id']]
            require(ds[0]==K.one and all(emb.sign(v)>0 for v in ds),'positive normalized character')
            require(all(sum((K(R[i][j][k])*ds[k]for k in range(12)),K.zero)==ds[i]*ds[j]for i,j in itertools.product(range(12),repeat=2)),'every exact FP character equation')
            matched=dict(id=p['id'],tensor_sha256=p['tensor_sha256'],family=name,field_polynomial=exact.pc(f),positive_root_interval=[str(emb.lo),str(emb.hi)],dimensions_in_field=[exact.ec(v)for v in ds]);break
        require(matched is not None,'unresolved dimension pattern exactly identified');out.append(matched)
    (ROOT/'unresolved_families.json').write_text(json.dumps(dict(records=out,counts=dict(collections.Counter(r['family']for r in out))),indent=2)+'\n')
    print('PASS exact dimension patterns for',len(out),'unresolved rings')
if __name__=='__main__':build()
