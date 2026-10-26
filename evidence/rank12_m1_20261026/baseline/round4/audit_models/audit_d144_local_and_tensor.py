"""Independent local source and forced inverse-tensor audit for R320."""
from itertools import product
import json,sys
import numpy as np
from audit_liptrap import HERE,FIRST,need,audit as liptrap
from audit_d32_nonsplit import scalar_recouplings

def main():
    frozen=HERE/'d144_local_frozen';R=json.loads((frozen/'source_tensor.json').read_text());C=json.loads((frozen/'certificate.json').read_text());receipt=liptrap(R,C);F=scalar_recouplings(R,C)
    S=C['serfs'];M=C['lords'];n=len(R);du=[next(b for b in range(n) if R[a][b][0]) for a in range(n)]
    mul={(a,b):R[a][b].index(1) for a,b in product(range(n),repeat=2) if a in S or b in S}
    L=[0,2,5,7];f=lambda a,b:8 if (a,b)==(5,5) else 0
    need(all((F(a,b,c,mul[mul[a,b],c])-f(b,c)-f(a,mul[b,c])+f(mul[a,b],c)+f(a,b))%16==0 for a,b,c in product(L,repeat=3)),'actual neutral VecV4')
    need([mul[mul[1,a],du[1]] for a in L]==[0,2,7,5],'nontrivial square Brauer class')
    complements=[s for s in S if s not in L and mul[s,s]==0]
    need(len(complements)==2 and {mul[mul[l,complements[0]],du[l]] for l in L}==set(complements),'all reverse complements are neutrally conjugate')
    for s in complements:
        need(all(mul[mul[s,x],s]==x and du[x]!=mul[s,x] for x in M),'actual local support and duality distinction')
    # This is the already-audited m=0 source, not a target-ring guess.
    base=np.array(json.loads((frozen/'known_m0_integral.json').read_text()),dtype=int)
    records=json.loads((frozen/'forced_maps.json').read_text())
    target=np.array(json.loads((frozen/'target_R320.json').read_text()),dtype=int)
    z=[1,0,3,2];out=[]
    for a,b in product([0,1],repeat=2):
        for d in [[2,3,0,1],[3,2,1,0]]:
            actions=[]
            for k in range(8):
                T=np.zeros((4,4),dtype=int)
                for x,y in product(range(4),repeat=2):
                    if k==0:T[x,y]=int(x==y)
                    elif k==1:T[x,y]=int(z[x]==y)
                    elif k==2:T[x,y]=int(x==y)+int(z[x]==y)
                    elif k in [3,4,5]:T[x,y]=1
                    elif k==6:T[x,y]=1 if x//2!=y//2 else int(y==(x^(a if x<2 else b)))
                if k==7:T=actions[6][z]
                actions.append(T)
            tensor=np.zeros((12,12,12),dtype=int);tensor[:8,:8,:8]=base
            for k in range(8):
                for x,y in product(range(4),repeat=2):
                    tensor[k,x+8,y+8]=actions[k][x,y]
                    tensor[x+8,k,y+8]=actions[k][d[x],d[y]]
                    tensor[x+8,y+8,k]=actions[k][d[y],x]
            assoc=np.einsum('ijm,mkl->ijkl',tensor,tensor)-np.einsum('jkm,iml->ijkl',tensor,tensor)
            valid=not np.any(assoc);need(valid==(a!=b),'precisely opposite diagonal blocks are associative')
            row=dict(diagonal_swaps=[a,b],duality=d,valid=valid)
            if valid:
                matches=[r for r in records if r['P_signs']==[1 if a==0 else -1,1 if b==0 else -1] and r['duality']==d]
                need(len(matches)==1,'recorded map parameter binding');p=matches[0]['matches']['R12_1_320']
                need(np.array_equal(tensor,target[np.ix_(p,p,p)]),'all original1728 tensor coefficients')
                row['source_to_target']=p;row['coefficients_checked']=1728
            else:
                w=tuple(int(x) for x in np.argwhere(assoc)[0]);row['associativity_failure']=list(w);row['difference']=int(assoc[w])
            out.append(row)
    receipt.update(neutral_coboundary_equations=64,reverse_complements=complements,forced_nimreps=out,matched_id='R12_1_320',scope='Source/local bridge plus complete forced NIMrep reconstruction; global categorical existence is proved in the accompanying theoretical audit')
    (HERE/'d144_local_and_tensor_independent.json').write_text(json.dumps(receipt,indent=2)+'\n');print('PASS actual local category and all8 forced tensors; four complete R320 matches')

if __name__=='__main__':main()
