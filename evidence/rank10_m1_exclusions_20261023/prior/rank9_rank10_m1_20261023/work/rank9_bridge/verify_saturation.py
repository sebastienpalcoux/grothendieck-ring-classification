"""Independent verifier of saturated sign-associativity certificates."""
import hashlib,itertools,json
from pathlib import Path
import sympy as s

def verify(R,c):
    n=len(R);I=range(n)
    assert hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()==c['tensor_sha256']
    assert all(R[i][j][k] in (0,1) for i,j,k in itertools.product(I,repeat=3))
    assert all(R[0][i][j]==R[i][0][j]==int(i==j) for i,j in itertools.product(I,repeat=2))
    assert all(R[i][j][0]==int(i==j) for i,j in itertools.product(I,repeat=2))
    assert all(R[i][j][k]==R[j][i][k]==R[i][k][j] for i,j,k in itertools.product(I,repeat=3))
    assert all(sum(R[i][j][h]*R[h][k][l] for h in I)==sum(R[j][k][h]*R[i][h][l] for h in I) for i,j,k,l in itertools.product(I,repeat=4))
    triples=[t for t in itertools.combinations_with_replacement(range(1,n),3) if R[t[0]][t[1]][t[2]]]
    assert c['triples']==list(map(list,triples))
    index={t:j for j,t in enumerate(triples)}
    def mon(i,j,k):
        if not R[i][j][k]:return None
        return 0 if 0 in (i,j,k) else 1<<index[tuple(sorted((i,j,k)))]
    def equation(q):
        i,j,k,l=q; result={}
        for h in I:
            for sign,a,b in [(1,mon(i,j,h),mon(h,k,l)),(-1,mon(j,k,h),mon(i,h,l))]:
                if a is not None and b is not None:result[a^b]=result.get(a^b,0)+sign
        return {m:v for m,v in result.items() if v}
    rows={}
    def normal(m):
        for p in sorted(rows,reverse=True):
            if m>>p&1:m^=rows[p]
        return m
    def add(m):
        m=normal(m);assert m;rows[m.bit_length()-1]=m
        return m
    def quotient(eq):
        ans={}
        for m,v in eq.items():
            r=normal(m);ans[r]=ans.get(r,0)+v
        return {r:v for r,v in ans.items() if v}
    for step in c['deductions']:
        q=quotient(equation(step['associativity_indices']))
        assert sorted(q.items())==sorted(map(tuple,step['reduced_polynomial']))
        d=step['dominant_monomial']
        assert d in q and abs(q[d])==sum(abs(v) for m,v in q.items() if m!=d)
        assert all(q[d]*v<0 for m,v in q.items() if m!=d)
        new=[]
        for m in q:
            if m!=d and normal(m^d):new.append(add(m^d))
        assert new==step['new_relations']
    assert len(rows)==c['linear_rank']
    gauge=[sum((t.count(i)%2)<<a for a,t in enumerate(triples)) for i in range(1,n)]
    grows={}
    for v in gauge:
        assert all((v&r).bit_count()%2==0 for r in rows.values())
        for p in sorted(grows,reverse=True):
            if v>>p&1:v^=grows[p]
        if v:grows[v.bit_length()-1]=v
    assert len(grows)==c['gauge_rank']
    trivial=len(triples)-len(rows)==len(grows)
    assert trivial==c['gauge_trivial']
    if not trivial:return {'id':c['id'],'sphericality_proved':False,'generally_excluded':False,'PASS':True}
    N=list(map(s.Matrix,R));C=sum((A*A.T for A in N),s.zeros(n));factors=C.charpoly().as_poly().factor_list()[1]
    assert c['codegree_factors']==[list(map(int,q.all_coeffs())) for q,_ in factors]
    assert c['codegree_multiplicities']==[int(e) for _,e in factors]
    polynomials={tuple(map(int,q.all_coeffs())):q for q,e in factors}
    failures=[]
    for (q,e),test in zip(factors,c['dimension_codegree_tests']):
        assert test['dimension_polynomial']==list(map(int,q.all_coeffs()))
        fail=test['failure']
        if fail is not None:
            divisor=tuple(fail['divisor_polynomial']);assert divisor in polynomials
            g=polynomials[divisor]
            norm=s.Rational(abs(q.TC())**g.degree(),abs(g.TC())**q.degree())
            assert norm.q!=1 and fail['cross_norm_ratio']==[int(norm.p),int(norm.q)]
        failures.append(fail is not None)
    excluded=all(failures)
    assert excluded==c['general_exclusion_by_codegree_norm']
    return {'id':c['id'],'sphericality_proved':True,'generally_excluded':excluded,'PASS':True}

if __name__=='__main__':
    P=Path(__file__).resolve().parent;ROOT=P.parents[1]
    tensors=json.loads((ROOT/'work/input_audit/tensors.json').read_text())
    certificates=json.loads((P/'saturation_scan.json').read_text())
    results=[verify(tensors[id],c) for id,c in certificates.items()]
    (P/'saturation_verification.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps({'checks':len(results),'sphericality':sum(x['sphericality_proved'] for x in results),'general_exclusions':[x['id'] for x in results if x['generally_excluded']],'PASS':True},indent=2))
