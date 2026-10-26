from pathlib import Path
import itertools,json,sys,time
BASE=Path(__file__).resolve().parents[2]/'rank12-m1-offline-20261025';OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE));import group_models as gm
import common
from twisted_h4 import construct,MOD
from order48_models import candidates

def schur_cover():
    vals,M=gm.matrix_group(3);ps,S=gm.permutation_group(4);pindex={p:i for i,p in enumerate(ps)}
    points=[(1,0),(0,1),(1,1),(1,2)];ptindex={p:i for i,p in enumerate(points)}
    def normalize(a):
        c=pow(a[0]if a[0]else a[1],-1,3);return(a[0]*c%3,a[1]*c%3)
    projections=[]
    for a,b,c,d in vals:
        projections.append(pindex[tuple(ptindex[normalize(((a*x+b*y)%3,(c*x+d*y)%3))]for x,y in points)])
    require=common.require;require(all(projections[M[a][b]]==S[projections[a]][projections[b]]for a,b in itertools.product(range(48),repeat=2)),'Schur cover quotient')
    lifts=[projections.index(i)for i in range(24)];beta=[[int(M[lifts[a]][lifts[b]]!=lifts[S[a][b]])for b in range(24)]for a in range(24)]
    require(all((beta[b][c]+beta[a][S[b][c]]-beta[S[a][b]][c]-beta[a][b])%2==0 for a,b,c in itertools.product(range(24),repeat=3)),'all Schur cocycle equations')
    return ps,S,beta

def families():
    ps,S,beta=schur_cover();parity=[sum(p[i]>p[j]for i in range(4)for j in range(i+1,4))%2 for p in ps]
    old=json.loads((OUT/'order48_models.json').read_text())
    for row in old:
        parms=row['model']['parameters'];G=parms['group_table'];H=parms['subgroup'];name=row['model']['name'];fiber='fiber'in name
        if fiber:
            q=[(parity[a//2]+2*(a%2))%4 for a in range(48)];Q=[[ (a+b)%4 for b in range(4)]for a in range(4)];chars=[[a%2 for a in q]]
        else:
            q=[2*parity[a//2]+a%2 for a in range(48)];Q=[[a^b for b in range(4)]for a in range(4)];chars=[[a//2 for a in q],[a%2 for a in q]]
        common.require(all(q[G[a][b]]==Q[q[a]][q[b]]for a,b in itertools.product(range(48),repeat=2)),'adaptation quotient')
        common.require({q[h]for h in H}==set(range(4)),'subgroup section isomorphism')
        section={q[h]:h for h in H};B=[[ (beta[a//2][b//2]-beta[section[q[a]]//2][section[q[b]]//2])%2 for b in range(48)]for a in range(48)]
        common.require(all(B[a][b]==0 for a,b in itertools.product(H,repeat=2)),'adapted 2-cocycle restriction')
        common.require(all((B[b][c]+B[a][G[b][c]]-B[G[a][b]][c]-B[a][b])%2==0 for a,b,c in itertools.product(range(48),repeat=3)),'all adapted 2-cocycle equations')
        for bits in itertools.product(range(2),repeat=len(chars)):
            lam=[sum(bit*ch[a]for bit,ch in zip(bits,chars))%2 for a in range(48)]
            common.require(all(lam[G[a][b]]==(lam[a]+lam[b])%2 for a,b in itertools.product(range(48),repeat=2)),'cup-product character homomorphism')
            def w(a,b,c,lam=lam,B=B):return 4*lam[a]*B[b][c]
            yield name,G,H,w,dict(modulus=8,cup_character=lam,adapted_schur_cocycle=B,character_coefficients=bits)

def main():
    start=time.monotonic();DATA=json.loads((BASE/'tensors.json').read_text());ids={r['id']for r in json.loads((BASE/'unresolved_families.json').read_text())['records']if r['family']=='D48'};results=[];attempts=[]
    for name,G,H,w,params in families():
        R,info=construct(G,H,w);hits=[]
        if R is not None:
            common.validate(R)
            for rid in ids:
                p=common.based_iso(DATA[rid],R)
                if p is not None:
                    hits.append(rid);results.append(dict(id=rid,status='unitarily_realized',model=dict(name=name+', adapted Schur cup cocycle',constructor='twisted_group_theoretical_h4',parameters=dict(group_table=G,subgroup=H,cocycle=params,objects=info['objects']),model_tensor=R,basis_map_source_to_model=p)))
        attempts.append(dict(name=name,coefficients=params['character_coefficients'],info={k:v for k,v in info.items()if k!='objects'},matches=hits));print(name,params['character_coefficients'],{k:v for k,v in info.items()if k!='objects'},hits,flush=True)
        (OUT/'twisted48_models.json').write_text(json.dumps(results,indent=2)+'\n');(OUT/'twisted48_attempts.json').write_text(json.dumps(attempts,indent=2)+'\n')
    print('DONE',len(results),'distinct',len({r['id']for r in results}),time.monotonic()-start)
if __name__=='__main__':main()
