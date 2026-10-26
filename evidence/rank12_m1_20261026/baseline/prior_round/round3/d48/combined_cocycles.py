from extra_groups import *
from transfer48_models import families as transfer
from twisted48_models import families as cup
from twisted_h4_matrix import construct

def main():
 D=json.loads((BASE/'tensors.json').read_text());U=json.loads((ROOT/'rank12-m1-round2-20261025/unresolved_tensors.json').read_text());ids=[r['id']for r in U if r['exact_dimension_character']['family']=='D48'];rows=[];attempts=[];start=time.monotonic();cups=list(cup())
 for name,G,H,w,psi,params in transfer():
  for name2,G2,H2,v,par2 in cups:
   if name2!=name:continue
   W=lambda a,b,c:(w(a,b,c)+v(a,b,c))%8
   R,info=construct(G,H,W,psi=psi);hits=[]
   if R is not None:
    common.validate(R)
    for rid in ids:
     p=common.based_iso(D[rid],R)
     if p is not None:hits.append(rid);rows.append(dict(id=rid,status='unitarily_realized',name=name+' combined transfer cup',group=G,subgroup=H,tensor=R,source_to_model=p,transfer=params,cup=par2))
   attempts.append(dict(name=name,transfer_bits=params['transfer_generator_bits'],subgroup_class=params['subgroup_class'],cup_bits=par2['character_coefficients'],info={k:v for k,v in info.items()if k!='objects'},hits=hits));print(name,params['transfer_generator_bits'],params['subgroup_class'],par2['character_coefficients'],{k:v for k,v in info.items()if k!='objects'},hits,flush=True)
   (OUT/'combined_models.json').write_text(json.dumps(rows,indent=2)+'\n');(OUT/'combined_attempts.json').write_text(json.dumps(attempts,indent=2)+'\n')
 print('DONE',len(rows),time.monotonic()-start)
if __name__=='__main__':main()
