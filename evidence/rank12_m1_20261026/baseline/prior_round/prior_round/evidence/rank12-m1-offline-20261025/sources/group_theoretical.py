"""Untwisted group-theoretical fusion rings by equivariant-bundle convolution.

The finite group and subgroup are explicit. No catalogue label is input.
Character routines cover the small stabilizers used in this release.
"""
import itertools,math
import sympy as s
from exact import require

def permutation_group(degree,even=False):
    G=[p for p in itertools.permutations(range(degree)) if not even or sum(p[i]>p[j] for i in range(degree) for j in range(i+1,degree))%2==0]
    ix={p:i for i,p in enumerate(G)}
    M=[[ix[tuple(p[q[i]] for i in range(degree))] for q in G] for p in G]
    return G,M

def subgroup(M,gens):
    H={0};last=set()
    while last!=H:
        last=set(H);H|={M[x][g] for x in H for g in gens}
    return sorted(H)

def powers(M,x):
    a=0;out=[]
    while a not in out:out.append(a);a=M[a][x]
    require(a==0,'bad group element order');return out

def real_characters(M,H,K):
    one=K.one;zero=K.zero
    if len(H)==1:return [{0:one}]
    # Every real one-dimensional character is explicitly enumerated.
    out=[]
    for signs in itertools.product((-1,1),repeat=len(H)-1):
        d=dict(zip(H,(1,)+signs))
        if all(d[M[a][b]]==d[a]*d[b] for a in H for b in H):out.append({a:K(d[a]) for a in H})
    out.sort(key=lambda d:tuple(-int(d[x].to_list()[0]) for x in H))
    if len(H)==2 or len(out)==len(H):return out
    if len(H)==6:
        require(len(out)==2,'expected S3 stabilizer')
        out.append({a:K(2 if a==0 else 0 if len(powers(M,a))==2 else -1) for a in H})
    elif len(H)==10:
        require(len(out)==2,'expected D10 stabilizer');r=next(a for a in H if len(powers(M,a))==5);rr=powers(M,r);root=K.unit
        for l in (1,2):
            d={a:zero for a in H};d[0]=K(2)
            for j in range(1,5):d[rr[j]]=(root-K.one)/K(2) if (j*l)%5 in (1,4) else (-root-K.one)/K(2)
            out.append(d)
    elif len(H)==8:
        require(len(out)==4,'expected nonabelian order-eight stabilizer')
        z=next(a for a in H if a!=0 and all(M[a][b]==M[b][a] for b in H))
        out.append({a:K(2 if a==0 else -2 if a==z else 0) for a in H})
    else:raise ValueError('unsupported stabilizer order '+str(len(H)))
    for i,a in enumerate(out):
        for j,b in enumerate(out):require(sum((a[x]*b[x] for x in H),zero)==K(len(H)*int(i==j)),'character orthogonality')
    require(sum(int(c[0].to_list()[0])**2 for c in out)==len(H),'characters incomplete')
    return out

def fusion(M,H):
    n=len(M);H=sorted(H);require(H[0]==0,'identity index must be zero')
    inv=[next(j for j in range(n) if M[i][j]==0) for i in range(n)];hs=set(H)
    K=s.QQ.alg_field_from_poly(s.Poly(s.Symbol('t')**2-5,s.Symbol('t')),alias='sqrt5');zero=K.zero
    objects=[];covered=set()
    for z in range(n):
        if z in covered:continue
        orbit={M[M[u][z]][inv[v]]:(u,v) for u in H for v in H};covered|=set(orbit)
        stab=[a for a in H if M[M[inv[z]][a]][z] in hs]
        for chi in real_characters(M,stab,K):objects.append((z,stab,chi,orbit))
    cosets=[];covered=set()
    for x in range(n):
        if x not in covered:cosets.append(x);covered|={M[x][h] for h in H}
    cache={}
    def val(i,x,a,b):
        key=i,x,a,b
        if key in cache:return cache[key]
        z,stab,chi,orb=objects[i]
        if x not in orb or M[a][x]!=M[x][b]:result=zero
        else:
            u,v=orb[x];result=chi[M[M[inv[u]][a]][u]]
        cache[key]=result;return result
    rank=len(objects);R=[[[0]*rank for _ in range(rank)] for _ in range(rank)]
    for k,(z,stab,chi,orb) in enumerate(objects):
        for i,j in itertools.product(range(rank),repeat=2):
            result=zero
            for a in stab:
                b=M[M[inv[z]][a]][z];trace=zero
                for x in cosets:
                    h=M[M[inv[x]][a]][x]
                    if h in hs:trace+=val(i,x,a,h)*val(j,M[inv[x]][z],h,b)
                result+=chi[a]*trace
            result/=K(len(stab));co=result.to_list()
            require(len(co)<=1 and (not co or co[0].denominator==1 and co[0]>=0),'invalid fusion coefficient')
            R[i][j][k]=int(co[0]) if co else 0
    require(all(R[0][i][j]==R[i][0][j]==int(i==j) for i in range(rank) for j in range(rank)),'wrong tensor unit')
    return R

def examples():
    G,M=permutation_group(4,True);a=G.index((1,0,3,2));H=subgroup(M,[a])
    yield 'C(A4,C2)',fusion(M,H),{'group':'A4','permutation_degree':4,'even':True,'subgroup_generators':[G[a]]}
    G,M=permutation_group(5,True);r=G.index((1,2,3,4,0));h=G.index((0,4,3,2,1));H=subgroup(M,[r,h])
    yield 'C(A5,D10)',fusion(M,H),{'group':'A5','permutation_degree':5,'even':True,'subgroup_generators':[G[r],G[h]]}
    r=G.index((1,2,0,3,4));h=G.index((1,0,2,4,3));H=subgroup(M,[r,h])
    yield 'C(A5,S3)',fusion(M,H),{'group':'A5','permutation_degree':5,'even':True,'subgroup_generators':[G[r],G[h]]}

if __name__=='__main__':
    import json,time
    from pathlib import Path
    from prepare import key as canonical_key
    P=Path(__file__).resolve().parents[1];rows=json.load(open(P/'data/census.json'));index={canonical_key(r['N']):r['id'] for r in rows};out=[]
    for name,R,construction in examples():
        print(name,'rank',len(R),'mult',max(x for A in R for row in A for x in row),'match',index.get(canonical_key(R)),flush=True)
        out.append({'name':name,'N':R,'construction':construction,'id':index.get(canonical_key(R))})
    (P/'data/group_theoretical_models.json').write_text(json.dumps(out,separators=(',',':')))
