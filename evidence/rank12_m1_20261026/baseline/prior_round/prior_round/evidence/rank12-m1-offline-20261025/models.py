"""Established unitary constructions; each match checks all 1728 coefficients."""
from pathlib import Path
import collections,itertools,json,sys,time
import numpy as np
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'sources/work/models'))
sys.path.insert(0,str(ROOT/'sources/work/root_models'))
sys.path.insert(0,str(ROOT/'sources/work/rank11/known_models'))
import match_models as mm
from extra_models import metaplectic,abelian_table,dihedral_table,dicyclic_table,a4_table,auts,pointed_equivariant
from zest_models import gradings,zest
from construct import half_even_metaplectic
from standard import cyclic_equivariant
sys.path.insert(0,str(ROOT/'sources/work/rank11'))
import common

def direct():
    for orders in [(12,),(6,2)]:
        yield 'Vec('+str(orders)+')',mm.group(orders),'pointed',dict(orders=orders),True
    for name,G in [('D12',dihedral_table(6)),('Dic3',dicyclic_table(3)),('A4',a4_table())]:
        M=[[[int(G[i][j]==k)for k in range(12)]for j in range(12)]for i in range(12)]
        yield 'Vec('+name+')',M,'pointed_group',dict(group=name,group_table=G),False
    yield 'TY(C11)',mm.ty((11,)),'ty',dict(orders=[11]),False
    for k,e in [(11,False),(22,True),(23,True)]:
        yield ('PSU'if e else'SU')+f'(2)_{k}',mm.su2(k,e),'su2',dict(level=k,even=e),True
    for m,d in [(18,False),(18,True),(21,False)]:
        yield ('Rep(Dic9)'if d else f'Rep(D{2*m})'),mm.rep_dihedral(m,d),'dihedral_rep',dict(m=m,dicyclic=d),True
    yield 'SO(17)_2',metaplectic(17),'odd_metaplectic',dict(N=17),True
    # Literature existence, not a numerical modular-data inference:
    # Grossman-Izumi, Quantum Topol.13 (2022), Example4.5, gives two actual
    # generalized Haagerup categories for C6 with these same fusion rules.
    m=6;n=12;T=[[[0]*n for _ in range(n)]for _ in range(n)]
    for a,b in itertools.product(range(m),repeat=2):
        T[a][b][(a+b)%m]=1;T[a][m+b][m+(a+b)%m]=1
        T[m+a][b][m+(a-b)%m]=1;T[m+a][m+b][(a-b)%m]=1
        for c in range(m):T[m+a][m+b][m+c]=1
    yield 'Generalized Haagerup(C6)',T,'haagerup_izumi_cyclic',dict(group_order=6,reference='Grossman-Izumi, Drinfeld centers of fusion categories arising from generalized Haagerup subfactors, Quantum Topol.13 (2022),593-668, Example4.5; arXiv:1501.07679v2'),False
    M,labs=half_even_metaplectic(28)
    yield 'Half SO(28)_2',M,'half_even_metaplectic',dict(N=28,labels=labs),True
    two=[('Vec(C2)',mm.group((2,))),('Fib',mm.su2(3,True))]
    # Every rank-six M1 positive class from the accepted lower-rank catalogue.
    for r in json.loads((ROOT/'lower_rank6_all.json').read_text()):
        for name,A in two:
            rn=r['name']
            rb=('\\Rep('in rn or rn.startswith('$PSU')or rn=='$SO(5)_2$'or rn.startswith('$\\Vec_{C_2}\\boxtimes\\mathrm{Ising}')or rn.startswith('$\\Vec_{C_2}\\boxtimes\\Rep')or rn.startswith('$\\Vec_{C_2}\\boxtimes PSU')or rn.startswith('$\\mathrm{Fib}\\boxtimes')or rn.startswith('$\\Vec_{C_2}\\boxtimes\\Vec'))
            lifts=True if rb else[len(r['tensor'])]if name=='Vec(C2)'else False
            yield name+' x '+rn,mm.prod(A,r['tensor']),'deligne_product',dict(left_name=name,left_tensor=A,right_name=rn,right_tensor=r['tensor'],right_reference=r['reference'],central_lift_from_left_factor=name=='Vec(C2)'),lifts
    three=[('Vec(C3)',mm.group((3,))),('Ising',mm.ty((2,))),('Rep(S3)',mm.rep_dihedral(3)),('PSU(2)_5',mm.su2(5,True))]
    for r in json.loads((ROOT/'lower_rank45_models.json').read_text()):
        B=r['tensor']
        if len(B)!=4 or max(v for A in B for row in A for v in row)>1:continue
        for name,A in three:
            rb=r['name']not in['TY(C3)','pseudo-PSU(2)_6']
            lifts=True if rb else[len(B)]if name in['Ising','Rep(S3)']else False
            yield name+' x '+r['name'],mm.prod(A,B),'deligne_product',dict(left_name=name,left_tensor=A,right_name=r['name'],right_tensor=B,right_reference=r['reference'],central_lift_from_left_factor=name in['Ising','Rep(S3)']),lifts
    # Strict group-automorphism actions on pointed categories.
    groups=[('C12',abelian_table((12,))),('C6xC2',abelian_table((6,2))),('D12',dihedral_table(6)),('Dic3',dicyclic_table(3)),('A4',a4_table()),('C15',abelian_table((15,))),('C18',abelian_table((18,))),('C3xC3xC2',abelian_table((3,3,2))),('D18',dihedral_table(9)),('C21',abelian_table((21,)))]
    for name,G in groups:
        for sigma in auts(G):
            if not all(sigma[sigma[i]]==i for i in range(len(G))):continue
            f=sum(sigma[i]==i for i in range(len(G)))
            if len(G)+3*f!=24:continue
            M=pointed_equivariant(G,sigma)
            braided=all(G[i][j]==G[j][i]for i,j in itertools.product(range(len(G)),repeat=2))
            yield 'Vec('+name+')^C2',M,'pointed_equivariant',dict(group=name,group_table=G,automorphism=sigma),braided
    # Orthogonal TY involutions and their two parity coherences.
    for m in [8,14,17]:
        for u in range(1,m):
            if (u*u-1)%m:continue
            sigma=[u*a%m for a in range(m)]+[m]
            f=sum(sigma[i]==i for i in range(m+1))
            if m+1+3*f!=24:continue
            for parity in [0,1]:
                pp=[0]*m+[parity];M,labs=cyclic_equivariant(mm.ty((m,)),sigma,2,pp)
                yield f'TY(C{m})^C2[u={u}; parity={parity}]',M,'ty_cyclic_equivariant',dict(orders=[m],automorphism=sigma,parity=pp,labels=labs,bicharacter_modulus=m,bicharacter_exponents=[[a*b%m for b in range(m)]for a in range(m)]),False
    for orders in [(4,2),(2,2,2)]:
        G=abelian_table(orders);els=list(itertools.product(*(range(a)for a in orders)));forms=[]
        if orders==(4,2):
            mod=4
            for a,b,c in itertools.product(range(4),range(2),range(2)):
                C=[[(a*x[0]*y[0]+2*b*(x[0]*y[1]+x[1]*y[0])+2*c*x[1]*y[1])%4 for y in els]for x in els]
                if len(set(map(tuple,C)))==8:forms.append(C)
        else:
            mod=2;pos=[(a,b)for a in range(3)for b in range(a,3)]
            for vals in itertools.product(range(2),repeat=6):
                A=[[0]*3 for _ in range(3)]
                for (a,b),v in zip(pos,vals):A[a][b]=A[b][a]=v
                C=[[sum(A[a][b]*x[a]*y[b]for a,b in itertools.product(range(3),repeat=2))%2 for y in els]for x in els]
                if len(set(map(tuple,C)))==8:forms.append(C)
        for sig in auts(G):
            if not all(sig[sig[a]]==a for a in range(8))or sum(sig[a]==a for a in range(8))!=4:continue
            chi=next((C for C in forms if all(C[sig[a]][sig[b]]==C[a][b]for a,b in itertools.product(range(8),repeat=2))),None)
            if chi is None:continue
            for parity in [0,1]:
                pp=[0]*8+[parity];sigma=sig+[8];M,labs=cyclic_equivariant(mm.ty(orders),sigma,2,pp)
                yield f'TY({orders})^C2[parity={parity}]',M,'ty_cyclic_equivariant',dict(orders=list(orders),automorphism=sigma,parity=pp,labels=labs,bicharacter_modulus=mod,bicharacter_exponents=chi),False

def main():
    start=time.monotonic();data=json.loads((ROOT/'tensors.json').read_text());buckets=collections.defaultdict(list)
    for rid,R in data.items():buckets[common.coarse(R)].append((rid,R))
    out=collections.defaultdict(list);attempts=[];seen=set()
    for name,R,kind,par,braided in direct():
        variants=[(name,R,kind,par)]
        if braided:
            for g in gradings(R):
                for h in range(1,len(R)):
                    if isinstance(braided,list)and h not in braided:continue
                    if g[h]or R[h][h]!=[1]+[0]*(len(R)-1):continue
                    U=zest(R,g,h)
                    variants.append((f'C2-zest({name}; h={h})',U,'associative_C2_zest',dict(base_constructor=kind,base_parameters=par,base_name=name,base_tensor=R,grading=g,central_invertible=h)))
        for nm,M,kd,params in variants:
            h=common.sha(M)
            if h in seen:continue
            seen.add(h)
            if len(M)!=12 or max(v for A in M for B in A for v in B)>1:continue
            common.validate(M);hits=[]
            for rid,T in buckets[common.coarse(M)]:
                p=common.based_iso(T,M)
                if p is None:continue
                common.require(all(T[i][j][k]==M[p[i]][p[j]][p[k]]for i,j,k in itertools.product(range(12),repeat=3)),'full tensor equality')
                out[rid].append(dict(name=nm,constructor=kd,parameters=params,model_tensor=M,basis_map_source_to_model=p));hits.append(rid)
            attempts.append(dict(name=nm,constructor=kd,tensor_sha256=h,matches=hits))
    records=[dict(id=rid,tensor_sha256=common.sha(data[rid]),models=out[rid])for rid in data if rid in out]
    (ROOT/'models.json').write_text(json.dumps(records,indent=2)+'\n')
    (ROOT/'model_attempts.json').write_text(json.dumps(attempts,indent=2)+'\n')
    print('MODELS',len(records),'unique candidates',len(attempts),'seconds',time.monotonic()-start)
    print([(r['id'],r['models'][0]['name'])for r in records])

if __name__=='__main__':main()
