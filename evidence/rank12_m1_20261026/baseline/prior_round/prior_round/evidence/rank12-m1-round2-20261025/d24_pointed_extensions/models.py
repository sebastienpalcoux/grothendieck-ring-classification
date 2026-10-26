"""One fixed subgroup and two relative cocycles model four dimension-24 rings."""
from pathlib import Path
import itertools,json,sys,time
import numpy as np
BASE=Path(__file__).resolve().parents[2]/'rank12-m1-offline-20261025';OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE));import twisted_c2_models as old
import common

def T(u):return ((u>>1)&1)|((((u&1)^((u>>1)&1)))<<1)
def Tp(u,k):
    for _ in range(k%3):u=T(u)
    return u
def bit(u,i):return(u>>i)&1
def B(u,v):return(bit(u,0)*bit(v,0)+bit(u,0)*bit(v,1)+bit(u,1)*bit(v,1))%2
def avg(a,b,c):return sum(bit(Tp(a,j),0)*bit(Tp(b,j),1)*bit(Tp(c,j),1)for j in range(3))%2

def setup():
    E=list(itertools.product(range(3),range(4),range(2)));ix={e:i for i,e in enumerate(E)}
    G=[[ix[((a[0]+b[0])%3,a[1]^Tp(b[1],a[0]),a[2]^b[2])]for b in E]for a in E]
    ss=ix[(0,1,1)];return E,G,ss

def cocycle(E,coefficients,modulus=4):
    def w(a,b,c):
        ka,ua,za=E[a];kb,ub,zb=E[b];kc,uc,zc=E[c];x=ua;y=Tp(ub,ka);z=Tp(uc,ka+kb)
        f0=(B(x,y)*zc+za*zb*zc)%2
        f1=(avg(x,y,z)+za*zb*zc)%2
        return(modulus//2)*((coefficients[0]*f0+coefficients[1]*f1)%2)
    return w

def verify_group_cocycle(G,H,w,modulus):
    A=np.array(G,dtype=np.int64);n=len(G)
    common.require(n==24 and np.array_equal(A[0],np.arange(n))and np.array_equal(A[:,0],np.arange(n)),'group unit and order')
    common.require(all(np.array_equal(A[A[a,:],:],A[a,A])for a in range(n)),'all group associativity equations')
    common.require(all(any(G[a][b]==G[b][a]==0 for b in range(n))for a in range(n)),'all group inverses')
    common.require(len(H)==2 and H[0]==0 and G[H[1]][H[1]]==0,'actual C2 subgroup')
    W=np.array([[[w(a,b,c)for c in range(n)]for b in range(n)]for a in range(n)],dtype=np.int16)
    common.require(not W[0,:,:].any()and not W[:,0,:].any()and not W[:,:,0].any(),'normalized cocycle')
    bs=np.arange(n)[:,None,None];cs=np.arange(n)[None,:,None];ds=np.arange(n)[None,None,:]
    for a in range(n):
        delta=W+W[a,A[:,:,None],ds]+W[a,:,:,None]-W[A[a,:,None,None],cs,ds]-W[a,bs,A[None,:,:]]
        common.require(not(np.mod(delta,modulus).any()),'all 24^4 cocycle equations')
    common.require(all(w(a,b,c)%modulus==0 for a,b,c in itertools.product(H,repeat=3)),'trivial exact restriction to subgroup')
    return W

def main():
    start=time.monotonic();D=json.loads((BASE/'tensors.json').read_text());E,G,ss=setup();expected={(0,0):'R12_1_351',(0,1):'R12_1_513',(1,0):'R12_1_428',(1,1):'R12_1_597'};rows=[]
    for coeff,rid in expected.items():
        w=cocycle(E,coeff);verify_group_cocycle(G,[0,ss],w,4);R,info=old.construct(G,ss,w);common.require(R is not None,'complete scalar stabilizer bimodule construction');common.validate(R)
        p=common.based_iso(D[rid],R);common.require(p is not None,'exact expected input identification')
        rows.append(dict(id=rid,status='unitarily_realized',tensor_sha256=common.sha(D[rid]),model=dict(name='C(A4 x C2, relative invariant cocycle, diagonal C2)',constructor='a4c2_relative_cocycle_bimodules',parameters=dict(group_table=G,normal_coordinates=E,subgroup_generator=ss,relative_cocycle_coefficients=list(coeff),phase_modulus=4,subgroup_cochain='trivial',objects=info['objects']),model_tensor=R,basis_map_source_to_model=p)))
    out=dict(models=rows,new_model_ids=['R12_1_428','R12_1_513'],independent_alternative_model_ids=['R12_1_351','R12_1_597'],elapsed_seconds=time.monotonic()-start,online_revision_performed=False)
    (OUT/'models.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items()if k!='models'},indent=2))
if __name__=='__main__':main()
