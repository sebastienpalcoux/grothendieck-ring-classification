"""Exact model replay and left/right stabilizer obstruction certificates."""
from pathlib import Path
import itertools,json,sys,time
from models import BASE,OUT,setup,cocycle,verify_group_cocycle,common
sys.path.insert(0,str(OUT.parent/'family_integral'))
from twisted_h4_matrix import construct

def order(R,g):
    v=0
    for k in range(1,len(R)+1):
        v=R[v][g].index(1)
        if v==0:return k
    raise ValueError('finite invertible order')

def main():
    start=time.monotonic();D=json.loads((BASE/'tensors.json').read_text());rows=json.loads((OUT/'models.json').read_text())['models'];E,G,ss=setup();models=[]
    for row in rows:
        rid=row['id'];m=row['model'];pa=m['parameters'];common.require(pa['group_table']==G and pa['normal_coordinates']==[list(v)for v in E] and pa['subgroup_generator']==ss,'fixed group and subgroup binding')
        w=cocycle(E,pa['relative_cocycle_coefficients'],modulus=8);verify_group_cocycle(G,[0,ss],w,8)
        M,info=construct(G,[0,ss],w);common.require(M is not None,'independent exact balanced bimodule construction');common.validate(M)
        common.require(common.based_iso(M,m['model_tensor'])is not None,'independent algorithm agrees with stored tensor')
        p=m['basis_map_source_to_model'];common.require(p[0]==0 and sorted(p)==list(range(12)),'unit-preserving basis bijection')
        common.require(common.sha(D[rid])==row['tensor_sha256'],'input hash binding')
        common.require(all(D[rid][i][j][k]==m['model_tensor'][p[i]][p[j]][p[k]]for i,j,k in itertools.product(range(12),repeat=3)),'all1728sourcecoefficients')
        models.append(rid)
    exclusions=[]
    for rid,x in [('R12_1_445',3),('R12_1_493',5)]:
        R=D[rid];du=common.dual(R);G0=[g for g in range(12)if sum(R[g][du[g]])==1];X=[i for i in range(12)if i not in G0]
        C1=sorted({R[g][x].index(1)for g in G0});C2=sorted({du[y]for y in C1});common.require(len(G0)==8 and len(C1)==len(C2)==2 and set(C1).isdisjoint(C2)and set(C1+C2)==set(X),'faithful three-component partition')
        deg={i:0 for i in G0}|{i:1 for i in C1}|{i:2 for i in C2}
        common.require(all(not R[i][j][k]or(deg[i]+deg[j])%3==deg[k]for i,j,k in itertools.product(range(12),repeat=3)),'all exact C3 grading equations')
        L=[g for g in G0 if R[g][x][x]];H=[g for g in G0 if R[x][g][x]]
        common.require(len(L)==len(H)==4 and all(R[a][b]==R[b][a]for K in[L,H]for a,b in itertools.product(K,repeat=2)),'abelian stabilizers of orderfour')
        lo=sorted(order(R,g)for g in L);ro=sorted(order(R,g)for g in H);common.require(lo==[1,2,2,2]and ro==[1,2,4,4],'V4 versus C4 character-duality contradiction')
        exclusions.append(dict(id=rid,tensor_sha256=common.sha(R),scope='arbitrary_complex_fusion_category',criterion='invertible_pointed_bimodule_stabilizer_duality',object=x,grading_components=[G0,C1,C2],left_stabilizer=L,right_stabilizer=H,left_orders=lo,right_orders=ro,reference='Galindo-Plavnik arXiv:1407.2783v4 Corollary7.11(2); ENO arXiv:0909.3140 Theorem6.1'))
    (OUT/'exclusions.json').write_text(json.dumps(dict(records=exclusions),indent=2)+'\n')
    out=dict(status='PASS',newly_modeled=['R12_1_428','R12_1_513'],newly_excluded=[r['id']for r in exclusions],all_model_identifications=models,optimized_python=not __debug__,elapsed_seconds=time.monotonic()-start)
    (OUT/('verification_optimized.json'if not __debug__ else'verification.json')).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
