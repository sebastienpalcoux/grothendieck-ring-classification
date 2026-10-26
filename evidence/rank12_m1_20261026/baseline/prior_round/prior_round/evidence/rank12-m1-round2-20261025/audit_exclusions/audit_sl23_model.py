"""Independent weighted balanced-quotient audit of the SL2(3) model R597.

Uses stored actual scalar-fiber actions as witnesses, independently verifies
every defining module equation and complete stabilizer characters, then
recomputes all tensor products by phase-weighted quotient graphs over Q(ζ8).
No import from the root's or integral agent's model constructors.
"""
from itertools import product
from collections import defaultdict
import json,time
import numpy as np
from independent_audit import BASE,HERE,require

def rational(co):
    co=co[:]
    for i in range(7,3,-1):co[i-4]-=co[i];co[i]=0
    require(not any(co[1:]),'exact Q(zeta8) rationality')
    return co[0]

def reconstruct(r):
    par=r['parameters'];G=par['group_table'];H=par['subgroup'];W=np.array(par['cocycle_exponents'],dtype=np.int64);psi={(a,b):v for a,b,v in par['subgroup_cochain']};n=len(G)
    vals=[v for v in product(range(3),repeat=4)if(v[0]*v[3]-v[1]*v[2])%3==1];one=(1,0,0,1);vals=[one]+[v for v in vals if v!=one];ix={v:i for i,v in enumerate(vals)}
    def mul(a,b):return((a[0]*b[0]+a[1]*b[2])%3,(a[0]*b[1]+a[1]*b[3])%3,(a[2]*b[0]+a[3]*b[2])%3,(a[2]*b[1]+a[3]*b[3])%3)
    require(n==24 and G==[[ix[mul(a,b)]for b in vals]for a in vals],'fresh actual SL2(F3) table')
    inv=[next(j for j in range(n)if G[i][j]==0)for i in range(n)];A=np.array(G);b,c,d=np.indices((n,n,n))
    require(W.shape==(n,n,n)and not W[0].any()and not W[:,0].any()and not W[:,:,0].any(),'normalized explicit U1 cocycle')
    for a in range(n):require(not np.any((W[b,c,d]+W[a,A[b,c],d]+W[a,b,c]-W[A[a,b],c,d]-W[a,b,A[c,d]])%8),'all actual 24^4 group cocycle identities')
    require(len(H)==4 and 0 in H and all(G[a][b]in H for a,b in product(H,repeat=2)),'actual order-four subgroup')
    gen=par['construction']['order4_generator'];powers=[0]
    for _ in range(3):powers.append(G[powers[-1]][gen])
    require(sorted(powers)==H and G[powers[-1]][gen]==0,'cyclic C4 subgroup')
    require(all(psi[0,h]==psi[h,0]==0 for h in H),'normalized subgroup algebra')
    require(all((psi[b,c]+psi[a,G[b][c]]-psi[G[a][b],c]-psi[a,b]+int(W[a,b,c]))%8==0 for a,b,c in product(H,repeat=3)),'all algebra associativity equations')
    O=[];blocks=defaultdict(list)
    for raw in r['bimodule_witness']['objects']:
        require(raw['fiber_dimension']==1,'all stabilizers cyclic: scalar witnesses suffice')
        g=raw['representative'];D=raw['support'];L={(h,x):v for h,x,v in raw['left_phases']};R={(x,h):v for x,h,v in raw['right_phases']}
        require(D==sorted({G[G[a][g]][b]for a,b in product(H,repeat=2)}),'exact support double coset')
        require(set(L)==set(product(H,D))and set(R)==set(product(D,H)),'complete action tables')
        require(all(L[0,x]==R[x,0]==0 for x in D),'unit actions')
        for a,b,x in product(H,H,D):
            require((L[b,x]+L[a,G[b][x]]+int(W[a,b,x])-psi[a,b]-L[G[a][b],x])%8==0,'left module associativity')
            require((R[x,a]+R[G[x][a],b]-int(W[x,a,b])-psi[a,b]-R[x,G[a][b]])%8==0,'right module associativity')
            require((L[a,x]+R[G[a][x],b]-R[x,b]-L[a,G[x][b]]-int(W[a,x,b]))%8==0,'bimodule compatibility')
        K=[h for h in H if G[G[inv[g]][h]][g]in H]
        gamma={h:(R[g,G[G[inv[g]][h]][g]]-L[h,g])%8 for h in K}
        o=dict(g=g,D=D,L=L,R=R,K=K,gamma=gamma);O.append(o);blocks[tuple(D)].append(o)
    require(len(O)==12 and set.union(*(set(D)for D in blocks))==set(range(n)),'complete support inventory')
    for D,objects in blocks.items():
        K=objects[0]['K'];require(len(objects)==len(K),'complete projective scalar degrees')
        for i,C in enumerate(objects):
            for j,B in enumerate(objects):
                co=[0]*8
                for h in K:co[(C['gamma'][h]-B['gamma'][h])%8]+=1
                require(rational(co)==len(K)*int(i==j),'all projective characters orthogonal')
    N=[[[0]*12 for _ in range(12)]for _ in range(12)];balanced_count=0
    for i,C in enumerate(O):
        for j,B in enumerate(O):
            remaining=set(product(C['D'],B['D']));maps={}
            while remaining:
                root=min(remaining);maps[root]=(root,0);queue=[root]
                for x,y in queue:
                    _,e=maps[x,y]
                    for h in H:
                        q=G[inv[h]][y];Q=(G[x][h],q);phase=(e+int(W[x,h,q])+B['L'][h,q]-C['R'][x,h])%8
                        if Q in maps:require(maps[Q]==(root,phase),'consistent weighted balanced graph')
                        else:maps[Q]=(root,phase);queue.append(Q)
                require(len(queue)==4,'free balanced subgroup action');remaining.difference_update(queue)
            roots=sorted({r for r,e in maps.values()});balanced_count+=len(roots);L={};R={}
            for h in H:
                L[h]={};R[h]={}
                for P in roots:
                    x,y=P;root,e=maps[G[h][x],y];L[h][P]=(root,(C['L'][h,x]-int(W[h,x,y])+e)%8)
                    root,e=maps[x,G[y][h]];R[h][P]=(root,(int(W[x,y,h])+B['R'][y,h]+e)%8)
            Linv={h:{Q:(P,-e%8)for P,(Q,e)in L[h].items()}for h in H}
            for k,F in enumerate(O):
                g=F['g'];co=[0]*8;fiber=[P for P in roots if G[P[0]][P[1]]==g]
                for h in F['K']:
                    q=G[G[inv[g]][h]][g]
                    for P in fiber:
                        Q,e=R[q][P];T,f=Linv[h][Q]
                        if T==P:co[(e+f-F['gamma'][h])%8]+=1
                numerator=rational(co);denom=len(F['K']);require(numerator>=0 and numerator%denom==0,'actual nonnegative integral fusion coefficient');N[i][j][k]=numerator//denom
    return N,balanced_count

if __name__=='__main__':
    start=time.monotonic();r=json.loads((HERE.parent/'root/sl23_twist_models.json').read_text())['models'][0];N,balanced=reconstruct(r)
    require(N==r['model_tensor'],'independent full tensor agrees with the recorded constructor')
    R=json.loads((BASE/'tensors.json').read_text())[r['id']];p=r['basis_map_source_to_model']
    require(p[0]==0 and sorted(p)==list(range(12))and all(R[i][j][k]==N[p[i]][p[j]][p[k]]for i,j,k in product(range(12),repeat=3)),'all1728 input/model coefficients')
    out=dict(status='PASS',id=r['id'],model='C(SL2(3),omega,C4,psi)',actual_group_cocycle_equations=24**4,all_algebra_module_and_bimodule_equations=True,complete_projective_characters=True,balanced_quotient_basis_states=balanced,input_tensor_coefficients=1728,elapsed_seconds=time.monotonic()-start)
    (HERE/'sl23_model_independent.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
