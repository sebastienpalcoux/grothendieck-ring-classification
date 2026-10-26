"""Classical C(G,1,H,1) constructions; full equivariant-bundle convolution.

The inherited real-character implementation is extended to cyclic/dicyclic
stabilizers by complete ordinary characters and conjugate inner products.
"""
from pathlib import Path
import collections,itertools,json,math,sys,time
import numpy as np
import sympy as s
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'sources/work/models'))
from extra_models import dihedral_table,a4_table
sys.path.insert(0,str(ROOT/'sources/work/rank11'))
import common

def order(M,a):
    x=a;k=1
    while x:x=M[x][a];k+=1
    return k
def subgroup(M,gens):
    out={0};queue=[0]
    for x in queue:
        for g in gens:
            y=M[x][g]
            if y not in out:out.add(y);queue.append(y)
    return sorted(out)
def group_product(A,B):
    b=len(B)
    return [[A[i//b][j//b]*b+B[i%b][j%b]for j in range(len(A)*b)]for i in range(len(A)*b)]
def matrix_group(p,special=False):
    vals=[a for a in itertools.product(range(p),repeat=4)if ((a[0]*a[3]-a[1]*a[2])%p==1 if special else(a[0]*a[3]-a[1]*a[2])%p!=0)]
    one=(1,0,0,1);vals=[one]+[a for a in vals if a!=one];ix={a:i for i,a in enumerate(vals)}
    def mul(a,b):return((a[0]*b[0]+a[1]*b[2])%p,(a[0]*b[1]+a[1]*b[3])%p,(a[2]*b[0]+a[3]*b[2])%p,(a[2]*b[1]+a[3]*b[3])%p)
    return vals,[[ix[mul(a,b)]for b in vals]for a in vals]
def permutation_group(n):
    vals=list(itertools.permutations(range(n)));ix={a:i for i,a in enumerate(vals)}
    return vals,[[ix[tuple(a[b[i]]for i in range(n))]for b in vals]for a in vals]

def characters(M,H,K,L):
    inv={a:next(b for b in H if M[a][b]==0)for a in H};gens=[]
    while len(subgroup(M,gens))<len(H):gens.append(next(a for a in H if a not in subgroup(M,gens)))
    zeta=K.unit;out=[]
    for images in itertools.product(*(range(order(M,a))for a in gens)):
        phase={0:0};queue=[0];good=True
        for a in queue:
            for g,k in zip(gens,images):
                b=M[a][g];v=(phase[a]+k*(L//order(M,g)))%L
                if b in phase:
                    if phase[b]!=v:good=False;break
                else:phase[b]=v;queue.append(b)
            if not good:break
        if good:out.append({a:zeta**phase[a]for a in H})
    out.sort(key=lambda c:0 if all(v==K.one for v in c.values())else 1)
    if len(out)!=len(H):
        m=len(H)//2;r=next((a for a in H if order(M,a)==m),None)
        common.require(r is not None,'supported index-two cyclic stabilizer')
        A=[0]
        for _ in range(1,m):A.append(M[A[-1]][r])
        x=next(a for a in H if a not in A)
        common.require(M[M[x][r]][inv[x]]==inv[r],'dihedral/dicyclic inversion action')
        for k in range(1,(m+1)//2):
            row={a:K.zero for a in H}
            for j,a in enumerate(A):row[a]=zeta**((L//m*k*j)%L)+zeta**((-L//m*k*j)%L)
            out.append(row)
    common.require(sum(int(c[0].to_list()[0])**2 for c in out)==len(H),'complete irreducible degrees')
    for i,c in enumerate(out):
        for j,d in enumerate(out):common.require(sum((c[inv[a]]*d[a]for a in H),K.zero)==K(len(H)*int(i==j)),'character orthogonality')
    return out

def fusion(M,H):
    n=len(M);H=sorted(H);hs=set(H);inv=[next(j for j in range(n)if M[i][j]==0)for i in range(n)]
    L=math.lcm(*(order(M,a)for a in H));K=s.QQ.cyclotomic_field(L);zero=K.zero
    objects=[];covered=set()
    for z in range(n):
        if z in covered:continue
        orbit={M[M[u][z]][inv[v]]:(u,v)for u in H for v in H};covered|=set(orbit)
        stab=[a for a in H if M[M[inv[z]][a]][z]in hs]
        for chi in characters(M,stab,K,L):objects.append((z,stab,chi,orbit))
    rank=len(objects)
    if rank!=12:return None,dict(rank=rank)
    cosets=[];covered=set()
    for x in range(n):
        if x not in covered:cosets.append(x);covered|={M[x][h]for h in H}
    cache={}
    def val(i,x,a,b):
        key=(i,x,a,b)
        if key in cache:return cache[key]
        z,stab,chi,orb=objects[i]
        if x not in orb or M[a][x]!=M[x][b]:v=zero
        else:
            u,v0=orb[x];v=chi[M[M[inv[u]][a]][u]]
        cache[key]=v;return v
    R=[[[0]*rank for _ in range(rank)]for _ in range(rank)]
    for k,(z,stab,chi,orb)in enumerate(objects):
        for i,j in itertools.product(range(rank),repeat=2):
            result=zero
            for a in stab:
                b=M[M[inv[z]][a]][z];tr=zero
                for x in cosets:
                    h=M[M[inv[x]][a]][x]
                    if h in hs:tr+=val(i,x,a,h)*val(j,M[inv[x]][z],h,b)
                result+=chi[inv[a]]*tr
            result/=K(len(stab));co=result.to_list()
            common.require(len(co)<=1 and(not co or co[0].denominator==1 and co[0]>=0),'exact nonnegative integral convolution')
            R[i][j][k]=int(co[0])if co else 0
            if R[i][j][k]>1:return None,dict(rank=rank,not_multiplicity_one=True,first_multiplicity=[i,j,k,R[i][j][k]])
    common.validate(R)
    return R,dict(rank=rank,cyclotomic_order=L,group_order=n,subgroup_order=len(H),simple_dimensions=[len(orb)*int(chi[0].to_list()[0])//len(H)for z,stab,chi,orb in objects])

def candidates():
    vals,G=permutation_group(4);a=vals.index((1,0,3,2));yield 'C(S4,<double transposition>)',G,subgroup(G,[a])
    A=a4_table();C2=[[0,1],[1,0]];G=group_product(A,C2);a=next(x for x in range(1,12)if order(A,x)==2)
    for t in [0,1]:yield f'C(A4 x C2,<(a,{t})>)',G,subgroup(G,[2*a+t])
    S=dihedral_table(3);G=group_product(S,S);yield 'C(S3 x S3,<diagonal reflection>)',G,subgroup(G,[21])
    els=list(itertools.product(range(4),range(3),range(3)));ix={a:i for i,a in enumerate(els)}
    def mul(x,y):
        g,a,b=x;h,c,d=y
        for _ in range(g):c,d=-d%3,c
        return((g+h)%4,(a+c)%3,(b+d)%3)
    G=[[ix[mul(a,b)]for b in els]for a in els]
    yield 'C((C3^2) semidirect C4,<square of C4>)',G,subgroup(G,[18])
    vals,G=matrix_group(3);H=[i for i,a in enumerate(vals)if a[1]==a[2]==0];yield 'C(GL(2,3),diagonal V4)',G,H
    vals,G=matrix_group(5,True);inv=[next(j for j in range(len(G))if G[i][j]==0)for i in range(len(G))]
    a=next(i for i in range(1,len(G))if order(G,i)==10);A=set(subgroup(G,[a]));H=[g for g in range(len(G))if {G[G[g][x]][inv[g]]for x in A}==A]
    common.require(len(H)==20,'binary dihedral normalizer')
    yield 'C(SL(2,5),Dic5)',G,H
    vals,G=permutation_group(5);r=vals.index((1,2,3,4,0));t=vals.index((0,4,3,2,1));yield 'C(S5,D10)',G,subgroup(G,[r,t])

def main():
    start=time.monotonic();data=json.loads((ROOT/'tensors.json').read_text());buckets=collections.defaultdict(list)
    for rid,R in data.items():buckets[common.coarse(R)].append((rid,R))
    rows=[];attempts=[]
    for name,G,H in candidates():
        A=np.array(G,dtype=np.int64)
        common.require(all(np.array_equal(A[A[i,:],:],A[i,A])for i in range(len(G))),'all group associativity equations')
        common.require(H==subgroup(G,H),'subgroup closure')
        R,info=fusion(G,H);hits=[]
        if R is not None:
            for rid,T in buckets[common.coarse(R)]:
                p=common.based_iso(T,R)
                if p is None:continue
                hits.append(rid);rows.append(dict(id=rid,tensor_sha256=common.sha(T),models=[dict(name=name,constructor='group_theoretical',parameters=dict(group_table=G,subgroup=H,cocycle='trivial',subgroup_cochain='trivial'),model_tensor=R,basis_map_source_to_model=p,reference='C(G,1,H,1): bimodules over the subgroup algebra in Vec(G); equivariant-bundle convolution')]))
        attempts.append(dict(name=name,info=info,matches=hits));print(name,info,hits,flush=True)
        (ROOT/'group_models.json').write_text(json.dumps(rows,indent=2)+'\n')
        (ROOT/'group_model_attempts.json').write_text(json.dumps(attempts,indent=2)+'\n')
    print('DONE',len(rows),'seconds',time.monotonic()-start)
if __name__=='__main__':main()
