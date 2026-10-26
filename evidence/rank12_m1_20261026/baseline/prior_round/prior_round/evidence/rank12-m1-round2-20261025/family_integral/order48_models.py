from pathlib import Path
import collections,itertools,json,sys,time
BASE=Path(__file__).resolve().parents[2]/'rank12-m1-offline-20261025';OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE));import group_models as gm
import common
DATA=json.loads((BASE/'tensors.json').read_text())
IDS={r['id']for r in json.loads((BASE/'unresolved_families.json').read_text())['records']if r['family']=='D48'}

def conjugacy_subgroups(G,size):
    inv=[next(j for j in range(len(G))if G[i][j]==0)for i in range(len(G))];seen=set()
    els=[i for i in range(len(G))if size%gm.order(G,i)==0]
    allsubs=set()
    for a,b in itertools.combinations(els,2):
        H=gm.subgroup(G,[a,b])
        if len(H)==size:allsubs.add(tuple(H))
    for H in sorted(allsubs):
        if H in seen:continue
        for g in range(len(G)):seen.add(tuple(sorted(G[G[g][h]][inv[g]]for h in H)))
        yield list(H)

def candidates():
    vals,S=gm.permutation_group(4);C2=[[0,1],[1,0]]
    yield'S4xC2',gm.group_product(S,C2)
    E=[(i,j)for i,p in enumerate(vals)for j in range(4)if sum(p[a]>p[b]for a in range(4)for b in range(a+1,4))%2==j%2];ix={v:i for i,v in enumerate(E)}
    G=[[ix[(S[a][c],(b+d)%4)]for c,d in E]for a,b in E]
    yield'S4_fiber_C4',G
    vals,G=gm.matrix_group(3);yield'GL2_3',G

def main():
    t=time.monotonic();results=[];attempts=[]
    for name,G in candidates():
        for H in conjugacy_subgroups(G,4):
            R,info=gm.fusion(G,H);hits=[]
            if R is not None:
                for rid in IDS:
                    p=common.based_iso(DATA[rid],R)
                    if p is not None:
                        hits.append(rid)
                        results.append(dict(id=rid,status='unitarily_realized',model=dict(name=f'C({name},H4)',constructor='group_theoretical',parameters=dict(group_table=G,subgroup=H,cocycle='trivial',subgroup_cochain='trivial'),model_tensor=R,basis_map_source_to_model=p)))
            attempts.append(dict(group=name,subgroup=H,info=info,matches=hits));print(name,H,info,hits,flush=True)
            (OUT/'order48_models.json').write_text(json.dumps(results,indent=2)+'\n');(OUT/'order48_attempts.json').write_text(json.dumps(attempts,indent=2)+'\n')
    print('DONE',len(results),time.monotonic()-t)
if __name__=='__main__':main()
