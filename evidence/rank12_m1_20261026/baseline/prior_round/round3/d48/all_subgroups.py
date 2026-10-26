from extra_groups import *
from order48_models import candidates
from product48_models import groups as products

def all_subgroups(G):
 n=len(G);inv=[next(j for j in range(n)if G[i][j]==0)for i in range(n)];seen=set();queue=[(0,)]
 for H in queue:
  if H in seen:continue
  seen.add(H)
  for a in range(n):
   if a in H:continue
   K=tuple(gm.subgroup(G,list(H)+[a]))
   if len(K)>16 or len(K)not in [1,2,3,4,6,8,12,16]:continue
   key=min(tuple(sorted(G[G[g][h]][inv[g]]for h in K))for g in range(n))
   if key not in seen and key not in queue:queue.append(key)
  yield list(H)

def main():
 D=json.loads((BASE/'tensors.json').read_text());U=json.loads((ROOT/'rank12-m1-round2-20261025/unresolved_tensors.json').read_text());ids=[r['id']for r in U if r['exact_dimension_character']['family']=='D48'];rows=[];attempts=[];start=time.monotonic()
 for name,G in itertools.chain(groups(),candidates(),products()):
  for H in all_subgroups(G):
   if len(H)not in [8,12,16]:continue
   try:R,info=gm.fusion(G,H)
   except ValueError as e:R=None;info=dict(unsupported=str(e))
   hits=[]
   if R is not None:
    for rid in ids:
     p=common.based_iso(D[rid],R)
     if p is not None:hits.append(rid);rows.append(dict(id=rid,status='unitarily_realized',name='C('+name+',H,1)',group=G,subgroup=H,tensor=R,source_to_model=p))
   attempts.append(dict(name=name,subgroup=H,info=info,hits=hits));print(name,H,info,hits,flush=True)
   (OUT/'all_subgroup_models.json').write_text(json.dumps(rows,indent=2)+'\n');(OUT/'all_subgroup_attempts.json').write_text(json.dumps(attempts,indent=2)+'\n')
 print('DONE',len(rows),time.monotonic()-start)
if __name__=='__main__':main()
