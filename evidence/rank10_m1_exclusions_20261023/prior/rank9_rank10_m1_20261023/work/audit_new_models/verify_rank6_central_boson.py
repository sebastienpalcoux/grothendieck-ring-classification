#!/usr/bin/env python3
"""Independent finite input for the dimension24 rank6 unique-boson lemma.
Enumerates O^+(4,2) by images of basis vectors, not the discovery matrices.
Also checks the three sign-quotient profiles in the original dimension48 rings.
"""
import itertools,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).parent
P=itertools.product
I=(1,2,4,8)
def q(x):return ((x&3)&(x>>2)).bit_count()%2
def act(M,x):
    y=0
    for i in range(4):
        if x>>i&1:y^=M[i]
    return y
def compose(M,N):return tuple(act(M,x) for x in N)
def inverse(M):return tuple(next(x for x in range(16) if act(M,x)==e) for e in I)
def rows(M):return [sum(((M[j]>>i)&1)<<j for j in range(4)) for i in range(4)]
def main():
    O=[]
    for M in P(range(1,16),repeat=4):
        vals=[act(M,x) for x in range(16)]
        if len(set(vals))==16 and all(q(vals[x])==q(x) for x in range(16)):O.append(M)
    assert len(O)==72
    par=[M for M in O if M[2]&3==M[3]&3==0]
    assert len(par)==12
    candidates=[M for M in O if M!=I and compose(compose(M,M),M)==I and M[2]&3 and M[3]&3 and M[2]&3!=M[3]&3]
    assert len(candidates)==6
    left=set(candidates);classes=[]
    while left:
        M=min(left)
        orbit={compose(compose(p,m),inverse(p)) for p in par for m in (M,inverse(M))}
        assert orbit<=set(candidates);left-=orbit
        fixed=[x for x in range(16) if act(M,x)==x]
        assert all(q(x)==1 for x in fixed if x)
        norms=[s for s in par if compose(s,s)==I and compose(compose(s,M),s)==inverse(M) and (s[0]&3,s[1]&3)!=(1,2)]
        assert len(norms)==3
        for N in orbit:assert all(x==0 or q(x)==1 for x in range(16) if act(N,x)==x)
        classes.append({'representative_rows':rows(M),'parabolic_and_inversion_orbit_size':len(orbit),'triality_fixed_vectors':fixed,'fixed_twists':[1 if q(x)==0 else -1 for x in fixed],'involutive_neutral_transposition_normalizers':[rows(s) for s in norms]})
    assert sorted(c['parabolic_and_inversion_orbit_size'] for c in classes)==[2,4]
    # The cyclic-order-four neutral alternative has no triality.
    o_c4=[]
    for a,b,c,d in P(range(4),repeat=4):
        vals=[((a*x+b*y)%4,(c*x+d*y)%4) for x,y in P(range(4),repeat=2)]
        if len(set(vals))==16 and all((u*v-x*y)%4==0 for (x,y),(u,v) in zip(P(range(4),repeat=2),vals)):o_c4.append((a,b,c,d))
    assert len(o_c4)==4
    inputs=json.loads((ROOT/'work/input_audit/tensors.json').read_text());profiles=[]
    for rid in ('R9_1_12','R9_1_62','R9_1_87','R9_1_108'):
        T=inputs[rid];n=len(T)
        inv=[i for i in range(n) if all(sum(T[i][j])==1 for j in range(n))]
        rest=[i for i in range(n) if i not in inv];poss=[]
        for twos in itertools.combinations(rest,3):
            d=[1 if i in inv else 2 if i in twos else 4 for i in range(n)]
            if all(sum(T[i][j][k]*d[k] for k in range(n))==d[i]*d[j] for i,j in P(range(n),repeat=2)):poss.append(d)
        assert len(poss)==1;d=poss[0];ps=[]
        for g in inv:
            if g==0:continue
            perm=[next(k for k,x in enumerate(T[g][j]) if x) for j in range(n)]
            assert all(perm[perm[j]]==j for j in range(n))
            unseen=set(range(n));quot=[]
            while unseen:
                j=min(unseen);k=perm[j];unseen.discard(j);unseen.discard(k)
                if j==k:
                    assert d[j]%2==0;quot.extend([d[j]//2]*2)
                else:quot.append(d[j])
            quot.sort();assert sum(x*x for x in quot)==24
            ps.append({'sign_original_basis_id':g,'quotient_dimensions':quot})
        assert sorted(tuple(p['quotient_dimensions']) for p in ps)==sorted([(1,)*8+(4,),(1,)*4+(2,4),(1,)*4+(2,)*5])
        ng=next(p['sign_original_basis_id'] for p in ps if p['quotient_dimensions']==[1]*8+[4])
        profiles.append({'id':rid,'dimensions':d,'all_sign_quotients':ps,'near_group_sign':ng})
    report={'status':'PASS','cyclic_order_four_center_isometries':o_c4,'cyclic_order_four_center_isometry_order':4,'orthogonal_group_order':72,'parabolic_order':12,'admissible_order_three_matrices':6,'classes':classes,'conclusion':'Every triality-fixed nonzero central invertible is fermionic; there is no nonzero isotropic fixed vector.','original_sign_profiles':profiles}
    (OUT/'rank6_central_boson_audit.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
