"""Exhaustive rank-nine D24 reconstruction from the actual D48 orbit tensors."""
from quotient_reconstruct import *
import time

def groups4():
    yield 'C4',[[(a+b)%4 for b in range(4)]for a in range(4)]
    yield 'V4',[[a^b for b in range(4)]for a in range(4)]

def actions5(G):
    gens=[1] if G[1][1]!=0 else [1,2]
    perms=list(itertools.permutations(range(5)));I=tuple(range(5));out=[]
    for images in itertools.product(perms,repeat=len(gens)):
        ps={0:I};queue=[0];ok=True
        while queue and ok:
            a=queue.pop()
            for g,u in zip(gens,images):
                b=G[a][g];v=compose(ps[a],u)
                if b in ps:
                    if ps[b]!=v:ok=False;break
                else:ps[b]=v;queue.append(b)
        if ok:
            require(len(ps)==4,'generating set')
            out.append(tuple(ps[i]for i in range(4)))
    return out

def linear_solutions(A,b,upper):
    # Exact exhaustive bounded-integer recursion with interval propagation.
    m=len(upper);A=np.asarray(A,dtype=np.int64);b=np.asarray(b,dtype=np.int64)
    def dfs(values):
        values=values.copy()
        while True:
            changed=False
            for row,rhs in zip(A,b):
                residual=int(rhs)-sum(int(row[j])*v for j,v in enumerate(values)if v is not None)
                left=[j for j in range(m)if values[j]is None and row[j]]
                if residual<0 or residual>sum(int(row[j])*upper[j]for j in left):return
                if not left:
                    if residual:return
                elif residual==0:
                    for j in left:values[j]=0;changed=True
                elif residual==sum(int(row[j])*upper[j]for j in left):
                    for j in left:values[j]=upper[j];changed=True
                elif len(left)==1:
                    j=left[0]
                    if residual%int(row[j]):return
                    values[j]=residual//int(row[j]);changed=True
            if not changed:break
        left=[j for j in range(m)if values[j]is None]
        if not left:yield values;return
        j=max(left,key=lambda j:sum(A[:,j]!=0))
        for v in range(upper[j]+1):
            nxt=values.copy();nxt[j]=v;yield from dfs(nxt)
    yield from dfs([None]*m)

def reconstruct9(Q,ds):
    require(np.array_equal(np.asarray(Q),np.asarray(Q).transpose(1,0,2)),'invariant commutativity')
    require(sorted(ds)==[1]*4+[2]+[4]*2,'rank9 orbit dimensions')
    O=[[0],[1],[2],[3],[4],[5,6],[7,8]];p=(0,1,2,3,4,6,5,8,7);px=(0,2,1,4,3)
    results=[];stats=collections.Counter()
    for name,G in groups4():
        acts=actions5(G);stats[name+'_actions']=len(acts);gi=[next(b for b in range(4)if G[a][b]==0)for a in range(4)]
        unit=[i for i,d in enumerate(ds)if d==1];Tindex=ds.index(2);free=[i for i,d in enumerate(ds)if d==4]
        for order in itertools.permutations([i for i in unit if i!=0]):
            f=[0]+list(order)+[Tindex]+free;T=np.asarray(Q)[np.ix_(f,f,f)]
            if any(T[a,b,c]!=int(G[a][b]==c)for a,b,c in itertools.product(range(4),repeat=3)):continue
            stats['pointed_matches']+=1;candidates=[]
            for A in acts:
                if any(compose(px,A[g])!=compose(A[g],px)for g in range(4)):continue
                if any(sum(A[g][x-4]+4==C[0]for x in B)!=T[g,b,c]for g in range(4)for b,B in enumerate(O)if b>=4 for c,C in enumerate(O)):continue
                candidates.append(A)
            stats['action_candidates']+=len(candidates)
            for L,B in itertools.product(candidates,repeat=2):
                R=tuple(B[gi[g]]for g in range(4))
                if any(compose(L[a],R[b])!=compose(R[b],L[a])for a,b in itertools.product(range(4),repeat=2)):continue
                N=np.zeros((9,9,9),dtype=np.int64)
                for a,b in itertools.product(range(4),repeat=2):N[a,b,G[a][b]]=1
                for g,x in itertools.product(range(4),range(5)):N[g,4+x,4+L[g][x]]=N[4+x,g,4+R[g][x]]=1
                if any(sum(N[i,j,C[0]]for i in A for j in B)!=T[a,b,c]for a,A in enumerate(O)for b,B in enumerate(O)for c,C in enumerate(O)if a<4 or b<4):continue
                for dx in itertools.permutations(range(5)):
                    if any(dx[dx[x]]!=x for x in range(5)):continue
                    d=gi+[4+x for x in dx]
                    if any(d[p[i]]!=p[d[i]]for i in range(9)):continue
                    for i,j,g in itertools.product(range(4,9),range(4,9),range(4)):N[i,j,g]=N[g,d[j],i]
                    if any(N[i,j,k]!=N[d[i],k,j] or N[i,j,k]!=N[k,d[j],i] or N[i,j,k]!=N[d[j],d[i],d[k]]for i,j,k in itertools.product(range(9),repeat=3)if min(i,j,k)<4):continue
                    if any(sum(N[i,j,C[0]]for i in A for j in B)!=T[a,b,c]for a,A in enumerate(O)for b,B in enumerate(O)for c,C in enumerate(O)if c<4):continue
                    stats['module_dual_candidates']+=1
                    triples=list(itertools.product(range(4,9),repeat=3));idx={t:i for i,t in enumerate(triples)};parent=list(range(125))
                    def find(a):
                        while parent[a]!=a:parent[a]=parent[parent[a]];a=parent[a]
                        return a
                    def union(t,u):
                        a,b=find(idx[t]),find(idx[u]);parent[a]=b
                    for i,j,k in triples:
                        for u in [(d[i],k,j),(k,d[j],i),(d[j],d[i],d[k]),(p[i],p[j],p[k])]:union((i,j,k),u)
                        for g in range(4):
                            union((4+L[g][i-4],j,4+L[g][k-4]),(i,j,k))
                            union((i,4+R[g][j-4],4+R[g][k-4]),(i,j,k))
                            union((4+R[g][i-4],j,k),(i,4+L[g][j-4],k))
                    classes=collections.defaultdict(list)
                    for t in triples:classes[find(idx[t])].append(t)
                    cls=list(classes.values());ci={t:j for j,ts in enumerate(cls)for t in ts};m=len(cls)
                    stats['max_variables']=max(stats['max_variables'],m)
                    A=[];bb=[]
                    for a,b,c in itertools.product(range(4,7),repeat=3):
                        row=[0]*m
                        for i,j in itertools.product(O[a],O[b]):row[ci[(i,j,O[c][0])]]+=1
                        A.append(row);bb.append(int(T[a,b,c]))
                    for i,j in itertools.product(range(4,9),repeat=2):
                        row=[0]*m
                        for k in range(4,9):row[ci[(i,j,k)]]+=2
                        A.append(row);bb.append(4-int(N[i,j,:4].sum()))
                    upper=[min(rhs//row[j]for row,rhs in zip(A,bb)if row[j])for j in range(m)]
                    for vals in linear_solutions(A,bb,upper):
                        stats['linear_solutions']+=1
                        for v,ts in zip(vals,cls):
                            for t in ts:N[t]=v
                        if not invariant_constraints(N,O,T):continue
                        if not np.array_equal(np.einsum('ijm,mkl->ijkl',N,N),np.einsum('jkm,iml->ijkl',N,N)):continue
                        common.validate(N.tolist());stats['valid_tables']+=1
                        if any(common.based_iso(N.tolist(),z['tensor'])is not None for z in results):continue
                        # Exact C3 grading with TY8 neutral must be exhibited, not presumed.
                        neutral=set(range(5));outside=list(range(5,9));gradings=[]
                        require(N[4,4,:4].tolist()==[1]*4 and not any(N[4,4,4:]),'TY neutral square')
                        for first in itertools.combinations(outside,2):
                            degree=[0]*5+[1 if i in first else 2 for i in outside]
                            if all(not N[i,j,k]or degree[k]==(degree[i]+degree[j])%3 for i,j,k in itertools.product(range(9),repeat=3)):gradings.append(degree)
                        # Preserve alternatives honestly; categorical closure is separate.
                        require(np.array_equal(N,N[np.ix_(p,p,p)]),'actual quotient action')
                        adj={0}|{k for i in range(9)for k in range(9)if N[i,d[i],k]}
                        while True:
                            nxt=adj|{k for i,j in itertools.product(adj,repeat=2)for k in range(9)if N[i,j,k]}
                            if nxt==adj:break
                            adj=nxt
                        require(len(adj)==9,'survivor has trivial universal grading')
                        central=[h for h in range(1,4)if N[h,h,0]==1 and np.array_equal(N[h],N[:,h,:])]
                        require(len(central)==1,'unique nontrivial central involution')
                        h=central[0]
                        require(p[h]==h,'outer action preserves unique boson')
                        require(all(N[h,i,i]==1 for i in range(4,9)),'boson fixes all five noninvertibles')
                        results.append(dict(group=name,tensor=N.tolist(),automorphism=p,source_orbit_map=f,TY_neutral=list(range(5)),C3_gradings=gradings,adjoint_closure=sorted(adj),unique_central_involution=h,pointed_deequivariantization_dimension=12))
        print(name,dict(stats),flush=True)
    return results,dict(stats)

def main():
    start=time.monotonic();rows=source_branches();classes=[];bindings=[]
    for row in rows:
        for b in row['branches']:
            if b['case']!='rank9_dimension24_type_1_4_2_5':continue
            Q=b['quotient_tensor'];ds=b['dimensions'];found=None
            for j,c in enumerate(classes):
                iso=common.based_iso(Q,c['tensor'])
                if iso is not None:
                    require(all(ds[i]==c['dimensions'][iso[i]]for i in range(7)),'orbit dimension preserving');found=(j,iso);break
            if found is None:found=(len(classes),list(range(7)));classes.append(dict(tensor=Q,dimensions=ds,first_source=row['id']))
            bindings.append(dict(id=row['id'],involution=b['involution'],source_hash=row['sha256'],reconstruction_class=found[0],class_basis_map=found[1]))
    print('rank9 orbit classes',len(classes),flush=True);out=[]
    for c in classes:
        found,stats=reconstruct9(c['tensor'],c['dimensions'])
        out.append(dict(source=c,reconstructions=found,statistics=stats));print('CLASS DONE',c['first_source'],len(found),flush=True)
    result=dict(status='PASS',source_binding=bindings,reconstruction_classes=out)
    (OUT/'rank9_reconstruction.json').write_text(json.dumps(result,indent=2)+'\n')
    print('DONE',time.monotonic()-start)
if __name__=='__main__':main()
