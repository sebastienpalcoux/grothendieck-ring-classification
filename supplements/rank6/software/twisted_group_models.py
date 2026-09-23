"""Exact three-double-coset construction for a twisted S4 category.
All phases are exponents modulo four. No numerical character calculation occurs.
"""
import itertools,math,json
from pathlib import Path
from functools import lru_cache
from exact import require
from oriented_signed import validate_general

def matmul(a,b):
    return ((a[0]*b[0]+a[1]*b[2])%3,(a[0]*b[1]+a[1]*b[3])%3,(a[2]*b[0]+a[3]*b[2])%3,(a[2]*b[1]+a[3]*b[3])%3)
def normalize(a):
    c=next(x for x in a if x);return tuple(c*x%3 for x in a),int(c==2)

@lru_cache(maxsize=1)
def twisted_s4():
    I=(1,0,0,1)
    mats=sorted({normalize(a)[0] for a in itertools.product(range(3),repeat=4) if (a[0]*a[3]-a[1]*a[2])%3})
    mats.remove(I);mats.insert(0,I);ix={a:i for i,a in enumerate(mats)};n=len(mats);require(n==24,'PGL2F3 order')
    G=[[ix[normalize(matmul(a,b))[0]] for b in mats] for a in mats]
    beta=[[normalize(matmul(a,b))[1] for b in mats] for a in mats]
    alpha=[int((a[0]*a[3]-a[1]*a[2])%3==2) for a in mats]
    inv=[G[a].index(0) for a in range(n)]
    lines=[(1,0),(0,1),(1,1),(1,2)]
    def act(a,v):
        w=((a[0]*v[0]+a[1]*v[1])%3,(a[2]*v[0]+a[3]*v[1])%3);c=next(x for x in w if x)
        return lines.index(tuple(c*x%3 for x in w))
    perms=[tuple(act(a,v) for v in lines) for a in mats]
    require(len(set(perms))==24 and perms[0]==tuple(range(4)),'faithful S4 action')
    for a,b in itertools.product(range(n),repeat=2):
        require(perms[G[a][b]]==tuple(perms[a][perms[b][i]] for i in range(4)),'action multiplication')
        require(alpha[G[a][b]]==(alpha[a]^alpha[b]),'determinant not a character')
    for a,b,c in itertools.product(range(n),repeat=3):
        require(G[G[a][b]][c]==G[a][G[b][c]],'group associativity')
        require((beta[b][c]+beta[a][G[b][c]]-beta[G[a][b]][c]-beta[a][b])%2==0,'central-extension cocycle')
    h1=perms.index((1,0,2,3));h2=perms.index((0,1,3,2));H=sorted([0,h1,h2,G[h1][h2]])
    require(len(set(H))==4 and all(G[h][h]==0 for h in H),'H is not V4')
    pairs=list(itertools.product(H[1:],repeat=2));pindex={v:i for i,v in enumerate(pairs)}
    qvalues=[0,2,0,3,0,1,1,0,1]
    q=lambda a,b:0 if a==0 or b==0 else qvalues[pindex[a,b]]
    w=lambda a,b,c:2*alpha[a]*beta[b][c]
    for a,b,c in itertools.product(H,repeat=3):
        require((q(b,c)+q(a,G[b][c])-q(G[a][b],c)-q(a,b)-w(a,b,c))%4==0,'invalid boundary cochain')
    # This exhaustive 4-tuple check is redundant with the cup-product proof,
    # but guards both the implementation and its convention.
    for a,b,c,d in itertools.product(range(n),repeat=4):
        require((w(b,c,d)-w(G[a][b],c,d)+w(a,G[b][c],d)-w(a,b,G[c][d])+w(a,b,c))%4==0,'3-cocycle failure')
    seen=set();cosets=[]
    for g in range(n):
        if g in seen:continue
        dc={G[G[a][g]][b] for a,b in itertools.product(H,repeat=2)};seen|=dc
        conj=lambda a:G[G[inv[g]][a]][g]
        J=[a for a in H if conj(a) in H]
        def factor(a,b):
            v=conj(inv[b]);u=conj(inv[a])
            return (q(a,b)+q(v,u)+w(a,b,g)+w(a,G[b][g],v)-w(G[G[a][b]][g],v,u))%4
        f=[[factor(a,b) for b in J] for a in J]
        for a,b,c in itertools.product(J,repeat=3):
            require((factor(b,c)+factor(a,G[b][c])-factor(G[a][b],c)-factor(a,b))%4==0,'stabilizer factor not a 2-cocycle')
        rad=[a for a in J if all(factor(a,b)==factor(b,a) for b in J)]
        size=math.isqrt(len(J)//len(rad));require(size*size*len(rad)==len(J),'non-square projective degree')
        cosets.append({'representative':g,'double_coset':sorted(dc),'stabilizer':J,'factor_mod4':f,'radical':rad,'projective_degree':size,'number_of_simples':len(rad),'simple_dimension':len(H)//len(J)*size})
    require(len(seen)==n and len(cosets)==3,'not three double cosets')
    ident=next(c for c in cosets if c['representative']==0)
    normal=next(c for c in cosets if c['representative'] and len(c['double_coset'])==4)
    outer=next(c for c in cosets if len(c['double_coset'])==16)
    require(ident['number_of_simples']==4 and normal['number_of_simples']==outer['number_of_simples']==1,'projective spectrum hypothesis')
    require(normal['simple_dimension']==2 and outer['simple_dimension']==4,'dimension hypothesis')
    N=set(ident['double_coset'])|set(normal['double_coset'])
    require(all(G[a][b] in N for a,b in itertools.product(N,repeat=2)),'normalizer subgroup')
    require(all(G[a][b] in H for a,b in itertools.product(normal['double_coset'],repeat=2)),'normalizer quotient is not C2')
    require(all(G[a][b] in outer['double_coset'] and G[b][a] in outer['double_coset'] for a in N for b in outer['double_coset']),'outer support not stable')
    chars=[]
    for bits in itertools.product(range(2),repeat=3):
        chi=dict(zip(H,[0]+list(bits)))
        if all(chi[G[a][b]]==(chi[a]^chi[b]) for a,b in itertools.product(H,repeat=2)):chars.append(tuple(chi[a] for a in H))
    require(len(chars)==4,'wrong character group');cindex={v:i for i,v in enumerate(chars)}
    R=[[[0]*6 for _ in range(6)] for _ in range(6)]
    for i,j in itertools.product(range(4),repeat=2):R[i][j][cindex[tuple(a^b for a,b in zip(chars[i],chars[j]))]]=1
    for i in range(4):
        R[i][4][4]=R[4][i][4]=R[i][5][5]=R[5][i][5]=1;R[4][4][i]=R[5][5][i]=1
    R[4][5][5]=R[5][4][5]=2;R[5][5][4]=R[5][5][5]=2
    validate_general(R)
    aux={'group':'PGL(2,F3) = S4','matrices':mats,'permutations':perms,'H':H,'boundary_pairs':pairs,'boundary_exponents_mod4':qvalues,'double_cosets':cosets,'dimensions':[1,1,1,1,2,4],'omega_4tuple_checks':24**4}
    return R,aux

if __name__=='__main__':
    from prepare import key
    P=Path(__file__).resolve().parents[1];R,aux=twisted_s4();hits=[r['id'] for r in json.load(open(P/'data/census.json')) if key(r['N'])==key(R)]
    require(len(hits)==1,'ambiguous model');print('EXACT TWISTED MODEL',hits,flush=True)
    (P/'data/twisted_s4_certificate.json').write_text(json.dumps(aux,separators=(',',':'))+'\n')
