"""Actual scalar-fiber subgroup bimodules and balanced quotients, phases Z/8.

Positive constructions only. Unsupported nonscalar stabilizers or phase ranges
yield no conclusion, never an exclusion.
"""
import itertools
import numpy as np

MOD=8
def require(c,m):
    if not c:raise ValueError(m)

def solve(A,b,mod=MOD,first=False):
    A=np.array(A,dtype=np.int64);b=np.array(b,dtype=np.int64)
    n=A.shape[1];E=np.column_stack((A,b))%mod;r=0;piv=[]
    for c in range(n):
        hit=next((i for i in range(r,len(E))if E[i,c]%2),None)
        if hit is None:continue
        E[[r,hit]]=E[[hit,r]];E[r]=(E[r]*pow(int(E[r,c]),-1,mod))%mod
        for i in range(len(E)):
            if i!=r and E[i,c]:E[i]=(E[i]-E[i,c]*E[r])%mod
        piv.append(c);r+=1
    free=[c for c in range(n)if c not in piv];sub=E[r:][:,free];rhs=E[r:,-1]
    if any(rhs%2):return[]
    if mod==2:
        if any(rhs):return[]
        bottom=[(0,)*len(free)]
    else:bottom=solve(sub//2,rhs//2,mod//2,first=first)
    ans=[]
    for v in bottom:
        for bits in itertools.product(range(2),repeat=len(free)):
            x=[0]*n
            for c,a,bit in zip(free,v,bits):x[c]=(int(a)+mod//2*bit)%mod
            for i,c in enumerate(piv):x[c]=int((E[i,-1]-sum(E[i,j]*x[j]for j in free))%mod)
            require(np.array_equal((A@np.array(x))%mod,b%mod),'linear phase solution')
            ans.append(x)
            if first:return ans
    return ans

def objects(G,H,w,psi,allow_matrix=False):
    n=len(G);inv=[next(j for j in range(n)if G[i][j]==0)for i in range(n)]
    require(all((psi(b,c)+psi(a,G[b][c])-psi(G[a][b],c)-psi(a,b)+w(a,b,c))%MOD==0 for a,b,c in itertools.product(H,repeat=3)),'all subgroup algebra cocycle equations')
    hs=set(H);covered=set();out=[]
    for z in range(n):
        if z in covered:continue
        D=sorted({G[G[a][z]][b]for a,b in itertools.product(H,repeat=2)});covered.update(D)
        reps={};cosets={};L={};remaining=set(D)
        while remaining:
            t=min(remaining)
            for b in H:reps[G[b][t]]=(b,t);cosets[G[b][t]]=t
            remaining-={G[b][t]for b in H}
        for a,x in itertools.product(H,D):
            b,t=reps[x];L[a,x]=(psi(a,b)-w(a,b,t))%MOD
        require(all((L[b,x]+L[a,G[b][x]]+w(a,b,x)-psi(a,b)-L[G[a][b],x])%MOD==0 for a,b,x in itertools.product(H,H,D)),'all left module equations')
        variables=[(x,h)for x in D for h in H if h];ix={v:i for i,v in enumerate(variables)};A=[];B=[]
        def equation(terms,rhs):
            row=[0]*len(variables)
            for x,h,c in terms:
                if h:row[ix[x,h]]+=c
            A.append(row);B.append(rhs%MOD)
        for x,a,b in itertools.product(D,H,H):
            equation([(x,a,1),(G[x][a],b,1),(x,G[a][b],-1)],w(x,a,b)+psi(a,b))
        for a,x,b in itertools.product(H,D,H):
            equation([(G[a][x],b,1),(x,b,-1)],L[a,G[x][b]]+w(a,x,b)-L[a,x])
        # Remove precisely the remaining constant-on-left-orbit basis gauges.
        seen={cosets[z]};queue=[cosets[z]]
        for x in queue:
            for h in H:
                y=cosets[G[x][h]]
                if y not in seen:
                    seen.add(y);queue.append(y);equation([(x,h,1)],0)
        require(seen==set(cosets.values()),'connected double coset right action')
        solutions=solve(A,B)
        stab=[a for a in H if G[G[inv[z]][a]][z]in hs]
        if len(solutions)!=len(stab):
            if allow_matrix and not solutions and len(stab)==len(H)==len(D)==4 and all(G[h][h]==0 for h in H):
                good=None
                for signs in itertools.product(range(2),repeat=3):
                    ch=dict(zip(H,(0,)+signs))
                    if not any(signs)or any(ch[G[a][b]]!=(ch[a]+ch[b])%2 for a,b in itertools.product(H,repeat=2)):continue
                    var=[(x,h,t)for x in D for h in H if h for t in range(2)];ix2={v:i for i,v in enumerate(var)};A2=[];B2=[]
                    def eq2(terms,rhs):
                        row=[0]*len(var)
                        for x,h,t,c in terms:
                            if h:row[ix2[x,h,t]]+=c
                        A2.append(row);B2.append(rhs%MOD)
                    for x,a,b,t in itertools.product(D,H,H,range(2)):
                        eq2([(x,a,t,1),(G[x][a],b,(t+ch[a])%2,1),(x,G[a][b],t,-1)],w(x,a,b)+psi(a,b))
                    for a,x,b,t in itertools.product(H,D,H,range(2)):
                        eq2([(G[a][x],b,t,1),(x,b,t,-1)],L[a,G[x][b]]+w(a,x,b)-L[a,x])
                    flip=next(h for h in H if ch[h]);eq2([(z,flip,0,1)],0)
                    sol=solve(A2,B2,first=True)
                    if sol:
                        R={v:a for v,a in zip(var,sol[0])};R.update({(x,0,t):0 for x,t in itertools.product(D,range(2))})
                        good=dict(z=z,D=D,L=L,R=R,stab=stab,dimension=2,right_permutation=ch);break
                if good is None:return None,dict(unsupported='no explicit matrix projective model',representative=z)
                out.append(good);continue
            return None,dict(unsupported='nonscalar stabilizer or phase bound',representative=z,solutions=len(solutions),stabilizer=len(stab))
        for vals in sorted(solutions):
            R={v:val for v,val in zip(variables,vals)};R.update({(x,0):0 for x in D})
            out.append(dict(z=z,D=D,L=L,R=R,stab=stab))
    return out,dict(rank=len(out))

def construct(G,H,w,expected_rank=12,psi=None):
    if psi is None:psi=lambda a,b:0
    objs,info=objects(G,H,w,psi)
    if objs is None:return None,info
    rank=len(objs)
    if rank!=expected_rank:return None,info
    n=len(G);inv=[next(j for j in range(n)if G[i][j]==0)for i in range(n)];N=[[[0]*rank for _ in range(rank)]for _ in range(rank)]
    for i,A in enumerate(objs):
        for j,B in enumerate(objs):
            pairs=set(itertools.product(A['D'],B['D']));maps={};remaining=set(pairs)
            while remaining:
                rep=min(remaining);maps[rep]=(rep,0);queue=[rep]
                for x,y in queue:
                    root,phase=maps[x,y]
                    for h in H:
                        Q=(G[x][h],G[inv[h]][y]);delta=(w(x,h,Q[1])+B['L'][h,Q[1]]-A['R'][x,h])%MOD;v=(phase+delta)%MOD
                        if Q in maps:require(maps[Q]==(rep,v),'consistent balanced quotient')
                        else:maps[Q]=(rep,v);queue.append(Q)
                require(len(queue)==len(H),'free balanced action');remaining-=set(queue)
            reps=sorted({v[0]for v in maps.values()});left={};right={}
            for h in H:
                left[h]={};right[h]={}
                for P in reps:
                    x,y=P;Q,a=maps[G[h][x],y];left[h][P]=(Q,(A['L'][h,x]-w(h,x,y)+a)%MOD)
                    Q,a=maps[x,G[y][h]];right[h][P]=(Q,(w(x,y,h)+B['R'][y,h]+a)%MOD)
                for x,y in pairs:
                    rep,a=maps[x,y]
                    for target,phase,ops in [((G[h][x],y),A['L'][h,x]-w(h,x,y),left[h]),((x,G[y][h]),w(x,y,h)+B['R'][y,h],right[h])]:
                        r,b=maps[target];r0,c=ops[rep];require(r==r0 and(phase+b-a-c)%MOD==0,'all balanced actions descend')
            for a,b,P in itertools.product(H,H,reps):
                grade=G[P[0]][P[1]]
                Q,v=left[b][P];T,u=left[a][Q];T0,c=left[G[a][b]][P]
                require(T==T0 and(v+u+w(a,b,grade)-psi(a,b)-c)%MOD==0,'quotient left module equation')
                Q,v=right[a][P];T,u=right[b][Q];T0,c=right[G[a][b]][P]
                require(T==T0 and(v+u-w(grade,a,b)-psi(a,b)-c)%MOD==0,'quotient right module equation')
                Q,v=left[a][P];T,u=right[b][Q];Q0,c=right[b][P];T0,d=left[a][Q0]
                require(T==T0 and(v+u-c-d-w(a,grade,b))%MOD==0,'quotient bimodule compatibility')
            inverses={h:{Q:(P,(-a)%MOD)for P,(Q,a)in left[h].items()}for h in H}
            for k,C in enumerate(objs):
                z=C['z'];fiber=[P for P in reps if G[P[0]][P[1]]==z];co=[0]*MOD
                for h in C['stab']:
                    q=G[G[inv[z]][h]][z];chi=(C['R'][z,q]-C['L'][h,z])%MOD
                    for P in fiber:
                        Q,a=right[q][P];T,b=inverses[h][Q]
                        if T==P:co[(a+b-chi)%MOD]+=1
                require(co[2]==co[6] and co[1]-co[3]-co[5]+co[7]==0 and co[1]+co[3]-co[5]-co[7]==0,'rational exact stabilizer projection')
                numerator=co[0]-co[4];denom=len(C['stab'])
                require(numerator>=0 and numerator%denom==0,'nonnegative integral fusion coefficient')
                N[i][j][k]=numerator//denom
                if N[i][j][k]>1:return None,dict(rank=rank,not_multiplicity_one=True)
    units=[u for u in range(rank)if all(N[u][i][j]==N[i][u][j]==int(i==j)for i,j in itertools.product(range(rank),repeat=2))]
    require(len(units)==1,'unique subgroup algebra tensor unit')
    perm=[units[0]]+[i for i in range(rank)if i!=units[0]]
    N=[[[N[a][b][c]for c in perm]for b in perm]for a in perm];objs=[objs[a]for a in perm]
    return N,dict(rank=rank,objects=[dict(z=o['z'],support=o['D'],left_phases=[[h,x,v]for(h,x),v in o['L'].items()],right_phases=[[x,h,v]for(x,h),v in o['R'].items()])for o in objs])
