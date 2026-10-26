"""Finite reconstruction of all dimension-24 quotients; no census completeness used."""
from pathlib import Path
import itertools,json,hashlib
import numpy as np
import ring_utils as common
OUT=Path(__file__).resolve().parent
INPUTS=json.loads((OUT/"quotient_inputs.json").read_text())
DATA={r:v["tensor"]for r,v in INPUTS["records"].items()}
IDS=INPUTS["source_ids"]
import collections

def require(v,m):
    if not v:raise ValueError(m)

def compose(p,q):return tuple(p[q[i]]for i in range(len(p)))
def inv(p):return tuple(p.index(i)for i in range(len(p)))
def groups8():
    yield 'C8',[[(a+b)%8 for b in range(8)]for a in range(8)]
    yield 'C4xC2',[[((a%4+b%4)%4)+4*((a//4+b//4)%2)for b in range(8)]for a in range(8)]
    yield 'V8',[[a^b for b in range(8)]for a in range(8)]
    for name,eps in [('D8',0),('Q8',2)]:
        yield name,[[((a%4+(-1)**(a//4)*(b%4)+eps*(a//4)*(b//4))%4)+4*((a//4+b//4)%2)for b in range(8)]for a in range(8)]

def autos(G):
    for q in itertools.permutations(range(1,8)):
        p=(0,)+q
        if any(p[p[i]]!=i for i in range(8))or sum(p[i]==i for i in range(8))!=4:continue
        if all(p[G[a][b]]==G[p[a]][p[b]]for a,b in itertools.product(range(8),repeat=2)):yield p

def orbits(p):
    seen=set();out=[]
    for i in range(len(p)):
        if i not in seen:
            o=sorted({i,p[i]});out.append(o);seen.update(o)
    return out

def quotient(N,p):
    O=orbits(p)
    Q=[[[sum(N[a[0]][b[0]][k]for k in c)for c in O]for b in O]for a in O]
    require(all([sum(N[i][j][k]for k in c)for c in O]==Q[a][b] for a,A in enumerate(O)for b,B in enumerate(O)for i in A for j in B),'quotient well-defined')
    return O,Q

def generators(G):
    gens=[];seen={0}
    while len(seen)<8:
        gens.append(next(i for i in range(8)if i not in seen))
        while True:
            new=seen|{G[a][g]for a in seen for g in gens}
            if new==seen:break
            seen=new
    return gens

def actions(G):
    gens=generators(G);perms=list(itertools.permutations(range(4)));I=tuple(range(4));out=[]
    for images in itertools.product(perms,repeat=len(gens)):
        ps={0:I};queue=[0];ok=True
        while queue and ok:
            a=queue.pop()
            for g,u in zip(gens,images):
                b=G[a][g];v=compose(ps[a],u)
                if b in ps:
                    if ps[b]!=v:ok=False;break
                else:ps[b]=v;queue.append(b)
        if ok:out.append(tuple(ps[i]for i in range(8)))
    return out

def pointed_matches(G,p,Q,ds):
    O=orbits(p); inds=[i for i,d in enumerate(ds)if d==1];pairs=[i for i,d in enumerate(ds)if d==2]
    fixed=[i for i,o in enumerate(O)if len(o)==1];free=[i for i,o in enumerate(O)if len(o)==2]
    for a,b in itertools.product(itertools.permutations([i for i in inds if i!=0]),itertools.permutations(pairs)):
        f={0:0};f.update(zip(fixed[1:],a));f.update(zip(free,b))
        good=True
        for i,A in enumerate(O):
            for j,B in enumerate(O):
                v=collections.Counter(G[x][y]for x in A for y in B)
                if any(Q[f[i]][f[j]][f[k]]!=v[C[0]]for k,C in enumerate(O)):good=False;break
            if not good:break
        if good:yield O,[f[i]for i in range(6)]

def invariant_constraints(N,O,Q):
    return all(sum(N[i,j,C[0]]for i in A for j in B)==Q[a][b][c]for a,A in enumerate(O)for b,B in enumerate(O)for c,C in enumerate(O))

def reconstruct(Q,ds):
    require(np.array_equal(np.asarray(Q),np.asarray(Q).transpose(1,0,2)),"source invariant ring commutative")
    noninv=[i for i,d in enumerate(ds)if d==4]
    require(all(Q[a][b][c]<=1 for a,b,c in itertools.product(noninv,repeat=3)),"binary noninvertible coefficients forced")
    results=[];stats=collections.Counter()
    for name,G in groups8():
        acts=actions(G);stats[name+'_actions']=len(acts)
        for pg in autos(G):
            p=tuple(pg)+(9,8,11,10);px=(1,0,3,2)
            for OG,f in pointed_matches(G,pg,Q,ds):
                O=OG+[[8,9],[10,11]];f=f+[i for i,d in enumerate(ds)if d==4]
                T=np.asarray(Q)[np.ix_(f,f,f)]
                stats['pointed_matches']+=1
                # Both sides are representations (right action represented with inverses).
                candidates=[]
                for A in acts:
                    if not all(compose(px,A[g])==compose(A[pg[g]],px)for g in range(8)):continue
                    good=True
                    for a,gg in enumerate(OG):
                        for t,XX in enumerate(O[6:]):
                            v=collections.Counter(A[g][x-8]+8 for g in gg for x in XX)
                            if any(v[C[0]]!=T[a,6+t,c]for c,C in enumerate(O)):good=False;break
                        if not good:break
                    if good:candidates.append(A)
                stats['action_candidates']+=len(candidates)
                gi=[next(b for b in range(8)if G[a][b]==0)for a in range(8)]
                for L,B in itertools.product(candidates,repeat=2):
                    R=tuple(B[gi[g]]for g in range(8))
                    if not all(compose(L[a],R[b])==compose(R[b],L[a])for a,b in itertools.product(range(8),repeat=2)):continue
                    N=np.zeros((12,12,12),dtype=np.int64)
                    for a,b in itertools.product(range(8),repeat=2):N[a,b,G[a][b]]=1
                    for g,x in itertools.product(range(8),range(4)):N[g,8+x,8+L[g][x]]=N[8+x,g,8+R[g][x]]=1
                    if any(sum(N[i,j,C[0]]for i in A for j in B)!=T[a,b,c]for a,A in enumerate(O)for b,B in enumerate(O)for c,C in enumerate(O)if a<6 or b<6):continue
                    for dx in itertools.permutations(range(4)):
                        if any(dx[dx[x]]!=x for x in range(4)):continue
                        d=gi+[8+x for x in dx]
                        if any(d[p[i]]!=p[d[i]]for i in range(12)):continue
                        for i,j,g in itertools.product(range(8,12),range(8,12),range(8)):N[i,j,g]=N[g,d[j],i]
                        if any(N[i,j,k]!=N[d[i],k,j] or N[i,j,k]!=N[k,d[j],i] or N[i,j,k]!=N[d[j],d[i],d[k]]for i,j,k in itertools.product(range(12),repeat=3)if min(i,j,k)<8):continue
                        if any(sum(N[i,j,C[0]]for i in A for j in B)!=T[a,b,c]for a,A in enumerate(O)for b,B in enumerate(O)for c,C in enumerate(O)if c<6):continue
                        stats['module_dual_candidates']+=1
                        # Equalities on noninvertible coefficients generated by Frobenius,
                        # duality, involution, and all associativity constraints with an invertible.
                        triples=list(itertools.product(range(8,12),repeat=3));idx={t:i for i,t in enumerate(triples)};parent=list(range(64))
                        def find(a):
                            while parent[a]!=a:parent[a]=parent[parent[a]];a=parent[a]
                            return a
                        def union(t,u):
                            a,b=find(idx[t]),find(idx[u]);parent[a]=b
                        for i,j,k in triples:
                            for u in [(d[i],k,j),(k,d[j],i),(d[j],d[i],d[k]),(p[i],p[j],p[k])]:union((i,j,k),u)
                            for g in range(8):
                                union((8+L[g][i-8],j,8+L[g][k-8]),(i,j,k))
                                union((i,8+R[g][j-8],8+R[g][k-8]),(i,j,k))
                                union((8+R[g][i-8],j,k),(i,8+L[g][j-8],k))
                        classes=collections.defaultdict(list)
                        for t in triples:classes[find(idx[t])].append(t)
                        cls=list(classes.values());stats['max_binary_variables']=max(stats['max_binary_variables'],len(cls))
                        for bits in itertools.product(range(2),repeat=len(cls)):
                            for v,ts in zip(bits,cls):
                                for t in ts:N[t]=v
                            if not all(sum(N[i,j,k]*([1]*8+[2]*4)[k]for k in range(12))==4 for i,j in itertools.product(range(8,12),repeat=2)):continue
                            if not invariant_constraints(N,O,T):continue
                            if not np.array_equal(np.einsum('ijm,mkl->ijkl',N,N),np.einsum('jkm,iml->ijkl',N,N)):continue
                            common.validate(N.tolist());stats['valid_tables']+=1; independent_bind(N)
                            if any(common.based_iso(N.tolist(),z['tensor'])is not None for z in results):continue
                            results.append(dict(group=name,tensor=N.tolist(),automorphism=p,orbits=O,source_orbit_map=f))
        print(name,dict(stats),flush=True)
    return results,dict(stats)

def source_branches():
    rows=[]
    for rid in IDS:
        rec=INPUTS['records'][rid];R=rec['tensor'];ds=rec['dimensions'];N=np.asarray(R)
        require(hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()==rec['sha256'],'source hash')
        common.validate(R)
        require(sorted(ds)==[1]*8+[2]*2+[4]*2,'source dimensions')
        require(all(sum(R[i][j][k]*ds[k]for k in range(12))==ds[i]*ds[j]for i,j in itertools.product(range(12),repeat=2)),'dimension character')
        require(N.max()==1,'multiplicity1')
        dual=common.dual(R);adj={0}|{k for i in range(12)for k in range(12)if R[i][dual[i]][k]}
        while True:
            nxt=adj|{k for i,j in itertools.product(adj,repeat=2)for k in range(12)if R[i][j][k]}
            if nxt==adj:break
            adj=nxt
        require(len(adj)==12,'trivial universal grading')
        require(all(common.based_iso(R,DATA['R12_1_'+str(j)])is None for j in [30,417,414,531]),'not a conditional GT model')
        branches=[]
        for b in range(1,12):
            if ds[b]!=1 or R[b][b][0]!=1 or any(R[b][i]!=R[i][b]for i in range(12)):continue
            p=[R[b][i].index(1)for i in range(12)]
            require(all(p[p[i]]==i for i in range(12)),'involution permutation')
            pattern=collections.Counter(ds[i]for i in range(12)if p[i]==i)
            O,Q=quotient(R,p);qd=[ds[o[0]]for o in O]
            if pattern=={2:2,4:2}:kind='rank12_m1_dimension24'
            elif pattern=={2:2}:kind='near_group_G8_m2'
            elif pattern=={4:2}:kind='rank9_dimension24_type_1_4_2_5'
            elif not pattern:
                kind='free_rank6_quotient';common.validate(Q)
                require(sorted(qd)==[1]*4+[2,4],'free quotient type')
                y=qd.index(4)
                require(Q[y][y]==[1 if d==1 else 2 for d in qd],'free quotient adjoint generator')
            else:raise ValueError('unhandled central involution pattern')
            branches.append(dict(involution=b,fixed_dimensions=dict(pattern),case=kind,source_orbits=O,quotient_tensor=Q,dimensions=qd))
        require(branches,'at least one possible central boson')
        rows.append(dict(id=rid,sha256=rec['sha256'],branches=branches))
    return rows

def main():
    rows=source_branches();classes=[]
    for row in rows:
        for b in row['branches']:
            if b['case']!='rank12_m1_dimension24':continue
            Q=b['quotient_tensor'];d=b['dimensions']
            found=None
            for j,c in enumerate(classes):
                iso=common.based_iso(Q,c['tensor'])
                if iso is not None:
                    require(all(d[i]==c['dimensions'][iso[i]]for i in range(len(d))),'dimension-preserving invariant isomorphism')
                    found=(j,iso);break
            if found is None:
                found=(len(classes),list(range(len(Q))));classes.append(dict(tensor=Q,dimensions=d,first_source=row['id']))
            b['reconstruction_class'],b['class_basis_map']=found
    print('source quotient classes',len(classes),flush=True)
    out=[]
    for c in classes:
        found,stats=reconstruct(c['tensor'],c['dimensions'])
        for r in found:
            r['known_match']=None
            for rid in ['R12_1_351','R12_1_513']:
                iso=common.based_iso(r['tensor'],DATA[rid])
                if iso is not None:r['known_match']=rid;r['known_basis_map']=iso;break
            require(r['known_match'] is not None,'every reconstruction is a proved quotient type')
        require(found,'nonempty reconstruction class')
        out.append(dict(source=c,reconstructions=found,statistics=stats))
        print('CLASS DONE',c['first_source'],[(r['group'],r['known_match'])for r in found],flush=True)
    for row in rows:
        for b in row['branches']:
            if b['case']=='rank12_m1_dimension24':b['target_ids']=sorted({r['known_match']for r in out[b['reconstruction_class']]['reconstructions']})
    result=dict(status='PASS',source_binding=rows,reconstruction_classes=out)
    (OUT/'quotient_reconstruction.json').write_text(json.dumps(result,indent=2)+'\n')
if __name__=='__main__':main()
