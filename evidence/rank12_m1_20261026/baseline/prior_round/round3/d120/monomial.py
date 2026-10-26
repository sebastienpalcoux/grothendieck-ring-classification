"""Explicit H4-bimodules with scalar or irreducible 2-dimensional fibers.

All tensor coefficients come from actual finite balanced quotients and exact
projective-character projection. No representation catalogue is assumed.
"""
import itertools
from scalar_base import objects,require
MOD=20
def rational(co):
    co=list(co)
    for j in range(19,7,-1):
        a=co[j];co[j]=0
        for off,c in [(2,1),(4,-1),(6,1),(8,-1)]:co[j-off]+=c*a
    require(not any(co[1:8]),"exact cyclotomic rationality")
    return co[0]


def construct(G,H,w,psi=None,expected_rank=12):
    if psi is None:psi=lambda a,b:0
    objs,info=objects(G,H,lambda a,b,c:w(a,b,c)//5,lambda a,b:psi(a,b)//5,allow_matrix=True)
    if objs is None:return None,info
    rank=len(objs)
    if rank!=expected_rank:return None,info
    n=len(G);inv=[next(j for j in range(n)if G[i][j]==0)for i in range(n)]
    def dim(A):return A.get('dimension',1)
    def rp(A,x,h,t):return A['R'][x,h,t]if dim(A)>1 else A['R'][x,h]
    def rt(A,h,t):return(t+A['right_permutation'][h])%2 if dim(A)>1 else 0
    def basis(A):return[(x,t)for x in A['D']for t in range(dim(A))]
    # Check original actions before tensor products.
    for A in objs:
        for x,a,b,t in itertools.product(A['D'],H,H,range(dim(A))):
            require(rt(A,b,rt(A,a,t))==rt(A,G[a][b],t),'original right permutation action')
            require((rp(A,x,a,t)+rp(A,G[x][a],b,rt(A,a,t))-rp(A,x,G[a][b],t)-w(x,a,b)-psi(a,b))%MOD==0,'original right module action')
            require((rp(A,G[a][x],b,t)-rp(A,x,b,t)-A['L'][a,G[x][b]]-w(a,x,b)+A['L'][a,x])%MOD==0,'original bimodule compatibility')
    # The projective characters in each double coset are complete and orthogonal.
    for D in {tuple(A['D'])for A in objs}:
        O=[A for A in objs if tuple(A['D'])==D];stab=O[0]['stab'];z=O[0]['z']
        require(sum(dim(A)**2 for A in O)==len(stab),'complete projective degrees')
        chars=[]
        for A in O:
            row={}
            for h in stab:
                q=G[G[inv[z]][h]][z];row[h]=[(rp(A,z,q,t)-A['L'][h,z])%MOD for t in range(dim(A))if rt(A,q,t)==t]
            chars.append(row)
        for i,a in enumerate(chars):
            for j,b in enumerate(chars):
                co=[0]*MOD
                for h in stab:
                    for v,u in itertools.product(a[h],b[h]):co[(u-v)%MOD]+=1
                require(rational(co)==len(stab)*int(i==j),'projective character orthogonality')
    N=[[[0]*rank for _ in range(rank)]for _ in range(rank)]
    for i,A in enumerate(objs):
        for j,B in enumerate(objs):
            pairs=set(itertools.product(basis(A),basis(B)));maps={};remaining=set(pairs)
            while remaining:
                rep=min(remaining);maps[rep]=(rep,0);queue=[rep]
                for P in queue:
                    (x,t),(y,u)=P;root,phase=maps[P]
                    for h in H:
                        q=G[inv[h]][y];Q=((G[x][h],rt(A,h,t)),(q,u));delta=(w(x,h,q)+B['L'][h,q]-rp(A,x,h,t))%MOD;v=(phase+delta)%MOD
                        if Q in maps:require(maps[Q]==(rep,v),'consistent balanced quotient')
                        else:maps[Q]=(rep,v);queue.append(Q)
                require(len(queue)==len(H),'free balanced action');remaining-=set(queue)
            reps=sorted({v[0]for v in maps.values()});left={};right={}
            for h in H:
                left[h]={};right[h]={}
                for P in reps:
                    (x,t),(y,u)=P;Q,a=maps[((G[h][x],t),(y,u))];left[h][P]=(Q,(A['L'][h,x]-w(h,x,y)+a)%MOD)
                    Q,a=maps[((x,t),(G[y][h],rt(B,h,u)))];right[h][P]=(Q,(w(x,y,h)+rp(B,y,h,u)+a)%MOD)
                for P in pairs:
                    (x,t),(y,u)=P;rep,a=maps[P]
                    for target,phase,ops in [(((G[h][x],t),(y,u)),A['L'][h,x]-w(h,x,y),left[h]),(((x,t),(G[y][h],rt(B,h,u))),w(x,y,h)+rp(B,y,h,u),right[h])]:
                        r,b=maps[target];r0,c=ops[rep];require(r==r0 and(phase+b-a-c)%MOD==0,'all quotient actions descend')
            for a,b,P in itertools.product(H,H,reps):
                grade=G[P[0][0]][P[1][0]]
                Q,v=left[b][P];T,u=left[a][Q];T0,c=left[G[a][b]][P]
                require(T==T0 and(v+u+w(a,b,grade)-psi(a,b)-c)%MOD==0,'quotient left module identity')
                Q,v=right[a][P];T,u=right[b][Q];T0,c=right[G[a][b]][P]
                require(T==T0 and(v+u-w(grade,a,b)-psi(a,b)-c)%MOD==0,'quotient right module identity')
                Q,v=left[a][P];T,u=right[b][Q];Q0,c=right[b][P];T0,d=left[a][Q0]
                require(T==T0 and(v+u-c-d-w(a,grade,b))%MOD==0,'quotient bimodule compatibility')
            inverses={h:{Q:(P,(-a)%MOD)for P,(Q,a)in left[h].items()}for h in H}
            for k,C in enumerate(objs):
                z=C['z'];fiber=[P for P in reps if G[P[0][0]][P[1][0]]==z];co=[0]*MOD
                for h in C['stab']:
                    q=G[G[inv[z]][h]][z]
                    phases=[(rp(C,z,q,t)-C['L'][h,z])%MOD for t in range(dim(C))if rt(C,q,t)==t]
                    for chi in phases:
                        for P in fiber:
                            Q,a=right[q][P];T,b=inverses[h][Q]
                            if T==P:co[(a+b-chi)%MOD]+=1
                num=rational(co);den=len(C['stab']);require(num>=0 and num%den==0,'nonnegative integral tensor coefficient');N[i][j][k]=num//den
                if N[i][j][k]>1:return None,dict(rank=rank,not_multiplicity_one=True)
    units=[u for u in range(rank)if all(N[u][i][j]==N[i][u][j]==int(i==j)for i,j in itertools.product(range(rank),repeat=2))];require(len(units)==1,'unique subgroup algebra unit')
    p=[units[0]]+[i for i in range(rank)if i!=units[0]];N=[[[N[a][b][c]for c in p]for b in p]for a in p];objs=[objs[a]for a in p]
    return N,dict(rank=rank,objects=[dict(representative=A['z'],support=A['D'],fiber_dimension=dim(A),right_permutation=A.get('right_permutation'),left_phases=[[h,x,v]for(h,x),v in A['L'].items()],right_phases=[list(k)+[v]for k,v in A['R'].items()])for A in objs])
