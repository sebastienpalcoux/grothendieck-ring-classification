"""Small Sylow-D8 cocycle construction and exact cohomological transfer.

This is positive discovery only; absence of a match is not a criterion.
"""
from pathlib import Path
import itertools,json,sys,time
import numpy as np
BASE=Path(__file__).resolve().parents[2]/'rank12-m1-offline-20261025';OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE));import group_models as gm
import common
from twisted_h4 import solve,MOD
from twisted_h4_matrix import construct
from twisted48_models import schur_cover

def cocycles_d8():
    G=gm.dihedral_table(4);trip=list(itertools.product(range(1,8),repeat=3));ix={t:i for i,t in enumerate(trip)};quad=list(itertools.product(range(1,8),repeat=4));rows=[];terms=[]
    for a,b,c,d in quad:
        ts=[((b,c,d),1),((G[a][b],c,d),-1),((a,G[b][c],d),1),((a,b,G[c][d]),-1),((a,b,c),1)];line=[(ix[t],z)for t,z in ts if all(t)];terms.append(line);mask=0
        for j,z in line:mask^=1<<j
        rows.append(mask)
    piv={};deps=[]
    for i,row in enumerate(rows):
        x=row;trans=1<<i
        while x:
            p=(x&-x).bit_length()-1
            if p not in piv:piv[p]=(x,trans);break
            x^=piv[p][0];trans^=piv[p][1]
        if not x:deps.append(trans)
    free=[i for i in range(len(trip))if i not in piv];kernel=[]
    for f in free:
        x=1<<f
        for p,(row,tr)in sorted(piv.items(),reverse=True):
            if (row&x).bit_count()%2:x^=1<<p
        kernel.append(x)
    span={}
    def add(x):
        while x:
            p=(x&-x).bit_length()-1
            if p not in span:span[p]=x;return True
            x^=span[p]
        return False
    for a,b in itertools.product(range(1,8),repeat=2):
        x=0
        for j,(u,v,w)in enumerate(trip):
            val=int((v,w)==(a,b))+int((G[u][v],w)==(a,b))+int((u,G[v][w])==(a,b))+int((u,v)==(a,b))
            if val%2:x^=1<<j
        add(x)
    hs=[x for x in kernel if add(x)]
    lift=None
    for bits in itertools.product(range(2),repeat=len(hs)):
        v=0
        for bit,x in zip(bits,hs):
            if bit:v^=x
        if not v:continue
        rhs=0
        for i,line in enumerate(terms):
            val=sum(z*((v>>j)&1)for j,z in line)
            common.require(val%2==0,'mod2 3-cocycle')
            if (val//2)%2:rhs^=1<<i
        if any((dep&rhs).bit_count()%2 for dep in deps):continue
        u=0
        for p,(row,tr)in sorted(piv.items(),reverse=True):
            bit=(tr&rhs).bit_count()%2
            if bit^((row&u).bit_count()%2):u^=1<<p
        w=[((v>>j)&1)+2*((u>>j)&1)for j in range(len(trip))]
        common.require(all(sum(z*w[j]for j,z in line)%4==0 for line in terms),'lifted Z4 3-cocycle')
        lift=w;break
    common.require(lift is not None,'explicit fourth-root lift found')
    gens=[[2*((x>>j)&1)for j in range(len(trip))]for x in hs]+[lift]
    tables=[]
    for v in gens:
        W=np.zeros((8,8,8),dtype=np.int16)
        for t,a in zip(trip,v):W[t]=a
        tables.append(W)
    return G,tables,dict(mod2_cohomology_dimension=len(hs),mod2_cocycle_dimension=len(kernel),normalized_variables=343,normalized_equations=2401)

def transfer_generators():
    D,ws,info=cocycles_d8();ps,G=gm.permutation_group(4);a=ps.index((1,2,3,0));b=ps.index((0,3,2,1));H=gm.subgroup(G,[a,b]);inv=[next(j for j in range(24)if G[i][j]==0)for i in range(24)];powers=[0]
    for _ in range(3):powers.append(G[powers[-1]][a])
    iso={2*i+j:G[powers[i]][b]if j else powers[i]for i in range(4)for j in range(2)}
    # Inherited dihedral_table uses rotations 0..3 then reflections4..7.
    iso={i:powers[i]for i in range(4)}|{4+i:G[powers[i]][b]for i in range(4)}
    common.require(all(iso[D[x][y]]==G[iso[x]][iso[y]]for x,y in itertools.product(range(8),repeat=2)),'Sylow D8 identification')
    inviso={v:k for k,v in iso.items()};cosets=[];which={}
    for x in range(24):
        if x in which:continue
        t=len(cosets);cosets.append(x)
        for h in H:which[G[h][x]]=t
    common.require(len(cosets)==3,'Sylow index three')
    step={}
    for ti,x in enumerate(cosets):
        for g in range(24):
            y=G[x][g];tj=which[y];h=G[y][inv[cosets[tj]]];step[ti,g]=(tj,inviso[h])
    out=[]
    for W in ws:
        V=np.zeros((24,24,24),dtype=np.int16)
        for a,b,c in itertools.product(range(24),repeat=3):
            val=0
            for ti in range(3):
                tj,x=step[ti,a];tk,y=step[tj,b];tl,z=step[tk,c];val+=int(W[x,y,z])
            V[a,b,c]=val%4
        out.append(V)
    info.update(sylow_subgroup=H,dihedral_to_symmetric=iso,coset_representatives=cosets)
    return ps,G,out,info

def families():
    ps,S,gens,info=transfer_generators();old=json.loads((OUT/'order48_models.json').read_text());fingerprints=set();parity=[sum(p[i]>p[j]for i in range(4)for j in range(i+1,4))%2 for p in ps]
    common.dump(OUT/'transfer_cohomology_setup.json',dict(info=info,generator_tables=[W.tolist()for W in gens]))
    for bits in itertools.product(range(2),repeat=len(gens)):
        V=sum((bit*W for bit,W in zip(bits,gens)),np.zeros((24,24,24),dtype=np.int16))%4
        fingerprint=[]
        for g in range(24):
            k=0;v=0
            while True:
                v+=int(V[g,k,g]);k=S[k][g]
                if k==0:break
            fingerprint.append(v%4)
        # Sampling one representative per cyclic restriction fingerprint is
        # a discovery choice, not a claim of cohomological exhaustiveness.
        fp=tuple(fingerprint)
        if fp in fingerprints:continue
        fingerprints.add(fp)
        for row in old:
            G=row['model']['parameters']['group_table'];H=row['model']['parameters']['subgroup'];name=row['model']['name'];W=np.array([[[2*V[a//2,b//2,c//2]for c in range(48)]for b in range(48)]for a in range(48)],dtype=np.int16)
            A=np.array(G);bs=np.arange(48)[:,None,None];cs=np.arange(48)[None,:,None];ds=np.arange(48)[None,None,:]
            for a in range(48):
                delta=W+W[a,A[:,:,None],ds]+W[a,:,:,None]-W[A[a,:,None,None],cs,ds]-W[a,bs,A[None,:,:]]
                common.require(not(np.mod(delta,MOD).any()),'all transferred group cocycle identities')
            def w(a,b,c,W=W):return int(W[a,b,c])
            var=[(a,b)for a,b in itertools.product(H,repeat=2)if a and b];ix={v:i for i,v in enumerate(var)};eq=[];rhs=[]
            for a,b,c in itertools.product(H,repeat=3):
                r=[0]*len(var)
                for x,y,z in[(b,c,1),(a,G[b][c],1),(G[a][b],c,-1),(a,b,-1)]:
                    if x and y:r[ix[x,y]]+=z
                eq.append(r);rhs.append(-w(a,b,c)%MOD)
            sol=solve(eq,rhs,first=True)
            if not sol:continue
            psi0={v:x for v,x in zip(var,sol[0])};psi0.update({(a,b):0 for a,b in itertools.product(H,repeat=2)if not a or not b})
            classes=[0,1]if all(G[h][h]==0 for h in H)else[0]
            h1,h2=H[1:3];labels={0:(0,0),h1:(1,0),h2:(0,1),G[h1][h2]:(1,1)}
            for cl in classes:
                def psi(a,b,psi0=psi0,cl=cl,labels=labels):return(psi0[a,b]+4*cl*labels[a][0]*labels[b][1])%MOD
                yield name,G,H,w,psi,dict(transfer_generator_bits=bits,cyclic_restriction_fingerprint=fingerprint,subgroup_class=cl,subgroup_cochain=[[a,b,psi(a,b)]for a,b in itertools.product(H,repeat=2)],symmetric_cocycle_table=V.tolist(),modulus=MOD)

def main():
    start=time.monotonic();D=json.loads((BASE/'tensors.json').read_text());ids={r['id']for r in json.loads((BASE/'unresolved_families.json').read_text())['records']if r['family']=='D48'};results=[];attempts=[]
    for name,G,H,w,psi,params in families():
        R,info=construct(G,H,w,psi=psi);hits=[]
        if R is not None:
            common.validate(R)
            for rid in ids:
                p=common.based_iso(D[rid],R)
                if p is not None:
                    hits.append(rid);results.append(dict(id=rid,status='unitarily_realized',model=dict(name=name+', Sylow-transfer cocycle',constructor='sylow_transfer_h4_bimodules',parameters=dict(group_table=G,subgroup=H,cocycle=params,objects=info['objects']),model_tensor=R,basis_map_source_to_model=p)))
        attempts.append(dict(name=name,bits=params['transfer_generator_bits'],subgroup_class=params['subgroup_class'],info={k:v for k,v in info.items()if k!='objects'},matches=hits));print(name,params['transfer_generator_bits'],params['subgroup_class'],{k:v for k,v in info.items()if k!='objects'},hits,flush=True)
        (OUT/'transfer48_models.json').write_text(json.dumps(results,indent=2)+'\n');(OUT/'transfer48_attempts.json').write_text(json.dumps(attempts,indent=2)+'\n')
    print('DONE',len(results),'distinct',len({r['id']for r in results}),time.monotonic()-start)
if __name__=='__main__':main()
