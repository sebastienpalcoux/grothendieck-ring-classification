"""Opposite-pair arithmetic at conductor 16, in the split residue algebra modulo 17."""
from itertools import product

P=17
UNITS=((15,8,15,8),(2,13,16,15),(13,16,15,2))
SEEDS=((14,11,7,10),(12,3,6,12))

def normalize(v):
    return tuple(i*pow(v[0],-1,P)%P for i in v)

def multiply(x,y):
    return tuple(a*b%P for a,b in zip(x,y))

def unit_orbit():
    return {normalize(tuple(u**a*v**b*w**c%P for u,v,w in zip(*UNITS)))
            for a,b,c in product(range(8),repeat=3)}

def check(H,K,M,V):
    rows=unit_orbit()
    for seed in SEEDS:
        zs={normalize(multiply(seed,u)) for u in rows}; counts=[0]*5
        for z in zs:
            T=sum(z)%P; jz=z[2:]+z[:2]
            if (sum(b*b*pow(a,-1,P) for a,b in zip(z,jz))-V*T)%P:continue
            counts[0]+=1
            assert T  # Excludes x reducing to zero in the first moment.
            for u in rows:
                xu=sum(a*b for a,b in zip(z,u))%P
                if not xu:continue
                scalar=T*pow(xu,-1,P)%P
                x=tuple(scalar*v%P for v in u); jx=x[2:]+x[:2]
                counts[1]+=1
                if (sum(t*v for t,v in zip(z,jx))-H*T)%P:continue
                counts[2]+=1
                if (sum(t*u*v for t,u,v in zip(z,x,jx))-K*T)%P:continue
                counts[3]+=1
                if (sum(t*v*v for t,v in zip(z,jx))-M*T)%P:continue
                counts[4]+=1
        print((H,K,M,V),seed, len(rows), len(zs), counts)
        assert not counts[4]

if __name__=='__main__':
    check(3,1,11,5)
    check(7,3,53,17)
