from extra_groups import *
def main():
 D=json.loads((BASE/'tensors.json').read_text());U=json.loads((ROOT/'rank12-m1-round2-20261025/unresolved_tensors.json').read_text());ids=[r['id']for r in U if r['exact_dimension_character']['family']=='D48'];rows=[];attempts=[];start=time.monotonic()
 for row in json.loads((OUT/'all48_candidates.json').read_text()):
  G,H=row['table'],row['subgroup'];name=f"SmallGroup{row['smallgroup']}"
  try:R,info=gm.fusion(G,H)
  except ValueError as e:R=None;info=dict(unsupported=str(e))
  hits=[]
  if R is not None:
   for rid in ids:
    p=common.based_iso(D[rid],R)
    if p is not None:hits.append(rid);rows.append(dict(id=rid,status='unitarily_realized',name='C('+name+',H,1)',group=G,subgroup=H,tensor=R,source_to_model=p))
  attempts.append(dict(name=name,subgroup=H,info=info,hits=hits));print(name,H,info,hits,flush=True)
  (OUT/'all48_models.json').write_text(json.dumps(rows,indent=2)+'\n');(OUT/'all48_fusion_attempts.json').write_text(json.dumps(attempts,indent=2)+'\n')
 print('DONE',len(rows),time.monotonic()-start)
if __name__=='__main__':main()
