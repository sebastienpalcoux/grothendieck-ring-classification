from pathlib import Path
import json,itertools,time,collections
from feudal_dual import construct,common,need
from grading_cocycles import representatives
BASE=Path(__file__).resolve().parents[2]/'rank12-m1-offline-20261025';OUT=Path(__file__).resolve().parent
D=json.loads((BASE/'tensors.json').read_text());targets={r['id']for r in json.loads((BASE/'unresolved_families.json').read_text())['records']if r['family']=='D40'}
def main():
 rows=collections.defaultdict(list);attempts=[]
 for source in json.loads((OUT/'feudal40_models_sparse.json').read_text()):
  par=source['parameters']
  if par['group']!='D10xC2'or par['sigma']!=[0,1,2,3]:continue
  R=source['tensor'];cert=source['certificate'];p0=par['p'];G=[[(a%4)^(b%4)^(p0 if a//4 and b//4 else 0)+0 for b in range(8)]for a in range(8)]
  G=[[(a%4)^(b%4)^(p0 if a//4 and b//4 else 0) | (4*((a//4)^(b//4)))for b in range(8)]for a in range(8)]
  degree=[a//5 for a in range(20)]+list(range(4,8));need(all(degree[k]==G[degree[a]][degree[b]]for a,b,k in itertools.product(range(24),repeat=3)if R[a][b][k]),'actual abelian universal grading')
  if p0==0:
   terms=[(1,1,1),(2,2,2),(0,1,1),(0,2,2),(1,2,2),(0,1,2)];ws=[]
   for bits in itertools.product(range(2),repeat=6):
    w=[[[2*(sum(v*((a>>i)&1)*((b>>j)&1)*((c>>k)&1)for v,(i,j,k)in zip(bits,terms))%2)for c in range(8)]for b in range(8)]for a in range(8)];ws.append(w)
  else:
   ws,inf=representatives(G,1);print('C4xC2 cocycles',inf,flush=True)
  seen=set()
  for ix,w in enumerate(ws):
   need(w[1][1][1]==0 and all((w[b][c][d]+w[a][G[b][c]][d]+w[a][b][c]-w[G[a][b]][c][d]-w[a][b][G[c][d]])%4==0 for a,b,c,d in itertools.product(range(8),repeat=4)),'all normalized cocycle equations')
   twist=dict(grading_group_table=G,grading=degree,cocycle=w,modulus=4);T,info=construct(R,cert,5,twist=twist);hits=[]
   if T is not None:
    sha=common.sha(T)
    if sha not in seen:
     seen.add(sha)
     for rid in targets:
      p=common.based_iso(D[rid],T)
      if p is not None:hits.append(rid);rows[rid].append(dict(name=f'C2 Morita dual of graded-twisted D10xC2-Liptrap category [p={p0},cocycle={ix}]',constructor='graded_twist_feudal_c2_morita_dual',parameters=dict(feudal_parameters=par,feudal_tensor=R,feudal_certificate=cert,subgroup_generator=5,grading_twist=twist),model_tensor=T,basis_map_source_to_model=p))
   attempts.append(dict(feudal_p=p0,cocycle_index=ix,rank=info['rank'],matches=hits))
   if hits:print('HIT',p0,ix,hits,flush=True)
 (OUT/'feudal_abelian_twist_results.json').write_text(json.dumps([dict(id=rid,family='D40',models=ms)for rid,ms in rows.items()],indent=2)+'\n');(OUT/'feudal_abelian_twist_attempts.json').write_text(json.dumps(attempts,indent=2)+'\n')
 print('DONE',len(attempts),'candidates',len(rows),'resolved IDs',flush=True)
if __name__=='__main__':main()
