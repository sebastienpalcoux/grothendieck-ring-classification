"""Exact independent source check for the two pointed-bimodule obstructions."""
from itertools import product
import json
from independent_audit import BASE,HERE,dual,require

if __name__=='__main__':
    data=json.loads((BASE/'tensors.json').read_text());out=[]
    for i in (445,493):
        rid=f'R12_1_{i}';R=data[rid];n=len(R);du=dual(R);G=[j for j in range(n)if sum(R[j][du[j]])==1];X=[j for j in range(n)if j not in G];x=min(X)
        unit=lambda a:[int(a==b)for b in range(n)]
        first=sorted({R[g][x].index(1)for g in G});second=sorted(set(X)-set(first));require(len(G)==8 and len(first)==len(second)==2,'pointed neutral8 and two nontrivial components2')
        grade=[0 if j in G else 1 if j in first else 2 for j in range(n)]
        require(all(grade[k]==(grade[a]+grade[b])%3 for a,b,k in product(range(n),repeat=3)if R[a][b][k]),'every fusion coefficient respects faithful C3 grading')
        require(all(grade[du[j]]==(-grade[j])%3 for j in range(n)),'dual grading')
        left=[g for g in G if R[g][x]==unit(x)];right=[g for g in G if R[x][g]==unit(x)]
        def group_orders(H):
            require(0 in H and all(R[a][b].index(1)in H for a,b in product(H,repeat=2)),'actual stabilizer subgroup')
            require(all(R[a][b]==R[b][a]for a,b in product(H,repeat=2)),'abelian stabilizer')
            out=[]
            for a in H:
                z=0;k=0
                while True:
                    z=R[z][a].index(1);k+=1
                    if not z:break
                    require(k<=len(H),'finite order')
                out.append(k)
            return sorted(out)
        lo=group_orders(left);ro=group_orders(right)
        require(lo==[1,2,2,2]and ro==[1,2,4,4],'nonisomorphic V4 and C4 kernels')
        require({R[g][x].index(1)for g in G}=={R[x][g].index(1)for g in G}==set(first),'bitransitive component')
        out.append(dict(id=rid,kind='nonisomorphic_pointed_bimodule_stabilizers',scope='general_complex_fusion_category',grading=grade,neutral_pointed_group=G,object=x,left_stabilizer=left,right_stabilizer=right,left_element_orders=lo,right_element_orders=ro,reference='Galindo–Plavnik arXiv1407.2783v4 Corollary7.11(2), arbitrary omega'))
    receipt=dict(status='PASS',records=out)
    (HERE/'pointed_stabilizers_independent.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
