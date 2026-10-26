"""Independent actual graded-bimodule reconstruction of C(A5xC2,graph D10).

Unlike the root's character-convolution implementation, this constructs every
simple as an induced monomial graded H--H bimodule, every balanced tensor
quotient, and every stabilizer-character projection over Q(zeta_10).
"""
from pathlib import Path
from itertools import permutations,product
import hashlib,json,time
import numpy as np
from independent_audit import BASE,HERE,require

def candidate():
    perms=[p for p in permutations(range(5))if sum(p[i]>p[j]for i in range(5)for j in range(i+1,5))%2==0]
    E=list(product(perms,range(2)));ix={e:i for i,e in enumerate(E)}
    G=[[ix[(tuple(p[q[i]]for i in range(5)),(a+b)%2)]for q,b in E]for p,a in E]
    r=ix[((1,2,3,4,0),0)];s=ix[((0,4,3,2,1),1)]
    powers=[0]
    for _ in range(4):powers.append(G[powers[-1]][r])
    coord={G[a][s]:(j,1)for j,a in enumerate(powers)};coord.update({a:(j,0)for j,a in enumerate(powers)})
    H=sorted(coord);require(len(H)==10 and all(G[a][b]in H for a,b in product(H,repeat=2)),'actual graph D10 subgroup')
    require({E[h][1]for h in H}=={0,1},'graph not contained in A5x1')
    return G,H,coord

def plus(A,B):
    # Both monomial states are (target, exponent).
    target,e=A;target2,f=B[target];return target2,(e+f)%10

def objects(G,H,coord):
    inv=[next(j for j in range(len(G))if G[i][j]==0)for i in range(len(G))];S=set(H);covered=set();out=[]
    for g in range(len(G)):
        if g in covered:continue
        reps={}
        for a,b in product(H,repeat=2):reps.setdefault(G[G[a][g]][inv[b]],(a,b))
        D=sorted(reps);covered.update(D);K=[a for a in H if G[G[inv[g]][a]][g]in S]
        require(len(K)in(2,10),'only D10/C2 stabilizers')
        kinds=[('linear',0),('linear',1),('dihedral',1),('dihedral',2)]if len(K)==10 else[('cyclic',0),('cyclic',1)]
        for kind,j in kinds:
            dim=2 if kind=='dihedral'else 1
            def pi(h,t,kind=kind,j=j):
                if kind=='cyclic':return t,(5*j*int(h!=0))%10
                a,b=coord[h]
                if kind=='linear':return t,(5*j*b)%10
                q=t^b;return q,(2*j*a*(1 if q==0 else-1))%10
            states=list(product(D,range(dim)));L={};R={}
            for h in H:
                L[h]={};R[h]={}
                for x,t in states:
                    a,b=reps[x];y=G[h][x];ay,by=reps[y];k=G[G[inv[ay]][h]][a]
                    require(k in K,'left stabilizer');u,e=pi(k,t);L[h][x,t]=((y,u),e)
                    y=G[x][h];ay,by=reps[y];k=G[inv[ay]][a]
                    require(k in K,'right stabilizer');u,e=pi(k,t);R[h][x,t]=((y,u),e)
            for a,b,state in product(H,H,states):
                require(plus(L[b][state],L[a])==L[G[a][b]][state],'all induced left module equations')
                require(plus(R[a][state],R[b])==R[G[a][b]][state],'all induced right module equations')
                require(plus(L[a][state],R[b])==plus(R[b][state],L[a]),'all induced bimodule compatibility')
            out.append(dict(g=g,D=D,K=K,dim=dim,pi=pi,states=states,L=L,R=R))
    require(len(out)==12,'complete twelve simple bimodules')
    return out,inv

def constant(co):
    co=co[:]
    for k in range(9,3,-1):
        a=co[k]
        for j,b in enumerate((1,-1,1,-1,1)):co[k-4+j]-=a*b
    require(not any(co[1:]),'exact cyclotomic rationality')
    return co[0]

def construct(G,H,coord):
    O,inv=objects(G,H,coord);n=len(O);N=[[[0]*n for _ in range(n)]for _ in range(n)];balanced_count=0
    for i,A in enumerate(O):
        for j,B in enumerate(O):
            remaining=set(product(A['states'],B['states']));maps={}
            while remaining:
                root=min(remaining);maps[root]=(root,0);queue=[root]
                for P in queue:
                    first,second=P;_,phase=maps[P]
                    for h in H:
                        f,ea=A['R'][h][first];q,eb=B['L'][inv[h]][second];Q=(f,q);v=(phase-ea-eb)%10
                        if Q in maps:require(maps[Q]==(root,v),'consistent balanced quotient')
                        else:maps[Q]=(root,v);queue.append(Q)
                require(len(queue)==10,'free balanced H action');remaining.difference_update(queue)
            roots=sorted({r for r,e in maps.values()});balanced_count+=len(roots)
            L={};R={}
            for h in H:
                L[h]={};R[h]={}
                for P in roots:
                    first,second=P;q,e=A['L'][h][first];root,f=maps[q,second];L[h][P]=(root,(e+f)%10)
                    q,e=B['R'][h][second];root,f=maps[first,q];R[h][P]=(root,(e+f)%10)
            for k,C in enumerate(O):
                g=C['g'];fiber=[P for P in roots if G[P[0][0]][P[1][0]]==g];co=[0]*10
                for h in C['K']:
                    q=G[G[inv[g]][h]][g];char=[e for t in range(C['dim'])for u,e in [C['pi'](h,t)]if u==t]
                    for P in fiber:
                        Q,ea=R[q][P];T,eb=L[inv[h]][Q]
                        if T==P:
                            for e in char:co[(ea+eb+e)%10]+=1
                num=constant(co);den=len(C['K']);require(num>=0 and num%den==0,'nonnegative integral exact multiplicity')
                N[i][j][k]=num//den
    require(all(N[0][i][j]==N[i][0][j]==int(i==j)for i,j in product(range(n),repeat=2)),'actual algebra is tensor unit')
    return N,[len(A['D'])*A['dim']//len(H)for A in O],balanced_count

if __name__=='__main__':
    start=time.monotonic();G,H,coord=candidate()
    root=json.loads((HERE.parent/'root/group_graph_models.json').read_text())['models'][0]
    require(root['parameters']['group_table']==G and root['parameters']['subgroup']==H,'independent A5xC2 graph identification')
    N,dims,count=construct(G,H,coord)
    R=json.loads((BASE/'tensors.json').read_text())['R12_1_25'];P={r['id']:r for r in json.loads((BASE/'profile.json').read_text())['records']};ds=list(map(lambda x:int(x**0.5),P['R12_1_25']['squared_dimensions']))
    groups=[([i for i in range(1,12)if ds[i]==d],[i for i in range(1,12)if dims[i]==d])for d in(1,2,5)];T=np.array(R);M=np.array(N);basis=None
    for choices in product(*(permutations(J)for I,J in groups)):
        p=[0]*12
        for (I,J),v in zip(groups,choices):
            for i,j in zip(I,v):p[i]=j
        if np.array_equal(T,M[np.ix_(p,p,p)]):basis=p;break
    require(basis is not None,'independent balanced reconstruction matches all1728 coefficients')
    out=dict(status='PASS',id='R12_1_25',group_order=120,subgroup_order=10,subgroup='graph of D10 reflection sign in A5xC2',model='C(A5xC2,1,H,1)',simple_dimensions=dims,basis_map_source_to_independent_model=basis,balanced_quotient_basis_states=count,all_induced_module_equations_checked=True,exact_field='Q(zeta10)',model_tensor=N,elapsed_seconds=time.monotonic()-start)
    (HERE/'graph_model_independent.json').write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in out.items()if k!='model_tensor'})
