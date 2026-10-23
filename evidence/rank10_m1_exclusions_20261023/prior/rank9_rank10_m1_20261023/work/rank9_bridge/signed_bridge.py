"""Exact sign-associativity analysis of a self-dual multiplicity-free ring.

No pivotal/indicator normalization is used.  Every nonzero signed coefficient
is a sign, indexed by an unordered triple of non-unit labels.  Associativity
is evaluated in the group algebra of F_2^v.  Two-term equations yield necessary
linear equations on sign exponents.  Repeated reduction is exact.
"""
import collections, gzip, hashlib, itertools, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]

def read_ring():
    line=gzip.open(ROOT/'inputs/rank9_M1_verified/FusionRingMultiplicationTables.txt.gz','rt').read().splitlines()[40]
    return json.loads(line.replace('{','[').replace('}',']'))

def build(R):
    n=len(R)
    assert all(R[i][j][0]==int(i==j) for i in range(n) for j in range(n))
    assert all(R[i][j][k] in (0,1) for i,j,k in itertools.product(range(n),repeat=3))
    triples=[t for t in itertools.combinations_with_replacement(range(1,n),3) if R[t[0]][t[1]][t[2]]]
    ix={t:i for i,t in enumerate(triples)}
    def mono(i,j,k):
        if not R[i][j][k]: return None
        if 0 in (i,j,k): return 0
        return 1<<ix[tuple(sorted((i,j,k)))]
    eqs=[]
    for i,j,k,l in itertools.product(range(n),repeat=4):
        p=collections.Counter()
        for h in range(n):
            a,b=mono(i,j,h),mono(h,k,l)
            if a is not None and b is not None:p[a^b]+=1
            a,b=mono(j,k,h),mono(i,h,l)
            if a is not None and b is not None:p[a^b]-=1
        p={m:c for m,c in p.items() if c}
        if p: eqs.append(((i,j,k,l),p))
    # Every equation is satisfied by the original all-positive table.
    assert all(sum(p.values())==0 for _,p in eqs)
    return triples,eqs

def analyze(R):
    triples,eqs=build(R)
    basis={}; deductions=[]
    def reduce(m):
        for pivot in sorted(basis,reverse=True):
            if m>>pivot&1:m^=basis[pivot]
        return m
    def reduce_poly(p):
        q=collections.Counter()
        for m,c in p.items():q[reduce(m)]+=c
        return {m:c for m,c in q.items() if c}
    passes=0
    while True:
        before=len(basis);passes+=1
        for source,p in eqs:
            q=reduce_poly(p)
            if len(q)==2:
                (a,ca),(b,cb)=sorted(q.items())
                assert ca==-cb
                relation=reduce(a^b)
                if relation:
                    basis[relation.bit_length()-1]=relation
                    deductions.append({'associativity_indices':list(source),'reduced_terms':[[a,ca],[b,cb]],'relation':relation})
        if len(basis)==before:break
    residues=[(source,reduce_poly(p)) for source,p in eqs if reduce_poly(p)]
    # Gauge action s_i -> signs of coefficients s_i*s_j*s_k.
    gauge=[]
    for i in range(1,len(R)):
        vec=sum((sum(x==i for x in t)%2)<<a for a,t in enumerate(triples))
        gauge.append(vec)
    def gf2_rank(rows):
        piv={}
        for x in rows:
            for i in sorted(piv,reverse=True):
                if x>>i&1:x^=piv[i]
            if x:piv[x.bit_length()-1]=x
        return len(piv)
    def parity(x):return x.bit_count()%2
    assert all(parity(x&row)==0 for row in basis.values() for x in gauge)
    grank=gf2_rank(gauge)
    free=[i for i in range(len(triples)) if i not in basis]
    reduced_variables=[reduce(1<<i) for i in range(len(triples))]
    solutions=[]
    unique_residues=list({tuple(sorted(p.items())) for _,p in residues})
    for z in range(1<<len(free)):
        zfull=sum(((z>>j)&1)<<i for j,i in enumerate(free))
        if any(sum(c*(-1 if parity(m&zfull) else 1) for m,c in p) for p in unique_residues):continue
        solutions.append(sum(parity(m&zfull)<<i for i,m in enumerate(reduced_variables)))
    gauges={0}
    for x in gauge:gauges|={y^x for y in list(gauges)}
    representatives=sorted({min(x^g for g in gauges) for x in solutions})
    gauge_coordinate_pivots={};gauge_coordinates=[]
    for j,t in enumerate(triples):
        mask=sum((sum(x==i for x in t)%2)<<(i-1) for i in range(1,len(R)))
        for p in sorted(gauge_coordinate_pivots,reverse=True):
            if mask>>p&1:mask^=gauge_coordinate_pivots[p]
        if mask:
            gauge_coordinate_pivots[mask.bit_length()-1]=mask
            gauge_coordinates.append(j)
    normalized_basis=dict(basis)
    for i in gauge_coordinates:
        row=reduce(1<<i)
        assert row
        basis[row.bit_length()-1]=row
    norm_free=[i for i in range(len(triples)) if i not in basis]
    norm_variables=[reduce(1<<i) for i in range(len(triples))]
    norm_cases=[]
    for z in range(1<<len(norm_free)):
        zfull=sum(((z>>j)&1)<<i for j,i in enumerate(norm_free))
        values=sum(parity(m&zfull)<<i for i,m in enumerate(norm_variables))
        failure=None
        for source,p in eqs:
            value=sum(c*(-1 if parity(m&values) else 1) for m,c in p.items())
            if value:
                failure={'associativity_indices':list(source),'difference':value,'polynomial':list(reduce_poly(p).items())}
                break
        norm_cases.append({'free_bits':z,'sign_assignment':values,'failure':failure})
    saturated_source=(3,3,4,4)
    saturated=next(reduce_poly(p) for source,p in eqs if source==saturated_source)
    assert saturated.get(0)==-3 and sum(abs(c) for m,c in saturated.items() if m)==3
    assert all(c>0 for m,c in saturated.items() if m)
    saturation_rows=[]
    for m,c in saturated.items():
        if not m:continue
        row=reduce(m)
        if row:
            basis[row.bit_length()-1]=row;saturation_rows.append(row)
    assert len(basis)==len(triples)
    return {
        'id':'R9_1_41','rank':len(R),'tensor_sha256':hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest(),
        'triples':[list(x) for x in triples], 'variables':len(triples),'associativity_equations_nonzero':len(eqs),
        'deductions':deductions,'linear_rank':len(normalized_basis),'linear_kernel_dimension':len(triples)-len(normalized_basis),
        'gauge_rank':grank,'gauge_vectors':gauge,'remaining_equations':[[list(x),list(p.items())] for x,p in residues],
        'all_signed_tables_are_gauge_original': representatives==[0],
        'passes':passes,
        'associative_signed_tables':len(solutions),'gauge_orbit_representatives':representatives,
        'solutions':solutions,
        'gauge_coordinates':gauge_coordinates,'normalized_rank':len(triples)-len(norm_free),'normalized_free_variables':norm_free,'normalized_cases':norm_cases,
        'normalized_variable_exponents':norm_variables,
        'final_saturation':{'associativity_indices':list(saturated_source),'polynomial':list(saturated.items()),'new_relations':saturation_rows,'final_rank':len(basis)},
    }

if __name__=='__main__':
    result=analyze(read_ring())
    (Path(__file__).parent/'signed_bridge_certificate.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('triples','deductions','gauge_vectors','remaining_equations','solutions')},indent=2))
    print('residual equations',len(result['remaining_equations']))
