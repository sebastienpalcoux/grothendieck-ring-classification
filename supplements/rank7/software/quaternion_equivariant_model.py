"""Unitary Vec(Q8)^S3 model from the strict signed-axis permutation action."""
import hashlib
import itertools
import json
from functools import lru_cache
from exact import require


def parity(p):
    return sum(p[i]>p[j] for i in range(3) for j in range(i+1,3))%2


def mul(a,b):
    s,x=a;t,y=b
    if x==0:return s^t,y
    if y==0:return s^t,x
    if x==y:return s^t^1,0
    return s^t^int((x,y)not in ((1,2),(2,3),(3,1))),6-x-y


def act(p,a):
    s,x=a
    return a if x==0 else (s^parity(p),p[x-1]+1)


@lru_cache(None)
def model_tensor():
    group=list(itertools.permutations(range(3)));Q=list(itertools.product(range(2),range(4)))
    for a,b,c in itertools.product(Q,repeat=3):
        require(mul(mul(a,b),c)==mul(a,mul(b,c)),'quaternion associativity')
    for p,a,b in itertools.product(group,Q,Q):
        require(act(p,mul(a,b))==mul(act(p,a),act(p,b)),'action automorphism')
    for p,q,a in itertools.product(group,group,Q):
        require(act(tuple(p[q[i]] for i in range(3)),a)==act(p,act(q,a)), 'action composition')
    orbit=[a for a in Q if a[1]!=0]
    require(set(act(p,(0,1))for p in group)==set(orbit),'free noncentral orbit')
    require(all(act(p,(s,0))==(s,0) for p in group for s in range(2)),'central fixed objects')
    def character(a,p):
        return (1,(-1)**parity(p),sum(p[i]==i for i in range(3))-1)[a]
    dims=[1,1,2];N=[[[0]*7 for _ in range(7)] for _ in range(7)]
    for i,j in itertools.product(range(7),repeat=2):
        if i<6 and j<6:
            z,a=divmod(i,3);w,b=divmod(j,3)
            for c in range(3):
                value=sum(character(a,p)*character(b,p)*character(c,p) for p in group)
                require(value%6==0,'S3 character product')
                N[i][j][3*(z^w)+c]=value//6
        elif i==j==6:
            for z in range(2):
                pairs=[(a,b) for a,b in itertools.product(orbit,repeat=2) if mul(a,b)==(z,0)]
                traces=[sum(act(p,a)==a and act(p,b)==b for a,b in pairs) for p in group]
                require(sorted(traces)==[0,0,0,0,0,6],'central pair representation is not regular')
                for c in range(3):
                    value=sum(tr*character(c,p) for tr,p in zip(traces,group))
                    require(value%6==0,'central character multiplicity')
                    N[i][j][3*z+c]=value//6
            counts=[sum(mul(a,b)==c for a,b in itertools.product(orbit,repeat=2))for c in orbit]
            require(counts==[4]*6,'noncentral product multiplicity')
            N[i][j][6]=4
        else:
            a=j if i==6 else i
            N[i][j][6]=dims[a%3]
    return N


def models():
    return [('Vec(Q8)^S3',model_tensor(),
             'The unitary equivariantization Vec(Q8)^S3 for the strict action e_a -> sign(p)*e_p(a) on the three quaternion axes. Fixed central grades carry the three ordinary S3 irreducibles; the six noncentral grades form one free orbit.',
             'Explicit quaternion group and signed-axis S3 action; orbit/stabilizer equivariantization theory of Burciu--Natale, Fusion rules of equivariantizations of fusion categories. Full construction and proof in the manuscript.',
             'https://arxiv.org/abs/1206.6625')]


def verify_target(rows):
    T=next(r['tensor']for r in rows if r['id']=='R7_4_2');N=model_tensor();p=[0,5,4,1,2,3,6]
    require(all(N[i][j][k]==T[p[i]][p[j]][p[k]] for i,j,k in itertools.product(range(7),repeat=3)),
            'quaternion model census match')
    return {'passed':True,'id':'R7_4_2','model_to_census':p,
            'tensor_sha256':hashlib.sha256(json.dumps(T,separators=(',',':')).encode()).hexdigest(),
            'group_associativity_checks':512,'action_automorphism_checks':384,
            'action_composition_checks':288,'coefficients_checked':343,
            'central_pair_characters':'two regular S3 representations',
            'noncentral_pair_counts':[4]*6}


if __name__=='__main__':
    from pathlib import Path
    root=Path(__file__).resolve().parents[1]
    receipt=verify_target(json.loads((root/'output/rank7_ledger.json').read_text()))
    (root/'output/quaternion_equivariant_model_verification.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))
