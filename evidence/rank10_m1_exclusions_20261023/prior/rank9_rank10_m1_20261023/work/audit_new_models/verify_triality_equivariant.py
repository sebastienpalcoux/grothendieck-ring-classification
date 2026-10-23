#!/usr/bin/env python3
"""Independent exact induction-tensor and D16 subgroup audit; standard library only.
The categorical existence input is documented in TRIALITY_EQUIVARIANT_AUDIT.md.
No discovery program is imported. Run from any directory.
"""
import json,itertools,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).parent
P=itertools.product

def empty(n):return [[[0]*n for _ in range(n)] for _ in range(n)]
def triality():
    T=empty(9)
    for g,h in P(range(4),repeat=2):T[g][h][g^h]=1
    for g in range(4):T[g][4][4]=T[4][g][4]=T[4][4][g]=1
    phi=lambda g:g//2
    psi=lambda g:g%2
    for i in range(2):
        for g in range(4):
            T[g][5+i][5+(i^phi(g))]=T[5+i][g][5+(i^psi(g))]=1
            T[g][7+i][7+(i^psi(g))]=T[7+i][g][7+(i^phi(g))]=1
        for j in range(2):
            for a in (5,7):T[4][a+i][a+j]=T[a+i][4][a+j]=1
            T[5+i][7+j][4]=T[7+i][5+j][4]=1
            for g in range(4):
                T[5+i][7+j][g]=int(phi(g)==(i^j))
                T[7+i][5+j][g]=int(psi(g)==(i^j))
            for k in range(2):T[5+i][5+j][7+k]=T[7+i][7+j][5+k]=1
    return T

def group_characters(automorphism):
    # G=<q,s | q^8=s^2=1, s q s=q^automorphism>.
    # Character Fourier frequencies on C8; linear reflection signs separately.
    weights=[(0,),(0,),(4,),(4,)]
    weights += [(k,(automorphism*k)%8) for k in ([1,2,3] if automorphism==7 else [1,2,5])]
    T=empty(7)
    for i,j,k in P(range(7),repeat=3):
        rot=sum((a+b-c)%8==0 for a,b,c in P(weights[i],weights[j],weights[k]))
        refl=0
        if max(i,j,k)<4 and (i//2+j//2-k//2)%2==0:
            refl=(-1)**((i+j+k)%2)
        assert (rot+refl)%2==0
        T[i][j][k]=(rot+refl)//2
        assert T[i][j][k]>=0
    return T

def fusion_checks(T,d):
    n=len(T)
    for i,j in P(range(n),repeat=2):
        assert sum(T[i][j][k]*d[k] for k in range(n))==d[i]*d[j]
        assert T[0][i][j]==int(i==j)==T[i][0][j]
    dual=[]
    for i in range(n):
        ds=[j for j in range(n) if T[i][j][0]]
        assert len(ds)==1 and T[i][ds[0]][0]==1
        dual.append(ds[0])
    for i,j,k,l in P(range(n),repeat=4):
        assert sum(T[i][j][x]*T[x][k][l] for x in range(n))==sum(T[j][k][x]*T[i][x][l] for x in range(n))
    return dual

def reconstruct(automorphism,pairing):
    E=triality();B=group_characters(automorphism)
    F=[[0]*9 for _ in range(9)]
    for i,a in enumerate([0,3,0,3,4,None,4]):
        if a is not None:F[i][a]=1
    F[5][1]=F[5][2]=1
    for i in range(2):F[7+i][5+i]=F[7+i][7+(i^pairing)]=1
    T=empty(9)
    for i,j,k in P(range(7),repeat=3):T[i][j][k]=B[i][j][k]
    for i,j in P(range(9),repeat=2):
        if max(i,j)<7:continue
        answers=[]
        if i>=7:
            x=5+i-7
            answers.append([sum(F[j][a]*E[x][a][z]*F[k][z] for a,z in P(range(9),repeat=2)) for k in range(9)])
        if j>=7:
            x=5+j-7
            answers.append([sum(F[i][a]*E[a][x][z]*F[k][z] for a,z in P(range(9),repeat=2)) for k in range(9)])
        assert all(v==answers[0] for v in answers)
        T[i][j]=answers[0]
    for i,j,z in P(range(9),repeat=3):
        assert sum(T[i][j][k]*F[k][z] for k in range(9))==sum(F[i][a]*F[j][b]*E[a][b][z] for a,b in P(range(9),repeat=2))
    return T,F,E

def subgroup_audit():
    G=frozenset(P(range(8),range(2)))
    mul=lambda x,y:((x[0]+(-1)**x[1]*y[0])%8,x[1]^y[1])
    inv=lambda x:next(y for y in G if mul(x,y)==(0,0))
    def closure(S):
        S=set(S)|{(0,0)}
        while True:
            old=len(S);S|={mul(x,y) for x,y in P(tuple(S),repeat=2)}
            if len(S)==old:return frozenset(S)
    groups={frozenset({(0,0)})};todo=list(groups)
    while todo:
        H=todo.pop()
        for g in G-H:
            K=closure(set(H)|{g})
            if K not in groups:groups.add(K);todo.append(K)
    counts={};allowed=0
    for H in groups:
        N={g for g in G if {mul(mul(g,h),inv(g)) for h in H}==H}
        comm=closure({mul(mul(mul(a,b),inv(a)),inv(b)) for a,b in P(H,repeat=2)})
        ab=len(H)//len(comm)
        lower=len(N)//len(H)*ab
        key=(len(H),len(N),ab,lower);counts[str(key)]=counts.get(str(key),0)+1
        if lower==4:
            assert len(H)==16 or (len(H)==2 and any(h[1] for h in H))
            allowed+=1
        else:assert lower>4
        if len(H)==2 and any(h[1] for h in H):
            remaining=set(G);ds=[]
            while remaining:
                g=min(remaining);D={mul(mul(h,g),k) for h,k in P(H,repeat=2)}
                assert {inv(x) for x in D}==D
                K=H&{mul(mul(g,h),inv(g)) for h in H}
                if len(K)==2:assert all(mul(g,h)==mul(h,g) for h in H)
                ds.append((len(D),len(K)));remaining-=D
            assert sorted(ds)==[(2,2),(2,2),(4,1),(4,1),(4,1)]
    return {'subgroups':len(groups),'subgroup_types_order_normalizer_abelianization_invertible_lower_bound':counts,'compatible_subgroups':allowed,'reflection_double_cosets_self_dual':True}

def main():
    inputs=json.loads((ROOT/'work/input_audit/tensors.json').read_text())
    records=json.loads((ROOT/'work/resolve_small_models/triality_equivariant_certificate.json').read_text())
    report={'arithmetic':'exact integers, standard library only','D16_subgroup_audit':subgroup_audit(),'models':[]}
    assert [r['id'] for r in records]==['R9_1_12','R9_1_108']
    for rec,a,pairing in zip(records,[7,3],[0,1]):
        T,F,E=reconstruct(a,pairing)
        assert T==rec['model_tensor'] and F==rec['restriction_to_triality'] and E==rec['triality_tensor']
        fusion_checks(E,[1]*4+[2]*5)
        dual=fusion_checks(T,[1]*4+[2]*3+[4]*2)
        p=rec['source_to_model'];R=inputs[rec['id']]
        assert sorted(p)==list(range(9))
        for i,j,k in P(range(9),repeat=3):assert R[i][j][k]==T[p[i]][p[j]][p[k]]
        assert max(v for row in T for cell in row for v in cell)==1
        report['models'].append({'id':rec['id'],'all_729_original_coefficients_verified':True,'source_to_model':p,'model_dual_permutation':dual,'categorical_existence_status':'accepted baseline' if pairing==0 else 'accepted direct inner-twist action; see categorical audit'})
    (OUT/'triality_equivariant_audit.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
