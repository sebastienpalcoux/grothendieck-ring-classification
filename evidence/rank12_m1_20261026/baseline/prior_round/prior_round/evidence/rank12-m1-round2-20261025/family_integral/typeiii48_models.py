"""Relative invariant type-III cocycles on (V4+V4) semidirect C3.

H is the graph plane {(u,u)}; all categorical hypotheses are checked exactly.
"""
from pathlib import Path
import itertools,json,sys,time
import numpy as np
BASE=Path(__file__).resolve().parents[2]/'rank12-m1-offline-20261025';OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE));sys.path.insert(0,str(BASE/'sources/work/rank11'));import common
from twisted_h4 import solve,require,MOD
from twisted_h4_matrix import construct

def T(u):return ((u>>1)&1)|((((u&1)^((u>>1)&1)))<<1)
def Tp(u,k):
    for _ in range(k%3):u=T(u)
    return u
def bit(u,i):return(u>>i)&1
def B(u,v):return(bit(u,0)*bit(v,0)+bit(u,0)*bit(v,1)+bit(u,1)*bit(v,1))%2
def avg(a,b,c):return sum(bit(Tp(a,k),0)*bit(Tp(b,k),1)*bit(Tp(c,k),1)for k in range(3))%2

def families():
    E=list(itertools.product(range(3),range(4),range(4)));ix={e:i for i,e in enumerate(E)}
    def mul(a,b):
        k,u,v=a;l,x,y=b;return((k+l)%3,u^Tp(x,k),v^y)
    G=[[ix[mul(a,b)]for b in E]for a in E];H=[ix[(0,u,u)]for u in range(4)];A=np.array(G)
    require(all(np.array_equal(A[A[a,:],:],A[a,A])for a in range(48)),'all group associativity equations')
    bs=np.arange(48)[:,None,None];cs=np.arange(48)[None,:,None];ds=np.arange(48)[None,None,:]
    for bits in itertools.product(range(2),repeat=3):
        def w(a,b,c,bits=bits):
            ka,ua,va=E[a];kb,ub,vb=E[b];kc,uc,vc=E[c];ub=Tp(ub,ka);uc=Tp(uc,ka+kb)
            f0=(B(ua,ub)*bit(vc,0)+bit(va,0)*bit(vb,0)*bit(vc,0))%2
            f1=(B(ua,ub)*bit(vc,1)+bit(va,1)*bit(vb,1)*bit(vc,1))%2
            f2=(avg(ua,ub,uc)+avg(va,vb,vc))%2
            return 4*((bits[0]*f0+bits[1]*f1+bits[2]*f2)%2)
        W=np.array([[[w(a,b,c)for c in range(48)]for b in range(48)]for a in range(48)],dtype=np.int16)
        require(not W[0,:,:].any()and not W[:,0,:].any()and not W[:,:,0].any(),'normalized cocycle')
        for a in range(48):
            delta=W+W[a,A[:,:,None],ds]+W[a,:,:,None]-W[A[a,:,None,None],cs,ds]-W[a,bs,A[None,:,:]]
            require(not(np.mod(delta,MOD).any()),'all 48^4 cocycle equations')
        variables=[(a,b)for a,b in itertools.product(H,repeat=2)if a and b];idx={v:i for i,v in enumerate(variables)};L=[];rhs=[]
        for a,b,c in itertools.product(H,repeat=3):
            row=[0]*len(variables)
            for x,y,z in[(b,c,1),(a,G[b][c],1),(G[a][b],c,-1),(a,b,-1)]:
                if x and y:row[idx[x,y]]+=z
            L.append(row);rhs.append(-w(a,b,c)%MOD)
        sol=solve(L,rhs,first=True)
        if not sol:
            yield G,H,w,None,dict(bits=bits,no_algebra=True);continue
        psi0={v:x for v,x in zip(variables,sol[0])};psi0.update({(a,b):0 for a,b in itertools.product(H,repeat=2)if not a or not b})
        for twist in range(2):
            def psi(a,b,psi0=psi0,twist=twist):return(psi0[a,b]+4*twist*bit(E[a][1],0)*bit(E[b][1],1))%MOD
            yield G,H,w,psi,dict(bits=bits,subgroup_class=twist,normal_coordinates=E,subgroup_cochain=[[a,b,psi(a,b)]for a,b in itertools.product(H,repeat=2)],modulus=MOD,group_order=48)

def main():
    start=time.monotonic();D=json.loads((BASE/'tensors.json').read_text());ids={r['id']for r in json.loads((BASE/'unresolved_families.json').read_text())['records']if r['family']=='D48'};results=[];attempts=[]
    for G,H,w,psi,params in families():
        if psi is None:print(params,flush=True);continue
        R,info=construct(G,H,w,psi=psi);hits=[]
        if R is not None:
            common.validate(R)
            for rid in ids:
                p=common.based_iso(D[rid],R)
                if p is not None:
                    hits.append(rid);results.append(dict(id=rid,status='unitarily_realized',model=dict(name='C((V4+V4) semidirect C3, invariant relative cocycle, graph V4)',constructor='typeiii48_graph_bimodules',parameters=dict(group_table=G,subgroup=H,cocycle=params,objects=info['objects']),model_tensor=R,basis_map_source_to_model=p)))
        attempts.append(dict(parameters=params,info={k:v for k,v in info.items()if k!='objects'},matches=hits));print(params['bits'],params['subgroup_class'],{k:v for k,v in info.items()if k!='objects'},hits,flush=True)
        (OUT/'typeiii48_models.json').write_text(json.dumps(results,indent=2)+'\n');(OUT/'typeiii48_attempts.json').write_text(json.dumps(attempts,indent=2)+'\n')
    print('DONE',len(results),'distinct',len({r['id']for r in results}),time.monotonic()-start)
if __name__=='__main__':main()
