"""General exact sign-associativity saturation, no indicator assumptions."""
import collections,hashlib,itertools,json,sys,time
from pathlib import Path
import sympy as s
from signed_bridge import build

P=Path(__file__).resolve().parent;ROOT=P.parents[1]

def rank2(vectors):
    rows={}
    for v in vectors:
        for p in sorted(rows,reverse=True):
            if v>>p&1:v^=rows[p]
        if v:rows[v.bit_length()-1]=v
    return len(rows)

def saturate(R):
    triples,eqs=build(R);rows={};deductions=[]
    def reduce(v):
        for p in sorted(rows,reverse=True):
            if v>>p&1:v^=rows[p]
        return v
    def poly(p):
        q=collections.Counter()
        for m,c in p.items():q[reduce(m)]+=c
        return {m:c for m,c in q.items() if c}
    passes=0
    while True:
        count=len(rows);passes+=1
        for source,p in eqs:
            q=poly(p)
            if not q:continue
            dominant=max(q,key=lambda m:abs(q[m]))
            if abs(q[dominant])==sum(abs(c) for m,c in q.items() if m!=dominant):
                assert all(c*q[dominant]<0 for m,c in q.items() if m!=dominant)
                new=[]
                for m in q:
                    if m==dominant:continue
                    v=reduce(m^dominant)
                    if v:rows[v.bit_length()-1]=v;new.append(v)
                if new:deductions.append({'associativity_indices':list(source),'reduced_polynomial':list(q.items()),'dominant_monomial':dominant,'new_relations':new})
        if count==len(rows):break
    gauge=[sum((t.count(i)%2)<<a for a,t in enumerate(triples)) for i in range(1,len(R))]
    assert all((v&row).bit_count()%2==0 for v in gauge for row in rows.values())
    free=len(triples)-len(rows);grank=rank2(gauge)
    out={'variables':len(triples),'linear_rank':len(rows),'kernel_dimension':free,'gauge_rank':grank,'gauge_trivial':free==grank,'deductions':deductions,'triples':list(map(list,triples)),'passes':passes}
    if free==grank:
        N=list(map(s.Matrix,R));C=sum((A*A.T for A in N),s.zeros(len(R)))
        factors=C.charpoly().as_poly().factor_list()[1]
        out['codegree_factors']=[list(map(int,q.all_coeffs())) for q,_ in factors]
        out['codegree_multiplicities']=[int(e) for _,e in factors]
        # A norm obstruction suffices to reject all possible dimension codegrees.
        # For D root of f degree d and h other formal codegree irreducible g
        # degree e, norm(D/h) in common splitting field has necessary rational
        # integrality: Norm(f)^e / Norm(g)^d must be an integer.
        # Better use algebraic-integer norm of D/c for integer codegree c.
        candidate_fail=[]
        for q,e in factors:
            why=None
            for g,ge in factors:
                ratio=s.Rational(abs(q.TC())**g.degree(),abs(g.TC())**q.degree())
                if ratio.q!=1:
                    why={'kind':'cross_norm_codegree','divisor_polynomial':list(map(int,g.all_coeffs())),'cross_norm_ratio':[int(ratio.p),int(ratio.q)]};break
            candidate_fail.append({'dimension_polynomial':list(map(int,q.all_coeffs())),'failure':why})
        out['dimension_codegree_tests']=candidate_fail
        out['general_exclusion_by_codegree_norm']=all(x['failure'] for x in candidate_fail)
    return out

def main():
    tensors=json.loads((ROOT/'work/input_audit/tensors.json').read_text())
    audits=json.loads((ROOT/'work/input_audit/audit.json').read_text())
    selfdual={r['id'] for k,v in audits.items() for r in v['rings'] if r['dual']==list(range(v['rank']))}
    survivors={r['id'] for r in json.loads((ROOT/'work/obstructions/survivors.json').read_text())}
    targets=sorted(survivors&selfdual,key=lambda x:tuple(map(int,x[1:].split('_'))))
    if len(sys.argv)>1:targets=sys.argv[1:]
    results={}
    for id in targets:
        t=time.monotonic()
        r=saturate(tensors[id]);r['id']=id
        r['tensor_sha256']=hashlib.sha256(json.dumps(tensors[id],separators=(',',':')).encode()).hexdigest()
        results[id]=r
        print(id,{k:v for k,v in r.items() if k in ('variables','linear_rank','kernel_dimension','gauge_rank','gauge_trivial','codegree_factors','general_exclusion_by_codegree_norm')},'seconds',round(time.monotonic()-t,3),flush=True)
        (P/'saturation_scan.json').write_text(json.dumps(results,indent=2)+'\n')
if __name__=='__main__':main()
