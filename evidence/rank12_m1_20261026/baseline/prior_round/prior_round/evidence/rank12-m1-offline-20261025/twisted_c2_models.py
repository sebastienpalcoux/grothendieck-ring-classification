"""Usual twisted group-theoretical C2 bimodules, all phases exact modulo four.

Every model is the dual of Vec_G^omega at the separable subgroup algebra.
The tensor products below are actual balanced quotients of explicit bimodules.
"""
from pathlib import Path
import collections,itertools,json,sys,time
import numpy as np
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'sources/work/models'))
from extra_models import dihedral_table
sys.path.insert(0,str(ROOT/'sources/work/rank11'))
import common
from group_models import group_product,order

def construct(G,ss,w,expected_rank=12):
    n=len(G);seen=set();objs=[]
    common.require(ss!=0 and G[ss][ss]==0,'involutive subgroup generator')
    common.require(all(w(a,b,c)%4==0 for a,b,c in itertools.product([0,ss],repeat=3)),'trivial restricted cocycle')
    for z in range(n):
        if z in seen:continue
        D=sorted({z,G[ss][z],G[z][ss],G[G[ss][z]][ss]});seen.update(D)
        L={};todo=set(D)
        while todo:
            x=min(todo);y=G[ss][x];L[x]=0;L[y]=(-w(ss,ss,x))%4;todo-={x,y}
        choices=[]
        for vals in itertools.product(range(4),repeat=len(D)):
            R=dict(zip(D,vals))
            if any((L[x]+L[G[ss][x]]+w(ss,ss,x))%4 for x in D):continue
            if any((R[x]+R[G[x][ss]]-w(x,ss,ss))%4 for x in D):continue
            if any((L[x]+R[G[ss][x]]-R[x]-L[G[x][ss]]-w(ss,x,ss))%4 for x in D):continue
            choices.append(R)
        common.require(bool(choices),'explicit bimodule action exists')
        if len(D)==4:choices=choices[:1]
        else:common.require(len(D)==2 and len(choices)==2,'complete stabilizer characters')
        for R in choices:objs.append(dict(z=z,D=D,L=L,R=R))
    rank=len(objs)
    if rank!=expected_rank:return None,dict(rank=rank)
    N=[[[0]*rank for _ in range(rank)]for _ in range(rank)]
    for i,A in enumerate(objs):
        for j,B in enumerate(objs):
            pairs=list(itertools.product(A['D'],B['D']));maps={}
            for x,y in pairs:
                P=(x,y);Q=(G[x][ss],G[ss][y]);delta=(w(G[x][ss],ss,y)+B['L'][y]-A['R'][G[x][ss]])%4
                back=(w(x,ss,G[ss][y])+B['L'][G[ss][y]]-A['R'][x])%4
                common.require((delta+back)%4==0 and G[x][y]==G[Q[0]][Q[1]],'balanced relation and grade')
                rep=min(P,Q);maps[P]=(rep,0 if P==rep else delta)
            reps=sorted({rep for rep,phase in maps.values()})
            left={};right={}
            for P in reps:
                x,y=P;Q,phase=maps[G[ss][x],y]
                left[P]=(Q,(A['L'][x]-w(ss,x,y)+phase)%4)
                Q,phase=maps[x,G[y][ss]]
                right[P]=(Q,(w(x,y,ss)+B['R'][y]+phase)%4)
            # The balanced actions must respect both representatives of each relation.
            for P in pairs:
                x,y=P;rep,a=maps[P]
                for label,target,phase,ops in [('L',(G[ss][x],y),A['L'][x]-w(ss,x,y),left),('R',(x,G[y][ss]),w(x,y,ss)+B['R'][y],right)]:
                    r,b=maps[target];r0,c=ops[rep]
                    common.require(r==r0 and(phase+b-a-c)%4==0,'action descends to balanced quotient')
            linv={Q:(P,(-phase)%4)for P,(Q,phase)in left.items()}
            common.require(len(linv)==len(reps),'invertible left action')
            for P in reps:
                grade=G[P[0]][P[1]];Q,a=left[P];T,b=left[Q]
                common.require(T==P and(a+b+w(ss,ss,grade))%4==0,'balanced left module equation')
                Q,a=right[P];T,b=right[Q]
                common.require(T==P and(a+b-w(grade,ss,ss))%4==0,'balanced right module equation')
                Q,a=left[P];T,b=right[Q];Q0,c=right[P];T0,d=left[Q0]
                common.require(T==T0 and(a+b-c-d-w(ss,grade,ss))%4==0,'balanced bimodule compatibility')
            for k,C in enumerate(objs):
                z=C['z'];basis=[P for P in reps if G[P[0]][P[1]]==z]
                if len(C['D'])==4:N[i][j][k]=len(basis)
                else:
                    chi=(C['R'][z]-C['L'][z])%4;co=[0]*4
                    for P in basis:
                        Q,a=right[P];U,b=linv[Q]
                        if U==P:co[(a+b-chi)%4]+=1
                    common.require(co[1]==co[3],'real normalized stabilizer trace')
                    count=len(basis)+co[0]-co[2]
                    common.require(count>=0 and count%2==0,'exact nonnegative stabilizer multiplicity')
                    N[i][j][k]=count//2
                if N[i][j][k]>1:return None,dict(rank=rank,not_multiplicity_one=True)
    common.validate(N)
    return N,dict(rank=rank,objects=objs)

def families():
    S=dihedral_table(3);V=[[a^b for b in range(4)]for a in range(4)];G=group_product(S,V);ss=3*4
    # H^3(C2^3,C*) has the standard type-I, II and III representatives.
    # Omit type-I in the subgroup coordinate so omega|H is exactly trivial.
    terms=[(1,1,1),(2,2,2),(0,1,1),(0,2,2),(1,2,2),(0,1,2)]
    qlabel=[(int(a//4>=3),(a%4)&1,((a%4)>>1)&1)for a in range(24)]
    for bits in itertools.product(range(2),repeat=6):
        def wq(a,b,c,bits=bits):return 2*(sum(bit*a[i]*b[j]*c[k]for bit,(i,j,k)in zip(bits,terms))%2)
        yield 'C(S3 x V4,omega,C2)',G,ss,qlabel,wq,dict(quotient='C2^3',trilinear_terms=terms,coefficients=bits)
    G=group_product(S,S);ss=21;qlabel=[(int(a//6>=3),int(a%6>=3))for a in range(36)]
    terms=[(0,0,0),(1,1,1),(0,1,1)]
    for bits in itertools.product(range(2),repeat=3):
        if sum(bits)%2:continue
        def wq(a,b,c,bits=bits):return 2*(sum(bit*a[i]*b[j]*c[k]for bit,(i,j,k)in zip(bits,terms))%2)
        yield 'C(S3 x S3,omega,diagonal C2)',G,ss,qlabel,wq,dict(quotient='C2^2',trilinear_terms=terms,coefficients=bits)
    els=list(itertools.product(range(4),range(3),range(3)));ix={a:i for i,a in enumerate(els)}
    def mul(x,y):
        g,a,b=x;h,c,d=y
        for _ in range(g):c,d=-d%3,c
        return((g+h)%4,(a+c)%3,(b+d)%3)
    G=[[ix[mul(a,b)]for b in els]for a in els];qlabel=[(a[0],)for a in els]
    def wq(a,b,c):return(2*a[0]*((b[0]+c[0])//4))%4
    yield 'C((C3^2) semidirect C4,omega2,C2)',G,18,qlabel,wq,dict(quotient='C4',cyclic_cocycle_class=2)

def main():
    start=time.monotonic();data=json.loads((ROOT/'tensors.json').read_text());buckets=collections.defaultdict(list)
    for rid,R in data.items():buckets[common.coarse(R)].append((rid,R))
    rows=[];attempts=[]
    for name,G,ss,qlabel,wq,parameters in families():
        if parameters['quotient']=='C4':q=[(a,)for a in range(4)];add=lambda a,b:((a[0]+b[0])%4,)
        else:q=list(itertools.product(range(2),repeat=len(qlabel[0])));add=lambda a,b:tuple(x^y for x,y in zip(a,b))
        common.require(all(qlabel[G[a][b]]==add(qlabel[a],qlabel[b])for a,b in itertools.product(range(len(G)),repeat=2)),'quotient homomorphism')
        common.require(all((wq(b,c,d)+wq(a,add(b,c),d)+wq(a,b,c)-wq(add(a,b),c,d)-wq(a,b,add(c,d)))%4==0 for a,b,c,d in itertools.product(q,repeat=4)),'complete quotient cocycle equations')
        w=lambda a,b,c:wq(qlabel[a],qlabel[b],qlabel[c])
        M,info=construct(G,ss,w);hits=[]
        if M is not None:
            for rid,R in buckets[common.coarse(M)]:
                p=common.based_iso(R,M)
                if p is None:continue
                hits.append(rid);rows.append(dict(id=rid,tensor_sha256=common.sha(R),models=[dict(name=name,constructor='twisted_group_theoretical_c2',parameters=dict(group_table=G,subgroup_generator=ss,quotient_labels=qlabel,cocycle_parameters=parameters,objects=info['objects']),model_tensor=M,basis_map_source_to_model=p)]))
        attempts.append(dict(name=name,parameters=parameters,rank=info['rank'],matches=hits))
    (ROOT/'twisted_c2_models.json').write_text(json.dumps(rows,indent=2)+'\n');(ROOT/'twisted_c2_attempts.json').write_text(json.dumps(attempts,indent=2)+'\n')
    print('candidates',len(attempts),'matched records',len(rows),'distinct',len(set(r['id']for r in rows)),'seconds',time.monotonic()-start)
    print(sorted(set(r['id']for r in rows)))
if __name__=='__main__':main()
