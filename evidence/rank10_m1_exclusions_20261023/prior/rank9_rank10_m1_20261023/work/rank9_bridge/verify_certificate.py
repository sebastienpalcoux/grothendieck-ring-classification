"""Independent exact verifier for the R9_1_41 sphericality certificate.

Uses only Python integer arithmetic for all sign deductions. SymPy is used
only to calculate the characteristic polynomial of the exact Casimir matrix.
It neither calls the discovery routine nor trusts its claimed exhaustive list.
"""
import hashlib,itertools,json
from pathlib import Path
import sympy as s

P=Path(__file__).resolve().parent

def verify(R,c):
    n=len(R);I=range(n)
    assert hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()==c['tensor_sha256']
    assert all(R[i][j][k] in (0,1) for i,j,k in itertools.product(I,repeat=3))
    assert all(R[0][i][j]==R[i][0][j]==int(i==j) for i,j in itertools.product(I,repeat=2))
    assert all(R[i][j][0]==int(i==j) for i,j in itertools.product(I,repeat=2))
    assert all(R[i][j][k]==R[j][i][k]==R[i][k][j] for i,j,k in itertools.product(I,repeat=3))
    assert all(sum(R[i][j][h]*R[h][k][l] for h in I)==sum(R[j][k][h]*R[i][h][l] for h in I) for i,j,k,l in itertools.product(I,repeat=4))
    triples=[t for t in itertools.combinations_with_replacement(range(1,n),3) if R[t[0]][t[1]][t[2]]]
    assert c['triples']==[list(t) for t in triples]
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
        assert len(q)==2 and sum(q.values())==0
        assert sorted(map(list,q.items()))==step['reduced_terms']
        a,b=list(q)
        assert add(a^b)==step['relation']
    assert len(rows)==36==c['linear_rank']
    gauge_rows={}
    for j in c['gauge_coordinates']:
        t=triples[j]
        mask=sum((t.count(i)%2)<<(i-1) for i in range(1,n))
        for p in sorted(gauge_rows,reverse=True):
            if mask>>p&1:mask^=gauge_rows[p]
        assert mask;gauge_rows[mask.bit_length()-1]=mask
        add(1<<j)
    assert len(gauge_rows)==n-1==8 and len(rows)==44
    assert [normal(1<<i) for i in range(len(triples))]==c['normalized_variable_exponents']
    final=c['final_saturation']
    q=quotient(equation(final['associativity_indices']))
    assert sorted(q.items())==sorted(map(tuple,final['polynomial']))
    assert q[0]==-3 and all(v>0 for m,v in q.items() if m) and sum(v for m,v in q.items() if m)==3
    # Sum of three signed terms attains its upper bound: every term is +1.
    added=[]
    for m,v in q.items():
        if m and normal(m):added.append(add(m))
    assert added==final['new_relations']
    assert len(rows)==47==len(triples)==final['final_rank']
    N=list(map(s.Matrix,R));C=sum((A*A.T for A in N),s.zeros(n));x=s.Symbol('x')
    expected=(x-15)**6*(x-2)*(x*x-120*x+1200)
    assert s.Poly(C.charpoly(x).as_expr()-expected,x).is_zero
    assert s.Rational(2,15).q!=1 and s.Rational(15,2).q!=1
    # The norm of (60 +/-20 sqrt(6))/15 is 1200/225=16/3.
    assert s.Rational(1200,15**2)==s.Rational(16,3)
    return {'id':'R9_1_41','status':'generally_excluded','sphericality':'all associative signed quotients are basis-sign gauges of R','signed_variables':47,'linear_relations':36,'gauge_normalizations':8,'saturation_relations':3,'codegrees':['2','15 (multiplicity 6)','60+20*sqrt(6)','60-20*sqrt(6)'],'PASS':True}

if __name__=='__main__':
    result=verify(json.loads((P/'tensor.json').read_text()),json.loads((P/'signed_bridge_certificate.json').read_text()))
    (P/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
