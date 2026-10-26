from pathlib import Path
import itertools,json,sys,time
BASE=Path(__file__).resolve().parents[2]/'rank12-m1-offline-20261025';OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE));import group_models as gm
import common
from order48_models import conjugacy_subgroups
from twisted_h4_matrix import construct

def groups():
    S=gm.dihedral_table(3)
    C8=[[(a+b)%8 for b in range(8)]for a in range(8)];V8=[[a^b for b in range(8)]for a in range(8)];C4C2=[[((a//2+b//2)%4)*2+((a%2+b%2)%2)for b in range(8)]for a in range(8)]
    Q8=[[((a//2+(-1)**(a%2)*(b//2)+2*(a%2)*(b%2))%4)*2+(a%2+b%2)%2 for b in range(8)]for a in range(8)]
    for name,K in [('C8',C8),('V8',V8),('C4C2',C4C2),('D8',gm.dihedral_table(4)),('Q8',Q8)]:yield'S3x'+name,gm.group_product(S,K)

def main():
    start=time.monotonic();D=json.loads((BASE/'tensors.json').read_text());ids={r['id']for r in json.loads((BASE/'unresolved_families.json').read_text())['records']if r['family']=='D48'};results=[];attempts=[]
    for name,G in groups():
        for H in conjugacy_subgroups(G,4):
            R,info=gm.fusion(G,H);hits=[]
            if R is not None:
                for rid in ids:
                    p=common.based_iso(D[rid],R)
                    if p is not None:
                        hits.append(rid);results.append(dict(id=rid,status='unitarily_realized',model=dict(name=f'C({name},H4)',constructor='group_theoretical',parameters=dict(group_table=G,subgroup=H,cocycle='trivial',subgroup_cochain='trivial'),model_tensor=R,basis_map_source_to_model=p)))
            attempts.append(dict(group=name,subgroup=H,info=info,matches=hits));print(name,H,info,hits,flush=True)
            if R is not None and all(G[h][h]==0 for h in H):
                a,b=H[1:3];labels={0:(0,0),a:(1,0),b:(0,1),G[a][b]:(1,1)};psi=lambda x,y:4*labels[x][0]*labels[y][1]
                M,inf=construct(G,H,lambda a,b,c:0,psi=psi);hits2=[]
                if M is not None:
                    common.validate(M)
                    for rid in ids:
                        p=common.based_iso(D[rid],M)
                        if p is not None:
                            hits2.append(rid);results.append(dict(id=rid,status='unitarily_realized',model=dict(name=f'C({name},H4,nontrivial psi)',constructor='subgroup_twist_h4',parameters=dict(group_table=G,subgroup=H,subgroup_cochain=[[x,y,psi(x,y)]for x,y in itertools.product(H,repeat=2)]),model_tensor=M,basis_map_source_to_model=p)))
                attempts.append(dict(group=name,subgroup=H,psi_class=1,info={k:v for k,v in inf.items()if k!='objects'},matches=hits2));print('PSI',hits2,flush=True)
            (OUT/'product48_models.json').write_text(json.dumps(results,indent=2)+'\n');(OUT/'product48_attempts.json').write_text(json.dumps(attempts,indent=2)+'\n')
    print('DONE',len(results),'distinct',len({r['id']for r in results}),time.monotonic()-start)
if __name__=='__main__':main()
