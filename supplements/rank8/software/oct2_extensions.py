"""Small tensor constructions and graded-category obstructions, 2026-10-02.

All arithmetic is integer arithmetic. The categorical theorems justifying the
constructors and obstruction certificates are stated in the accompanying paper.
"""
from itertools import product
from functools import lru_cache
import json, hashlib
from pathlib import Path


def require(ok, message='exact condition failed'):
    if not ok:
        raise ValueError(message)


def tensor(n):
    return [[[0]*n for _ in range(n)] for _ in range(n)]


def quadratic(group, multiplicity):
    add=(lambda g,h:(g+h)%4) if group=='C4' else (lambda g,h:g^h)
    neg=(lambda g:-g%4) if group=='C4' else (lambda g:g)
    T=tensor(8)
    for g,h in product(range(4),repeat=2):
        T[g][h][add(g,h)]=1
        T[g][4+h][4+add(g,h)]=1
        T[4+g][h][4+add(g,neg(h))]=1
        T[4+g][4+h][add(g,neg(h))]=1
        for a in range(4):T[4+g][4+h][4+a]=multiplicity
    return T


def fib_swap():
    F=[[[1,0],[0,1]],[[0,1],[1,1]]]
    lab=list(product(range(2),repeat=3))
    # Keep model labels in (a,b,g), ordered by g then a then b.
    lab=[(a,b,g) for g in range(2) for a in range(2) for b in range(2)]
    T=tensor(8)
    for i,(a,b,g) in enumerate(lab):
        for j,(c,d,h) in enumerate(lab):
            if g:c,d=d,c
            for k,(e,f,t) in enumerate(lab):
                T[i][j][k]=F[a][c][e]*F[b][d][f] if t==(g+h)%2 else 0
    return T


def ty_diagonal():
    lab=[(a,z) for z in range(4) for a in range(4) if (a==3)==(z%2==1)]
    T=tensor(8)
    for i,(a,g) in enumerate(lab):
        for j,(b,h) in enumerate(lab):
            ks=list(range(3)) if a==b==3 else [3] if a==3 or b==3 else [(a+b)%3]
            for k in ks:T[i][j][lab.index((k,(g+h)%4))]=1
    return T


def ty6_equivariant():
    # T is inversion, with identity tensorator in the standard TY gauge.
    # The action coherence T^2=>Id is -1 on m and +1 on the pointed part.
    # Equivariant m objects therefore have eigenvalues +/- i. Their product
    # acquires the additional -1 appearing in the character trace below.
    A=6;m=A;R=tensor(7)
    for a,b in product(range(A),repeat=2):R[a][b][(a+b)%A]=1
    for a in range(A):R[a][m][m]=R[m][a][m]=R[m][m][a]=1
    sigma=[(-a)%A for a in range(A)]+[m]
    labels=[([0],1),([0],-1),([1,5],0),([2,4],0),([3],1),([3],-1),([m],1),([m],-1)]
    T=tensor(8)
    for i,(oa,sa) in enumerate(labels):
        for j,(ob,sb) in enumerate(labels):
            for k,(oc,sc) in enumerate(labels):
                c=oc[0];dim=sum(R[a][b][c] for a in oa for b in ob)
                if len(oc)==1:
                    tr=sum(R[a][b][c]*sa*sb*(-1 if a==b==m else 1)
                           for a in oa for b in ob if sigma[a]==a and sigma[b]==b)
                    require((dim+sc*tr)%2==0)
                    T[i][j][k]=(dim+sc*tr)//2
                else:T[i][j][k]=dim
    return T


def bosonic_c4():
    # Representatives V_0 z^a and V_2 z^a, a=0,1,2,3.
    reps = [(j, a) for j in (0, 2) for a in range(4)]
    def orbit(j, a):
        # Tensoring by b=V_6 z^2 sends (j,a) to (6-j,a+2).
        return frozenset(((j, a % 4), (6-j, (a+2) % 4)))
    index = {orbit(j, a): i for i, (j, a) in enumerate(reps)}
    require(len(index) == 8)
    require(set().union(*index) == set(product((0,2,4,6), range(4))))
    T = [[[0]*8 for _ in range(8)] for _ in range(8)]
    for x, (j,a) in enumerate(reps):
        for y, (k,c) in enumerate(reps):
            # SU(2)_6: V_j V_k = sum_{l=|j-k| step2}^{min(j+k,12-j-k)} V_l.
            for l in range(abs(j-k), min(j+k,12-j-k)+1, 2):
                T[x][y][index[orbit(l,a+c)]] += 1
    return T



def central_square_root():
    # Base pseudo-PSU(2)_6: 1,g,x,gx with g^2=1 and x^2=g+x+gx.
    B=tensor(4)
    for a,b in product(range(2),repeat=2):
        B[a][b][(a+b)%2]=1
        B[a][2+b][2+(a+b)%2]=B[2+a][b][2+(a+b)%2]=1
        B[2+a][2+b][(a+b+1)%2]=1
        B[2+a][2+b][2]=B[2+a][2+b][3]=1
    # Two regular components, with the central cocycle t(1,1)=g.
    act=[1,0,3,2];T=tensor(8)
    for a,b,i,j,k in product(range(2),range(2),range(4),range(4),range(4)):
        target=4*((a+b)%2)+(act[k] if a*b else k)
        T[4*a+i][4*b+j][target]=B[i][j][k]
    return T


def model_tensor(rid):
    if rid=='R8_1_83':
        from extension_models import triality_m0
        return triality_m0()
    if rid=='R8_1_12':
        from verify_r8_1_12_orbifold import model_tensor as cyclic_orbifold
        return cyclic_orbifold()
    if rid=='R8_1_53':
        from verify_r8_1_53_orbifold import model_tensor as orbifold
        return orbifold()
    from extension_models import psu_flip,q8_equivariant,ty9,ty_v4_s3
    if rid=='R8_2_154':return ty_v4_s3(1)
    if rid=='R8_2_611':return ty_v4_s3(0)
    if rid=='R8_1_11':return psu_flip(True,1)
    if rid=='R8_1_14':return psu_flip(False,1)
    if rid=='R8_1_25':return psu_flip(False,0)
    if rid=='R8_1_42':return psu_flip(True,0)
    if rid=='R8_1_23':return q8_equivariant()
    if rid=='R8_1_34':return ty9('C9')
    if rid=='R8_1_35':return ty9('C3xC3')
    if rid=='R8_1_7':return central_square_root()
    if rid=='R8_1_6':return bosonic_c4()
    if rid=='R8_1_3':
        from twisted_group_theoretical_c2 import construct
        return construct()[0]
    if rid=='R8_1_15':return quadratic('C4',1)
    if rid=='R8_1_69':return quadratic('V4',1)
    if rid=='R8_2_39':return quadratic('C4',2)
    if rid=='R8_2_484':return quadratic('V4',2)
    if rid=='R8_1_19':return fib_swap()
    if rid=='R8_1_22':return ty_diagonal()
    if rid=='R8_1_30':return ty6_equivariant()
    raise ValueError(rid)


def components(R):
    n=len(R);du=[next(j for j in range(n) if R[i][j][0]) for i in range(n)]
    A={0}
    for i in range(n):A.update(k for k,v in enumerate(R[i][du[i]]) if v)
    while True:
        B=A|{k for i,j in product(A,repeat=2) for k,v in enumerate(R[i][j]) if v}
        if B==A:break
        A=B
    cs=[];todo=set(range(n))
    while todo:
        i=min(todo);C={k for a in A for k,v in enumerate(R[a][i]) if v}
        require(C<=todo);cs.append(sorted(C));todo-=C
    degrees={a:i for i,C in enumerate(cs) for a in C}
    G=[]
    for C in cs:
        row=[]
        for D in cs:
            support={degrees[k] for a,b in product(C,D) for k,v in enumerate(R[a][b]) if v}
            require(len(support)==1);row.append(support.pop())
        G.append(row)
    require(all(G[0][i]==G[i][0]==i for i in range(len(cs))))
    require(all(0 in G[i] for i in range(len(cs))))
    return sorted(A),cs,G


def is_pointed(R,A):
    return all(sum(R[a][b])==1 and R[a][b].index(1) in A for a,b in product(A,repeat=2))


@lru_cache(None)
def orthogonal_counts():
    # O(F3^2,xy): four matrices, all with square one.
    q3=lambda v:v[0]*v[1]%3
    o3=[]
    for a,b,c,d in product(range(3),repeat=4):
        if (a*d-b*c)%3==0:continue
        if all(q3(((a*x+b*y)%3,(c*x+d*y)%3))==q3((x,y)) for x,y in product(range(3),repeat=2)):
            o3.append((a,b,c,d))
            require(((a*a+b*c)%3,(a*b+b*d)%3,(c*a+d*c)%3,(c*b+d*d)%3)==(1,0,0,1))
    require(len(o3)==4)
    # O(F2^4, x1*y1+x2*y2): direct enumeration of linear maps.
    q2=lambda v:((v&1)*((v>>2)&1)+((v>>1)&1)*((v>>3)&1))%2
    count=0
    for cols in product(range(1,16),repeat=4):
        images=[]
        for v in range(16):
            z=0
            for j in range(4):
                if v>>j&1:z^=cols[j]
            images.append(z)
        if len(set(images))==16 and all(q2(images[v])==q2(v) for v in range(16)):count+=1
    require(count==72)
    return (4,count)


def certificate(R):
    A,cs,G=components(R)
    if len(A)==3 and is_pointed(R,A) and sorted(map(len,cs))==[1,1,3,3]:
        g=next((i for i,C in enumerate(cs) if len(C)==1 and G[i][i]!=0),None)
        if g is not None:
            square=G[g][g];require(len(cs[square])==3)
            a=next(x for x in A if x);s=cs[square][0]
            ai=next(x for x in A if R[a][x][0]);si=next(x for x in range(8) if R[s][x][0])
            sa=R[s][a].index(1);conj=R[sa][si].index(1)
            if conj==ai and a!=ai:
                orthogonal_counts()
                return {'kind':'graded_brauer_picard','case':'C3_C4_inversion','neutral_basis':A,
                        'components':cs,'component_group_table':G,'degree_one_component':g,
                        'inverting_object':s,'neutral_generator':a,
                        'criterion':'ENO, Fusion categories and homotopy theory, Corollary 1.2 and Theorem 1.3; rank-one module lemma'}
    if len(A)==4 and is_pointed(R,A) and sorted(map(len,cs))==[1,1,1,1,4]:
        involutions=sum(R[a][a][0] for a in A)
        require(involutions in (2,4))
        orthogonal_counts()
        return {'kind':'graded_brauer_picard','case':'C5_rank_one','neutral_group':'C4' if involutions==2 else 'C2xC2',
                'neutral_basis':A,'components':cs,'component_group_table':G,
                'criterion':'ENO, Fusion categories and homotopy theory, Corollary 1.2 and Theorem 1.3; rank-one module lemma'}
    if len(A)==3 and any(len(C)==1 for C in cs[1:]):
        inv=[a for a in A if sum(R[a][a])==1 and R[a][a][0]]
        if len(inv)==2:
            g=next(a for a in inv if a);x=next(a for a in A if a not in inv)
            v=[int(k in A) for k in range(8)]
            if R[g][g][0]==1 and R[g][x][x]==R[x][g][x]==1 and R[x][x]==v:
                return {'kind':'graded_fiber_functor','case':'rank3_dimension6_rank_one_component','neutral_basis':A,
                        'components':cs,'component_group_table':G,
                        'criterion':'ENO graded components are invertible; semisimple Hopf algebra dimension-six classification; rank-one module reconstruction'}
    return None


def verify_certificate(R,c):
    if c['kind']=='solvable_equivariantization':
        from solvable_equivariantization import verify_certificate as verify_solvable
        verify_solvable(R,c)
    else:
        require(certificate(R)==c,'graded obstruction mismatch')
