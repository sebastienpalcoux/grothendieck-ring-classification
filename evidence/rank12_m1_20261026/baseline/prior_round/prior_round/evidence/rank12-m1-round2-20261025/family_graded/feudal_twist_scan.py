from pathlib import Path
import json,sys,itertools,collections,time
from feudal_dual import construct,common,need
BASE=Path(__file__).resolve().parents[2]/'rank12-m1-offline-20261025';OUT=Path(__file__).resolve().parent
D=json.loads((BASE/'tensors.json').read_text());targets={r['id']for r in json.loads((BASE/'unresolved_families.json').read_text())['records']if r['family']=='D40'}
def main():
 source=next(r for r in json.loads((OUT/'feudal40_models_sparse.json').read_text())if r['parameters']['group']=='F20');R=source['tensor'];cert=source['certificate'];c=10;z=json.loads((OUT/'d8_cocycles.json').read_text());G=z['group_table'];degree=[a//5 for a in range(20)]+list(range(4,8));need(all(degree[k]==G[degree[a]][degree[b]]for a,b,k in itertools.product(range(24),repeat=3)if R[a][b][k]),'actual D8 grading')
 rows=collections.defaultdict(list);attempts=[];seen=set()
 for i,w in enumerate(z['representatives']):
  start=time.monotonic();twist=dict(grading_group_table=G,grading=degree,cocycle=w,modulus=4);T,info=construct(R,cert,c,twist=twist);hits=[]
  if T is not None:
   sha=common.sha(T)
   seen.add(sha)
   for rid in targets:
    p=common.based_iso(D[rid],T)
    if p is not None:hits.append(rid);rows[rid].append(dict(name=f'C2 Morita dual of D8-twisted F20-Liptrap category [cocycle {i}]',constructor='graded_twist_feudal_c2_morita_dual',parameters=dict(feudal_parameters=source['parameters'],feudal_tensor=R,feudal_certificate=cert,subgroup_generator=c,grading_twist=twist),model_tensor=T,basis_map_source_to_model=p))
  need(len(hits)==1,'every exhaustive relative twist has one identified source ring')
  attempts.append(dict(cocycle_index=i,rank=info['rank'],matches=hits,model_tensor_sha256=common.sha(T),seconds=time.monotonic()-start));print(i,info['rank'],hits,time.monotonic()-start,flush=True)
 (OUT/'feudal_twist_results.json').write_text(json.dumps([dict(id=rid,family='D40',models=ms)for rid,ms in rows.items()],indent=2)+'\n');(OUT/'feudal_twist_attempts.json').write_text(json.dumps(attempts,indent=2)+'\n')
if __name__=='__main__':main()
