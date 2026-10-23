import itertools,json,sys,hashlib
from pathlib import Path
import sympy as s
from signed_bridge import build
from saturation_scan import saturate
P=Path(__file__).resolve().parent;ROOT=P.parents[1]

def extra(R):
    result=saturate(R);triples,eqs=build(R);rows={}
    result['tensor_sha256']=hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()
    for step in result['deductions']:
        for r in step['new_relations']:rows[r.bit_length()-1]=r
    def reduce(v):
        for p in sorted(rows,reverse=True):
            if v>>p&1:v^=rows[p]
        return v
    free=[i for i in range(len(triples)) if i not in rows]
    var=[reduce(1<<i) for i in range(len(triples))]
    gauge=[sum((t.count(i)%2)<<a for a,t in enumerate(triples)) for i in range(1,len(R))]
    gauges={0}
    for v in gauge:gauges|={x^v for x in list(gauges)}
    reps={}
    for z in range(1<<len(free)):
        zfull=sum(((z>>j)&1)<<i for j,i in enumerate(free))
        values=sum(((v&zfull).bit_count()%2)<<i for i,v in enumerate(var))
        representative=min(values^g for g in gauges)
        if representative in reps:continue
        if any(sum(c*(-1 if (m&values).bit_count()%2 else 1) for m,c in p.items()) for _,p in eqs):continue
        T=[[[R[i][j][k] for k in range(len(R))] for j in range(len(R))] for i in range(len(R))]
        for a,t in enumerate(triples):
            sign=-1 if representative>>a&1 else 1
            for i,j,k in set(itertools.permutations(t)):T[i][j][k]=sign
        parity=[]
        for i in range(1,len(R)):
            plus=[j for j in range(1,len(R)) if T[j][j][i]==1]
            minus=[j for j in range(1,len(R)) if T[j][j][i]==-1]
            if plus and minus:parity.append({'object':i,'positive_squares':plus,'negative_squares':minus})
        N=list(map(s.Matrix,T));C=sum((A*A.T for A in N),s.zeros(len(R)))
        cp=C.charpoly().as_poly().factor_list()[1]
        failures=[]
        original_N=list(map(s.Matrix,R));original_C=sum((A*A.T for A in original_N),s.zeros(len(R)))
        original_factors=original_C.charpoly().as_poly().factor_list()[1]
        if representative:
            for q,e in cp:
                why=None
                for g,_ in original_factors:
                    ratio=s.Rational(abs(q.TC())**g.degree(),abs(g.TC())**q.degree())
                    if ratio.q!=1:
                        why={'dimension_polynomial':list(map(int,q.all_coeffs())),'divisor_polynomial':list(map(int,g.all_coeffs())),'cross_norm_ratio':[int(ratio.p),int(ratio.q)]};break
                failures.append(why)
        reps[representative]={'representative':representative,'tensor':T,'adjoint_parity_failures':parity,'codegree_factors':[(list(map(int,q.all_coeffs())),int(e)) for q,e in cp],'cross_norm_failures':failures,'excluded':bool(representative) and all(failures)}
    return {'base_saturation':result,'sign_gauge_classes':list(reps.values())}

if __name__=='__main__':
    tensors=json.loads((ROOT/'work/input_audit/tensors.json').read_text());out={}
    for id in ['R9_1_12','R10_1_10','R10_1_36']:
        out[id]=extra(tensors[id]);out[id]['base_saturation']['id']=id
        print(id,[{k:v for k,v in r.items() if k!='tensor'} for r in out[id]['sign_gauge_classes']],flush=True)
    (P/'extra_signed.json').write_text(json.dumps(out,indent=2)+'\n')
