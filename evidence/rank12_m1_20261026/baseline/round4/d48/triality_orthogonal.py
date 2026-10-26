"""Exact O^+(4,2) check for the non-GT C3 extension of Vec(V4)."""
from setup import *

def apply(cols,v):
    r=0
    for i in range(4):
        if v>>i&1:r^=cols[i]
    return r
def product(A,B):return tuple(apply(A,v) for v in B)
def power(A,k):
    r=(1,2,4,8)
    for _ in range(k):r=product(r,A)
    return r
def quadratic(v):return ((v&1)*((v>>2)&1)+((v>>1)&1)*((v>>3)&1))%2
def span(vs):return frozenset(apply(vs,v) for v in range(1<<len(vs)))

def main():
    I=(1,2,4,8)
    O=[c for c in itertools.product(range(16),repeat=4) if len(span(c))==16 and all(quadratic(apply(c,v))==quadratic(v) for v in range(16))]
    L=sorted(set(span((a,b)) for a,b in itertools.combinations(range(1,16),2) if len(span((a,b)))==4 and all(quadratic(v)==0 for v in span((a,b)))),key=lambda s:sorted(s))
    # x in V4, y in its character group. The nontrivial alternating cocycle
    # sends (x1,x2,y1,y2) -> (x1,x2,y1+x2,y2+x1).
    shear=(9,6,4,8)
    order3=[c for c in O if c!=I and product(product(c,c),c)==I]
    rows=[]
    for c in order3:
        stable=[sorted(l) for l in L if frozenset(apply(c,v) for v in l)==l]
        fixed=[v for v in range(16) if apply(c,v)==v]
        rows.append(dict(matrix_columns=c,stable_lagrangians=stable,fixed_vectors=fixed,
                         soft_shear_commutes=product(c,shear)==product(shear,c),
                         fixed_projection_to_V4=sorted(set(v&3 for v in fixed))))
    ng=[r for r in rows if not r['stable_lagrangians']]
    Y=frozenset([0,4,8,12])
    parabolic=[p for p in O if frozenset(apply(p,v) for v in Y)==Y]
    for r in ng:
        c=tuple(r['matrix_columns']);c2=product(c,c)
        normalizer=[]
        for p in parabolic:
            direct=product(p,c)==product(c,p)
            inverse=product(p,c)==product(c2,p)
            if direct or inverse:
                normalizer.append(dict(matrix_columns=p,grade_action=1 if direct else -1,
                                       induced_V4=[apply(p,v)&3 for v in range(4)],
                                       order=next(k for k in range(1,73) if power(p,k)==I)))
        r['neutral_parabolic_normalizer']=normalizer
    result=dict(orthogonal_order=len(O),lagrangians=[sorted(l) for l in L],order3_elements=rows,
                nonGT_count=len(ng),nonGT_soft_shear_commuting=sum(r['soft_shear_commutes'] for r in ng))
    (OUT/'triality_orthogonal.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
