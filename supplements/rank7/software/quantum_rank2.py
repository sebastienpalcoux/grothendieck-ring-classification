"""Exact principal WZW fusion rules for A2 and G2, from Weyl alternants.
No census data, floating point, or fitted fusion coefficients are used.
Weights use the short fundamental weight first for G2.
"""
from functools import lru_cache
import itertools
import sympy as s
from exact import require, field, t

def weyl_group(cartan):
    r=len(cartan);identity=s.eye(r);gens=[]
    for i in range(r):
        reflection=identity.copy()
        for j in range(r):reflection[j,i]-=cartan[i][j]
        gens.append(reflection)
    seen={tuple(identity)};queue=[identity]
    for w in queue:
        for a in gens:
            v=w*a
            if tuple(v) not in seen:seen.add(tuple(v));queue.append(v)
    return [(w,int(w.det())) for w in queue]

def row_reduce(a,K):
    a=[row.copy() for row in a];r=0;piv=[]
    for j in range(len(a[0])):
        at=next((i for i in range(r,len(a)) if a[i][j]),None)
        if at is None:continue
        a[at],a[r]=a[r],a[at];v=a[r][j];a[r]=[x/v for x in a[r]]
        for i in range(len(a)):
            if i!=r and a[i][j]:
                v=a[i][j];a[i]=[x-v*y for x,y in zip(a[i],a[r])]
        piv.append(j);r+=1
        if r==len(a):break
    return a,piv

def inverse(a,K):
    n=len(a);rr,piv=row_reduce([row+[K(int(i==j)) for j in range(n)] for i,row in enumerate(a)],K)
    require(piv==list(range(n)),'singular character submatrix')
    return [row[n:] for row in rr]

@lru_cache(None)
def principal(kind,level,adjoint=False):
    require(type(level) is int and level>0,'positive integral WZW level required')
    if kind=='G2':
        A=s.Matrix([[2,-1],[-3,2]]);B=s.Matrix([[s.Rational(2,3),-1],[-1,2]]);h=4
        weights=[(a,b) for b in range(level//2+1) for a in range(level-2*b+1)]
        require(not adjoint,'G2 adjoint selection not required')
    elif kind=='A2':
        A=s.Matrix([[2,-1],[-1,2]]);B=A;h=3
        weights=[(a,b) for b in range(level+1) for a in range(level-b+1)]
    else:raise ValueError('Supported root systems: A2, G2')
    basis=[w for w in weights if not adjoint or (w[0]-w[1])%3==0]
    G=A.inv()*B*A.inv().T;W=weyl_group(A.tolist());n=len(basis)
    conductor=int(s.ilcm(*(v.q for v in G)))*(level+h)
    K=field(s.Poly(s.cyclotomic_poly(conductor,t),t));z=K([1,0]);powers=[z**i for i in range(conductor)]
    def alternant(l,m):
        v=s.Matrix([x+1 for x in l]);u=s.Matrix([x+1 for x in m]);out=K.zero
        for w,sign in W:
            e=-(w*v).dot(G*u)*conductor/(level+h)
            require(e.q==1,'nonintegral cyclotomic exponent');out+=sign*powers[int(e)%conductor]
        return out
    den=[alternant((0,0),m) for m in weights]
    require(all(den),'Weyl denominator vanishes')
    C=[[alternant(l,m)/d for m,d in zip(weights,den)] for l in basis]
    _,piv=row_reduce(C,K);require(len(piv)==n,'characters fail to separate the fusion algebra')
    square=[[row[j] for j in piv] for row in C];inv=inverse(square,K);R=[]
    for i in range(n):
        mat=[]
        for j in range(n):
            row=[]
            for k in range(n):
                v=sum((square[i][a]*square[j][a]*inv[a][k] for a in range(n)),K.zero)
                co=v.to_list()
                require(len(co)<=1 and (not co or co[0].denominator==1),'nonintegral Weyl-character product')
                row.append(int(co[0]) if co else 0)
            require(min(row)>=0,'negative fusion coefficient')
            for a in range(len(weights)):
                require(C[i][a]*C[j][a]==sum((row[k]*C[k][a] for k in range(n)),K.zero),'character equation failed')
            mat.append(row)
        R.append(mat)
    return R,basis,conductor

if __name__=='__main__':
    import json,time
    from pathlib import Path
    from prepare import key
    P=Path(__file__).resolve().parents[1];start=time.monotonic()
    for kind,lev,ad in [('G2',3,False),('A2',6,True)]:
        R,b,c=principal(kind,lev,ad)
        print(kind,lev,'rank',len(b),'conductor',c,'basis',b,'seconds',time.monotonic()-start,flush=True)
        if len(R)==6:
            print('matches',[r['id'] for r in json.load(open(P/'data/census.json')) if key(r['N'])==key(R)],flush=True)
        (P/'research'/f'weyl_{kind}_{lev}.json').write_text(json.dumps({'N':R,'basis':b,'conductor':c})+'\n')
