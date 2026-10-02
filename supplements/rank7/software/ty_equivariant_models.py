"""Two unitary TY(C3) equivariantizations, with finite action-coherence replay.

See papers/ty_equivariant_models.md for the categorical construction.
All arithmetic below is integral; powers of i are represented modulo four.
The TY automorphism action is the input theorem GNN, Proposition 4.8.
"""
import hashlib
import itertools
import json
from functools import lru_cache
from exact import require

U=((0,0,0,0),(0,0,0,3),(0,3,2,1),(0,1,0,0))
GNN_URL='https://msp.org/ant/2009/3-8/ant-v3-n8-p05-s.pdf'


def w(a,b,c):
    return (a%4)*(((b%4)+(c%4))//4)


@lru_cache(None)
def verify_coherence():
    require(all(U[0][a]==U[a][0]==0 for a in range(4)), 'tensorator unit')
    for a,b,c,d in itertools.product(range(4),repeat=4):
        require((w(b,c,d)-w(a+b,c,d)+w(a,b+c,d)-w(a,b,c+d)+w(a,b,c))%4==0,
                'pointed cocycle equation')
    for a,b,c in itertools.product(range(4),repeat=3):
        require((U[b][c]-U[(a+b)%4][c]+U[a][(b+c)%4]-U[a][b]
                 -w(a,b,c)+w(-a,-b,-c))%4==0, 'tensorator equation')
    for a,b in itertools.product(range(4),repeat=2):
        require((U[a][b]+U[-a%4][-b%4])%4==0, 'action square')
    require(all((a*b-(-a%3)*(-b%3))%3==0
                for a,b in itertools.product(range(3),repeat=2)), 'TY bicharacter preservation')
    require(U[2][2]==2, 'fixed degree-two lift must square to the sign object')
    require(U[1][1]==U[3][3]==0 and (U[1][3]+U[3][1])%4==0,
            'odd-channel swaps must square to identity')
    return {'passed':True,'cocycle_equations':256,'tensorator_equations':64,
            'action_square_equations':16,'bicharacter_equations':9,
            'tensorator_exponents':[list(v) for v in U],
            'eta_exponents':[0,0,0,0], 'fixed_degree_two_square':'sign object'}


def orbit_tensor(twisted):
    """Reconstruct equivariant Hom invariants from the eight base simples.

    TY label 3 denotes m. All base fusion multiplicities are one. On a
    Hom basis F permutes the three simple labels (input,input,output).
    Thus only triples of fixed labels contribute to its trace; these have
    pointed degrees 0 or 2, so their tensorator scalars are signs.
    The invariant multiplicity is (dimension + trace)/2.
    """
    mod=4 if twisted else 2
    ev=lambda e:2*e if twisted else e
    odd=(1,3) if twisted else (0,1)
    base=[(a,ev(e)) for e in range(2) for a in range(3)]+[(3,b) for b in odd]
    def action(x):
        a,b=x
        return ((-a)%3 if a!=3 else 3,(-b)%4 if twisted else (b+int(a==3))%2)
    def product(x,y):
        a,b=x;c,d=y;degree=(b+d)%mod
        if a==c==3:return [(v,degree) for v in range(3)]
        return [(3 if 3 in (a,c) else (a+c)%3,degree)]
    require(all(action(action(x))==x for x in base),'base action square')
    for x,y in itertools.product(base,repeat=2):
        require(sorted(action(z)for z in product(x,y))==sorted(product(action(x),action(y))),
                'action preserves base fusion channels')
    # Basis (1,h,t,ht,P0,P1,Z), with equivariant signs on singleton orbits.
    labels=[([(0,ev(0))],1), ([(0,ev(0))],-1),
            ([(0,ev(1))],1), ([(0,ev(1))],-1),
            ([(1,ev(0)),(2,ev(0))],1), ([(1,ev(1)),(2,ev(1))],1),
            ([(3,b)for b in odd],1)]
    tensor=[[[0]*7 for _ in range(7)] for _ in range(7)]
    for i,j,k in itertools.product(range(7),repeat=3):
        A,ea=labels[i];B,eb=labels[j];C,ec=labels[k];dimension=trace=0
        for a,b,c in itertools.product(A,B,C):
            if c not in product(a,b):continue
            dimension+=1
            if all(action(v)==v for v in (a,b,c)):
                exponent=U[a[1]][b[1]] if twisted else 0
                require(exponent%2==0,'fixed-channel scalar not a sign')
                trace+=ea*eb*ec*((-1)**(exponent//2))
        require((dimension+trace)%2==0 and dimension>=abs(trace),'invalid invariant multiplicity')
        tensor[i][j][k]=(dimension+trace)//2
    return tensor


@lru_cache(None)
def model_tensor(twisted=False):
    verify_coherence()
    N=[[[0]*7 for _ in range(7)] for _ in range(7)]
    for i,j in itertools.product(range(7),repeat=2):
        if i<4 and j<4:
            if twisted:
                powers=[0,2,1,3]
                k=powers.index((powers[i]+powers[j])%4)
            else:k=2*((i//2+j//2)%2)+(i%2+j%2)%2
            N[i][j][k]=1
        elif i<4 or j<4:
            g,x=(i,j) if i<4 else (j,i)
            N[i][j][6 if x==6 else 4+(g//2+x-4)%2]=1
        elif i<6 and j<6:
            e=(i+j-8)%2
            N[i][j][2*e]=N[i][j][2*e+1]=N[i][j][4+e]=1
        elif i==j==6:N[i][j]=[1,1,1,1,2,2,0]
        else:N[i][j][6]=2
    require(N==orbit_tensor(twisted),'fusion rules differ from equivariant Hom invariants')
    require(all(sum(N[i][j][a]*N[a][k][l] for a in range(7))==
                sum(N[j][k][a]*N[i][a][l] for a in range(7))
                for i,j,k,l in itertools.product(range(7),repeat=4)),'model associativity')
    return N


def models():
    reference=('Tambara--Yamagami, J. Algebra 209 (1998), 692-707; '
               'Gelaki--Naidu--Nikshych, Centers of graded fusion categories, '
               'Section 4A and Proposition 4.8; explicit coherent actions in papers/ty_equivariant_models.md.')
    return [
        ('TY(C3)-parity-equivariantization',model_tensor(False),
         '(TY(C3,chi,+1/sqrt(3)) Deligne Vec(C2))^C2, with chi(a,b)=exp(2*pi*i*a*b/3) and F(X,e)=(I(X),e+|X|); canonical tensorators and identity square coherence.',
         reference,GNN_URL),
        ('TY(C3)-twisted-C4-equivariantization',model_tensor(True),
         'The C2 equivariantization of the diagonal subcategory of TY(C3,chi,+1/sqrt(3)) Deligne Vec(C4,omega1); simultaneous inversion, explicit scalar tensorator U, and identity square coherence. All phases, cocycle equations and equivariant Hom invariants are replayed in software/ty_equivariant_models.py.',
         reference,GNN_URL)]


def verify_targets(rows):
    by={r['id']:r for r in rows};result=[]
    specs=[('R7_2_1',False,[0,5,1,2,4,3,6],
            'bb405c73678267340ddd95a9d44e735e5272c3f080997a6bd0974b90e54e639f'),
           ('R7_2_195',True,[0,6,1,2,5,3,4],
            'd9ba378c7d570f70991119f50d2bd41d552df4bb81955714b71b0ed3963a3f5f')]
    for rid,twisted,p,sha in specs:
        S=model_tensor(twisted);T=by[rid]['tensor']
        require(hashlib.sha256(json.dumps(T,separators=(',',':')).encode()).hexdigest()==sha,
                'target census tensor changed')
        require(all(S[i][j][k]==T[p[i]][p[j]][p[k]]
                    for i,j,k in itertools.product(range(7),repeat=3)),'model-to-census mismatch')
        result.append({'id':rid,'model_to_census':p,'tensor_sha256':sha,
                       'coefficients_checked':343,'orbit_invariant_coefficients_checked':343,
                       'associativity_equations':2401})
    return {'passed':True,'coherence':verify_coherence(),'models':result}


if __name__=='__main__':
    from pathlib import Path
    root=Path(__file__).resolve().parents[1]
    receipt=verify_targets(json.loads((root/'output/rank7_ledger.json').read_text()))
    target=root/'output/ty_equivariant_models_verification.json'
    target.write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))
