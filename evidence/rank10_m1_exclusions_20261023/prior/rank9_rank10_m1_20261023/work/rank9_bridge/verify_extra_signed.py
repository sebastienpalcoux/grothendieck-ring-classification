"""Independent sign-branch coverage and cross-norm arithmetic verification."""
import hashlib,itertools,json
from pathlib import Path
import sympy as s
from verify_saturation import verify as verify_base

def check(R,c):
    base=c['base_saturation'];assert not verify_base(R,base)['sphericality_proved']
    n=len(R);I=range(n);triples=[tuple(t) for t in base['triples']];rows={}
    for step in base['deductions']:
        for v in step['new_relations']:rows[v.bit_length()-1]=v
    def normal(v):
        for p in sorted(rows,reverse=True):
            if v>>p&1:v^=rows[p]
        return v
    free=[i for i in range(len(triples)) if i not in rows];var=[normal(1<<i) for i in range(len(triples))]
    gauges={0}
    for j in range(1,n):
        v=sum((t.count(j)%2)<<a for a,t in enumerate(triples));gauges|={x^v for x in list(gauges)}
    candidates=set()
    for z in range(1<<len(free)):
        full=sum(((z>>j)&1)<<i for j,i in enumerate(free))
        v=sum(((m&full).bit_count()%2)<<a for a,m in enumerate(var))
        candidates.add(min(v^g for g in gauges))
    actual={}
    for v in candidates:
        T=[[[R[i][j][k] for k in I] for j in I] for i in I]
        for a,t in enumerate(triples):
            for i,j,k in set(itertools.permutations(t)):T[i][j][k]=-1 if v>>a&1 else 1
        if all(sum(T[i][j][h]*T[h][k][l] for h in I)==sum(T[j][k][h]*T[i][h][l] for h in I) for i,j,k,l in itertools.product(I,repeat=4)):actual[v]=T
    assert set(actual)=={b['representative'] for b in c['sign_gauge_classes']}
    N=list(map(s.Matrix,R));C=sum((A*A.T for A in N),s.zeros(n));original={tuple(map(int,f.all_coeffs())):f for f,e in C.charpoly().as_poly().factor_list()[1]}
    nontrivial=0
    for b in c['sign_gauge_classes']:
        v=b['representative'];T=actual[v];assert T==b['tensor']
        if not v:continue
        nontrivial+=1
        N=list(map(s.Matrix,T));C=sum((A*A.T for A in N),s.zeros(n));factors=C.charpoly().as_poly().factor_list()[1]
        assert len(factors)==len(b['cross_norm_failures'])
        for (f,e),w in zip(factors,b['cross_norm_failures']):
            assert w is not None and w['dimension_polynomial']==list(map(int,f.all_coeffs()))
            g=original[tuple(w['divisor_polynomial'])]
            ratio=s.Rational(abs(f.TC())**g.degree(),abs(g.TC())**f.degree())
            assert ratio.q!=1 and w['cross_norm_ratio']==[int(ratio.p),int(ratio.q)]
        assert b['excluded']
    return {'id':base['id'],'signed_gauge_classes':len(actual),'nontrivial_classes_excluded':nontrivial,'general_implies_spherical':True,'PASS':True}

if __name__=='__main__':
    P=Path(__file__).resolve().parent;ROOT=P.parents[1]
    tensors=json.loads((ROOT/'work/input_audit/tensors.json').read_text());data=json.loads((P/'extra_signed.json').read_text())
    out=[check(tensors[id],c) for id,c in data.items()]
    (P/'extra_signed_verification.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
