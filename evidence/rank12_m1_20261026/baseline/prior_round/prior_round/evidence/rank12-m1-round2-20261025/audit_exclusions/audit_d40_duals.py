"""Independent C2-Morita tensor audit for every relative D8 cocycle.

Reconstructs scalar Liptrap associators needed by an order-two algebra,
propagates its module equations rather than doing the discovery phase search,
and computes balanced products using an independent involution-trace formula.
"""
from itertools import product
from functools import lru_cache
import json,time
import numpy as np
from independent_audit import BASE,HERE,dual,require

FAMILY=HERE.parent/'family_graded'

def scalar_associator(R,cert):
    require(cert['modulus']==5,'recorded primitive fifth-root model')
    n=len(R);S=cert['serfs'];M=cert['lords'];ss=set(S);du=dual(R);mul=lambda a,b:R[a][b].index(1)
    P={tuple(v[:-1]):v[-1]for v in cert['phase_values']};v=lambda f,a,b,m:P.get((f,a,b,m),0)
    chi=lambda a,b,m:v('chi',a,b,m);u=lambda a,b,m:v('upsilon',a,b,m)
    require(cert['tau']=='positive_inverse_square_root','constant positive tau')
    H=cert['stabilizer'];require(len(H)==5,'adjoint C5')
    for m in M:
        C=[tuple(chi(a,b,m)%5 for b in H)for a in H];require(len(set(C))==5,'nondegenerate bicharacter')
        for a,b,c in product(H,repeat=3):require((chi(a,b,m)-chi(b,a,m))%5==0 and(chi(mul(a,b),c,m)-chi(a,c,m)-chi(b,c,m))%5==0,'symmetric bicharacter')
    for a,b,m in product(S,S,M):require((chi(b,a,du[m])-chi(a,b,mul(mul(a,m),b)))%5==0,'Liptrap quasisymmetry')
    for a,b,c,m in product(S,S,S,M):require((u(a,b,m)-u(a,b,mul(m,du[c]))+chi(mul(a,b),c,m)-chi(a,c,m)-chi(b,c,mul(du[a],m)))%5==0,'Liptrap biderivation')
    @lru_cache(None)
    def alpha(a,b,c):
        vals={(u(a,b,m)+u(mul(a,b),c,m)-u(a,mul(b,c),m)-u(b,c,mul(du[a],m)))%5 for m in M}
        require(len(vals)==1,'actual pointed associator independent of lord');return vals.pop()
    @lru_cache(None)
    def F(a,b,c,k):
        if a in ss and b in ss and c in ss:return alpha(a,b,c)
        if a in ss and b in ss:return u(a,b,k)%5
        if a in ss and c in ss:return chi(a,c,k)%5
        if b in ss and c in ss:return-u(b,c,du[a])%5
        if a in ss:return(alpha(du[k],a,mul(du[a],k))-u(du[k],a,mul(mul(du[k],a),b)))%5
        if b in ss:return(u(k,du[k],a)-u(k,du[k],mul(a,b))+chi(k,b,mul(a,b)))%5
        if c in ss:
            require(mul(c,c)==0,'this beta3 formula only used for self-inverse algebra elements')
            return(u(c,du[k],du[b])-alpha(c,du[k],k)-alpha(mul(c,du[k]),mul(k,c),c))%5
        raise ValueError('three-lord Fourier matrices are never needed by this C2 bimodule calculation')
    return F,mul,du

def model(R,F0,mul,c,degree,W):
    q=40;F=lambda a,b,d,k:(8*F0(a,b,d,k)+10*W[degree[a]][degree[b]][degree[d]])%q
    require(mul(c,c)==0 and F(c,c,c,c)==0,'actual subgroup algebra')
    objs=[];seen=set();n=len(R)
    for z in range(n):
        if z in seen:continue
        D=sorted({z,mul(c,z),mul(z,c),mul(c,mul(z,c))});seen.update(D);L={}
        for x in D:
            if x in L:continue
            y=mul(c,x);require(x!=y,'free left action');L[x]=0;L[y]=-F(c,c,x,x)%q
        choices=[]
        for seed in(range(q)if len(D)==2 else[0]):
            A={z:seed};queue=[z];consistent=True
            for x in queue:
                for y,value in((mul(x,c),F(x,c,c,x)-A[x]),(mul(c,x),F(c,x,c,mul(c,mul(x,c)))+A[x]+L[mul(x,c)]-L[x])):
                    value%=q
                    if y in A:
                        if A[y]!=value:consistent=False;break
                    else:A[y]=value;queue.append(y)
                if not consistent:break
            if consistent:
                require(set(A)==set(D),'full double-coset propagation');choices.append(A)
        require(len(choices)==(2 if len(D)==2 else 1),'complete projective C2 stabilizer characters')
        for A in choices:objs.append(dict(z=z,D=D,L=L,R=A))
    require(len(objs)==12,'rank12 full dual')
    N=[[[0]*12 for _ in range(12)]for _ in range(12)]
    for i,A in enumerate(objs):
        for j,B in enumerate(objs):
            todo={(x,y,k)for x,y in product(A['D'],B['D'])for k,v in enumerate(R[x][y])if v};maps={}
            while todo:
                P=min(todo);x,y,k=P;Q=(mul(x,c),mul(c,y),k)
                phase=(F(x,c,mul(c,y),k)+B['L'][mul(c,y)]-A['R'][x])%q
                back=(F(mul(x,c),c,y,k)+B['L'][y]-A['R'][mul(x,c)])%q
                require((phase+back)%q==0,'inverse balancing relations')
                maps[P]=(P,0);maps[Q]=(P,phase);todo.difference_update((P,Q))
            roots=sorted({v[0]for v in maps.values()});L={};Rop={}
            for P in roots:
                x,y,k=P;Q,e=maps[mul(c,x),y,mul(c,k)];L[P]=(Q,(A['L'][x]-F(c,x,y,mul(c,k))+e)%q)
                Q,e=maps[x,mul(y,c),mul(k,c)];Rop[P]=(Q,(F(x,y,c,mul(k,c))+B['R'][y]+e)%q)
            Linv={Q:(P,-e%q)for P,(Q,e)in L.items()};require(len(Linv)==len(roots),'left action bijective')
            for k,C in enumerate(objs):
                fiber=[P for P in roots if P[2]==C['z']]
                if len(C['D'])==4:N[i][j][k]=len(fiber);continue
                gamma=(C['R'][C['z']]-C['L'][C['z']])%q;trace=0
                for P in fiber:
                    Q,e=Rop[P];T,f=Linv[Q]
                    if T==P:
                        phase=(e+f-gamma)%q;require(phase in(0,q//2),'normalized stabilizer involution has eigenvalues ±1')
                        trace+=1 if phase==0 else-1
                numerator=len(fiber)+trace;require(numerator>=0 and numerator%2==0,'exact involution eigenspace dimension');N[i][j][k]=numerator//2
    units=[u for u in range(12)if all(N[u][i][j]==N[i][u][j]==int(i==j)for i,j in product(range(12),repeat=2))];require(len(units)==1,'unique dual tensor unit')
    perm=units+[i for i in range(12)if i not in units]
    return[[[N[a][b][c]for c in perm]for b in perm]for a in perm]

if __name__=='__main__':
    start=time.monotonic();source=next(r for r in json.loads((FAMILY/'feudal40_models_sparse.json').read_text())if r['parameters']['group']=='F20');R=source['tensor'];cert=source['certificate'];F,mul,du=scalar_associator(R,cert)
    coc=json.loads((FAMILY/'d8_cocycles.json').read_text());degree=[a//5 for a in range(20)]+list(range(4,8));G=coc['group_table']
    require(all(G[degree[a]][degree[b]]==degree[k]for a,b,k in product(range(24),repeat=3)if R[a][b][k]),'actual universal D8 grading')
    outputs=[]
    # Reference outputs are recomputed once by the discovery constructor and
    # stored only per resulting model; compare both directly up to a based
    # permutation by testing all tensor entries through the supplied maps.
    target=json.loads((BASE/'tensors.json').read_text());accepted=json.loads((FAMILY/'feudal_twist_results.json').read_text());known={}
    for row in accepted:
        for m in row['models']:
            idx=m['parameters']['grading_twist']['cocycle'];known[json.dumps(idx)]=(row['id'],m)
    for index,W in enumerate(coc['representatives']):
        N=model(R,F,mul,10,degree,W);entry=dict(cocycle_index=index)
        pair=known.get(json.dumps(W))
        if pair:
            rid,m=pair;p=m['basis_map_source_to_model'];stored=m['model_tensor']
            # Independent module gauge choices may permute charged objects.
            import networkx as nx
            # The small multiplicity-free based matcher is used only to find
            # a permutation; all1728 equations are checked independently.
            import sys
            sys.path.insert(0,str(BASE/'sources/work/rank11'));from common import based_iso
            p0=based_iso(N,stored);require(p0 is not None,'independent tensor equals discovery output up to basis')
            require(all(N[i][j][k]==stored[p0[i]][p0[j]][p0[k]]for i,j,k in product(range(12),repeat=3)),'all independent/discovery coefficients')
            require(all(target[rid][i][j][k]==stored[p[i]][p[j]][p[k]]for i,j,k in product(range(12),repeat=3)),'all target binding coefficients')
            entry['matched_id']=rid
        else:
            # Every candidate must still match one of the two accepted input
            # tensors; this includes coincident cohomology outputs discarded
            # by the discovery driver's duplicate-output cache.
            import sys
            sys.path.insert(0,str(BASE/'sources/work/rank11'));from common import based_iso
            matches=[]
            for rid in('R12_1_156','R12_1_263'):
                perm=based_iso(target[rid],N)
                if perm is not None:
                    require(all(target[rid][i][j][k]==N[perm[i]][perm[j]][perm[k]]for i,j,k in product(range(12),repeat=3)),'all target/independent coefficients')
                    matches.append(rid)
            require(len(matches)==1,'all16 exact duals are covered by the two accepted tensors');entry['matched_id']=matches[0]
        outputs.append(entry)
    result=dict(status='PASS',source_categorical_hypotheses='all Liptrap identities independently checked; phases unitary and bicharacter nondegenerate',relative_cocycle_count=16,records=outputs,elapsed_seconds=time.monotonic()-start)
    (HERE/'d40_duals_independent.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
